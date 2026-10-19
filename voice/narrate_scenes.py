#!/usr/bin/env python3
"""Render a story's narration with the Gemini voices: one WAV per scene.

  source voice/gemini_env.sh
  python voice/narrate_scenes.py --lines stories/lion_and_mouse_v5/dialogue_coverage.json \\
      --story lion_and_mouse_v5 --lang en [--scenes 1 2] [--redo]

Input: a JSON with `lines`: [{id, scene, speaker, performance_direction, text}]
(the v4 dialogue_coverage.json format; a relative path is taken from the repo
root). The text is spoken as written: `--lang` only names the output folder,
so another language needs its own translated lines file. Each line is spoken
by its speaker's voice (`--voices-file` and `--voices`, default
narrator/lion/mouse -> the saved voices in voice/), with its performance
direction as Gemini's style note, then the lines of a scene are joined with
short pauses.

A speaker can have several voices (a chorus, e.g. three ducklings): each voice
speaks the line into its own file, lines/<ID>_v1.wav, _v2, ... (for layering in
the edit), and the scene file carries their mix, as long as the longest take.
  --voices-file stories/<story>/voices.yaml   SPEAKER: folder, or a list of folders
  --voices SPEAKER=folder[,folder...]          overrides, after the file

Output (git-ignored), under work/stories/<story>/audio/<lang>/:
  sceneNN.wav       one file per scene (for the animatic and the edit)
  lines/<ID>.wav    every line alone (+ .json: text, voice, style, seconds)
  timing.json       seconds per line and per scene
Existing line files are reused (delete one, or --redo, to re-render it).

Rate limits: one call every MIN_GAP s. One attempt per line by default; explicit
--attempts and --max-requests control any approved retry budget. A rerun resumes
saved lines. V7 additionally requires a versioned --out-root and --max-requests.
--dry-run works without credentials or google-genai and lists requests only.
The API key comes from GEMINI_API_KEY (never printed or written).
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import sys
import time
import wave
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from speak import MIN_GAP, MODEL, synthesize, to_wav, create_client  # noqa: E402
from feltwillow import paths  # noqa: E402

VOICES = {"NARRATOR": "narrators/moonlight_storyteller_1", "LION": "cast/leo", "MOUSE": "cast/milo"}
PAUSE_SAME = 0.45      # seconds between two lines of the same speaker
PAUSE_CHANGE = 0.70    # seconds when the speaker changes (production/timing_sheet.py repeats both)
TAIL = 1.0             # silence at the end of each scene
_last_call = [0.0]


def speak(client, voice: str, text: str, style: str, *, attempts=1, before_call=None) -> tuple[bytes, int]:
    """One line -> PCM16 mono; retries require an explicit attempt budget."""
    for attempt in range(1, attempts + 1):
        if before_call:
            before_call()
        time.sleep(max(0.0, _last_call[0] + MIN_GAP - time.time()))
        _last_call[0] = time.time()
        try:
            data, mime = synthesize(client, voice, text, style, MODEL)
            with wave.open(io.BytesIO(to_wav(data, mime))) as w:
                if (w.getnchannels(), w.getsampwidth()) != (1, 2):
                    raise ValueError(f"expected 16-bit mono, got {w.getnchannels()} channel(s), "
                                     f"{8 * w.getsampwidth()} bit")
                return w.readframes(w.getnframes()), w.getframerate()
        except Exception as e:                     # rate limit / timeout / no audio / transient error
            code = getattr(e, 'code', None)
            status = f', HTTP {code}' if isinstance(code, int) else ''
            print(f"    attempt {attempt}/{attempts} failed ({type(e).__name__}{status}); no response content logged", flush=True)
            if attempt < attempts:
                time.sleep(20)
    raise SystemExit(f"giving up on: {text[:60]}")


def write_wav(path: Path, frames: bytes, rate: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(frames)


def mix(takes: list[bytes]) -> bytes:
    """Several PCM16 takes of one line, started together: their sum scaled by
    1/sqrt(n) (about the loudness of one voice), clipped; as long as the longest."""
    import array
    arrs = [array.array("h", t) for t in takes]
    n, g = max(len(a) for a in arrs), 1 / len(arrs) ** 0.5
    out = array.array("h", bytes(2 * n))
    for i in range(n):
        v = sum(a[i] for a in arrs if i < len(a)) * g
        out[i] = max(-32768, min(32767, int(v)))
    return out.tobytes()


def read_wav(path: Path) -> tuple[bytes, int]:
    with wave.open(str(path)) as w:
        return w.readframes(w.getnframes()), w.getframerate()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lines", type=Path, required=True)
    ap.add_argument("--story", required=True)
    ap.add_argument("--lang", default="en")
    ap.add_argument("--scenes", nargs="+", type=int)
    ap.add_argument("--voices-file", type=Path,
                    help="YAML SPEAKER: folder (or list of folders, relative to voice/)")
    ap.add_argument("--voices", nargs="+", default=[],
                    help="SPEAKER=folder[,folder...] overrides, e.g. NARRATOR=narrators/golden_hour_storyteller_3")
    ap.add_argument("--redo", action="store_true")
    ap.add_argument('--out-root', type=Path,
                    help='explicit final audio directory, e.g. voice/narration/lion_and_mouse_v7/en/r001')
    ap.add_argument('--dry-run', action='store_true', help='list exact line/voice requests and output paths; no key/API needed')
    ap.add_argument('--attempts', type=int, default=1, help='max attempts per line; default 1, no automatic paid retries')
    ap.add_argument('--max-requests', type=int, help='hard cap on attempted provider requests in this invocation')
    args = ap.parse_args()
    if args.attempts < 1 or (args.max_requests is not None and args.max_requests < 1):
        ap.error('attempt and request budgets must be positive')
    if args.story == 'lion_and_mouse_v7' and args.redo:
        ap.error('v7 recordings are immutable revisions; use a new --out-root revision instead of --redo')

    if bad := [v for v in args.voices if "=" not in v]:
        sys.exit(f"--voices takes SPEAKER=folder, got {bad}")
    voices = dict(VOICES)
    if args.voices_file:
        vf = args.voices_file if args.voices_file.is_absolute() else paths.REPO / args.voices_file
        voices.update(yaml.safe_load(vf.read_text())["voices"])
    voices.update({k: v.split(",") for k, v in (x.split("=", 1) for x in args.voices)})
    voices = {sp: [f] if isinstance(f, str) else list(f) for sp, f in voices.items()}
    ids = {sp: [yaml.safe_load((HERE / f / "voice.yaml").read_text())["voice_id"] for f in fs]
           for sp, fs in voices.items()}
    lines = json.loads((args.lines if args.lines.is_absolute() else paths.REPO / args.lines).read_text())["lines"]
    todo = [line for line in lines if not args.scenes or line["scene"] in args.scenes]
    # checked before the first call, so a missing voice does not waste the daily quota
    if missing := sorted({line["speaker"] for line in todo} - ids.keys()):
        sys.exit(f"no voice for speaker(s) {missing}: add --voices SPEAKER=folder")
    out = args.out_root.resolve() if args.out_root else paths.story_audio(args.story, args.lang)
    if args.story == 'lion_and_mouse_v7' and not args.out_root:
        ap.error('v7 requires an explicit versioned --out-root to keep recordings outside disposable work folders')
    if args.story == 'lion_and_mouse_v7' and not re.fullmatch(r'r[0-9]{3,}', out.name):
        ap.error('v7 --out-root must end in a recording revision such as r001')
    request_plan = []
    for line in todo:
        for k, vid in enumerate(ids[line['speaker']]):
            suffix = f'_v{k+1}' if len(ids[line['speaker']]) > 1 else ''
            target = out / 'lines' / f"{line['id']}{suffix}.wav"
            if not target.exists() or args.redo:
                request_plan.append({'line_id': line['id'], 'speaker': line['speaker'], 'voice': vid,
                    'model': MODEL, 'text': line['text'], 'style': line.get('performance_direction', ''),
                    'output': str(target), 'max_attempts': args.attempts})
    if args.dry_run:
        print(json.dumps({'story': args.story, 'language': args.lang, 'out_root': str(out),
            'requests_without_retries': len(request_plan),
            'maximum_attempts': sum(r['max_attempts'] for r in request_plan),
            'request_budget': args.max_requests, 'requests': request_plan,
            'note': 'No API called. Fresh recordings have new hashes/durations; old timing is not reusable.'}, indent=2))
        return
    if not os.environ.get('GEMINI_API_KEY'):
        sys.exit('GEMINI_API_KEY is not set: use voice/gemini_local.py run or voice/gemini_env.sh')
    if args.story == 'lion_and_mouse_v7' and args.max_requests is None:
        ap.error('v7 requires --max-requests matching the concrete approved batch')
    client = create_client()             # keep a reference: an unreferenced client closes itself
    attempted = 0
    def before_call():
        nonlocal attempted
        if args.max_requests is not None and attempted >= args.max_requests:
            raise SystemExit('Approved request budget reached; saved line WAVs are retained for resume.')
        attempted += 1

    timing = json.loads((out / "timing.json").read_text()) if (out / "timing.json").is_file() else {}
    for scene in sorted({line["scene"] for line in todo}):
        chunks, rate, rows, prev = [], None, [], None
        for line in [x for x in todo if x["scene"] == scene]:
            takes = []
            for k, (vid, folder) in enumerate(zip(ids[line["speaker"]], voices[line["speaker"]])):
                suffix = f"_v{k + 1}" if len(ids[line["speaker"]]) > 1 else ""
                f = out / "lines" / f"{line['id']}{suffix}.wav"
                if f.is_file() and not args.redo:
                    if args.story == 'lion_and_mouse_v7':
                        sidecar = f.with_suffix('.json')
                        if not sidecar.is_file():
                            raise SystemExit(f'{f.name}: missing receipt; review before reusing existing audio')
                        prior = json.loads(sidecar.read_text())
                        expected = {'text': line['text'], 'voice': vid, 'model': MODEL,
                                    'lang': args.lang, 'style': line.get('performance_direction', '')}
                        if any(prior.get(k) != v for k, v in expected.items()) or prior.get('sha256') != hashlib.sha256(f.read_bytes()).hexdigest():
                            raise SystemExit(f'{f.name}: source specification or WAV hash changed; use a new revision')
                    takes.append(read_wav(f))
                    continue
                t0 = time.time()
                style = line.get("performance_direction", "")
                pcm, r = speak(client, vid, line["text"], style, attempts=args.attempts, before_call=before_call)
                write_wav(f, pcm, r)
                f.with_suffix(".json").write_text(json.dumps(dict(
                    id=line["id"], scene=scene, speaker=line["speaker"], voice=vid,
                    voice_folder=folder, model=MODEL, text=line["text"],
                    style=style, lang=args.lang,
                    sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
                    provider_receipt=getattr(synthesize, 'last_receipt', None),
                    seconds=round(len(pcm) / 2 / r, 2), render_seconds=round(time.time() - t0, 1)), indent=2))
                print(f"  {line['id']}{suffix} {line['speaker']:9s} {len(pcm) / 2 / r:5.1f} s", flush=True)
                takes.append((pcm, r))
            if len({r for _, r in takes}) > 1:
                raise SystemExit(f"sample rates differ between the voices of {line['id']}")
            pcm, r = takes[0] if len(takes) == 1 else (mix([p for p, _ in takes]), takes[0][1])
            if rate and r != rate:
                raise SystemExit(f"sample rate changed ({rate} -> {r}) in {line['id']}")
            rate = r
            if prev is not None:
                gap = PAUSE_SAME if prev == line["speaker"] else PAUSE_CHANGE
                chunks.append(b"\0\0" * int(gap * rate))
            chunks.append(pcm)
            prev = line["speaker"]
            rows.append(dict(id=line["id"], speaker=line["speaker"], seconds=round(len(pcm) / 2 / rate, 2)))
        chunks.append(b"\0\0" * int(TAIL * rate))
        pcm = b"".join(chunks)
        write_wav(out / f"scene{scene:02d}.wav", pcm, rate)
        timing[str(scene)] = dict(seconds=round(len(pcm) / 2 / rate, 2), lines=rows)
        (out / "timing.json").write_text(json.dumps(timing, indent=2))
        print(f"scene {scene:2d}: {len(pcm) / 2 / rate:6.1f} s ({len(rows)} lines) -> {out / f'scene{scene:02d}.wav'}", flush=True)
    total = sum(v["seconds"] for v in timing.values())
    print(f"total {total / 60:.1f} min in {len(timing)} scenes")


if __name__ == "__main__":
    main()
