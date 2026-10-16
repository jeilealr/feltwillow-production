# Perceptual-world staging

Agent A policy, 2026-10-16. Applies to still-image planning, generation and review
for stories with large character size differences. Companion rule:
[spatial staging](spatial-staging-consistency.md). This adds a narrative
readability check to the existing identity, plate, grounding and scale checks.

## Choose whose experience the audience inhabits

Physical scale describes anatomy at a given depth. Perceptual world describes
which character's experience the camera makes readable. Neither a correct
physical ratio nor an approved plate guarantees a successful composition.

| Mode | Choose when | Composition goal |
|---|---|---|
| Actor world | A solo actor or one emotional subject carries the beat | Face, gesture and local surroundings read at that actor's scale |
| Shared / bridge world | Multiple actors must communicate or interact | Every narratively important actor remains legible; preserve the size relationship |
| Environment | Empty location or explicitly justified establishing view | Geography is the subject; do not require a distant silhouette to deliver subtle emotion |

Story-specific names map to actor IDs, such as `milo`, `leo`, `shared` and
`environment`. Select from intended subject and action, not the filename,
nominal view family, or size of the largest cast member. A speaker close-up
with an offscreen listener is the speaker's world. A supplemental `x` ID is
not evidence of a close-up or a continuous zoom.

## Compose before generating

1. Name the emotional subject, required facial/gesture information and viewing
   size. Preserve the existing canonical and physical-scale authority.
2. Choose a registered camera crop that keeps the small subject's eyes, gaze,
   mouth crease, ears and relevant action readable. Magnify the actor, nearby
   ground and same-depth landmarks together. Keep a recognizable local landmark
   and the registered light direction; not every distant landmark must fit.
3. For shared shots, bring the relationship into a compact composition: the
   smaller actor beside the larger actor's face/paw, a close two-shot, or
   alternating registered speaker portraits. Changes in pose/contact must be
   possible and explicitly staged. A resting large actor can reduce the span
   without changing anatomy. Do not invent contact or move an actor between
   depths only to enlarge it without recording the move.
4. Reduce unused background *through framing*. Blur may reduce distraction but
   cannot create missing facial pixels. Compressing background area means
   excluding it with the camera; it does not mean warping plate geography.
5. If both faces and their required action cannot fit at useful detail, use a
   relationship shot plus speaker views. Register each view and its anchor
   before generation. Existing crop/anchor constraints remain authoritative;
   unresolved geometry is a planning stop, not permission to resize anatomy.

A new crop is a camera change and ordinarily a cut. It needs a matching setup
anchor; an anchor from the old wide is not automatically an approved close-view
anchor. Do not promise motion continuity merely because stills look compatible.
A stylized scale exception needs its own explicit, scoped owner decision and
hash-bound authority. World mode alone never grants that exception.

## Reusable generation brief

Record these items alongside the existing staging and reference stack:

- **World and subject:** whose experience, and which face/action must read.
- **Composition:** view, crop, focus, eye line, support, depth, landmark and
  actor-to-landmark relationship from the registered staging plan.
- **Detail task:** the expression/gesture the audience must distinguish at
  delivery resolution and at a 480×270 preview of a 1920×1080 image.
- **Exception:** any establishing purpose, why a distant subject suffices and
  which adjacent close view supplies the emotional information.

Use positive directions such as: “Inhabit the smaller actor's experience.
Frame its eyes, gaze and hand action clearly against the registered local
landmark. Apply the registered crop to character and environment together.”
For a shared view: “Keep the larger actor's presence and the smaller actor's
expression readable in the same compact interaction area.” For a portrait:
“Show the head, complete ears/mane, shoulders and upper chest against the
strongly defocused registered location.” These are composition clauses, not
complete executable prompts or new identity descriptions. Combine them with
canonical identities, exact ordered references, hashes and current staging only
after geometry and authority gates pass. Do not append contradictory instructions
to a prompt still asking for a tiny actor in a wide landscape.

## Readability review

Review at native resolution for identity/detail and a 480×270 whole-frame
preview for attention and emotional legibility. Do not judge only an enlarged
crop of the small actor. Record exact candidate hash and inspection scope.

A non-establishing subject passes when its gaze, intended expression and action
can be distinguished without searching for it. A shared view passes when the
small actor contributes to the beat independently of the large actor. A close
view passes when it provides new emotional information rather than merely a
slightly larger version of an unreadable wide. A full-body figure on blurred
scenery does not meet the standing upper-body portrait standard.

Record one or more failure labels:

| Label | Meaning |
|---|---|
| `tiny_subject` | Subject cannot carry the assigned beat at viewing size |
| `detail_floor` | Silhouette is visible but facial/action information is insufficient |
| `world_mode_mismatch` | Camera prioritizes another actor's world or scenery |
| `shared_shot_imbalance` | Large actor reads; small actor's contribution is lost |
| `false_zoom` | A view actually intended as a close view fails to restore detail |
| `environment_dominance` | Scenery overwhelms the assigned subject |

For a future candidate, fix a readability failure before adoption even if scale
is physically correct. For an existing owner-selected image, record a separate
remediation recommendation; do not rewrite its acceptance or technical checks.

## Numeric checks support judgment

Keep story-specific warning thresholds in planning metadata. A full-body
standing-equivalent height target can flag a likely problem but cannot prove
visible face size: sitting, occlusion, cropped portraits and wide poses all
change the visible box. Record measured visible body/head boxes separately in
actual reviews; do not invent them from planned anatomy. Portrait targets may
exceed 1.0 because the body is outside frame; do not treat these as invalid.

Use warnings for small planned occupancy, nominal close views, shared dialogue
and unsupported establishing exceptions. Use hard errors for stale/missing
source bindings, duplicate/missing frame records or invalid metadata. No numeric
threshold automatically approves or rejects an image. Existing physical-scale,
reference, visual and runtime gates remain in force.

The Lion and Mouse [policy](../stories/lion_and_mouse_v6/PERCEPTUAL_WORLD_POLICY.md)
and [audit](../stories/lion_and_mouse_v6/WORLD_SCALE_AUDIT.md) demonstrate this
pattern without modifying the production video implementation.
