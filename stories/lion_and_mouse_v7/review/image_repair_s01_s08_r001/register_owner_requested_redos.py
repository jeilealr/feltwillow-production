"""Register owner-requested redo images and camera-bounded proposals.

Original selected images and prior candidate revisions are immutable. Each
output remains an unselected revision until the owner reviews its exact bytes.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SCENES = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions"
GENERATED = Path("/Users/lealroja/.codex/generated_images/01a1533f-9137-7e20-a37c-3eeb1ab8afad")

# source generation, exact selected/accepted camera base, raw revision, bounded
# revision, and the only region allowed to differ from that base.
JOBS = [
    (
        "exec-f5656329-0cb0-473a-9e4c-ea1c6d9da1c7.png",
        "S05-L009-B01-I03_local_roll_r002_candidate.png",
        "S05-L009-B01-I04_grounded_nose_landing_r003_candidate.png",
        "S05-L009-B01-I04_grounded_nose_landing_r004_candidate.png",
        [(780, 530), (1350, 530), (1370, 830), (770, 840)],
        "compact Milo body/ground support and nose landing",
    ),
    (
        "exec-28391ecf-6e41-4df8-ac92-93140e80f6ab.png",
        "S06-L001-B02-I02_end_path_arrival_r001_candidate.png",
        "S06-L001-B02-I01_scramble_descent_r004_candidate.png",
        "S06-L001-B02-I01_scramble_descent_r005_candidate.png",
        [(1090, 430), (1570, 430), (1600, 830), (1050, 840)],
        "Milo stepping body and path between nose and arrival",
    ),
    (
        "exec-17536e00-ed6a-47ea-ac03-4c739f018574.png",
        "S06-L002-B01-I03_end_front_paw_block_r001_candidate.png",
        "S06-L002-B01-I01_front_paw_ready_r003_candidate.png",
        "S06-L002-B01-I01_front_paw_ready_r004_candidate.png",
        [(810, 555), (1250, 555), (1260, 830), (800, 835)],
        "one anatomically attached Leo front paw beginning to lift",
    ),
    (
        "exec-05453750-fb59-485e-a5c6-ba1397d0f0ac.png",
        "S06-L002-B01-I03_end_front_paw_block_r001_candidate.png",
        "S06-L002-B01-I02_front_paw_descending_r003_candidate.png",
        "S06-L002-B01-I02_front_paw_descending_r004_candidate.png",
        [(810, 555), (1250, 555), (1260, 830), (800, 835)],
        "same Leo front foreleg in an intermediate descending pose",
    ),
    (
        "exec-0446e6d7-af77-44d4-aeda-959707f213fe.png",
        "S08-L016-B01-I01_single_gentle_clear_r001_candidate.png",
        "S08-L016-B01-I01_single_gentle_clear_r003_candidate.png",
        "S08-L016-B01-I01_single_gentle_clear_r004_candidate.png",
        [(790, 555), (1220, 555), (1230, 815), (780, 815)],
        "second separately visible image-top-right Leo front paw",
    ),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows = []
    for generated_name, base_name, raw_name, bounded_name, polygon, intent in JOBS:
        original = GENERATED / generated_name
        base = SCENES / base_name
        raw = SCENES / raw_name
        bounded = SCENES / bounded_name
        mask_path = HERE / f"{bounded.stem}_allowed_mask.png"
        if bounded.exists() and bounded.with_suffix(".json").exists():
            row = json.loads(bounded.with_suffix(".json").read_text())
            if sha(bounded) != row["output_sha256"] or sha(original) != row["provider_output_sha256"]:
                raise ValueError(f"stale completed output: {bounded}")
            rows.append(row)
            continue
        for path in (bounded, mask_path, raw.with_suffix(".json"), bounded.with_suffix(".json")):
            if path.exists():
                raise FileExistsError(path)
        if raw.exists():
            if sha(raw) != sha(original):
                raise ValueError(f"stale copied provider output: {raw}")
        else:
            shutil.copyfile(original, raw)
        base_pixels = np.asarray(Image.open(base).convert("RGB"), dtype=np.float32)
        raw_pixels = np.asarray(Image.open(raw).convert("RGB"), dtype=np.float32)
        if raw_pixels.shape[0] == base_pixels.shape[0] and raw_pixels.shape[1] == base_pixels.shape[1] - 1:
            # ImageGen occasionally returns one fewer right-edge column. The
            # edit mask never touches that edge, so preserve the base column.
            raw_pixels = np.concatenate([raw_pixels, base_pixels[:, -1:, :]], axis=1)
        if base_pixels.shape != raw_pixels.shape:
            raise ValueError(f"dimension mismatch: {raw}")
        allowed = np.zeros(base_pixels.shape[:2], dtype=np.uint8)
        cv2.fillPoly(allowed, [np.asarray(polygon, dtype=np.int32)], 255)
        distance = cv2.distanceTransform((allowed > 0).astype(np.uint8), cv2.DIST_L2, 5)
        weight = np.minimum(distance / 26.0, 1.0)
        result = np.rint(base_pixels * (1 - weight[..., None]) + raw_pixels * weight[..., None]).astype(np.uint8)
        if not np.array_equal(result[allowed == 0], base_pixels.astype(np.uint8)[allowed == 0]):
            raise AssertionError(f"protected exterior changed: {bounded}")
        Image.fromarray(allowed, mode="L").save(mask_path)
        Image.fromarray(result, mode="RGB").save(bounded)
        common = {
            "schema": "feltwillow.bounded-connected-candidate.v1",
            "status": "unselected_owner_requested_redo_pending_native_review",
            "replaces_rejected_candidate_sha256": None,
            "base_path": str(base.relative_to(ROOT)),
            "base_sha256": sha(base),
            "edit_path": str(raw.relative_to(ROOT)),
            "edit_sha256": sha(raw),
            "provider_output_path": str(original),
            "provider_output_sha256": sha(original),
            "provider_calls": 1,
            "automatic_retries": 0,
            "request_id": None,
            "cost": None,
            "selection": None,
            "technical_visual_pass": None,
            "review_intent": intent,
        }
        raw_record = {**common, "output_path": str(raw.relative_to(ROOT)), "output_sha256": sha(raw), "bounded": False}
        raw.with_suffix(".json").write_text(json.dumps(raw_record, indent=2) + "\n")
        row = {
            **common,
            "allowed_mask_path": str(mask_path.relative_to(ROOT)),
            "allowed_mask_sha256": sha(mask_path),
            "output_path": str(bounded.relative_to(ROOT)),
            "output_sha256": sha(bounded),
            "changed_pixels_outside_allowed_mask": 0,
        }
        bounded.with_suffix(".json").write_text(json.dumps(row, indent=2) + "\n")
        rows.append(row)
    (HERE / "OWNER_REQUESTED_REDOS.json").write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
