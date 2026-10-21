# S01–S03 missing Milo performances: concrete first batch

Endpoint `image_gen.imagegen`; 14 requests; zero retries. Transparent alpha; model/seed managed by built-in tool; cost unknown. No generation submitted.

11 body/action poses plus 3 angle-specific portrait bases. Existing berry/sky/portrait candidates are included for review without regenerating them. Seven expressions remain a second stage, because their exact base hashes and geometry review do not exist yet. Acorn/berry poses reserve hand contacts but contain no invented prop designs. Strict fork pixel/root preservation must be checked/composited later, not promised by a prompt.

## Exact ordered inputs and hashes

- character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`; Identity, base anatomy, intrinsic palette and felt only
- character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png — SHA-256 `3e6bf489a5b2f04585eda046a6467c51b621c7538584a957ab754c55f5c41233`; Owner-endorsed proportion target; full asset approval not inferred
- character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_sky_r001_candidate.png — SHA-256 `8e939f2551b8a0fae293585d21c2a8d504939b16a0e7b200e005aab852e80f07`; Existing candidate stationary-body reference; no approval inferred
- character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r001_candidate.png — SHA-256 `7b4f4ebf931c7782928baa3e49224e009d69fdfeb9644a87d2e5f5a3649c92d0`; Existing candidate forward-right head geometry; no approval inferred

## Request 1: milo.harvest.berries.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_harvest_berries_3q_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png

Exact prompt:

Create exactly one reusable Milo character-performance candidate on true transparent alpha. Image 1 is canonical identity; image 2 supplies the owner-preferred berry-pose head/torso balance. Preserve canonical head size, ear silhouette, grey needle-felt wool, green eyes, cream muzzle/chest, charcoal nose, orange tail, short sturdy limbs and lean non-bulging waist. Readable upper chest and short natural neck transition, shoulders below jaw; no long neck, shortened torso, inflated head or belly. Restrained three-quarter screen-right body view, neutral studio light, closed mouth, no visible teeth. Full-body pose with complete ears, feet, hands and tail inside frame with margins, both feet on one support plane. No scenery, ground, shadows, props, text, watermark or duplicate characters. Stationary berry-harvesting action: one hand reaches forward/up with a gentle pinching grip, the other cups below to receive a berry. No berry or branch rendered; preserve two distinct readable hand roles for later prop/contact staging.

## Request 2: milo.acorn.pick_hold.3q:approach

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_pick_hold_3q_approach_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png

Exact prompt:

Create exactly one reusable Milo character-performance candidate on true transparent alpha. Image 1 is canonical identity; image 2 supplies the owner-preferred berry-pose head/torso balance. Preserve canonical head size, ear silhouette, grey needle-felt wool, green eyes, cream muzzle/chest, charcoal nose, orange tail, short sturdy limbs and lean non-bulging waist. Readable upper chest and short natural neck transition, shoulders below jaw; no long neck, shortened torso, inflated head or belly. Restrained three-quarter screen-right body view, neutral studio light, closed mouth, no visible teeth. Full-body pose with complete ears, feet, hands and tail inside frame with margins, both feet on one support plane. No scenery, ground, shadows, props, text, watermark or duplicate characters. Before pickup: feet planted, shallow knee bend, one hand reaches toward an acorn that remains on the ground in the later scene. Empty hands here, no acorn. Preserve visible neck and upper chest; do not deep-crouch or push skull toward camera.

## Request 3: milo.acorn.pick_hold.3q:hold

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_pick_hold_3q_hold_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png

Exact prompt:

Create exactly one reusable Milo character-performance candidate on true transparent alpha. Image 1 is canonical identity; image 2 supplies the owner-preferred berry-pose head/torso balance. Preserve canonical head size, ear silhouette, grey needle-felt wool, green eyes, cream muzzle/chest, charcoal nose, orange tail, short sturdy limbs and lean non-bulging waist. Readable upper chest and short natural neck transition, shoulders below jaw; no long neck, shortened torso, inflated head or belly. Restrained three-quarter screen-right body view, neutral studio light, closed mouth, no visible teeth. Full-body pose with complete ears, feet, hands and tail inside frame with margins, both feet on one support plane. No scenery, ground, shadows, props, text, watermark or duplicate characters. Pickup completed: upright body, hands gently cupped together just below chest to support one later-staged acorn; gaze at hands. Empty grip space here, no acorn rendered.

## Request 4: milo.acorn.pick_hold.3q:savor

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_pick_hold_3q_savor_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png

Exact prompt:

Create exactly one reusable Milo character-performance candidate on true transparent alpha. Image 1 is canonical identity; image 2 supplies the owner-preferred berry-pose head/torso balance. Preserve canonical head size, ear silhouette, grey needle-felt wool, green eyes, cream muzzle/chest, charcoal nose, orange tail, short sturdy limbs and lean non-bulging waist. Readable upper chest and short natural neck transition, shoulders below jaw; no long neck, shortened torso, inflated head or belly. Restrained three-quarter screen-right body view, neutral studio light, closed mouth, no visible teeth. Full-body pose with complete ears, feet, hands and tail inside frame with margins, both feet on one support plane. No scenery, ground, shadows, props, text, watermark or duplicate characters. Enjoying the discovered acorn: relaxed upright body, cupped hands raised toward but not covering closed muzzle, pleased eyelids and gentle smile. Reserve space for one later-staged acorn; render no prop, bite, teeth or speech mouth.

## Request 5: milo.acorn.hold.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_hold_3q_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png

Exact prompt:

Create exactly one reusable Milo character-performance candidate on true transparent alpha. Image 1 is canonical identity; image 2 supplies the owner-preferred berry-pose head/torso balance. Preserve canonical head size, ear silhouette, grey needle-felt wool, green eyes, cream muzzle/chest, charcoal nose, orange tail, short sturdy limbs and lean non-bulging waist. Readable upper chest and short natural neck transition, shoulders below jaw; no long neck, shortened torso, inflated head or belly. Restrained three-quarter screen-right body view, neutral studio light, closed mouth, no visible teeth. Full-body pose with complete ears, feet, hands and tail inside frame with margins, both feet on one support plane. No scenery, ground, shadows, props, text, watermark or duplicate characters. Stand holding one later-staged acorn at waist height, cupped hands with relaxed shoulders; head faces forward-right and eyes attentive to surroundings. Render empty grip space rather than a new acorn design.

## Request 6: milo.acorn.place.3q:hold

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_place_3q_hold_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png

Exact prompt:

Create exactly one reusable Milo character-performance candidate on true transparent alpha. Image 1 is canonical identity; image 2 supplies the owner-preferred berry-pose head/torso balance. Preserve canonical head size, ear silhouette, grey needle-felt wool, green eyes, cream muzzle/chest, charcoal nose, orange tail, short sturdy limbs and lean non-bulging waist. Readable upper chest and short natural neck transition, shoulders below jaw; no long neck, shortened torso, inflated head or belly. Restrained three-quarter screen-right body view, neutral studio light, closed mouth, no visible teeth. Full-body pose with complete ears, feet, hands and tail inside frame with margins, both feet on one support plane. No scenery, ground, shadows, props, text, watermark or duplicate characters. Start placing action: planted feet, shallow bend, both hands cupped at lower waist holding a later-staged single acorn. Eyes look toward intended placement. No acorn or stone rendered.

## Request 7: milo.acorn.place.3q:lower

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_place_3q_lower_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png

Exact prompt:

Create exactly one reusable Milo character-performance candidate on true transparent alpha. Image 1 is canonical identity; image 2 supplies the owner-preferred berry-pose head/torso balance. Preserve canonical head size, ear silhouette, grey needle-felt wool, green eyes, cream muzzle/chest, charcoal nose, orange tail, short sturdy limbs and lean non-bulging waist. Readable upper chest and short natural neck transition, shoulders below jaw; no long neck, shortened torso, inflated head or belly. Restrained three-quarter screen-right body view, neutral studio light, closed mouth, no visible teeth. Full-body pose with complete ears, feet, hands and tail inside frame with margins, both feet on one support plane. No scenery, ground, shadows, props, text, watermark or duplicate characters. Middle placing action: same orientation, planted feet and lean torso; modest knees/hip bend, hands lowered together to low stone-top height. Maintain visible neck and readable chest, no giant foreground head. Acorn still held in later scene, no prop rendered here.

## Request 8: milo.acorn.place.3q:released

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_place_3q_released_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png

Exact prompt:

Create exactly one reusable Milo character-performance candidate on true transparent alpha. Image 1 is canonical identity; image 2 supplies the owner-preferred berry-pose head/torso balance. Preserve canonical head size, ear silhouette, grey needle-felt wool, green eyes, cream muzzle/chest, charcoal nose, orange tail, short sturdy limbs and lean non-bulging waist. Readable upper chest and short natural neck transition, shoulders below jaw; no long neck, shortened torso, inflated head or belly. Restrained three-quarter screen-right body view, neutral studio light, closed mouth, no visible teeth. Full-body pose with complete ears, feet, hands and tail inside frame with margins, both feet on one support plane. No scenery, ground, shadows, props, text, watermark or duplicate characters. After release: same planted body and low hand position, fingers open and withdraw slightly from where the acorn rests on a later-staged stone. Hands now empty; no acorn or stone rendered. Do not return acorn to hands.

## Request 9: milo.decision.stationary.3q:forward

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_forward_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_sky_r001_candidate.png

Exact prompt:

Create exactly one reusable Milo character-performance candidate on true transparent alpha. Image 1 is canonical identity; image 2 supplies the owner-preferred berry-pose head/torso balance. Preserve canonical head size, ear silhouette, grey needle-felt wool, green eyes, cream muzzle/chest, charcoal nose, orange tail, short sturdy limbs and lean non-bulging waist. Readable upper chest and short natural neck transition, shoulders below jaw; no long neck, shortened torso, inflated head or belly. Restrained three-quarter screen-right body view, neutral studio light, closed mouth, no visible teeth. Full-body pose with complete ears, feet, hands and tail inside frame with margins, both feet on one support plane. No scenery, ground, shadows, props, text, watermark or duplicate characters. Stationary route consideration before commitment: use image 3 stationary sky body as body/feet/root reference, relax head to forward-right; neutral thoughtful gaze, no walking, stepping or held acorn. Preserve anatomical head/body dimensions; do not resize actor to match canvas.

## Request 10: milo.decision.stationary.3q:long_path

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_long_path_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_sky_r001_candidate.png

Exact prompt:

Create exactly one reusable Milo character-performance candidate on true transparent alpha. Image 1 is canonical identity; image 2 supplies the owner-preferred berry-pose head/torso balance. Preserve canonical head size, ear silhouette, grey needle-felt wool, green eyes, cream muzzle/chest, charcoal nose, orange tail, short sturdy limbs and lean non-bulging waist. Readable upper chest and short natural neck transition, shoulders below jaw; no long neck, shortened torso, inflated head or belly. Restrained three-quarter screen-right body view, neutral studio light, closed mouth, no visible teeth. Full-body pose with complete ears, feet, hands and tail inside frame with margins, both feet on one support plane. No scenery, ground, shadows, props, text, watermark or duplicate characters. Stationary gaze to safe long route on screen-left: use image 3 sky body as fixed body/feet/root reference, change only head/eye direction with physically plausible neck rotation toward left; retain three-quarter rather than an incompatible rear view. No step, body turn, acorn or route commitment. Preserve anatomical dimensions.

## Request 11: milo.decision.stationary.3q:shortcut

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_shortcut_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_sky_r001_candidate.png

Exact prompt:

Create exactly one reusable Milo character-performance candidate on true transparent alpha. Image 1 is canonical identity; image 2 supplies the owner-preferred berry-pose head/torso balance. Preserve canonical head size, ear silhouette, grey needle-felt wool, green eyes, cream muzzle/chest, charcoal nose, orange tail, short sturdy limbs and lean non-bulging waist. Readable upper chest and short natural neck transition, shoulders below jaw; no long neck, shortened torso, inflated head or belly. Restrained three-quarter screen-right body view, neutral studio light, closed mouth, no visible teeth. Full-body pose with complete ears, feet, hands and tail inside frame with margins, both feet on one support plane. No scenery, ground, shadows, props, text, watermark or duplicate characters. Stationary gaze to shortcut on screen-right: use image 3 sky body as fixed body/feet/root reference, change only head/eye direction toward right. No step, body turn, acorn or route commitment. Preserve anatomical dimensions; decision is later.

## Request 12: milo.portrait.base.3q.look_up:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_look_up_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r001_candidate.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_sky_r001_candidate.png

Exact prompt:

Create one transparent Milo full-head/upper-chest neutral portrait-base candidate. Image 1 controls canonical identity/anatomy/material/palette; image 2 is the existing candidate portrait geometry inspiration, not approval; image 3 supplies stationary body/neck anatomy and upward-view inspiration only. Preserve skull/ear/head proportions, muzzle, green eyes, grey felt and cream upper chest. Turn head/eyeline up with physically plausible short neck and a compatible three-quarter view; body remains screen-right. Keep both ears entirely inside frame with ample margin, visible neck transition and shoulders. Neutral attentive closed-mouth expression, no teeth, speech shape or new head silhouette. No scenery, props, ground, shadow, text or watermark. Neutral studio light, real transparent alpha. New angle is a proposed geometry base requiring owner review before dependent expressions.

## Request 13: milo.portrait.base.3q.look_left:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_look_left_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r001_candidate.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_sky_r001_candidate.png

Exact prompt:

Create one transparent Milo full-head/upper-chest neutral portrait-base candidate. Image 1 controls canonical identity/anatomy/material/palette; image 2 is the existing candidate portrait geometry inspiration, not approval; image 3 supplies stationary body/neck anatomy and upward-view inspiration only. Preserve skull/ear/head proportions, muzzle, green eyes, grey felt and cream upper chest. Turn head/eyeline left with physically plausible short neck and a compatible three-quarter view; body remains screen-right. Keep both ears entirely inside frame with ample margin, visible neck transition and shoulders. Neutral attentive closed-mouth expression, no teeth, speech shape or new head silhouette. No scenery, props, ground, shadow, text or watermark. Neutral studio light, real transparent alpha. New angle is a proposed geometry base requiring owner review before dependent expressions.

## Request 14: milo.portrait.base.3q.look_right:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_look_right_r001_candidate.png`

