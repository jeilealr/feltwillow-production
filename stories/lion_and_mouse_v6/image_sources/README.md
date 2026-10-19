# Selected composition sources

Resolve the current image by frame ID in `../keyframe_plan.json` and confirm its
hash in `../owner_visual_acceptance.json`. The perceptual-world recipes and
owner-adoption receipt here describe the geometric bases selected before the
subsequent C-style integration finish. Their original output paths, status
strings and hashes describe that selection event, not every current revision.

For a finished frame, `selected_composition_record` identifies its geometric base;
`selected_integration_finish` supplies the additional finishing receipt, original
archive/hash and finished hash. Apply both stages when reproducing the selection.
For the subsequent `s04_p02` facial-lighting correction, also apply
`selected_lighting_repair`; its receipt binds the preserved r13 input and current
r14 output. The initial finishing receipt continues to describe r13.

The [integration audit](../review/integration_finish/README.md) records exactly
which frames changed; `adoption_paths.json` maps prior paths to preserved original
PNGs and active revisions. Never infer current status from an old revision name.

`cleanup_manifest.json` maps earlier relocated inputs and provides Git recovery
locators for removed derivatives. Original receipt paths and exact prompt text
remain generation-time provenance. Reusable current RGBA layers live under
`character/characters/lion_and_mouse_v6/interactions/sources/`. Replaced finishing
bases live in that folder's `integration_originals/`, outside the active keyframe
directory. Recovering an earlier rejected image does not authorize reusing it.

For another story or review, follow the [integration rules](../../../docs/character-background-integration.md)
and start a new scoped run. Preserve geometry first, then apply only the needed
integration finish; retain the original when a trial offers no clear benefit.
