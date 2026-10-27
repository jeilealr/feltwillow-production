"""Measure whether proposed connected stills preserve protected scene pixels.

This is a narrow technical gate. It never certifies anatomy or artistic quality.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
SCENES = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions"
REPORT = Path(__file__).with_name("CONNECTED_PIXEL_AUDIT.json")

GROUPS = {
    "S01_bite": (
        "S01-L004-B03-I03_key_acorn_glade_r005_candidate.png",
        ["S01-L004-B03_key_tiny_toothless_contact_r001_candidate.png", "S01-L004-B03-I04_end_tasted_acorn_r001_candidate.png"],
    ),
    "S02_placement": (
        "S02-L004-B02-I02_key_stone_acorn_contact_r004_candidate.png",
        ["S02-L004-B02-I02_key_ground_beside_stone_contact_r005_candidate.png", "S02-L004-B02-I03_end_ground_beside_stone_release_r005_candidate.png"],
    ),
    "S05_trip": (
        "S05-L008-B01-I02_key_first_joint_rear_paw_contact_r004_candidate.png",
        ["S05-L008-B01-I01_grounded_approach_r001_candidate.png", "S05-L008-B01-I03_forward_pitch_r001_candidate.png", "S05-L009-B01-I04_grounded_nose_landing_r001_candidate.png"],
    ),
    "S06_block": (
        "S06-L002-B01-I03_end_front_paw_block_r001_candidate.png",
        [
            "S06-L001-B01-I02_head_raised_r001_candidate.png",
            "S06-L001-B02-I01_scramble_descent_r001_candidate.png",
            "S06-L002-B01-I01_front_paw_ready_r001_candidate.png",
            "S06-L002-B01-I02_front_paw_descending_r001_candidate.png",
            "S06-L003-B01-I02_frozen_r001_candidate.png",
            "S06-L004-B01-I02_worried_r001_candidate.png",
            "S06-L005-B01-I02_humbled_r001_candidate.png",
        ],
    ),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def protected_border(height: int, width: int) -> np.ndarray:
    # Corners lie outside the actor/prop action in these reviewed compositions.
    # This deliberately tests only the conservative outer background.
    mask = np.zeros((height, width), dtype=bool)
    band_x = min(240, width // 7)
    band_y = min(170, height // 7)
    for x0 in (0, width - band_x):
        for y0 in (0, height - band_y):
            mask[y0 : y0 + band_y, x0 : x0 + band_x] = True
    return mask


def main() -> None:
    rows = []
    for group, (anchor_name, candidates) in GROUPS.items():
        anchor_path = SCENES / anchor_name
        anchor = np.asarray(Image.open(anchor_path).convert("RGB"))
        border = protected_border(*anchor.shape[:2])
        for filename in candidates:
            path = SCENES / filename
            candidate = np.asarray(Image.open(path).convert("RGB"))
            if candidate.shape != anchor.shape:
                rows.append({"group": group, "candidate": filename, "status": "canvas_mismatch"})
                continue
            delta = np.abs(anchor.astype(np.int16) - candidate.astype(np.int16))
            any_change = np.any(delta > 0, axis=2)
            significant_change = np.any(delta > 12, axis=2)
            rows.append(
                {
                    "group": group,
                    "anchor": str(anchor_path.relative_to(ROOT)),
                    "anchor_sha256": sha(anchor_path),
                    "candidate": str(path.relative_to(ROOT)),
                    "candidate_sha256": sha(path),
                    "protected_border_pixels": int(border.sum()),
                    "protected_border_exact_changed_fraction": round(float(any_change[border].mean()), 6),
                    "protected_border_over_12_changed_fraction": round(float(significant_change[border].mean()), 6),
                    "status": "background_lock_unverified" if any_change[border].any() else "protected_border_exact",
                    "note": "Protected border equality is necessary for an exact camera/background lock, not sufficient for full visual consistency.",
                }
            )
    REPORT.write_text(json.dumps({"schema": "feltwillow.connected-pixel-audit.v1", "rows": rows}, indent=2) + "\n")
    print(f"wrote {REPORT}: {len(rows)} comparisons")


if __name__ == "__main__":
    main()
