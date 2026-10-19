#!/usr/bin/env python3
"""Share one repository skill between Claude Code and Codex (macOS/Linux).

Dry-run by default. Add --apply to install/link. No network, paid calls, client
configuration changes, Git commits, or modifications to Blender assets.
Existing skill contents take precedence over the supplied archive.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile
from zipfile import BadZipFile, ZipFile

NAME = "feltwillow-blender-production"
RELATIVE_TARGET = "../../.claude/skills/" + NAME
MAX_BYTES = 25 * 1024 * 1024


def present(path: Path) -> bool:
    return os.path.lexists(path)


def check_skill(folder: Path) -> None:
    entry = folder / "SKILL.md"
    if folder.is_symlink() or not folder.is_dir() or entry.is_symlink() or not entry.is_file():
        raise ValueError(f"Expected an actual skill directory with a regular SKILL.md: {folder}")
    text = entry.read_text(encoding="utf-8")
    front = text.split("---", 2)
    if len(front) < 3 or front[0].strip() or not re.search(
        rf"(?m)^name:\s*{re.escape(NAME)}\s*$", front[1]
    ):
        raise ValueError(f"Unexpected skill name/frontmatter in {entry}")


def fingerprint(folder: Path) -> dict[str, tuple]:
    """Compare bytes and permissions, including hidden files; never follow links."""
    result: dict[str, tuple] = {}
    for parent, dirs, files in os.walk(folder, followlinks=False):
        for name in sorted(dirs + files):
            path = Path(parent) / name
            rel = path.relative_to(folder).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("link", os.readlink(path))
            elif stat.S_ISDIR(mode):
                result[rel] = ("directory", stat.S_IMODE(mode))
            elif stat.S_ISREG(mode):
                result[rel] = ("file", stat.S_IMODE(mode), hashlib.sha256(path.read_bytes()).hexdigest())
            else:
                raise ValueError(f"Unsupported special file: {path}")
    return result


def check_archive(archive: Path) -> None:
    if not archive.is_file() or archive.stat().st_size > MAX_BYTES:
        raise ValueError(f"Archive missing or larger than 25 MiB: {archive}")
    with ZipFile(archive) as z:
        entries = z.infolist()
        if sum(i.file_size for i in entries) > MAX_BYTES:
            raise ValueError("Expanded archive exceeds 25 MiB; refusing extraction.")
        names: set[str] = set()
        for item in entries:
            raw = item.filename
            path = PurePosixPath(raw)
            parts = raw.rstrip("/").split("/")
            if (path.is_absolute() or "\\" in raw or any(p in ("", ".", "..") for p in parts)
                    or not parts or parts[0] != NAME or raw in names):
                raise ValueError(f"Unsafe, duplicate, or unexpected ZIP entry: {raw}")
            kind = stat.S_IFMT(item.external_attr >> 16)
            if kind not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise ValueError(f"Link/special ZIP entry is not permitted: {raw}")
            names.add(raw)
        entrypoints = [n for n in names if PurePosixPath(n).name.upper() == "SKILL.MD"]
        if entrypoints != [f"{NAME}/SKILL.md"]:
            raise ValueError("Archive must contain exactly one skill in the expected folder.")
        required = ("SKILL.md", "agents/openai.yaml", "references/installation.md")
        for name in required:
            if f"{NAME}/{name}" not in names:
                raise ValueError(f"Archive is missing {name}")
        front = z.read(f"{NAME}/SKILL.md").decode("utf-8").split("---", 2)
        if len(front) < 3 or front[0].strip() or not re.search(
            rf"(?m)^name:\s*{re.escape(NAME)}\s*$", front[1]
        ):
            raise ValueError("Unexpected archive skill name/frontmatter.")
        bad = z.testzip()
        if bad:
            raise ValueError(f"Corrupt archive entry: {bad}")


def setup(repo: Path, archive: Path, backup_root: Path, apply: bool = False) -> None:
    repo = repo.expanduser().resolve(strict=True)
    archive = archive.expanduser().resolve()
    backup_root = backup_root.expanduser().resolve()
    if not repo.is_dir() or not (repo / ".git").exists():
        raise ValueError(f"Not a Git checkout root (a .git directory or worktree file is required): {repo}")
    if backup_root == repo or repo in backup_root.parents:
        raise ValueError("Backup directory must be outside the repository and its skills discovery paths.")
    # Never silently write through a linked parent directory.
    for rel in (".claude", ".claude/skills", ".agents", ".agents/skills"):
        path = repo / rel
        if path.is_symlink() or (present(path) and not path.is_dir()):
            raise ValueError(f"Parent is a symlink or non-directory; inspect it manually first: {path}")
    source = repo / ".claude/skills" / NAME
    alias = repo / ".agents/skills" / NAME
    if source.is_symlink():
        raise ValueError(f"Claude's skill is already a symlink; inspect its existing source before changing it: {source}")
    source_present = present(source)
    alias_present = present(alias)
    if source_present:
        check_skill(source)
    if alias_present and alias.is_symlink():
        if alias.resolve(strict=False) != source:
            raise ValueError(f"Codex entry points somewhere else; no changes made: {alias} -> {os.readlink(alias)}")
    elif alias_present:
        check_skill(alias)

    duplicate = source_present and alias_present and not alias.is_symlink()
    if duplicate and fingerprint(source) != fingerprint(alias):
        raise ValueError(
            "The Claude and Codex folders differ. Nothing was changed. Compare and merge them first:\n"
            f"  {source}\n  {alias}\n"
            "Keep unique edits; do not overwrite either folder with the ZIP."
        )
    mode = "keep" if source_present else "migrate" if alias_present and not alias.is_symlink() else "extract"
    if mode == "extract":
        check_archive(archive)
    print(f"Source of truth: {source}")
    print(f"Codex link:      {alias} -> {RELATIVE_TARGET}")
    print({"keep": "Preserve the installed Claude skill unchanged (this is not an upgrade).",
           "migrate": "Move the existing Codex skill to Claude's folder, preserving its contents.",
           "extract": f"Install the skill from {archive}."}[mode])
    if duplicate:
        print(f"Move the identical Codex duplicate to a timestamped backup under {backup_root}.")
    if not apply:
        print("DRY RUN: no changes made. Add --apply to perform this setup.")
        return

    source.parent.mkdir(parents=True, exist_ok=True)
    alias.parent.mkdir(parents=True, exist_ok=True)
    moved_backup = None
    new_source = False
    if mode == "migrate":
        alias.rename(source)
    elif mode == "extract":
        with tempfile.TemporaryDirectory(prefix=".feltwillow-install-", dir=source.parent) as temp:
            with ZipFile(archive) as z:
                z.extractall(temp)
            extracted = Path(temp) / NAME
            check_skill(extracted)
            extracted.rename(source)
            new_source = True
    if duplicate:
        backup_root.mkdir(parents=True, exist_ok=True)
        holder = Path(tempfile.mkdtemp(prefix=NAME + "-", dir=backup_root))
        moved_backup = holder / "codex-copy"
        shutil.move(str(alias), str(moved_backup))
        print(f"Identical duplicate backed up at: {moved_backup}")
    try:
        if not present(alias):
            alias.symlink_to(RELATIVE_TARGET, target_is_directory=True)
        if not os.path.samefile(source / "SKILL.md", alias / "SKILL.md"):
            raise ValueError("Verification failed: Claude and Codex do not resolve to the same SKILL.md.")
    except Exception:
        # Restore a migrated/duplicate directory if link creation fails.
        if not present(alias) and moved_backup is not None:
            shutil.move(str(moved_backup), str(alias))
        elif not present(alias) and mode == "migrate":
            source.rename(alias)
        if new_source:
            print(f"The new skill was retained at {source}; inspect the link failure before retrying.", file=sys.stderr)
        raise
    print("VERIFIED: both paths resolve to the exact same SKILL.md file.")
    print("Edit only the source-of-truth folder. Existing Blender/fal/MCP configuration was not changed.")
    print("Start fresh Claude Code and Codex sessions in this checkout to test discovery.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="Root of the existing Feltwillow Git checkout")
    parser.add_argument("--archive", type=Path, default=Path(__file__).with_name("skill.zip"),
                        help="Skill ZIP; needed only when neither client has an existing installation")
    parser.add_argument("--backup-root", type=Path,
                        default=Path.home() / ".local/share/feltwillow/skill-backups")
    parser.add_argument("--apply", action="store_true", help="Apply changes; omit for a read-only dry run")
    args = parser.parse_args()
    try:
        setup(args.repo, args.archive, args.backup_root, args.apply)
    except (ValueError, OSError, BadZipFile, UnicodeError, RuntimeError) as error:
        print(f"STOP: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
