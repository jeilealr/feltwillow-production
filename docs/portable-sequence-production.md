# Mac authoring, portable execution, reviewed results

The Mac is the development and review environment. LUMI remains a possible GPU execution host; the worker uses ordinary Python and Slurm, with no Codex process, Bubblewrap namespace, agent login or interactive tool host on the execution node. Linux/AMD compatibility, cached model/LoRA files, source/config pins, free space/quota and scheduler resources must still be verified on that host before an authorized trial. CPU fixtures establish contracts only.

Wan, bounded 2D local treatments and Blender are separate methods. Packaging does not convert one into another or claim full-frame continuity. No new model/backend has been added. The Slurm script is a launch adapter for an approved existing environment, not a provisioning or automatic submission script.

## A. Local authoring and source gates

`audio_visual_plan.json` owns visual units, chronology, cast and mouth rules. Exact selected media, technical source/edge/projection/paw evidence and actual sample timing remain separate inputs. `sequence_readiness.py` gates realization, stills, timing and execution; a technically ready packet remains unauthorized. Camera-locked groups require exact-hash native/fitted 2D root/body/background/canvas/crop evidence, and portraits need reviewed crop/closed-mouth/toothless/body-exclusion contracts. These observations are reviewer supplied; the validator cannot infer correct anatomy or certify newly generated video.

Run CPU checks in the verified existing environment; never install or replace an environment implicitly. The current Mac interpreter is `/Users/lealroja/miniconda3/envs/feltwillow/bin/python`.

```sh
python production/audio_visual_plan.py --story lion_and_mouse_v7 validate
python production/check_sequence_requirements.py
python production/sequence_package.py --help
```

`sequence_editor.py` exposes Python functions, not a command parser: import `plan_edit`, `edit_review_digest` and `bind_takes`. Use the API contract below for editor integration.

## B. Freeze render recipes and intended editorial allocations

`sequence_export.py` retains the legacy diagnostic path and supports typed production edit intervals. `recipe.pieces` maps stable piece IDs to permitted frame/step/guidance overrides. Wan pieces remain 5–81 frames, `4k+1`,16fps; static/local CPU pieces may have arbitrary positive integer frame counts. Every meaningful distinct pair is preserved; adjacent aliases do not add calls.

For production, `timing.intervals` is a contiguous half-open PCM timeline containing `kind: render_piece` (with `piece_id`, or matching interval ID) and `kind: static_hold` (with exact `use_id`). A hold requires `hold_review` with reviewer, pass status, source/fit hashes, `settled: true`, `resting_mouth: true`. It cannot freeze an unreviewed fall or open speech mouth. `boundary` is `cut` or `continuous`.

`timing.render_allocations[piece_id]` records effective frames/fps, `reviewed: true`, and optional `source_mapping: {start_frame, frame_count}`. The intended mapping is bound by `timing.editorial_review: {status: reviewed, reviewer, allocation_sha256}`. Compute the hash with `edit_review_digest(packet, pieces)`, whose piece records contain actual `id, frames, fps, method, start, end`. Do not fabricate a review to compile blocked story art. `plan_edit` rejects unknown/duplicate/reordered/dropped pieces or stale allocations. Frozen runtime, commands and receipts carry this edit identity.

An intended trim/retime before generating frames is not returned-motion approval. After exact returned takes are reviewed and selected, `bind_takes(editorial, selection, reviews, root, audio)` invokes the sample editor against actual decoded FPS/count and exact source bytes. It requires actual trim, retime and join evidence when needed. Cuts never interpolate incompatible views.

`sequence_timeline.py` uses one cumulative rational frame-cell quantization. Each retime/trim review binds the source SHA, source-window digest and **target** digest (start/end samples, sample rate, fps, first/last frame cells). A join additionally binds both source windows and both target intervals with `join_digest(left,right,rate,fps)`; changing a trim cannot inherit old join review. Automatic frame deletion, crossfades or time stretching are not implicit. `render_preview` only produces a review preview; no final-film authorization is inferred.

## C. Prepare and verify a portable package

Use the real CLI help for argument shapes:

```sh
python production/sequence_package.py build --help
python production/sequence_package.py verify --help
python production/sequence_package.py worker --help
python production/sequence_package.py collect --help
python production/sequence_package.py verify-results --help
python production/sequence_package.py take-proposals --help
```

