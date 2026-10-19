# Experimental artifact contract — proposal v0

This is a proposed experimental schema, not a production runtime schema or a
validated Fun Control API. The implemented audit emits a smaller discovery
record. Implement a strict manifest/receipt validator before any future renderer.

## Run tree

```text
$FELTWILLOW_WORK/stories/<story>/experiments/blender_fun_control/<run_id>/
  input_manifest.json
  start.png                         # frozen copy of selected bytes
  end.png                           # optional; explicit conditioning/evaluation role
  motion_spec.json
  guide_frames/000000.png ...        # exactly N frames in index order
  guide_edges/                      # or guide_depth, actual preprocessing output
  control_video.mp4                 # optional; backend-specific encoding
  blender_scene.blend                # optional, only if used
  baseline_i2v.mp4
  baseline_i2v.json
  controlled.mp4
  controlled.json
  control_ablation.mp4              # same backend, changed control only
  control_ablation.json
  compare.md
```

Create the run directory exclusively and refuse an existing ID. Freeze inputs
before processing, compare copied hashes to the selected source, and record
all transformations. Successful sidecars are written atomically after output
hashes exist. A failed run writes a distinct failure receipt with error, stage,
partial artifacts and consumed time; it must never look like a completed render.
An unsuccessful baseline comparison may still preserve its completed sidecar.

## Required manifest fields

| Field/group | Required semantics |
|---|---|
| `schema` | `feltwillow.video-control-experiment.v0-proposal` |
| `run_id`, `story`, `pilot_id` | Unique run, real story and selection ID; no production piece ID inferred |
| `approval`, `production_eligible` | Exactly `isolated_experiment_not_for_production`, `false` |
| `repository` | Commit, branch, dirty status and patch SHA-256 if dirty; include script hashes |
| `sources` | Repo-relative start/end/plate paths, keyframe IDs and actual SHA-256s; hashes of staging, boundary, keyframe plan, owner selection, visual review and runtime contract; actual approval status as observed |
| `end_image_role` | `absent`, `evaluation_only`, or `conditioning_verified`; last requires capability test receipt |
| `image_roles` | Distinguish fixed start from appearance reference; include backend capability evidence |
| `geometry` | Source canvas, plate crop x/y/w/h, registered view, actors/contact/depth and target dimensions; source→crop→resize matrix for every modality |
| `timing` | Integer frames/FPS; first sample t=0, frame i at i/FPS; N/FPS encoded duration; source and resampling timestamps; experimental timing flag |
| `control` | Representation, ordered frame paths/hashes, channel order, bit depth, range/normalization, depth orientation if used; preprocessing package/revision/script hash and all parameters; video codec/pixel format/FPS if encoded |
| `motion` | Motion-spec path/hash, actor ID, endpoint states, interpolation, camera behavior; no silently invented staging positions |
| `backend` | Exact model repo/revision and file hashes, framework commit, pipeline/config names, precision, attention implementation, offload mode, scheduler, steps, guidance, seeds/generator, LoRA files/revisions/hashes/expert mapping or explicit empty list |
| `environment` | Container path and verified digest, environment lock hash, Python/PyTorch/ROCm/diffusers/backend/Blender versions; null with reason if absent |
| `allocation` | SLURM job ID, partition, account, nodes, tasks, GCDs, cores, host RAM request, walltime cap, purpose/hypothesis; null for local read-only discovery |

Keep external source paths rooted in explicit `repo`/`work` namespaces and run
artifacts relative to the run directory. Resolve symlinks and reject escapes
or aliases into canonical output directories. Validate actual source hashes,
not just strings of 64 hex characters. An example placeholder is never valid
input for submission. Unknown required capability or missing evidence blocks
rendering rather than falling back silently.

Each `baseline_i2v.json`, `controlled.json`, and ablation receipt additionally
requires: schema `feltwillow.video-control-result.v0-proposal`, manifest SHA-256,
backend kind, run approval constants, status (`complete` or `failed`), start/end
UTC, load/encode/denoise/decode/total seconds, measured peak host RSS and HBM
(or explicit unavailable reason), exit code/errors, and output relative paths,
SHA-256s, decoded frame count/dimensions/FPS. Preserve baseline model revision
and actual settings even when different from Control. A model comparison and a
control ablation are separate evidence.

## Motion spec and geometry

Use schema `feltwillow.proxy-motion.v0-proposal`, with source-plan hashes,
frames/FPS, camera fixed/moving designation, source plate pixel dimensions,
registered crop and per-actor source contacts/depth at each specified key sample.
Record interpolation and guide-generator version/seed. Copy the current staging
formula or reference its hashed source; do not create a new physical-scale rule.

For a crop `[cx,cy,cw,ch]`, convert plate normalized contact `(x,y)` to
`((x-cx)/cw, (y-cy)/ch)`, then apply target resizing in pixels. That is an
image-space projection, not a calibrated Blender ground plane. Off-screen
contacts can be legitimate in portraits; do not clamp them and shift actors.
Record pose-box geometry separately from standing-equivalent body height.
For fixed-camera P1 the existing contacts and depth are unchanged. Depth values
must not be treated as metric distance, depth-map intensity or camera focal length.

Before GPU allocation, verify: supported backend control type; decoded dimensions,
frame count and FPS; exact image/guide transform agreement; source and processing
hashes; registered same-view/hold geometry; no cut crossing; end-image capability;
resource and partition purpose; unique output directory. Before production,
independently require the existing runtime gate. Neither this proposed contract
nor the local audit can substitute for it.
