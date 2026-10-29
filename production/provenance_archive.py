"""Audit retained V7 source bytes in the worktree and an actual Git tree."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from production.audio_visual_plan import local


INDEX = Path("stories/lion_and_mouse_v7/history/retained_sources/INDEX.json")


def audit(root: Path, tree: str = "HEAD") -> dict:
    root = root.resolve()
    index = json.loads(local(root, INDEX.as_posix()).read_text())
    if index.get("schema") != "feltwillow.retained-sources.v1":
        raise ValueError("unsupported retained-source index")
    findings = []
    for logical, record in sorted(index["files"].items()):
        archived = record["archived_path"]
        target = local(root, archived)
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
    return {"schema": "feltwillow.retained-source-audit.v1", "git_tree": tree,
            "index_sha256": hashlib.sha256(local(root, INDEX.as_posix()).read_bytes()).hexdigest(),
            "status": "PASS" if all(f["status"] == "PRESENT_AND_MATCHED" for f in findings) else "BLOCKED",
            "findings": findings}


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
                      "counts": dict(Counter(f["status"] for f in result["findings"]))}, indent=2))
    raise SystemExit(result["status"] != "PASS")


if __name__ == "__main__":
    main()
