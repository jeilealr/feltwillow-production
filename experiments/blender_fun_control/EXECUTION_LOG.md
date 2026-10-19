# Feasibility execution — started 2026-10-16

**Preservation note, 19 October 2026:** Unavailable historical/local media links below are retained as code paths. Recover only exact historical bytes through the cleanup receipts/Git history or the verified local archive; these paths are not active generation authorities. Original dated results remain in source history.

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

Three-way review (`../../work/stories/lion_and_mouse_v6/experiments/blender_fun_control/blender_sparse_probe_20261016/comparison_3way.mp4`)
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

## Parallel experiment queue and short depth diagnostic

Owner explicitly requested a dev-g experiment without cancelling existing
small-g jobs, and several distinct additional small-g comparisons. Existing
`22914092` (continuity) and `22915166` (three-action six-way) remain unchanged.
A single short dev-g job runs alongside queued regular-partition experiments;
no second dev-g job, queue workaround, new weight set or environment is used.

Named recipe runner: `run_video_matrix.py`; regular batch entry point
`video_matrix.sbatch <recipe>`. New run roots are
`matrix_<recipe>_20261016`, never overwritten. All runs are isolated, explicitly
ineligible for production and inherit scratch `tmp` configuration.

| Job | Partition / cap | Recipe | New question |
|---|---|---|---|
| 22916689 | dev-g / 30 min | depth_diagnostic | Does a moving true-3D camera-depth guide change the result versus the same guide frozen at frame zero? |
| 22916690 | small-g / 2 h | endpoint | Does existing 4-step Lightning I2V honor an optional ending image while preserving plausible action and identity? |
| 22916691 | small-g / 2 h | seeds | Is the preferred 4-step behavior repeatable across seeds 44/45/46, compared with existing queued seed43? |
| 22916692 | small-g / 2 h | representation | Does an articulated reach work better with geometry edges or depth? Does moving depth differ from stationary depth? |

The dev-g job is a single bounded input-behavior diagnostic: two 33-frame
416×240 Control clips share one model load, 28 steps/CFG6, identical seed43,
source image, prompt and settings. It uniformly samples the full 49-frame proxy
camera path into 33 frames; stationary repeats the first depth frame 33 times.
This changes the action duration to 2.0625 s, explicitly not production timing.
The matched control ablation needs no separately loaded normal Wan model; the
normal comparison stays in the existing regular six-clip job. If the diagnostic
hits its cap, preserve partial receipts rather than auto-repeat.

Endpoint uses 81 frames at 416×240, four steps, CFG1/1, seed43. One start-only
clip and one start+end clip share all other settings. Existing frozen
`s01_p04_r02_candidate.png` changes pose and apparent size, so inspect for
morphing or unintended camera/scale changes. End-image role is **conditioning**
only in that case, evaluation-only otherwise. Target pixel MAE is diagnostic,
not independent evidence of video quality, anatomy or image approval.
Lightning endpoint behavior is genuinely untested; no success is assumed.

Seeds uses 81 frames at 832×480 and the original feeding prompt. Three new seeds
44/45/46, four steps/CFG1/1, unchanged source and model/cache. Queued continuity
job's `long_81` supplies the matching seed43 reference once complete; no duplicate
seed43 render. Assess action completion, identity/contact and camera drift,
not which seed merely looks most active. Four seeds are not a statistical study.

Representation uses 49 frames at 416×240: reach edges (Canny10/25), moving depth,
stationary depth, all same Fun Control/seed43/prompt/28 steps/CFG6. Fixed-range
near-bright camera-Z with inverse sRGB decoding; no per-frame normalization.
Same rough 3D reach geometry, not a new scene or rig. Edge input excludes most
background outside a fixed actor ROI while depth is full scene; this is a
comparison of the current guide recipes, not a pure modality ablation with
identical spatial support. Synthetic depth domain and proxy/image mismatch
remain confounders. The moving/stationary depth pair is the cleaner causal test.

All recipes save input originals/fitted hashes, guide source hashes and sample
indices, script snapshots, model/cache/adapter provenance, frame sheets, MP4
format checks, output hashes, timings and peak HBM. Review MP4s are labeled per
case. Camera diagnostic removes camera movement/zoom from its negative prompt;
other recipes retain the original fixed-camera negative. Existing eight safety
tests, Python and batch syntax pass. Five total small-g jobs now cover distinct
questions; avoid further expansion until results guide the next hypothesis.

## 2026-10-17 — queue and resource-sizing investigation

Owner requested more quick dev-g investigation and better scheduling requests,
explicitly **without stopping current small-g jobs**. Accounting at inspection:
all five experiment small-g jobs remain pending; completed `22916689` was dev-g,
14m17 elapsed, exit 0. Existing queue requests/dependencies were not changed.

### Completed depth diagnostic assessment

Receipt/hash checks pass for both clips and `comparison.mp4`. Actual recorded
load time 246.24 s; moving-depth inference 365.28 s; warm stationary inference
115.08 s; Python elapsed 780.30 s (13m00), allocation 14m17. Slurm step MaxRSS
72,407,664 KiB (~69.05 GiB); peak allocated HBM ~28.16 GiB. Original raw receipt
is preserved in `evidence/depth_diagnostic_22916689.json`.

