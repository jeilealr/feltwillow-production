# S01–S03 LUMI handoff

Owner selected all 26 current images, bound to exact hashes in `../../scene_image_selection.json`. There are 18 audio lines (S01 four, S02 four, S03 ten), plus three assembled scene WAVs. Images and receipts are in Git; full narration WAVs are deliberately excluded. No video has been rendered or approved by this handoff.

## On LUMI after pulling the branch

Run from the repository root in the existing LUMI environment. The local Mac conda path is not used on LUMI.

```bash
git pull --ff-only origin wan-new-image-approach
bash lumi/run_in_container.sh python production/opening_handoff.py validate
bash lumi/run_in_container.sh python production/opening_handoff.py prepare-pilots
bash lumi/run_in_container.sh python production/shot.py --story lion_and_mouse_v7 --scene 1 --shot s01_l001_b01_i02 --fast --dry-run
```

`prepare-pilots` is CPU-only. It freezes selected input bytes under `work/stories/lion_and_mouse_v7/keyframes/opening_pilot/` and derives `stories/lion_and_mouse_v7/story.yaml` from the handoff proposals. It refuses to overwrite a different runtime. No model is loaded and no job is submitted. Each proposal is an 81-frame, 16-fps, seed-1 single-image animation test at 1280×720, not a narration-duration assertion. Review prompts in `CLIP_PROPOSALS.json` before spending GPU time.

Inside a GPU allocation, remove `--dry-run` from that one-shot command to test animation. Existing receipt-aware `lumi/render_story.sh` can inventory/queue the prepared runtime, but it retries missing outputs and renders all 26 proposals: start with one pilot and inspect it before requesting a full queue. This handoff did not submit jobs.

## Narration transfer, separate from Git

`AUDIO_TRANSFER_MANIFEST.json` records exact WAV hashes and `audio-transfer-files.txt` gives repository-relative files. From the Mac checkout, after confirming the remote checkout path, copy with:

```bash
rsync -av --files-from=stories/lion_and_mouse_v7/handoff/s01_s03/audio-transfer-files.txt ./ lumi:/scratch/project_465002727/jelealro/feltwillow-production/
```

That is a suggested manual command, not a transfer already executed. The earlier voice backup may instead be under `/scratch/project_465002727/jelealro/feltwillow-video-control/voice`; preserve the manifest-relative hierarchy when restoring it. On LUMI run `production/opening_handoff.py validate --require-audio` after restoration. Do not assume Git restored WAVs.

## What remains before a finished movie

The 26 images are reviewed representative stills, not every endpoint in the authored audio-visual plan. Single-image pilots can start now; a complete no-cut/story-timed export remains pending phrase/key alignment, missing endpoints (including S01 whole-to-tasted I04), contact/prop continuity review and later dialogue/lip-sync. Exact fork/S02 background pixels and some prop/anatomy checks have known technical flags; owner visual selection preserves those observations. The first forest+walk line is 9.96 s, not automatically one 5-second clip. Do not invent equal timing windows.

All 161 r001 line recordings now exist locally. S13–S16 have actual audio bindings and remain pending visual authoring; no new beats or images were invented. A clone without WAVs can validate the selected-image handoff; full local-audio inventory checks require restoring audio.

## Cleanup

`CLEANUP_MANIFEST.json` lists discarded duplicate HTML backups, superseded console logs and a bytecode cache, with hashes and a verified local recovery archive. Original/source images and immutable receipts remain because current source-chain hashes and tests reference them. No canonical image, audio file or unrelated version was removed.
