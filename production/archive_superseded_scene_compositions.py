"""Move superseded V7 scene PNGs and sidecars to the retained-source archive.

Only an exact-hash owner selection for a newer revision of the same image ID
qualifies an older pair. Historical records keep their original paths; the
existing read-only source_file resolver finds their bytes through INDEX.json.
"""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from production.sequence_plan import selection_catalog


SCENES = Path("character/characters/lion_and_mouse_v7/interactions/scene_compositions")
ARCHIVE = Path("stories/lion_and_mouse_v7/history/retained_sources")
REVISION = re.compile(r"^(S\d\d-L\d\d\d-B\d\d-I\d\d).*_r(\d+)_candidate\.png$")


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def candidates(root, selections):
    """Return old pairs only when a newer selected image is present and valid."""
    selected = {row["image_id"]: row for row in selections if row.get("image_id")}
    result = []
    for png in sorted((root / SCENES).glob("*.png")):
        match = REVISION.fullmatch(png.name)
        if not match or match[1] not in selected:
            continue
        row = selected[match[1]]
        chosen = Path(row["path"])
        chosen_match = REVISION.fullmatch(chosen.name)
        if chosen_match:
            if chosen_match[1] != match[1] or int(chosen_match[2]) <= int(match[2]):
                continue
        elif chosen.is_relative_to(SCENES):
            # A selected scene stored elsewhere may replace all active-folder
            # attempts for that ID; a differently named active candidate may not.
            continue
        if chosen != png.relative_to(root):
            chosen_file = root / chosen
            if not chosen_file.is_file() or digest(chosen_file) != row["sha256"]:
                raise ValueError(f"selected source missing or changed: {chosen}")
        else:
            continue
        sidecar = png.with_suffix(".json")
        if not sidecar.is_file():
            raise ValueError(f"missing sidecar: {sidecar}")
        record = json.loads(sidecar.read_text())
        recorded_id = record.get("image_id")
        recorded_path = record.get("path") or record.get("output_path") or record.get("candidate_path")
        recorded_hash = record.get("sha256") or record.get("output_sha256") or record.get("candidate_sha256")
        if (recorded_id is not None and recorded_id != match[1]) or recorded_path != str(png.relative_to(root)) or recorded_hash != digest(png):
            raise ValueError(f"candidate sidecar mismatch: {sidecar}")
        result.append((png, sidecar))
    return result


def run(root, apply=False):
    root = root.resolve(strict=True)
    if subprocess.run(["git", "branch", "--show-current"], cwd=root, capture_output=True, text=True, check=True).stdout.strip() != "wan-new-image-approach":
        raise ValueError("unexpected branch")
    folder = root / "stories/lion_and_mouse_v7"
    pairs = candidates(root, selection_catalog(folder))
    index_path = root / ARCHIVE / "INDEX.json"
    index = json.loads(index_path.read_text())
    if index.get("schema") != "feltwillow.retained-sources.v1":
        raise ValueError("unexpected archive schema")
    entries = []
    for pair in pairs:
        for source in pair:
            relative = str(source.relative_to(root))
            destination = root / ARCHIVE / "files" / relative
            if relative in index["files"] or destination.exists():
                raise ValueError(f"archive collision: {relative}")
            tracked = subprocess.run(["git", "ls-files", "--error-unmatch", "--", relative], cwd=root, capture_output=True)
            if tracked.returncode:
                raise ValueError(f"untracked source: {relative}")
            unchanged = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", relative], cwd=root)
            if unchanged.returncode:
                raise ValueError(f"uncommitted source change: {relative}")
            entries.append((source, destination, relative, digest(source)))
    if not apply:
        return entries
    for source, destination, relative, sha in entries:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        if digest(destination) != sha:
            raise ValueError(f"archive copy changed: {relative}")
        index["files"][relative] = {"archived_path": str(destination.relative_to(root)), "sha256": sha}
        temp = index_path.with_suffix(".json.tmp")
        temp.write_text(json.dumps(index, indent=2) + "\n")
        temp.replace(index_path)
        source.unlink()
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    entries = run(args.repo, args.apply)
    print(json.dumps({"mode": "apply" if args.apply else "dry_run", "pairs": len(entries) // 2,
                      "files": len(entries), "bytes": sum((p.stat().st_size if p.exists() else (d.stat().st_size)) for p, d, _, _ in entries),
                      "paths": [relative for _, _, relative, _ in entries]}, indent=2))


if __name__ == "__main__":
    main()
