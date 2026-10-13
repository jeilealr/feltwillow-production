"""Read-only validation of a rendered clip against its recorded inputs."""

from __future__ import annotations

import json
from pathlib import Path


def inspect_render(out: Path, expected: dict) -> tuple[str, str | None]:
    """Return (complete|missing|stale, reason); never modify existing media."""
    if not out.is_file():
        return "missing", None
    sidecar = out.with_suffix(".json")
    try:
        recorded = json.loads(sidecar.read_text())
    except (OSError, ValueError) as error:
        return "stale", f"no readable render sidecar: {error}"
    if not isinstance(recorded, dict):
        return "stale", "render sidecar is not a JSON object"
    changed = [key for key, value in expected.items() if recorded.get(key) != value]
    if changed:
        return "stale", "stale or unrecorded render inputs: " + ", ".join(changed)
    return "complete", None
