# Video experiment results — 2026-10-18

Seven of nine small-g jobs completed. Seeds45/46 timed out at30 minutes; no completed clip receipts exist for them. Lip-sync dev-g job22929108 completed. No model inference was repeated to assemble these reviews. All results remain isolated experiments, not approved production outputs.

## Playable reviews

- [Milo: animated-face lip-sync, with audio](../work/stories/lion_and_mouse_v6/experiments/lipsync_probe/20261017/wan_milo/review_with_audio.mp4)
- [Leo: animated-face lip-sync, with audio](../work/stories/lion_and_mouse_v6/experiments/lipsync_probe/20261017/wan_leo/review_with_audio.mp4)
- [Continuity: generated last frame versus next story keyframe](../work/stories/lion_and_mouse_v6/experiments/blender_fun_control/i2v_followup_20261016/continuity_comparison.mp4)
- [Articulated Blender: reach, walk and camera, normal vs Control](../work/stories/lion_and_mouse_v6/experiments/blender_fun_control/reviews_available_20261018/articulated_6way.mp4)
- [Endpoint: start-only vs start-and-end image](../work/stories/lion_and_mouse_v6/experiments/blender_fun_control/matrix_endpoint_20261016/comparison.mp4)
- [Guide representation: edges, depth, stationary depth](../work/stories/lion_and_mouse_v6/experiments/blender_fun_control/matrix_representation_20261016/comparison.mp4)
- [Available seed comparison: 43 vs 44](../work/stories/lion_and_mouse_v6/experiments/blender_fun_control/reviews_available_20261018/seeds_available.mp4)
- [Milo static-face lip-sync control, with audio](../work/stories/lion_and_mouse_v6/experiments/lipsync_probe/20261017/static_milo/review_with_audio.mp4)
- [Leo static-face lip-sync control, with audio](../work/stories/lion_and_mouse_v6/experiments/lipsync_probe/20261017/static_leo/review_with_audio.mp4)

Lip-sync reviews show original video on the left and word-timed composite on the right, with the actual line recording and0.5s matched padding. Silent composite and padded PCM WAV are beside each review for DaVinci. Alignment/export success is not a perceptual-sync approval. The method is one-shape jaw pulsing in a fixed ROI; it does not synthesize phoneme-specific lips. Approximate maximum source mouth-region displacement was4.5px for moving Milo and18.5px for moving Leo: inspect mask sliding and ghosting, especially Leo.

Blender review rows are reach/walk/camera; normal Wan on left, guided Control on right. Mid-frame poster inspection shows conspicuous shape/prop distortions in guided reach and camera cases. This is preliminary visual evidence, not a full playback score; rough proxy proportions and scene mismatch remain confounders. The guide is a working control mechanism, not demonstrated improvement.

Endpoint target pixel MAE decreased from35.81 to22.93/255 with ending-image conditioning. This is not proof of correct anatomy, acting or exact endpoint reproduction. Seed comparison includes only43/44 and makes no statistical robustness claim.

## Completed job runtimes

| Test | Job | Elapsed |
|---|---|---|
| Endpoint pair |22916690|8m17|
| Guide representation |22916692|15m07|
| Continuity first |22928746|11m19|
| Continuity follow-ups |22928747|16m17|
| Seed44 |22928748|10m48|
| Articulated normal |22928751|9m36|
| Articulated Control |22928752|16m41|
| Lip-sync diagnostic |22929108|14m37|

Seeds45/46 (22928749/22928750) both timed out on nid005097 after30m03. Logs reached step2/4; incomplete attempt receipts still say running because termination prevented finalization. They are not running now and were not silently relabeled complete. No inference rerun was submitted.

The original combined review job22928753 was permanently dependency-blocked by the two timeouts and was retired. A first CPU repair22939316 failed on a missing seed receipt. Versioned collector22939358 then independently verified completed source hashes and exported the six-way Blender and two-seed reviews, explicitly recording omitted seeds. No completed source clip was overwritten.
