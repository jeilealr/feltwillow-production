# Milo width-aware revisions — proposed operation

**Prepared only; no requests submitted or authorization inferred.** Endpoint `image_gen.imagegen`; 22 requests, one per current reusable pose/portrait, no automatic retries. Transparent background; model/seed managed by the built-in tool and not exposed. Current pricing and total cost are unknown.

Operation SHA-256: `d39a08b2342aa26de2616455cc7011d5911f7e41e04f511acba805c0a3e51deb`

Scope: 18 Milo body poses and four portrait bases. Preserve all existing images/receipts and exact approvals as history; new outputs begin pending review. This does not regenerate the story scene compositions.

The three ordered references are the canonical identity, its width annotation (measurement scope only), and the previous candidate (acting only). Exact files/hashes and full prompts follow. Width baselines are projected observations with uncertainty, not automatic geometric enforcement.

## 1. milo.walk.screen_right.lightstep.3q:contact

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_screen_right_lightstep_3q_contact_r005_candidate.png`

Audio-linked uses: S01-L001-B01-I01, S01-L002-B03-I01, S01-L003-B01-I01

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_screen_right_lightstep_3q_contact_r004_candidate.png | b95682a1c53d3f5f1fad7e4dee2823dddb414229c2e3905d63e597703549f81f |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Light exploratory walk toward screen-right, three-quarter view; key contact. Output complete full-body cutout with readable torso and all limbs, feet and tail. The gait key must be visibly distinct: leading foot contacts the ground plane; coherent opposite arm swing.
```

## 2. milo.walk.screen_right.lightstep.3q:passing_step

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_screen_right_lightstep_3q_passing_step_r004_candidate.png`

Audio-linked uses: S01-L001-B01-I02, S01-L002-B03-I02, S01-L003-B01-I02

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_screen_right_lightstep_3q_passing_step_r003_candidate.png | 11db4427a0b03fc805446cf7b315b2a1d6ed3c3e8bd9852dd4897cc9718ae75d |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Light exploratory walk toward screen-right, three-quarter view; key passing_step. Output complete full-body cutout with readable torso and all limbs, feet and tail. The gait key must be visibly distinct: weight on supporting leg; other foot lifts/passes under hips rather than an extended contact stamp.
```

## 3. milo.walk.screen_right.lightstep.3q:opposite_contact

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_screen_right_lightstep_3q_opposite_contact_r004_candidate.png`

Audio-linked uses: portrait-base dependency; no direct scene assignment

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_screen_right_lightstep_3q_opposite_contact_r003_candidate.png | 965ccce86bf77a1505a3f31b4a95d12dc4ac437a2ac04267a5da05ef377ef25a |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Light exploratory walk toward screen-right, three-quarter view; key opposite_contact. Output complete full-body cutout with readable torso and all limbs, feet and tail. The gait key must be visibly distinct: reverse the contact/support and arm swing relative to contact, while body still faces and travels screen-right.
```

## 4. milo.decision.stationary.3q:forward

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_forward_r003_candidate.png`

Audio-linked uses: S03-L001-B01-I01, S03-L001-B01-I02, S03-L002-B01-I01, S03-L002-B01-I02, S03-L003-B01-I01, S03-L003-B01-I02, S03-L004-B01-I01, S03-L004-B01-I02, S03-L005-B01-I01, S03-L005-B01-I02, S03-L006-B01-I01

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_forward_r002_candidate.png | 34c8265428766c72cfd23556781ac703012e978667e8f4a001ddf4bbbedda327 |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Stationary fork consideration; feet/root fixed, head angle variants reviewed; key forward. Output complete full-body cutout with readable torso and all limbs, feet and tail. Keep a stationary screen-right three-quarter torso, identical body orientation and planted support configuration across the family. Only compatible head/gaze changes; no mirroring, full-body rotation, stepping or walking. Look ahead toward screen-right.
```

## 5. milo.decision.stationary.3q:sky

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_sky_r003_candidate.png`

Audio-linked uses: S03-L006-B01-I02, S03-L007-B01-I01

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_sky_r002_candidate.png | a2a78a92988579e6b22d6c07020094cde27de4c7d5428192fa4feb0be6c47aaf |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Stationary fork consideration; feet/root fixed, head angle variants reviewed; key sky. Output complete full-body cutout with readable torso and all limbs, feet and tail. Keep a stationary screen-right three-quarter torso, identical body orientation and planted support configuration across the family. Only compatible head/gaze changes; no mirroring, full-body rotation, stepping or walking. Look upward toward the sky.
```

