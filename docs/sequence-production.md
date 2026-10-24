# Ordered v7 sequences

The optional `audio_visual_plan.json.production_sequences` section is authored. Planned image slots retain their null-media lifecycle. `production/sequence_plan.py` resolves exact scoped scene selections and explicit aliases separately; `derived/sequence_realization_index.json` is generated, never another story authority. Current engineering/media status is in `stories/lion_and_mouse_v7/review/sequence_readiness_r001/`.

A sequence has `id`, ordered `uses` and exactly one edge per adjacency. A use has a unique semantic `id` and an existing `image_id`, an explicitly selected `source: {path, sha256}`, or `alias_of` an earlier use/existing image. A hold includes `hold: true` and `hold_reason`. Edges use `from`, `to`, `kind: motion|hold|cut`, and complete per-piece `prompt`. A hold cannot claim a new visible action. Cast changes require cuts in this supported route. Existing event/custody authority survives cuts. Sequence-level `blockers` prevent technical readiness.

Resolution distinguishes selected exact/alias/hold, pending selection, missing distinct state, incompatible edge, unavailable bytes and ambiguous authority. Conflicting selections fail; revision filenames never pick a winner. Later S06/S07 acceptance ledgers and exact embedded S08 scene approvals have their own scopes. Performance-only selection never grants scene selection. Shared S02 standing and S05 L006 pixels do not require duplicate PNGs.

## CPU commands

Run from the repository root using `/Users/lealroja/miniconda3/envs/feltwillow/bin/python` on the owner's Mac. Other hosts must select their documented interpreter deliberately.

```sh
/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/audio_visual_plan.py --story lion_and_mouse_v7 validate
/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/sequence_plan.py --story lion_and_mouse_v7 --sequence s03_fork
/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/sequence_plan.py --story lion_and_mouse_v7 --audio
/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/audio_visual_plan.py --story lion_and_mouse_v7 readiness --sequence s03_fork --stage realization
```

The last command currently reports blocked media, not a render request. `derive` writes generated indexes and must not be described as read-only. All 161 audio lines exist; later visual authoring remains pending. Audio offsets/PCM comparisons do not identify phrase boundaries.

`sequence_review.py PACKET --out DIRECTORY` builds a native/fitted HTML board. `sequence_readiness.py PACKET --stage realization|still|timing|execution --mode diagnostic|production` reports scoped gates and exits nonzero when blocked. `audio_visual_plan.py readiness --sequence ID --packet PACKET` accepts the same evidence packet. Missing future unrelated media does not block this scope. Readiness grants no resource authorization.

## Evidence contract

Resolved packets carry source file hashes, source selection records, native mode/size, crop box, RGB conversion/resize policy and a versioned fitted-pixel digest (`feltwillow.rgb.v1`, RGB dimensions, row-major bytes). Transparent scene inputs fail. `dependency_sha256` covers normalized scope inputs/order/fit; changing these invalidates technical evidence. Source plan provenance is recorded separately.

`technical_evidence.uses[use_id]` needs a reviewer, `status: pass`, exact `source_sha256` and `fit_sha256`. `technical_evidence.edges["from->to"]` needs a reviewer, `status: pass`, ordered `source_sha256s` and `edge_sha256`. These records require actual observation. Keep detailed anatomy, contact, support, palette, protected-pixel, projection and integration findings alongside the record. An identical-raster motion edge fails. `applied_performance_evidence` validates an optional exact-scene acting record with expression-source hashes and native reviewed 2D landmarks; planned `not_applied`/`camera_unknown` records are not cosmetically changed. Physical camera calibration is never inferred.

Timing needs `status: reviewed`, reviewer, positive integer `sample_rate`, matching `dependency_sha256`, mode, complete contiguous integer `intervals` from zero and `total_samples`. Production also requires `pcm_verified: true` and a reviewed `render_allocations` entry per render piece. Those allocations must explicitly declare frames/fps; unsupported retiming is rejected. Diagnostic timing is never promoted to narration alignment.

Execution needs inspected installed endpoint capability: source/config evidence, actual pipeline class, source hash and `expand_timesteps: false`. The Mac has no Diffusers installation; its CPU fixtures are not LUMI capability evidence. The read-only LUMI inspection is recorded in `LUMI_CAPABILITY_SOURCE.json` and `LUMI_CAPABILITY.json`: installed Diffusers 0.39.0 source supports last-image conditioning; the cached pinned model inherits `expand_timesteps=False`. No weights were loaded. Reverify these frozen source/config hashes on the execution host before loading. Actual endpoint adherence requires rendered review.

