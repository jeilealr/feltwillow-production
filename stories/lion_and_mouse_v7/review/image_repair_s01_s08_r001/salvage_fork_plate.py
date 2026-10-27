"""Propose a wider, feathered local blend of the already-returned S03 plate.

This is an unselected technical experiment. It makes no provider call and does
not overwrite the first bounded candidate or its receipt.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
REVIEW = Path(__file__).resolve().parent
SOURCE = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L001-B01-I02_end_homeward_distance_r004_candidate.png"
ORIGINAL_MASK = ROOT / "stories/lion_and_mouse_v7/review/sequence_readiness_r001/fork_turn_preparation_r001/milo_removal_allowed_mask.png"
RAW = REVIEW / "s03_fork_clean_plate_raw_provider_r001.png"
PROPOSED_MASK = REVIEW / "fork_clean_plate_allowed_mask_r002_proposed.png"
TARGET = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L001-B01_location_fork_clean_plate_r002_candidate.png"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if TARGET.exists() or PROPOSED_MASK.exists():
        raise FileExistsError("proposal already exists")
    source = np.asarray(Image.open(SOURCE).convert("RGB"), dtype=np.float32)
    raw = np.asarray(Image.open(RAW).convert("RGB"), dtype=np.float32)
    original = np.asarray(Image.open(ORIGINAL_MASK).convert("L")) > 0
    if source.shape != raw.shape or original.shape != source.shape[:2]:
        raise ValueError("input canvas mismatch")
    proposed = cv2.dilate(original.astype(np.uint8), np.ones((91, 91), np.uint8)) > 0
    # All pixels outside the proposed envelope remain byte-identical to source.
    distance = cv2.distanceTransform(proposed.astype(np.uint8), cv2.DIST_L2, 5)
    weight = np.clip(distance / 24.0, 0.0, 1.0)
    weight[original] = 1.0
    result = np.rint(source * (1.0 - weight[..., None]) + raw * weight[..., None]).astype(np.uint8)
    if not np.array_equal(result[~proposed], source.astype(np.uint8)[~proposed]):
        raise AssertionError("protected pixels changed")
    Image.fromarray((proposed * 255).astype(np.uint8), "L").save(PROPOSED_MASK)
    Image.fromarray(result, "RGB").save(TARGET)
    record = {
        "status": "local_technical_candidate_pending_mask_review_not_selected",
        "source_sha256": sha(SOURCE),
        "raw_provider_sha256": sha(RAW),
        "original_mask_sha256": sha(ORIGINAL_MASK),
        "proposed_mask_sha256": sha(PROPOSED_MASK),
        "candidate_sha256": sha(TARGET),
        "changed_pixels_outside_proposed_mask": 0,
        "mask_dilation_square_px": 91,
        "feather_distance_px": 24,
        "provider_calls_added": 0,
        "next_gate": "native seam/tail/background review before any technical use; expanded region is not the original approved mask",
    }
    TARGET.with_suffix(".json").write_text(json.dumps(record, indent=2) + "\n")
    (REVIEW / "S03_CLEAN_PLATE_SALVAGE.json").write_text(json.dumps(record, indent=2) + "\n")


if __name__ == "__main__":
    main()
