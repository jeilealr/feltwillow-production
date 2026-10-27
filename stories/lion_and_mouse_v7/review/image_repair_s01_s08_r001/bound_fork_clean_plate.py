"""Bound one returned S03 operator plate to the preapproved reconstruction mask."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
REVIEW = Path(__file__).resolve().parent
SOURCE = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L001-B01-I02_end_homeward_distance_r004_candidate.png"
MASK = ROOT / "stories/lion_and_mouse_v7/review/sequence_readiness_r001/fork_turn_preparation_r001/milo_removal_allowed_mask.png"
RAW = REVIEW / "s03_fork_clean_plate_raw_provider_r001.png"
TARGET = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L001-B01_location_fork_clean_plate_r001_candidate.png"
EXPECTED = {
    SOURCE: "5163cea0a436d27ec4b1ea4a16c857b5ffdb504a0309d587fe34d84a7d2beee6",
    MASK: "f601c6c086532dac8c630c97995aa009701a0dd735d7398172a11b052f312888",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for path, expected in EXPECTED.items():
        if sha(path) != expected:
            raise ValueError(f"changed input: {path}")
    if TARGET.exists():
        raise FileExistsError(TARGET)
    with Image.open(SOURCE) as image:
        source = np.asarray(image.convert("RGB"))
    with Image.open(RAW) as image:
        if image.mode != "RGB" or image.size != (1672, 941):
            raise ValueError("returned candidate has unexpected mode/canvas")
        returned = np.asarray(image)
    with Image.open(MASK) as image:
        mask = np.asarray(image.convert("L"))
    if mask.shape != source.shape[:2] or not np.isin(mask, [0, 255]).all():
        raise ValueError("mask is not exact binary canvas")
    editable = mask == 255
    output = source.copy()
    output[editable] = returned[editable]
    if np.any(output[~editable] != source[~editable]):
        raise AssertionError("protected pixels changed")
    Image.fromarray(output, "RGB").save(TARGET)
    record = {
        "schema": "feltwillow.image-candidate-receipt.v1",
        "operation_id": "s03-common-fork-clean-plate-r001",
        "status": "candidate_pending_technical_review_not_owner_selected",
        "provider": "image_gen.imagegen",
        "request_count": 1,
        "automatic_retries": 0,
        "request_id": None,
        "cost": "unknown; tool did not expose per-call cost",
        "source_path": str(SOURCE.relative_to(ROOT)),
        "source_sha256": sha(SOURCE),
        "mask_path": str(MASK.relative_to(ROOT)),
        "mask_sha256": sha(MASK),
        "raw_path": str(RAW.relative_to(ROOT)),
        "raw_sha256": sha(RAW),
        "candidate_path": str(TARGET.relative_to(ROOT)),
        "candidate_sha256": sha(TARGET),
        "canvas": [1672, 941],
        "rgb_mode": True,
        "editable_pixels": int(editable.sum()),
        "protected_pixels": int((~editable).sum()),
        "protected_pixel_differences": 0,
        "prompt_ref": str((REVIEW / "FIRST_OPERATION_PACKET.md").relative_to(ROOT)),
        "approval_ref": "owner message 2026-10-25: I approve. go ahead and repair them all; first-operation packet previously shown",
        "next_gate": "native/fitted seam and geography review; still not selected story art",
    }
    TARGET.with_suffix(".json").write_text(json.dumps(record, indent=2) + "\n")
    (REVIEW / "S03_CLEAN_PLATE_RESULT.json").write_text(json.dumps(record, indent=2) + "\n")


if __name__ == "__main__":
    main()
