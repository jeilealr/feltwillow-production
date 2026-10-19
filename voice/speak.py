#!/usr/bin/env python3
"""Speak one line with a Gemini 3.8 Flash TTS voice and save it as a WAV.

  source voice/gemini_env.sh
  python voice/speak.py --voice voice_g00mo8cbdefq \\
      --text "Once upon a time..." --out work/voices/test.wav \\
      [--style "warm bedtime storytelling"] [--model gemini-3.8-flash-tts]

Writes the WAV plus a .json sidecar (model, voice, text, style, mime, seconds).
The API key comes from GEMINI_API_KEY (never printed or written).
The other voice scripts share this file's API call (`synthesize`), its audio
helpers and its limits (MODEL, CALL_LIMIT, MIN_GAP).
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import signal
import sys
import wave
from pathlib import Path


MODEL = "gemini-3.8-flash-tts"
CALL_LIMIT = 90        # seconds per call: past the daily quota a call hangs instead of failing
MIN_GAP = 8.0          # seconds between calls: Tier 1 allows 10 requests/min, 10K tokens/min
                       # and 100 requests/day for this model (AI Studio > Rate limits)


def create_client():
    """Use the chosen Gemini key explicitly and disable hidden HTTP retries."""
    from google import genai
    from google.genai import types
    return genai.Client(api_key=os.environ['GEMINI_API_KEY'],
        http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=1)))


def audio_bytes(interaction) -> tuple[bytes, str]:
    """Find the audio payload in an Interaction, whatever its exact shape."""
    def walk(o, depth=0):
        if depth > 8 or o is None:
            return
        if isinstance(o, dict):
            items = o.items()
        elif hasattr(o, "model_dump"):
            items = o.model_dump().items()
        elif isinstance(o, (list, tuple)):
            for x in o:
                yield from walk(x, depth + 1)
            return
        else:
            return
        d = dict(items)
        if d.get("data") and ("mime_type" in d or "mimeType" in d or d.get("type") == "audio"):
            yield d
        for v in d.values():
            yield from walk(v, depth + 1)
    for d in walk(interaction):
        data = d["data"]
        if isinstance(data, str):
            data = base64.b64decode(data)
        return data, d.get("mime_type") or d.get("mimeType") or ""
    raise RuntimeError("no audio in the response")


def to_wav(data: bytes, mime: str | None) -> bytes:
    """WAV bytes: a RIFF file passes through; raw PCM16 mono is wrapped at the
    rate the mime type names (default 24 kHz)."""
    if data[:4] == b"RIFF":
        return data
    rate = 24000
    for part in (mime or "").split(";"):
        if part.strip().lower().startswith("rate="):
            rate = int(part.split("=", 1)[1])
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(data)
    return buf.getvalue()


def synthesize(client, voice: str, text: str, style: str = "", model: str = MODEL) -> tuple[bytes, str]:
    """One TTS request -> (audio bytes, mime type). Raises TimeoutError after
    CALL_LIMIT s (a call once hung for an hour) and RuntimeError without audio."""
    synthesize.last_receipt = None
    content = {"type": "text", "text": text}
    if style:
        content["annotations"] = [{"type": "speech_metadata", "style": style}]

    def _timeout(*_):
        raise TimeoutError(f"no answer in {CALL_LIMIT} s")

    previous = signal.signal(signal.SIGALRM, _timeout)
    signal.alarm(CALL_LIMIT)
    try:
        inter = client.interactions.create(
            model=model, input=[{"type": "user_input", "content": [content]}],
            response_format={"type": "audio"},
            generation_config={"speech_config": [{"voice": voice}]},
            timeout=120)
        def safe_value(value):
            if hasattr(value, 'model_dump'):
                return value.model_dump(mode='json')
            if isinstance(value, (dict, list, str, int, float, bool)) or value is None:
                return value
            return None
        # Retain provider identity/usage without audio payloads, URLs or credentials.
        synthesize.last_receipt = {
            'request_id': getattr(inter, 'id', None),
            'model': getattr(inter, 'model', model),
            'usage': safe_value(getattr(inter, 'usage', None)),
            'actual_cost': None,
        }
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
    return audio_bytes(inter)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--voice", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--style", default="")
    ap.add_argument("--model", default=MODEL)
    args = ap.parse_args()
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set: source voice/gemini_env.sh")
    client = create_client()             # keep a reference: an unreferenced client closes itself
    try:
        data, mime = synthesize(client, args.voice, args.text, args.style, args.model)
    except (TimeoutError, RuntimeError) as e:
        sys.exit(f"{args.out.name}: {e}")
    wav = to_wav(data, mime)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(wav)
    with wave.open(str(args.out)) as w:
        secs = w.getnframes() / w.getframerate()
    args.out.with_suffix(".json").write_text(json.dumps(dict(
        model=args.model, voice=args.voice, text=args.text, style=args.style,
        mime=mime, seconds=round(secs, 2)), indent=2))
    print(f"{args.out} ({secs:.1f} s, {mime})")


if __name__ == "__main__":
    main()
