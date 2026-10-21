# Opening correction image operation

Endpoint `image_gen.imagegen`; 11 requests, one candidate each, opaque 16:9, model/seed tool-managed, no retries; cost unknown. Operation SHA-256 `cd799b0ab407f8360fa3baf3f79a07cefc2692e8c3c8d404bd59f96fe2e14207`.

L006 fork anchor and L010 portrait reference stay intact. Exact-pixel/root consistency remains subject to audit; no technical pass promised.

## 1. S01-L004-B01-I01

character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B01-I01_single_tall_grass_seed_patch_r003_candidate.png

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- edit_base: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B01-I01_single_tall_grass_seed_patch_r002_candidate.png` · `6ae9239924877f4d61588a526d42a1c0828358e223679c9cc248c5a44bc3c966`
- later_reaching_pose_contrast_only: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B01-I02_single_tall_grass_seed_patch_r002_candidate.png` · `c0fc399b05229cc5c1ba91acd616cbd3050082dce66a829409bf0b98ee57fe40`

```text
Use case: identity-preserve, Feltwillow narrative scene edit. Return ONE complete 16:9 landscape image. Reference 1 supplies approved Milo identity/anatomy/material. Reference 2 is the edit target and camera/background/scale anchor. Change Milo to the clearly earlier phase: mostly upright with an easy, slight head-down look at seeds on the ground, both hands held away from seeds. He has just noticed them and has not bent to pick any. Make a clear visible pose/action contrast to the deep reaching crouch of I02, while preserving this exact grass/seed-patch background, camera, subject depth and scale. Seeds remain on ground; no acorn.
Audience hears: There had been so many wonderful things to eat — tiny seeds beneath the tall grass, sweet berries beside the stream, and one particularly delicious acorn that took much longer to enjoy than expected.
Preserve grey felt, cream muzzle and narrow elongated chest/belly inset, orange tail, green eyes and short readable neck. Lean canonical body; no independently enlarged head, inflated abdomen or short torso. Applicable comparable upright projected head fraction is 0.39 +/-0.01; bent/pitched/portrait views require local comparable proportions, not that global fraction. Preserve horizontal torso/paw/cream-patch proportions too. No visible teeth. Mouth closed in this still; narration never drives mouth, dialogue uses later lip-sync. No new animals, text, corner symbols, watermark, labels or measurement marks. Match scene light, support contacts/shadows and occlusion. Do not resize parts independently. Return a candidate only; generation guidance does not certify measured anatomy or exact pixels. Reference 3 supplies only the specifically labeled supporting pose/comparison role; it must not change the reference-2 setup or camera.
```

## 2. S03-L001-B01-I02

character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L001-B01-I02_end_homeward_distance_r003_candidate.png

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- edit_base_and_setup_anchor: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L006-B01-I02_end_decision_locked_background_r001_candidate.png` · `7842d9c8a4c2f67848fb38195d11544e985f414a61e6a8f0a4658208bd80fb68`

```text
Use case: identity-preserve, Feltwillow narrative scene edit. Return ONE complete 16:9 landscape image. Reference 1 supplies approved Milo identity/anatomy/material. Reference 2 is the edit target and camera/background/scale anchor. Make a tightly scoped performance edit to reference 2 (S03-L006 anchor): Milo pauses and looks ahead at the fork, hands relaxed; no hand-to-chin requirement. Keep the original complete background unchanged: fork paths, stone, trees, sky, shadows, lens/crop and framing. Keep Milo at EXACTLY the same foot/root position and standing depth as reference 2, both feet grounded on the SAME ground contact pixels, same apparent body and head scale. No walking, travelling, sliding or independent resizing. Keep torso orientation, leg spacing, tail attachment and actor construction from the anchor; change only head/eyes and minimal local acting. Preserve LEFT safe sunny meadow and RIGHT dark shortcut. Empty hands; acorn remains behind on stream stone offscreen.
Audience hears: Home was still quite a distance away.
Preserve grey felt, cream muzzle and narrow elongated chest/belly inset, orange tail, green eyes and short readable neck. Lean canonical body; no independently enlarged head, inflated abdomen or short torso. Applicable comparable upright projected head fraction is 0.39 +/-0.01; bent/pitched/portrait views require local comparable proportions, not that global fraction. Preserve horizontal torso/paw/cream-patch proportions too. No visible teeth. Mouth closed in this still; narration never drives mouth, dialogue uses later lip-sync. No new animals, text, corner symbols, watermark, labels or measurement marks. Match scene light, support contacts/shadows and occlusion. Do not resize parts independently. Return a candidate only; generation guidance does not certify measured anatomy or exact pixels.
```

## 3. S03-L002-B01-I02

character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L002-B01-I02_end_two_routes_r003_candidate.png

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- edit_base_and_setup_anchor: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L006-B01-I02_end_decision_locked_background_r001_candidate.png` · `7842d9c8a4c2f67848fb38195d11544e985f414a61e6a8f0a4658208bd80fb68`

