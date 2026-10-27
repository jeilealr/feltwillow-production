"""Preserve one-call S05/S06 source-art outputs as unselected revisions."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
REVIEW = Path(__file__).resolve().parent
SCENES = ROOT / "character/characters/lion_and_mouse_v7/interactions/scene_compositions"
GENERATED = Path("/Users/lealroja/.codex/generated_images/01a1533f-9137-7e20-a37c-3eeb1ab8afad")

# These are proposals for the named uses, not selection-ledger updates.
ITEMS = [
    ("S05-L008-B01-I01_grounded_approach_r001_candidate.png", "exec-ae5b126c-fd8d-48f5-a3ca-b7fbb9cd6f07.png", ["S05-L008-B01-I02_key_first_joint_rear_paw_contact_r004_candidate.png"], "grounded approach; connected camera and rear-paw geometry unverified"),
    ("S05-L008-B01-I03_forward_pitch_r001_candidate.png", "exec-d609f535-d89d-48e5-a9b0-f1b29a1afb1a.png", ["S05-L008-B01-I02_key_first_joint_rear_paw_contact_r004_candidate.png", "S05-L008-B01-I04_local_trip_r002_candidate.png"], "forward pitch; contact, support and scale unverified"),
    ("S05-L009-B01-I04_grounded_nose_landing_r001_candidate.png", "exec-88825d46-4ab4-42c5-913d-feff008691e0.png", ["S05-L009-B01-I03_local_roll_r002_candidate.png"], "nose landing; trajectory and connected background unverified"),
    ("S06-L001-B01-I02_head_raised_r001_candidate.png", "exec-18cb1114-3f51-467c-bc4c-e9d34cac1209.png", ["S06-L001-B01-I01_start_rest_nose_r001_candidate.png"], "head raise; locked camera and anatomy unverified"),
    ("S06-L001-B02-I01_scramble_descent_r001_candidate.png", "exec-93386ec4-3a32-44f5-80d0-11d8cf7010a2.png", ["S06-L001-B01-I01_start_rest_nose_r001_candidate.png", "S06-L001-B02-I02_end_path_arrival_r001_candidate.png"], "likely fails: Milo appears to overshoot the selected path-arrival position"),
    ("S06-L002-B01-I01_front_paw_ready_r001_candidate.png", "exec-95bf4e73-7e00-419c-b435-d0601694a4c5.png", ["S06-L001-B02-I02_end_path_arrival_r001_candidate.png", "S06-L002-B01-I03_end_front_paw_block_r001_candidate.png"], "front-paw raise; actor/root/background lock unverified"),
    ("S06-L002-B01-I02_front_paw_descending_r001_candidate.png", "exec-ba13d0ba-8c4e-4788-9004-5831bf21244d.png", ["S06-L002-B01-I03_end_front_paw_block_r001_candidate.png"], "front paw descends; actor/root/background lock unverified"),
    ("S06-L003-B01-I02_frozen_r001_candidate.png", "exec-2d2b95e6-52e8-4abb-b9e3-fdd4c0233362.png", ["S06-L002-B01-I03_end_front_paw_block_r001_candidate.png"], "frozen reaction; expression, limb and background continuity unverified"),
    ("S06-L004-B01-I02_worried_r001_candidate.png", "exec-268c35c9-5e39-41b8-883d-83d8643dc21f.png", ["S06-L002-B01-I03_end_front_paw_block_r001_candidate.png"], "worried reaction; expression, limb and background continuity unverified"),
    ("S06-L005-B01-I02_humbled_r001_candidate.png", "exec-b9cb4e9f-848e-42cd-8a6a-f8039464f584.png", ["S06-L002-B01-I03_end_front_paw_block_r001_candidate.png"], "humbled reaction; expression, limb and background continuity unverified"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    records = []
    for filename, generated_name, references, review_note in ITEMS:
        source = GENERATED / generated_name
        target = SCENES / filename
        sidecar = target.with_suffix(".json")
        if not source.is_file():
            raise FileNotFoundError(source)
        if target.exists() or sidecar.exists():
            raise FileExistsError(target)
        refs = [SCENES / name for name in references]
        for ref in refs:
            if not ref.is_file():
                raise FileNotFoundError(ref)
        with Image.open(source) as image:
            canvas = list(image.size)
            mode = image.mode
        shutil.copy2(source, target)
        record = {
            "schema": "feltwillow.image-candidate-receipt.v1",
            "role": filename.removesuffix(".png"),
            "status": "unselected_candidate",
            "technical_visual_pass": None,
            "review_note": review_note,
            "provider": "image_gen.imagegen",
            "request_count": 1,
            "automatic_retries": 0,
            "cost": "unknown; tool did not expose per-call price",
            "request_id": None,
            "output_path": str(target.relative_to(ROOT)),
            "output_sha256": digest(target),
            "canvas": canvas,
            "mode": mode,
            "input_references": [{"path": str(ref.relative_to(ROOT)), "sha256": digest(ref)} for ref in refs],
            "generation_output_path": str(source),
            "approval_scope": "owner 2026-10-25: I approve. go ahead and repair them all",
            "selection": None,
        }
        sidecar.write_text(json.dumps(record, indent=2) + "\n")
        records.append(record)
    (REVIEW / "TRIP_AND_BLOCK_CANDIDATES.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    main()
