"""Register one targeted rear-paw contact edit and bound it to the selected camera."""

import hashlib
import json
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
REVIEW = Path(__file__).resolve().parent
SCENES = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions"
PROVIDER = Path("/Users/lealroja/.codex/generated_images/01a1533f-9137-7e20-a37c-3eeb1ab8afad/exec-c44153ec-d673-48e4-8ec4-2e7af311aee7.png")
BASE = SCENES / "S05-L008-B01-I02_key_first_joint_rear_paw_contact_r004_candidate.png"
RAW = SCENES / "S05-L008-B01-I02_key_first_joint_rear_paw_contact_r005_candidate.png"
OUT = SCENES / "S05-L008-B01-I02_key_first_joint_rear_paw_contact_r006_candidate.png"
MASK = REVIEW / "s05_rear_paw_contact_r006_allowed_mask.png"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    for path in (RAW, OUT, MASK, RAW.with_suffix(".json"), OUT.with_suffix(".json")):
        if path.exists():
            raise FileExistsError(path)
    shutil.copyfile(PROVIDER, RAW)
    source = np.asarray(Image.open(BASE).convert("RGB"), dtype=np.float32)
    edit = np.asarray(Image.open(RAW).convert("RGB"), dtype=np.float32)
    if source.shape != edit.shape:
        raise ValueError("source/edit dimensions differ")
    allowed = np.zeros(source.shape[:2], np.uint8)
    cv2.fillPoly(allowed, [np.asarray([(45, 305), (730, 305), (800, 790), (50, 825)], np.int32)], 255)
    distance = cv2.distanceTransform((allowed > 0).astype(np.uint8), cv2.DIST_L2, 5)
    weight = np.minimum(distance / 24.0, 1.0)
    result = np.rint(source * (1 - weight[..., None]) + edit * weight[..., None]).astype(np.uint8)
    if not np.array_equal(result[allowed == 0], source.astype(np.uint8)[allowed == 0]):
        raise AssertionError("protected exterior changed")
    Image.fromarray(allowed, "L").save(MASK)
    Image.fromarray(result, "RGB").save(OUT)
    common = {
        "schema": "feltwillow.bounded-connected-candidate.v1",
        "status": "unselected_candidate_pending_native_contact_and_anatomy_review",
        "base_path": str(BASE.relative_to(ROOT)),
        "base_sha256": sha(BASE),
        "edit_path": str(RAW.relative_to(ROOT)),
        "edit_sha256": sha(RAW),
        "provider_output_path": str(PROVIDER),
        "provider_output_sha256": sha(PROVIDER),
        "provider_calls": 1,
        "automatic_retries": 0,
        "request_id": None,
        "cost": None,
        "selection": None,
        "technical_visual_pass": None,
    }
    RAW.with_suffix(".json").write_text(json.dumps({**common, "output_path": str(RAW.relative_to(ROOT)), "output_sha256": sha(RAW), "bounded": False}, indent=2) + "\n")
    bounded = {**common,
        "allowed_mask_path": str(MASK.relative_to(ROOT)),
        "allowed_mask_sha256": sha(MASK),
        "output_path": str(OUT.relative_to(ROOT)),
        "output_sha256": sha(OUT),
        "changed_pixels_outside_allowed_mask": 0,
        "review_note": "Leading Milo foot must visibly catch on Leo's rear paw before forward pitch. Check toe/paw overlap and grounded trailing foot.",
    }
    OUT.with_suffix(".json").write_text(json.dumps(bounded, indent=2) + "\n")
    (REVIEW / "S05_REAR_PAW_CONTACT_R006.json").write_text(json.dumps(bounded, indent=2) + "\n")


if __name__ == "__main__":
    main()
