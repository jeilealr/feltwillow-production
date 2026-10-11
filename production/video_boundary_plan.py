#!/usr/bin/env python3
"""Plan v6 scene endpoints and cuts without rendering or approving images.

The plan names actual candidate files, but every video use still requires visual
approval. A camera-crop change is a cut unless a separate camera move is designed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Story-specific chronology, shared joins and reasons live beside the story.
# New-story scaffolding creates an empty config that must be filled before use.
def load_config(story: str) -> dict:
    path = REPO / "stories" / story / "video_boundary_config.json"
    return json.loads(path.read_text())


def build(keyframes: dict, config: dict) -> dict:
    if config.get("schema") != "feltwillow.video-boundary-config.v1":
        raise ValueError("missing or unsupported video boundary config")
    if config.get("story") != keyframes.get("story"):
        raise ValueError("video boundary config story differs from keyframe plan")
    orders = {int(k): v for k, v in config.get("scene_order_overrides", {}).items()}
    shared_entries = {int(k): int(v) for k, v in config.get("shared_entries", {}).items()}
    cut_reasons = {int(k): v for k, v in config.get("cut_reasons", {}).items()}
    images = keyframes["images"]
    by_id = {image["id"]: image for image in images}
    if len(by_id) != len(images):
        raise ValueError("duplicate keyframe ID")
    grouped = {}
    for image in images:
        grouped.setdefault(image["scene"], []).append(image)
    scenes = []
    for number in sorted(grouped):
        owned = grouped[number]
        order = orders.get(number)
        if order is None and any("x_p" in image["id"] for image in owned):
            raise ValueError(f"scene {number:02d}: supplemental views need an explicit "
                             "chronological order in video_boundary_config.json")
        ids = order.split() if order else [image["id"] for image in owned]
        if len(ids) != len(owned) or set(ids) != {image["id"] for image in owned}:
            raise ValueError(f"scene {number:02d}: chronological order does not cover each keyframe exactly once")
        first, last = by_id[ids[0]], by_id[ids[-1]]
        previous = scenes[-1] if scenes else None
        shared_from = shared_entries.get(number)
        if shared_from is not None:
            if previous is None or previous["scene"] != shared_from:
                raise ValueError(f"scene {number:02d}: missing preceding scene {shared_from:02d}")
            prior_last = by_id[previous["last_keyframe"]]
            if (prior_last["approved_plate"] != first["approved_plate"] or
                    prior_last["crop_rect_on_plate"] != first["crop_rect_on_plate"]):
                raise ValueError(f"scene {number:02d}: shared boundary changes plate or crop")
            start = prior_last
            entry = "shared_boundary_candidate"
            entry_motion = {"start_image": prior_last["candidate_path"],
                            "end_image": first["candidate_path"],
                            "status": "pending_endpoint_match_and_timing"}
        else:
            start = first
            entry = "cut"
            entry_motion = None
            if not cut_reasons.get(number):
                raise ValueError(f"scene {number:02d}: cut needs an explicit reason")
        entry_reason = (f"Exact shared image from Scene {shared_from:02d}; same plate and crop"
                        if shared_from is not None else cut_reasons[number])
        transitions = []
        for a_id, b_id in zip(ids, ids[1:]):
            a, b = by_id[a_id], by_id[b_id]
            if a["approved_plate"] != b["approved_plate"]:
                kind = "location_cut"
            elif a["crop_rect_on_plate"] != b["crop_rect_on_plate"]:
                kind = "camera_cut"
            else:
                kind = "same_view_motion_candidate"
            transitions.append({
                "from": a_id,
                "to": b_id,
                "kind": kind,
                "start_image": a["candidate_path"],
                "end_image": (b["candidate_path"] if kind == "same_view_motion_candidate"
                              else a["candidate_path"]),
                "next_start_image": b["candidate_path"],
                "status": "pending_endpoint_match_and_timing",
            })
        scenes.append({
            "scene": number,
            "entry": entry,
            "entry_reason": entry_reason,
            "entry_motion": entry_motion,
            "shared_from_scene": shared_from,
            "start_keyframe": start["id"],
            "start_image": start["candidate_path"],
            "first_own_keyframe": first["id"],
            "first_own_image": first["candidate_path"],
            "last_keyframe": last["id"],
            "end_image": last["candidate_path"],
            "ordered_keyframes": ids,
            "internal_transitions": transitions,
        })
    if sum(len(scene["ordered_keyframes"]) for scene in scenes) != len(images):
        raise ValueError("not every keyframe has a scene boundary assignment")
    return {
        "schema": "feltwillow.video-boundaries.v1",
        "story": keyframes["story"],
        "status": "candidate_plan_pending_visual_review_and_word_timing",
        "rules": {
            "shared_boundary": "The exact previous end image is the next scene's start image; revise the next target frame until its geometry, identity and size match before video rendering.",
            "camera_cut": "Different plate crop; never interpolate actor scale as if the actor grew or shrank. A deliberate zoom needs its own registered camera move and endpoint review.",
            "same_view_motion_candidate": "Same plate and crop only; compare the real pixels, character anatomy, landmark ratios, depth and ground contact before using as start/end of one moving clip.",
            "timing": "Whole-line unit boundaries are known; exact cuts within long lines still need word alignment.",
        },
        "scenes": scenes,
    }


def markdown(plan: dict) -> str:
    lines = [
        f"# {plan['story']} video scene boundaries",
        "",
        "**Status:** planning only. The listed PNGs are unapproved candidates; "
        "no video is render-ready from this table. Run "
        f"`python3 production/keyframe_visual_gate.py --story {plan['story']}` "
        "before video export.",
        "",
        "The start image is the first boundary of that audio scene and the end image "
        "is its last boundary. At a shared entry, the previous scene's **exact end "
        "PNG** becomes the next scene's start PNG; its first own keyframe is the "
        "next motion target. A change of crop is a cut unless a separate zoom path "
        "is approved. Internal cuts and chronological frame order are in "
        "[`video_boundary_plan.json`](video_boundary_plan.json).",
        "",
        "| Scene | Entry | Start boundary | First own image | End boundary | Ordered images |",
        "|---|---|---|---|---|---:|",
    ]
    for scene in plan["scenes"]:
        lines.append(
            f"| {scene['scene']:02d} | {scene['entry_reason']} | "
            f"`{scene['start_keyframe']}` | `{scene['first_own_keyframe']}` | "
            f"`{scene['last_keyframe']}` | {len(scene['ordered_keyframes'])} |"
        )
    lines.extend([
        "",
        "Each internal transition in the JSON also has explicit candidate "
        "`start_image` and `end_image` paths. On a camera/location cut, the outgoing "
        "endpoint remains its own image and `next_start_image` begins the next "
        "view; never morph the two views. `same_view_motion_candidate` uses the "
        "next PNG as its proposed end. Its actual pixels, identity, scale, "
        "landmarks and ground contact must still pass review. See "
        "[`KEYFRAME_CONSISTENCY_AUDIT.md`](KEYFRAME_CONSISTENCY_AUDIT.md).",
        "",
        "Cuts within a long narrator line need word-level timing before clip durations "
        "or edit points are final. Only character dialogue gets lip-sync.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story", required=True)
    args = parser.parse_args()
    path = REPO / "stories" / args.story / "keyframe_plan.json"
    plan = build(json.loads(path.read_text()), load_config(args.story))
    out = path.with_name("video_boundary_plan.json")
    out.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    out.with_name("VIDEO_BOUNDARIES.md").write_text(markdown(plan))
    print(f"{out}: {len(plan['scenes'])} scenes with explicit start/end images")


if __name__ == "__main__":
    main()
