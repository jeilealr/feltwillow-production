"""Propose locally bounded S05/S06 action edits against selected scene anchors.

These preserve exact exterior pixels but remain unselected and require native
actor/ground-contact/seam review. A failed raw state is not made valid merely
by compositing it.
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
    ("S05-L008-B01-I02_key_first_joint_rear_paw_contact_r004_candidate.png", "S05-L008-B01-I01_grounded_approach_r001_candidate.png", "S05-L008-B01-I01_grounded_approach_r002_candidate.png", [(35, 315), (1530, 275), (1570, 790), (50, 820)], "approach; paw chronology still pending"),
    ("S05-L008-B01-I02_key_first_joint_rear_paw_contact_r004_candidate.png", "S05-L008-B01-I03_forward_pitch_r001_candidate.png", "S05-L008-B01-I03_forward_pitch_r002_candidate.png", [(35, 315), (1530, 275), (1570, 790), (50, 820)], "pitch; paw collision/scale still pending"),
    ("S05-L009-B01-I03_local_roll_r002_candidate.png", "S05-L009-B01-I04_grounded_nose_landing_r001_candidate.png", "S05-L009-B01-I04_grounded_nose_landing_r002_candidate.png", [(35, 315), (1530, 275), (1570, 790), (50, 820)], "nose landing; roll trajectory still pending"),
    ("S06-L001-B01-I01_start_rest_nose_r001_candidate.png", "S06-L001-B01-I02_head_raised_r001_candidate.png", "S06-L001-B01-I02_head_raised_r002_candidate.png", [(650, 170), (1220, 150), (1300, 610), (630, 650)], "head rise; check mane/body junction"),
    ("S06-L002-B01-I03_end_front_paw_block_r001_candidate.png", "S06-L002-B01-I01_front_paw_ready_r001_candidate.png", "S06-L002-B01-I01_front_paw_ready_r002_candidate.png", [(735, 515), (1320, 500), (1330, 815), (710, 820)], "front paw ready; check attached foreleg and removed planted paw"),
    ("S06-L002-B01-I03_end_front_paw_block_r001_candidate.png", "S06-L002-B01-I02_front_paw_descending_r001_candidate.png", "S06-L002-B01-I02_front_paw_descending_r002_candidate.png", [(735, 515), (1320, 500), (1330, 815), (710, 820)], "front paw descent; check attached foreleg and support"),
    ("S06-L002-B01-I03_end_front_paw_block_r001_candidate.png", "S06-L003-B01-I02_frozen_r001_candidate.png", "S06-L003-B01-I02_frozen_r002_candidate.png", [(1140, 370), (1540, 370), (1540, 690), (1150, 690)], "Milo freeze; check face/neck/ear seam"),
    ("S06-L002-B01-I03_end_front_paw_block_r001_candidate.png", "S06-L004-B01-I02_worried_r001_candidate.png", "S06-L004-B01-I02_worried_r002_candidate.png", [(1140, 370), (1540, 370), (1540, 690), (1150, 690)], "Milo worry; check face/neck/ear seam"),
    ("S06-L002-B01-I03_end_front_paw_block_r001_candidate.png", "S06-L005-B01-I02_humbled_r001_candidate.png", "S06-L005-B01-I02_humbled_r002_candidate.png", [(1140, 370), (1540, 370), (1540, 690), (1150, 690)], "Milo humbled; check face/neck/ear seam"),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows = []
    for base_name, edit_name, output_name, polygon, review_note in JOBS:
        base_path = SCENES / base_name
        edit_path = SCENES / edit_name
        output_path = SCENES / output_name
        mask_path = REVIEW / (output_path.stem + "_allowed_mask.png")
        if output_path.exists() or output_path.with_suffix(".json").exists() or mask_path.exists():
            raise FileExistsError(output_path)
        base = np.asarray(Image.open(base_path).convert("RGB"), dtype=np.float32)
        edit = np.asarray(Image.open(edit_path).convert("RGB"), dtype=np.float32)
        if base.shape != edit.shape:
            raise ValueError(edit_path)
        mask = np.zeros(base.shape[:2], np.uint8)
        cv2.fillPoly(mask, [np.asarray(polygon, np.int32)], 255)
        distance = cv2.distanceTransform((mask > 0).astype(np.uint8), cv2.DIST_L2, 5)
        weight = np.minimum(distance / 28.0, 1.0)
        result = np.rint(base * (1.0 - weight[..., None]) + edit * weight[..., None]).astype(np.uint8)
        if not np.array_equal(result[mask == 0], base.astype(np.uint8)[mask == 0]):
            raise AssertionError("protected exterior changed")
        Image.fromarray(mask, "L").save(mask_path)
        Image.fromarray(result, "RGB").save(output_path)
        row = {
            "schema": "feltwillow.bounded-connected-candidate.v1",
            "status": "unselected_technical_candidate_pending_native_review",
            "base_path": str(base_path.relative_to(ROOT)),
            "base_sha256": sha(base_path),
            "edit_path": str(edit_path.relative_to(ROOT)),
            "edit_sha256": sha(edit_path),
            "allowed_mask_path": str(mask_path.relative_to(ROOT)),
            "allowed_mask_sha256": sha(mask_path),
            "output_path": str(output_path.relative_to(ROOT)),
            "output_sha256": sha(output_path),
            "changed_pixels_outside_allowed_mask": 0,
            "review_note": review_note,
            "provider_calls_added": 0,
            "technical_visual_pass": None,
            "selection": None,
        }
        output_path.with_suffix(".json").write_text(json.dumps(row, indent=2) + "\n")
        rows.append(row)
    (REVIEW / "BOUNDED_TRIP_AND_BLOCK.json").write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
