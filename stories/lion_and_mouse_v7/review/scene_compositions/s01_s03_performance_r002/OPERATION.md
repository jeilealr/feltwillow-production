# S01–S03 Milo scene replacements · proposed operation

**Prepared only. No image requests submitted.** Endpoint: `image_gen.imagegen`. 20 requests, one candidate per request, zero automatic retries. Full-scene 16:9 image guidance, opaque output. Model and seed are managed by the tool, not exposed. Total cost is unknown.

Twenty owner-review scene edits; three fixed-fork shots held; one environment-only cutaway unchanged. Milo performances are owner-selected, while anatomy/prop/standalone expression/staging evidence is incomplete. This proposal does not declare production readiness or bypass those gates. Existing scene originals stay intact and new outputs use r002.

Operation SHA-256: `ac8b5095a1c5c874532fd26c9105e70f104b6a10c659aa4be47afec8ff9ebc86`

## Held fixed-fork group

- S03-L006-B01-I02: Keep S03-L006–L008 as one group. Shared camera/depth/root/scale anchor is unmeasured and long_path still turns the whole body. Guidance cannot promise exact background pixels.
- S03-L007-B01-I02: Keep S03-L006–L008 as one group. Shared camera/depth/root/scale anchor is unmeasured and long_path still turns the whole body. Guidance cannot promise exact background pixels.
- S03-L008-B01-I02: Keep S03-L006–L008 as one group. Shared camera/depth/root/scale anchor is unmeasured and long_path still turns the whole body. Guidance cannot promise exact background pixels.

Environment retained: S02-L002-B01-I02.

## 1. S01-L001-B01-I02

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L001-B01-I02_end_forest_edge_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_screen_right_lightstep_3q_passing_step_r004_candidate.png | 73cd8aa416afe6acb7f87db94f924d47a4773b3cad59eb7a4b0096ed97cad150 |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L001-B01-I02_end_forest_edge_r001_candidate.png | 3f2d19e062c06461befb73d32697be755f30ae2a3d85ac58ec0f2739f32d00bc |

Expression requirement: milo.expression.curious.3q (planned). No standalone expression file invented.

Readiness limitations: Passing foot does not clearly travel beneath the hips; gait/support sequence remains unverified.; Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S01-L001-B01-I02. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.walk.screen_right.lightstep.3q:passing_step); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: Once upon a time, at the edge of a wide and peaceful forest, there lived a little mouse who loved exploring.
Visual beat: Establish the wide, peaceful forest where the story takes place; Milo is a small explorer within the setting, with readable open ground and forest depth. No obligatory stream, mountain or hollow log.
Key-image phase: Action end
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

Do not add an acorn: it has not yet entered this shot. Do not import incidental props from the pose reference. Show one readable rightward walking moment, with a grounded supporting foot. This scene still does not prove a complete gait cycle.
Persistent world state: WORLD_S01-L001-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 2. S01-L002-B01-I01

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L002-B01-I01_single_berry_thicket_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r003_candidate.png | 85739a4443c078635a804a687f8313cabf3d0a6f5eacfbc444482cbe3f943a36 |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L002-B01-I01_single_berry_thicket_r001_candidate.png | 4d12beaaba817975bcb20952c34fd4da8da80e3eb91a8341e7fe591f84073f0a |

Expression requirement: milo.expression.curious.3q (planned). No standalone expression file invented.

Readiness limitations: Unexpected berry branch overlaps fingers and exits frame; not a prop-free reusable character layer.; Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S01-L002-B01-I01. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.inspect.berry_thicket.3q:default); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: The mouse knew every berry bush, every hollow log, and nearly every winding path beneath the trees.
Visual beat: Independent intimate berry-thicket scene at mouse height; Milo knows this place well. Fill the local world with felt leaves/berries and dry ground, without obligatory river or distant landscape.
Key-image phase: Milo peers into a familiar berry bush at mouse height
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

Do not add an acorn: it has not yet entered this shot. Do not import incidental props from the pose reference. Preserve berries/vegetation belonging to the scene base; do not import the isolated pose branch or replace scene berries with unrelated blueberries. Match grip to the existing story plant.
Persistent world state: WORLD_S01-L001-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 3. S01-L002-B02-I01

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L002-B02-I01_single_hollow_log_clearing_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_log_3q_r004_candidate.png | cefd31b01a39a955bf771d4c07ac1936b0a67d04caeaf925d2c069c1d3e4c868 |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L002-B02-I01_single_hollow_log_clearing_r001_candidate.png | 27078f474b54e66d08b9cd612c43082e671f27cac95b7cb57ec01c6b49e55aad |

