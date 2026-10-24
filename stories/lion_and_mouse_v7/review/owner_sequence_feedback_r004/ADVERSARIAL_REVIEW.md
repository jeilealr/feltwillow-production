# Independent adversarial runtime review

Reviewer: `/root/editorial`, separate from the runtime writer. Source HEAD: `1a74ab85c605ea864fc249c0346cebbe1e60d8c1`; reviewed uncommitted r004 implementation on 24 October 2026. Read-only code review and CPU temporary fixtures; no provider, download, model load, GPU submission or source-art change. The reviewer authored the earlier visual source migration, so this is independent review of runtime/assembly changes, not independent authorship of the entire pipeline.

## Actual checks

Command: `/Users/lealroja/miniconda3/envs/feltwillow/bin/python -m unittest tests.test_r004_runtime.R004RuntimeTests.test_C06_single_reaches_backend_without_last_image tests.test_r004_runtime.R004RuntimeTests.test_C29_piece_frames_reach_actual_backend tests.test_r004_runtime.R004RuntimeTests.test_C37_alias_retained_without_extra_model_job tests.test_sequence_timeline -v`

Result: **7 tests passed**. Checked C06 one-image backend `last_image=None`; C29 piece frame settings; C37 alias job suppression; C28 cumulative cells/gaps/duplicate rejection; C40/C41 short/long accounting fixture; C48 absent review rejection; real CPU static preview encode/decode. Two ResourceWarnings reported unclosed backend input image handles; no visual quality was inferred. The fake Wan outputs are deliberately not playable and prove wiring only.

Existing `tests.test_audio_visual_plan -q` session 24332 was polled once after resumption: process ID unknown, result unavailable to this reviewer. Do not count it as passing from this report.

## Blocking findings reproduced

1. **Per-piece static frame override bypasses validation (C29).** Set a valid synthetic packet to `sequence.method=static_frame_hold`, one individual input/no edges, base frames=5, and `recipe.pieces.chain_p000.frames=-3`. `compile_packet` accepted and froze `render_pieces[0].frames=-3`. The static preflight substitutes 5 instead of checking the effective override. Validate each effective static count as positive nonboolean integer before freezing; add negative/boolean override regressions. The renderer may later reject it, but a technically-ready frozen packet is already false.
2. **Rejected retime/trim evidence can pass (C48).** A ten-frame source allocation into sixteen output cells accepts `retime_review={reviewer:fixture,status:failed}`; only reviewer presence is checked. Trim evidence uses the same pattern. Require pass status and source/mapping-bound review fingerprints, not reviewer text alone.
3. **Source FPS is ignored, allowing unreviewed speed changes (C28/C41/C48).** CPU FFmpeg fixture encoded sixteen frames at 8 fps (2 s). `compile_timeline` accepted those sixteen source frames into sixteen output cells at16fps (1 s), without any retime review, because frame counts agree. Inspect and bind actual source frame rate/decode facts; compare source-window duration to editorial duration and require reviewed mapping for any speed change.
4. **End trims are self-declared, allowing silent loss (C48).** CPU fixture encoded100frames at16fps; mapping start_frame=0/frame_count=16 with no `trimmed_end_frames` was accepted without trim review. Infer omitted leading/trailing frames from actual decoded count; require contact/word-bound trim approval rather than trusting omission of a flag.

All four findings were sent directly to the runtime integrator. This report records the observed pre-fix state; it is not an unconditional sign-off. Recheck fixes and regressions before engineering closure. Current quantization was also inspected: `sequence_timeline.quantize` uses the same exact Fraction/round convention as `sequence_plan.frame_accounting`, including half-cell ties.

## Scope limits

Source/alias/timing guards inspected include exact source SHA/fit recheck before freezing, immutable runtime/run identity, one-image optional end, same-hash shared-boundary suppression, static distinct-end rejection, bounded Wan frames, zero model calls for static method, source-native boundary capture and output-pending labels. Missing source states and sequence blockers remain readiness blockers. These are code checks, not a still/whole-motion/mouth/owner acceptance. Real audio phrase markers, source art, joins and motion remain outside these fixtures.

## Checked file fingerprints

- `production/sequence_export.py`: `2108eca0b4b501f697e9ac5553155ed8973f64f7b718242a6597c8c66a35042e`
- `production/shot.py`: `e80eb4ad53c0d6c3e34ac5fc98142a748e22dc617d5284840563383e896b1c80`
- `production/sequence_readiness.py`: `fb269655e1e6dd263a617ef1220b5fdfb7cb7c6ac745574524726d44f9c1258f`
- `production/sequence_timeline.py`: `de068d2279e0b573a311154fe78d51debccf2fa4525d0ded6dcf93cc557b5949`
- `feltwillow/local_video.py`: `00788bb6c6047c106984ed1d5eaff60cbdb682dedd46c4d6046c1cddae589fa3`
- `tests/test_r004_runtime.py`: `6206e5f4cf8974c09acd13f4a32c2265873c1cf314d8517c50c5c47accdabe8b`
- `tests/test_sequence_timeline.py`: `7fa33c6dc33d8b304a08214811a07c177880aa45a4e27848a85d1e9893a33ca9`

## Independent fix verification, 24 October 2026

Re-executed all four original adversarial fixtures against the updated source. Each now rejects before freezing/assembly:

- F1: `positive integer effective static frame count required`.
- F2: `retime requires explicit reviewed mapping` for failed review status.
- F3: `source FPS/duration change requires reviewed retime` for sixteen source frames at8fps into sixteen cells at16fps.
- F4: `trim requires actual contact/word review` for first16of100frames with omitted end-trim flag.

The same seven targeted unit/CPU integration tests passed again (7 tests, 0.365 s); unclosed input-image ResourceWarnings persist. Original four findings are fixed by this verification.

### Newly discovered target-mapping invalidation blocker (C49/C48)

`valid_mapping_review` fingerprints only source mapping fields. The target timeline interval, sample rate/fps and output frame cells are excluded. Actual CPU fixture: sixteen source frames at16fps, mapping `{start_frame:0,frame_count:16}` with a pass/sourceSHA/mappingSHA-bound retime review. Compile into an initially reviewed8-cell target (`end_sample:12000` at24kHz). Change only the target to24cells (`end_sample:36000`, total_samples accordingly) and reuse that review: compilation still succeeds. Thus a retime review can transfer to a different target speed/duration. Include target sample/frame mapping in the reviewed fingerprint and validate its actual values against the interval; regression must reject the changed target without fresh review. This finding was sent to the integrator. Sign-off remains pending that narrow invalidation fix.

Fix-verification fingerprints:

- `production/sequence_export.py`: `19807ca993fc620374989c058581dfeabc3872580d6fa173786567c4ad1bda11`
- `production/sequence_timeline.py`: `de068d2279e0b573a311154fe78d51debccf2fa4525d0ded6dcf93cc557b5949`
