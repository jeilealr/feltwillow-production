#!/usr/bin/env python3
"""Read-only Feltwillow cleanup inventory and literal-reference leads.

No delete, no git rm, no auto-selection. Python standard library only.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

REVIEW_PREFIX = "stories/lion_and_mouse_v7/review/"
V6_PREFIX = "stories/lion_and_mouse_v6/"
CHRONO_PREFIX = "character/characters/_chrono_probe/"
CANDIDATE_RE = re.compile(r"^(?P<stem>.+)_r(?P<num>\d{2,3})_candidate\.(?P<ext>png|jpe?g|json)$", re.I)
PROTECTED_WORDS = (
    "owner_acceptance", "owner_selection", "owner_approval", "owner_decision",
    "owner_feedback", "owner_selected", "approval_ledger", "acceptance_ledger",
    "selected_use", "scene_use_matrix", "authority_ledger",
)


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    if check and p.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed ({p.returncode}): {p.stderr.decode('utf8', 'replace')[:300]}")
    return p


def repo_root(raw: str) -> Path:
    start = Path(raw).resolve(strict=True)
    top = Path(git(start, "rev-parse", "--show-toplevel").stdout.decode().strip()).resolve()
    if start != top:
        raise ValueError(f"Use the exact Git root for --repo: {top}")
    return top


def tracked(root: Path) -> list[str]:
    data = git(root, "ls-files", "-z", "--cached").stdout
    return sorted({p.decode("utf8", "surrogateescape") for p in data.split(b"\0") if p})


def snapshot(root: Path) -> dict:
    return {
        "branch": git(root, "branch", "--show-current").stdout.decode().strip(),
        "head": git(root, "rev-parse", "HEAD").stdout.decode().strip(),
        "status_porcelain": git(root, "status", "--porcelain=v1", "-z").stdout.decode("utf8", "replace").replace("\0", "\n").strip(),
    }


def validate_path(root: Path, raw: str) -> Path:
    if not isinstance(raw, str) or not raw or "\x00" in raw or "\\" in raw:
        raise ValueError("Path must be a nonempty, relative POSIX Git path")
    path = PurePosixPath(raw)
    if path.is_absolute() or any(part in {".", ".."} for part in path.parts) or raw.startswith("./"):
        raise ValueError(f"Unsafe path: {raw}")
    local = root.joinpath(*path.parts)
    # Walk parent components without resolving through symlinks.
    p = root
    for part in path.parts:
        p = p / part
        if p.is_symlink():
            raise ValueError(f"Symlink path or parent is unsafe: {raw}")
    if not local.is_file():
        raise FileNotFoundError(raw)
    return local


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_protected_evidence(rel: str) -> bool:
    low = rel.lower()
    return any(word in low for word in PROTECTED_WORDS)


def scene_match(rel: str, scenes: set[str]) -> bool:
    if not scenes:
        return True
    return any(re.search(r"(?<![A-Z0-9])" + re.escape(s) + r"[-_/]", rel.upper()) for s in scenes)


def inventory(root: Path, scenes: set[str]) -> dict:
    snap = snapshot(root)
    paths = tracked(root)
    versions: dict[tuple[str, str, str], list[tuple[int, str]]] = defaultdict(list)
    for rel in paths:
        m = CANDIDATE_RE.fullmatch(PurePosixPath(rel).name)
        if m:
            key = (str(PurePosixPath(rel).parent), m.group("stem"), m.group("ext").lower())
            versions[key].append((int(m.group("num")), rel))
    old_rev = {}
    for rows in versions.values():
        if len({n for n, _ in rows}) > 1:
            newest = max(n for n, _ in rows)
            for n, rel in rows:
                if n < newest:
                    old_rev[rel] = newest

    counts, sizes, rows = Counter(), Counter(), []
    group_samples = defaultdict(list)
    total_bytes, unknown_size = 0, 0
    for rel in paths:
        local = root / rel
        try:
            size = local.lstat().st_size
            if local.is_symlink() or not local.is_file():
                category = "PROTECTED_SYMLINK_OR_SPECIAL"
            else:
                category = ""
        except OSError:
            size, category = 0, "MISSING_OR_STAGED"
            unknown_size += 1
        total_bytes += size
        if not category:
            if is_protected_evidence(rel):
                category = "PROTECT_AUTHORITY_EVIDENCE"
            elif rel.startswith(REVIEW_PREFIX):
                category = "REVIEW_HISTORY_DEPENDENCY_CHECK"
            elif rel.startswith(V6_PREFIX):
                category = "LEGACY_V6_DEPENDENCY_CHECK"
            elif rel.startswith(CHRONO_PREFIX):
                category = "CHRONO_PROBE_DEPENDENCY_CHECK"
            elif rel in old_rev and scene_match(rel, scenes):
                category = "OLDER_REVISION_DEPENDENCY_CHECK"
            else:
                continue
        counts[category] += 1
        sizes[category] += size
        row = {"path": rel, "bytes": size, "classification": category,
               "deletion_authorized": False}
        if rel in old_rev:
            row["newest_number_present_not_necessarily_selected"] = old_rev[rel]
        rows.append(row)
        top = rel.split("/")
        key = "/".join(top[:4]) if rel.startswith(REVIEW_PREFIX) else (V6_PREFIX.rstrip("/") if rel.startswith(V6_PREFIX) else CHRONO_PREFIX.rstrip("/") if rel.startswith(CHRONO_PREFIX) else "revision_history")
        if len(group_samples[key]) < 5:
            group_samples[key].append(rel)
    return {
        "schema": "feltwillow.cleanup-inventory.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "READ_ONLY; no file is approved for deletion",
        "snapshot": snap,
        "scenes_revision_filter": sorted(scenes),
        "total_git_tracked_paths": len(paths),
        "total_tracked_worktree_bytes_stat_estimate": total_bytes,
        "missing_or_staged_paths": unknown_size,
        "category_counts": dict(counts),
        "category_bytes": dict(sizes),
        "samples_by_group": dict(group_samples),
        "entries_requiring_investigation": rows,
        "warning": "No approval, dependency closure, exact selected-use resolution, or deletion safety is inferred by this inventory. Missing literal references are not proof of safe removal.",
    }


def safe_write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf8") as f:
        f.write(contents)


def summary_text(data: dict) -> str:
    s = data["snapshot"]
    lines = ["# Feltwillow cleanup inventory — READ ONLY", "", f"Branch: `{s['branch']}`  HEAD: `{s['head']}`", "",
             "**No deletion is authorized.** Full candidate paths are in the JSON inventory.", "",
             f"Git-tracked paths: {data['total_git_tracked_paths']:,}", "",
             "| Candidate class | Files | Approx current bytes |", "|---|---:|---:|"]
    for k, count in sorted(data["category_counts"].items()):
        lines.append(f"| `{k}` | {count:,} | {data['category_bytes'].get(k,0):,} |")
    lines += ["", "## Next steps", "", "Resolve current owner-selected hashes and active sequence uses; check inbound references, tests and reproducibility; obtain exact owner removal approval; create a verified external archive; only then allow scoped `git rm`.", "",
              "`newest_number_present_not_necessarily_selected` is a numeric comparison, **not** an acceptance decision.", "",
              "`git rm` does not reduce Git history size; do not rewrite history or run aggressive GC as part of this cleanup.", ""]
    if s["status_porcelain"]:
        lines += ["## Pre-existing worktree changes (do not touch)", "", "```", s["status_porcelain"][:2500], "```", ""]
    return "\n".join(lines)


def reference_leads(root: Path, raw: str, limit: int = 70) -> dict:
    local = validate_path(root, raw)
    if raw not in set(tracked(root)):
        raise ValueError(f"Not tracked: {raw}")
    name = PurePosixPath(raw).name
    proc = git(root, "grep", "-n", "-I", "-F", "-e", raw, "-e", name, "--", check=False)
    if proc.returncode not in {0, 1}:
        raise RuntimeError(proc.stderr.decode("utf8", "replace")[:400])
    rows = proc.stdout.decode("utf8", "replace").splitlines()
    return {"path": raw, "sha256": sha256(local), "bytes": local.stat().st_size,
            "literal_hits_count": len(rows), "literal_hits_capped": rows[:limit],
            "hits_truncated": len(rows) > limit,
            "conclusion": "REFERENCE LEADS ONLY; no-hit does not prove removable; consult active owner ledgers, resolvers, dynamic paths, tests and source ancestry."}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    inv = sub.add_parser("inventory", help="Read-only inventory; never removes files")
    inv.add_argument("--repo", required=True)
    inv.add_argument("--out", type=Path, required=True)
    inv.add_argument("--scenes", nargs="*", default=[])
    refs = sub.add_parser("refs", help="Targeted SHA and tracked-text reference leads")
    refs.add_argument("--repo", required=True)
    refs.add_argument("--path", required=True)
    args = ap.parse_args(argv)
    try:
        root = repo_root(args.repo)
        if args.cmd == "inventory":
            scenes = {s.upper() for s in args.scenes}
            if any(not re.fullmatch(r"S\d{2}", s) for s in scenes):
                raise ValueError("--scenes requires S01, S08, etc.")
            data = inventory(root, scenes)
            out = args.out.resolve()
            report = out.with_name(out.stem + "_SUMMARY.md")
            if out.exists() or report.exists():
                raise FileExistsError("Inventory paths already exist; use a fresh review revision")
            safe_write(out, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            safe_write(report, summary_text(data))
            print(f"Inventory written: {out} and {report}; NO DELETIONS.\n" + summary_text(data)[:1800])
        else:
            print(json.dumps(reference_leads(root, args.path), indent=2, ensure_ascii=False))
        return 0
    except (ValueError, RuntimeError, FileNotFoundError, FileExistsError, OSError) as e:
        print(f"BLOCKED: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