Expression requirement: milo.expression.curious.3q (planned). No standalone expression file invented.

Readiness limitations: Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S01-L002-B02-I01. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.inspect.log.3q:default); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: The mouse knew every berry bush, every hollow log, and nearly every winding path beneath the trees.
Visual beat: Independent woodland clearing at a hollow log; Milo explores its opening. This need not be the log across the canonical stream and needs no water or mountains.
Key-image phase: Milo explores the mouth of the familiar hollow log
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

Do not add an acorn: it has not yet entered this shot. Do not import incidental props from the pose reference.
Persistent world state: WORLD_S01-L001-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 4. S01-L002-B03-I02

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L002-B03-I02_end_winding_woodland_path_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_screen_right_lightstep_3q_passing_step_r004_candidate.png | 73cd8aa416afe6acb7f87db94f924d47a4773b3cad59eb7a4b0096ed97cad150 |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L002-B03-I02_end_winding_woodland_path_r001_candidate.png | 82a06406184a3b7eeae67b6b913dc3893b52974bfd0034e78733ad0a00f0f2f8 |

Expression requirement: milo.expression.curious.3q (planned). No standalone expression file invented.

Readiness limitations: Passing foot does not clearly travel beneath the hips; gait/support sequence remains unverified.; Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S01-L002-B03-I02. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.walk.screen_right.lightstep.3q:passing_step); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: The mouse knew every berry bush, every hollow log, and nearly every winding path beneath the trees.
Visual beat: Independent winding path beneath towering forest trees, immersive at Milo scale; a distinct forest place, with no required stream-bank geography.
Key-image phase: Action end
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

Do not add an acorn: it has not yet entered this shot. Do not import incidental props from the pose reference. Show one readable rightward walking moment, with a grounded supporting foot. This scene still does not prove a complete gait cycle.
Persistent world state: WORLD_S01-L002-B03-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 5. S01-L003-B01-I02

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L003-B01-I02_end_deeper_forest_trail_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_screen_right_lightstep_3q_passing_step_r004_candidate.png | 73cd8aa416afe6acb7f87db94f924d47a4773b3cad59eb7a4b0096ed97cad150 |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L003-B01-I02_end_deeper_forest_trail_r001_candidate.png | 21fb3f5294962612f785c6c3b8e23e09c0b076d07f0c4147cf65d25be03373fc |

Expression requirement: milo.expression.curious.3q (planned). No standalone expression file invented.

Readiness limitations: Passing foot does not clearly travel beneath the hips; gait/support sequence remains unverified.; Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S01-L003-B01-I02. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.walk.screen_right.lightstep.3q:passing_step); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: One afternoon, the mouse wandered farther from home than usual.
Visual beat: Independent deeper woodland trail with receding forest depth showing Milo farther from home; choose a different clearing/composition from the previous path.
Key-image phase: Action end
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

Do not add an acorn: it has not yet entered this shot. Do not import incidental props from the pose reference. Show one readable rightward walking moment, with a grounded supporting foot. This scene still does not prove a complete gait cycle.
Persistent world state: WORLD_S01-L003-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 6. S01-L004-B01-I01

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B01-I01_single_tall_grass_seed_patch_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_forage_seeds_3q_r006_candidate.png | 4f26414c10b1d9e820e08ea112069a15afbc8df3830e2bc9a253e909474ba75d |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B01-I01_single_tall_grass_seed_patch_r001_candidate.png | 0192f5da4c2988c8e3b18a00bde76fc2927e73c175fa29d65f7cb16de64f1794 |

Expression requirement: milo.expression.curious.3q (planned). No standalone expression file invented.

Readiness limitations: Foraging head is strongly bowed and far ear has very tight right-frame clearance; cannot use upright head fraction.; Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S01-L004-B01-I01. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.forage.seeds.3q:default); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: There had been so many wonderful things to eat — tiny seeds beneath the tall grass, sweet berries beside the stream, and one particularly delicious acorn that took much longer to enjoy than expected.
Visual beat: Independent close scene of Milo foraging tiny seeds beneath tall grass; seed/grass scale is the visual idea, with the surrounding forest mostly outside the close frame.
Key-image phase: Cut from seeds under tall grass to Milo enjoying the familiar seed patch
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