Ordered inputs: character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png, character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r001_candidate.png, character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_sky_r001_candidate.png

Exact prompt:

Create one transparent Milo full-head/upper-chest neutral portrait-base candidate. Image 1 controls canonical identity/anatomy/material/palette; image 2 is the existing candidate portrait geometry inspiration, not approval; image 3 supplies stationary body/neck anatomy and upward-view inspiration only. Preserve skull/ear/head proportions, muzzle, green eyes, grey felt and cream upper chest. Turn head/eyeline right with physically plausible short neck and a compatible three-quarter view; body remains screen-right. Keep both ears entirely inside frame with ample margin, visible neck transition and shoulders. Neutral attentive closed-mouth expression, no teeth, speech shape or new head silhouette. No scenery, props, ground, shadow, text or watermark. Neutral studio light, real transparent alpha. New angle is a proposed geometry base requiring owner review before dependent expressions.

## Deferred expression stage

- milo.expression.curious.3q (needs reviewed compatible base)
- milo.expression.decisive.3q (needs reviewed compatible base)
- milo.expression.hopeful_confidence.3q (needs reviewed compatible base)
- milo.expression.startled_realization.3q (needs reviewed compatible base)
- milo.expression.startled_realization.3q.look_left (needs reviewed compatible base)
- milo.expression.startled_realization.3q.look_right (needs reviewed compatible base)
- milo.expression.startled_realization.3q.look_up (needs reviewed compatible base)
