"""Freeze references and the positive edit instructions for five manual redos."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SCENES = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions"
GENERATED = Path("/Users/lealroja/.codex/generated_images/01a1533f-9137-7e20-a37c-3eeb1ab8afad")

OPERATIONS = [
    {
        "output": "exec-f5656329-0cb0-473a-9e4c-ea1c6d9da1c7.png",
        "references": ["S05-L009-B01-I03_local_roll_r002_candidate.png", "S05-L009-B01-I04_grounded_nose_landing_r002_candidate.png"],
        "prompt": "Repair the final landing still in a connected felt/plush animation. First image is the exact camera/background and Leo sleeping pose to preserve. Second image is the approved preceding Milo roll and defines Milo's anatomy, scale and tail. Make the next physical state after that roll: ONE complete Milo mouse lying naturally on his side on the grass immediately in front of Leo's nose/front paws, fully supported by the ground, compact torso, one head, two ears, two arms, two legs, one tail attached at the rump; limbs at plausible joints with no stretched body or duplicate parts. His nose rests near Leo's nose without penetrating Leo's paw. Leo remains asleep with exactly four anatomically attached paws, same body, mane, head and exact position. Preserve tree/sky/path/camera/light. Change only Milo's local pose and contact shadow; do not enlarge or shrink either character. No teeth, no text.",
    },
    {
        "output": "exec-28391ecf-6e41-4df8-ac92-93140e80f6ab.png",
        "references": ["S06-L001-B01-I02_head_raised_r005_candidate.png", "S06-L001-B02-I02_end_path_arrival_r001_candidate.png"],
        "prompt": "Create a single in-between frame for this exact locked-camera felt/plush film scene. Image 1 is the preceding pose: Leo lies under the tree with head raised, Milo is beside his nose. Image 2 is the later pose: Milo has arrived at the path. Show the intermediate moment in which Milo scrambles down from beside Leo's nose toward his own destination on the path at screen right, still facing/looking at Leo, with a natural compact mouse body and four attached mouse limbs, at least one foot grounded and another stepping. Keep Milo's identity, head size, ears, chest, tail and overall scale consistent with both references. Leo remains lying in the SAME pose and location as image 1 with all paws intact and no body deformation. Exact fixed background/camera/tree/sunset. One mouse, one lion, no extra paws or hands, no teeth, no text. Make a normal believable stepping pose, not a floating, hunched or stretched body.",
    },
    {
        "output": "exec-17536e00-ed6a-47ea-ac03-4c739f018574.png",
        "references": ["S06-L001-B02-I02_end_path_arrival_r001_candidate.png", "S06-L002-B01-I03_end_front_paw_block_r001_candidate.png"],
        "prompt": "Edit this exact felt/plush scene as the BEFORE state of the lion's front-paw block. Preserve the whole lion Leo body, head, mane, back, hind legs, tail and mouse Milo exactly like reference image 1; preserve fixed tree/forest/sunset/camera and their scale/root positions. Image 2 shows the later blocking endpoint and identifies the SAME one front foreleg on Leo's screen-right side (the long foreleg nearest Milo). In this new before state, that foreleg is still safely planted near Leo's chest but its paw is just beginning to lift, moving toward Milo; the shoulder, elbow, wrist and rounded paw form one anatomically continuous limb. His other three paws remain exactly in their existing places. Milo stands at viewer-right with exactly the same body, feet and expression as reference 1, no body distortion. Do not add an extra paw or remove the planted source paw; do not change Leo's head or torso. No teeth, no text.",
    },
    {
        "output": "exec-05453750-fb59-485e-a5c6-ba1397d0f0ac.png",
        "references": ["exec-17536e00-ed6a-47ea-ac03-4c739f018574.png", "S06-L002-B01-I03_end_front_paw_block_r001_candidate.png"],
        "prompt": "Produce the MIDDLE key of one continuous Leo front-paw blocking action in the same locked-camera felt/plush scene. Use image 1 for the beginning and image 2 for the final paw on the ground beside Milo. Keep Leo's exact head, mane, torso, hindquarters, tail and the other three paws; keep Milo's exact upright mouse anatomy, root, feet, face and scale; same tree/sky/ground/camera. Animate ONLY Leo's one screen-right front foreleg: it extends naturally from the existing shoulder, paw halfway between raised position and its final planted block next to Milo. One continuous shoulder-elbow-wrist-paw shape with no duplicate stump or fifth paw; the near front paw and both rear paws remain grounded and unchanged. Milo is not touched or deformed. No missing paw, no extra limbs, no teeth, no text.",
    },
    {
        "output": "exec-0446e6d7-af77-44d4-aeda-959707f213fe.png",
        "references": ["S08-L016-B01-I01_single_gentle_clear_r001_candidate.png", "S08-L001-B01-I01_start_restrained_blocked_r001_candidate.png"],
        "prompt": "Precise anatomy repair to IMAGE 1, the source frame. Preserve image 1's exact Leo head, mane, lying torso, tail, Milo, sunset tree and camera. Leo must have exactly FOUR attached paws: two rear paws at image-left as already present, the near front paw in front of his chest as already present, AND a second FAR FRONT PAW extending from behind his chest toward the upper-right of Leo's body, visible on the ground just to image-left of Milo's feet (around x=1130-1210, y=680-750 in the 1672x941 frame). This is the missing image-top-right paw the owner identifies. Give that paw a continuous golden foreleg attached at Leo's shoulder, rounded cream toes and ground-contact shadow. IMAGE 2 shows how that far foreleg and paw project in the same tree setting; copy its limb topology but keep IMAGE 1's softer Leo pose and existing camera. Do not merely reshape the existing near paw or create a fifth paw; the far paw must be separately visible to the right of the near paw. Milo remains unchanged, fully visible with no overlap/extra limbs. No teeth, claws, text or scene redraw.",
    },
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    output = []
    for item in OPERATIONS:
        target = GENERATED / item["output"]
        refs = []
        for name in item["references"]:
            path = GENERATED / name if name.startswith("exec-") else SCENES / name
            refs.append({"path": str(path), "sha256": sha(path)})
        output.append({
            "operation": "one_manual_image_edit_call",
            "provider_output": str(target),
            "provider_output_sha256": sha(target),
            "ordered_references": refs,
            "prompt": item["prompt"],
            "automatic_retry_count": 0,
            "provider_request_id": None,
            "cost": None,
            "selection": None,
        })
    (HERE / "OWNER_REDO_GENERATION.json").write_text(json.dumps({
        "schema": "feltwillow.owner-redo-generation.v1",
        "date": "2026-10-27",
        "calls": output,
        "note": "Five owner-directed manual redo calls; two narrower-mask local revisions used no extra provider call.",
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
