# Three-voice narration pilot — approval pending

Endpoint: `POST https://generativelanguage.googleapis.com/v1beta/interactions`.

Model: `gemini-3.8-flash-tts`; **3 requests**, one per voice. Application and SDK transport attempts are both one; no retries. Output: WAV, with text/voice/style/hash receipts. No seed exposed.

Standard paid estimate: **about $0.004 total**, expected below $0.01 at previous durations. This is an estimate, not a billing cap. Published rates checked 19 October 2026: $0.50 / million input text tokens and $9 / million audio tokens; 25 audio tokens per second. Previous total duration was 13.8 seconds; fresh duration and token usage determine actual billing. [Official pricing](https://ai.google.dev/gemini-api/docs/pricing#gemini-3.8-flash-tts).

Exact request payloads and all input/code SHA-256 values are in `OPERATION.json`.

## NARRATOR — S01-L001

Voice: `voice_v5bpq98uj7qh`

Once upon a time, at the edge of a wide and peaceful forest, there lived a little mouse who loved exploring.

Performance direction: warm, inviting, gentle sense of wonder

## LION — S05-L011

Voice: `voice_zdbgqrcerxqu`

What in the forest was THAT?

Performance direction: startled, deep and imposing but not frightening

## MOUSE — S02-L003

Voice: `voice_vf2w20rcys8a`

Oh! It's getting late!

Performance direction: startled realization, then hurried but playful

## Input files

- `stories/lion_and_mouse_v7/narration_pilot/lines.json` — `1e2b9a5b501c36f476b4e8871ffcfd589afa50a6e60d3bed473ab6145d85c654`
- `voice/narrators/moonlight_storyteller_1/voice.yaml` — `0f8fe7d28cc4cda22e47c587d27543d1f379d3c895165da79be73acf85a66ed5`
- `voice/cast/leo/voice.yaml` — `d1d3d8b6d970dd79f19b24e39bffc010e8e6604c596ea4b5d23d55aca96fb362`
- `voice/cast/milo/voice.yaml` — `e6d07a7770d79bff8849cff3353932755b3bdf5456d152e56c5962e0de7f78f4`

Local output: `voice/narration/lion_and_mouse_v7/en/pilot/r001/`. These are isolated pilot lines, not complete scenes. Preserve and review actual WAVs before any full-story batch. No API generation request has been made.
