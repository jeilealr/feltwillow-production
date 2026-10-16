#!/usr/bin/env python3
"""Read-only v6 pilot input audit; no renderer, model imports, or approvals.

Exit 0 certifies metadata consistency only. Production eligibility is always false.
Requires Python 3.9+; outputs JSON to stdout and never writes files.
"""

import argparse
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
STORY = "lion_and_mouse_v6"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def contained_file(root, relative):
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError("expected a repository-relative source path")
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError("source missing or outside repository: " + relative)
    return path


def geometry(row):
    # Fail if planned and candidate geometry differ; neither overrides the other.
    view = row.get("view")
    crop = row.get("crop_rect_on_plate")
    if not view or not crop or row.get("planned_view") != view:
        raise ValueError("missing or inconsistent planned/candidate view: " + row["id"])
    if row.get("planned_crop_rect_on_plate") != crop:
        raise ValueError("planned/candidate crop differs: " + row["id"])
    if (not isinstance(crop, list) or len(crop) != 4 or
            any(type(x) not in (int, float) or not 0 <= x <= 1 for x in crop) or
            crop[2] == 0 or crop[3] == 0 or
            crop[0] + crop[2] > 1.00001 or crop[1] + crop[3] > 1.00001):
        raise ValueError("invalid normalized x/y/width/height crop: " + row["id"])
    plate = row.get("approved_plate")
    if not plate:
        raise ValueError("missing plate: " + row["id"])
    return {"plate": plate, "view": view, "crop_xywh": crop}


def audit(root, start_id, end_id):
    base = "stories/" + STORY + "/"
    documents = {}
    hashes = {}
    for name in ("keyframe_plan.json", "video_boundary_plan.json", "staging_plan.json",
                 "keyframe_visual_reviews.json", "owner_visual_acceptance.json"):
        path = contained_file(root, base + name)
        documents[name] = json.loads(path.read_text())
        hashes[base + name] = sha256(path)
    contract = contained_file(root, base + "RUNTIME_CONTRACT.md")
    hashes[base + "RUNTIME_CONTRACT.md"] = sha256(contract)
    for name in ("keyframe_plan.json", "video_boundary_plan.json", "staging_plan.json"):
        if documents[name].get("story") != STORY:
            raise ValueError("story identity mismatch: " + name)
    rows = {row["id"]: row for row in documents["keyframe_plan.json"]["images"]}
    if start_id not in rows or end_id not in rows:
        raise ValueError("unknown keyframe ID")
    start, end = rows[start_id], rows[end_id]
    if start.get("scene") != end.get("scene"):
        raise ValueError("cross-scene pilots are excluded")
    if start_id != end_id:
        transitions = [t for s in documents["video_boundary_plan.json"]["scenes"]
                       for t in s["internal_transitions"]
                       if t["from"] == start_id and t["to"] == end_id]
        if len(transitions) != 1 or transitions[0]["kind"] != "same_view_motion_candidate":
            raise ValueError("pilot must be a hold or a registered same-view candidate; cuts excluded")
        for key, row in (("start_image", start), ("end_image", end)):
            if transitions[0].get(key) != row["candidate_path"]:
                raise ValueError("boundary endpoint path differs from selected keyframe")
    first_geometry, last_geometry = geometry(start), geometry(end)
    if first_geometry != last_geometry:
        raise ValueError("plate/view/crop mismatch despite boundary label")
    actors = []
    endpoints = []
    for row in (start, end):
        planned = row.get("planned_actors")
        if not isinstance(planned, dict) or not planned:
            raise ValueError("missing planned actor metadata: " + row["id"])
        actors.append(set(planned))
        source = contained_file(root, row["candidate_path"])
        actual_hash = sha256(source)
        if actual_hash != row.get("sha256"):
            raise ValueError("selected image hash differs from keyframe plan: " + row["id"])
        endpoints.append({"id": row["id"], "path": row["candidate_path"],
                          "sha256": actual_hash, "planned_actors": planned,
                          "dialogue_speakers": row.get("dialogue_speakers", [])})
    if actors[0] != actors[1]:
        raise ValueError("actor set changes across pilot")
    plate = contained_file(root, first_geometry["plate"])
    return {"schema": "feltwillow.video-control-input-audit.v0",
            "story": STORY, "approval": "isolated_experiment_not_for_production",
            "production_eligible": False, "metadata_consistent": True,
            "visual_review_performed": False, "runtime_preflight_performed": False,
            "boundary": "hold" if start_id == end_id else "same_view_motion_candidate",
            "geometry": first_geometry, "plate_sha256": sha256(plate),
            "endpoints": endpoints, "document_sha256": hashes,
            "limitations": ["Not a runtime, staging or visual approval",
                            "No control/backend capability or endpoint preservation proven",
                            "Re-audit after any source or policy change"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", required=True, help="registered keyframe ID")
    parser.add_argument("--end", required=True, help="same-view endpoint ID or same ID for hold")
    args = parser.parse_args()
    try:
        result = audit(REPO, args.start, args.end)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"production_eligible": False, "metadata_consistent": False,
                          "error": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
