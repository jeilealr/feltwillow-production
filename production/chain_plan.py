#!/usr/bin/env python3
"""Time a chained story's pieces from its narration (CR-21): the audio is the timeline.

  python3 production/chain_plan.py --story lion_and_mouse_v6 --audio-story lion_and_mouse_v6 suggest
  python3 production/chain_plan.py --story lion_and_mouse_v6 --audio-story lion_and_mouse_v6 check
  python3 production/chain_plan.py --story lion_and_mouse_v6 --audio-story lion_and_mouse_v6 apply

Reads the narration timing (work/stories/<audio story>/audio/<lang>/timing.json, from
voice/narrate_scenes.py), the line list (stories/<story>/dialogue_coverage.json) and the pieces
(the shots of stories/<story>/prompt_manifest.json, each with `lines`).

How a piece gets its time. Inside a scene every line owns the span from its start to the next
line's start (the pause after it included; the last line also owns the scene's 1 s tail), so the
spans add up to the scene's audio exactly. A piece lists the lines it covers, in order;
consecutive pieces may share a line, and a shared line's span is split evenly between them. A
piece lasts the sum of its shares. Its clip length is the Wan length (4k+1 frames, 49 to 81 at
16 fps) closest to that, and the rest is a retime: speed = clip seconds / piece seconds, allowed
from 0.80 to 1.25 (RIFE in post). So a piece covers 2.45 s to 6.33 s; outside that, change the
plan (merge pieces or split a line over more pieces). Pieces are never trimmed: the cut-off part
would be the image the next piece starts on.

  suggest   every line with its span and the number of pieces it needs on its own (no pieces read)
  check     report coverage and bounds; exit 1 on an error. A `reuse` piece keeps its rendered
            frame count (81 for v5 clips), so it must last 4.05 to 6.33 s
  apply     check, then write each variant's `frames` into the manifest, and write
            stories/<story>/TIMING_SHEET.md and timing_plan.json (the edit plan: start, length,
            frames and speed of every piece; nothing is held or stretched)
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from feltwillow import paths  # noqa: E402
from feltwillow.version_policy import require_story_local_audio  # noqa: E402

FPS = 16
FRAME_CHOICES = list(range(49, 82, 4))              # Wan: 4k+1 frames, 49..81
MIN_SPEED, MAX_SPEED = 0.80, 1.25
MIN_S, MAX_S = FRAME_CHOICES[0] / FPS / MAX_SPEED, FRAME_CHOICES[-1] / FPS / MIN_SPEED
PAUSE_SAME, PAUSE_CHANGE = 0.45, 0.70               # must match voice/narrate_scenes.py


def fmt(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:04.1f}"


def frames_for(seconds: float) -> tuple[int, float]:
    """Wan frame count closest to the piece's seconds, and the playback speed that fits it."""
    n = min(FRAME_CHOICES, key=lambda f: abs(f / FPS - seconds))
    return n, (n / FPS) / seconds