## 6. milo.decision.stationary.3q:long_path

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_long_path_r003_candidate.png`

Audio-linked uses: S03-L007-B01-I02, S03-L008-B01-I01

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_long_path_r002_candidate.png | ec6cb81a39369c569131a201044d9158612d6d89032d2b40deb271c56b3c0c85 |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Stationary fork consideration; feet/root fixed, head angle variants reviewed; key long_path. Output complete full-body cutout with readable torso and all limbs, feet and tail. Keep a stationary screen-right three-quarter torso, identical body orientation and planted support configuration across the family. Only compatible head/gaze changes; no mirroring, full-body rotation, stepping or walking. Turn only head/gaze toward the long path at screen-left while torso, feet and tail remain the same screen-right-facing body; previous candidate wrongly turned the whole body.
```

## 7. milo.decision.stationary.3q:shortcut

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_shortcut_r003_candidate.png`

Audio-linked uses: S03-L008-B01-I02

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_shortcut_r002_candidate.png | 13f86e259ebc58caa37a8456b73a004ae757aaf929a72b0a1e7f8731a7441688 |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Stationary fork consideration; feet/root fixed, head angle variants reviewed; key shortcut. Output complete full-body cutout with readable torso and all limbs, feet and tail. Keep a stationary screen-right three-quarter torso, identical body orientation and planted support configuration across the family. Only compatible head/gaze changes; no mirroring, full-body rotation, stepping or walking. Look toward the shortcut at screen-right; same planted body.
```

## 8. milo.portrait.base.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r003_candidate.png`

Audio-linked uses: S02-L003-B01-I01, S03-L009-B01-I01, S03-L010-B01-I01, S05-L007-B01-I01, S06-L003-B01-I01, S06-L004-B01-I01, S06-L005-B01-I01, S07-L003-B01-I01, S07-L004-B01-I01, S07-L005-B01-I01, S08-L002-B01-I01, S08-L012-B01-I01, S08-L016-B01-I01, S08-L017-B01-I01, S08-L019-B01-I01, S08-L020-B01-I01, S08-L021-B01-I01, S12-L002-B01-I01, S12-L003-B01-I01

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r002_candidate.png | e38179fd7f12ae5c70666910396a99da5fc5b9b70335e11070302cf4cf0d7d67 |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Full ears/mane and upper chest; stable angle-specific portrait geometry; key default. Output portrait framing, not a full-body image; retain the requested head view without clipping ears or whiskers.
```

## 9. milo.inspect.log.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_log_3q_r004_candidate.png`

Audio-linked uses: S01-L002-B02-I01

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_log_3q_r003_candidate.png | 9fab395ff98fa06bcd3385f5e7cc0079010f43fbaddf5a7a2e6861398de18cfb |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Lean toward hollow-log opening, hands grounded on rim; key default. Output complete full-body cutout with readable torso and all limbs, feet and tail.
```

## 10. milo.forage.seeds.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_forage_seeds_3q_r006_candidate.png`

Audio-linked uses: S01-L004-B01-I01, S01-L004-B01-I02

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_forage_seeds_3q_r005_candidate.png | 31bcbab68c60c9149279fcfcb4489c2536204bb3eb6b607447f2d900261181b6 |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Low crouch picking seeds; retain compact torso and hand contact; key default. Output complete full-body cutout with readable torso and all limbs, feet and tail.
```

## 11. milo.acorn.pick_hold.3q:approach

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_pick_hold_3q_approach_r003_candidate.png`

Audio-linked uses: S01-L004-B03-I01

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_pick_hold_3q_approach_r002_candidate.png | a2fffcf578a6d8d93956d39311fa35ac92bdba6f5a74fdfd97266859a6f3854b |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Approach, pick up and savor acorn with closed mouth; key approach. Output complete full-body cutout with readable torso and all limbs, feet and tail. Preserve exact action phase; empty hands are planned contact space, not proof of prop fit. Do not generate an acorn or enlarge hands/belly to accommodate one.
```

## 12. milo.acorn.pick_hold.3q:hold

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_pick_hold_3q_hold_r003_candidate.png`

Audio-linked uses: S01-L004-B03-I02

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_pick_hold_3q_hold_r002_candidate.png | ecb89dc02841cf97b3850082005bdf7ec4d958c2a1d23c35e09723bed6409245 |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Approach, pick up and savor acorn with closed mouth; key hold. Output complete full-body cutout with readable torso and all limbs, feet and tail. Preserve exact action phase; empty hands are planned contact space, not proof of prop fit. Do not generate an acorn or enlarge hands/belly to accommodate one.
```

## 13. milo.acorn.pick_hold.3q:savor

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_pick_hold_3q_savor_r003_candidate.png`

