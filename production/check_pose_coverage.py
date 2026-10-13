#!/usr/bin/env python3
"""Check that every staged actor has a usable, version-local pose reference."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def check(story: str, root: Path = REPO) -> list[str]:
    home = root / "stories" / story
    staging = json.loads((home / "staging_plan.json").read_text())
    plan = json.loads((home / "pose_reference_plan.json").read_text())
    errors: list[str] = []
    poses = plan.get("poses", {})
    mappings = plan.get("frames", {})
    staged = {frame["id"]: set(frame["actors"]) for frame in staging["frames"]}
    if set(mappings) != set(staged):
        errors.append(f"frame IDs differ: missing={sorted(set(staged)-set(mappings))}; extra={sorted(set(mappings)-set(staged))}")
    for pose_id, pose in poses.items():
        sheet = pose.get("sheet", "")
        if not sheet or not (root / sheet).is_file():
            errors.append(f"{pose_id}: missing sheet {sheet}")
        cell = pose.get("cell")
        if not isinstance(cell, list) or len(cell) != 2 or any(not isinstance(n, int) or n < 0 for n in cell):
            errors.append(f"{pose_id}: invalid sheet cell {cell}")
        anchor = pose.get("preferred_scene_anchor")
        if anchor and not (root / anchor).is_file():
            errors.append(f"{pose_id}: missing preferred scene anchor {anchor}")
    for frame_id, actors in staged.items():
        assigned = mappings.get(frame_id, {})
        if set(assigned) != actors:
            errors.append(f"{frame_id}: staged actors {sorted(actors)}, pose actors {sorted(assigned)}")
        for actor, pose_ids in assigned.items():
            if not isinstance(pose_ids, list) or not pose_ids:
                errors.append(f"{frame_id}/{actor}: no pose")
                continue
            for pose_id in pose_ids:
                pose = poses.get(pose_id)
                if pose is None or pose.get("actor") != actor:
                    errors.append(f"{frame_id}/{actor}: invalid pose {pose_id}")
    expression = plan.get("expression_overrides", {})
    if expression:
        sheet = expression.get("sheet", "")
        if not sheet or not (root / sheet).is_file():
            errors.append(f"missing expression override sheet {sheet}")
        for frame_id, cell_id in expression.get("frames", {}).items():
            if "leo" not in staged.get(frame_id, set()):
                errors.append(f"{frame_id}: Leo expression override without staged Leo")
            if cell_id not in expression.get("cells", {}):
                errors.append(f"{frame_id}: unknown expression {cell_id}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story", required=True)
    args = parser.parse_args()
    errors = check(args.story)
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    plan = json.loads((REPO / "stories" / args.story / "pose_reference_plan.json").read_text())
    print(f"0 errors; {len(plan['poses'])} pose definitions cover {len(plan['frames'])} staged frames")


if __name__ == "__main__":
    main()
