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


## Temporary-directory preference

The owner requested `/scratch/project_465002727/jelealro/tmp` instead of `/tmp`.
Subsequent experiment wrappers set TMPDIR, TMP and TEMP to job-specific
subdirectories there, and put pip/runtime caches on scratch. The already-running
motion diagnostic was not restarted just to change its inherited environment.


The moving/stationary motion diagnostic completed in 11m59s (exit 0).
Both clips have 33 frames. At peak-motion frame 8, the acorn is visibly higher
with moving control; all-frame contact sheets show the repeated guide cycle.
Stationary control is nearly a hold. This establishes control response, not
yet superiority over baseline or lifelike nibbling. Source color/texture
reconstruction is imperfect and requires comparison, not assumed acceptance.

Matched baseline job `22907388` was submitted serially. It encountered HTTP
429 on optional cached-model HEAD checks, then advanced to component loading.
All 47 entries under the pinned snapshot are present, with no broken symlinks.
The useful loading job was left running; subsequent experiment wrappers force
HF_HUB_OFFLINE and TRANSFORMERS_OFFLINE so inference never stages weights or
retries network metadata. No production wrapper/environment was changed.


## Blender end-to-end result

Blender 4.5.0 rendered 33 aligned textured image-plane guide frames with Cycles
CPU in 7.0 s (50 s CPU step including startup, 157 MB peak RSS) inside the
otherwise-loading baseline allocation. First-frame RGB MAE against the fitted
input was 0.165/255. `finalize_blender.py` encoded the actual render as Canny
100/200 RGB control. Job `22907824` then generated a 33-frame Blender-conditioned
Wan clip successfully, about 9.5 minutes total; actual frame 8/24 outputs were
inspected. This proves headless CPU guide generation and model consumption;
it does not prove that a 3D animal rig or depth control improves the story.

## Baseline storage bottleneck and controlled cache test

The initial baseline `22907388` was cancelled before inference after 11m24s:
FP32 expert loading was too slow for the quick-test budget. Its completed CPU
Blender step remains valid even though the parent baseline job was cancelled.
Longer baseline `22907863` was queued on small-g as a fallback.

The initial CPU small preparation job `22907694` remained pending and was
cancelled. A **new cache-writer integrity/throughput diagnostic**, `22907910`,
ran serially on CPU debug with a 15-minute cap. It first measured four shards
and would have stopped if projected total conversion exceeded ten minutes.
It completed in **2m39s**, peak RSS 16,292,604 KiB. The converter took 135.3 s.
All **2,190 tensors in 24 expert shards** were bytewise verified against the
ordinary `torch.bfloat16` cast. Original weights were untouched; VAE and text
encoder retain their original files. The resulting extra expert cache is
57.16 GB, with source/output SHA-256s in `evidence/baseline_cache_22907910.json`.
This is normal baseline load precision, not an extra FP8 approximation.
Routine/bulk cache preparation belongs on small; the debug run was the bounded
first validation of a new experimental cache writer.

Matched baseline diagnostic `22908225` now calls the existing `wan.load` and
`wan.generate` with that verified local storage path in this process only.
Its 416×240, 33-frame, 28-step, seed-43 recipe matches the control tests' common
settings. The production wrapper, pinned origin revision and original cache
were not edited. Small-g fallback now depends on failure of this diagnostic,
so it cannot run alongside it or duplicate a successful result.

## Baseline render and preview recovery

Job `22908225` loaded the verified cache successfully (136.3 s including the
explicit VAE/model loading; pipeline-component progress alone was ~53 s).
Generation took 293.0 s. It saved the complete MP4, then this experiment's
preview writer failed because Diffusers 0.39 returned NumPy frames instead of
PIL images. The existing production MP4 export supports those arrays; this
was an experimental preview bug. The raw job/receipt remains failed, unchanged.

`recover_previews.py` decoded the existing MP4 on CPU and verified all **33
frames, 416×240, 16 FPS**, then created previews and a separate recovery receipt.
No inference was repeated and no review/production approval was manufactured.
The recovery binds the raw failed receipt SHA and MP4 SHA; both receipts are
tracked under `evidence/`. Future experimental previews normalize NumPy/PIL
frames explicitly. Small-g fallback `22907863` was cancelled to avoid an
unnecessary rerender.