Do not add an acorn: it has not yet entered this shot. Do not import incidental props from the pose reference.
Persistent world state: WORLD_S01-L003-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 7. S01-L004-B01-I02

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B01-I02_single_tall_grass_seed_patch_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_forage_seeds_3q_r006_candidate.png | 4f26414c10b1d9e820e08ea112069a15afbc8df3830e2bc9a253e909474ba75d |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B01-I02_single_tall_grass_seed_patch_r001_candidate.png | d52a4af0b9a74df4279f1f808da5d991b38ff6604f00e496be1582e1f029f557 |

Expression requirement: milo.expression.curious.3q (planned). No standalone expression file invented.

Readiness limitations: Foraging head is strongly bowed and far ear has very tight right-frame clearance; cannot use upright head fraction.; Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S01-L004-B01-I02. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.forage.seeds.3q:default); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: There had been so many wonderful things to eat — tiny seeds beneath the tall grass, sweet berries beside the stream, and one particularly delicious acorn that took much longer to enjoy than expected.
Visual beat: Independent close scene of Milo foraging tiny seeds beneath tall grass; seed/grass scale is the visual idea, with the surrounding forest mostly outside the close frame.
Key-image phase: Cut from seeds under tall grass to Milo enjoying the familiar seed patch
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

Do not add an acorn: it has not yet entered this shot. Do not import incidental props from the pose reference.
Persistent world state: WORLD_S01-L003-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 8. S01-L004-B02-I01

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B02-I01_single_independent_stream_margin_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_harvest_berries_3q_r003_candidate.png | 8f97910c3cda5fb9bf7fcd78282cee245c93c845caf53f1d2dd6efc6f623725d |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B02-I01_single_independent_stream_margin_r001_candidate.png | 2e84dd24bb8bc9ee0c2bf7ce1f53bcf63917e088a259c17dd476c912c0aa91b4 |

Expression requirement: milo.expression.curious.3q (planned). No standalone expression file invented.

Readiness limitations: Unexpected blueberries occlude both hands; not a prop-free reusable character layer.; Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S01-L004-B02-I01. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.harvest.berries.3q:default); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: There had been so many wonderful things to eat — tiny seeds beneath the tall grass, sweet berries beside the stream, and one particularly delicious acorn that took much longer to enjoy than expected.
Visual beat: Independent stream-side berry scene because the words name water; choose any bank orientation and local vegetation, without repeating the canonical river-on-right, mountains or opposite-bank log.
Key-image phase: Milo enjoys berries beside the recognizable stream
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

Do not add an acorn: it has not yet entered this shot. Do not import incidental props from the pose reference. Preserve berries/vegetation belonging to the scene base; do not import the isolated pose branch or replace scene berries with unrelated blueberries. Match grip to the existing story plant.
Persistent world state: WORLD_S01-L003-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 9. S01-L004-B03-I03

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B03-I03_end_acorn_glade_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_pick_hold_3q_savor_r003_candidate.png | 0d090d3bb8834d280300264defafc60347b8da7fbcc1b49548f92180ec0defeb |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B03-I03_end_acorn_glade_r001_candidate.png | c0c24ee62217f1bec893f95978e1933514baea8159e586e8d13661a40573f900 |

Expression requirement: milo.expression.curious.3q (planned). No standalone expression file invented.

Readiness limitations: Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S01-L004-B03-I03. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.acorn.pick_hold.3q:savor); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: There had been so many wonderful things to eat — tiny seeds beneath the tall grass, sweet berries beside the stream, and one particularly delicious acorn that took much longer to enjoy than expected.
Visual beat: Independent sheltered forest glade where Milo picks up and savors the acorn. Keep the acorn readable and its custody explicit; no compulsory water or stream-master landmarks.
Key-image phase: Action end
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

Milo retains the same story acorn from the scene reference. Do not adopt a different acorn from the pose reference or resize hands to fit it. Preserve plausible finger contact and occlusion; actual acorn fit remains for owner review.
Persistent world state: WORLD_S01-L004-B03-E02; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 10. S02-L001-B01-I02

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L001-B01-I02_end_evening_glade_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_hold_3q_r003_candidate.png | fc8bd6d0b64ee8302a79420bbdd96c59264f09d003045264dc4c8a8bd6e3bb02 |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L001-B01-I02_end_evening_glade_r001_candidate.png | 5826f5dd3fd98b17077e1803505161097a4cd639473acdfed8c958fbede16aeb |