```text
Use case: identity-preserve, Feltwillow narrative scene edit. Return ONE complete 16:9 landscape image. Reference 1 supplies approved Milo identity/anatomy/material. Reference 2 is the edit target and camera/background/scale anchor. Make a tightly scoped performance edit to reference 2 (S03-L006 anchor): Milo considers the two routes with a thoughtful forward gaze. Keep the original complete background unchanged: fork paths, stone, trees, sky, shadows, lens/crop and framing. Keep Milo at EXACTLY the same foot/root position and standing depth as reference 2, both feet grounded on the SAME ground contact pixels, same apparent body and head scale. No walking, travelling, sliding or independent resizing. Keep torso orientation, leg spacing, tail attachment and actor construction from the anchor; change only head/eyes and minimal local acting. Preserve LEFT safe sunny meadow and RIGHT dark shortcut. Empty hands; acorn remains behind on stream stone offscreen.
Audience hears: There were two ways to get there.
Preserve grey felt, cream muzzle and narrow elongated chest/belly inset, orange tail, green eyes and short readable neck. Lean canonical body; no independently enlarged head, inflated abdomen or short torso. Applicable comparable upright projected head fraction is 0.39 +/-0.01; bent/pitched/portrait views require local comparable proportions, not that global fraction. Preserve horizontal torso/paw/cream-patch proportions too. No visible teeth. Mouth closed in this still; narration never drives mouth, dialogue uses later lip-sync. No new animals, text, corner symbols, watermark, labels or measurement marks. Match scene light, support contacts/shadows and occlusion. Do not resize parts independently. Return a candidate only; generation guidance does not certify measured anatomy or exact pixels.
```

## 4. S03-L003-B01-I02

character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L003-B01-I02_end_safe_left_meadow_r003_candidate.png

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- edit_base_and_setup_anchor: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L006-B01-I02_end_decision_locked_background_r001_candidate.png` · `7842d9c8a4c2f67848fb38195d11544e985f414a61e6a8f0a4658208bd80fb68`

```text
Use case: identity-preserve, Feltwillow narrative scene edit. Return ONE complete 16:9 landscape image. Reference 1 supplies approved Milo identity/anatomy/material. Reference 2 is the edit target and camera/background/scale anchor. Make a tightly scoped performance edit to reference 2 (S03-L006 anchor): Turn only the head/gaze toward the long LEFT meadow path, keeping body and feet planted. Keep the original complete background unchanged: fork paths, stone, trees, sky, shadows, lens/crop and framing. Keep Milo at EXACTLY the same foot/root position and standing depth as reference 2, both feet grounded on the SAME ground contact pixels, same apparent body and head scale. No walking, travelling, sliding or independent resizing. Keep torso orientation, leg spacing, tail attachment and actor construction from the anchor; change only head/eyes and minimal local acting. Preserve LEFT safe sunny meadow and RIGHT dark shortcut. Empty hands; acorn remains behind on stream stone offscreen.
Audience hears: One was the familiar path that curved safely around a sunny meadow.
Preserve grey felt, cream muzzle and narrow elongated chest/belly inset, orange tail, green eyes and short readable neck. Lean canonical body; no independently enlarged head, inflated abdomen or short torso. Applicable comparable upright projected head fraction is 0.39 +/-0.01; bent/pitched/portrait views require local comparable proportions, not that global fraction. Preserve horizontal torso/paw/cream-patch proportions too. No visible teeth. Mouth closed in this still; narration never drives mouth, dialogue uses later lip-sync. No new animals, text, corner symbols, watermark, labels or measurement marks. Match scene light, support contacts/shadows and occlusion. Do not resize parts independently. Return a candidate only; generation guidance does not certify measured anatomy or exact pixels.
```

## 5. S03-L004-B01-I02

character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L004-B01-I02_end_short_right_route_r003_candidate.png

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- edit_base_and_setup_anchor: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L006-B01-I02_end_decision_locked_background_r001_candidate.png` · `7842d9c8a4c2f67848fb38195d11544e985f414a61e6a8f0a4658208bd80fb68`

