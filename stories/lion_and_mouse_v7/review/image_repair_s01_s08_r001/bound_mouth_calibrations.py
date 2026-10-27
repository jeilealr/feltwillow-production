"""Constrain actor speech calibrations to their source-mouth regions only."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
EXPRESSIONS = ROOT / "character/characters/lion_and_mouse_v7"
REVIEW = Path(__file__).resolve().parent

JOBS = [
    {
        "actor": "Milo",
        "closed": "Milo/expressions/milo_portrait_base_3q_default_r003_candidate.png",
        "generated": "Milo/expressions/milo_portrait_base_3q_default_tiny_open_toothless_r001_candidate.png",
        "target": "Milo/expressions/milo_portrait_base_3q_default_tiny_open_toothless_r002_candidate.png",
        "ellipse": (890, 753, 130, 82),
    },
    {
        "actor": "Leo",
        "closed": "Leo/expressions/leo_portrait_base_3q_r001_candidate.png",
        "generated": "Leo/expressions/leo_portrait_base_3q_tiny_open_toothless_r001_candidate.png",
        "target": "Leo/expressions/leo_portrait_base_3q_tiny_open_toothless_r002_candidate.png",
        "ellipse": (778, 750, 130, 75),
    },
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows = []
    for job in JOBS:
        source = EXPRESSIONS / job["closed"]
        generated = EXPRESSIONS / job["generated"]
        target = EXPRESSIONS / job["target"]
        mask_path = REVIEW / (target.stem + "_mouth_roi.png")
        if target.exists() or target.with_suffix(".json").exists() or mask_path.exists():
            raise FileExistsError(target)
        closed = np.asarray(Image.open(source).convert("RGBA"), dtype=np.float32)
        opened = np.asarray(Image.open(generated).convert("RGBA"), dtype=np.float32)
        if closed.shape != opened.shape:
            raise ValueError("calibration canvas mismatch")
        height, width = closed.shape[:2]
        mask = np.zeros((height, width), np.uint8)
        center_x, center_y, radius_x, radius_y = job["ellipse"]
        cv2.ellipse(mask, (center_x, center_y), (radius_x, radius_y), 0, 0, 360, 255, -1)
        dist = cv2.distanceTransform((mask > 0).astype(np.uint8), cv2.DIST_L2, 5)
        weight = np.minimum(dist / 12.0, 1.0)
        # Alpha remains exactly the selected closed-source alpha everywhere.
        result = np.rint(closed).astype(np.uint8)
        result[:, :, :3] = np.rint(closed[:, :, :3] * (1 - weight[..., None]) + opened[:, :, :3] * weight[..., None]).astype(np.uint8)
        if not np.array_equal(result[mask == 0], closed.astype(np.uint8)[mask == 0]):
            raise AssertionError("non-mouth pixels changed")
        if not np.array_equal(result[:, :, 3], closed.astype(np.uint8)[:, :, 3]):
            raise AssertionError("alpha changed")
        Image.fromarray(mask, "L").save(mask_path)
        Image.fromarray(result, "RGBA").save(target)
        row = {
            "schema": "feltwillow.mouth-calibration-candidate.v1",
            "actor": job["actor"],
            "status": "unselected_auxiliary_candidate_pending_angle_and_mouth_review",
            "closed_source_path": str(source.relative_to(ROOT)),
            "closed_source_sha256": sha(source),
            "generated_open_path": str(generated.relative_to(ROOT)),
            "generated_open_sha256": sha(generated),
            "mouth_roi_path": str(mask_path.relative_to(ROOT)),
            "mouth_roi_sha256": sha(mask_path),
            "output_path": str(target.relative_to(ROOT)),
            "output_sha256": sha(target),
            "outside_roi_changed_pixels": 0,
            "alpha_changed_pixels": 0,
            "provider_calls_added": 0,
            "selection": None,
        }
        target.with_suffix(".json").write_text(json.dumps(row, indent=2) + "\n")
        rows.append(row)
    (REVIEW / "BOUNDED_MOUTH_CALIBRATIONS.json").write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
