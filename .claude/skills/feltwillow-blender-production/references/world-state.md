# World state, prop events and interactions

## Separate state layers

A shot snapshot must identify environment/asset revisions; world-space placements and units; camera; light/color setup; prop states; visible cast; character rig/action state; ambient time/phase; and simulation/cache dependencies when present. A continuous join also needs compatible velocities or phase derivatives, not only equal poses. An equal JSON snapshot is necessary evidence, not proof that every render pixel matches.

Store IDs and values, not just sentences such as "same as before." Example conceptual state:

```json
{
  "environment_revision": "ENV_Trap@candidate03",
  "story_time": {"frame": 120, "fps_num": 24, "fps_den": 1},
  "props": {"net": {"state": "fallen_intact", "topology_revision": "net_graph_01"}},
  "events": [],
  "ambient_preset": "gentle_breeze@01"
}
```

This is illustrative. Use the package's complete chain template for validation, and a deliberately designed repository adapter before deploying it. Do not insert this schema into existing story plans without migration.

## Event graph

Define legal transitions and their time. For a trap: `bundled -> released -> fallen_intact -> knot_worked -> cut -> released_from_body`. Owner/story direction determines the exact sequence. Preserve rope connection IDs and attachment positions; only the specified event changes graph connectivity. A different net mesh at every pose is a redesign, not animation.

For an acorn: ground position -> contact -> attached/carry -> transfer -> released -> resting. A parent/constraint switch must preserve the world transform at the handoff unless motion explicitly moves it. Record custody, orientation, support and visibility. The same logic covers a human carrying a basket, a bird holding an object in its beak and an animal pulling a rope.

Prefer controllable authored curves, rigs or shape sequences for the net if they serve the miniature look. Simulate only when the needed behavior justifies the cost and the cached result can be reviewed. Retain the main knot and story causal point. On v6 Milo must not suddenly acquire visible teeth because a generic gnawing rig does so.

## Interaction contract

For each interaction record initiator/receiver, contact parts, support surface, start/end times, expected relative motion, clearance and collision checks, prop state transition and failure fallback. A paw contacting a nose needs gentle, anatomically plausible placement at the real scale. A wing must clear foliage over the entire flap, not just the key poses. A doorway must fit the character plus a carried object.

Check constraints and contacts from more than the hero camera. An apparently fine frontal handover can contain large depth penetration. Use diagnostic cameras and surface overlays. Distinguish temporary allowed penetration for stylized squash from mistakes; any allowance is bounded and documented.

## Reversible world operations

Apply explicit state configurations rather than hiding/disabling arbitrary objects in ad hoc scripts. Save evaluated state references for review, and make a fresh scene rebuild produce the same intended setup. Keep spawn/despawn, fracture, costume changes and growth explicit. The presence of a cached simulation must not obscure the underlying state transition.

## Joining pieces

Choose `continuous`, `cut` or a separately specified transition. For continuous pieces: identical boundary time, current source bindings, same world/camera/light state, consistent pose and velocity, no ambient reseed, and the same applicable simulation cache. For a cut: preserve continuing world state while allowing the registered camera/time/location change; record the reason. A cut is valid storytelling, not a blanket excuse for inconsistent canon.

Use half-open editorial ranges `[start, end)` at rational FPS to avoid double-counting frames. The shared state at `end` equals the next `start`; this does not mean that both exported clips should include a duplicated endpoint sample. When an older endpoint-based tool requires inclusive endpoints, keep its generation convention and remove the duplicated sample only in a deliberate edit adapter. Do not shift audio to hide a join.

## Chain validator scope

`scripts/preflight.py chain` checks timing, source-binding syntax, and exact declared continuous-boundary state equality. It cannot infer missing scene properties, collision correctness, physical plausibility, or pixel equality. The implementation must populate complete states; omissions are not proof that nothing changed. Keep full `.blend`/cache/settings signatures and visual join tests as independent checks.

Before distributed rendering, pre-bake simulations where used and verify cache portability for the pinned Blender version [B10](sources.md#b10), [B11](sources.md#b11). Do not ask an arbitrary farm frame to evolve an unbaked sequential simulation from nowhere.