```text
Use case: identity-preserve, Feltwillow narrative scene edit. Return ONE complete 16:9 landscape image. Reference 1 supplies approved Milo identity/anatomy/material. Reference 2 is the edit target and camera/background/scale anchor. Make a tightly scoped performance edit to reference 2 (S03-L006 anchor): Turn only head/gaze toward the short RIGHT forest path. Do not step toward or enter it. Keep the original complete background unchanged: fork paths, stone, trees, sky, shadows, lens/crop and framing. Keep Milo at EXACTLY the same foot/root position and standing depth as reference 2, both feet grounded on the SAME ground contact pixels, same apparent body and head scale. No walking, travelling, sliding or independent resizing. Keep torso orientation, leg spacing, tail attachment and actor construction from the anchor; change only head/eyes and minimal local acting. Preserve LEFT safe sunny meadow and RIGHT dark shortcut. Empty hands; acorn remains behind on stream stone offscreen.
Audience hears: The other was much shorter.
Preserve grey felt, cream muzzle and narrow elongated chest/belly inset, orange tail, green eyes and short readable neck. Lean canonical body; no independently enlarged head, inflated abdomen or short torso. Applicable comparable upright projected head fraction is 0.39 +/-0.01; bent/pitched/portrait views require local comparable proportions, not that global fraction. Preserve horizontal torso/paw/cream-patch proportions too. No visible teeth. Mouth closed in this still; narration never drives mouth, dialogue uses later lip-sync. No new animals, text, corner symbols, watermark, labels or measurement marks. Match scene light, support contacts/shadows and occlusion. Do not resize parts independently. Return a candidate only; generation guidance does not certify measured anatomy or exact pixels.
```

## 6. S03-L005-B01-I02

character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L005-B01-I02_end_shortcut_entrance_r003_candidate.png

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- edit_base_and_setup_anchor: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L006-B01-I02_end_decision_locked_background_r001_candidate.png` · `7842d9c8a4c2f67848fb38195d11544e985f414a61e6a8f0a4658208bd80fb68`

```text
Use case: identity-preserve, Feltwillow narrative scene edit. Return ONE complete 16:9 landscape image. Reference 1 supplies approved Milo identity/anatomy/material. Reference 2 is the edit target and camera/background/scale anchor. Make a tightly scoped performance edit to reference 2 (S03-L006 anchor): Milo studies the quiet RIGHT shortcut with mild concern. No step into it. Keep the original complete background unchanged: fork paths, stone, trees, sky, shadows, lens/crop and framing. Keep Milo at EXACTLY the same foot/root position and standing depth as reference 2, both feet grounded on the SAME ground contact pixels, same apparent body and head scale. No walking, travelling, sliding or independent resizing. Keep torso orientation, leg spacing, tail attachment and actor construction from the anchor; change only head/eyes and minimal local acting. Preserve LEFT safe sunny meadow and RIGHT dark shortcut. Empty hands; acorn remains behind on stream stone offscreen.
Audience hears: It cut straight through a quiet part of the forest that the mouse rarely visited.
Preserve grey felt, cream muzzle and narrow elongated chest/belly inset, orange tail, green eyes and short readable neck. Lean canonical body; no independently enlarged head, inflated abdomen or short torso. Applicable comparable upright projected head fraction is 0.39 +/-0.01; bent/pitched/portrait views require local comparable proportions, not that global fraction. Preserve horizontal torso/paw/cream-patch proportions too. No visible teeth. Mouth closed in this still; narration never drives mouth, dialogue uses later lip-sync. No new animals, text, corner symbols, watermark, labels or measurement marks. Match scene light, support contacts/shadows and occlusion. Do not resize parts independently. Return a candidate only; generation guidance does not certify measured anatomy or exact pixels.
```

## 7. S03-L007-B01-I02

character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L007-B01-I02_end_decision_locked_background_r003_candidate.png

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- edit_base_and_setup_anchor: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L006-B01-I02_end_decision_locked_background_r001_candidate.png` · `7842d9c8a4c2f67848fb38195d11544e985f414a61e6a8f0a4658208bd80fb68`

