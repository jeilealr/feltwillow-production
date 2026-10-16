#!/usr/bin/env python3
"""Check a story's cast scale, background placements, and depth-based sizing.

Run ``python3 production/staging_contract.py --story <slug>`` before scene-image
generation. New stories receive a draft contract from image_prompts.py new-story.
"""

import argparse
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_contract(contract, bible, root=REPO, required_frame_ids=(), manifest_records=()):
    """Return actionable errors; no image generation can prove visual compliance."""
    errors = []
    if contract.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not contract.get("story"):
        errors.append("story is missing")
    bible_cast = bible.get("cast_scale", {})
    if contract.get("cast_scale", {}) != bible_cast:
        errors.append("cast_scale must match visual_bible.json exactly")
    # visual_bible.json is the single numeric authority. The copy in the
    # staging document is checked as a snapshot, never used for calculations.
    ratios = bible_cast.get("same_depth_standing_equivalent_height_ratio", {})
    bases = bible_cast.get("wide_foreground_frame_height_fraction", {})
    if not ratios or not bases:
        errors.append("cast_scale needs numeric same-depth ratios and wide foreground heights")
    for name, value in bases.items():
        if name not in bible.get("characters", {}):
            errors.append(f"cast_scale: unknown character {name}")
        if not _number(value) or not 0 < value < 1:
            errors.append(f"cast_scale: {name} wide foreground height must be between 0 and 1")
    for pair, spec in ratios.items():
        try:
            first, second = pair.split("_to_")
            target = spec["standing_equivalent_height"]
            low, high = spec["allowed_review_range"]
            actual = bases[first] / bases[second]
            if not all(_number(x) for x in (target, low, high)) or not low <= target <= high:
                raise ValueError
            if abs(actual - target) > 0.005:
                errors.append(f"cast_scale: {pair} target {target} differs from base heights ({actual:.3f})")
        except (KeyError, ValueError, ZeroDivisionError):
            errors.append(f"cast_scale: {pair} needs a valid pair, target and review range")
    depth = contract.get("depth_model", {})
    far, near = depth.get("far_scale"), depth.get("near_scale")
    if not _number(far) or not _number(near) or not 0 < far < near:
        errors.append("depth_model needs 0 < far_scale < near_scale")
        far, near = 0.55, 1.0
    views = contract.get("views", {})
    locations = contract.get("locations", {})
    frames = contract.get("frames", [])
    setup_anchors = contract.get("setup_anchors", {})
    if not views:
        errors.append("views are missing")
    if not locations:
        errors.append("locations are missing")
    if not frames:
        errors.append("frames are missing")
    for name, loc in locations.items():
        source = bible.get("locations", {}).get(name)
        if source is None:
            errors.append(f"location {name} is absent from visual_bible.json")
        elif loc.get("plate") != source.get("plate"):
            errors.append(f"location {name} plate differs from visual_bible.json")
        plate = loc.get("plate")
        if not plate or not (root / plate).is_file():
            errors.append(f"location {name} approved plate is missing: {plate}")
        y0, y1 = loc.get("far_contact_y"), loc.get("near_contact_y")
        if not _number(y0) or not _number(y1) or not 0 <= y0 < y1 <= 1:
            errors.append(f"location {name} needs valid far/near contact y values")
        for zone_name, zone in loc.get("walkable_zones", {}).items():
            xr, yr = zone.get("x_range", []), zone.get("contact_y_range", [])
            if len(xr) != 2 or len(yr) != 2 or not all(_number(v) for v in [*xr, *yr]) or not (0 <= xr[0] < xr[1] <= 1 and 0 <= yr[0] < yr[1] <= 1):
                errors.append(f"location {name} zone {zone_name} needs normalized x/y ranges")
    by_id = {}
    for frame in frames:
        fid = frame.get("id")
        if not fid or fid in by_id:
            errors.append(f"duplicate or missing frame id: {fid}")
            continue
        by_id[fid] = frame
        anchor_id = frame.get("size_anchor_id")
        if contract.get("size_anchor_policy", {}).get("required_for_regeneration"):
            anchor = setup_anchors.get(anchor_id, {})
            if not anchor_id or not anchor:
                errors.append(f"{fid}: registered size_anchor_id is missing")
            elif (fid not in anchor.get("frame_ids", []) or
                  anchor.get("location") != frame.get("location") or
                  anchor.get("view") != frame.get("view") or
                  set(anchor.get("actor_set", [])) != set(frame.get("actors", {}))):
                errors.append(f"{fid}: size-anchor family does not match its camera, location and cast")
        name = frame.get("location")
        loc = locations.get(name)
        if loc is None:
            errors.append(f"{fid}: unknown location {name}")
            continue
        if frame.get("plate") != loc.get("plate"):
            errors.append(f"{fid}: plate must be the approved plate for {name}")
        view = views.get(frame.get("view"))
        camera_center = frame.get("camera_center_xy_on_plate")
        if camera_center is not None and (len(camera_center) != 2 or
                not all(_number(v) and 0 <= v <= 1 for v in camera_center)):
            errors.append(f"{fid}: camera_center_xy_on_plate needs two normalized coordinates")
        if view is None or not _number(view.get("magnification")) or view["magnification"] <= 0:
            errors.append(f"{fid}: unknown or invalid view {frame.get('view')}")
            continue
        for actor, placement in frame.get("actors", {}).items():
            if actor not in bases:
                errors.append(f"{fid}: {actor} has no cast-scale base height")
                continue
            zone_name = placement.get("support_zone")
            zone = loc.get("walkable_zones", {}).get(zone_name)
            if zone is None:
                errors.append(f"{fid}: {actor} uses undefined walkable zone {zone_name}")
                continue
            xy = placement.get("contact_xy_on_plate", [])
            if len(xy) != 2 or not all(_number(v) for v in xy):
                errors.append(f"{fid}: {actor} needs numeric contact_xy_on_plate")
                continue
            x, y = xy
            xr, yr = zone["x_range"], zone["contact_y_range"]
            if not (xr[0] <= x <= xr[1] and yr[0] <= y <= yr[1]):
                errors.append(f"{fid}: {actor} contact {xy} is outside walkable zone {zone_name}")
            y0, y1 = loc["far_contact_y"], loc["near_contact_y"]
            expected_depth = (y - y0) / (y1 - y0)
            recorded_depth = placement.get("depth_t")
            if not _number(recorded_depth) or abs(expected_depth - recorded_depth) > 0.005:
                errors.append(f"{fid}: {actor} depth_t must follow the contact point on the plate")
            height = placement.get("standing_equivalent_height_fraction_after_crop")
            expected_height = bases[actor] * (far + (near - far) * expected_depth) * view["magnification"]
            override = placement.get("owner_scale_override")
            if override is not None:
                reference = (root / override.get("reference_path", "")).resolve()
                target = override.get("standing_equivalent_height_fraction")
                valid = (override.get("status") == "approved_owner_hash_bound" and
                         override.get("reviewer") == "project_owner" and
                         bool(override.get("reason")) and _number(target) and 0 < target < 1 and
                         reference.is_relative_to(root.resolve()) and reference.is_file() and
                         hashlib.sha256(reference.read_bytes()).hexdigest() == override.get("sha256"))
                if not valid:
                    errors.append(f"{fid}: owner scale override needs an explicit hash-bound reference and target")
                else:
                    expected_height = target
            if not _number(height) or abs(expected_height - height) > 0.005:
                errors.append(f"{fid}: {actor} height must follow cast scale, depth and camera crop ({expected_height:.3f})")
    for fid in required_frame_ids:
        if fid not in by_id:
            errors.append(f"scene image {fid} has no staging frame")
    for rec in manifest_records:
        frame = by_id.get(rec.get("id"))
        if frame and rec.get("setup") and frame.get("setup") != rec["setup"]:
            errors.append(f"{rec['id']}: staging setup differs from image record")
    scene_plan_path = contract.get("scene_plan")
    if scene_plan_path and (root / scene_plan_path).is_file():
        scene_plan = json.loads((root / scene_plan_path).read_text())
        expected = {p["panel_id"] for s in scene_plan.get("scenes", []) for p in s.get("panels", [])}
        extra_path = contract.get("visual_sequence_plan")
        if extra_path and (root / extra_path).is_file():
            visual_plan = json.loads((root / extra_path).read_text())
            expected.update(p["id"] for board in visual_plan.get("supplemental_boards", [])
                            for p in board.get("panels", []))
        if set(by_id) != expected:
            errors.append(f"staging frames differ from scene_plan panels: missing {sorted(expected-set(by_id))}, extra {sorted(set(by_id)-expected)}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story", required=True)
    args = parser.parse_args()
    story_dir = REPO / "stories" / args.story
    bible = json.loads((story_dir / "visual_bible.json").read_text())
    path = REPO / bible.get("staging_contract", f"stories/{args.story}/staging_plan.json")
    contract = json.loads(path.read_text())
    errors = validate_contract(contract, bible)
    for error in errors:
        print("ERROR:", error)
    print(f"{len(errors)} errors; {len(contract.get('frames', []))} staged frames")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