Expression requirement: milo.expression.curious.3q (planned). No standalone expression file invented.

Readiness limitations: Unexpected acorn generated despite prop-free request; not a clean character layer or approved prop design.; Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S02-L001-B01-I02. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.acorn.hold.3q:default); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: By the time the mouse finally looked up, the golden afternoon light had begun to fade.
Visual beat: Independent forest view of Milo looking up as warm afternoon light fades; the acorn remains with him. An opening in the canopy conveys evening without a required stream-bank panorama.
Key-image phase: Action end
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

Milo retains the same story acorn from the scene reference. Do not adopt a different acorn from the pose reference or resize hands to fit it. Preserve plausible finger contact and occlusion; actual acorn fit remains for owner review.
Persistent world state: WORLD_S02-L001-B01-E02; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 11. S02-L003-B01-I01

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L003-B01-I01_single_evening_glade_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r003_candidate.png | a981bbb205d20384279db3785045d9d5dce0836e1d666963b0f962ec214a1d79 |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L003-B01-I01_single_evening_glade_r001_candidate.png | 68e71c21f2d0cd51469dd48360fa853360bc60d358de6d0df27eb0279795ac0a |

Expression requirement: milo.expression.startled_realization.3q (planned). No standalone expression file invented.

Readiness limitations: Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal portrait evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S02-L003-B01-I01. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.portrait.base.3q:default); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: Oh! It's getting late!
Visual beat: Close-up of Milo’s startled realization, with a softly blurred forest background. Preserve his identity and acorn custody offscreen; no required recognizable stream landmarks.
Key-image phase: Milo realizes with startled urgency that it is late
Performance/emotion: startled_realization.
Full head and both ears, short natural neck, shoulders and upper chest only; shallow-focus background from this scene. All whiskers inside frame with margin; no torso, hands, tail or feet in this portrait.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

Milo retains the same story acorn from the scene reference. Do not adopt a different acorn from the pose reference or resize hands to fit it. Acorn possession persists offscreen in this portrait; do not include hands/acorn/lower torso in the crop.
Persistent world state: WORLD_S02-L003-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 12. S02-L004-B01-I02

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L004-B01-I02_end_stone_beside_stream_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_hold_3q_r003_candidate.png | fc8bd6d0b64ee8302a79420bbdd96c59264f09d003045264dc4c8a8bd6e3bb02 |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L004-B01-I02_end_stone_beside_stream_r001_candidate.png | 9995387e4136a821d46023f42e68fe3967789c9bc167518b45f94abfaabccde6 |

Expression requirement: milo.expression.startled_realization.3q (planned). No standalone expression file invented.

Readiness limitations: Unexpected acorn generated despite prop-free request; not a clean character layer or approved prop design.; Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S02-L004-B01-I02. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.acorn.hold.3q:default); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: Still holding the acorn, the mouse stood up. Then the little traveler set it carefully beside a stone at the stream.
Visual beat: Milo stands while still holding the acorn, near a stone by a stream. This local action setting follows the words, without copying the original stream panorama.
Key-image phase: Action end
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

Milo retains the same story acorn from the scene reference. Do not adopt a different acorn from the pose reference or resize hands to fit it. Preserve plausible finger contact and occlusion; actual acorn fit remains for owner review.
Persistent world state: WORLD_S02-L004-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 13. S02-L004-B02-I03

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L004-B02-I03_end_stone_beside_stream_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_acorn_place_3q_released_r003_candidate.png | a10c15527ea7cb8eba19f6d2aea63c1b2b089167c2936f4e895178915c92905a |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L004-B02-I03_end_stone_beside_stream_r001_candidate.png | 1004f53190038fe37820ed1728c9ebf3a82b6b957f9343efe8a8f19c1bbd9957 |

Expression requirement: milo.expression.startled_realization.3q (planned). No standalone expression file invented.

Readiness limitations: Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S02-L004-B02-I03. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.acorn.place.3q:released); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: Still holding the acorn, the mouse stood up. Then the little traveler set it carefully beside a stone at the stream.
Visual beat: Milo lowers the acorn, establishes contact beside the stream stone, then releases it. Preserve custody/contact across this action, with framing chosen locally rather than a repeated canonical landscape.
Key-image phase: Milo releases the acorn beside the stone; custody transfers to the stone
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

