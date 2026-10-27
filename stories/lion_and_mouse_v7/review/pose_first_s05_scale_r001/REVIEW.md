# S05 scale correction — unselected CPU preview

The registered grounded Milo pose remains byte-identical at SHA256
`f23d5d9b38a7bfdacbb6a917bb10a0f54970bf8c301d93a717594bf4926a58a5`.
The previous S05 roll was composed at `0.32`; the first grounded diagnostic
used `0.24`. Native matching near-ear and near-iris spans, with the same
camera/local depth contract, derive `0.2734478808705613` for the landing.
The feature ratios are `0.847938` and `0.861111`. This is an approximate
projection comparison, not a hidden 3D measurement.

The Milo nose target `[1230,718]` is recorded from Leo's muzzle landmark
`[1300,625]` with clearance `[-70,+93]`, independently of scale. Grass support
target is `[1070,760]`. The derived-scale anchor residual is `7.66` native
pixels against a reviewed 12-pixel diagnostic tolerance. The previous target
was computed from the chosen scale and therefore had a meaningless near-zero
residual. Source/target landmarks and confidence are in `ANCHOR_RECIPE.json`.

The corrected composition is visually closer to the roll's apparent Milo size
than the old preview. Milo stays low on the grass, with no visible muzzle or
paw penetration. The underlying Leo/tree/sunset pixels are unchanged outside
the actor/shadow effect mask. **Still unresolved:** Milo's mouth reads slightly
cheerful for a fresh impact; the contact shadow is approximate; Leo foreground
depth/occlusion is not reviewed. No selection or video readiness is implied.

One corrected CPU candidate was made. No pose generation, provider call, GPU
job or retry occurred in this correction.
