# Four S05 pose-local facial edits

**Prepared only: 4 image_gen.imagegen requests, one output each, no retries. Cost unknown.**

Operation SHA-256: `01f8f6515698dd2d975922cbc671d0e83962e55103781a50ab62040dc980e72d`. [Exact operation](OPERATION.json) contains all prompts, settings, inputs and hashes.

Apply panic/worried acting to trip, support_lost, tumble and roll while preserving each existing body and local head angle. Use falling_panic as emotion guidance only. It remains a candidate; this does not approve it or replace canonical identity. Body preservation is requested and must be checked after generation; generative editing does not guarantee pixel identity.

Native PNG review: all four retain a pleasant/smiling mouth despite falling. Roll has a strongly tilted head, so an upright portrait replacement would be incompatible. No quantitative anatomy defect is asserted.

## Requests

### 1. milo.trip.rear_paw.3q:trip

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_trip_rear_paw_trip_3q_r002_candidate.png`

Uses: S05-L008-B01-I04

- pose: `character/characters/lion_and_mouse_v7/Milo/poses/milo_trip_rear_paw_trip_3q_r001_candidate.png` — SHA-256 `07407db61abd193319078fab8d0803c49e81f6e9e42312167caf3714cba8d2b1`

- expression: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_expression_falling_panic_3q_r001_candidate.png` — SHA-256 `aeb779f17676f06aa838b519c019110b3d66d8d31bd1354e4c89838e4651b6fd`

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`

Prompt: Use case: identity-preserve. Make a FACE-ONLY acting edit of image 1, the full-body pose edit target. Image 2 is a facial emotion reference only (a candidate, not a new identity master); image 3 is the unchanged Milo canonical identity. Sudden panic as his balance tips after tripping: raised inner brows, wide alert eyes and a tense downturned closed mouth, absolutely no smile. Change only eyebrow expression, eyelids, gaze and the closed-mouth crease on image 1. Transfer the worried/panic acting from image 2 into image 1's EXISTING local head yaw, pitch and roll; do not paste the upright portrait head. Preserve the exact head silhouette and head/ear/eye/iris/muzzle sizes, short neck, felt construction and pigment of image 1. Do not change the head angle or inflate the eyes/head to express alarm. Preserve ALL existing torso/belly/cream-patch geometry, limbs, limb connections, hands, feet, tail, articulated pose, position, scale, framing, lighting and transparent silhouette outside the face. Do not redraw or redesign the retained body or make it more chubby/short. No new props, ground, backdrop, shadow, teeth, tongue or speech mouth. Narrator audio does not animate speech. Genuine transparent alpha. Keep full character, ears, whiskers and tail with the same existing margins. Exactly one output, no variations. This is local acting applied to the pose, not a new portrait or a replacement canonical.

### 2. milo.tumble.flank_to_face.3q:support_lost

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_tumble_flank_to_face_support_lost_3q_r002_candidate.png`

Uses: S05-L009-B01-I01

- pose: `character/characters/lion_and_mouse_v7/Milo/poses/milo_tumble_flank_to_face_support_lost_3q_r001_candidate.png` — SHA-256 `4e7db2fdbc3e37f09b1b1e4177e9546c049cbeb02bce177fcbf3a3ec0b966653`

- expression: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_expression_falling_panic_3q_r001_candidate.png` — SHA-256 `aeb779f17676f06aa838b519c019110b3d66d8d31bd1354e4c89838e4651b6fd`

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`

Prompt: Use case: identity-preserve. Make a FACE-ONLY acting edit of image 1, the full-body pose edit target. Image 2 is a facial emotion reference only (a candidate, not a new identity master); image 3 is the unchanged Milo canonical identity. Clearly frightened as support disappears: worried raised brows, wide eyes and a tense downturned closed muzzle. He is falling, not joyfully flying; no smile. Change only eyebrow expression, eyelids, gaze and the closed-mouth crease on image 1. Transfer the worried/panic acting from image 2 into image 1's EXISTING local head yaw, pitch and roll; do not paste the upright portrait head. Preserve the exact head silhouette and head/ear/eye/iris/muzzle sizes, short neck, felt construction and pigment of image 1. Do not change the head angle or inflate the eyes/head to express alarm. Preserve ALL existing torso/belly/cream-patch geometry, limbs, limb connections, hands, feet, tail, articulated pose, position, scale, framing, lighting and transparent silhouette outside the face. Do not redraw or redesign the retained body or make it more chubby/short. No new props, ground, backdrop, shadow, teeth, tongue or speech mouth. Narrator audio does not animate speech. Genuine transparent alpha. Keep full character, ears, whiskers and tail with the same existing margins. Exactly one output, no variations. This is local acting applied to the pose, not a new portrait or a replacement canonical.

