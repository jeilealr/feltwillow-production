#!/usr/bin/env python3
"""Build individual v6 keyframe records from the audio and staging contracts.

The resulting images remain owner-review candidates until visual approval. This
script only writes the plan; image generation is an explicit separate step.
"""

from __future__ import annotations

import argparse
import json
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


def build(story: str) -> dict:
    home = REPO / "stories" / story
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
                "dialogue_speakers": [],
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
        if "acorn" in action.lower():
            prop = bible["props"]["acorn"]["reference"]
        elif (frame["scene"] in (11, 13, 14) or
              (frame["scene"] == 10 and fid != "s10_p01") or
              any(word in action.lower() for word in ("net", "rope", "strand", "mesh", "fibre", "fiber"))):
            prop = bible["props"]["hunter_net"]["reference"]
        view = frame["view"]
        crop = crop_for_frame(frame, staging["views"][view]["magnification"])
        reference_plate = (frame["plate"] if crop == [0.0, 0.0, 1.0, 1.0] else
                           f"work/stories/{story}/keyframe_plate_crops/{fid}.png")
        refs = [reference_plate]
        for actor in ("leo", "milo"):
            if actor in frame["actors"]:
                refs.append(bible["characters"][actor]["canonical"])
        if prop:
            refs.append(prop)
        if len(frame["actors"]) > 1 and len(refs) < 5:
            refs.append(boards[fid])
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
        identities = []
        if "milo" in frame["actors"]:
            identities.append("Milo is compact grey felt with green eyes and both ears fully visible in full-body views")
        if "leo" in frame["actors"]:
            identities.append("Leo is tawny felt, quadrupedal, with planted paws unless explicitly lying down")
        if len(frame["actors"]) == 2:
            identities.append("At equal depth Milo's standing height is about 40% of Leo's mane-to-paw height")
        count_word = {0: "NO animals", 1: "exactly ONE animal", 2: "exactly TWO animals"}[len(frame["actors"])]
        net_continuity = ""
        if "leo" in frame["actors"] and (frame["scene"] in (11, 13) or
                (frame["scene"] == 10 and fid != "s10_p01") or
                (frame["scene"] == 14 and fid != "s14_p06")):
            net_continuity = ("Leo remains trapped under the SAME flax-rope diamond-mesh net, "
                              "held on his body and hindquarters; his face and muzzle remain clear. "
                              "The one closure loop is at his flank. Do not free Leo or leave only a "
                              "loose rope pile before s14_p06. ")
        elif fid == "s14_p06":
            net_continuity = "This is the ONLY escape beat: Leo steps out and the parted net falls behind him. "
        elif frame["scene"] == 15 and "leo" in frame["actors"]:
            net_continuity = "Leo is now free; the discarded net stays behind both characters on the trap path. "
        board_note = (f"The last attached storyboard is a pose guide for panel {fid} only, "
                      "never a source of background geography. " if boards[fid] in refs else "")
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
        prompt = (f"Edit reference image 1 into ONE full-frame 16:9 production video keyframe for "
                  f"{story}, audio scene {frame['scene']:02d}, {fid}. Keep its registered {view} "
                  "crop, landmarks, camera, lighting and walkable ground fixed. Add "
                  f"{count_word}. {board_note}Action: {prompt_action} "
                  f"Placement: {'; '.join(people) if people else 'empty approved location view'}. "
                  f"Identity: {'; '.join(identities) if identities else 'no cast'}. "
                  f"{net_continuity}{detail_rule}"
                  "Add only story props necessary for this action. Keep mouths closed in this "
                  "boundary keyframe; only character dialogue receives separate lip-sync later. "
                  "Preserve matte handmade needle-felt texture. Do not zoom out, reveal more "
                  "scenery, add bags, pouches, clothing, accessories, any other animal, "
                  "redesign the plate, add captions, letters, "
                  "speech bubbles, a narrator figure, borders or multiple panels.")
        images.append({
            "id": fid,
            "scene": frame["scene"],
            "audio_line_ids": lines,
            "visual_unit_ids": unit_ids,
            "status": "planned",
            "candidate_path": f"character/characters/{story}/interactions/keyframes/{fid}_r01_candidate.png",
            "approved_plate": frame["plate"],
            "reference_plate": reference_plate,
            "board_reference": boards[fid],
            "view": view,
            "crop_rect_on_plate": crop,
            "staging_ref": fid,
            "references": refs,
            "action": action,
            "dialogue_speakers": panel["dialogue_speakers"],
            "prompt": prompt,
        })
    return {
        "revision": "2026-10-11-r01",
        "story": story,
        "status": "production_keyframe_candidates_pending_owner_review",
        "prompt_policy": "Prompts on generated records are historical provenance, not approved reusable generation instructions. Build a new revision from current staging and re-review its result.",
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
                             "crop_rect_on_plate", "staging_ref")
                changed = [key for key in immutable if old.get(key) != frame.get(key)]
                if changed:
                    raise SystemExit(f"{frame['id']}: generated candidate has stale staging "
                                     f"({', '.join(changed)}); revise and review it explicitly")
                # The exact prompt, ordered references and crop are provenance
                # for the existing image. Never overwrite them on a re-plan.
                plan["images"][index] = old
    out.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    print(f"{out}: {plan['keyframe_count']} planned keyframes")


if __name__ == "__main__":
    main()
