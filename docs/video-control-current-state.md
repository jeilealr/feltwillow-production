# Video control: current state

Initial inspection: 2026-10-16 at `6fae81c` (Agent B). Subsequent
[allocated test results](../experiments/blender_fun_control/RESULTS_2026-10-16.md)
prove the isolated control/Blender paths at pilot scale; production is unchanged. Start with the
[experiment policy](video-control-experiment-policy.md),
[LUMI validation](../experiments/blender_fun_control/LUMI_VALIDATION.md), and
[pilot selection](../experiments/blender_fun_control/PILOT_SELECTION.md).

## Established video path

`production/shot.py` reads a legacy `stories/<slug>/story.yaml`, resolves a
first keyframe and optional `end_keyframe`, composition recipe or continuation,
assembles prompts/LoRAs, and calls `feltwillow.wan.load('i2v')` then
`generate(..., image=..., last_image=...)`. Its defaults are 1280×720,
40 steps, guidance (3.5, 3.5). `--fast` selects the separately pinned Lightning
4-step recipe. `--dry-run` checks inputs; `--audit-existing` checks receipts.
An MP4 and JSON sidecar bind inputs/hashes, prompt, seed, model/LoRA revisions,
settings and time. Existing outputs must pass the receipt audit before reuse.

`feltwillow/wan.py` uses `diffusers.WanImageToVideoPipeline`, pinned to
`Wan-AI/Wan2.2-I2V-A14B-Diffusers@596658fd9ca6b7b71d5057529bbf319ecbc61d74`.
Weights use bf16, VAE fp32, and module CPU offload. Native clips are 81 frames
at 16 FPS (5.0625 s encoded duration; first-to-last sample interval is 5 s).
Frame count follows 4k+1. Source comments estimate 80–100 GB host RAM per
process; this is baseline experience, not a Fun Control measurement.

`wan.fit()` center-crops each input to target aspect and resizes it. Any
experimental guide, masks, depth, and contact coordinates need the identical
spatial transform. An independent crop is a conditioning alignment bug.
There is **no control video, depth, trajectory, pose, or camera-control argument**
in the current wrapper. Changing weights alone cannot supply that interface.

`feltwillow/paths.py` resolves `FELTWILLOW_WORK`, otherwise `<checkout>/work`.
`lumi/site.sh` selects the shared ROCm container, generation venv, scratch cache
and logs. A new worktree has its own default work root; it does not inherit
ignored media from another checkout.

## V6 remains gated

V6 has no renderable legacy `story.yaml`. Its authoritative
[RUNTIME_CONTRACT.md](../stories/lion_and_mouse_v6/RUNTIME_CONTRACT.md) requires
current hash-bound visual evidence, boundary validation, audio provenance and
reviewed timing. Export creates an input receipt, `runtime_plan.json`; a tested
renderer translation is still required. `production/shot.py` is not a v6
renderer just because it accepts a story slug.

The read-only preflight in this separate worktree exited 1 with **1572 blockers**
and **81 historical provenance warnings**; see the LUMI note for context.
Owner selection of 96 images is not completion of structured technical review.
No gates or review records were changed. Isolated candidate experiments confer
no production readiness and cannot be used to manufacture a runtime plan.

Boundary metadata contains camera/location cuts and same-view candidates.
Some same-view labels disagree with planned views, for example
`s15_p03 → s15x_p04` and `s16_p02 → s16_p03`. Treat these as pilot exclusions
pending reconciliation by the responsible owner, not permission to interpolate.

## Isolated extension

Current work adds documentation and a read-only input audit under
`experiments/blender_fun_control/`. It imports no production render code and
cannot generate, submit jobs, approve images or export runtime plans.
Future guide/backend/orchestrator modules stay there until backend feasibility
and an owner-reviewed benefit are demonstrated. No changes to `wan.py`,
`shot.py`, staging, prompts, source images, or runtime/export policy are needed
for this phase.
