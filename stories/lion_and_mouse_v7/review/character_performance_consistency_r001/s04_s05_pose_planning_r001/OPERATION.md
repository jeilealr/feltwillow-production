# S04–S05 Milo pose proposal — 16 requests, not submitted

Endpoint `image_gen.imagegen`; one transparent candidate per request; **16 requests, no retries, cost unknown**. No Leo/background/scene/audio/video generation. Operation SHA-256 `3500e5beb19bc63e3ac255a488cc97108dc324ac2fd5bf67a54bf198f2597410`.

## Exact shared input references

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- canonical_measurement_annotation: `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg` · `614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5`
- reviewed_walking_anatomy_reference: `character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_screen_right_lightstep_3q_contact_r005_candidate.png` · `0aa6e06a2df69af19bcfe77c68c11ec79956337ec0f0560df2944629d32bc5e2`

## Common exact prompt

```text
Create exactly ONE reusable Milo performance candidate on genuine transparent alpha. Reference 1 is the unchanged approved Milo canonical and controls identity, anatomy, felt materials and palette. Reference 2 is its annotated measurement derivative: use its visible-surface guides only; do not render lines, numbers, labels or its background. Reference 3 is the owner-selected walking/contact depiction and clarifies lean head/body/leg balance only, not the requested action. Render the new requested action rather than copying the walk.

Preserve compact but lean grey felt mouse, moss-green eyes, cream muzzle/chest patch, short readable neck, rounded felt feet/closed hands and orange tail. No visible teeth, mouth closed. Do not inflate the head, shorten torso, widen belly or spread the cream patch. At compatible upright pitch/support ONLY, crown-to-chin (excluding ears) / crown-to-supporting sole target is 0.39 +/-0.01. Never force it on running flexion, crouch, airborne tumble, roll or tilted head. Articulation changes projection, not limb lengths/thickness. Canonical visible head/torso axis baseline is about 1.06. At compatible yaw/lean, upper/mid/lower torso-panel widths / head width are about 0.44/0.53/0.49; belly panel / torso height 0.62, pelvis-band/head 0.74, near thigh/head 0.29, near arm/head 0.20. Exclude arms/tail from torso widths. Cream patch at upper/mid/lower stations is about 0.61/0.61/0.63 of the corresponding visible torso panel. These are uncertain visible-surface reference baselines, not hidden skeleton or universal tolerances. Preserve near/far ear and eye construction at compatible head angle; do not independently rescale body parts. Keep paw/hand bulk and toe construction canonical, without extra digits.

Show the entire character including ears, whiskers, toes and full tail with margins. Soft neutral studio light and genuine transparent background, no scenery, ground plane, contact shadow, props, Leo, labels, watermark or graphic symbols. Ground/contact directions can be implied by anatomy, without drawing support objects. Species-specific contact/grip and final scene perspective remain a later staging review. A cutout alone does not certify anatomy or physical contact.

```

## 1 · milo.run.rescue.3q:contact

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_run_rescue_contact_3q_r001_candidate.png`

Uses: S04-L001-B01-I01, S04-L002-B01-I01, S04-L005-B01-I01

Exact prompt suffix:

```text
Requested key: Forward urgent but light three-quarter screen-right running step; one foot planted with believable heel/toe support, opposite leg lifted and coherent arm counter-swing. Intent on getting home; do not add rescue props.
```

## 2 · milo.run.rescue.3q:passing_step

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_run_rescue_passing_step_3q_r001_candidate.png`

Uses: S04-L001-B01-I02, S04-L002-B01-I02, S04-L005-B01-I02

Exact prompt suffix:

```text
Requested key: Distinct three-quarter screen-right passing/lift phase of the same run: supporting leg under pelvis, opposite knee passing forward, coherent opposite arm swing. Not the contact pose repeated.
```

## 3 · milo.run.duck.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_run_duck_default_3q_r001_candidate.png`

Uses: S04-L003-B01-I01

Exact prompt suffix:

```text
Requested key: Run-duck entry under an imagined low branch: bend knees/hips and angle torso/head below clearance, maintain short neck and coherent limbs, one load-bearing foot. No branch shown; no crushed torso.
```

## 4 · milo.run.duck.3q:clear

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_run_duck_clear_3q_r001_candidate.png`

Uses: S04-L003-B01-I02

Exact prompt suffix:

```text
Requested key: Run-duck exit: clear the imagined branch and begin rising through hips/knees into the next grounded forward step. Distinct from low duck entry, same proportions.
```

## 5 · milo.run.turn_stump.3q:turn_entry

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_run_turn_stump_turn_entry_3q_r001_candidate.png`

Uses: S04-L004-B01-I01

Exact prompt suffix:

