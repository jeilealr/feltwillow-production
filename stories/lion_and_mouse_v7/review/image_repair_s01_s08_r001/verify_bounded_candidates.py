"""Recheck exact file hashes and protected pixels for local image repairs.

This verifies provenance and the declared edit envelope. It cannot certify
anatomy, contacts, expression, or continuity inside the envelope.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
RECORDS = (
    "BOUNDED_SMALL_ACTIONS.json",
    "BOUNDED_MOUTH_CALIBRATIONS.json",
    "BOUNDED_TRIP_AND_BLOCK.json",
    "FORK_TURN_LOCAL_CANDIDATES.json",
    "S02_BESIDE_STONE_BOUNDED.json",
    "S06_HEAD_RAISE_R005.json",
    "S06_SCRAMBLE_R003.json",
    "S05_REAR_PAW_CONTACT_R006.json",
    "OWNER_REQUESTED_REDOS.json",
    "OWNER_REDO_MASK_REFINEMENT.json",
    "S08_PAW_RESULT.json",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records(value):
    if isinstance(value, dict):
        if "base_path" in value and "output_path" in value:
            yield value
        else:
            for child in value.values():
                yield from records(child)
    elif isinstance(value, list):
        for child in value:
            yield from records(child)


def main() -> int:
    output = []
    for name in RECORDS:
        for item in records(json.loads((HERE / name).read_text())):
            row = {"record": name, "output_path": item["output_path"]}
            errors = []
            for role in ("base", "edit", "allowed_mask", "output"):
                path_key = f"{role}_path"
                if path_key not in item:
                    continue
                path = ROOT / item[path_key]
                if not path.is_file():
                    errors.append(f"missing {role}: {path}")
                    continue
                expected = item.get(f"{role}_sha256")
                if expected and sha(path) != expected:
                    errors.append(f"stale {role} hash")
            if not errors and "allowed_mask_path" in item:
                base = np.asarray(Image.open(ROOT / item["base_path"]).convert("RGB"))
                result = np.asarray(Image.open(ROOT / item["output_path"]).convert("RGB"))
                mask = np.asarray(Image.open(ROOT / item["allowed_mask_path"]).convert("L")) > 0
                if base.shape != result.shape or base.shape[:2] != mask.shape:
                    errors.append("dimension mismatch")
                else:
                    changed = np.any(base != result, axis=2)
                    row["changed_pixels_outside_allowed_mask"] = int(np.count_nonzero(changed & ~mask))
                    row["changed_pixels_inside_allowed_mask"] = int(np.count_nonzero(changed & mask))
                    if row["changed_pixels_outside_allowed_mask"]:
                        errors.append("protected pixels changed")
            row["status"] = "pass" if not errors else "fail"
            row["errors"] = errors
            output.append(row)
    report = {
        "schema": "feltwillow.bounded-repair-verification.v1",
        "scope": "hashes_and_declared_protected_pixels_only",
        "visual_anatomy_or_edge_pass": False,
        "records": output,
    }
    (HERE / "BOUNDED_VERIFICATION.json").write_text(json.dumps(report, indent=2) + "\n")
    failures = [row for row in output if row["status"] != "pass"]
    print(f"verified {len(output)} bounded candidates; failures={len(failures)}")
    for row in failures:
        print(row["output_path"], row["errors"])
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
