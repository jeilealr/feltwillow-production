#!/usr/bin/env python3
"""Copy exact-hash tracked files to a verified ZIP outside the repo. NEVER deletes files.

This is a backup tool, NOT an approval oracle or git-remove command.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from zipfile import ZipFile, ZIP_STORED

from cleanup_audit import git, repo_root, sha256, tracked, validate_path


def verify_manifest(root: Path, manifest: dict) -> list[tuple[str, Path, str]]:
    if manifest.get("schema") != "feltwillow.cleanup-archive.v1":
        raise ValueError("Unsupported archive manifest schema")
    branch = git(root, "branch", "--show-current").stdout.decode().strip()
    head = git(root, "rev-parse", "HEAD").stdout.decode().strip()
    if not branch or manifest.get("source_branch") != branch or manifest.get("source_head") != head:
        raise ValueError("Manifest branch/HEAD mismatch; refresh the review and owner decision")
    # Prevent packaging transient modified tracked files under old approved hashes.
    if git(root, "diff", "--quiet", check=False).returncode != 0 or git(root, "diff", "--cached", "--quiet", check=False).returncode != 0:
        raise ValueError("Tracked working tree/index is dirty; archive only a reviewed stable snapshot")
    rows = manifest.get("files")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Manifest must list nonempty files")
    known = set(tracked(root))
    seen: set[str] = set()
    results = []
    for item in rows:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise ValueError("Every entry must have only path and sha256")
        rel, expected = item["path"], item["sha256"]
        if not isinstance(rel, str) or rel in seen:
            raise ValueError(f"Duplicate or invalid archive path: {rel}")
        seen.add(rel)
        if rel not in known:
            raise ValueError(f"Archive path is not tracked: {rel}")
        if not isinstance(expected, str) or not re.fullmatch("[0-9a-f]{64}", expected):
            raise ValueError(f"Invalid SHA-256 for {rel}")
        path = validate_path(root, rel)
        if sha256(path) != expected:
            raise ValueError(f"Source hash mismatch: {rel}")
        results.append((rel, path, expected))
    return results


def sha_stream(stream) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(chunk)
    return digest.hexdigest()


def archive(root: Path, manifest_path: Path, dest: Path) -> dict:
    root = root.resolve(strict=True)
    manifest_raw = manifest_path.read_bytes()
    manifest = json.loads(manifest_raw)
    items = verify_manifest(root, manifest)
    if dest.suffix.lower() != ".zip":
        raise ValueError("External archive must use .zip")
    dest = dest.expanduser().resolve()
    if dest == root or root in dest.parents:
        raise ValueError("Archive must live OUTSIDE repository (and .git)")
    if dest.exists():
        raise FileExistsError("Archive already exists; refuse overwrite")
    if not dest.parent.is_dir():
        raise FileNotFoundError(f"Create external destination directory yourself first: {dest.parent}")
    embedded = {
        "schema": "feltwillow.verified-external-archive.v1",
        "source_manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "source_branch": manifest["source_branch"],
        "source_head": manifest["source_head"],
        "archived_utc": datetime.now(timezone.utc).isoformat(),
        "files": manifest["files"],
        "warning": "Backup only. Never grants owner deletion/selection authority."
    }
    tmpname = None
    try:
        with tempfile.NamedTemporaryFile(prefix=".feltwillow-archive-", suffix=".tmp", dir=dest.parent, delete=False) as t:
            tmpname = Path(t.name)
        with ZipFile(tmpname, "w", compression=ZIP_STORED, allowZip64=True) as z:
            for rel, path, expected in items:
                if sha256(path) != expected:
                    raise ValueError(f"Source changed during archive: {rel}")
                z.write(path, arcname=rel)
                if sha256(path) != expected:
                    raise ValueError(f"Source changed during archive write: {rel}")
            z.writestr("FELTWILLOW_ARCHIVE_MANIFEST.json", json.dumps(embedded, indent=2) + "\n")
        with ZipFile(tmpname) as z:
            if set(z.namelist()) != {rel for rel, _, _ in items} | {"FELTWILLOW_ARCHIVE_MANIFEST.json"}:
                raise ValueError("Archive members mismatch")
            for rel, _, expected in items:
                with z.open(rel) as stream:
                    if sha_stream(stream) != expected:
                        raise ValueError(f"Archive extraction checksum mismatch: {rel}")
            actual = json.loads(z.read("FELTWILLOW_ARCHIVE_MANIFEST.json"))
            if actual != embedded:
                raise ValueError("Embedded manifest mismatch")
        # Atomic no-replace publish. Hardlink fails closed if archive already exists.
        os.link(tmpname, dest)
        os.unlink(tmpname)
        tmpname = None
        return {"archive": str(dest), "sha256": sha256(dest), "count": len(items),
                "bytes": dest.stat().st_size, "source_manifest_sha256": embedded["source_manifest_sha256"],
                "status": "VERIFIED_COPY_ONLY_NO_FILES_REMOVED"}
    finally:
        if tmpname is not None:
            tmpname.unlink(missing_ok=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)
    try:
        root = repo_root(args.repo)
        result = archive(root, args.manifest, args.out)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, FileNotFoundError, FileExistsError, RuntimeError, OSError, json.JSONDecodeError) as e:
        print(f"BLOCKED: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
