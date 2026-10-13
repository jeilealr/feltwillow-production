#!/usr/bin/env python3
"""Adopt a new, separately saved keyframe revision and rebuild its boundary plan.

The prior image and its review/rejection history remain untouched. This changes
the active candidate, not its approval state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import struct
import tempfile
from pathlib import Path

import keyframe_plan
import video_boundary_plan

REPO = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as source:
        head = source.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", head[16:24])


def revise(story: str, frame_id: str, relative_image: str, prompt: str,
           references: list[str], reason: str, root: Path = REPO) -> tuple[dict, dict]:
    root = root.resolve()
    story_dir = root / "stories" / story
    existing = json.loads((story_dir / "keyframe_plan.json").read_text())
    current = {row["id"]: row for row in existing["images"]}
    if frame_id not in current:
        raise ValueError(f"unknown keyframe {frame_id}")
    old = current[frame_id]
    keyframe_dir = (root / "character" / "characters" / story / "interactions" / "keyframes").resolve()
    new_path = (root / relative_image).resolve()
    if new_path.parent != keyframe_dir or new_path != root / relative_image:
        raise ValueError("revised image must be a direct, version-local keyframe path")
    old_match = re.fullmatch(rf"{re.escape(frame_id)}_r(\d+)_candidate\.png",
                             Path(old["candidate_path"]).name)
    new_match = re.fullmatch(rf"{re.escape(frame_id)}_r(\d+)_candidate\.png", new_path.name)
    if not old_match or not new_match or int(new_match[1]) <= int(old_match[1]):
        raise ValueError("candidate filename must have a strictly newer revision")
    if not new_path.is_file() or dimensions(new_path) != (1920, 1080):
        raise ValueError("candidate must exist as a 1920x1080 PNG")
    if not prompt.strip() or not references or not reason.strip():
        raise ValueError("exact revision prompt, references and reason are required")
    for reference in references:
        path = (root / reference).resolve()
        if not path.is_file() or (root not in path.parents and path != root):
            raise ValueError(f"missing or external reference: {reference}")
    fresh = keyframe_plan.build(story)
    planned = {row["id"]: row for row in fresh["images"]}[frame_id]
    immutable = ("scene", "audio_line_ids", "visual_unit_ids", "approved_plate",
                 "crop_rect_on_plate", "staging_ref")
    changed = [field for field in immutable if old.get(field) != planned.get(field)]
    if changed:
        raise ValueError(f"staging changed before revision: {', '.join(changed)}")
    updated = json.loads(json.dumps(existing))
    row = next(item for item in updated["images"] if item["id"] == frame_id)
    history = row.setdefault("superseded", [])
    history.append({key: row.get(key) for key in ("candidate_path", "sha256", "prompt",
                                                   "references", "generated_source")})
    history[-1]["reason"] = reason
    row.update(candidate_path=relative_image, sha256=sha256(new_path), prompt=prompt.strip(),
               references=references, revision_note=reason,
               status="candidate_generated_pending_owner_review",
               canvas_px=[1920, 1080], generation_tool="built-in imagegen")
    row.pop("generated_source", None)
    row.pop("revision_prompt", None)
    row.pop("revision_references", None)
    config = json.loads((story_dir / "video_boundary_config.json").read_text())
    boundaries = video_boundary_plan.build(updated, config)
    return updated, boundaries


def write_plan(story: str, plan: dict, boundaries: dict, root: Path = REPO) -> None:
    story_dir = root / "stories" / story
    outputs = {
        story_dir / "keyframe_plan.json": json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
        story_dir / "video_boundary_plan.json": json.dumps(boundaries, indent=2, ensure_ascii=False) + "\n",
        story_dir / "VIDEO_BOUNDARIES.md": video_boundary_plan.markdown(boundaries),
    }
    staged = []
    try:
        for target, content in outputs.items():
            with tempfile.NamedTemporaryFile(mode="w", dir=story_dir, prefix=".revision-",
                                             delete=False, encoding="utf-8") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
                staged.append((Path(handle.name), target))
        for temporary, target in staged:
            temporary.replace(target)
    finally:
        for temporary, _ in staged:
            temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story", required=True)
    parser.add_argument("--frame", required=True)
    parser.add_argument("--image", required=True, help="repository-relative new candidate PNG")
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--reference", action="append", required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()
    plan, boundaries = revise(args.story, args.frame, args.image,
                              args.prompt_file.read_text(), args.reference, args.reason)
    write_plan(args.story, plan, boundaries)
    print(f"{args.frame}: active candidate {args.image}; visual review still required")


if __name__ == "__main__":
    main()
