"""Resolve an explicitly selected sequence take for dialogue or edit consumers.

This adapter performs no rendering, selection, retiming or final assembly.
"""

from pathlib import Path
import json

from feltwillow.render_receipt import inspect_render
from production.sequence_plan import digest


def selected_source(document, piece):
    if document.get("schema") != "feltwillow.sequence-takes.v1":
        raise ValueError("unsupported sequence take schema")
    row = document.get("takes", {}).get(piece)
    if not row or row.get("owner_decision") != "selected":
        raise ValueError(f"{piece}: exact owner take decision missing")
    source = Path(row["path"])
    if (
        not source.is_absolute()
        or not source.is_file()
        or digest(source) != row["sha256"]
    ):
        raise ValueError(f"{piece}: selected take bytes unavailable or changed")
    receipt = json.loads(source.with_suffix(".json").read_text())
    for field in ("run_id", "runtime_sha256"):
        if not document.get(field) or receipt.get(field) != document[field]:
            raise ValueError(f"{piece}: take/runtime identity mismatch")
    if receipt.get("shot") != piece:
        raise ValueError(f"{piece}: receipt identifies a different piece")
    transport=row.get('boundary_paths')
    if transport is not None:
        references={b[k] for b in receipt.get('native_boundaries',{}).values() for k in ('path','preview_path') if b.get(k)}
        if not isinstance(transport,dict) or set(transport)!=references or any(not Path(p).is_absolute() for p in transport.values()):
            raise ValueError(f"{piece}: malformed native boundary transport map")
    status, reason = inspect_render(source, receipt,boundary_paths=transport)
    if status != "complete":
        raise ValueError(f"{piece}: {reason}")
    review = row.get("full_motion_review", {})
    if (
        review.get("status") != "pass"
        or not review.get("reviewer")
        or review.get("output_sha256") != row["sha256"]
        or review.get("whole_clip_watched") is not True
        or review.get("joins_reviewed") is not True
    ):
        raise ValueError(f"{piece}: whole-motion/join review missing or stale")
    return source, {
        "run_id": document["run_id"],
        "runtime_sha256": document["runtime_sha256"],
        "source_sha256": row["sha256"],
        "post_dialogue_review": "pending",
        "assembly_authorized": False,
    }
