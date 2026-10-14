#!/usr/bin/env python3
"""Build individual v6 keyframe records from the audio and staging contracts.

The resulting images remain owner-review candidates until visual approval. This
script only writes the plan; image generation is an explicit separate step.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def crop_for_frame(frame: dict, magnification: float) -> list[float]:
    if magnification == 1:
        return [0.0, 0.0, 1.0, 1.0]
    width = height = 1 / magnification
    contacts = [a["contact_xy_on_plate"] for a in frame["actors"].values()]
    center_x = sum(x for x, _ in contacts) / len(contacts) if contacts else 0.5
    contact_y = max((y for _, y in contacts), default=0.8)
    left = max(0.0, min(1 - width, center_x - width / 2))
    top = max(0.0, min(1 - height, contact_y - height * 0.8))
    return [round(left, 5), round(top, 5), round(width, 5), round(height, 5)]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _identity_lock(actor: str, bible: dict) -> str:
    """Render identity from the story bible; code adds enforcement, not a second design."""
    record = bible.get("characters", {}).get(actor)
    if not record or not record.get("identity"):
        raise ValueError(f"{actor}: visual_bible.json needs an identity description")
    name = record.get("name") or actor.title()
    return (f"{name} must match the registered {name} canonical exactly: {record['identity']} "
            "Preserve the canonical silhouette, intrinsic colors, feature count and anatomy; "
            "the canonical also controls the intrinsic felt pigment, fiber density and fiber scale "
            "on the coat, face, paws, mane and tail. Direct light may warm illuminated surfaces "
            "and edges, but the softly lit midtones and shaded fibers must still read as the "
            "canonical material. Do not recolor the whole character to match a sunset or style "
            "swatch, enlarge the fibers into open yarn loops, redesign the character or add "
            "features absent from the canonical.")


def _cast_scale_lock(bible: dict) -> str:
    """Render the current same-depth cast relation from the single bible authority."""
    try:
        ratio = float(bible["cast_scale"]["same_depth_standing_equivalent_height_ratio"]
                      ["milo_to_leo"]["standing_equivalent_height"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("visual_bible.json needs a numeric Milo-to-Leo standing-equivalent ratio") from exc
    if not 0 < ratio < 1:
        raise ValueError("visual_bible.json Milo-to-Leo standing-equivalent ratio must be between 0 and 1")
    percent = f"{ratio * 100:g}%"
    return (f"At equal depth and camera Milo's upright ear-to-foot standing-equivalent height is "
            f"about {percent} of Leo's quadrupedal mane-top-to-supporting-front-paw height; "
            "preserve their anatomy and apply the registered depth and crop separately.")


def _historicalize_candidate(row: dict) -> dict:
    """Rename generated-record instructions as provenance before persisting an active candidate."""
    row = dict(row)
    mapping = {
        "prompt": "historical_candidate_prompt",
        "references": "historical_candidate_references",
        "reference_roles": "historical_candidate_reference_roles",
        "generation_inputs": "historical_candidate_inputs",
        "generation_tool": "historical_candidate_tool",
    }
    for source, destination in mapping.items():
        if source in row:
            row.setdefault(destination, row[source])
            row.pop(source, None)
    return row


def _prompt_action(action: str) -> str:
    """Remove storyboard mouth poses from closed production-boundary prompts."""
    action = re.sub(r";?\s*open mouth only on [^.;]+", "", action, flags=re.IGNORECASE)
    action = re.sub(r"\s+with an open mouth for his line", "", action, flags=re.IGNORECASE)
    action = re.sub(r"\s+open mouth only on [^.;]+", "", action, flags=re.IGNORECASE)
    action = re.sub(r"\s+alternate speaking mouth only for the named line speaker", "", action,
                    flags=re.IGNORECASE)
    action = re.sub(r"\s+(?:with\s+)?(?:a\s+)?(?:determined\s+|wide\s+|softly\s+)?open mouth"
                    r"(?:\s+[^.;,]*)?", "", action, flags=re.IGNORECASE)
    action = re.sub(r"\s+(?:with\s+)?(?:a\s+)?speaking mouth(?:\s+[^,.;]*)?", "",
                    action, flags=re.IGNORECASE)
    action = re.sub(r"\s+(?:his|her|their) mouth (?:is )?open(?:\s+[^,.;]*)?", "",
                    action, flags=re.IGNORECASE)
    action = re.sub(r"\s+(?:opens?|opening) (?:his|her|their|the) mouth(?:\s+[^,.;]*)?", "",
                    action, flags=re.IGNORECASE)
    return action.strip(" ;")


def build(story: str, root: Path = REPO) -> dict:
    root = root.resolve()
    home = root / "stories" / story
    scene = json.loads((home / "scene_plan.json").read_text())
    sequence = json.loads((home / "visual_sequence_plan.json").read_text())
    staging = json.loads((home / "staging_plan.json").read_text())
    bible = json.loads((home / "visual_bible.json").read_text())
    by_frame = {x["id"]: x for x in staging["frames"]}
    by_panel = {}
    boards = {}
    for board in scene["scenes"]:
        for panel in board["panels"]:
            by_panel[panel["panel_id"]] = {
                "line_ids": panel["covered_line_ids"],
                "dialogue_speakers": panel["dialogue_speakers"],
                "action": panel["action"],
            }
            boards[panel["panel_id"]] = board["candidate_path"]
    for board in sequence["supplemental_boards"]:
        for panel in board["panels"]:
            by_panel[panel["id"]] = {
                "line_ids": panel["line_ids"],
                "dialogue_speakers": panel.get("dialogue_speakers", []),
                "action": panel["action"],
            }
            boards[panel["id"]] = board["candidate_path"]
    units = sequence["units"]
    images = []
    for frame in staging["frames"]:
        fid = frame["id"]
        panel = by_panel[fid]
        lines = panel["line_ids"]
        unit_ids = [u["id"] for u in units if u["audio_scene"] == frame["scene"]
                    and set(u["line_ids"]) & set(lines)]
        action = panel["action"]
        prop = None
        prop_name = None
        if "acorn" in action.lower():
            prop_name = "acorn"
        elif (frame["scene"] in (10, 11, 13, 14) or
              # The rebuilt Scene 15 explanation frame explicitly stages the
              # released net and carries its approved prop authority.
              (fid == "s15_p04") or
              any(word in action.lower() for word in ("net", "rope", "strand", "mesh", "fibre", "fiber"))):
            prop_name = "hunter_net"
        prop_record = bible.get("props", {}).get(prop_name, {}) if prop_name else {}
        if prop_name and prop_record.get("status") in ("approved", "approved_owner_hash_bound"):
            prop = prop_record.get("reference")
        view = frame["view"]
        crop = crop_for_frame(frame, staging["views"][view]["magnification"])
        # The approved plate is the portable authority. Its registered crop is
        # materialized from this path and crop rectangle by the crop tool.
        reference_plate = frame["plate"]
        refs = [reference_plate]
        reference_roles = [{"role": "approved_plate", "path": reference_plate,
                            "sha256": sha256(root / reference_plate), "required": True,
                            "crop_rect_on_plate": crop,
                            "materializer": "normalized_crop.v1",
                            "output_resolution": "derived from registered crop without resampling"}]
        for actor in ("leo", "milo"):
            if actor in frame["actors"]:
                path = bible["characters"][actor]["canonical"]
                refs.append(path)
                reference_roles.append({"role": "identity_root", "actor": actor,
                                        "path": path, "sha256": sha256(root / path),
                                        "required": True})
        anchor = staging.get("setup_anchors", {}).get(frame.get("size_anchor_id"), {})
        if (anchor.get("status") == "approved_owner_hash_bound" and anchor.get("image_path") and
                anchor.get("sha256")):
            anchor_path = anchor["image_path"]
            anchor_file = root / anchor_path
            if not anchor_file.is_file() or sha256(anchor_file) != anchor["sha256"]:
                raise ValueError(f"{fid}: approved size anchor path/hash is stale")
            refs.append(anchor_path)
            reference_roles.append({"role": "size_anchor", "id": frame["size_anchor_id"],
                                    "path": anchor_path, "sha256": anchor["sha256"],
                                    "required": True})
        if prop and (root / prop).is_file():
            refs.append(prop)
            reference_roles.append({"role": "prop", "path": prop,
                                    "sha256": sha256(root / prop), "required": True,
                                    "id": prop_name})
        scene_style = bible.get("scene_style_standards", {}).get(str(frame["scene"]))
        if scene_style and fid == scene_style.get("standard_frame_id"):
            # The immutable owner-liked master defines this look; never make a
            # generated revision of the standard depend on a crop of itself.
            scene_style = None
        scene_style_clause = ""
        if scene_style:
            swatch = scene_style.get("swatch", {})
            style_path = swatch.get("path")
            style_file = root / style_path if style_path else None
            if (not style_file or not style_file.is_file() or
                    sha256(style_file) != swatch.get("sha256")):
                raise ValueError(f"{fid}: scene style swatch path/hash is missing or stale")
            standard = scene_style.get("standard_frame", {})
            if (standard.get("path") != scene_style.get("derived_from_path") or
                    standard.get("sha256") != scene_style.get("derived_from_sha256")):
                raise ValueError(f"{fid}: scene style standard source is inconsistent")
            standard_file = root / standard.get("path", "")
            if (not standard_file.is_file() or
                    sha256(standard_file) != standard.get("sha256")):
                raise ValueError(f"{fid}: scene style master path/hash is missing or stale")
            refs.append(style_path)
            reference_roles.append({
                "role": "style_reference", "id": scene_style.get("id"),
                "path": style_path, "sha256": swatch["sha256"], "required": True,
                "authority_scope": swatch.get("authority_scope"),
                "derived_from_path": standard.get("path"),
                "derived_from_sha256": standard.get("sha256"),
            })
            scene_style_clause = (
                f"SCENE STYLE LOCK: {scene_style.get('lighting_prompt_clause', '')} "
                f"{scene_style.get('prompt_clause', '')} ")
        people = []
        for name, actor in frame["actors"].items():
            x, y = actor["contact_xy_on_plate"]
            cx, cy, cw, ch = crop
            projected_x, projected_y = (x - cx) / cw, (y - cy) / ch
            height = actor["standing_equivalent_height_fraction_after_crop"]
            people.append(f"{name.title()} planted contact at ({projected_x:.0%}, {projected_y:.0%}) "
                          f"of this image; standing-equivalent anatomical height target "
                          f"{height:.0%} of this frame. Keep head/body proportions fixed when "
                          "the pose bends, sits or lies down")
        identities = [_identity_lock(actor, bible) for actor in ("leo", "milo") if actor in frame["actors"]]
        if len(frame["actors"]) == 2:
            identities.append(_cast_scale_lock(bible))
        count_word = {0: "NO animals", 1: "exactly ONE animal", 2: "exactly TWO animals"}[len(frame["actors"])]
        net_continuity = ""
        if "leo" in frame["actors"] and (frame["scene"] in (11, 13) or
                (frame["scene"] == 10 and fid == "s10_p03") or
                (frame["scene"] == 14 and fid != "s14_p06")):
            net_continuity = ("Leo remains trapped under the SAME flax-rope diamond-mesh net, "
                              "held on his body and hindquarters; his face and muzzle remain clear. "
                              "The one closure loop is at his flank. Do not free Leo or leave only a "
                              "loose rope pile before s14_p06. ")
        elif fid == "s14_p06":
            net_continuity = "This is the ONLY escape beat: Leo steps out and the parted net falls behind him. "
        elif fid in ("s10_p01", "s10_p02"):
            net_continuity = ("Show the SAME leaf-covered flax-rope trigger loop lying flat on "
                              "the path ahead of Leo, visibly connected by rope to a folded net "
                              "suspended from the overhead branch. Keep the ground trigger at "
                              "the same path position in both frames. Leo is not yet caught; "
                              "do not replace the trigger with a stone or omit it. ")
        elif frame["scene"] == 15 and "leo" in frame["actors"]:
            net_continuity = "Leo is now free; the discarded net stays behind both characters on the trap path. "
        board_note = (f"The storyboard panel {fid} guides the beat and composition only; it carries no "
                      "authority for identity, physical scale, lighting or background geography. "
                      if boards.get(fid) else "")
        solo_detail = (frame["scene"] == 14 and view == "detail_insert"
                       and "leo" not in frame["actors"])
        if solo_detail:
            # The source action may mention Leo's face as a negative instruction.
            # Avoid naming an off-camera character at all in a one-animal prompt.
            if fid == "s14_p04":
                prompt_action = "Close detail of fibers fraying on the strand at Milo's teeth."
            elif fid == "s14_p05":
                prompt_action = "The same frayed strand parts at Milo's teeth; the net remains intact elsewhere."
            else:
                prompt_action = action
            detail_rule = ("Only Milo, rope fibers and the registered background are visible; "
                           "do not include a second animal or body. ")
        else:
            prompt_action = action
            detail_rule = ""
        dialogue_close_rule = ""
        if view in ("close_solo", "portrait_milo") and panel["dialogue_speakers"]:
            actor = next(iter(frame["actors"])) if len(frame["actors"]) == 1 else None
            subject = ("Milo's sharp canonical face and upper torso, with both large rounded ears visible "
                       "and no mane or top-hair" if actor == "milo" else
                       "Leo's sharp canonical face and upper chest, preserving the full mane silhouette"
                       if actor == "leo" else "the sharp canonical speaker face and upper chest")
            dialogue_close_rule = (
                f"Intentional dialogue camera cut on {subject}. Retain the registered location crop and "
                "strongly defocus the approved background in the reviewed s07x portrait style. The crop "
                "changes screen occupancy, not anatomy or physical cast scale. ")
        size_anchor_clause = (f"The attached {frame.get('size_anchor_id')} image is the same-setup "
                              "physical-size anchor; preserve its anatomical dimensions and same-depth "
                              "landmark ratio. The crop changes screen occupancy only. "
                              if anchor.get("status") == "approved_owner_hash_bound" else
                              "No visible characters are staged, so no physical-size anchor applies. "
                              if not frame["actors"] else
                              "No approved same-setup size anchor is registered yet; this prompt is not ready for generation. ")
        location_contract = bible["locations"].get(frame["location"], {}).get("image_generation_contract", {})
        lighting_lock = location_contract.get("prompt_clause") or (
            f"Preserve the exact approved {frame['location']} plate lighting, exposure, white balance, "
            "landmark geometry and intrinsic canonical character colors.")
        if scene_style:
            # This owner-directed scene-specific style standard controls the
            # scene's rendered brightness and felt finish while the approved
            # plate remains authoritative for camera, geography and light direction.
            lighting_lock = scene_style.get("lighting_prompt_clause", lighting_lock)
        action_for_prompt = _prompt_action(prompt_action)
        prompt = (f"Edit reference image 1 into ONE full-frame 16:9 production video keyframe for "
                  f"{story}, audio scene {frame['scene']:02d}, {fid}. Use the approved plate crop "
                  f"registered as normalized x/y/width/height {crop}; keep its camera, landmarks and "
                  f"walkable ground fixed. Add {count_word}. {board_note}WORLD AND LIGHT LOCK: "
                  f"{lighting_lock} {scene_style_clause}SIZE ANCHOR: {size_anchor_clause}Action: {action_for_prompt} "
                  f"Placement: {'; '.join(people) if people else 'empty approved location view'}. "
                  f"IDENTITY LOCK: {'; '.join(identities) if identities else 'no cast'}. "
                  f"{net_continuity}{detail_rule}{dialogue_close_rule}"
                  "Add only story props necessary for this action. MOUTH POLICY: closed production "
                  "boundary; dialogue speaker and expression remain metadata for later lip-sync. "
                  "Preserve matte handmade needle-felt texture. Do not zoom out, reveal more "
                  "scenery, add bags, pouches, clothing, accessories, any other animal, "
                  "redesign the plate, apply a global color grade, add captions, letters, "
                  "speech bubbles, a narrator figure, borders or multiple panels.")
        images.append({
            "id": fid,
            "scene": frame["scene"],
            "audio_line_ids": lines,
            "visual_unit_ids": unit_ids,
            "status": "planned",
            "candidate_path": f"character/characters/{story}/interactions/keyframes/{fid}_r01_candidate.png",
            "approved_plate": frame["plate"],
            "location": frame["location"],
            "actors": frame["actors"],
            "reference_plate": reference_plate,
            "board_reference": boards[fid],
            "view": view,
            "crop_rect_on_plate": crop,
            "staging_ref": fid,
            "references": refs,
            "reference_roles": reference_roles,
            "required_props": ([{"id": prop_name, "path": prop_record.get("reference"),
                                 "status": prop_record.get("status")}]
                               if prop_name else []),
            "mouth_policy": "closed_boundary_for_lipsync",
            "size_anchor_id": frame.get("size_anchor_id"),
            "camera_family": f"{frame['location']}:{view}",
            "action": action,
            "dialogue_speakers": panel["dialogue_speakers"],
            "prompt": prompt,
        })
    return {
        "revision": "2026-10-11-r01",
        "story": story,
        "status": "production_keyframe_candidates_pending_owner_review",
        "prompt_policy": "Active candidate prompt/reference provenance is stored under historical_candidate_* fields and is never a runnable source stack. Build new instructions from the current plan builder and keyframe_regeneration_contract.json.",
        "audio_scene_count": scene["scene_count"],
        "visual_unit_count": sequence["visual_unit_count"],
        "keyframe_count": len(images),
        "overview_keyframe_count": scene["panel_count"],
        "supplemental_keyframe_count": len(images) - scene["panel_count"],
        "images": images,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--story", required=True)
    args = ap.parse_args()
    plan = build(args.story)
    out = REPO / "stories" / args.story / "keyframe_plan.json"
    if out.is_file():
        previous = {x["id"]: x for x in json.loads(out.read_text()).get("images", [])}
        for index, frame in enumerate(plan["images"]):
            old = previous.get(frame["id"], {})
            if old.get("status") == "candidate_generated_pending_owner_review":
                immutable = ("scene", "audio_line_ids", "visual_unit_ids", "approved_plate",
                             "staging_ref")
                changed = [key for key in immutable if old.get(key) != frame.get(key)]
                planned_fields = {
                    "view": frame.get("view"),
                    "crop_rect_on_plate": frame.get("crop_rect_on_plate"),
                }
                staging_changed = [key for key, value in planned_fields.items()
                                   if old.get(key) != value]
                changed.extend(key for key in staging_changed if key not in changed)
                # The exact prompt, ordered references and crop are provenance
                # for the existing image. Never overwrite them on a re-plan.
                preserved = _historicalize_candidate(old)
                if changed:
                    preserved["regeneration_status"] = "stale_pending_new_revision"
                    preserved["planned_staging_changes"] = changed
                    preserved["planned_crop_rect_on_plate"] = frame.get("crop_rect_on_plate")
                    preserved["planned_view"] = frame.get("view")
                    preserved["planned_size_anchor_id"] = frame.get("size_anchor_id")
                    preserved["planned_actors"] = frame.get("actors")
                    preserved["planned_camera_family"] = frame.get("camera_family")
                else:
                    preserved["regeneration_status"] = "current_staging_matches_candidate_record"
                    preserved["planned_view"] = frame.get("view")
                    preserved["planned_crop_rect_on_plate"] = frame.get("crop_rect_on_plate")
                    preserved["planned_size_anchor_id"] = frame.get("size_anchor_id")
                    preserved["planned_actors"] = frame.get("actors")
                    preserved["planned_camera_family"] = frame.get("camera_family")
                plan["images"][index] = preserved
    out.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    review_path = out.with_name("keyframe_visual_reviews.json")
    if review_path.is_file():
        try:
            from .keyframe_visual_gate import build_frame_dispositions
        except ImportError:  # pragma: no cover - direct script entry point
            from keyframe_visual_gate import build_frame_dispositions
        reviews = json.loads(review_path.read_text())
        reviews["frame_dispositions"] = build_frame_dispositions(plan, reviews)
        review_path.write_text(json.dumps(reviews, indent=2, ensure_ascii=False) + "\n")
    print(f"{out}: {plan['keyframe_count']} planned keyframes")


if __name__ == "__main__":
    main()
