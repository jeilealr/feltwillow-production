"""Scoped sequence readiness: technical eligibility never grants submission."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import argparse, json
from pathlib import Path
from production.sequence_plan import fingerprint, dependency_fingerprint


def evaluate(packet, stage="execution", mode="diagnostic"):
    if stage not in {"realization", "still", "timing", "execution"} or mode not in {
        "diagnostic",
        "production",
    }:
        raise ValueError("unsupported stage/mode")
    blockers = list(packet.get("global_schema_errors", [])) + list(
        packet.get("sequence", {}).get("blockers", [])
    )
    rank = ["realization", "still", "timing", "execution"].index(stage)
    for u in packet["resolved_images"]:
        if u["status"] not in {"selected_exact", "selected_alias", "selected_hold"}:
            blockers.append(f"{u['id']}: {u['status']}: {u.get('blockers')}")
    if dependency_fingerprint(packet) != packet.get("dependency_sha256"):
        blockers.append("sequence inputs/order/fit changed after realization")
    evidence = packet.get("technical_evidence", {})
    if rank >= 1:
        for u in packet["resolved_images"]:
            review = evidence.get("uses", {}).get(u["id"], {})
            if (
                not review.get("reviewer")
                or review.get("status") != "pass"
                or review.get("source_sha256") != u.get("source", {}).get("sha256")
                or review.get("fit_sha256") != u.get("fit", {}).get("pixel_sha256")
            ):
                blockers.append(
                    u["id"] + ": exact native/fitted technical review pending/stale"
                )
        for edge in packet["edges"]:
            if edge["kind"] == "cut":
                continue
            key = edge["from"] + "->" + edge["to"]
            review = evidence.get("edges", {}).get(key, {})
            hashes = [
                next(u for u in packet["resolved_images"] if u["id"] == uid)
                .get("source", {})
                .get("sha256")
                for uid in [edge["from"], edge["to"]]
            ]
            if (
                not review.get("reviewer")
                or review.get("status") != "pass"
                or review.get("source_sha256s") != hashes
                or review.get("edge_sha256") != fingerprint(edge)
            ):
                blockers.append(key + ": edge quality pending/stale")
            if edge["kind"] == "motion" and hashes[0] == hashes[1]:
                blockers.append(
                    key + ": identical raster cannot prove new visible action"
                )
    if rank >= 2:
        timing = packet.get("timing", {})
        if (
            not isinstance(timing.get("sample_rate"), int)
            or timing.get("sample_rate", 0) <= 0
        ):
            blockers.append("positive integer timing sample rate required")
        if (
            timing.get("status") != "reviewed"
            or timing.get("mode") != mode
            or not timing.get("reviewer")
            or timing.get("dependency_sha256") != packet["dependency_sha256"]
        ):
            blockers.append("reviewed scoped timing pending/stale")
        intervals = timing.get("intervals", [])
        cursor = 0
        for interval in intervals:
            if (
                interval.get("start_sample") != cursor
                or interval.get("end_sample", 0) <= cursor
            ):
                blockers.append("timing gap/overlap/nonpositive interval")
            cursor = interval.get("end_sample", cursor)
        if not intervals or cursor != timing.get("total_samples"):
            blockers.append("timing coverage incomplete")
        if mode == "production" and timing.get("pcm_verified") is not True:
            blockers.append("production PCM/alignment verification pending")
    if rank >= 3:
        capability = packet.get("capability", {})
        if (
            capability.get("endpoint_supported") is not True
            or capability.get("evidence_level") != "inspected_source_config"
            or not capability.get("source_sha256")
            or capability.get("expand_timesteps") is not False
        ):
            blockers.append("installed endpoint capability/configuration pending")
    return {
        "sequence_id": packet["sequence_id"],
        "stage": stage,
        "mode": mode,
        "technical_render_ready": not blockers and rank == 3,
        "stage_passed": not blockers,
        "submission_authorized": False,
        "blockers": blockers,
        "dependency_sha256": packet["dependency_sha256"],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("packet", type=Path)
    p.add_argument("--stage", default="execution")
    p.add_argument("--mode", default="diagnostic")
    a = p.parse_args()
    out = evaluate(json.loads(a.packet.read_text()), a.stage, a.mode)
    print(json.dumps(out, indent=2))
    return 0 if out["stage_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