```text
Requested key: Enter a curved path around an imagined stump: screen-right three-quarter body, slight inward lean and outside foot supporting the turn, coherent curved travel and counterbalancing arms. No stump.
```

## 6 · milo.run.turn_stump.3q:turn_exit

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_run_turn_stump_turn_exit_3q_r001_candidate.png`

Uses: S04-L004-B01-I02

Exact prompt suffix:

```text
Requested key: Exit that grounded curve: shoulders and pelvis unwind toward screen-right, next foot plants forward, natural arm swing; keep anatomy unchanged, no stump.
```

## 7 · milo.approach.rear_paw.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_approach_rear_paw_default_3q_r001_candidate.png`

Uses: S05-L005-B01-I01

Exact prompt suffix:

```text
Requested key: Round an imagined tree root at a hurried but grounded step, moving screen-left to screen-right. Focus ahead, unaware of the paw; clear full-body silhouette and restrained lean.
```

## 8 · milo.approach.rear_paw.3q:near_paw

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_approach_rear_paw_near_paw_3q_r001_candidate.png`

Uses: S05-L005-B01-I02, S05-L006-B01-I01

Exact prompt suffix:

```text
Requested key: Next grounded hurried step after the root, close to an imagined low rear-paw obstacle; foot not yet caught, anatomy consistent, no jumping or premature airborne fall.
```

## 9 · milo.trip.rear_paw.3q:approach

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_trip_rear_paw_approach_3q_r001_candidate.png`

Uses: S05-L007-B01-I01, S05-L008-B01-I01

Exact prompt suffix:

```text
Requested key: Grounded startled anticipation before catching a low obstacle: full-body screen-right, eyes widen slightly, short neck visible, hands start counterbalancing, no open mouth. Do not lift off yet.
```

## 10 · milo.trip.rear_paw.3q:paw_contact

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_trip_rear_paw_paw_contact_3q_r001_candidate.png`

Uses: S05-L008-B01-I02

Exact prompt suffix:

```text
Requested key: Leading foot catches an imagined low rear-paw obstacle, body begins to lose balance and arms react. One foot remains caught/loaded; not airborne yet. No lion/obstacle drawn.
```

## 11 · milo.trip.rear_paw.3q:forward_pitch

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_trip_rear_paw_forward_pitch_3q_r001_candidate.png`

Uses: S05-L008-B01-I03

Exact prompt suffix:

```text
Requested key: Next trip key: torso pitches farther forward over the caught foot, trailing foot unloads, arms extend to counterbalance. Preserve limb construction and neck; supporting contact still at imagined paw.
```

## 12 · milo.trip.rear_paw.3q:trip

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_trip_rear_paw_trip_3q_r001_candidate.png`

Uses: S05-L008-B01-I04

Exact prompt suffix:

```text
Requested key: Final unbalanced tipping key just before support is lost: weight projects past the caught front foot, arms attempt recovery, trailing leg releases. Preserve remaining paw-contact support; airborne motion belongs to next family.
```

## 13 · milo.tumble.flank_to_face.3q:support_lost

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_tumble_flank_to_face_support_lost_3q_r001_candidate.png`

Uses: S05-L009-B01-I01

Exact prompt suffix:

```text
Requested key: First fully airborne key after the rear-paw trip: both feet lose support, body tips forward and arms reach to recover, with coherent rotation toward screen-right. No planted support or ground shadow.
```

## 14 · milo.tumble.flank_to_face.3q:tumble

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_tumble_flank_to_face_tumble_3q_r001_candidate.png`

Uses: S05-L009-B01-I02

Exact prompt suffix:

```text
Requested key: A distinct forward airborne tumble key: rotate the same body farther, knees/hips flex naturally with counterbalancing tail. Keep recognizable head, ears, neck and torso; no compressed anatomy or cloned limbs.
```

## 15 · milo.tumble.flank_to_face.3q:roll

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_tumble_flank_to_face_roll_3q_r001_candidate.png`

Uses: S05-L009-B01-I03

Exact prompt suffix:

```text
Requested key: Ground-rolling key after the tumble: tuck into a coherent side/shoulder roll heading screen-right, back/shoulder is intended contact, feet are not standing. Keep full head/ears/tail readable; do not squeeze anatomy to upright ratios.
```

## 16 · milo.tumble.flank_to_face.3q:nose_landing

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_tumble_flank_to_face_nose_landing_3q_r001_candidate.png`

Uses: S05-L009-B01-I04

Exact prompt suffix:

```text
Requested key: Surprised landed/recovery pose against an imagined large lion nose at screen-right: Milo remains on the ground, front hands/body gently brace toward the nose, hind body supported. No nose/Leo drawn; exact contact clearance will be staged after Leo sleeping setup is reviewed. No suspension or character resizing.
```

