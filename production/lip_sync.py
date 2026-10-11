#!/usr/bin/env python3
"""Align narration words and animate approved mouth shapes on chosen dialogue clips.

  python production/lip_sync.py align --story lion_and_mouse_v6 --audio-story lion_and_mouse_v6 --lang en --device cpu
  python production/lip_sync.py apply --story lion_and_mouse_v6

`align` uses WhisperX forced alignment against the exact recorded line text. `apply` takes the
owner-selected clip, maps word times through the chain timing plan, and composites only the
approved closed/open mouth difference into the source frames. The first and last frames are
preserved exactly for chain continuity. Outputs are separate from source renders and hash-bound
in work/stories/<story>/lipsync/lipsync_manifest.json.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "production"))
from feltwillow import paths  # noqa: E402
from feltwillow.version_policy import require_story_local_audio  # noqa: E402
from feltwillow.lipsync import line_audio_path, recipe_sha256  # noqa: E402
from feltwillow.media import locate_ffmpeg, read_frames  # noqa: E402
from chain_plan import line_spans  # noqa: E402
from chain_preview import find_take  # noqa: E402

ALIGN_SCHEMA = "feltwillow.word-timings.v1"
SYNC_SCHEMA = "feltwillow.lip-sync.v1"
VOWELS = re.compile(r"[aeiouy]+", re.I)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def audio_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / wav.getframerate()


def token(text: str) -> str:
    return re.sub(r"[^\w']", "", text, flags=re.UNICODE).casefold()


def alignment_path(audio_story: str, lang: str) -> Path:
    return paths.story_audio(audio_story, lang) / "word_timings.json"


def align(args) -> None:
    require_story_local_audio(args.story, args.audio_story, consumer="lip_sync align")
    # WhisperX shells out to `ffmpeg` by name; expose the private bundled binary.
    private_ffmpeg = Path(sys.executable).parent / "ffmpeg"
    if private_ffmpeg.is_file():
        os.environ["PATH"] = f"{private_ffmpeg.parent}{os.pathsep}{os.environ.get('PATH', '')}"
    try:
        import whisperx
    except ImportError as exc:
        raise SystemExit("word alignment needs WhisperX; install voice/requirements-lipsync.txt") from exc

    story_dir = paths.STORIES / args.story
    cov = load_json(story_dir / "dialogue_coverage.json")
    audio_dir = paths.story_audio(args.audio_story, args.lang)
    output = alignment_path(args.audio_story, args.lang)
    previous = load_json(output) if output.is_file() and not args.redo else {}
    device = args.device
    try:
        version = importlib.metadata.version("whisperx")
    except importlib.metadata.PackageNotFoundError:
        version = "unknown"
    model, metadata = whisperx.load_align_model(language_code=args.lang, device=device)
    rows = {}
    failed = []
    for line in cov["lines"]:
        lid = line["id"]
        if args.scenes and line["scene"] not in args.scenes:
            cached = previous.get("lines", {}).get(lid)
            if cached:
                cached = dict(cached)
                audio_file = line_audio_path(audio_dir, cached.get("audio_file", ""))
                if audio_file:
                    cached["audio_file"] = audio_file.relative_to(audio_dir).as_posix()
                rows[lid] = cached
            continue
        wav_path = audio_dir / "lines" / f"{lid}.wav"
        if not wav_path.is_file():
            alternatives = sorted((audio_dir / "lines").glob(f"{lid}_v*.wav"))
            if alternatives:
                wav_path = alternatives[0]
            else:
                failed.append(f"{lid}: missing line audio {wav_path}")
                continue
        transcript = line["text"].strip()
        audio_hash = sha256_file(wav_path)
        cached = previous.get("lines", {}).get(lid)
        if (cached and cached.get("audio_sha256") == audio_hash
                and cached.get("transcript") == transcript
                and cached.get("speaker") == line["speaker"]
                and cached.get("scene") == line["scene"] and not args.redo):
            cached = dict(cached)
            cached["audio_file"] = wav_path.relative_to(audio_dir).as_posix()
            rows[lid] = cached
            continue
        audio = whisperx.load_audio(str(wav_path))
        duration = len(audio) / 16000.0
        segments = [{"start": 0.0, "end": duration, "text": transcript}]
        result = whisperx.align(segments, model, metadata, audio, device,
                                return_char_alignments=False)
        words = []
        for seg in result.get("segments", []):
            for word in seg.get("words", []):
                if word.get("start") is None or word.get("end") is None:
                    continue
                start, end = float(word["start"]), float(word["end"])
                if not (math.isfinite(start) and math.isfinite(end) and 0 <= start < end <= duration + 0.05):
                    continue
                words.append({"text": word.get("word", "").strip(), "start": round(start, 4),
                              "end": round(min(end, duration), 4), "score": word.get("score")})
        if not words:
            failed.append(f"{lid}: aligner returned no word timings")
            continue
        aligned_tokens = [token(w["text"]) for w in words]
        expected_tokens = [token(x) for x in re.findall(r"[\w']+", transcript, flags=re.UNICODE)]
        missing_tokens = [x for x in expected_tokens if x not in aligned_tokens]
        rows[lid] = {"scene": line["scene"], "speaker": line["speaker"], "transcript": transcript,
                     "audio_file": wav_path.relative_to(audio_dir).as_posix(), "audio_sha256": audio_hash,
                     "audio_seconds": round(duration, 4), "words": words,
                     "unaligned_expected_tokens": missing_tokens,
                     "alignment_status": "review" if missing_tokens else "aligned"}
        print(f"{lid}: {len(words)} words" + (f"; review {missing_tokens}" if missing_tokens else ""),
              flush=True)
    if failed:
        raise SystemExit("alignment incomplete:\n  " + "\n  ".join(failed))
    doc = {"schema": ALIGN_SCHEMA, "story": args.story, "audio_story": args.audio_story,
           "lang": args.lang, "aligner": "WhisperX forced alignment", "aligner_version": version,
           "device": device, "lines": rows}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(rows)} lines -> {output}")


def piece_word_cues(story: str, row: dict, word_doc: dict) -> list[dict]:
    story_dir = paths.STORIES / story
    plan = load_json(story_dir / "timing_plan.json")
    coverage = load_json(story_dir / "dialogue_coverage.json")
    audio_dir = paths.story_audio(plan.get("audio_story", story), plan.get("lang", "en"))
    timing = load_json(audio_dir / "timing.json")
    spans = line_spans(coverage["lines"], timing)
    line_starts = {ln["id"]: start for scene_rows in spans.values()
                   for ln, start, _ in scene_rows}
    rows = plan["segments"]
    scene_start = min(r["film_start"] for r in rows if r["scene"] == row["scene"])
    piece_start = row["film_start"] - scene_start
    piece_end = piece_start + row["seconds"]
    variants = [v for s in load_json(story_dir / "prompt_manifest.json")["shots"]
                if s["id"] == row["piece"] for v in s["variants"]
                if v["id"] == row["variant"]]
    if len(variants) != 1 or variants[0].get("mode") != "mouth":
        raise SystemExit(f"{row['piece']}: selected mouth variant {row['variant']} is missing or ambiguous")
    variant = variants[0]
    speaker = variant.get("speaker")
    if not speaker or token(speaker) == token("NARRATOR"):
        raise SystemExit(f"{row['piece']}: mouth mode has no explicit character speaker; narrator audio must never drive character lips")
    wanted_speaker = token(speaker)
    cues = []
    for lid in row["lines"]:
        rec = word_doc.get("lines", {}).get(lid)
        if not rec:
            raise SystemExit(f"{row['piece']}: no word alignment for {lid}")
        line = next((ln for ln in coverage["lines"] if ln["id"] == lid), None)
        if not line or rec.get("speaker") != line["speaker"] or rec.get("scene") != line["scene"] or rec.get("transcript") != line["text"].strip():
            raise SystemExit(f"{lid}: aligned speaker, scene or transcript differs from dialogue coverage; rerun alignment")
        audio_file = line_audio_path(audio_dir, rec.get("audio_file", ""))
        if not audio_file or rec.get("audio_sha256") != sha256_file(audio_file):
            raise SystemExit(f"{lid}: line audio changed since alignment; rerun alignment")
        if rec.get("alignment_status") != "aligned":
            raise SystemExit(f"{lid}: alignment needs review before lipsync")
        if token(rec.get("speaker", "")) == token("NARRATOR"):
            continue
        if token(rec.get("speaker", "")) != wanted_speaker:
            continue
        line_start = line_starts[lid]
        for word in rec["words"]:
            start = line_start + word["start"] - piece_start
            end = line_start + word["end"] - piece_start
            if end <= 0 or start >= row["seconds"]:
                continue
            cues.append({"text": word["text"], "start": max(0.0, start),
                         "end": min(row["seconds"], end), "line_id": lid})
    return sorted(cues, key=lambda x: (x["start"], x["end"]))


def _open_curve(word: str, t: float, start: float, end: float) -> float:
    """Broad syllable-timed jaw opening within one aligned word (not phoneme synthesis)."""
    if not start <= t <= end or end <= start:
        return 0.0
    letters = re.sub(r"[^a-z]", "", word.casefold())
    groups = list(VOWELS.finditer(letters))
    if not groups:
        return 0.14
    duration = end - start
    centers = [((g.start() + g.end()) / 2) / max(1, len(letters)) for g in groups]
    rel = (t - start) / duration
    width = max(0.12, min(0.32, 0.52 / len(centers)))
    pulse = max(max(0.0, 1.0 - abs(rel - c) / width) for c in centers)
    # Labial stops close the mouth at the edge of a word; endpoint keyframes remain authoritative.
    if letters[:1] in ("m", "b", "p") and rel < 0.10:
        return 0.0
    if letters[-1:] in ("m", "b", "p") and rel > 0.90:
        return 0.0
    return min(0.92, 0.12 + 0.78 * pulse)


def _alpha_at(t: float, cues: list[dict]) -> float:
    return max((_open_curve(c["text"], t, c["start"], c["end"]) for c in cues), default=0.0)


def _anchors_and_mask(closed_path: Path, open_path: Path, size: tuple[int, int], roi: tuple[float, ...]):
    closed = np.asarray(Image.open(closed_path).convert("RGB").resize(size, Image.Resampling.LANCZOS), dtype=np.uint8)
    opened = np.asarray(Image.open(open_path).convert("RGB").resize(size, Image.Resampling.LANCZOS), dtype=np.uint8)
    diff = np.max(np.abs(opened.astype(np.int16) - closed.astype(np.int16)), axis=2)
    w, h = size
    x0, y0, x1, y1 = (round(roi[0] * w), round(roi[1] * h), round(roi[2] * w), round(roi[3] * h))
    local = diff[y0:y1, x0:x1]
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[y0:y1, x0:x1] = (local >= 18).astype(np.uint8) * 255
    pil = Image.fromarray(mask).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
    alpha = np.asarray(pil, dtype=np.float32) / 255.0
    area = float(np.count_nonzero(alpha > 0.2)) / (w * h)
    if not 0.00002 <= area <= 0.05:
        raise SystemExit(f"mouth difference mask is ambiguous ({area:.3%} of frame); adjust the character's mouth_animation.roi or review the endpoint images")
    return closed.astype(np.float32), opened.astype(np.float32), alpha[:, :, None]


def render_piece(story: str, row: dict, source: Path, output: Path,
                 cues: list[dict], manifest: dict, bible: dict, fps: int):
    shot = next(s for s in manifest["shots"] if s["id"] == row["piece"])
    variant = next(v for v in shot["variants"] if v["id"] == row["variant"])
    if variant.get("mode") != "mouth":
        raise SystemExit(f"{row['piece']}: only mouth variants receive timed mouth animation")
    endpoints = [manifest["_image_index"][rid] for rid in
                 (variant.get("start_image", shot["start_image"]), variant.get("end_image", shot["end_image"]))]
    if any(r.get("mouth_character") or r.get("mouth") for r in endpoints):
        raise SystemExit(f"{row['piece']}: open-mouth boundary would animate during a silent pause; use closed endpoints")
    mouth_image_id = variant.get("mouth_open_image")
    if mouth_image_id:
        open_rec = manifest["_image_index"].get(mouth_image_id)
        if not open_rec:
            raise SystemExit(f"{row['piece']}: separate mouth anchor is missing")
        bases = [r["id"] for r in open_rec.get("ordered_references", []) if r.get("role") == "edit_base"]
        closed_by_id = {r["id"]: r for r in endpoints}
        if len(bases) != 1 or bases[0] not in closed_by_id:
            raise SystemExit(f"{row['piece']}: open-mouth anchor must be an edit of one closed endpoint")
        close_rec = closed_by_id[bases[0]]
    else:
        opens = [r for r in endpoints if r.get("mouth_character") or r.get("mouth")]
        closes = [r for r in endpoints if not (r.get("mouth_character") or r.get("mouth"))]
        if len(opens) != 1 or len(closes) != 1:
            raise SystemExit(f"{row['piece']}: needs one marked open-mouth image and one closed endpoint, or a separate mouth_open_image anchor")
        open_rec, close_rec = opens[0], closes[0]
    char = open_rec.get("mouth_character") or open_rec.get("mouth")
    char_record = bible.get("characters", {}).get(char, {}) if char else {}
    if not char_record or token(char_record.get("voice_speaker", "")) != token(variant.get("speaker", "")):
        raise SystemExit(f"{row['piece']}: approved open-mouth character must match the declared audio speaker")
    open_path, closed_path = REPO / open_rec["target"], REPO / close_rec["target"]
    if not open_path.is_file() or not closed_path.is_file():
        raise SystemExit(f"{row['piece']}: approved closed/open mouth images are not generated yet")
    frames = read_frames(source)
    if len(frames) != row["frames"]:
        raise SystemExit(f"{row['piece']}: {source.name} has {len(frames)} frames, expected {row['frames']}")
    h, w = frames.shape[1:3]
    roi = bible["characters"][char].get("mouth_animation", {}).get("roi", [0.25, 0.30, 0.75, 0.78])
    closed, opened, mask = _anchors_and_mask(closed_path, open_path, (w, h), tuple(roi))
    speed = float(row["speed"])
    output.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = locate_ffmpeg()
    proc = subprocess.Popen([ffmpeg, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-an", "-c:v", "libx264",
                             "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p", "-movflags",
                             "+faststart", str(output)], stdin=subprocess.PIPE)
    assert proc.stdin is not None
    try:
        for index, frame in enumerate(frames):
            if index == 0 or index == len(frames) - 1:
                result = frame
            else:
                film_t = (index / fps) / speed
                amount = _alpha_at(film_t, cues)
                anchors = closed * (1.0 - amount) + opened * amount
                result = np.clip(frame.astype(np.float32) * (1.0 - mask) + anchors * mask, 0, 255).astype(np.uint8)
            proc.stdin.write(result.tobytes())
    finally:
        proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit(f"ffmpeg failed writing {output}")
    return {"character": char, "mouth_mask_area": round(float(np.mean(mask > 0.2)), 6),
            "word_cues": cues, "source_fps": fps, "output_frames": len(frames)}


def apply(args) -> None:
    story_dir = paths.STORIES / args.story
    manifest = load_json(story_dir / "prompt_manifest.json")
    bible = load_json(story_dir / "visual_bible.json")
    plan = load_json(story_dir / "timing_plan.json")
    audio_story, lang = plan.get("audio_story", args.story), plan.get("lang", "en")
    require_story_local_audio(args.story, audio_story, consumer="lip_sync apply")
    wtiming = alignment_path(audio_story, lang)
    if not wtiming.is_file():
        raise SystemExit(f"missing aligned word timings: run `production/lip_sync.py align --story {args.story} --audio-story {audio_story} --lang {lang}`")
    word_doc = load_json(wtiming)
    if (word_doc.get("schema") != ALIGN_SCHEMA or word_doc.get("story") != args.story
            or word_doc.get("audio_story") != audio_story or word_doc.get("lang") != lang):
        raise SystemExit(f"word timing metadata does not match {audio_story}/{lang}")
    takes_path = story_dir / "takes.yaml"
    import yaml
    takes = yaml.safe_load(takes_path.read_text()) if takes_path.is_file() else {}
    rows = {r["piece"]: r for r in plan["segments"]}
    if args.pieces:
        rows = {k: v for k, v in rows.items() if k in set(args.pieces)}
    manifest["_image_index"] = {r["id"]: r for r in manifest["images"]}
    sync_root = paths.story_work(args.story) / "lipsync"
    sync_root.mkdir(parents=True, exist_ok=True)
    index_path = sync_root / "lipsync_manifest.json"
    index = load_json(index_path) if index_path.is_file() else {"schema": SYNC_SCHEMA, "story": args.story, "pieces": {}}
    from chain_preview import find_take
    missing = []
    changed = 0
    for row in rows.values():
        if row.get("mode") != "mouth":
            continue
        source, how = find_take(args.story, row, takes or {}, None, prefer_lipsync=False)
        if source is None:
            missing.append(f"{row['piece']}: {how}")
            continue
        cues = piece_word_cues(args.story, row, word_doc)
        if not cues:
            missing.append(f"{row['piece']}: no aligned speaker words fall inside this piece")
            continue
        recipe_hash = recipe_sha256(args.story, row["piece"])
        if recipe_hash is None:
            raise SystemExit(f"{row['piece']}: mouth recipe is incomplete; check timing, alignment and approved image anchors")
        src_hash = sha256_file(source)
        timing_hash = sha256_file(wtiming)
        outfile = sync_root / f"{row['piece']}_{src_hash[:10]}_{recipe_hash[:8]}.mp4"
        prior = index.get("pieces", {}).get(row["piece"], {})
        if (outfile.is_file() and not args.redo and prior.get("source_sha256") == src_hash
                and prior.get("word_timing_sha256") == timing_hash
                and prior.get("recipe_sha256") == recipe_hash
                and prior.get("output_sha256") == sha256_file(outfile)):
            continue
        details = render_piece(args.story, row, source, outfile, cues, manifest, bible, plan.get("fps", 16))
        stat = source.stat()
        out_stat = outfile.stat()
        index["pieces"][row["piece"]] = {
            "variant": row["variant"], "source_file": str(source.resolve()), "source_sha256": src_hash,
            "source_size": stat.st_size, "source_mtime_ns": stat.st_mtime_ns,
            "output_file": str(outfile.resolve()), "output_sha256": sha256_file(outfile),
            "output_size": out_stat.st_size, "output_mtime_ns": out_stat.st_mtime_ns,
            "word_timing_file": str(wtiming.resolve()), "word_timing_sha256": timing_hash,
            "recipe_sha256": recipe_hash, "retime_speed": row["speed"], **details}
        changed += 1
        print(f"{row['piece']}: {len(cues)} word cues -> {outfile}", flush=True)
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    if missing:
        raise SystemExit("lip-sync incomplete:\n  " + "\n  ".join(missing))
    print(f"{changed} mouth clips processed -> {index_path}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    a = sub.add_parser("align", help="create forced word timings for narration line WAVs")
    a.add_argument("--story", required=True, help="visual story whose dialogue_coverage.json supplies text")
    a.add_argument("--audio-story", help="audio folder owner; defaults to --story")
    a.add_argument("--lang", default="en")
    a.add_argument("--device", default="cpu", choices=("cpu", "cuda"))
    a.add_argument("--scenes", nargs="+", type=int)
    a.add_argument("--redo", action="store_true")
    a.set_defaults(func=align)
    r = sub.add_parser("apply", help="animate word-timed mouth movement on all chosen mouth clips")
    r.add_argument("--story", required=True)
    r.add_argument("--pieces", nargs="+", help="limit to selected piece IDs")
    r.add_argument("--redo", action="store_true")
    r.set_defaults(func=apply)
    args = ap.parse_args()
    if args.command == "align" and not args.audio_story:
        args.audio_story = args.story
    args.func(args)


if __name__ == "__main__":
    main()