## Frozen execution

`sequence_export.py PACKET --out NEW_DIRECTORY --run-id ID --recipe RECIPE_JSON` validates then atomically freezes `runtime.yaml`, structured `commands.json`, `realization.json` and final `packet.json`. Nonidentical existing destinations fail. Recipe fields are width/height/frames/steps/guidance/guidance_2/preset/seed. The bounded route accepts 5–81 frames, `4k+1`, dimensions divisible by 16, positive steps and finite guidance. Lightning settings must equal the supported four-step CFG-1 preset. Diagnostic baseline remains 1280×720, 81 frames, 16 fps, seed 1; recipe choice is not authorization.

A/B/C becomes A→B and B→C; cuts are separate editorial units. Both equal-image hold arguments are retained. Commands freeze one explicit seed and runtime SHA256 per operation. `shot.py --runtime FILE --runtime-sha256 HASH --run-id ID` retains legacy defaults when absent, rejects changed input/runtime hashes before model loading and isolates outputs under `work/stories/STORY/runs/ID/shots`. `--dry-run` prints effective settings without loading/downloading/submitting anything. Negative text is inactive for CFG-1 Lightning.

`render_story_inventory.py` propagates runtime/run/hash to audit and commands. A reconciled `--operations JOURNAL_JSON` is required before it even proposes missing sequence operations: `{runtime_sha256, operations: {operation_id: "not_submitted"}}`. Pending, uncertain, failed or absent identities stay blocked. Missing output alone never implies permission to retry. This journal is operational evidence, not budget authority. Compiler commands remain unauthorized proposals; no submission adapter or automatic retry is provided. **Do not feed new sequence runs into `lumi/render_story.sh`.**

Receipts preserve key order, alignment/edge/runtime fingerprints, effective settings, native first/last hashes before encoding (PIL PNG, or lossless NPY for floating arrays with a separately labeled PNG preview) and MP4 hash. Recipe validity and full media decode/size/frame/fps validity are separate from visual acceptance. Continuation from an unreviewed or decoded prior endpoint is rejected in frozen mode: prepare a new reviewed input packet instead. Matching source endpoints does not establish matching generated pixels, velocity or support. Full clips and joins require observation at normal/reduced speed.

## Dialogue and assembly boundary

`sequence_take.selected_source` verifies an exact owner-selected take, run/runtime identity, receipt/decode, whole-clip and join review. A take mapping uses schema `feltwillow.sequence-takes.v1`, story, run_id, runtime_sha256 and `takes[piece]` containing absolute path, SHA256, owner_decision `selected`, and exact-hash `full_motion_review` with reviewer/status/whole_clip_watched/joins_reviewed. It never selects a take automatically.

`lip_sync.py apply --sequence-selection FILE` supplies exact sequence sources and isolates lip-sync outputs under that run when the existing dialogue timing/mouth recipe is ready. It retains the tracked-mouth route and speaker/word checks; it does not fabricate a v7 dialogue recipe from narration. Resulting bytes remain pending post-dialogue review. Narrator audio never drives mouths. Assembly is separately authorized; no final edit is executed by these commands.

## Verification

`tests/test_sequence_pipeline.py` uses tiny RGB fixtures and a fake backend. It proves ordered endpoint arguments, equal holds, cut preservation, runtime/seed identity, native capture, immutable packets, preflight rejection and uncertain-job guards without weights/network/GPU/scheduler. Existing planner, handoff and receipt tests protect historical behavior. Full suite cadence remains once before an authorized commit, not after every image.

Compile on the intended execution host so absolute repository/media/runtime paths and the exact Python executable refer to that host. The compiler does not transfer files or rewrite Mac paths into LUMI paths. Each renderer attempt has an exclusive immutable claim before model loading; an interrupted claim must be reconciled, never automatically retried.

Normal endpoint recipes with guidance scales on opposite sides of the CFG activation threshold are rejected until separately verified. This keeps negative-conditioning provenance explicit; standard 1/1 Lightning and 3.5/3.5 normal settings remain supported.
