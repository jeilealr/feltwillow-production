"""Local beside-stone contact and release on one selected S02 camera plate."""

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
ORIGINAL = SCENES / "S02-L004-B02-I02_key_stone_acorn_contact_r004_candidate.png"
CONTACT_EDIT = SCENES / "S02-L004-B02-I02_key_ground_beside_stone_contact_r005_candidate.png"
RELEASE_EDIT = SCENES / "S02-L004-B02-I03_end_ground_beside_stone_release_r005_candidate.png"
CONTACT = SCENES / "S02-L004-B02-I02_key_ground_beside_stone_contact_r006_candidate.png"
RELEASE = SCENES / "S02-L004-B02-I03_end_ground_beside_stone_release_r007_candidate.png"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for target in (CONTACT, RELEASE):
        if target.exists() or target.with_suffix(".json").exists():
            raise FileExistsError(target)
    original = np.asarray(Image.open(ORIGINAL).convert("RGB"), dtype=np.float32)
    contact_edit = np.asarray(Image.open(CONTACT_EDIT).convert("RGB"), dtype=np.float32)
    release_edit = np.asarray(Image.open(RELEASE_EDIT).convert("RGB"), dtype=np.float32)
    if original.shape != contact_edit.shape or original.shape != release_edit.shape:
        raise ValueError("canvas mismatch")
    mask = np.zeros(original.shape[:2], np.uint8)
    cv2.fillPoly(mask, [np.asarray([(690, 475), (1100, 475), (1140, 845), (680, 855)], np.int32)], 255)
    distance = cv2.distanceTransform((mask > 0).astype(np.uint8), cv2.DIST_L2, 5)
    weight = np.minimum(distance / 22.0, 1.0)
    mask_path = REVIEW / "s02_beside_stone_contact_release_mask_r001.png"
    if mask_path.exists():
        raise FileExistsError(mask_path)
    Image.fromarray(mask, "L").save(mask_path)
    rows = []
    base = original
    for target, edit, edit_path, role in (
        (CONTACT, contact_edit, CONTACT_EDIT, "hands lower acorn to ground beside stone"),
        (RELEASE, release_edit, RELEASE_EDIT, "hands release grounded acorn"),
    ):
        result = np.rint(base * (1.0 - weight[..., None]) + edit * weight[..., None]).astype(np.uint8)
        if not np.array_equal(result[mask == 0], base.astype(np.uint8)[mask == 0]):
            raise AssertionError("protected exterior changed")
        Image.fromarray(result, "RGB").save(target)
        row = {
            "schema": "feltwillow.bounded-acorn-candidate.v1",
            "status": "unselected_candidate_pending_native_contact_and_seam_review",
            "role": role,
            "base_path": str((ORIGINAL if target == CONTACT else CONTACT).relative_to(ROOT)),
            "base_sha256": sha(ORIGINAL if target == CONTACT else CONTACT),
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
        target.with_suffix(".json").write_text(json.dumps(row, indent=2) + "\n")
        rows.append(row)
        base = result.astype(np.float32)
    (REVIEW / "S02_BESIDE_STONE_BOUNDED.json").write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
