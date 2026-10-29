"""Audit retained V7 source bytes in the worktree and an actual Git tree."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from production.audio_visual_plan import local


INDEX = Path("stories/lion_and_mouse_v7/history/retained_sources/INDEX.json")
PERFORMANCE = Path("stories/lion_and_mouse_v7/character_performance_library.json")


def performance_references(value):
    """Find exact file references without treating arbitrary prose as authority."""
    if isinstance(value, dict):
        if (isinstance(value.get("path"), str) and isinstance(value.get("sha256"), str)):
            yield value["path"], value["sha256"]
        for item in value.values():
            yield from performance_references(item)
    elif isinstance(value, list):
        for item in value:
            yield from performance_references(item)


def audit(root: Path, tree: str = "HEAD") -> dict:
    root = root.resolve()
    index = json.loads(local(root, INDEX.as_posix()).read_text())
    if index.get("schema") != "feltwillow.retained-sources.v1":
        raise ValueError("unsupported retained-source index")
    findings = []
    for logical, record in sorted(index["files"].items()):
        archived = record["archived_path"]
        target = local(root, archived)
        if any(part.is_symlink() for part in (root / archived, *(root / archived).parents) if part != root):
            raise ValueError(f"symlink in archived path: {archived}")
        expected = record["sha256"]
        actual = hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else None
        blob = subprocess.run(["git", "show", f"{tree}:{archived}"], cwd=root,
                              capture_output=True, check=False)
        tree_sha = hashlib.sha256(blob.stdout).hexdigest() if blob.returncode == 0 else None
        status = ("MISSING" if actual is None else
                  "HASH_MISMATCH" if actual != expected else
                  "UNTRACKED_IN_GIT" if tree_sha is None else
                  "GIT_HASH_MISMATCH" if tree_sha != expected else "PRESENT_AND_MATCHED")
        findings.append({"logical_path": logical, "archived_path": archived,
                         "expected_sha256": expected, "worktree_sha256": actual,
                         "git_tree_sha256": tree_sha, "status": status})
    references = []
    performance_path = local(root, PERFORMANCE.as_posix())
    if not performance_path.is_file():
        raise ValueError(f"missing performance registry: {PERFORMANCE}")
    if performance_path.is_file():
        for logical, expected in sorted(set(performance_references(json.loads(performance_path.read_text())))):
            archived = index["files"].get(logical, {}).get("archived_path", logical)
            target = local(root, archived)
            if any(part.is_symlink() for part in (root / archived, *(root / archived).parents) if part != root):
                raise ValueError(f"symlink in performance path: {archived}")
            actual = hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else None
            blob = subprocess.run(["git", "show", f"{tree}:{archived}"], cwd=root,
                                  capture_output=True, check=False)
            tree_sha = hashlib.sha256(blob.stdout).hexdigest() if blob.returncode == 0 else None
            status = ("MISSING" if actual is None else
                      "HASH_MISMATCH" if actual != expected else
                      "UNTRACKED_IN_GIT" if tree_sha is None else
                      "GIT_HASH_MISMATCH" if tree_sha != expected else "PRESENT_AND_MATCHED")
            references.append({"logical_path": logical, "resolved_path": archived,
                               "expected_sha256": expected, "worktree_sha256": actual,
                               "git_tree_sha256": tree_sha, "status": status})
    return {"schema": "feltwillow.retained-source-audit.v1", "git_tree": tree,
            "index_sha256": hashlib.sha256(local(root, INDEX.as_posix()).read_bytes()).hexdigest(),
            "status": "PASS" if all(f["status"] == "PRESENT_AND_MATCHED" for f in findings + references) else "BLOCKED",
            "findings": findings, "performance_references": references}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--tree", default="HEAD")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = audit(args.repo, args.tree)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2) + "\n")
    from collections import Counter
    print(json.dumps({"status": result["status"], "index_sha256": result["index_sha256"],
                      "archive_counts": dict(Counter(f["status"] for f in result["findings"])),
                      "performance_reference_counts": dict(Counter(f["status"] for f in result["performance_references"]))}, indent=2))
    raise SystemExit(result["status"] != "PASS")


if __name__ == "__main__":
    main()
