"""Make source-preserving local action proposals from generated full-frame art.

The masks are explicit review subjects. Pixel protection is verified; visual
anatomy, contact, and owner selection remain separate gates.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
SCENES = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions"
REVIEW = Path(__file__).resolve().parent

JOBS = [
    {
        "base": "S01-L004-B03-I03_key_acorn_glade_r005_candidate.png",
        "edit": "S01-L004-B03_key_tiny_toothless_contact_r001_candidate.png",
        "output": "S01-L004-B03_key_tiny_toothless_contact_r002_candidate.png",
        "polygon": [(740, 255), (940, 235), (1035, 295), (1050, 555), (895, 585), (770, 520)],
        "reason": "tiny toothless muzzle/acorn/hand contact while preserving the selected scene exterior",
    },
    {
        "base": "S01-L004-B03-I03_key_acorn_glade_r005_candidate.png",
        "edit": "S01-L004-B03-I04_end_tasted_acorn_r001_candidate.png",
        "output": "S01-L004-B03-I04_end_tasted_acorn_r002_candidate.png",
        "polygon": [(740, 255), (940, 235), (1035, 295), (1050, 555), (895, 585), (770, 520)],
        "reason": "closed post-bite muzzle and small shell notch while preserving the selected scene exterior",
    },
    {
        "base": "S02-L004-B02-I02_key_ground_beside_stone_contact_r005_candidate.png",
        "edit": "S02-L004-B02-I03_end_ground_beside_stone_release_r005_candidate.png",
        "output": "S02-L004-B02-I03_end_ground_beside_stone_release_r006_candidate.png",
        "polygon": [(740, 560), (1040, 535), (1090, 815), (750, 835)],
        "reason": "released hands/grounded acorn from the same new contact frame, with exact exterior pixels",
    },
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows = []
    for job in JOBS:
        base_path = SCENES / job["base"]
        edit_path = SCENES / job["edit"]
        target = SCENES / job["output"]
        sidecar = target.with_suffix(".json")
        mask_path = REVIEW / (target.stem + "_allowed_mask.png")
        if target.exists() or sidecar.exists() or mask_path.exists():
            raise FileExistsError(target)
        base = np.asarray(Image.open(base_path).convert("RGB"), dtype=np.float32)
        edit = np.asarray(Image.open(edit_path).convert("RGB"), dtype=np.float32)
        if base.shape != edit.shape:
            raise ValueError("canvas mismatch")
        h, w = base.shape[:2]
        mask = np.zeros((h, w), np.uint8)
        cv2.fillPoly(mask, [np.asarray(job["polygon"], np.int32)], 255)
        dist = cv2.distanceTransform((mask > 0).astype(np.uint8), cv2.DIST_L2, 5)
        weight = np.minimum(dist / 18.0, 1.0)
        result = np.rint(base * (1.0 - weight[..., None]) + edit * weight[..., None]).astype(np.uint8)
        outside = mask == 0
        if not np.array_equal(result[outside], base.astype(np.uint8)[outside]):
            raise AssertionError("protected exterior changed")
        Image.fromarray(mask, "L").save(mask_path)
        Image.fromarray(result, "RGB").save(target)
        row = {
            "schema": "feltwillow.bounded-local-candidate.v1",
            "status": "unselected_technical_candidate_pending_native_review",
            "method": "feathered local source-pixel blend",
            "purpose": job["reason"],
            "base_path": str(base_path.relative_to(ROOT)),
            "base_sha256": sha(base_path),
            "edit_path": str(edit_path.relative_to(ROOT)),
            "edit_sha256": sha(edit_path),
            "allowed_mask_path": str(mask_path.relative_to(ROOT)),
            "allowed_mask_sha256": sha(mask_path),
            "output_path": str(target.relative_to(ROOT)),
            "output_sha256": sha(target),
            "changed_pixels_outside_allowed_mask": 0,
            "provider_calls_added": 0,
            "technical_visual_pass": None,
            "selection": None,
        }
        sidecar.write_text(json.dumps(row, indent=2) + "\n")
        rows.append(row)
    (REVIEW / "BOUNDED_SMALL_ACTIONS.json").write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
