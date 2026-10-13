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
          "ground_contact", "visible_animal_count", "world_state", "adjacent_continuity",
          "lighting_color_continuity", "camera_family_match", "identity_reference_match")


def validate(plan: dict, reviews: dict, root: Path = REPO,
             staging: dict | None = None, bible: dict | None = None) -> list[str]:
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
        visible_actors = item.get("planned_actors", {})
        if visible_actors:
            planned_anchor_id = item.get("planned_size_anchor_id") or item.get("size_anchor_id")
            if not planned_anchor_id or review.get("size_anchor_id") != planned_anchor_id:
                errors.append(f"{fid}: review size anchor ID must match the planned setup anchor")
            anchor_hash = None
            if staging is not None and planned_anchor_id:
                anchor = staging.get("setup_anchors", {}).get(planned_anchor_id, {})
                if anchor.get("status") != "approved_owner_hash_bound" or not anchor.get("sha256"):
                    errors.append(f"{fid}: planned setup anchor is not owner-approved and hash-bound")
                else:
                    anchor_hash = anchor["sha256"]
            if not review.get("size_anchor_sha256"):
                errors.append(f"{fid}: hash-bound same-setup anchor SHA-256 is required")
            elif anchor_hash and review.get("size_anchor_sha256") != anchor_hash:
                errors.append(f"{fid}: review anchor SHA-256 differs from the registered setup anchor")
            if not review.get("size_evidence"):
                errors.append(f"{fid}: measured same-depth size evidence is required")
            identities = review.get("identity_reference_sha256")
            if not isinstance(identities, dict) or set(identities) != set(visible_actors):
                errors.append(f"{fid}: identity_reference_sha256 must bind every visible actor canonical")
            else:
                for actor, digest in identities.items():
                    if not isinstance(digest, str) or len(digest) != 64:
                        errors.append(f"{fid}: {actor} identity reference needs a SHA-256")
                    elif bible is not None:
                        canonical = bible.get("characters", {}).get(actor, {}).get("canonical")
                        path = (root / canonical).resolve() if canonical else None
                        if not path or not path.is_file():
                            errors.append(f"{fid}: {actor} canonical is unavailable for visual evidence")
                        elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                            errors.append(f"{fid}: {actor} identity-reference hash differs from the canonical")
        expected_camera = item.get("planned_camera_family") or item.get("camera_family")
        if not review.get("camera_family"):
            errors.append(f"{fid}: camera_family evidence is required")
        elif expected_camera and review.get("camera_family") != expected_camera:
            errors.append(f"{fid}: review camera_family differs from the planned camera family")
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
    staging = json.loads((story / "staging_plan.json").read_text())
    bible = json.loads((story / "visual_bible.json").read_text())
    errors = validate(plan, reviews, staging=staging, bible=bible)
    for error in errors[:25]:
        print("BLOCKED:", error)
    if len(errors) > 25:
        print(f"...and {len(errors) - 25} more")
    print(f"{len(errors)} blockers; {len(plan['images'])} candidate keyframes")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
