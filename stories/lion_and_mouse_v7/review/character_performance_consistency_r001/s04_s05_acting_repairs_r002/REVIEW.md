# Milo S04–S05 acting and two body repairs

Prepared only. **7 requests, one output each, no retries**, endpoint `image_gen.imagegen`. Cost unknown; model and seed not exposed. No generation submitted.

Operation SHA-256: `4dbdb6a147fce16beede63372f1c709c04def469e8834fd33c0034d65fd1a62c`. Exact input hashes, complete prompts and tool arguments: [OPERATION.json](OPERATION.json).

Body-only owner retention is recorded separately in [OWNER_FEEDBACK.json](OWNER_FEEDBACK.json). It is not full acting approval or measured anatomy approval. Turn entry now reuses the existing exit file without duplication. Original images, receipts, audio, world events and S01–S03 selection remain untouched.

The original forward-pitch request returned no image or provider ID. Outcome/cost cannot be reconciled from a provider ID; no new submission for that key is included.

## Proposed requests

### 1. milo.run.duck.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_run_duck_default_3q_r002_candidate.png`

body repair plus requested acting; new bytes require owner review

Inputs:

- `character/characters/lion_and_mouse_v7/Milo/poses/milo_run_duck_default_3q_r001_candidate.png` — SHA-256 `52cb7003a9332646d2bf4f87f9bb8aa44711865990f68d6371577897546c3d40`; acting_reference_only; no anatomy authority or approval transfer

- `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`; identity_anatomy_material_palette

- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg` — SHA-256 `614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5`; visible_surface_measurements_only; never render markings

Prompt:

Edit reference 1 for the requested local body correction. Reference 2 owns identity/anatomy; reference 3 contains measurement guides. Preserve the approved Milo canonical identity, lean grey felt anatomy, cream muzzle and belly boundaries, moss-green eyes, orange tail, canonical ears, eyes and paw construction. Short readable neck; no enlarged head, wide belly, shortened limbs or independently scaled body parts. Canonical upright projected head fraction 0.39 +/-0.01 applies only at comparable upright angle/support, never crouch or tumble. Use annotated visible-surface width, cream patch and paw references at comparable views, not hidden-joint guesses. Do not render annotations. Mouth closed, no teeth, no speech mouth. Genuine transparent alpha, neutral soft light, no background, ground plane, props, labels or shadows. Exactly one candidate; no variants. Crouch very low near the imagined floor beneath a low branch. Flex hips and knees coherently with both feet supporting the body, chest leaning forward and head lowered without crushing torso or shortening neck. Hands held clear near knees. Focused hurried concentration, not a pleasant smile. Entire character including ears, toes and tail visible with margins.

### 2. milo.trip.rear_paw.3q:paw_contact

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_trip_rear_paw_paw_contact_3q_r002_candidate.png`

body repair plus requested acting; new bytes require owner review

Inputs:

- `character/characters/lion_and_mouse_v7/Milo/poses/milo_trip_rear_paw_paw_contact_3q_r001_candidate.png` — SHA-256 `57e21c52da787a31d43e53d67514902237ac02651327c6fb9ce5068223099ceb`; acting_reference_only; no anatomy authority or approval transfer

- `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`; identity_anatomy_material_palette

- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg` — SHA-256 `614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5`; visible_surface_measurements_only; never render markings

Prompt:

Edit reference 1 for the requested local body correction. Reference 2 owns identity/anatomy; reference 3 contains measurement guides. Preserve the approved Milo canonical identity, lean grey felt anatomy, cream muzzle and belly boundaries, moss-green eyes, orange tail, canonical ears, eyes and paw construction. Short readable neck; no enlarged head, wide belly, shortened limbs or independently scaled body parts. Canonical upright projected head fraction 0.39 +/-0.01 applies only at comparable upright angle/support, never crouch or tumble. Use annotated visible-surface width, cream patch and paw references at comparable views, not hidden-joint guesses. Do not render annotations. Mouth closed, no teeth, no speech mouth. Genuine transparent alpha, neutral soft light, no background, ground plane, props, labels or shadows. Exactly one candidate; no variants. Repair the image-left leg: visible continuous attachment through hip and thigh into knee, shin, ankle and paw, no floating/disconnected segment. Preserve the stumbling rear-paw-contact action, canonical limb construction and other body geometry. Alarmed raised brows, wide eyes and tense closed muzzle, no smile. Full character with margins; Leo obstacle is implied, not drawn.

### 3. milo.expression.hurried_focus.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_expression_hurried_focus_3q_r001_candidate.png`

standalone expression candidate; does not apply face to retained body PNGs

Inputs:

- `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r003_candidate.png` — SHA-256 `a981bbb205d20384279db3785045d9d5dce0836e1d666963b0f962ec214a1d79`; portrait_geometry_only

- `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`; identity_anatomy_material_palette

- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg` — SHA-256 `614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5`; visible_surface_measurements_only; never render markings

Prompt:

Edit reference 1, the owner-selected portrait base, to create a reusable facial acting variant. Reference 2 owns canonical identity and reference 3 only measurement guides. Preserve the approved Milo canonical identity, lean grey felt anatomy, cream muzzle and belly boundaries, moss-green eyes, orange tail, canonical ears, eyes and paw construction. Short readable neck; no enlarged head, wide belly, shortened limbs or independently scaled body parts. Canonical upright projected head fraction 0.39 +/-0.01 applies only at comparable upright angle/support, never crouch or tumble. Use annotated visible-surface width, cream patch and paw references at comparable views, not hidden-joint guesses. Do not render annotations. Mouth closed, no teeth, no speech mouth. Genuine transparent alpha, neutral soft light, no background, ground plane, props, labels or shadows. Exactly one candidate; no variants. Keep reference 1 head silhouette, three-quarter forward-right head angle, head/ear/eye/muzzle sizes and positions, short neck, shoulder and upper-chest crop exactly compatible. Full ears and whiskers with clearance. Change only eyebrows, eyelids, gaze and restrained closed-muzzle crease to express: Hurried focus: urgent forward eyeline, slightly lowered inner brows, alert lids, closed concentrated muzzle; no casual smile. Do not enlarge skull or change iris/ear design to amplify emotion. This face asset will require local pitch/roll/view registration before use on ducked or falling bodies; do not rotate or distort the base in this request.

### 4. milo.expression.low_clearance_focus.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_expression_low_clearance_focus_3q_r001_candidate.png`

standalone expression candidate; does not apply face to retained body PNGs

Inputs:

- `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r003_candidate.png` — SHA-256 `a981bbb205d20384279db3785045d9d5dce0836e1d666963b0f962ec214a1d79`; portrait_geometry_only

- `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`; identity_anatomy_material_palette

- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg` — SHA-256 `614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5`; visible_surface_measurements_only; never render markings

Prompt:

Edit reference 1, the owner-selected portrait base, to create a reusable facial acting variant. Reference 2 owns canonical identity and reference 3 only measurement guides. Preserve the approved Milo canonical identity, lean grey felt anatomy, cream muzzle and belly boundaries, moss-green eyes, orange tail, canonical ears, eyes and paw construction. Short readable neck; no enlarged head, wide belly, shortened limbs or independently scaled body parts. Canonical upright projected head fraction 0.39 +/-0.01 applies only at comparable upright angle/support, never crouch or tumble. Use annotated visible-surface width, cream patch and paw references at comparable views, not hidden-joint guesses. Do not render annotations. Mouth closed, no teeth, no speech mouth. Genuine transparent alpha, neutral soft light, no background, ground plane, props, labels or shadows. Exactly one candidate; no variants. Keep reference 1 head silhouette, three-quarter forward-right head angle, head/ear/eye/muzzle sizes and positions, short neck, shoulder and upper-chest crop exactly compatible. Full ears and whiskers with clearance. Change only eyebrows, eyelids, gaze and restrained closed-muzzle crease to express: Low-clearance concentration: focused forward/down eyeline and intent brows, closed mouth, no casual smile. Do not enlarge skull or change iris/ear design to amplify emotion. This face asset will require local pitch/roll/view registration before use on ducked or falling bodies; do not rotate or distort the base in this request.

### 5. milo.expression.startled.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_expression_startled_3q_r001_candidate.png`

standalone expression candidate; does not apply face to retained body PNGs

Inputs:

- `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r003_candidate.png` — SHA-256 `a981bbb205d20384279db3785045d9d5dce0836e1d666963b0f962ec214a1d79`; portrait_geometry_only

- `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`; identity_anatomy_material_palette

- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg` — SHA-256 `614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5`; visible_surface_measurements_only; never render markings

Prompt:

Edit reference 1, the owner-selected portrait base, to create a reusable facial acting variant. Reference 2 owns canonical identity and reference 3 only measurement guides. Preserve the approved Milo canonical identity, lean grey felt anatomy, cream muzzle and belly boundaries, moss-green eyes, orange tail, canonical ears, eyes and paw construction. Short readable neck; no enlarged head, wide belly, shortened limbs or independently scaled body parts. Canonical upright projected head fraction 0.39 +/-0.01 applies only at comparable upright angle/support, never crouch or tumble. Use annotated visible-surface width, cream patch and paw references at comparable views, not hidden-joint guesses. Do not render annotations. Mouth closed, no teeth, no speech mouth. Genuine transparent alpha, neutral soft light, no background, ground plane, props, labels or shadows. Exactly one candidate; no variants. Keep reference 1 head silhouette, three-quarter forward-right head angle, head/ear/eye/muzzle sizes and positions, short neck, shoulder and upper-chest crop exactly compatible. Full ears and whiskers with clearance. Change only eyebrows, eyelids, gaze and restrained closed-muzzle crease to express: Sudden alarm: widened eyelids, raised brows and startled gaze, tense closed muzzle. Do not enlarge skull or change iris/ear design to amplify emotion. This face asset will require local pitch/roll/view registration before use on ducked or falling bodies; do not rotate or distort the base in this request.

### 6. milo.expression.falling_panic.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_expression_falling_panic_3q_r001_candidate.png`

