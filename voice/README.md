# Gemini 3.8 Flash TTS voices

Owner's choice (2026-09-27) for narration and character voices; the Chatterbox
tools in `voice/` are paused. Gemini runs on Google's servers: no GPU, no LUMI
job; any login-node shell works.

## Local Mac setup and v7 recordings

Use the existing `feltwillow` conda environment and `voice/gemini_local.py` on macOS. The LUMI environment script below activates scratch-specific paths and is not the local zsh setup. Follow [v7 narration setup and backup](narration/lion_and_mouse_v7/README.md) for secure key reuse, offline request planning, versioned output, request budgets and the owner's requested LUMI voice archive. `narrate_scenes.py` now defaults to one request attempt; the historical two-attempt notes below are superseded. No regeneration batch has been submitted.

## Setup (once)

1. API key, stored by the owner outside every repo:
   ```
   mkdir -p ~/.config/gemini && chmod 700 ~/.config/gemini
   read -s -p "Gemini API key: " K && printf 'GEMINI_API_KEY=%s\n' "$K" > ~/.config/gemini/env && chmod 600 ~/.config/gemini/env && unset K
   ```
2. Client: `/scratch/project_465002727/jelealro/gemini_env/venv` (google-genai
   2.25.0; voice design needs >= 2.25.0).

## Use

```bash
cd /scratch/project_465002727/jelealro
source voice/gemini_env.sh
python voice/list_voices.py      # -> voices_list.json
```

## Facts (checked 2026-09-27; see CLAUDE.md for sources)

- Models: `gemini-3.8-flash-tts` (quality), `gemini-3.8-flash-lite-tts`.
- Designed ("prompted") voices: stored per project, **200 voices max, 1-year
  TTL**. Keep each chosen voice's prompt and id here so it can be recreated.
- Price (paid tier): ~$0.0135 per minute of audio until 2026-12-31, ~$0.027
  from 2027 (25 audio tokens/s). Free tier: rate-limited.
- **Rate limits, Tier 1 (seen 2026-10-01, AI Studio > Rate limits): Gemini 3.8
  Flash TTS = 10 requests/min, 10K tokens/min, 100 requests/day**, reset at
  midnight Pacific (09:00 in Germany). Retries count. Past the daily limit the
  API does not return an error: calls just hang. `narrate_scenes.py` waits 8 s
  between calls, tries each line at most twice (90 s limit per call) and stops
  the run if a line fails twice; a full 160-line story needs two days.
- Outputs are the owner's ("Google won't claim ownership"); SynthID watermark.
- Open question for Google: API terms exclude services "directed towards or
  likely to be accessed by individuals under the age of 18".

## Cast

Every voice folder: `voice.yaml` (id, name, model, the exact design prompt,
expiry, notes) and `google_sample.wav` (the sample Google stores with the
voice; no audio was generated for it). Save a voice with
`python voice/save_voice.py --id <voice_id> --dir <folder> --role <role>`.

| Role | Voice | Folder |
|---|---|---|
| Leo | The Noble Lion 1 (`voice_zdbgqrcerxqu`) | `cast/leo/` |
| Milo | The Brave Little Mouse 1 (`voice_vf2w20rcys8a`) | `cast/milo/` |
| narrator (alternative) | The Fireside Grandfather 2 (`voice_4rdl7hydi35v`) | `narrators/fireside_grandfather_2/` |
| **narrator (Lion and Mouse v2)** | Moonlight Storyteller 1 (`voice_v5bpq98uj7qh`) | `narrators/moonlight_storyteller_1/` |
| narrator (alternative) | Golden Hour Storyteller 3 (`voice_g00mo8cbdefq`) | `narrators/golden_hour_storyteller_3/` |
| **narrator (The Ugly Duckling)** | The Cheery Tale Keeper 2 (`voice_8tnxrhfqk3ur`) | `narrators/cheery_tale_keeper_2/` |
| narrator (alternative) | Bright Trail Narrator 2 (`voice_tcrjw3ney7q8`) | `narrators/bright_trail_narrator_2/` |

**The Ugly Duckling** (owner, 2026-10-06; cast file `stories/ugly_duckling_v1/voices.yaml`):

| Role | Voice | Folder |
|---|---|---|
| Ollie (cygnet and swan) | Ollie 1 (`voice_07kspefjri22`) | `cast/ugly_duckling_v1/ollie/` |
| Mama Duck | Gacrux (Gemini prebuilt, no expiry) | `cast/ugly_duckling_v1/mama_duck/` |
| Ottie | Ottie the Otter 1 (`voice_i1odi373fxko`) | `cast/ugly_duckling_v1/ottie/` |
| the Swan | Algieba (Gemini prebuilt, no expiry) | `cast/ugly_duckling_v1/swan/` |
| the Ducklings (one voice for all three) | The 3 Ducklings 3 (`voice_mep0f54paagg`); 1 and 2 (`voice_wkpdjuv6njc9`, `voice_jtbo57dz6457`) saved, unused | `cast/ugly_duckling_v1/duckling_3/` |

Prebuilt voices (Gacrux, Algieba) are used by name; `voices.get` does not return them, so
their `voice.yaml` is written by hand. The ducklings first spoke with three voices at once, but the
three spoke at different speeds, so the owner chose one voice (2026-10-06; duckling_3: highest
pitch, steadiest pace). `narrate_scenes.py` still supports it: a speaker with a list of voices is
rendered once per voice into `lines/<ID>_v1.wav`, `_v2`, `_v3` for layering in the edit;
the scene file has their mix. The Ugly Duckling's designed voices expire on 2027-10-05.

`cast/` holds character voices (Lion and Mouse at the top, other stories in `cast/<story>/`); `narrators/` is the pool of narrator voices.
A story picks its voices in its `story.yaml` (`voices:`), e.g. the Lion and
Mouse v2 narrator is `narrators/moonlight_storyteller_1`. Samples:
`google_sample.wav` (Google's own) and `sample_scene*.wav` (story lines). All designed voices
expire on 2027-09-27: recreate each from its saved prompt before then.

## Languages

English is the default and keeps the plain file name; every other language
adds its code: `sample_scene01_line0.wav` (en), `sample_scene01_line0_es.wav`
(Spanish), `_de` German, `_fr` French, `_ru` Russian. The same voice id speaks
every language (Gemini detects the language from the text). Each file's .json
keeps the exact text spoken.

| Voice | Languages sampled |
|---|---|
| every narrator (Scene 1 line) | en, es, fr, de, ru, uk |
| cast/leo ("Go on your way") | en, es, fr, de, ru, uk |
| cast/milo ("Thank you") | en, es, fr, de, ru, uk |

One sample line per voice (owner). Render missing ones with
`python voice/render_samples.py` (texts in `sample_lines.yaml`).