All-frame sheets inspected for both cases. Moving depth introduces large rocks
and background/scene changes; frozen depth stays near a hold. This demonstrates
conditioning effect, **not better appearance, correct camera calibration or
successful foreground occlusion/contact**. Source scene changes are substantial.

A setup defect was found in the actual receipt: negative prompt still includes
`camera movement, zoom`. Earlier notes described its intended correction, but
this job actually executed the pre-correction function. The source file was
edited during startup, so its copied source snapshot reflects later text rather
than proving the live Python function matched it. The raw executed-parameter
receipt is authoritative. Do not rewrite that receipt or claim the intended
correction was applied. Current committed runner has the correction for future
jobs. Avoid editing source during startup/running jobs; this diagnostic is not
silently repeated to repair a historical claim.

### Queue evidence

- Pending jobs show `Priority`; articulated comparison additionally waits for
  its explicit dependency on continuity. Current `squeue --start` has no dates.
- About 1,550 jobs pending on priority were observed in small-g. This is a
  transient count, not an explanation of every scheduler decision.
- `sprio` shows priority composed of age, fairshare and partition factors;
  current continuity job priority 401 in the observed snapshot.
- Pending ReqTRES displays `gpu:a100=1` despite generic TresPerNode gpu:1 and
  MI250-only nodes. Completed successful dev-g jobs have the same ReqTRES but
  allocated MI250. Thus this field alone is not proof of a scheduling blocker.
  Explicit MI250 and generic GPU `sbatch --test-only` gave the same estimate.
- Read-only requests with 96 GiB at 15/30/60/120 min and 128 GiB at30 min all
  estimated around October28. These are hypothetical **new-job** estimates,
  volatile and different from existing aged-job predictions, not commitments.
  No real queue entries were created by --test-only despite assigned probe IDs.

`scheduler_probe.py` saves a reproducible queue/details/priority snapshot and
five sbatch --test-only comparisons to an isolated timestamped run folder.
It never submits a real allocation or mutates existing jobs. Snapshot run:
`scheduler_probe_20261017T073203Z/receipt.json` under the experiment work root.
Slurm backfill uses requested runtime and resources; accurate smaller requests
can fit more gaps but do not guarantee faster starts amid priority congestion.

### New bounded capacity diagnostic

Submitted `22928505`, dev-g, one explicit MI250 GCD, 7 CPU cores, **96 GiB host
RAM**, 25-minute cap. Script `profile_native.py`, batch `profile_native.sbatch`.
Test 81 frames at832×480, **only two denoising steps** through existing Wan2.2
I2V+Lightning and verified bf16 storage cache. This differs from pending quality
renders; it diagnoses full-size memory/phase timing, not four-step quality.
No new weights or environments, no seed sweep or production rendering.

Receipts checkpoint imports/loading/each denoising step/decoding with GPU sync,
process RSS, peak HBM, exact script/model/LoRA/cache/input hashes. No MP4 is
exported from under-stepped output. Preserve failure/checkpoints if it hits cap.
Do not linearly double its runtime to claim four-step production speed: transfers,
text encoding and decoding are fixed costs, and expert step distribution differs.
Results pending at submission. Previous measured short-run host peaks ~69–71 GiB
justify testing96 GiB, but do not prove every larger workload fits it.

Keep one-GCD/seven-core requests and model reuse until profiling justifies other
changes. Avoid time-min (could truncate a non-checkpointable render), extra GPUs
without parallel inference, or exclusive full nodes as queue workarounds.
No current queued job is cancelled, requeued, shortened or memory-reduced.

### Capacity diagnostic completed

`22928505` completed exit0 in **13m31** allocation time (Python789.81s), all81
832×480 frames decoded successfully with96 GiB host request. Actual load253.01s;
conditioning/first callback268.86s; second callback100.84s; decoding after final
callback110.18s. Inference+decode479.88s. First callback interval includes prompt
and image encoding/transfers; it is **not isolated denoising kernel time**.

Python peak RSS74,538,968KiB (~71.09GiB); Slurm step MaxRSS73,994,016KiB
(~70.57GiB), differing sampling/process accounting. Peak allocated HBM
34,008,858,112B (~31.67GiB), peak reserved37,169,922,048B (~34.62GiB).
Receipt retained in `evidence/native_profile_22928505.json`.

This validates96 GiB for this two-step480p81-frame baseline capacity test. A
future equivalent request can use `--mem=96G`; higher resolution, other backends,
endpoint conditioning and different offload settings still require their own
headroom check. Do not claim a four-step quality result or double13m31 as a
measured runtime. Keep one MI250/seven cores; native four-step/batch timings are
still pending in regular queue. Short-run evidence supports model reuse, not
extra unused GPUs or full-node allocation to chase shorter waits.