standalone expression candidate; does not apply face to retained body PNGs

Inputs:

- `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r003_candidate.png` — SHA-256 `a981bbb205d20384279db3785045d9d5dce0836e1d666963b0f962ec214a1d79`; portrait_geometry_only

- `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`; identity_anatomy_material_palette

- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg` — SHA-256 `614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5`; visible_surface_measurements_only; never render markings

Prompt:

Edit reference 1, the owner-selected portrait base, to create a reusable facial acting variant. Reference 2 owns canonical identity and reference 3 only measurement guides. Preserve the approved Milo canonical identity, lean grey felt anatomy, cream muzzle and belly boundaries, moss-green eyes, orange tail, canonical ears, eyes and paw construction. Short readable neck; no enlarged head, wide belly, shortened limbs or independently scaled body parts. Canonical upright projected head fraction 0.39 +/-0.01 applies only at comparable upright angle/support, never crouch or tumble. Use annotated visible-surface width, cream patch and paw references at comparable views, not hidden-joint guesses. Do not render annotations. Mouth closed, no teeth, no speech mouth. Genuine transparent alpha, neutral soft light, no background, ground plane, props, labels or shadows. Exactly one candidate; no variants. Keep reference 1 head silhouette, three-quarter forward-right head angle, head/ear/eye/muzzle sizes and positions, short neck, shoulder and upper-chest crop exactly compatible. Full ears and whiskers with clearance. Change only eyebrows, eyelids, gaze and restrained closed-muzzle crease to express: Falling panic: strongly raised worried brows, wide alarmed eyes and tense closed muzzle, no smile. Do not enlarge skull or change iris/ear design to amplify emotion. This face asset will require local pitch/roll/view registration before use on ducked or falling bodies; do not rotate or distort the base in this request.

### 7. milo.expression.stunned_landing.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_expression_stunned_landing_3q_r001_candidate.png`

standalone expression candidate; does not apply face to retained body PNGs

Inputs:

- `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r003_candidate.png` — SHA-256 `a981bbb205d20384279db3785045d9d5dce0836e1d666963b0f962ec214a1d79`; portrait_geometry_only

- `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`; identity_anatomy_material_palette

- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg` — SHA-256 `614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5`; visible_surface_measurements_only; never render markings

Prompt:

Edit reference 1, the owner-selected portrait base, to create a reusable facial acting variant. Reference 2 owns canonical identity and reference 3 only measurement guides. Preserve the approved Milo canonical identity, lean grey felt anatomy, cream muzzle and belly boundaries, moss-green eyes, orange tail, canonical ears, eyes and paw construction. Short readable neck; no enlarged head, wide belly, shortened limbs or independently scaled body parts. Canonical upright projected head fraction 0.39 +/-0.01 applies only at comparable upright angle/support, never crouch or tumble. Use annotated visible-surface width, cream patch and paw references at comparable views, not hidden-joint guesses. Do not render annotations. Mouth closed, no teeth, no speech mouth. Genuine transparent alpha, neutral soft light, no background, ground plane, props, labels or shadows. Exactly one candidate; no variants. Keep reference 1 head silhouette, three-quarter forward-right head angle, head/ear/eye/muzzle sizes and positions, short neck, shoulder and upper-chest crop exactly compatible. Full ears and whiskers with clearance. Change only eyebrows, eyelids, gaze and restrained closed-muzzle crease to express: Stunned landing: asymmetric dazed eyelids, brows raised unevenly, unfocused startled eyeline and slack but closed muzzle. Do not enlarge skull or change iris/ear design to amplify emotion. This face asset will require local pitch/roll/view registration before use on ducked or falling bodies; do not rotate or distort the base in this request.

## Face application gate

Expressions are standalone full-head/upper-chest references. Binding one does not update body PNG pixels. Retained bodies must receive compatible local face guidance/edits in a later reviewed operation; preserve body geometry and verify head pitch/roll, skull/ears, gaze and closed mouth. Angle incompatibility needs a local view variant. No blind portrait overlay. The first seven images above are the bounded reference/repair pass, not a claim that all action faces have been integrated.

## Verification

Planning validation, planning readiness, derivation and gallery rebuild pass in `/Users/lealroja/miniconda3/envs/feltwillow/bin/python`. Full suite: 228 tests pass (exit 0); focused tests: 12 pass. `git diff --check` passes. Live gallery HTTP 200. All 113 pre-existing canonical/candidate PNGs, sidecars and generation receipts retain their hashes; see [VERIFICATION.json](VERIFICATION.json) and [unit-tests.log](unit-tests.log). No generation calls, Git staging, commits or pushes performed.

Commands: `production/audio_visual_plan.py --story lion_and_mouse_v7 validate`, `derive`, `readiness --gate planning`; `production/character_performance.py --story lion_and_mouse_v7 derive`; `production/performance_review_gallery.py --story lion_and_mouse_v7`; `-m unittest discover -s tests -q`, all run with the exact conda Python above. Image readiness remains blocked on ungenerated/unapproved expressions, the two body repairs, local face application/registration, anatomy/staging/contact review and the unresolved forward-pitch candidate.