The acorn is released on the stream stone, Milo hands empty; retain the acorn beside the stone and contact/readable separation.
Persistent world state: WORLD_S02-L004-B02-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 14. S03-L001-B01-I02

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L001-B01-I02_end_homeward_distance_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_forward_r003_candidate.png | 55e69e9bc28b2214b19a3f046e5b26d8a799125c8e43c6e83af66684831c954f |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L001-B01-I02_end_homeward_distance_r001_candidate.png | 7ad3c547b2c911c1253eda6ce70bf11cf65004ee2d6248e926d0c6314e765840 |

Expression requirement: milo.expression.startled_realization.3q (planned). No standalone expression file invented.

Readiness limitations: Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S03-L001-B01-I02. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.decision.stationary.3q:forward); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: Home was still quite a distance away.
Visual beat: Milo pauses at the fork with the distant homeward route visible
Key-image phase: End composition: subtle readable progression within this same shot; final performance to be reviewed against audio
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

The acorn remains behind on the stream stone, offscreen. Milo hands are empty; do not insert an acorn in this route/portrait shot.
Persistent world state: WORLD_S03-L001-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 15. S03-L002-B01-I02

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L002-B01-I02_end_two_routes_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_forward_r003_candidate.png | 55e69e9bc28b2214b19a3f046e5b26d8a799125c8e43c6e83af66684831c954f |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L002-B01-I02_end_two_routes_r001_candidate.png | 3719fc117490072d7faeefe41a270d38bc2ce3de812a2fd374cf17bc4946d01c |

Expression requirement: milo.expression.startled_realization.3q (planned). No standalone expression file invented.

Readiness limitations: Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S03-L002-B01-I02. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.decision.stationary.3q:forward); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: There were two ways to get there.
Visual beat: Establish the fork and its two distinct routes without changing their topology
Key-image phase: End composition: subtle readable progression within this same shot; final performance to be reviewed against audio
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

The acorn remains behind on the stream stone, offscreen. Milo hands are empty; do not insert an acorn in this route/portrait shot.
Persistent world state: WORLD_S03-L001-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 16. S03-L003-B01-I02

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L003-B01-I02_end_safe_left_meadow_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_forward_r003_candidate.png | 55e69e9bc28b2214b19a3f046e5b26d8a799125c8e43c6e83af66684831c954f |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L003-B01-I02_end_safe_left_meadow_r001_candidate.png | 5d3218767aacdcd4bfb35b6a114531c31591788511024e9010363dff5652d3fe |

Expression requirement: milo.expression.startled_realization.3q (planned). No standalone expression file invented.

Readiness limitations: Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S03-L003-B01-I02. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.decision.stationary.3q:forward); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: One was the familiar path that curved safely around a sunny meadow.
Visual beat: Emphasize the familiar safe long path curving left around the sunny meadow
Key-image phase: End composition: subtle readable progression within this same shot; final performance to be reviewed against audio
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

The acorn remains behind on the stream stone, offscreen. Milo hands are empty; do not insert an acorn in this route/portrait shot. Milo is stationary and considering the route. Do not show him committing to or walking into the shortcut before S03-L009.
Persistent world state: WORLD_S03-L001-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 17. S03-L004-B01-I02

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L004-B01-I02_end_short_right_route_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_forward_r003_candidate.png | 55e69e9bc28b2214b19a3f046e5b26d8a799125c8e43c6e83af66684831c954f |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L004-B01-I02_end_short_right_route_r001_candidate.png | fdf44bb2c8a09aa91ebbffdcdd264bb050ed76b0788e7e8f49640f08c4a47274 |

Expression requirement: milo.expression.startled_realization.3q (planned). No standalone expression file invented.

Readiness limitations: Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S03-L004-B01-I02. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.decision.stationary.3q:forward); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: The other was much shorter.
Visual beat: Independent emphasis on the short right-hand route; preserve route identity without requiring the next shot to reuse its camera/background
Key-image phase: End composition: subtle readable progression within this same shot; final performance to be reviewed against audio
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