The first baseline samples show substantially more spontaneous feeding motion
than the guide-constrained clips, while the controlled versions stay nearer
the original outline. This is a practical tradeoff, not a universal quality
ranking: our deliberately simple guide prescribes small image-plane motion,
not a fully animated mouth/animal rig. Full frame-sequence inspection follows.

`production/render_story_inventory.py` confirms the bulk path uses `--fast`.
Therefore serial diagnostic `22908379` also tests that exact existing Lightning
flag (4 steps, guidance 1/1, already-cached pinned LoRAs), on the same source,
resolution, frame count and seed policy. It uses the verified storage cache;
no Lightning adapter is assumed compatible with the separate Control backend.

## Completion

Lightning `22908379` completed successfully, 33 frames, 400 active adapter
layers in each expert. Its Python elapsed time was 466.3 s; exact settings,
LoRA hashes and model/cache provenance are in the tracked receipt. All GPU
and CPU jobs are finished; unnecessary small-g fallback was cancelled.

`build_review.py` produced `comparison_4way.mp4`; all four output hashes,
common source-image hash, prompt, frame count, dimensions and seed policy were
verified into `evidence/comparison_manifest.json`. Final decoded-frame contact
sheets cover every frame of each method. The results report records the
practical no-go for changing the default workflow, successful technical
control/Blender feasibility, and the optional verified cache improvement.
Eight input safeguards pass; Python compilation, shell syntax and diff checks
pass. Image/staging policies and production approvals remain unchanged.

## Sparse Blender-guide constraint probe

Owner requested further Blender testing while the longer Wan comparison queues.
The first submission attempt was not executed: the automatic approval-review
service hit a usage limit. On explicit resume, created `blender_sparse_probe.py`
and submitted job `22914567` to dev-g, one GCD, 7 cores, 128 GB RAM, 20-minute cap.
This is one short input-constraint diagnostic (33 frames, 416×240, 28 steps), not
routine production or a repeated seed sweep. Longer Wan job `22914092` remains
on small-g and was given an `afterany:22914567` dependency to keep GPU work
sequential. No new model/environment installation or download.

Hypothesis: full-frame Canny suppressed spontaneous acting by constraining inner
facial features and the entire background. Reuse the 33 saved **actual Blender
renders**, removing most background and inner-face edges with a coarse fixed
image-space ROI after Canny extraction. No mask-border edges are invented.
This is not exact segmentation; background within the coarse actor region may
remain. Source frame hashes, ROI, guide and script hashes are saved. Same start
image, prompt, negative, seed, settings and Control backend as original Blender
run; runner asserts their equality after inference. No new Blender motion or
articulated model is introduced, so the test diagnoses conditioning freedom,
not 3D animal rig quality. Native depth, occlusion, articulated gait/paw contact,
camera movement and endpoint anchoring remain untested.

Output root:
`work/stories/lion_and_mouse_v6/experiments/blender_fun_control/blender_sparse_probe_20261016/`
The script saves guide/mask previews, inference receipts, all-frame sheet and
`comparison_3way.mp4`: normal Lightning / full Blender Canny / sparse Blender
Canny. Results pending. Existing experiment safety suite: 8 tests pass; new
Python syntax, batch shell syntax and diff whitespace checks pass.

### Sparse-guide result

Render and comparison receipts are complete. All 33 frames exported at
416×240/16 FPS. Inference 331.2 s; runner total 569.9 s; peak allocated GPU
30,240,855,040 bytes; peak process RSS 72,391,440 KiB. The full/sparse
comparison asserts matching prompt, negative, source image SHA, seed, FPS,
frame count, geometry, steps, guidance, model and backend commit. Guide content
is the intended changed variable. Saved output and comparison hashes verified.

Agent inspected all 33 sparse frames, all original full-guide frames and all
normal Lightning frames through contact sheets, plus matched peak frame 8.
Sparse guide still shows restrained head/acorn bobs, with no clear return of
normal Wan's visible blinking and larger feeding action. No obvious benefit
justifying adoption emerged in this one short low-resolution pilot. This does
not establish anatomical correctness or exclude useful articulated/depth guides.
Owner playback judgment remains separate; no visual approval ledger was edited.

[Three-way review](../../work/stories/lion_and_mouse_v6/experiments/blender_fun_control/blender_sparse_probe_20261016/comparison_3way.mp4)
shows normal four-step Wan, original full-frame Blender Canny and sparse Canny.
Blender motion itself was reused, not rerendered or rigged. More promising
untried Blender work would require articulated proxy motion with useful limb,
contact or depth/occlusion information, not another image-plane mask variant.
This would be a separate experiment with its own guide-quality check; no such
job is submitted by this probe.

