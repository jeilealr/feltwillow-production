# S01–S03 Milo scene revision preflight

The owner accepted the 22 current Milo depictions for performance use on 2026-10-21. `OWNER_PERFORMANCE_ACCEPTANCE.json` binds each decision to the exact PNG hash; `BEFORE_LIBRARY.json` and `before_sidecar_*.json` preserve prior metadata. Original PNGs, canonical images and historical generation facts are unchanged. This acceptance does not approve scene images, prop fit or anatomy measurements.

[Read-only comparison gallery](review.html) pairs each existing composition with the selected Milo reference and retains local audio playback. All 20 approved requests completed with one saved r002 candidate each and no retries. The three fork shots remain held and the environment cutaway is unchanged.

[Concrete proposed operation](OPERATION.md): 20 requests to `image_gen.imagegen`, one new r002 candidate per request, zero automatic retries, opaque 16:9 output, cost unknown. Each request records three ordered input paths/hashes and its exact prompt in `OPERATION.json`. The owner approved this exact operation with “yes”; see `AUTHORIZATION.json` and `EXECUTION.json`. The full-scene guidance strategy can redraw pixels and needs subsequent visual review.

S03-L006/007/008 remain held together: the shared camera, standing depth, actor root and scale anchor are unmeasured, and the long-path pose turns the whole body. S02-L002 remains the existing environment-only image. This pass revises representative stills, not every endpoint in S01–S03.

Known anatomy, prop, gait and planned-expression limitations remain visible in the proposal and gallery. No production readiness or scene selection is inferred.

## Completed run review

`AUDIO_IMAGE_INDEX.json` records the 20 new candidates plus three held and one retained source image. Each output has a same-basename receipt and exact audio/performance/input hashes. `VISUAL_OBSERVATIONS.json` records advisory findings: retained pale corner symbol on S01-L001, acorn scale variation across compositions, and hand contact remaining in the S02-L004 released endpoint. These need review; no extra repairs were submitted. No scene selection or measured anatomy pass has been inferred. Built-in model/seed/request IDs and actual cost were not exposed.