The acorn remains behind on the stream stone, offscreen. Milo hands are empty; do not insert an acorn in this route/portrait shot. Milo is stationary and considering the route. Do not show him committing to or walking into the shortcut before S03-L009.
Persistent world state: WORLD_S03-L001-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 18. S03-L005-B01-I02

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L005-B01-I02_end_shortcut_entrance_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_forward_r003_candidate.png | 55e69e9bc28b2214b19a3f046e5b26d8a799125c8e43c6e83af66684831c954f |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L005-B01-I02_end_shortcut_entrance_r001_candidate.png | 8bca5f933374a93591acfb8430c51d3893db7d4eaabfec1055255e55622e4da7 |

Expression requirement: milo.expression.startled_realization.3q (planned). No standalone expression file invented.

Readiness limitations: Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal body evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S03-L005-B01-I02. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.decision.stationary.3q:forward); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: It cut straight through a quiet part of the forest that the mouse rarely visited.
Visual beat: Independent focused view into the quiet, less familiar shortcut forest; related route geography, deliberate cut from the previous emphasis
Key-image phase: End composition: subtle readable progression within this same shot; final performance to be reviewed against audio
Performance/emotion: the listening audience should read the exact action and emotion of this line.
Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

The acorn remains behind on the stream stone, offscreen. Milo hands are empty; do not insert an acorn in this route/portrait shot. Milo is stationary and considering the route. Do not show him committing to or walking into the shortcut before S03-L009.
Persistent world state: WORLD_S03-L001-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 19. S03-L009-B01-I01

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L009-B01-I01_single_milo_decision_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r003_candidate.png | a981bbb205d20384279db3785045d9d5dce0836e1d666963b0f962ec214a1d79 |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L009-B01-I01_single_milo_decision_r001_candidate.png | a29335766953950d56eca5b1b9af6485829007f22911e14908d40e2f698d28de |

Expression requirement: milo.expression.decisive.3q (planned). No standalone expression file invented.

Readiness limitations: Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal portrait evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S03-L009-B01-I01. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.portrait.base.3q:default); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: The shortcut. Definitely the shortcut.
Visual beat: Cut decisively to Milo’s face as he chooses the shortcut
Key-image phase: Cut decisively to Milo’s face as he chooses the shortcut
Performance/emotion: decisive.
Full head and both ears, short natural neck, shoulders and upper chest only; shallow-focus background from this scene. All whiskers inside frame with margin; no torso, hands, tail or feet in this portrait.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

The acorn remains behind on the stream stone, offscreen. Milo hands are empty; do not insert an acorn in this route/portrait shot.
Persistent world state: WORLD_S03-L009-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

## 20. S03-L010-B01-I01

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L010-B01-I01_single_milo_decision_r002_candidate.png`

| Reference role | Exact input | SHA-256 |
|---|---|---|
| canonical_identity | character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png | c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f |
| reviewed_performance | character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r003_candidate.png | a981bbb205d20384279db3785045d9d5dce0836e1d666963b0f962ec214a1d79 |
| scene_edit_base | character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L010-B01-I01_single_milo_decision_r001_candidate.png | 7e0948752dc73d77562f4c5a0dd89a4fe49c822554f13b9f752c095651f26de7 |

Expression requirement: milo.expression.hopeful_confidence.3q (planned). No standalone expression file invented.

Readiness limitations: Milo: anatomy match pending; pose/acting approval does not certify proportions; Milo: horizontal portrait evidence pending; height alone cannot certify widths/cream patch; Required standalone expression asset remains planned; not a production-ready binding.

Exact prompt:

```text
Edit one existing 16:9 Feltwillow scene into a new candidate image for S03-L010-B01-I01. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance (milo.portrait.base.3q:default); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: I'll be home before the stars come out!
Visual beat: Close-up of Milo delivering his hopeful decision, with a shallow-focus blurred fork-world background; preserve canonical face and closed still-image mouth
Key-image phase: Continue the portrait idea with optimistic confidence; use a fresh editorial cut, not automatic image reuse
Performance/emotion: hopeful_confidence.
Full head and both ears, short natural neck, shoulders and upper chest only; shallow-focus background from this scene. All whiskers inside frame with margin; no torso, hands, tail or feet in this portrait.

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

The acorn remains behind on the stream stone, offscreen. Milo hands are empty; do not insert an acorn in this route/portrait shot.
Persistent world state: WORLD_S03-L010-B01-E01; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.
```