## Articulated 3D, contact and camera/depth expansion

Owner authorized all three untried areas after the sparse-guide result, while
asking whether another direction would be better. We retain the normal fast I2V
as default and test distinct constraints rather than build a finished character.
No production assets, staging policies, approvals or model defaults are changed.

### CPU geometry proof

- `22915081`: first true-3D proxy diagnostic on CPU debug, 15-minute hard cap.
  Primitive ellipsoids connected by analytic two-link limbs, explicit foot/paw
  targets, true camera-space depth emission, ground/rocks and orthographic camera.
  Generated three 49-frame sequences in ~27 seconds of renderer script time.
  Initial framing was visibly too small/narrow; no GPU inference used this guide.
- `22915125`: specific framing/proportion defect correction, same bounded CPU
  diagnostic. Completed exit 0 in 1m16 allocation time. Original attempt retained;
  corrected output root `articulated_20261016_v2`. Wider ears/body and closer framing.
- Actual start/mid reach, step phases and start/end camera frames inspected.
  Shape remains a rough front-facing mouse; original illustration is a different
  three-quarter pose. **This is not exact plate/camera/character calibration.**
  Guide gate permits isolated feasibility only, with explicit limitations.
- Both feet have zero world displacement in their authored stance interval.
  Paw-to-acorn center distance remains 0.150333 proxy units in all frames; hands
  track the object. This is analytic contact authoring, **not collision physics**.
  The procedural linked parts are not a skin-weighted Blender armature or finished
  Milo model. Two upright hind-foot steps, not a quadruped gait, suit this test.

### Six-clip video comparison queued

Job `22915166`, regular small-g, one GCD, 7 CPU cores, 128 GB host RAM, two-hour
hard cap. Dependency `afterany:22914092` keeps GPU work sequential after the
longer Wan/continuity experiment, which remains pending. No new model downloads.
Expected tens of minutes if resources behave like earlier short tests; two-hour
cap is a ceiling, not a benchmark or promised completion time.

Each row generates **normal Wan I2V + Lightning (4 steps, CFG 1/1)** and
**existing Fun Control (28 steps, CFG 6)**, same original start image fitted to
416×240, 49 frames at 16 FPS (3.0625 s), same row-specific prompt and seed policy43:

1. `reach`: acorn raised to mouth and lowered, paws attached; Canny 10/25 from
   actual depth renders to retain geometric outlines and moving limbs.
2. `walk`: two short steps to the right, alternating planted feet, acorn held;
   same Canny representation. Fixed generous image-space actor region excludes
   most background geometry; any background inside it can remain.
3. `camera`: seated mouse, short lateral camera arc/tracking move, foreground rock
   partly hides lower body, background rocks shift at different projected rates.
   Fixed-range inverse camera-Z, proxy near/far 5/12, nearer brighter. Renderer
   writes sRGB depth appearance; preprocessing applies inverse sRGB to recover
   linear normalized depth before uint8 RGB video. No per-frame normalization.
   This synthetic convention is exploratory, not calibrated monocular training
   depth. Generic Control supports depth; **explicit camera-pose model is a
   separate checkpoint and is not tested or downloaded here**.

The third test deliberately introduces a foreground object; it does not test
unchanged source-scene geometry. First-frame guide/illustration mismatch and
synthetic depth domain shift limit conclusions if Control fails. A guide failure
cannot establish that all articulated/depth workflows fail. Equal seeds across
backends do not imply identical CPU/HIP-generated noise.

Outputs under `articulated_comparison_20261016`: six MP4s, all-frame sheets,
first/quarter/mid/last PNGs, per-clip timings and peak HBM, hashed input/guide/source
frames and receipts. Final `comparison_6way.mp4` pairs normal/guided per action.
Runner rejects an uninspected or changed proxy receipt. Failed receipt is kept;
no automatic repeat. Existing 8 safety tests pass; script/batch syntax checked.

Assess guided vs normal for identity/ear/face stability, visible acorn-mouth
contact, paw attachment, foot sliding/lifting, action completion, correct relative
occlusion/parallax and camera trajectory. Extra motion alone is not improvement.
No visual review approvals or production eligibility can be inferred. Results
remain pending until jobs run and saved frames/playback can be reviewed.
