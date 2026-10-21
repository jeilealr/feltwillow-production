# Opening Milo proportion correction — one proposed edit

Endpoint `image_gen.imagegen`; **1 request**, one opaque 16:9 candidate, **no retries**, model/seed tool-managed. **Cost unknown.** No request submitted.

Operation SHA-256 `cf787aa54a4063e2522f449590023e3053fb871e7b564e1c3ee6f032f4405b25`.

Only `S01-L001-B01-I02` changes. Preserve all other candidate bytes and statuses. The existing source remains untouched; save a sibling r006 candidate.

- edit_base_forest_camera_support_contact: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L001-B01-I02_end_forest_edge_r002_candidate.png` · `73f47bbc343decd30554a8774ea3bc6c213ab6470c09905e2d45277bb4d53007`
- canonical_identity_anatomy: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- reviewed_walk_contact_performance_not_scene_scale: `character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_screen_right_lightstep_3q_contact_r005_candidate.png` · `0aa6e06a2df69af19bcfe77c68c11ec79956337ec0f0560df2944629d32bc5e2`
- owner_preferred_comparable_walking_scene_not_background: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L003-B01-I02_end_deeper_forest_trail_r002_candidate.png` · `937612f07bb4192961592f12618026003229654916269b7bb2020f9ee71cf1eb`

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L001-B01-I02_end_forest_edge_r006_candidate.png`

Exact prompt:

```text
Edit reference 1 into exactly ONE 16:9 Feltwillow scene candidate. Correct ONLY Milo's overly compact/squashed walking construction. Reference 2 is the unchanged canonical identity/anatomy/material authority; reference 3 is the owner-selected three-quarter screen-right lightstep contact performance; reference 4 is the owner-preferred S01-L003 walking appearance, for comparable head/body/neck/torso/leg balance ONLY, never its background. Rebuild Milo as a coherent lean felt mouse with readable short neck, natural shoulder-to-pelvis length, restrained belly, consistent leg construction and rounded felt feet. Keep a light exploratory screen-right step with a supporting foot on the same path/contact region; no running, squat or shortened torso. Preserve identity, grey felt, green eyes, cream muzzle/chest patch and orange tail. Do not stretch the entire existing sprite or independently rescale head, ears, torso, hands or feet; pose the same anatomical design. Do not force equal pixel height between the two different scenes.

For a compatible upright head pitch/support, requested crown-to-chin (excluding ears) / crown-to-supporting sole is 0.39 +/-0.01. A walking bend/foreshortening is not permission to fake this ratio; prefer an upright readable step so the projection can be reviewed. Canonical visible head/torso surface-axis baseline is approximately 1.06. At compatible yaw/lean, visible upper/mid/lower torso-panel widths / head width are approximately 0.44/0.53/0.49, mid-belly panel / torso surface height 0.62; lower-body pelvis-band / head width 0.74, near-thigh band 0.29, near-arm band 0.20. These are visible surface guides with uncertainty, not hidden skeleton or universal tolerance. Exclude arms/tail from torso width. Cream patch upper/mid/lower widths are approximately 0.61/0.61/0.63 of the corresponding visible torso panels; preserve its slim coverage rather than a broad round belly. Canonical-compatible ear/head, eye/head, paw and limb thickness carry through; no big-head/small-body redesign.

Preserve reference-1 forest background, tree/rocks/plants/path geography, afternoon light, lens/crop, composition, actor depth and contact region. Do not copy another setting or create props/acorn. Keep full ears, limbs and tail with comfortable clearance. One Milo only, mouth closed, no visible teeth. No lettering, watermark or corner symbol. Integrate compatible light, support shadow and occlusion. This is a local character correction, not a new scene or exact-match claim; output must receive visual/proportion review.
```
