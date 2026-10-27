"""Preserve newly generated V7 image candidates without transferring selection."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
REVIEW = Path(__file__).resolve().parent
COMPOSITIONS = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions"
EXPRESSIONS = ROOT / "character/characters/lion_and_mouse_v7"
GENERATED = Path("/Users/lealroja/.codex/generated_images/01a1533f-9137-7e20-a37c-3eeb1ab8afad")

ITEMS = [
    (
        "S01 tiny toothless contact",
        "exec-5f385d65-419f-4789-b6e1-606770b0ed95.png",
        COMPOSITIONS / "S01-L004-B03_key_tiny_toothless_contact_r001_candidate.png",
        [COMPOSITIONS / "S01-L004-B03-I03_key_acorn_glade_r005_candidate.png"],
        "unselected candidate; mouth, hand, acorn and background continuity pending native/fitted review",
    ),
    (
        "S01 closed tasted endpoint",
        "exec-acdfbba3-e222-4403-9a4e-507f7c5dc005.png",
        COMPOSITIONS / "S01-L004-B03-I04_end_tasted_acorn_r001_candidate.png",
        [GENERATED / "exec-5f385d65-419f-4789-b6e1-606770b0ed95.png"],
        "unselected candidate; small tasted notch and closed mouth pending native/fitted review",
    ),
    (
        "S02 beside-stone contact",
        "exec-b005881c-e0bb-4891-be71-9ecdc7ac7f9d.png",
        COMPOSITIONS / "S02-L004-B02-I02_key_ground_beside_stone_contact_r005_candidate.png",
        [
            COMPOSITIONS / "S02-L004-B02-I02_key_stone_acorn_contact_r004_candidate.png",
            COMPOSITIONS / "S02-L004-B02-I03_end_stone_beside_stream_r004_candidate.png",
        ],
        "unselected candidate; exact background/camera/prop-contact edge review pending",
    ),
    (
        "S02 beside-stone release",
        "exec-c8a9f9c7-74d4-42db-af30-5f55c6e97b24.png",
        COMPOSITIONS / "S02-L004-B02-I03_end_ground_beside_stone_release_r005_candidate.png",
        [
            GENERATED / "exec-b005881c-e0bb-4891-be71-9ecdc7ac7f9d.png",
            COMPOSITIONS / "S02-L004-B02-I03_end_stone_beside_stream_r004_candidate.png",
        ],
        "unselected candidate; exact background and ground contact/settle edge review pending",
    ),
    (
        "Milo three-quarter toothless speech calibration",
        "exec-c82d8fec-cda4-445d-998c-64f46084aff2.png",
        EXPRESSIONS / "Milo/expressions/milo_portrait_base_3q_default_tiny_open_toothless_r001_candidate.png",
        [EXPRESSIONS / "Milo/expressions/milo_portrait_base_3q_default_r003_candidate.png"],
        "unselected auxiliary calibration; mouth-only delta/angle/source review pending",
    ),
    (
        "Leo three-quarter toothless speech calibration",
        "exec-daf2cd74-b3ee-4f3a-a3a1-71d89b1fbe2b.png",
        EXPRESSIONS / "Leo/expressions/leo_portrait_base_3q_tiny_open_toothless_r001_candidate.png",
        [EXPRESSIONS / "Leo/expressions/leo_portrait_base_3q_r001_candidate.png"],
        "unselected auxiliary calibration; mouth-only delta/angle/source review pending",
    ),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> None:
    records = []
    for role, generated_name, target, inputs, status in ITEMS:
        generated = GENERATED / generated_name
        if target.exists() or target.with_suffix(".json").exists():
            raise FileExistsError(target)
        if not generated.is_file():
            raise FileNotFoundError(generated)
        with Image.open(generated) as image:
            size = list(image.size)
            mode = image.mode
        shutil.copy2(generated, target)
        record = {
            "schema": "feltwillow.image-candidate-receipt.v1",
            "role": role,
            "status": status,
            "provider": "image_gen.imagegen",
            "request_count": 1,
            "automatic_retries": 0,
            "cost": "unknown; tool did not expose per-call price",
            "request_id": None,
            "output_path": display(target),
            "output_sha256": sha(target),
            "canvas": size,
            "mode": mode,
            "input_references": [{"path": display(path), "sha256": sha(path)} for path in inputs],
            "generation_output_path": str(generated),
            "approval_scope": "owner 2026-10-25: I approve. go ahead and repair them all",
            "selection": None,
            "technical_visual_pass": None,
        }
        target.with_suffix(".json").write_text(json.dumps(record, indent=2) + "\n")
        records.append(record)
    (REVIEW / "GENERATED_CANDIDATES.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    main()
