"""Fail when v6 review thumbnails or table links lag behind active candidates."""

from __future__ import annotations

import json
import re
import hashlib
from pathlib import Path

try:
    from .keyframe_reference_gate import validate_active_inventory, validate_contract
except ImportError:  # pragma: no cover - script entry point
    from keyframe_reference_gate import validate_active_inventory, validate_contract


ROOT = Path(__file__).resolve().parents[1]
STORY = ROOT / "stories/lion_and_mouse_v6"
KEYFRAMES = ROOT / "character/characters/lion_and_mouse_v6/interactions/keyframes"
SHEETS = KEYFRAMES / ".review/contact_sheets/current"


def main() -> int:
    plan = json.loads((STORY / "keyframe_plan.json").read_text())
    manifest = json.loads((SHEETS / "manifest.json").read_text())
    current = {
        row["id"]: (row["candidate_path"], row["sha256"])
        for row in plan["images"]
    }
    thumbnails = {
        row["id"]: (row["candidate_path"], row["sha256"])
        for row in manifest["images"]
    }
    errors = []
    errors.extend(validate_active_inventory(plan, KEYFRAMES))
    contract_path = STORY / "keyframe_regeneration_contract.json"
    staging_path = STORY / "staging_plan.json"
    bible_path = STORY / "visual_bible.json"
    if contract_path.is_file():
        errors.extend(validate_contract(json.loads(contract_path.read_text()), ROOT,
                                        json.loads(staging_path.read_text()),
                                        json.loads(bible_path.read_text()), plan))
    else:
        errors.append("missing keyframe_regeneration_contract.json; run keyframe_reference_gate.py --write-contract")
    if current != thumbnails:
        errors.append("contact-sheet manifest differs from active keyframe plan; rebuild sheets")
    for frame_id, (path, digest) in current.items():
        image = ROOT / path
        if image.is_file() and hashlib.sha256(image.read_bytes()).hexdigest() != digest:
            errors.append(f"{frame_id}: PNG bytes differ from plan and contact-sheet manifest")
    for retired_dir in (KEYFRAMES / ".review/superseded", SHEETS.parent / "historical"):
        if retired_dir.is_dir() and any(retired_dir.rglob("*.png")):
            errors.append(f"retired PNGs remain in {retired_dir.relative_to(ROOT)}")

    review = (STORY / "KEYFRAME_REVIEW.md").read_text()
    linked = {}
    for line in review.splitlines():
        match = re.match(r"^\| `(s\d\dx?_p\d\d)` \|.*\]\(([^)]*\.png)\)", line)
        if match:
            linked[match.group(1)] = Path(match.group(2)).name
    if set(linked) != set(current):
        errors.append(f"review table IDs differ: {sorted(set(current) ^ set(linked))}")
    for frame_id, (path, _) in current.items():
        if linked.get(frame_id) != Path(path).name:
            errors.append(f"{frame_id}: review links {linked.get(frame_id)} instead of {Path(path).name}")
    for scene in range(1, 17):
        sheet = SHEETS / f"scene{scene:02d}_keyframes.png"
        if not sheet.is_file():
            errors.append(f"missing {sheet.relative_to(ROOT)}")
        if f"contact_sheets/current/scene{scene:02d}_keyframes.png" not in review:
            errors.append(f"Scene {scene:02d} does not link its current contact sheet")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"Current contact sheets and Markdown links match all {len(current)} active keyframes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
