# Seed-foraging correction r003

Exactly one `image_gen.imagegen` request; transparent background; no retries; model/seed/price not exposed; cost unknown.

## Exact references

- `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — canonical_identity; SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`.
- `character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_berry_thicket_3q_r001_candidate.png` — primary_head_body_proportion_target; SHA-256 `3e6bf489a5b2f04585eda046a6467c51b621c7538584a957ab754c55f5c41233`.
- `character/characters/lion_and_mouse_v7/Milo/poses/milo_inspect_log_3q_r002_candidate.png` — owner_passed_bent_knee_body_reference; SHA-256 `c451247d30eb261ee3dfe5b0a3247c5c35d9d54b403d257abca478bd5b417ac4`.
- `character/characters/lion_and_mouse_v7/Milo/poses/milo_forage_seeds_3q_r002_candidate.png` — rejected_seed_action_target; SHA-256 `bdf2fd18b2739e9ded818fa9e560a39e9b867fd584e76bc9f6aa5bec6572a1dd`.

## Exact prompt

Create one corrected seed-foraging Milo character on true transparency. References in order: 1 canonical identity, 2 owner-preferred berry pose proportions, 3 newly owner-passed log-inspection pose, 4 rejected seed-foraging image. Use the accepted LOG POSE as the main body construction and camera/depth starting point, keeping its head size, head/torso balance, readable ribcage length, lean waist, leg lengths and knee bend. Make the minimum change needed to forage: angle the gaze gently downward, lower one arm toward seed-picking height, retain the other for balance, and add only a shallow forward hinge while keeping the head vertically above the forward shoulder rather than thrust toward the camera. A modest squat or low reach is preferable to an exaggerated deep crouch. Do not inherit the rejected seed image's huge foreground head and shortened hidden torso. Keep the berry pose's head-to-body anatomical balance; do not enlarge skull or ears, shrink the torso, swell belly, or stretch limbs. Camera remains compatible three-quarter screen-right with restrained perspective. Both feet on one support plane, full head and ears, both hands/feet and entire orange tail inside frame with margin. Preserve canonical grey needle-felt wool, cream muzzle/chest inset, green eyes, charcoal nose, closed mouth and no teeth. One mouse, no seeds, ground, props, forest, text, watermark or cast ground shadow. Transparent alpha, neutral studio illumination. This is a seed-picking body pose, not a portrait.

Output: `character/characters/lion_and_mouse_v7/Milo/poses/milo_forage_seeds_3q_r003_candidate.png`. No request submitted.
