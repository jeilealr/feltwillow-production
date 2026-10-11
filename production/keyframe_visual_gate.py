#!/usr/bin/env python3
"""Require hash-bound visual decisions before keyframes are used for video.

This verifies review evidence, not image appearance. A human must inspect each
PNG at full size, measure it against its approved setup anchor, and record the
decision in stories/<story>/keyframe_visual_reviews.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHECKS = ("identity", "approved_plate", "anatomical_scale", "same_depth_landmark_scale",
          "ground_contact", "visible_animal_count", "world_state", "adjacent_continuity")


def validate(plan: dict, reviews: dict, root: Path = REPO) -> list[str]:
    errors = []
    if reviews.get("schema") != "feltwillow.keyframe-visual-reviews.v1":
        errors.append("visual reviews have missing or unsupported schema")
    records = reviews.get("images", {})
    rejected = reviews.get("known_rejections", {})
    ids = {item["id"] for item in plan["images"]}
    for item in plan["images"]:
        fid = item["id"]
        path = root / item["candidate_path"]
        if not path.is_file():
            errors.append(f"{fid}: candidate PNG is missing")
            continue
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != item.get("sha256"):
            errors.append(f"{fid}: PNG differs from keyframe_plan.json SHA-256")
        rejection = rejected.get(fid, {})
        if rejection.get("sha256") == actual_hash:
            errors.append(f"{fid}: known rejected PNG: {rejection.get('reason', 'visual failure')}")
        review = records.get(fid)
        if review is None:
            errors.append(f"{fid}: no full-resolution visual review")
            continue
        if review.get("sha256") != actual_hash:
            errors.append(f"{fid}: visual review is stale for this PNG")
        if not review.get("reviewer") or not review.get("reviewed_at"):
            errors.append(f"{fid}: reviewer and review date are required")
        if not review.get("size_anchor") or not review.get("size_evidence"):
            errors.append(f"{fid}: measured same-setup size anchor and evidence are required")
        for check in CHECKS:
            if review.get("checks", {}).get(check) is not True:
                errors.append(f"{fid}: {check} has not passed")
    for extra in sorted(set(records) - ids):
        errors.append(f"{extra}: visual review has no keyframe")
    for extra in sorted(set(rejected) - ids):
        errors.append(f"{extra}: rejection has no keyframe")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story", required=True)
    args = parser.parse_args()
    story = REPO / "stories" / args.story
    plan = json.loads((story / "keyframe_plan.json").read_text())
    review_path = story / "keyframe_visual_reviews.json"
    reviews = json.loads(review_path.read_text()) if review_path.is_file() else {}
    errors = validate(plan, reviews)
    for error in errors[:25]:
        print("BLOCKED:", error)
    if len(errors) > 25:
        print(f"...and {len(errors) - 25} more")
    print(f"{len(errors)} blockers; {len(plan['images'])} candidate keyframes")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