Audio-linked uses: S01-L004-B03-I03

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_pick_hold_3q_savor_r002_candidate.png | d49ee9246d9eb8538c8236a550207cce6ed6bd1a6e909514a953d2772cc24d73 |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Approach, pick up and savor acorn with closed mouth; key savor. Output complete full-body cutout with readable torso and all limbs, feet and tail. Preserve exact action phase; empty hands are planned contact space, not proof of prop fit. Do not generate an acorn or enlarge hands/belly to accommodate one.
```

## 14. milo.acorn.hold.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_hold_3q_r003_candidate.png`

Audio-linked uses: S02-L001-B01-I01, S02-L001-B01-I02, S02-L004-B01-I01, S02-L004-B01-I02

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_hold_3q_r002_candidate.png | 023d70033c2892a383d5bd926d9cf9215bea04647d01e8c974ee74d409b5f70f |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Stand holding the single acorn; support and grip preserved; key default. Output complete full-body cutout with readable torso and all limbs, feet and tail. Preserve exact action phase; empty hands are planned contact space, not proof of prop fit. Do not generate an acorn or enlarge hands/belly to accommodate one.
```

## 15. milo.acorn.place.3q:hold

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_place_3q_hold_r003_candidate.png`

Audio-linked uses: S02-L004-B02-I01

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_place_3q_hold_r002_candidate.png | 538c0b7806d643251202f5ead08737d0feea9ff2fa030bba593f1b746511f6c8 |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Lower acorn beside stream stone, ground contact then release; key hold. Output complete full-body cutout with readable torso and all limbs, feet and tail. Preserve exact action phase; empty hands are planned contact space, not proof of prop fit. Do not generate an acorn or enlarge hands/belly to accommodate one.
```

## 16. milo.acorn.place.3q:lower

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_place_3q_lower_r003_candidate.png`

Audio-linked uses: S02-L004-B02-I02

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_place_3q_lower_r002_candidate.png | 81d59172f0dc2b1403f7dc143288e5eb425fb3432540608d6cc85c699c0911ed |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Lower acorn beside stream stone, ground contact then release; key lower. Output complete full-body cutout with readable torso and all limbs, feet and tail. Preserve exact action phase; empty hands are planned contact space, not proof of prop fit. Do not generate an acorn or enlarge hands/belly to accommodate one.
```

## 17. milo.acorn.place.3q:released

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_place_3q_released_r003_candidate.png`

Audio-linked uses: S02-L004-B02-I03

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_place_3q_released_r002_candidate.png | 586be272e532ca8315e88ca222462cf915b25a7aea69c7b437e93539847322dd |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Lower acorn beside stream stone, ground contact then release; key released. Output complete full-body cutout with readable torso and all limbs, feet and tail. Preserve exact action phase; empty hands are planned contact space, not proof of prop fit. Do not generate an acorn or enlarge hands/belly to accommodate one.
```

## 18. milo.inspect.berry_thicket.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r003_candidate.png`

Audio-linked uses: S01-L002-B01-I01

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r002_candidate.png | 8b6571479f2f8dab54624d4d4e7059d762a26f434acf7c961795ce7da6205762 |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Reach and inspect berries with a clear supporting foot and paw/branch contact; key default. Output complete full-body cutout with readable torso and all limbs, feet and tail.
```

## 19. milo.harvest.berries.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_harvest_berries_3q_r003_candidate.png`

Audio-linked uses: S01-L004-B02-I01

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/poses/milo_harvest_berries_3q_r002_candidate.png | 9888012c9cd01f37dd2c11ad0f5cbb17eace950a1549bbd4cd82bdb748328fdd |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Harvest berries beside stream with a separate holding hand; no thicket-pose assumption; key default. Output complete full-body cutout with readable torso and all limbs, feet and tail.
```

## 20. milo.portrait.base.3q.look_up:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_look_up_r003_candidate.png`

Audio-linked uses: portrait-base dependency; no direct scene assignment

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_look_up_r002_candidate.png | 78c6e3ab12e258d71c9d81319325bc6966004651a008be49ceb7806d42e685a1 |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Angle-specific portrait base looking up; key default. Output portrait framing, not a full-body image; retain the requested head view without clipping ears or whiskers.
```

## 21. milo.portrait.base.3q.look_left:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_look_left_r003_candidate.png`

