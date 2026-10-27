"""Try selected-source head rise while keeping the original Milo nose pose.

Earlier bounded r002 visibly duplicated Milo and is rejected. This local
proposal uses two selected stills and no new provider call.
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
BASE = SCENES / "S06-L001-B01-I01_start_rest_nose_r001_candidate.png"
RAISED = SCENES / "S06-L001-B02-I02_end_path_arrival_r001_candidate.png"
OUTPUT = SCENES / "S06-L001-B01-I02_head_raised_r003_candidate.png"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blend_mask(shape: tuple[int, int], polygon: list[tuple[int, int]], feather: float) -> tuple[np.ndarray, np.ndarray]:
    mask = np.zeros(shape, np.uint8)
    cv2.fillPoly(mask, [np.asarray(polygon, np.int32)], 255)
    dist = cv2.distanceTransform((mask > 0).astype(np.uint8), cv2.DIST_L2, 5)
    return mask, np.minimum(dist / feather, 1.0)


def main() -> None:
    if OUTPUT.exists() or OUTPUT.with_suffix(".json").exists():
        raise FileExistsError(OUTPUT)
    base = np.asarray(Image.open(BASE).convert("RGB"), dtype=np.float32)
    raised = np.asarray(Image.open(RAISED).convert("RGB"), dtype=np.float32)
    if base.shape != raised.shape:
        raise ValueError("canvas mismatch")
    head_mask, head_weight = blend_mask(base.shape[:2], [(650, 170), (1190, 170), (1230, 540), (1100, 655), (650, 650)], 26.0)
    combined = base * (1 - head_weight[..., None]) + raised * head_weight[..., None]
    # Restore the original nearby Milo and nose-contact foreground. The Leo
    # head transition must still be inspected where these envelopes overlap.
    milo_mask, milo_weight = blend_mask(base.shape[:2], [(1160, 465), (1510, 455), (1540, 795), (1140, 795)], 18.0)
    result = np.rint(combined * (1 - milo_weight[..., None]) + base * milo_weight[..., None]).astype(np.uint8)
    union = (head_mask > 0) | (milo_mask > 0)
    if not np.array_equal(result[~union], base.astype(np.uint8)[~union]):
        raise AssertionError("protected pixels changed")
    Image.fromarray(result, "RGB").save(OUTPUT)
    head_path = REVIEW / "s06_head_raise_r003_head_mask.png"
    milo_path = REVIEW / "s06_head_raise_r003_milo_restore_mask.png"
    Image.fromarray(head_mask, "L").save(head_path)
    Image.fromarray(milo_mask, "L").save(milo_path)
    record = {
        "schema": "feltwillow.local-salvage-candidate.v1",
        "status": "unselected_candidate_pending_native_visual_review",
        "rejected_previous_candidate": "S06-L001-B01-I02_head_raised_r002_candidate.png",
        "rejected_reason": "visibly duplicated Milo at Leo's nose",
        "base_path": str(BASE.relative_to(ROOT)),
        "base_sha256": sha(BASE),
        "raised_reference_path": str(RAISED.relative_to(ROOT)),
        "raised_reference_sha256": sha(RAISED),
        "head_mask_sha256": sha(head_path),
        "milo_restore_mask_sha256": sha(milo_path),
        "output_path": str(OUTPUT.relative_to(ROOT)),
        "output_sha256": sha(OUTPUT),
        "changed_pixels_outside_union": 0,
        "provider_calls_added": 0,
        "technical_visual_pass": None,
        "selection": None,
    }
    OUTPUT.with_suffix(".json").write_text(json.dumps(record, indent=2) + "\n")
    (REVIEW / "S06_HEAD_RAISE_SALVAGE.json").write_text(json.dumps(record, indent=2) + "\n")


if __name__ == "__main__":
    main()
