"""Tighten owner redo masks where broad blends exposed duplicate anatomy."""

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SCENES = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make(source_record, output_name, polygon, note):
    record = json.loads((SCENES / source_record).read_text())
    base = ROOT / record["base_path"]
    edit = ROOT / record["edit_path"]
    output = SCENES / output_name
    mask_path = HERE / f"{output.stem}_allowed_mask.png"
    if output.exists() or output.with_suffix(".json").exists() or mask_path.exists():
        raise FileExistsError(output)
    a = np.asarray(Image.open(base).convert("RGB"), dtype=np.float32)
    b = np.asarray(Image.open(edit).convert("RGB"), dtype=np.float32)
    if b.shape[0] == a.shape[0] and b.shape[1] == a.shape[1] - 1:
        b = np.concatenate([b, a[:, -1:, :]], axis=1)
    if a.shape != b.shape:
        raise ValueError(edit)
    mask = np.zeros(a.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [np.asarray(polygon, dtype=np.int32)], 255)
    distance = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
    weight = np.minimum(distance / 16.0, 1.0)
    out = np.rint(a * (1 - weight[..., None]) + b * weight[..., None]).astype(np.uint8)
    if not np.array_equal(out[mask == 0], a.astype(np.uint8)[mask == 0]):
        raise AssertionError(output)
    Image.fromarray(mask, "L").save(mask_path)
    Image.fromarray(out, "RGB").save(output)
    final = {**record,
        "status": "unselected_owner_requested_redo_pending_native_review",
        "allowed_mask_path": str(mask_path.relative_to(ROOT)),
        "allowed_mask_sha256": sha(mask_path),
        "output_path": str(output.relative_to(ROOT)),
        "output_sha256": sha(output),
        "changed_pixels_outside_allowed_mask": 0,
        "review_note": note,
    }
    output.with_suffix(".json").write_text(json.dumps(final, indent=2) + "\n")
    return final


def main():
    rows = []
    existing = SCENES / "S06-L001-B02-I01_scramble_descent_r006_candidate.json"
    if existing.exists():
        rows.append(json.loads(existing.read_text()))
    else:
        rows.append(make(
            "S06-L001-B02-I01_scramble_descent_r005_candidate.json",
            "S06-L001-B02-I01_scramble_descent_r006_candidate.png",
            [(1240, 410), (1590, 410), (1620, 830), (1100, 835), (1130, 670), (1200, 570)],
            "Milo-only stepping edit; excludes Leo face to avoid duplicate eye",
        ))
    paw_region = [(990, 560), (1200, 560), (1245, 745), (1225, 820), (900, 820), (910, 690)]
    rows.append(make(
        "S06-L002-B01-I01_front_paw_ready_r004_candidate.json",
        "S06-L002-B01-I01_front_paw_ready_r005_candidate.png",
        paw_region,
        "Leo front-foreleg-only correction; protects Leo torso and Milo body",
    ))
    rows.append(make(
        "S06-L002-B01-I02_front_paw_descending_r004_candidate.json",
        "S06-L002-B01-I02_front_paw_descending_r005_candidate.png",
        paw_region,
        "Leo front-foreleg-only descent; protects Leo torso and Milo body",
    ))
    (HERE / "OWNER_REDO_MASK_REFINEMENT.json").write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