def validate_timing_input(lines: list[dict], timing: dict) -> list[str]:
    """Validate line/timing identity, durations, and the narration writer's pauses/tail."""
    errors = []
    if not isinstance(lines, list) or any(not isinstance(ln, dict) for ln in lines):
        return ["dialogue_coverage.json lines must be a list of objects"]
    if not isinstance(timing, dict):
        return ["timing.json must be an object keyed by scene"]
    ids = [ln.get("id") for ln in lines]
    if any(not isinstance(i, str) for i in ids) or len(ids) != len(set(ids)):
        errors.append("dialogue_coverage.json has a missing, non-string or duplicate line id")
    if any(not ln.get("speaker") for ln in lines):
        errors.append("dialogue_coverage.json has a line with no speaker")
    scenes = sorted({ln.get("scene") for ln in lines})
    expected_scene_keys = {str(scene) for scene in scenes}
    extra_scenes = set(timing) - expected_scene_keys
    if extra_scenes:
        errors.append(f"timing.json has scenes absent from dialogue_coverage.json: {sorted(extra_scenes)}")
    for scene in scenes:
        key = str(scene)
        t = timing.get(key)
        if t is None:
            errors.append(f"scene {scene}: missing timing entry {key!r}")
            continue
        if not isinstance(t, dict):
            errors.append(f"scene {scene}: timing entry must be an object")
            continue
        rows = t.get("lines", [])
        if not isinstance(rows, list):
            errors.append(f"scene {scene}: timing lines must be a list")
            continue
        if any(not isinstance(r, dict) for r in rows):
            errors.append(f"scene {scene}: timing line records must be objects")
            continue
        tids = [r.get("id") for r in rows]
        if any(not isinstance(i, str) for i in tids) or len(tids) != len(set(tids)):
            errors.append(f"scene {scene}: timing.json has a missing, non-string or duplicate line id")
            continue
        expected = [ln["id"] for ln in lines if ln.get("scene") == scene]
        if set(tids) != set(expected):
            errors.append(f"scene {scene}: timing line IDs differ (missing {sorted(set(expected)-set(tids))}; "
                          f"extra {sorted(set(tids)-set(expected))})")
            continue
        durations = []
        invalid = False
        for row in rows:
            value = row.get("seconds")
            if not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
                errors.append(f"scene {scene}: line {row['id']} duration must be finite and positive")
                invalid = True
            else:
                durations.append((row["id"], float(value)))
        scene_seconds = t.get("seconds")
        if not isinstance(scene_seconds, (int, float)) or not math.isfinite(scene_seconds) or scene_seconds <= 0:
            errors.append(f"scene {scene}: scene duration must be finite and positive")
            invalid = True
        if not invalid:
            by_id = dict(durations)
            ordered = [ln for ln in lines if ln.get("scene") == scene]
            total = sum(by_id[ln["id"]] for ln in ordered) + 1.0
            for before, after in zip(ordered, ordered[1:]):
                total += PAUSE_SAME if before["speaker"] == after["speaker"] else PAUSE_CHANGE
            tolerance = max(0.05, 0.005 * len(ordered) + 0.02)
            if abs(total - float(scene_seconds)) > tolerance:
                errors.append(f"scene {scene}: line durations + pauses + 1 s tail total {total:.2f}s, "
                              f"but timing.json says {scene_seconds:.2f}s (tolerance {tolerance:.2f}s)")
    return errors


def line_spans(lines: list[dict], timing: dict) -> dict[int, list[tuple[dict, float, float]]]:
    """Per scene: (line, start, span) with span = start of the next line (or the scene end) - start."""
    out = {}
    for scene in sorted({ln["scene"] for ln in lines}):
        t = timing.get(str(scene))
        if not t:
            continue
        secs = {r["id"]: r["seconds"] for r in t["lines"]}
        sl = [ln for ln in lines if ln["scene"] == scene]
        starts, cur, prev = [], 0.0, None
        for ln in sl:
            if prev is not None:
                cur += PAUSE_SAME if prev == ln["speaker"] else PAUSE_CHANGE
            starts.append(cur)
            cur += secs[ln["id"]]
            prev = ln["speaker"]
        ends = starts[1:] + [t["seconds"]]
        out[scene] = [(ln, a, b - a) for ln, a, b in zip(sl, starts, ends)]
    return out


