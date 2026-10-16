# Feasibility execution — started 2026-10-16

The owner explicitly authorized backend, proxy-guide and conditional Blender
tests, including downloads, dev-g diagnostics and small-g comparisons, after
the initial planning phase. This supersedes the earlier HOLD for authorized
experiments. Production approval/export remains out of scope.

## Frozen inputs and environment

- Branch/worktree: `feature/video-control`, `feltwillow-video-control`.
- Model: `alibaba-pai/Wan2.2-Fun-A14B-Control` revision
  `297be6d520f54908e124be0298e2317ee50ffdf4`; model API inventory totals
  69,049,496,959 bytes, staged once in scratch HF cache.
- Backend: VideoX-Fun commit `6183d41df8fbeb44f24b6c617efb8ef0ab690052`
  (Wan2.2-era snapshot). Current upstream imports many unrelated newer models;
  this narrower version matches the existing torch/diffusers generation stack.
- Separate environment: `/scratch/project_465002727/jelealro/video_control_env/venv`.
  The existing generation environment is a read-only dependency source. Added
  omegaconf 2.3.0, decord 0.6.0, torchsde 0.2.6, librosa 0.11.0 and dependencies
  only to the isolated environment. Full freeze is under the run tree.
- Attention: standard PyTorch SDPA, bf16, CPU model offload, no FP8, no LoRA,
  no compilation, no TeaCache. No changes to the production environment/code.
- Story pilot: P1 `s01x_p03 → s01_p04`; bytes frozen in `story_inputs/`.
  Current start image was inspected: one grounded Milo holding an acorn at the
  stream. End image is held out for evaluation, not used as control input.
- Run root: `<worktree>/work/stories/lion_and_mouse_v6/experiments/
  blender_fun_control/feasibility_20261016/`.

## Initial diagnostic

Job `22905341`, dev-g, one GCD, 7 CPU cores, 128 GB host RAM, 30-minute cap.
Question: can this pipeline load and execute control-conditioned denoising and
VAE decoding on MI250X? Official publisher sample (`asset/8.png`, `asset/pose.mp4`),
9 frames at 256×256, 2 steps. This tiny output is strictly a compatibility test,
not evidence of production quality.

The allocated bf16 SDPA kernel check passed on AMD Instinct MI250X with
68,702,699,520 HBM bytes visible. Further results are recorded below as tests
finish. Never infer success from job submission or package import alone.

## Scheduling observation

At initial submission, `sbatch --test-only` estimated small-g availability on
October 25 even for 45-minute requests. Standard-g estimates were earlier but
allocate/bill a full node. No full-node workaround was submitted. Keep long
comparisons on appropriate partitions and distinguish quick diagnostics from
routine rendering. Actual queued-job estimates may change.

## Backend compatibility result

Diagnostic `22905341` completed, exit 0, elapsed 10m14s. Nine frames decoded
and exported successfully; peak allocated HBM 29,667,705,344 bytes, peak process
RSS 72,168,568 KiB. Python-recorded model load 258.7 s and inference 260.4 s.
The tiny 2-step final frame was visually inspected and is distorted; **this is
execution compatibility evidence only**, not a successful quality/control score.
The exact receipt is tracked under `evidence/diagnostic_22905341.json`.

## Short motion diagnostic

Job `22906567` uses one dev-g GCD, 128 GB RAM and a hard 30-minute cap, after
the first diagnostic finished. Question: does a moving edge guide change the
intended head/acorn movement versus an otherwise identical stationary guide?
It is a one-off 416×240, 33-frame, 28-step development comparison, not a native
81-frame production render or a seed sweep. Actual input is identically fitted
for all models before conditioning; no independent Control resize/crop.
Two outputs reuse one loaded control model. The matching existing-I2V diagnostic
will run serially after this job, with the same fitted input, prompt, dimensions,
33 frames, 28 steps and seed policy. These short clips cannot establish 720p
production quality; default I2V normally uses 40 steps (or its separate fast path).

Blender 4.5.0's official 373 MB bpy wheel was staged in a separate Python 3.11
scratch environment for the conditional CPU/headless check. No Blender rendering
has run at this point, and no animal rig or GPU graphics path is assumed.
