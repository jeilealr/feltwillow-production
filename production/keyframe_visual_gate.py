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
          "lighting_color_continuity", "camera_family_match", "identity_reference_match",
          "anatomy_limb_count")


def _review_complete(item: dict, review: dict) -> bool:
    """Metadata completeness only; this never judges the pixels."""
    if (review.get("sha256") != item.get("sha256") or not review.get("reviewer") or
            not review.get("reviewed_at") or
            not all(review.get("checks", {}).get(name) is True for name in CHECKS)):
        return False
    actors = set(item.get("planned_actors", item.get("actors", {})))
    evidence = review.get("anatomy_evidence", {})
    for actor in actors:
        row = evidence.get(actor, {})
        expected = row.get("expected_visible_paw_count")
        observed = row.get("observed_visible_paw_count")
        if (not isinstance(expected, int) or isinstance(expected, bool) or not 0 <= expected <= 4 or
                not isinstance(observed, int) or isinstance(observed, bool) or
                observed != expected or row.get("missing_or_duplicated_limbs") is not False or
                not isinstance(row.get("support_contact"), str) or not row["support_contact"].strip()):
            return False
    return True


def build_frame_dispositions(plan: dict, reviews: dict) -> dict:
    """Build current candidate dispositions without inventing visual approvals."""
    records = reviews.get("images", {})
    rejected = reviews.get("known_rejections", {})
    result = {}
    for item in plan.get("images", []):
        fid = item["id"]
        digest = item.get("sha256")
        stale = item.get("regeneration_status") == "stale_pending_new_revision"
        rejection = rejected.get(fid, {})
        review = records.get(fid, {})
        if rejection.get("sha256") == digest:
            disposition = "rejected"
            reason = rejection.get("reason", "Hash-bound known visual rejection")
        elif stale:
            disposition = "supersede_for_camera_plan"
            reason = "Active candidate does not match the current registered camera/staging plan."
        elif _review_complete(item, review):
            disposition = "approved"
            reason = "Full-resolution review record is current and complete."
        else:
            disposition = "pending_review"
            reason = "No complete full-resolution review is recorded for the active candidate hash."
        result[fid] = {
            "active_sha256": digest,
            "staging_freshness": "stale" if stale else "current",
            "visual_disposition": disposition,
            "reason": reason,
        }
    return result


def validate_frame_dispositions(plan: dict, reviews: dict) -> list[str]:
    errors = []
    rows = {item["id"]: item for item in plan.get("images", [])}
    dispositions = reviews.get("frame_dispositions")
    if not isinstance(dispositions, dict):
        return ["frame_dispositions must distinguish staging freshness from visual disposition"]
    if set(dispositions) != set(rows):
        errors.append("frame_dispositions IDs differ from active keyframes")
    expected = build_frame_dispositions(plan, reviews)
    for fid in sorted(set(rows) & set(dispositions)):
        current, recorded = expected[fid], dispositions[fid]
        core_fields = ("active_sha256", "staging_freshness", "visual_disposition")
        if any(recorded.get(field) != current[field] for field in core_fields):
            errors.append(f"{fid}: frame disposition is stale or inconsistent with active hash/review evidence")
        if not isinstance(recorded.get("reason"), str) or not recorded["reason"].strip():
            errors.append(f"{fid}: frame disposition needs a concise reason")
        if current["staging_freshness"] == "stale":
            errors.append(f"{fid}: candidate is stale because its registered camera/staging changed")
        if current["visual_disposition"] == "rejected":
            errors.append(f"{fid}: active candidate hash is explicitly rejected")
    for extra in sorted(set(dispositions) - set(rows)):
        errors.append(f"{extra}: disposition has no active keyframe")
    return errors


def validate(plan: dict, reviews: dict, root: Path = REPO,
             staging: dict | None = None, bible: dict | None = None) -> list[str]:
    errors = []
    if reviews.get("schema") != "feltwillow.keyframe-visual-reviews.v1":
        errors.append("visual reviews have missing or unsupported schema")
    records = reviews.get("images", {})
    rejected = reviews.get("known_rejections", {})
    ids = {item["id"] for item in plan["images"]}
    errors.extend(validate_frame_dispositions(plan, reviews))
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
        anatomy = review.get("anatomy_evidence", {})
        for actor in visible_actors:
            evidence = anatomy.get(actor, {})
            expected_paws = evidence.get("expected_visible_paw_count")
            observed_paws = evidence.get("observed_visible_paw_count")
            if (not isinstance(expected_paws, int) or isinstance(expected_paws, bool) or
                    not 0 <= expected_paws <= 4):
                errors.append(f"{fid}: {actor} expected_visible_paw_count must be recorded from the pose")
            if (not isinstance(observed_paws, int) or isinstance(observed_paws, bool) or
                    observed_paws != expected_paws):
                errors.append(f"{fid}: {actor} visible paw count is missing or differs from expected anatomy")
            if evidence.get("missing_or_duplicated_limbs") is not False:
                errors.append(f"{fid}: {actor} review must confirm no missing or duplicated limbs")
            if not isinstance(evidence.get("support_contact"), str) or not evidence["support_contact"].strip():
                errors.append(f"{fid}: {actor} support_contact evidence is required")
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
