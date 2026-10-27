"""Propose a local, source-preserving paw revision from one generated edit."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
REVIEW = Path(__file__).resolve().parent
SOURCE = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions/S08-L016-B01-I01_single_gentle_clear_r001_candidate.png"
GENERATED = Path("/Users/lealroja/.codex/generated_images/01a1533f-9137-7e20-a37c-3eeb1ab8afad/exec-5c6db285-d82b-4ddd-8f63-d2e7a96e6018.png")
RAW = REVIEW / "s08_paw_raw_provider_r002.png"
MASK = REVIEW / "s08_paw_local_envelope_r002_proposed.png"
TARGET = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions/S08-L016-B01-I01_single_gentle_clear_r002_candidate.png"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if any(path.exists() for path in (RAW, MASK, TARGET, TARGET.with_suffix(".json"))):
        raise FileExistsError("operation already saved")
    if sha(SOURCE) != "516ea912c1a726927232e3e6df83a7e7f9eb3a3f54719e24a148f60c6dd94604":
        raise ValueError("selected r001 input changed")
    source = np.asarray(Image.open(SOURCE).convert("RGB"), dtype=np.float32)
    raw = np.asarray(Image.open(GENERATED).convert("RGB"), dtype=np.float32)
    if raw.shape != source.shape:
        raise ValueError("returned canvas changed")
    polygon = np.array([[913, 628], [961, 587], [1134, 563], [1200, 598], [1224, 672], [1207, 766], [1087, 798], [955, 784], [912, 734]], np.int32)
    local = np.zeros(source.shape[:2], dtype=np.uint8)
    cv2.fillPoly(local, [polygon], 255)
    distance = cv2.distanceTransform((local > 0).astype(np.uint8), cv2.DIST_L2, 5)
    weight = np.clip(distance / 25.0, 0.0, 1.0)
    output = np.rint(source * (1 - weight[..., None]) + raw * weight[..., None]).astype(np.uint8)
    protected = local == 0
    if not np.array_equal(output[protected], source.astype(np.uint8)[protected]):
        raise AssertionError("protected pixels changed")
    shutil.copy2(GENERATED, RAW)
    Image.fromarray(local, "L").save(MASK)
    Image.fromarray(output, "RGB").save(TARGET)
    record = {
        "schema": "feltwillow.image-candidate-receipt.v1",
        "status": "unselected_anatomy_and_mask_review_pending",
        "role": "S08-L016 far forepaw visibility repair, shared later by L017/L018 only after exact selection",
        "provider": "image_gen.imagegen",
        "request_count": 1,
        "automatic_retries": 0,
        "cost": "unknown; tool did not expose per-call price",
        "source_path": str(SOURCE.relative_to(ROOT)),
        "source_sha256": sha(SOURCE),
        "raw_path": str(RAW.relative_to(ROOT)),
        "raw_sha256": sha(RAW),
        "candidate_path": str(TARGET.relative_to(ROOT)),
        "candidate_sha256": sha(TARGET),
        "local_mask_path": str(MASK.relative_to(ROOT)),
        "local_mask_sha256": sha(MASK),
        "protected_pixel_differences": 0,
        "changed_region": "far foreleg/paw and contact shadow only; local mask is a new review proposal",
        "owner_selection": None,
        "technical_visual_pass": None,
    }
    TARGET.with_suffix(".json").write_text(json.dumps(record, indent=2) + "\n")
    (REVIEW / "S08_PAW_RESULT.json").write_text(json.dumps(record, indent=2) + "\n")


if __name__ == "__main__":
    main()
