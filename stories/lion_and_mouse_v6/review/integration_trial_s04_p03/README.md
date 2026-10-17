# Scene 04 p03 integration trial

New owner-authorized comparison, 2026-10-17; this does not reopen the completed perceptual-world review or replace a selected keyframe. Open [owner_review.html](owner_review.html) for the original/B/C slider, matching crops and full-resolution links.

B applies deterministic brightness shaping, restrained detail softening and additional supporting-foot contact shadow. It changes no character geometry or pigment hue. C uses a focused built-in ImageGen edit, then restores the original outside the selected RGBA silhouette and a small supporting-foot region; central eyes/muzzle/smile are also restored. C is warmer and has more modeled shading, but its interior wool/foot detail changes require inspection. Neither is adopted or a new technical approval.

The raw generator result also repainted background texture despite the prompt. It is retained as an input receipt, not a proposed whole-frame replacement. The bounded C candidate excludes those background changes. Exact source hashes, masks, operations, normalization and pixel checks are in `verification.json`; exact model instructions are in `integration_prompt.txt`. Original image, camera, staging, approvals, contact sheets and video-control implementation are unchanged.

Rebuild B/C and the comparison boards from the preserved raw result with Pillow, numpy and opencv-python:

```bash
export TMPDIR=/scratch/project_465002727/jelealro/tmp
python3 stories/lion_and_mouse_v6/review/integration_trial_s04_p03/build_trial.py \
  --generated stories/lion_and_mouse_v6/review/integration_trial_s04_p03/s04_p03_integration_generated_source_r01.png
```

This reproduces postprocessing, not a new model generation. The alpha/placement are replayed from the selected composition receipt; no archived rejected input is used. A sequence-wide finishing policy should follow a successful visual trial, with the same identity/geometry/contact protections and separately recorded adoption hashes.