Final queue inspection: current five small-g jobs remain unchanged/pending.
No new small-g copies were submitted; profiling was one distinct quick dev-g
capacity test. No renderer/media output was promoted to production. Python,
batch syntax and existing8 safety checks pass. Branch `feature/video-control`.

## 2026-10-17 — authorized queue resize and split migration

Owner explicitly authorized modifying/splitting the pending small-g batches to
request smaller scheduling slots, while retaining dev-g for genuine quick tests.
This supersedes the earlier instruction to leave those requests unchanged.
The 1.5/2-hour numbers were requested ceilings, not measured runtimes.

### New schedule (same experimental content)

All GPU requests now use **one MI250 GCD, seven CPU cores,96 GiB host RAM**.
96 GiB passed the larger81-frame480p two-step baseline capacity test; prior short
Control runs peaked around69 GiB. Control49-frame and native four-step timings
remain estimates, so the new30–45 min caps retain headroom. A timeout/failure
must be recorded and inspected; no automatic resubmission or quality claim.

| Experiment | Current job(s) | Ceiling | Change |
|---|---|---|---|
| Endpoint start-only vs start/end |22916690|40 min|Same ID retained; previously120 min/128 GiB|
| Reach edges/depth/frozen-depth |22916692|45 min|Same ID retained; previously120 min/128 GiB|
| Continuity first clip |22928746|30 min|First stage only; unchanged prompt/seed/frames/resolution|
| Continuity two follow-ups |22928747|45 min|afterok22928746; validates first clip and frozen input hashes|
| Seed44 |22928748|30 min|Single existing recipe case, separate output root|
| Seed45 |22928749|30 min|Same|
| Seed46 |22928750|30 min|Same|
| Articulated three normal-Wan actions |22928751|35 min|One backend load shared across three short clips|
| Articulated three Control actions |22928752|40 min|One backend load shared across three short clips|
| Review reconstruction (CPU small) |22928753|15 min,8 GiB|afterok all seven replacements; no GPU inference|

Endpoint and representation stay grouped to reuse expensive model loads. Splitting
seeds and continuity adds three cold model loads overall; this is a deliberate
tradeoff for shorter scheduling windows, not a throughput optimization. New jobs
start with new submission/age history; resizing the other two retains their IDs.
Smaller resource/time requests increase potential backfill fit but do not promise
an earlier start. New GPU requested ceilings total325 min vs previous570 min;
this is **not a measured43% reduction in compute time**.

### Safe transition and verification

Only the three pending batches to be replaced were temporarily held. The first
resize attempt rejected `MinMemoryNode=96G`; rollback released the held jobs
and submitted no replacements. Correct numeric MiB value `98304` was accepted.
Endpoint then successfully resized in place. Second migration submitted all
replacements held, verified them, built dependencies, then retired superseded
pending IDs22914092/22915166/22916691 and released the replacements. All three
retired jobs show cancelled with **zero compute elapsed**. No running job or
completed artifact was cancelled/overwritten. Endpoint/representation retain
original submission IDs. Evidence journal:
`evidence/queue_split_migration_20261017.json`; failed first-attempt journal stays
in the isolated work root as well.

Verified via live `scontrol`: all nine GPU requests have intended partition,
96 GiB memory and30–45 min limit; no jobs remain user-held. Continuity follow-ups
have afterok first-stage dependency. The previous artificial dependency tying
all articulated work to continuity is absent. CPU review depends on all seven
replacements. Refreshed read-only scheduler audit still estimates hypothetical
new jobs aroundOctober28; there is no immediate demonstrated queue-time gain.
Snapshot: `scheduler_probe_20261017T075713Z/receipt.json` in experiment work root.

### Review artifacts and source boundaries

- Continuity retains `i2v_followup_20261016/` and final
  `continuity_comparison.mp4`, with `receipt_first.json` and
  `receipt_continuations.json`, separate executed stage snapshots and per-clip
  receipts. Continuation validates the exact first-frame-source/final PNG
  provenance and first MP4 hash before reading it. First clip not regenerated.
- Seed folders: `matrix_seeds_seed_{44,45,46}_split_20261017/`, each own receipt,
  clip/contact sheet. Matching seed43 remains continuity `long_81`.
- Articulated folders: `articulated_normal_split_20261017/` and
  `articulated_control_split_20261017/`; same underlying guides and settings as
  original six-way plan. Neither stage loads the unused backend.
- CPU `review_split.py` verifies completed per-clip receipts, video hashes, FPS
  and geometry before rebuilding `split_reviews_20261017/articulated_6way.mp4`
  and `seeds_4way.mp4`. Continuity reconstructs its own paired sequences in the
  follow-up job. Endpoint/representation retain their own labeled comparisons.
- Default unsplit runner modes remain available for reproducibility. The new
  split batch wrapper accepts only the three named experiment drivers. Existing
  production code/image-generation/staging/approval/export rules are untouched.

Validation: all8 prior experiment safety tests pass, all experimental Python
compiles, new batch shell syntax and diff whitespace pass, stage/backend/case
CLI selectors checked, and actual scheduled request/dependency checks pass.
No new dev-g job or duplicate rendering batch submitted by this migration.
