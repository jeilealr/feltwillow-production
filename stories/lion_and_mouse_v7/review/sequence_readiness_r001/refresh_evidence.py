"""Refresh CPU-only media evidence for this run; never render, select or submit."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from production.sequence_plan import (
    digest,
    resolve_sequence,
    selection_catalog,
    audio_intervals,
)
from production.sequence_readiness import evaluate
from production.sequence_review import build
from feltwillow.render_receipt import inspect_media


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline-decode",
        action="store_true",
        help="fully decode historical local MP4s, without visual approval",
    )
    args = parser.parse_args()
    out = Path(__file__).resolve().parent
    folder = ROOT / "stories/lion_and_mouse_v7"
    plan = json.loads((folder / "audio_visual_plan.json").read_text())
    catalog = selection_catalog(folder)
    available = []
    for row in catalog:
        path = ROOT / row["path"]
        available.append(
            dict(
                image_id=row.get("image_id"),
                path=row["path"],
                expected_sha256=row["sha256"],
                available=path.is_file(),
                actual_sha256=digest(path) if path.is_file() else None,
            )
        )
    write(
        out / "MEDIA_AVAILABILITY.json",
        dict(
            selected_records=available,
            work_root=str(ROOT.parent / "work"),
            visual_review="not inferred from availability",
        ),
    )
    write(out / "AUDIO_INTERVALS.json", audio_intervals(plan, ROOT))
    capability = json.loads((out / "LUMI_CAPABILITY.json").read_text())
    packets = {}
    for sid in plan["production_sequences"]:
        packet = resolve_sequence(plan, sid, ROOT)
        packet["capability"] = capability
        packets[sid] = packet
        write(out / (sid + ".json"), packet)
        if sid in {
            "s01_opening",
            "s01_empty_hold",
            "s02_acorn",
            "s03_fork",
            "s05_trip",
        }:
            build(packet, ROOT, out / sid)
    write(out / "READINESS.json", {sid: evaluate(p) for sid, p in packets.items()})
    coverage = json.loads((folder / "selected_images/COVERAGE_GAPS.json").read_text())
    rows = []
    for gap in coverage["missing_planned_keys"]:
        iid = gap["image_id"]
        matches = [
            u
            for p in packets.values()
            for u in p["resolved_images"]
            if u.get("image_id") == iid
        ]
        resolved = next(
            (u for u in matches if u["status"].startswith("selected_")), None
        )
        if resolved:
            status = resolved["status"]
            action = (
                "Reuse exact selected source; technical edge review remains required."
            )
        elif iid=='S03-L001-B01-I01':
            status='planned_slot_unfilled_editorial_hold_authored'
            action='The narration/beat establishes a pause at the fork, not a visible arrival. Explicit S03-fork-establishment uses selected after-state directly. This planned I01 stays unfilled and is not forward-aliased.'
        elif iid.startswith("S04"):
            status = "missing_distinct_state"
            action = "Decide actual movement endpoint versus explicitly authored hold; do not generate automatically."
        elif iid == "S02-L002-B01-I01":
            status = "hold_or_missing_state_pending_review"
            action = "Review whether the environment insert is a true hold; no assumed new lighting event."
        else:
            status = "missing_distinct_state"
            action = {
                "S01-L001-B01-I01": "Milo walk start; the empty establishment is not this slot.",
                "S01-L002-B03-I01": "Walking contact in this winding-path setup, not a foraging image.",
                "S01-L003-B01-I01": "Walking contact in the distinct deeper-woodland setup.",
                "S01-L004-B03-I01": "Grounded approach: whole acorn remains on ground before pickup.",
                "S01-L004-B03-I02": "Newly acquired whole acorn; hands hold it before tasting.",
                "S01-L004-B03-I04": "Tasted endpoint after taste event; I03 stays whole before tasting.",
                "S02-L001-B01-I01": "Initial holding/sky attention in the shared setup; stale gaze labels are not prompts.",
                "S02-L004-B01-I01": "Coherent pre-rise state; standing duplicate cannot depict stood up.",
                "S03-L001-B01-I01": "First fork before-state or explicit editorial hold decision; no forward self-alias.",
                "S05-L008-B01-I01": "Grounded approach before actual rear-paw catch.",
                "S05-L008-B01-I03": "Forward pitch after actual catch; reconcile pending historical request first.",
                "S05-L009-B01-I04": "Nose landing after ground roll; preserve scale and sleeping/waking chronology.",
                "S05-L010-B01-I01": "Closed-eye wake-start portrait or explicit cut coverage; Milo remains offscreen at nose.",
            }.get(
                iid,
                "Review required distinct state against current narration and neighbors.",
            )
        rows.append(dict(gap, classification=status, next_action=action))
    write(
        out / "GAP_CLASSIFICATION.json",
        dict(
            source="selected_images/COVERAGE_GAPS.json",
            source_sha256=digest(folder / "selected_images/COVERAGE_GAPS.json"),
            recorded_gap_count=len(rows),
            rows=rows,
            generation_requests=0,
        ),
    )
    manifest_path = folder / "handoff/s01_s03/render_run_20261024/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    baseline = []
    for row in manifest["clips"]:
        path = (
            ROOT.parent
            / "work/stories/lion_and_mouse_v7/shots"
            / Path(row["video"]).name
        )
        receipt_path = manifest_path.parent / row["receipt"]
        receipt = json.loads(receipt_path.read_text())
        result = dict(
            clip=row["clip"],
            path=str(path),
            available=path.is_file(),
            expected_sha256=row["video_sha256"],
            actual_sha256=digest(path) if path.is_file() else None,
            receipt_sha256=digest(receipt_path),
            receipt_hash_matches=digest(receipt_path) == row["receipt_sha256"],
            end_image=receipt.get("end_keyframe"),
            end_image_sha256=receipt.get("end_keyframe_sha256"),
            full_motion_review="not performed this run",
        )
        if args.baseline_decode and path.is_file():
            state, reason = inspect_media(
                path,
                dict(
                    width=receipt["width"],
                    height=receipt["height"],
                    frames=receipt["frames"],
                    fps=16,
                ),
            )
            result["decode"] = dict(status=state, reason=reason)
        baseline.append(result)
    write(
        out / "HISTORICAL_BASELINE.json",
        dict(
            clips=baseline,
            scope="historical single-image pilots; no approval transferred to sequence execution",
        ),
    )
    print(
        json.dumps(
            dict(
                selected_records=len(available),
                hash_mismatches=sum(
                    r["expected_sha256"] != r["actual_sha256"] for r in available
                ),
                audio_lines=sum(
                    len(v["intervals"]) for v in audio_intervals(plan, ROOT).values()
                ),
                sequences=len(packets),
                historical_clips=len(baseline),
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
