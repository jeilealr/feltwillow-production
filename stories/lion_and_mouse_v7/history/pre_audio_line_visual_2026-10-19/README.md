# Lion and the Mouse v7

The v7 draft is migrated to a tested paired-image workflow. All 52 narrative units map to **146 provisional action pieces, 175 unique endpoints and 95 shared boundaries**. No new scene endpoint images have been generated, selected or owner approved; canonical identity and existing location-master approval are recorded separately. Audio timing remains provisional; this is not a finished image set or video-ready packet.

## What is available

The owner approved both v7 canonicals and existing location masters on 19 October 2026. V7 canonical filenames start at r01; original v6 revisions and hashes remain in provenance:

| Actor | V7 path | Source and destination SHA-256 |
|---|---|---|
| Leo | `character/characters/lion_and_mouse_v7/Leo/canonical/full-body_leo_neutral_pose_r01.png` | `6b587c8ee2739767bb7af056ee3176ec3d2e698a5bed0e013263814ee8059545` |
| Milo | `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` | `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f` |

Approval scope is identity only, inherited from the recorded v6 authority. No atlas was imported as approved performance authority. All nine existing v7 location copies match the registered v6 source hashes. Original scene candidates/foreground layers and **161 line WAVs plus 16 scene WAVs are missing**. Exact recovery paths/hashes are in `migration_report.json`; restore originals if recoverable, or follow the owner-authorized regeneration plan below. Never substitute SVG thumbnails.

The original v7 records are preserved byte-for-byte under `history/pre_paired_2026-10-19/`; their original hashes are in the migration report. `SCRIPT.md` and the copied timing metadata are unchanged. The morning S01 introduction is retained as an explicit introductory view with a cut to the afternoon stream. New neutral setup/support/crop approvals remain pending.

## Authored versus derived

Edit `character_library.json`, `location_library.json`, `shot_plan.json`, the existing script/audio records and scoped review/selection evidence. Fixed setup crops, neutral anatomical calibration and named state records prevent independent pose-box resizing, contact-following crops and world resets. Story-specific irreversible transitions live in the shot plan's event rules, not shared Python.

`derived/generation_manifest.json`, `derived/resume_queue.json`, `derived/SHOT_INVENTORY.md` and `review/paired/sequence/` are generated review outputs. Old `visual_unit_plan.json`, `GENERATION_PROMPTS.json` and SVG sheets retain historical draft content and are labeled accordingly. Active registration/composition wrappers reject the old unsafe bbox path.

Provisional piece intervals partition all 161 copied playback spans exactly, including pauses/tails. Long actions are incremental phases of one action; equal provisional timing windows are not word alignment. Restore audio and review action timing before a render plan is frozen. Revisit hold lengths/pacing and performance-specific close views during the pilot.

## Commands and validation

Use the existing conda environment; no new temporary environment is needed:

```bash
conda activate feltwillow
python production/paired_images.py --story lion_and_mouse_v7 validate
python production/paired_images.py --story lion_and_mouse_v7 readiness --gate source
python production/paired_images.py --story lion_and_mouse_v7 readiness --gate image
python production/paired_images.py --story lion_and_mouse_v7 derive
python production/paired_review.py --story lion_and_mouse_v7 --out stories/lion_and_mouse_v7/review/paired/sequence
python production/verify_audio_manifest.py --story lion_and_mouse_v7
python production/v7_runtime.py --story lion_and_mouse_v7 --preflight
python -m unittest discover -s tests -p 'test_*.py'
```

Structural validation and source readiness pass. Image/video readiness intentionally fail while foundation calibration, actual endpoints, audio and reviews are absent. CPU tests cover import/hash rejection, fixed/common transforms, pose/group calibration, portrait support, vacated-background restoration, transparent holes, pair geometry/pixel rejection, causal/offscreen state, interval coverage/speaker rules, atomic immutable registration/selection and mocked two-endpoint Wan preprocessing. V5/v6 behavior stays on its original paths. See `review/paired/validation/` for results and temporary-file cleanup evidence.

See [paired workflow](../../docs/paired-image-workflow.md) for calibrated composition, immutable registration, selection, pair-difference review and CPU Wan contract commands. A selected candidate is not approved. Planned endpoints stay separate from actual rendered boundary frames, and no Wan/TTS/GPU work is authorized by this packet.

## Review order and resume

1. Inspect [exact canonical sources](review/paired/foundation/canonical_sources.png); this is a reference comparison, not a scale anchor.
2. Canonical identity and existing location masters are now owner approved. The earlier Leo matte-extraction request is deferred; its price was unknown and it was never submitted. Derive a separate production matte only when composition requires it. Prepare the local Gemini environment using the linked narration guide; no further story text is needed.
3. Review any needed production mattes, neutral shared-scale foundation, minimum pilot performance views, registered support anchors/crops/axis and close-view detail. Foundation candidates do not approve themselves. No universal silhouette-height target is used.
4. Build the pilot queue flagged in `shot_plan.json`: solo Milo/acorn, shared Great Tree, trip chain, same-state S05/S06 handoff and portrait, trap activation and main-knot/rope chain. Review actual start/end pixels and adjacent state before owner foundation/pilot acceptance.
5. Continue the remaining chronological queue only after foundation/pilot review and concrete paid-generation approval where required. Restore audio independently; image-only work may proceed while it is missing. Video and dialogue readiness remain separate gates.

Starting HEAD: `8bc175a7444999d6147cd90ae96f82159c7c76dc`, branch `main`, clean before implementation. Changes are local; no staging, commits or pushes were performed. V6 assets, approvals and research are preserved. The next local step is Gemini setup and read-only voice-access verification. Foundation staging and a concretely approved narration/image pilot follow.

## Owner update — 19 October 2026

Both v7 canonicals and the existing location masters are approved. Both canonical filenames now start at `r01` for independent v7; source v6 revision names and exact hashes are retained in `character_library.json` and `owner_foundation_acceptance.json`. Milo already has RGBA transparency; Leo retains his approved RGB studio background. No pixel changes or canonical regeneration were needed. Future production mattes remain separate derivatives.

The owner authorized regenerating missing narration in principle. All 161 exact text lines, performance directions and prior voice assignments are retained. See [local Gemini setup and versioned narration storage](../../voice/narration/lion_and_mouse_v7/README.md) and `audio_regeneration_plan.json`. The proposed LUMI archive is `/scratch/project_465002727/jelealro/feltwillow-video-control/voice/narration/lion_and_mouse_v7/en/r001/`, with a matching local copy. No remote upload or TTS generation has occurred; concrete paid batch approval remains required. New recordings will have new hashes/durations and require fresh alignment and shot timing.

Current verification after the owner clarification: 26 focused paired-image/local-Gemini tests pass; compilation and source readiness pass. The full 130-test run has one repository-link-check error because a tracked v5 README was removed by an unrelated concurrent change. Those v5 deletions were not made or reverted by this work; all other tests pass.