def plan(manifest: dict, spans: dict) -> tuple[list[dict], list[str]]:
    """Seconds, frames and speed for every piece; errors for gaps, order and bounds."""
    errors, rows = [], []
    raw_pieces = manifest["shots"]
    valid_orders = all(isinstance(p, dict) and type(p.get("order")) is int for p in raw_pieces)
    if not valid_orders:
        errors.append("piece order values must be integers")
    pieces = sorted(raw_pieces, key=lambda s: s.get("order") if isinstance(s, dict) and
                    type(s.get("order")) is int else 0)
    orders = [p.get("order") for p in pieces]
    if valid_orders:
        if len(orders) != len(set(orders)):
            errors.append("piece order values must be unique")
        if orders != list(range(1, len(pieces) + 1)):
            errors.append("piece order values must be contiguous from 1 through the number of pieces")
    film_t = 0.0
    for scene, sp in spans.items():
        order = {ln["id"]: k for k, (ln, _, _) in enumerate(sp)}
        mine = [p for p in pieces if p["scene"] == scene]
        users = {ln["id"]: [] for ln, _, _ in sp}
        last = -1
        for p in mine:
            ids = p.get("lines") or []
            bad = [i for i in ids if i not in order]
            if bad or not ids:
                errors.append(f"{p['id']}: lines {bad or ids} are not scene {scene} narration lines")
                continue
            idx = [order[i] for i in ids]
            if idx != list(range(idx[0], idx[-1] + 1)):
                errors.append(f"{p['id']}: lines {ids} are not consecutive")
            if idx[0] < last:
                errors.append(f"{p['id']}: starts on {ids[0]}, before the previous piece's last line")
            last = idx[-1]
            for i in ids:
                users[i].append(p["id"])
        for ln, _, _ in sp:
            if not users[ln["id"]]:
                errors.append(f"scene {scene}: line {ln['id']} is covered by no piece")
        share = {ln["id"]: span / max(1, len(users[ln["id"]])) for ln, _, span in sp}
        start = {ln["id"]: a for ln, a, _ in sp}
        t = film_t
        for p in mine:
            ids = [i for i in (p.get("lines") or []) if i in share]
            if not ids:
                continue
            secs = sum(share[i] for i in ids)
            v = p["variants"][0]
            if p.get("reuse"):            # an earlier render: its frame count is fixed, only the speed fits it
                frames = v.get("frames", 81)
                speed = (frames / FPS) / secs
            else:
                frames, speed = frames_for(secs)
            if not MIN_SPEED - 1e-6 <= speed <= MAX_SPEED + 1e-6:
                errors.append(f"{p['id']}: {secs:.2f} s needs speed {speed:.2f} for {frames} frames "
                              f"(allowed {MIN_SPEED}-{MAX_SPEED}); merge pieces or split the line over more pieces")
            rows.append(dict(piece=p["id"], scene=scene, variant=v["id"], mode=v.get("mode"),
                             film_start=round(t, 3), seconds=round(secs, 3), frames=frames,
                             speed=round(speed, 3), lines=ids, join_in=p.get("join_in"),
                             cut_reason=p.get("cut_reason"), transition=p.get("transition", "cut"),
                             start_image=p["start_image"], end_image=p["end_image"],
                             reuse=p.get("reuse"), first_line_start=round(film_t + start[ids[0]], 3)))
            t += secs
        film_t += sum(span for _, _, span in sp)
    scenes_with_pieces = {p["scene"] for p in pieces}
    for s in sorted(scenes_with_pieces - set(spans)):
        errors.append(f"scene {s}: pieces but no narration timing")
    return rows, errors


