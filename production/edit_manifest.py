#!/usr/bin/env python3
"""Export a hash-bound, film-order handoff for a complete chained edit.

  python3 production/edit_manifest.py --story lion_and_mouse_v6 --require-takes

Requires an owner-chosen take for every piece, including pieces reused from an earlier story.
The JSON is an edit contract for DaVinci Resolve or another editor; it does not render or assemble.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from feltwillow import paths  # noqa: E402
from feltwillow.version_policy import require_story_local_audio  # noqa: E402
from chain_preview import find_take, probe_frames  # noqa: E402
from feltwillow.lipsync import entry_for  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def invalid_carried_endpoints(manifest: dict, rows: list[dict]) -> list[str]:
    """An inherited file is usable only while its source review state is accepted."""
    images = {image["id"]: image for image in manifest["images"]}
    shots = {shot["id"]: shot for shot in manifest["shots"]}
    errors = []
    seen = set()
    for row in rows:
        shot = shots[row["piece"]]
        variant = next(v for v in shot["variants"] if v["id"] == row["variant"])
        for rid in (variant["start_image"], variant["end_image"]):
            rec = images[rid]
            if rid in seen or not rec.get("carried_from") or rec.get("status") == "accepted":
                continue
            seen.add(rid)
            errors.append(f"{row['piece']}: carried image {rid} has status "
                          f"{rec.get('status')!r}, not accepted")
    return errors


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", required=True)
    ap.add_argument("--out", type=Path, help="default: work/stories/<story>/review/edit_manifest.json")
    ap.add_argument("--require-takes", action="store_true", default=True,
                    help="require explicit chosen takes (always enabled for this export)")
    args = ap.parse_args()
    sd = paths.STORIES / args.story
    plan = json.loads((sd / "timing_plan.json").read_text())
    require_story_local_audio(args.story, plan.get("audio_story") or args.story,
                              consumer="edit_manifest")
    takes_path = sd / "takes.yaml"
    takes = yaml.safe_load(takes_path.read_text()) if takes_path.is_file() else {}
    rows = sorted(plan["segments"], key=lambda r: r["film_start"])
    manifest = json.loads((sd / "prompt_manifest.json").read_text())
    invalid_images = invalid_carried_endpoints(manifest, rows)
    if invalid_images:
        raise SystemExit("cannot export complete edit manifest:\n  " + "\n  ".join(invalid_images))
    entries, missing = [], []
    scene_offsets, cursor = {}, 0.0
    for scene in sorted({r["scene"] for r in rows}):
        scene_offsets[scene] = cursor
        cursor += sum(r["seconds"] for r in rows if r["scene"] == scene)
    for row in rows:
        clip, how = find_take(args.story, row, takes or {}, None)
        if clip is None:
            missing.append(f"{row['piece']}: {how}")
            continue
        if row.get("mode") == "mouth" and how != "lip-synced take":
            missing.append(f"{row['piece']}: timed mouth animation is missing; run production/lip_sync.py apply")
            continue
        lip_record = entry_for(args.story, row["piece"]) if how == "lip-synced take" else None
        clip = clip.resolve()
        nframes = probe_frames(clip)
        if nframes != row["frames"]:
            missing.append(f"{row['piece']}: {clip} has {nframes} frames; expected {row['frames']}")
            continue
        scene_audio = paths.story_audio(plan.get("audio_story") or args.story, plan.get("lang", "en")) / f"scene{row['scene']:02d}.wav"
        if not scene_audio.is_file():
            missing.append(f"scene {row['scene']}: narration file missing: {scene_audio}")
            continue
        source_story = (row.get("reuse") or {}).get("story", args.story)
        entries.append({
            "order": len(entries) + 1, "piece": row["piece"], "variant": row["variant"],
            "source_story": source_story, "source_file": str(clip), "source_sha256": sha256(clip),
            "source_frames": nframes, "source_fps": 16, "retime_speed": row["speed"],
            "lip_sync": ({"method": "word-timed approved-mouth composite",
                          "source_file": lip_record.get("source_file"),
                          "source_sha256": lip_record.get("source_sha256"),
                          "output_sha256": lip_record.get("output_sha256"),
                          "word_timing_sha256": lip_record.get("word_timing_sha256")}
                         if lip_record else None),
            "film_in": row["film_start"], "film_out": round(row["film_start"] + row["seconds"], 3),
            "join_in": row["join_in"], "cut_reason": row.get("cut_reason"),
            "transition": row.get("transition", "cut"),
            "audio_file": str(scene_audio.resolve()), "audio_sha256": sha256(scene_audio),
            "audio_in": round(row["film_start"] - scene_offsets[row["scene"]], 3),
            "audio_out": round(row["film_start"] - scene_offsets[row["scene"]] + row["seconds"], 3),
        })
    if missing:
        raise SystemExit("cannot export complete edit manifest:\n  " + "\n  ".join(missing))
    out = args.out or (paths.story_work(args.story) / "review" / "edit_manifest.json")
    if not out.is_absolute():
        out = paths.REPO / out
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = {"schema": "feltwillow.chained-edit.v1", "story": args.story,
           "audio_story": plan.get("audio_story", args.story), "lang": plan.get("lang", "en"),
           "fps": 24, "seconds": plan["seconds"], "assembly": "external editor; no media rendered",
           "segments": entries}
    out.write_text(json.dumps(doc, indent=2) + "\n")
    print(f"{len(entries)} chosen pieces -> {out}")


if __name__ == "__main__":
    main()