Build takes a **previously frozen eligible packet directory** and a new destination. It copies exact selected/native inputs, local-effect targets/masks, versioned Python source and a path-neutral runtime template. It does not copy model weights, credentials, historical videos, audio synthesis tools or mutable budgets. The manifest records every file hash, original runtime/packet identity, one seed/operation, method/count and environment requirements. It rejects stale code/assets, attempted operations, duplicate identities and invocation-count mismatch.

The package digest must be recorded outside the transferred package. Treat the manifest and payload as untrusted until verification against that trusted digest. Do not execute the package's own copy of the verifier first. Use `production/sequence_package.py` from a trusted versioned checkout. Verify rejects missing/extra payload modules and symlinks; host materialization rejects runtime/output path escapes. Child Python disables bytecode writes into the frozen payload.

`worker` without `--execute` is CPU-only preflight and requires `--package-sha256` from the trusted record before any packaged code is run. Materialization creates a new local absolute runtime and packet marker; it retains the original package/source-runtime identity. Model source/config paths are host evidence: refresh and refreeze on the execution host if they differ. Do not edit a package manifest to hide stale capability evidence.

## D. Future authorized GPU execution

Execution additionally needs external `--authorization` and a durable external `--journal`. An authorization JSON has `scope: execution_authorization`, `decision: authorized`, `reviewer: project_owner`, exact `package_sha256`, an exact `operation_ids` list and `maximum_retries: 0`. This format stores an actual owner decision; a generated proposal with those words is not owner authority.

The trusted worker verifies inputs, performs dry preflight, then atomically claims one exact original runtime/operation in the external journal before launching the renderer. Failed/interrupted/unknown attempts keep their claim. Copying a package or losing an output is not permission to retry; retain the same journal across restarts and reconcile scheduler request/receipt/output identities. A fresh journal must not be used to bypass an existing attempt. Slurm auto-requeue is disabled in the adapter.

`lumi/sequence_job.sbatch` uses `FELTWILLOW_REPO` (trusted checkout) and `FELTWILLOW_PYTHON` (existing verified interpreter/container wrapper). It accepts package, one operation, journal and authorization paths. It supplies no account, partition, GPU count, walltime or cost estimate; those are part of a concrete separately approved job request. No command here submits a job. Ordinary Slurm/Python execution does not require Linux user namespaces for Codex.

Frozen Wan runs load cached model and Lightning files with `local_files_only=True`; the worker sets Hugging Face/Transformers offline mode. Missing weights fail instead of downloading. This does not prove cached weight completeness, AMD compatibility or actual endpoint behavior; those remain future host/probe checks. Loader semantics follow the [Diffusers pipeline reference](https://huggingface.co/docs/diffusers/api/pipelines/overview).

## E. Retrieve results without moving approvals

`collect` verifies actual encoded outputs/frames/fps/size, operation/seed/runtime/input identity and native boundary hashes, copies clips and **unchanged original receipts**, and records a separate boundary-path transport map. It refuses partial/missing results instead of retrying. Store its returned results digest independently over the trusted execution-host connection.

After ordinary file transfer, `verify-results` requires both independently recorded package and results digests, checks schema/nonempty operation inventory, every file hash, full video decode and relocated native boundaries. A self-signed empty manifest is rejected. Hashes prove integrity only; full-motion/joins/teeth/paws/cast/dialogue remain pending.

`take-proposals` produces `feltwillow.sequence-takes.v1` with **pending** owner and whole-motion decisions and the separate relocated boundary map. It grants no selections. After actual exact-byte full-motion/join review and owner selection, `sequence_take.selected_source` verifies those transported references for the V7 mouth/editor consumers. New oral outputs still require post-sync review and final take selection. Final film assembly remains separately authorized.

## Current verification and limits

Mac evidence: `stories/lion_and_mouse_v7/review/mac_engineering_r006/`. CPU synthetic fixtures prove relocated worker/encoder/result/take roundtrip, no model loading for local modes, no silent downloads, durable no-retry claims, mapping invalidation and speaker/mouth boundaries. They do not test Linux execution, Slurm, ROCm, diffusion motion or the actual paw/bite repairs. Known S02/S03/S05/S06/S08 art dependencies, unreviewed phrase markers and unfinished S09–S16 visual authoring remain explicit.
