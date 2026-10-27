"""Connect frozen render allocations to the selected-take sample editor.

Before rendering this records an intended edit only. Actual trim, speed and join
reviews bind returned bytes and the exact target timeline before preview assembly.
No authoring, selection, rendering or resource submission occurs here.
"""

from __future__ import annotations
import copy
from production.sequence_plan import fingerprint, digest, frame_accounting


def edit_review_digest(packet, pieces):
    timing = packet["timing"]
    return fingerprint(
        dict(
            intervals=timing["intervals"],
            render_allocations=timing.get("render_allocations", {}),
            pieces=[
                {k: p[k] for k in ("id", "frames", "fps", "method", "start", "end")}
                for p in pieces
            ],
            dependency_sha256=packet["dependency_sha256"],
        )
    )


def plan_edit(packet, pieces):
    timing = packet["timing"]
    rate = timing["sample_rate"]
    review = timing.get("editorial_review", {})
    if (
        review.get("status") != "reviewed"
        or not review.get("reviewer")
        or review.get("allocation_sha256") != edit_review_digest(packet, pieces)
    ):
        raise ValueError("reviewed exact editorial allocations pending/stale")
    cells = frame_accounting(timing["intervals"], rate)
    byid = {p["id"]: p for p in pieces}
    uses = {u["id"]: u for u in packet["resolved_images"]}
    allocations = timing.get("render_allocations", {})
    if set(allocations) != set(byid):
        raise ValueError("one allocation per meaningful render piece required")
    rows = []
    seen = []
    for raw, cell in zip(timing["intervals"], cells["intervals"]):
        row = copy.deepcopy(raw)
        row["frame_cells"] = cell["frame_cells"]
        if row.get("kind") == "render_piece":
            pid = row.get("piece_id", row["id"])
            if pid not in byid or pid in seen:
                raise ValueError("unknown/duplicate editorial piece")
            piece = byid[pid]
            allocation = allocations[pid]
            if (
                allocation.get("frames") != piece["frames"]
                or allocation.get("fps") != piece["fps"]
                or allocation.get("reviewed") is not True
            ):
                raise ValueError(
                    "allocation recipe differs from effective render piece"
                )
            mapping = allocation.get(
                "source_mapping", dict(start_frame=0, frame_count=piece["frames"])
            )
            start = mapping.get("start_frame")
            count = mapping.get("frame_count")
            if (
                any(
                    isinstance(v, bool) or not isinstance(v, int)
                    for v in (start, count)
                )
                or start < 0
                or count <= 0
                or start + count > piece["frames"]
            ):
                raise ValueError("planned edit source frame window invalid")
            row.update(
                piece_id=pid,
                source_mapping=copy.deepcopy(mapping),
                render_frames=piece["frames"],
                render_fps=piece["fps"],
                returned_motion_trim_retime_join_review="pending exact returned bytes",
            )
            seen.append(pid)
        elif row.get("kind") == "static_hold":
            uid = row.get("use_id")
            use = uses.get(uid)
            if not use or use["status"] not in {
                "selected_exact",
                "selected_alias",
                "selected_hold",
            }:
                raise ValueError("static hold requires usable exact selected source")
            hold = row.get("hold_review", {})
            if (
                hold.get("status") != "pass"
                or not hold.get("reviewer")
                or hold.get("source_sha256") != use["source"]["sha256"]
                or hold.get("fit_sha256") != use["fit"]["pixel_sha256"]
                or hold.get("settled") is not True
                or hold.get("resting_mouth") is not True
            ):
                raise ValueError("hold requires exact settled/resting-state review")
            row["source"] = copy.deepcopy(use["source"])
        else:
            raise ValueError(
                "editorial intervals must explicitly be render_piece or static_hold"
            )
        if row.get("boundary", "continuous") not in {"cut", "continuous"}:
            raise ValueError("unsupported editorial boundary")
        rows.append(row)
    if seen != list(byid):
        raise ValueError(
            "edit must retain every meaningful piece once in authored order"
        )
    result = dict(
        schema="feltwillow.planned-editorial.v1",
        sample_rate=rate,
        total_samples=timing["total_samples"],
        fps=16,
        intervals=rows,
        source_dependency_sha256=packet["dependency_sha256"],
        allocation_sha256=review["allocation_sha256"],
        whole_motion_review="pending",
        owner_take_selection="pending",
        final_assembly_authorized=False,
    )
    result["sha256"] = fingerprint(result)
    return result


def bind_takes(editorial, selection, reviews, root, audio=None):
    """Bind selected exact returned takes, then validate actual FPS/trim/joins."""
    from pathlib import Path
    from production.sequence_take import selected_source
    from production.sequence_timeline import compile_timeline

    check = {k: v for k, v in editorial.items() if k != "sha256"}
    if fingerprint(check) != editorial.get("sha256"):
        raise ValueError("frozen editorial plan changed")
    rows = []
    for source_row in editorial["intervals"]:
        row = copy.deepcopy(source_row)
        rid = row["id"]
        observed = reviews.get(rid, {})
        if row["kind"] == "render_piece":
            source, identity = selected_source(selection, row["piece_id"])
            row.update(
                kind="video",
                source=dict(path=str(source), sha256=identity["source_sha256"]),
                whole_motion_review=dict(
                    status="pass",
                    reviewer=selection["takes"][row["piece_id"]]["full_motion_review"][
                        "reviewer"
                    ],
                    source_sha256=identity["source_sha256"],
                ),
            )
            for key in ("retime_review", "trim_review"):
                if key in observed:
                    row["source_mapping"][key] = copy.deepcopy(observed[key])
            if "join_review" in observed:
                row["join_review"] = copy.deepcopy(observed["join_review"])
        else:
            source = (Path(root) / row["source"]["path"]).resolve()
            if digest(source) != row["source"]["sha256"]:
                raise ValueError("hold source changed")
            row["source"]["path"] = str(source)
            if "join_review" in observed:
                row["join_review"] = copy.deepcopy(observed["join_review"])
        rows.append(row)
    return compile_timeline(
        rows,
        editorial["sample_rate"],
        editorial["total_samples"],
        editorial["fps"],
        audio,
    )
