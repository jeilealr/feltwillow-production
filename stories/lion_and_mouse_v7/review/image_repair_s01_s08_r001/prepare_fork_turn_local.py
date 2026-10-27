"""Propose fixed-root fork turn composites from selected view-compatible heads.

This is a local visual experiment, not an approval or an exact-background pass
inside the head envelope. The protected scene and Milo's feet/body root remain
the accepted L001 r004 pixels outside the declared head/neck envelope.
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
BASE = SCENES / "S03-L001-B01-I02_end_homeward_distance_r004_candidate.png"

SOURCES = [
    ("S03-L002-B01-I02_end_two_routes_r003_candidate.png", "S03-L002-B01-I02_locked_local_head_r004_candidate.png"),
    ("S03-L003-B01-I02_end_safe_left_meadow_r003_candidate.png", "S03-L003-B01-I02_locked_local_head_r004_candidate.png"),
    ("S03-L004-B01-I02_end_short_right_route_r003_candidate.png", "S03-L004-B01-I02_locked_local_head_r004_candidate.png"),
    ("S03-L005-B01-I02_end_shortcut_entrance_r003_candidate.png", "S03-L005-B01-I02_locked_local_head_r004_candidate.png"),
    ("S03-L007-B01-I02_end_decision_locked_background_r003_candidate.png", "S03-L007-B01-I02_locked_local_head_r004_candidate.png"),
    ("S03-L008-B01-I02_end_decision_locked_background_r003_candidate.png", "S03-L008-B01-I02_locked_local_head_r004_candidate.png"),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    base = np.asarray(Image.open(BASE).convert("RGB"), dtype=np.float32)
    height, width = base.shape[:2]
    mask = np.zeros((height, width), np.uint8)
    # Complete ear/head silhouette and neck overlap; body and feet are protected.
    envelope = np.asarray(
        [(425, 240), (980, 230), (1015, 515), (915, 595), (570, 595), (415, 500)],
        np.int32,
    )
    cv2.fillPoly(mask, [envelope], 255)
    mask_path = REVIEW / "fork_turn_head_envelope_r001_proposed.png"
    if mask_path.exists():
        raise FileExistsError(mask_path)
    Image.fromarray(mask, "L").save(mask_path)
    distance = cv2.distanceTransform((mask > 0).astype(np.uint8), cv2.DIST_L2, 5)
    weight = np.minimum(distance / 35.0, 1.0)
    rows = []
    for source_name, output_name in SOURCES:
        source_path = SCENES / source_name
        output_path = SCENES / output_name
        if output_path.exists() or output_path.with_suffix(".json").exists():
            raise FileExistsError(output_path)
        source = np.asarray(Image.open(source_path).convert("RGB"), dtype=np.float32)
        if source.shape != base.shape:
            raise ValueError(source_path)
        output = np.rint(base * (1.0 - weight[..., None]) + source * weight[..., None]).astype(np.uint8)
        if not np.array_equal(output[mask == 0], base.astype(np.uint8)[mask == 0]):
            raise AssertionError("fixed background/body/root changed outside envelope")
        Image.fromarray(output, "RGB").save(output_path)
        row = {
            "schema": "feltwillow.fork-local-turn-candidate.v1",
            "status": "unselected_technical_candidate_pending_native_seam_and_actor_review",
            "base_path": str(BASE.relative_to(ROOT)),
            "base_sha256": sha(BASE),
            "turn_source_path": str(source_path.relative_to(ROOT)),
            "turn_source_sha256": sha(source_path),
            "head_envelope_path": str(mask_path.relative_to(ROOT)),
            "head_envelope_sha256": sha(mask_path),
            "output_path": str(output_path.relative_to(ROOT)),
            "output_sha256": sha(output_path),
            "changed_pixels_outside_envelope": 0,
            "provider_calls_added": 0,
            "warning": "Exact scene pixels within the broad head envelope and head/body seam remain under review; source r003 background was not exact.",
            "technical_visual_pass": None,
            "selection": None,
        }
        output_path.with_suffix(".json").write_text(json.dumps(row, indent=2) + "\n")
        rows.append(row)
    (REVIEW / "FORK_TURN_LOCAL_CANDIDATES.json").write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
