# Lion and the Mouse v7 narration

Current local r001 availability is 98 line WAV/JSON pairs and 12 complete scene assemblies (S01–S12). S13–S16 have 63 pending script lines. Actual WAV samples own timing. The active semantic visual plan is `stories/lion_and_mouse_v7/audio_visual_plan.json`; `dialogue_coverage.json` is its derived text/performance index. Historical regeneration settings and original voice IDs remain in `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/audio_regeneration_plan.json`. No synthesis is authorized by the visual-planning migration.
Local recording revision: `voice/narration/lion_and_mouse_v7/en/r001/`.

Matching LUMI destination, inside the owner's requested voice directory:
`/scratch/project_465002727/jelealro/feltwillow-video-control/voice/narration/lion_and_mouse_v7/en/r001/`.

WAVs are deliberately ignored by Git; text, voice settings, receipts and checksum manifests remain available for reconstruction and review. After every approved batch, keep both a local copy and a checksum-verified LUMI copy, plus an independent backup outside LUMI scratch. LUMI does not automatically back up storage; moving data between scratch folders alone does not prevent loss. See [LUMI storage policy](https://docs.lumi-supercomputer.eu/storage/).

## Local API setup

From the production repository root:

```bash
conda activate feltwillow
python -m pip install google-genai
python voice/gemini_local.py setup
python voice/gemini_local.py check
python voice/gemini_local.py run voice/list_voices.py
```

`setup` reuses an existing key in `~/.config/gemini/env` and secures its permissions. If there is no saved key, it prompts invisibly and saves outside the repository. Use `setup --replace` if you need a different key. The wrapper loads it only into the child process and does not print it. No key goes in chat, code, receipts or command arguments. Use a key associated with the same Google AI Studio project as the LUMI custom voices; verify the saved narrator, Leo and Milo voice IDs are accessible before selecting a paid batch. The final command lists voices; it does not synthesize audio.

Google documents key creation/loading in [Gemini API keys](https://ai.google.dev/gemini-api/docs/api-key). Setup and the offline check make no API calls. The existing `voice/gemini_env.sh` is a LUMI/Bash environment activator; the local wrapper avoids sourcing LUMI-specific paths from macOS zsh.

## Prepare and approve a batch

```bash
python voice/narrate_scenes.py --story lion_and_mouse_v7 --lines stories/lion_and_mouse_v7/dialogue_coverage.json --lang en --scenes 1 --out-root voice/narration/lion_and_mouse_v7/en/r001 --dry-run
```

This reports four prospective requests for Scene 1, with exact text, voice and style, and makes no API call. The full-story request plan has 161 lines. Before any paid run, resolve current pricing, show the concrete request count/text/voice/model/settings, estimate total cost and obtain explicit owner approval under `AGENTS.md`. The former approximately 11-minute timing is only historical; the new performance may differ. Do not use it as a fixed-duration generation contract.

Execution, **only after that concrete batch is approved**, uses the same arguments through `voice/gemini_local.py run voice/narrate_scenes.py`, removes `--dry-run` and adds `--max-requests` with the approved count. One attempt per request is the default. No automatic paid retry is implied. V7 requires a versioned output root and rejects `--redo`; replacements go into `r002` or later. Existing line reuse checks text, voice, style, model, language and the WAV hash. Partial completed line WAVs survive an interruption and are reused on a valid resume.

## Save and verify each batch

After actual WAVs exist, make a checksum manifest (works for partial batches):

```bash
python voice/narration_archive.py snapshot --audio-root voice/narration/lion_and_mouse_v7/en/r001
python voice/narration_archive.py verify --audio-root voice/narration/lion_and_mouse_v7/en/r001
```

When connected to LUMI, create the destination and copy that revision. These are backup commands, not generation commands:

```bash
ssh lumi 'mkdir -p /scratch/project_465002727/jelealro/feltwillow-video-control/voice/narration/lion_and_mouse_v7/en/r001'
rsync -av --checksum --ignore-existing --exclude SHA256SUMS --exclude archive_manifest.json voice/narration/lion_and_mouse_v7/en/r001/ lumi:/scratch/project_465002727/jelealro/feltwillow-video-control/voice/narration/lion_and_mouse_v7/en/r001/
rsync -av voice/narration/lion_and_mouse_v7/en/r001/SHA256SUMS voice/narration/lion_and_mouse_v7/en/r001/archive_manifest.json lumi:/scratch/project_465002727/jelealro/feltwillow-video-control/voice/narration/lion_and_mouse_v7/en/r001/
ssh lumi 'cd /scratch/project_465002727/jelealro/feltwillow-video-control/voice/narration/lion_and_mouse_v7/en/r001 && sha256sum -c SHA256SUMS'
```

Use the revision exclusively for this recording set and never use `rsync --delete`. If a conflicting remote revision exists, preserve it and choose a new revision instead of overwriting it. These remote commands have been prepared, not executed in this session; the local machine needs working LUMI SSH access. Keep another copy outside scratch.

Review words, voice identity, delivery, silence/clipping and complete scene assembly. New recordings require a new audio manifest, new actual durations and new alignment; do not change the old expected hashes to pretend byte-identical recovery. Adopt the reviewed recording revision explicitly into v7 runtime inputs and update the shot timing after review. Existing old-audio playback spans remain provisional history.

## Resume result — 19 October 2026, 12:27 UTC

The owner-generated first 97 line WAVs passed receipt/hash checks. At the owner’s explicit request to finish the remainder, the agent submitted a bounded resume with one attempt per missing line. `S12-L010` succeeded; `S13-L001` then reached the local 90-second timeout without a provider quota/billing code. No further retry was submitted. There are 98 saved line WAVs and 12 complete scene assemblies, with 63 lines remaining. This is not a confirmed insufficient-balance diagnosis.

All 209 currently saved audio/receipt/timing files were copied to the requested LUMI revision and verified there by SHA-256. Existing remote recordings were preserved; no remote files were deleted. See `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/validation/narration_lumi_backup.json`. New recordings remain pending speech review and alignment, separate from historical expected-audio hashes.
