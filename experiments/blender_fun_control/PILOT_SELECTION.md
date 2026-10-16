# V6 motion-control pilot selection

Metadata selection at `6fae81c`, 2026-10-16. **None is production-ready or
visually re-approved by Agent B.** All are isolated non-production candidates;
Agent A's subsequent review may change suitability. The only executable tool
in this phase audits inputs. No guide or video has been generated.

| Order / experiment | Endpoints | Intent | Eligibility and next gate |
|---|---|---|---|
| P1: simple same-view pose | `s01x_p03 → s01_p04` | Milo remains grounded while enjoying/nibbling the acorn; test small silhouette motion with stable camera | Registered same-view candidate; same `medium_solo`, plate and crop. Metadata contact/depth are identical, so do not invent a walk. Acorn authority and actual endpoint anatomy/contact still need review |
| P2: dialogue portrait hold | `s08_p03 → s08_p03` | Measure identity/ear/camera drift with mild head motion before lip-sync | Single `portrait_milo`, sole speaker MOUSE. Same-image hold avoids crossing its neighboring camera cuts. No claim that motion control produces speech or validated mouth timing |
| P3: shared close hold | `s05_p03 → s05_p03` | Small breathing/attention motion while preserving both silhouettes, grounding and actor separation | Current asset is the user-liked `s05_p03_r19_candidate.png`, `close_two`. Choose a hold because adjacent shots are cuts; verify with Agent A before any guide |

Start assets resolve from `keyframe_plan.json` rather than hard-coded candidate
filenames. Use `audit_inputs.py` for actual current file and planning hashes.
P1 crop is `[0.2775, 0.36, 0.625, 0.625]`; P2
`[0.55362, 0.67979, 0.21277, 0.21277]`; P3
`[0.35273, 0.45636, 0.45455, 0.45455]` at this snapshot. These are
**x, y, width, height** on the full plate, not opposite corners or world units.

P1 can test start-only conditioning while keeping the second keyframe as a
held-out evaluation target. If the backend cannot enforce an end image,
record `end_image_role: evaluation_only`; do not imply first/last parity with
baseline. For a fair first A/B comparison, use start-only in both models.
Test baseline's existing first+last recipe separately as the production-capable
comparator if needed. Holds likewise do not prove endpoint anchoring.

Do not use weak/tiny-subject examples as starting anchors. In particular,
`s07_p03 → s07_p04` is geometrically tempting but its first image was named as
weak by the user. Agent A must remediate/review it before video experimentation.
Do not infer shared-world success from a view name alone.

## Deferred stress test

`s10_p01 → s10_p02` is a registered Leo-only same-view approach on the trap
path. Ground contact changes from `(0.42,0.78)` to `(0.48,0.81)` and planned
depth from 0.588 to 0.676. It introduces rope/net prop topology, so defer it
until simple control demonstrates benefit and props/endpoints have appropriate
review. Do not include `s10_p02 → s10_p03` net release in the initial pilot.
No fourth job is authorized or scheduled.

## Execution sequence and acceptance

1. Validate an official reference control example on allocated ROCm compute.
   Change the control with other settings fixed; require visible corresponding
   movement and record resource measurements. No custom Blender work first.
2. Select only P1 initially. Re-read Agent A's current policy and selected-image
   evidence, inspect full-resolution endpoints, freeze hashes and write a new
   run manifest. Use documented backend dimensions and transform all inputs
   together. 81 frames/16 FPS is the A14B reference starting point, not approved
   narrative timing; do not pad or retime story audio to fit this test.
3. Try a cheap deterministic silhouette source followed by the actual backend's
   Canny preprocessing. Synthetic edges are not validated control merely because
   a video decoder accepts them. Keep P1 contact fixed; modulate small pose
   changes only. No new scale/framing policy is introduced.
4. Compare a baseline I2V clip, controlled clip and stationary/moving control
   ablation. Match start bytes, prompt intent, aspect/resolution where supported,
   duration and seed policy; disclose model-specific scheduler/guidance changes.
   Matched seeds across models are not matched noise. Apply no style or speed
   LoRA until compatible expert loading and visual behavior are demonstrated.
5. Inspect start/middle/end frames and full playback with the
   [scorecard](EVALUATION.md). Expand to P2/P3 only if there is a useful gain
   without identity/grounding regressions. Repeat on a second seed only after
   the first comparison justifies its cost.
6. Introduce Blender only if proxy-guide work succeeds and needs calibrated
   depth/camera/parallax it cannot cheaply provide. CPU/headless proof comes
   before investment in animal rigs. Never equate plate coordinates with 3D
   meters; human OpenPose is not a quadruped skeleton.

## Guide representation order

1. **Silhouette source → documented Canny/edge preprocessing.** Cheapest,
   deterministic, actor contact and outline measurable. Watch domain mismatch:
   a blob outline does not encode paws, faces or fur.
2. **Depth-like control.** Helpful for occlusion and approach, after documenting
   near/far convention, range, channels and model normalization. Story depth_t
   is a staging interpolation, not metric depth or automatically a depth map.
3. **Trajectories / camera proxies.** Try only the selected implementation's
   actual representation. Separate actor motion from camera motion; Control-Camera
   is a different backend, not a free extra control input.
4. **Adapted animal pose.** Advanced, needs quadruped/mouse keypoints or rigs.
   Do not use a human-pose sample as evidence of Leo/Milo pose suitability.