```text
Use case: identity-preserve, Feltwillow narrative scene edit. Return ONE complete 16:9 landscape image. Reference 1 supplies approved Milo identity/anatomy/material. Reference 2 is the edit target and camera/background/scale anchor. Make a tightly scoped performance edit to reference 2 (S03-L006 anchor): Turn head/gaze LEFT toward the long meadow path; do not turn the whole body left. Keep the original complete background unchanged: fork paths, stone, trees, sky, shadows, lens/crop and framing. Keep Milo at EXACTLY the same foot/root position and standing depth as reference 2, both feet grounded on the SAME ground contact pixels, same apparent body and head scale. No walking, travelling, sliding or independent resizing. Keep torso orientation, leg spacing, tail attachment and actor construction from the anchor; change only head/eyes and minimal local acting. Preserve LEFT safe sunny meadow and RIGHT dark shortcut. Empty hands; acorn remains behind on stream stone offscreen.
Audience hears: Then at the long path.
Preserve grey felt, cream muzzle and narrow elongated chest/belly inset, orange tail, green eyes and short readable neck. Lean canonical body; no independently enlarged head, inflated abdomen or short torso. Applicable comparable upright projected head fraction is 0.39 +/-0.01; bent/pitched/portrait views require local comparable proportions, not that global fraction. Preserve horizontal torso/paw/cream-patch proportions too. No visible teeth. Mouth closed in this still; narration never drives mouth, dialogue uses later lip-sync. No new animals, text, corner symbols, watermark, labels or measurement marks. Match scene light, support contacts/shadows and occlusion. Do not resize parts independently. Return a candidate only; generation guidance does not certify measured anatomy or exact pixels.
```

## 8. S03-L008-B01-I02

character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L008-B01-I02_end_decision_locked_background_r003_candidate.png

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- edit_base_and_setup_anchor: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L006-B01-I02_end_decision_locked_background_r001_candidate.png` · `7842d9c8a4c2f67848fb38195d11544e985f414a61e6a8f0a4658208bd80fb68`

```text
Use case: identity-preserve, Feltwillow narrative scene edit. Return ONE complete 16:9 landscape image. Reference 1 supplies approved Milo identity/anatomy/material. Reference 2 is the edit target and camera/background/scale anchor. Make a tightly scoped performance edit to reference 2 (S03-L006 anchor): Turn head/gaze RIGHT toward the shortcut; keep body and feet planted. Keep the original complete background unchanged: fork paths, stone, trees, sky, shadows, lens/crop and framing. Keep Milo at EXACTLY the same foot/root position and standing depth as reference 2, both feet grounded on the SAME ground contact pixels, same apparent body and head scale. No walking, travelling, sliding or independent resizing. Keep torso orientation, leg spacing, tail attachment and actor construction from the anchor; change only head/eyes and minimal local acting. Preserve LEFT safe sunny meadow and RIGHT dark shortcut. Empty hands; acorn remains behind on stream stone offscreen.
Audience hears: Then at the shortcut.
Preserve grey felt, cream muzzle and narrow elongated chest/belly inset, orange tail, green eyes and short readable neck. Lean canonical body; no independently enlarged head, inflated abdomen or short torso. Applicable comparable upright projected head fraction is 0.39 +/-0.01; bent/pitched/portrait views require local comparable proportions, not that global fraction. Preserve horizontal torso/paw/cream-patch proportions too. No visible teeth. Mouth closed in this still; narration never drives mouth, dialogue uses later lip-sync. No new animals, text, corner symbols, watermark, labels or measurement marks. Match scene light, support contacts/shadows and occlusion. Do not resize parts independently. Return a candidate only; generation guidance does not certify measured anatomy or exact pixels.
```

## 9. S03-L009-B01-I01

character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L009-B01-I01_single_milo_decision_r003_candidate.png

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- edit_base_and_setup_anchor: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L010-B01-I01_single_milo_decision_r002_candidate.png` · `dbe435cf3f87266d0ea7bae32b0580347939642702465fbe4b2900af672f1658`

