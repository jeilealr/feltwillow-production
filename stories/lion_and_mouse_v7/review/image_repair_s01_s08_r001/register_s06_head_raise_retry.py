"""Preserve the targeted one-call S06 head-rise replacement and bounded variant."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
SCENES = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions"
REVIEW = Path(__file__).resolve().parent
GENERATED = Path("/Users/lealroja/.codex/generated_images/01a1533f-9137-7e20-a37c-3eeb1ab8afad/exec-62730a20-8d7f-4495-ab33-102dedd020b2.png")
BASE = SCENES / "S06-L001-B01-I01_start_rest_nose_r001_candidate.png"
REFERENCE = SCENES / "S06-L001-B02-I02_end_path_arrival_r001_candidate.png"
RAW = SCENES / "S06-L001-B01-I02_head_raised_r004_candidate.png"
BOUNDED = SCENES / "S06-L001-B01-I02_head_raised_r005_candidate.png"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for target in (RAW, BOUNDED):
        if target.exists() or target.with_suffix(".json").exists():
            raise FileExistsError(target)
    shutil.copy2(GENERATED, RAW)
    raw_record = {
        "schema": "feltwillow.image-candidate-receipt.v1",
        "status": "unselected_candidate_pending_connected_visual_review",
        "purpose": "S06 Leo lifts head while Milo remains at the nose-side position",
        "provider": "image_gen.imagegen",
        "request_count": 1,
        "automatic_retries": 0,
        "cost": "unknown; tool did not expose per-call price",
        "request_id": None,
        "output_path": str(RAW.relative_to(ROOT)),
        "output_sha256": sha(RAW),
        "generation_output_path": str(GENERATED),
        "input_references": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)} for p in (BASE, REFERENCE)],
        "selection": None,
        "technical_visual_pass": None,
    }
    RAW.with_suffix(".json").write_text(json.dumps(raw_record, indent=2) + "\n")
    base = np.asarray(Image.open(BASE).convert("RGB"), dtype=np.float32)
    raw = np.asarray(Image.open(RAW).convert("RGB"), dtype=np.float32)
    if base.shape != raw.shape:
        raise ValueError("canvas mismatch")
    mask = np.zeros(base.shape[:2], np.uint8)
    cv2.fillPoly(mask, [np.asarray([(635, 170), (1210, 160), (1260, 620), (1100, 665), (630, 650)], np.int32)], 255)
    dist = cv2.distanceTransform((mask > 0).astype(np.uint8), cv2.DIST_L2, 5)
    weight = np.minimum(dist / 24.0, 1.0)
    result = np.rint(base * (1 - weight[..., None]) + raw * weight[..., None]).astype(np.uint8)
    if not np.array_equal(result[mask == 0], base.astype(np.uint8)[mask == 0]):
        raise AssertionError("protected exterior changed")
    Image.fromarray(result, "RGB").save(BOUNDED)
    mask_path = REVIEW / "s06_head_raise_r005_allowed_mask.png"
    Image.fromarray(mask, "L").save(mask_path)
    record = {
        "schema": "feltwillow.bounded-connected-candidate.v1",
        "status": "unselected_candidate_pending_native_seam_and_actor_review",
        "base_path": str(BASE.relative_to(ROOT)),
        "base_sha256": sha(BASE),
        "edit_path": str(RAW.relative_to(ROOT)),
        "edit_sha256": sha(RAW),
        "allowed_mask_path": str(mask_path.relative_to(ROOT)),
        "allowed_mask_sha256": sha(mask_path),
        "output_path": str(BOUNDED.relative_to(ROOT)),
        "output_sha256": sha(BOUNDED),
        "changed_pixels_outside_allowed_mask": 0,
        "provider_calls_added": 0,
        "selection": None,
        "technical_visual_pass": None,
    }
    BOUNDED.with_suffix(".json").write_text(json.dumps(record, indent=2) + "\n")
    (REVIEW / "S06_HEAD_RAISE_R005.json").write_text(json.dumps(record, indent=2) + "\n")


if __name__ == "__main__":
    main()