### 3. milo.tumble.flank_to_face.3q:tumble

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_tumble_flank_to_face_tumble_3q_r002_candidate.png`

Uses: S05-L009-B01-I02

- pose: `character/characters/lion_and_mouse_v7/Milo/poses/milo_tumble_flank_to_face_tumble_3q_r001_candidate.png` — SHA-256 `51d3737bd9547a443fbd8314ad2ca525eef209494d021f80dc0f600ccebe706a`

- expression: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_expression_falling_panic_3q_r001_candidate.png` — SHA-256 `aeb779f17676f06aa838b519c019110b3d66d8d31bd1354e4c89838e4651b6fd`

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`

Prompt: Use case: identity-preserve. Make a FACE-ONLY acting edit of image 1, the full-body pose edit target. Image 2 is a facial emotion reference only (a candidate, not a new identity master); image 3 is the unchanged Milo canonical identity. Panic during the uncontrolled tumble: raised worried brows, wide alarmed eyelids and tense downturned closed mouth; no smile or playful acting. Change only eyebrow expression, eyelids, gaze and the closed-mouth crease on image 1. Transfer the worried/panic acting from image 2 into image 1's EXISTING local head yaw, pitch and roll; do not paste the upright portrait head. Preserve the exact head silhouette and head/ear/eye/iris/muzzle sizes, short neck, felt construction and pigment of image 1. Do not change the head angle or inflate the eyes/head to express alarm. Preserve ALL existing torso/belly/cream-patch geometry, limbs, limb connections, hands, feet, tail, articulated pose, position, scale, framing, lighting and transparent silhouette outside the face. Do not redraw or redesign the retained body or make it more chubby/short. No new props, ground, backdrop, shadow, teeth, tongue or speech mouth. Narrator audio does not animate speech. Genuine transparent alpha. Keep full character, ears, whiskers and tail with the same existing margins. Exactly one output, no variations. This is local acting applied to the pose, not a new portrait or a replacement canonical.

### 4. milo.tumble.flank_to_face.3q:roll

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_tumble_flank_to_face_roll_3q_r002_candidate.png`

Uses: S05-L009-B01-I03

- pose: `character/characters/lion_and_mouse_v7/Milo/poses/milo_tumble_flank_to_face_roll_3q_r001_candidate.png` — SHA-256 `1dfac13eb95f0ab2d0cd0736a8d1020fcc08f52b651b48fdb6bb9d966686d327`

- expression: `character/characters/lion_and_mouse_v7/Milo/expressions/milo_expression_falling_panic_3q_r001_candidate.png` — SHA-256 `aeb779f17676f06aa838b519c019110b3d66d8d31bd1354e4c89838e4651b6fd`

- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`

Prompt: Use case: identity-preserve. Make a FACE-ONLY acting edit of image 1, the full-body pose edit target. Image 2 is a facial emotion reference only (a candidate, not a new identity master); image 3 is the unchanged Milo canonical identity. Worried disorientation during the roll: uneven worried brows, alert tense eyes and a downturned closed mouth; no smile. Keep the existing sideways head roll exactly. Change only eyebrow expression, eyelids, gaze and the closed-mouth crease on image 1. Transfer the worried/panic acting from image 2 into image 1's EXISTING local head yaw, pitch and roll; do not paste the upright portrait head. Preserve the exact head silhouette and head/ear/eye/iris/muzzle sizes, short neck, felt construction and pigment of image 1. Do not change the head angle or inflate the eyes/head to express alarm. Preserve ALL existing torso/belly/cream-patch geometry, limbs, limb connections, hands, feet, tail, articulated pose, position, scale, framing, lighting and transparent silhouette outside the face. Do not redraw or redesign the retained body or make it more chubby/short. No new props, ground, backdrop, shadow, teeth, tongue or speech mouth. Narrator audio does not animate speech. Genuine transparent alpha. Keep full character, ears, whiskers and tail with the same existing margins. Exactly one output, no variations. This is local acting applied to the pose, not a new portrait or a replacement canonical.

## Review and verification

Original PNGs, same-basename sidecars and receipts are preserved. Later results become new r002 candidates in the current gallery with exact source/output hashes. Owner approval of generation does not pass a candidate. No full unit-test suite is run for this image-only change. Check native images, transparent alpha, source/output hashes, receipts and gallery links; run the full suite once before a commit, with focused checks only where code changes justify them.