def write_sheet(story: str, lang: str, audio_story: str, rows: list[dict], spans: dict,
                manifest: dict) -> None:
    sd = paths.STORIES / story
    img = {i["id"]: i.get("target") for i in manifest["images"]}
    lines = {ln["id"]: (ln, a, span) for sp in spans.values() for ln, a, span in sp}
    scene_t, t = {}, 0.0
    for scene, sp in spans.items():
        scene_t[scene] = (t, sum(span for *_, span in sp))
        t += scene_t[scene][1]
    md = [f"# Timing sheet: {story} ({lang}), chained coverage", "",
          f"Generated by `production/chain_plan.py` from the narration of `{audio_story}` and the pieces in "
          "`prompt_manifest.json`; do not edit by hand. Every second of narration is covered by exactly one "
          "piece; nothing is held or stretched. A piece's clip is rendered at the frame count shown and "
          "retimed by the speed shown (RIFE in post). `chain` = starts on the previous piece's end image; "
          "`cut (...)` = a planned cut and its reason (CR-21).", "", "## Summary", "",
          "| Scene | Narration | Pieces | New renders | Reused | Speed range |", "|---|---|---|---|---|---|"]
    for scene, (a, secs) in scene_t.items():
        r = [x for x in rows if x["scene"] == scene]
        sp = [x["speed"] for x in r] or [1]
        md.append(f"| {scene} | {secs:.1f} s | {len(r)} | {sum(1 for x in r if not x['reuse'])} | "
                  f"{sum(1 for x in r if x['reuse'])} | {min(sp):.2f}-{max(sp):.2f} |")
    md.append(f"| **total** | **{fmt(t)}** | {len(rows)} | {sum(1 for x in rows if not x['reuse'])} | "
              f"{sum(1 for x in rows if x['reuse'])} | |")
    for scene, (a, secs) in scene_t.items():
        md += ["", f"## Scene {scene:02d} ({fmt(a)} - {fmt(a + secs)}, {secs:.1f} s, audio `scene{scene:02d}.wav`)", "",
               "| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |",
               "|---|---|---|---|---|---|---|---|"]
        for x in (x for x in rows if x["scene"] == scene):
            join = "chain" if x["join_in"] == "chain" else f"cut ({x['cut_reason']}, {x['transition']})"
            ends = " → ".join(f"`{Path(img.get(i) or i).name}`" for i in (x["start_image"], x["end_image"]))
            reuse = f" (reuses `{x['reuse']['variant']}`)" if x["reuse"] else ""
            md.append(f"| {fmt(x['film_start'])} | {x['seconds']:.2f} s | `{x['piece']}`{reuse} | {join} | "
                      f"{x['frames']} | {x['speed']:.2f} | {ends} | {', '.join(x['lines'])} |")
        md += ["", "<details><summary>Lines</summary>", ""]
        for ln, start, span in (lines[i] for i in lines if lines[i][0]["scene"] == scene):
            md.append(f"- `{ln['id']}` {fmt(a + start)} ({span:.1f} s incl. pause) **{ln['speaker']}**: {ln['text']}")
        md += ["", "</details>"]
    (sd / "TIMING_SHEET.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (sd / "timing_plan.json").write_text(json.dumps(dict(
        story=story, lang=lang, audio_story=audio_story, fps=FPS, kind="chained_coverage",
        seconds=round(t, 3), segments=rows), indent=2) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", required=True)
    ap.add_argument("--lang", default="en")
    ap.add_argument("--audio-story", help="story whose work/ folder holds the narration (default: --story)")
    ap.add_argument("cmd", choices=["suggest", "check", "apply"])
    args = ap.parse_args()
    audio_story = args.audio_story or args.story
    require_story_local_audio(args.story, audio_story, consumer="chain_plan")
    sd = paths.STORIES / args.story
    timing = json.loads((paths.story_audio(audio_story, args.lang) / "timing.json").read_text())
    lines = json.loads((sd / "dialogue_coverage.json").read_text(encoding="utf-8"))["lines"]
    input_errors = validate_timing_input(lines, timing)
    if input_errors:
        for error in input_errors:
            print("ERROR:", error)
        sys.exit(1)
    spans = line_spans(lines, timing)

    if args.cmd == "suggest":
        total = 0
        for scene, sp in spans.items():
            secs = sum(s for *_, s in sp)
            print(f"\nScene {scene} ({secs:.1f} s, at least {math.ceil(secs / MAX_S)} pieces, "
                  f"about {round(secs / (81 / FPS))} at full length)")
            for ln, a, span in sp:
                need = math.ceil(span / MAX_S)
                print(f"  {ln['id']} {fmt(a)} {span:5.2f} s  {need} piece(s) alone   "
                      f"{ln['speaker'][:5]:5} {ln['text'][:70]}")
            total += secs
        print(f"\ntotal {fmt(total)}; a piece covers {MIN_S:.2f}-{MAX_S:.2f} s")
        return

    mp = sd / "prompt_manifest.json"
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    rows, errors = plan(manifest, spans)
    for e in errors:
        print("ERROR:", e)
    covered = sum(r["seconds"] for r in rows)
    print(f"{len(rows)} pieces cover {fmt(covered)} of {fmt(sum(s for sp in spans.values() for *_, s in sp))}; "
          f"{len(errors)} errors")
    if errors:
        sys.exit(1)
    if args.cmd == "apply":
        frames = {r["piece"]: r["frames"] for r in rows}
        changed = 0
        for s in manifest["shots"]:
            v = s["variants"][0]
            if s["id"] in frames and v.get("frames") != frames[s["id"]]:
                v["frames"] = frames[s["id"]]
                changed += 1
        mp.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        write_sheet(args.story, args.lang, audio_story, rows, spans, manifest)
        print(f"{changed} frame counts updated; wrote {sd / 'TIMING_SHEET.md'} and timing_plan.json")


if __name__ == "__main__":
    main()