Audio-linked uses: portrait-base dependency; no direct scene assignment

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_look_left_r002_candidate.png | 6ef303854efb62bf5b060865b40b45691682f82ae8f72a5c990e5137b1fceab4 |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Angle-specific portrait base looking left; key default. Output portrait framing, not a full-body image; retain the requested head view without clipping ears or whiskers.
```

## 22. milo.portrait.base.3q.look_right:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_look_right_r003_candidate.png`

Audio-linked uses: portrait-base dependency; no direct scene assignment

| Role | Source | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| canonical_width_annotation | stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg | 614c82ea60cdcaebd5b80bd9a40f3733c8e741f25c523fe4e2117f9ca0d347c5 |
| previous_pose_candidate | character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_look_right_r002_candidate.png | 28ddb1eda67e330313cb293155edff43253e8cc9a04e40f0192acc5a711f916d |

Exact prompt:

```text
Create exactly one revised reusable Milo performance candidate on real transparent alpha. Reference 1 is the unchanged approved canonical and controls identity, anatomy, grey felt, cream muzzle/chest/belly material, green eyes, charcoal nose and orange tail. Reference 2 is an ANNOTATED DERIVATIVE of that same canonical: its W lines show visible width stations only; it is measurement guidance, not a new design or artwork to copy. Do not render its grey backing, colored lines, numbers or labels. Reference 3 is the previous performance candidate: retain ONLY the requested action/head direction after correcting the explicit issues below; it has no anatomy or approval authority.

Match the canonical lean torso, restrained belly projection, short readable neck, shoulder/hip transition, thigh thickness and cream-patch coverage. Do not preserve a rounder belly or shorter torso merely because reference 3 has one. Both vertical AND horizontal construction matter. The owner-requested upright crown-to-chin / crown-to-supporting-sole target stays 0.39 +/-0.01, excluding ears, ONLY with compatible upright pose/head pitch. Do not force this onto crouches, rolls, bowed/tilted heads or portrait crops. Canonical head/torso surface-axis baseline is approximately 1.06.

At canonical-compatible yaw/lean, approximate measured visible WIDTH references are: upper torso panel / head width 0.44, mid-belly panel / head width 0.53, lower belly panel / head width 0.49; mid-belly panel / torso surface height 0.62; lower-body pelvis band / head width 0.74; near thigh section / head width 0.29; near hanging arm section / head width 0.20. These are partial visible SURFACE spans, not full torso circumference, skeletal hip width or hidden back outlines. Torso panel widths EXCLUDE arms, hands, props and tail. Upper/mid/lower stations occur near 0.23/0.51/0.80 of neck-base-to-pelvis surface height; re-find equivalent local stations, never copy canonical pixel rows. The light cream material patch is separate: its upper/mid/lower widths are roughly 0.61/0.61/0.63 of their visible torso panels; mid-patch width / visible patch height is about 0.36. Keep the same patch shape and coverage instead of widening it to fill a rounder belly. New width values are approximate observational guides with annotation uncertainty; no invented universal numerical tolerance or hidden-joint target. If the requested projection obscures a width, preserve the canonical local anatomy without inventing a measurable pass.

For the head, use angle-compatible canonical ear/head, eye/head and eye-spacing construction. Approximate neutral near/far ear-to-head-width baselines 0.81/0.66, near/far eye-width-to-head 0.24/0.09, eye spacing/head 0.44 apply only at matching yaw/pitch and neutral eyelids. A portrait uses these local ratios; it does not have a measurable head-to-whole-body fraction or belly width. Bend arms/legs through coherent articulations without changing thickness or segment construction. Foreshortening must read as perspective rather than inflated anatomy. Keep mouth closed and no visible teeth; no arbitrary speech-mouth or facial overlay. Neutral soft studio lighting, no scenery, ground, contact shadow, prop, lettering or watermark. Do not crop ears, fingertips, feet or whiskers. Body images include entire tail; portrait images retain full head/ears, neck, shoulders and upper chest with comfortable margins.

Paw/hand guidance: preserve canonical rounded felt toes and restrained hand/foot bulk. Near closed-hand/head span is approximately 0.22, far closed hand/head 0.16; near front-view supporting foot/head span 0.38 and far more side-on heel-to-toe foot/head span 0.51. These projections are deliberately different, not a demand for unequal anatomy. Compare only the same side, orientation, wrist/ankle articulation and load. Closed hands do not establish open palm or acorn grip capacity. Keep full toe silhouettes without extra digits or visible teeth.
Requested action: Angle-specific portrait base looking right; key default. Output portrait framing, not a full-body image; retain the requested head view without clipping ears or whiskers.
```

