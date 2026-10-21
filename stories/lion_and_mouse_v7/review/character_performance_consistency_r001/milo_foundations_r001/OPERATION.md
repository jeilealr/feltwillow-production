# Milo foundation image operation — corrected source

Endpoint: `image_gen.imagegen` (built-in). Exactly **3 requests**, one transparent candidate per request, no retries. Model/seed/output-size controls and price are not exposed here; estimated/actual cost is **unknown**, not assumed free. No request has been submitted.

The prior eight-request pilot remains a staged draft. This operation concretely prepares its three independent foundation assets; dependent variants wait for real reviewed source images rather than invented hashes.

## Inputs

- `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — owner-approved identity only; SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`.
- `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L003-B01-I02_end_deeper_forest_trail_r001_candidate.png` — owner-requested S01-L003 body/pose inspiration; source scene remains pending owner review; SHA-256 `21fb3f5294962612f785c6c3b8e23e09c0b076d07f0c4147cf65d25be03373fc`.

S03-L004 is not an input. Selecting S01-L003 as inspiration does not change the existing scene approval or canonical authority.

## Exact requests

### 1. milo.walk.screen_right.lightstep.3q:contact

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_screen_right_lightstep_3q_contact_r001_candidate.png`.

Create exactly one reusable needle-felt Milo character asset on a truly transparent background. Reference 1 is the approved identity: preserve rounded forehead and cheeks, cream muzzle and chest inset, moss-green irises, large rounded grey-interior ears, charcoal nose, muted burnt-orange felt tail, warm neutral-grey matted wool and handmade texture. Mouth closed, no visible teeth, no mane, no hair tuft, no pot belly. Use neutral even studio illumination so forest sunset lighting is not baked into intrinsic colours. Leave comfortable padding around every requested body part. No forest, props, ground plate, typography, labels, watermark, collage or multiple figures. This is a candidate performance asset, not a replacement canonical. Reference 2 is S01-L003-B01-I02 and supplies the owner's preferred upright body/leg posture and overall walking silhouette only. Use that readable torso-to-leg balance; avoid the compressed, fuller-torso impression seen in other rejected-for-comparison shots. Do not invent a slim or stretched new animal; compare anatomical parts at a compatible three-quarter angle rather than copying the scene's pixel height. Do not copy the forest, shadows, camera crop or colour cast. Show the complete mouse, both ears, both feet and complete tail, three-quarter facing screen-right, in a light exploratory walking contact key. Near/support foot is planted with a readable sole/contact point; opposite foot is in a coherent trailing gait position. Preserve natural short sturdy limb anatomy without squashing the torso. Relaxed arms, curious calm closed-mouth face, gaze along the route. The asset must be useful as a reference for S01-L001, S01-L002 winding path and S01-L003, without enforcing the same scene screen size.

### 2. milo.portrait.base.3q:default

Output: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_portrait_base_3q_default_r001_candidate.png`.

Create exactly one reusable needle-felt Milo character asset on a truly transparent background. Reference 1 is the approved identity: preserve rounded forehead and cheeks, cream muzzle and chest inset, moss-green irises, large rounded grey-interior ears, charcoal nose, muted burnt-orange felt tail, warm neutral-grey matted wool and handmade texture. Mouth closed, no visible teeth, no mane, no hair tuft, no pot belly. Use neutral even studio illumination so forest sunset lighting is not baked into intrinsic colours. Leave comfortable padding around every requested body part. No forest, props, ground plate, typography, labels, watermark, collage or multiple figures. This is a candidate performance asset, not a replacement canonical. Create an angle-specific neutral portrait base, three-quarter facing screen-right: the complete head with BOTH ears and ample clearance, neck and upper chest. Preserve the canonical head/ear/muzzle silhouette and eye geometry; calm attentive eyes and a soft neutral closed-mouth expression. No face-only mask or detached face sticker. No camera or anatomy exaggeration. This neutral base will be reviewed before making startled and determined expression variants.

### 3. milo.decision.stationary.3q:sky

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_decision_stationary_3q_sky_r001_candidate.png`.

Create exactly one reusable needle-felt Milo character asset on a truly transparent background. Reference 1 is the approved identity: preserve rounded forehead and cheeks, cream muzzle and chest inset, moss-green irises, large rounded grey-interior ears, charcoal nose, muted burnt-orange felt tail, warm neutral-grey matted wool and handmade texture. Mouth closed, no visible teeth, no mane, no hair tuft, no pot belly. Use neutral even studio illumination so forest sunset lighting is not baked into intrinsic colours. Leave comfortable padding around every requested body part. No forest, props, ground plate, typography, labels, watermark, collage or multiple figures. This is a candidate performance asset, not a replacement canonical. Reference 2 is S01-L003-B01-I02 and supplies the owner's preferred upright body/leg posture and overall walking silhouette only. Use that readable torso-to-leg balance; avoid the compressed, fuller-torso impression seen in other rejected-for-comparison shots. Do not invent a slim or stretched new animal; compare anatomical parts at a compatible three-quarter angle rather than copying the scene's pixel height. Do not copy the forest, shadows, camera crop or colour cast. Show one complete full-body stationary mouse in the same three-quarter screen-right body orientation, both feet firmly planted on one plane, relaxed arms, tail fully visible. Establish stable head/body/leg geometry and clear foot-root landmarks. The head tilts gently up and eyes look toward the sky with a thoughtful concerned realization. Preserve anatomical head size under the projected tilt. No walking step, no acorn, no route commitment. Later left/right gaze variants must preserve this body's placement and proportions; do not create those variants in this image.

## Approval boundary

Only these three requests are proposed. Outputs stay candidates. After body/head geometry review, dependent gait, facial expression and fork-gaze variants can use the reviewed first-stage bytes. No existing image or canonical is overwritten.

The exact tool arguments and source hashes are in OPERATION.json. Its SHA-256 is `a137451b2add1c7231d90c8639c0ced10aa6e160047046b552023bf169c74aa3`.