```text
Use case: identity-preserve, Feltwillow narrative scene edit. Return ONE complete 16:9 landscape image. Reference 1 supplies approved Milo identity/anatomy/material. Reference 2 is the edit target and camera/background/scale anchor. Reference 2 is L010, the preferred portrait body/framing. Preserve EXACT full head/ear silhouette, head scale, neck/shoulders and visible upper-chest/torso region, pose, position and crop from L010. Change only angle-compatible eyes/brows/expression to quiet determination while choosing the shortcut. Keep the same blurred shallow-focus fork background. Do not expose more or less torso, add hands/tail, alter shoulders or enlarge head. Closed toothless still mouth.
Audience hears: The shortcut. Definitely the shortcut.
Preserve grey felt, cream muzzle and narrow elongated chest/belly inset, orange tail, green eyes and short readable neck. Lean canonical body; no independently enlarged head, inflated abdomen or short torso. Applicable comparable upright projected head fraction is 0.39 +/-0.01; bent/pitched/portrait views require local comparable proportions, not that global fraction. Preserve horizontal torso/paw/cream-patch proportions too. No visible teeth. Mouth closed in this still; narration never drives mouth, dialogue uses later lip-sync. No new animals, text, corner symbols, watermark, labels or measurement marks. Match scene light, support contacts/shadows and occlusion. Do not resize parts independently. Return a candidate only; generation guidance does not certify measured anatomy or exact pixels.
```

## 10. S02-L004-B01-I02

character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L004-B01-I02_end_stone_beside_stream_r003_candidate.png

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- edit_base_and_setup_anchor: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L004-B02-I03_end_stone_beside_stream_r002_candidate.png` · `ab3cfd7f6c6d7f31170e8432fec4b1cfb6e598b1738609e62a979684ff0cdaf8`
- reviewed_performance: `character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_hold_3q_r003_candidate.png` · `fc8bd6d0b64ee8302a79420bbdd96c59264f09d003045264dc4c8a8bd6e3bb02`

```text
Use case: identity-preserve, Feltwillow narrative scene edit. Return ONE complete 16:9 landscape image. Reference 1 supplies approved Milo identity/anatomy/material. Reference 2 is the edit target and camera/background/scale anchor. Reference 2 is the preferred stone/stream placement background. Keep its complete background/camera/framing unchanged. Change Milo from crouching to standing near the same stone on the same support plane and holding the SAME acorn in both paws before placement. Use one acorn, preserve its material/cap, and make its size consistent with reference 2 relative to Milo head/hands. Reference 3 is the standing/holding pose guide, not acorn size or background authority. Maintain local rooted contact and lighting; do not move the stone/stream or introduce a new route.
Audience hears: Still holding the acorn, the mouse stood up. Then the little traveler set it carefully beside a stone at the stream.
Preserve grey felt, cream muzzle and narrow elongated chest/belly inset, orange tail, green eyes and short readable neck. Lean canonical body; no independently enlarged head, inflated abdomen or short torso. Applicable comparable upright projected head fraction is 0.39 +/-0.01; bent/pitched/portrait views require local comparable proportions, not that global fraction. Preserve horizontal torso/paw/cream-patch proportions too. No visible teeth. Mouth closed in this still; narration never drives mouth, dialogue uses later lip-sync. No new animals, text, corner symbols, watermark, labels or measurement marks. Match scene light, support contacts/shadows and occlusion. Do not resize parts independently. Return a candidate only; generation guidance does not certify measured anatomy or exact pixels. Reference 3 supplies only the specifically labeled supporting pose/comparison role; it must not change the reference-2 setup or camera.
```

## 11. S01-L001 forest establishment

character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L001-B01_location_peaceful_forest_establish_r003_candidate.png

- forest_world_style_reference; new_wider_establishing_view: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L001-B01-I02_end_forest_edge_r002_candidate.png` · `73f47bbc343decd30554a8774ea3bc6c213ab6470c09905e2d45277bb4d53007`

```text
Create one 16:9 landscape peaceful-forest establishing image for the beginning of S01-L001, before cutting to the referenced Milo walking scene. Use reference 1 for handmade felt forest/material, afternoon light and forest-world identity. Show a noticeably WIDER welcoming forest edge, layers of trees, moss, small flowers and open exploratory ground. This is an environment-only editorial pre-roll: NO Milo, Leo or other characters, no acorn, no text, watermark or corner symbol. No mandatory stream, mountains or hollow log. Preserve handmade felt woodland art direction, warm natural light, appealing depth. This is a new establishing view, not an exact-pixel lock or a crop. The complete audio is 9.96 seconds; no text or timing labels in the image.
```
