# Whole-acorn and shared S02 setup · two proposed edits

Endpoint `image_gen.imagegen`; **2 requests**, one opaque 16:9 candidate each, zero retries, model/seed tool-managed, **cost unknown**. Operation SHA-256 `e6a704e8fc6885af47111da62c1ff26f88654635ab31a672f7bd7647c5b0fc33`. No submissions.

24 current candidates retained unchanged. S01 I04 is a future planned eating endpoint only, not an extra request.

## S01-L004-B03-I03

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B03-I03_key_acorn_glade_r005_candidate.png`

- edit_base: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S01-L004-B03-I03_end_acorn_glade_r004_candidate.png` · `41415c64e02e2d3450fb40bf0eba545d29c77cb00426344daffcff020f37ea93`
- S02_shared_setup_actor_and_acorn_size_reference: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L004-B01-I02_end_stone_beside_stream_r004_candidate.png` · `6ef75aae6378cd2d7710d937b427b13d8b9180bfe8794cdceec2515d72720cfd`
- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`

```text
Edit reference 1 into ONE 16:9 Feltwillow still. Change ONLY the acorn to its WHOLE pre-eating condition: completely restore the small missing patch and pale exposed interior beneath the cap to uninterrupted orange-brown felt nut shell. No bite notch, hole, pale eaten patch or missing piece anywhere. Keep cap/stem and whole prop physical size consistent with reference 2 relative to Milo head/hands; reference 2 is size/design only, not setting. Preserve reference-1 Milo pose, grey felt anatomy, face, cream chest, lean body, orange tail, grip, afternoon background and camera. Reference 3 is canonical identity. This still precedes future eating/chewing animation; no visible teeth, mouth closed, no eating already baked into the acorn. No text/watermark/corner symbol. Do not change the scene to the sunset reference.
```

## S02-L001-B01-I02

Output: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L001-B01-I02_end_evening_glade_r005_candidate.png`

- edit_base_shared_setup_actor_and_acorn_size: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L004-B01-I02_end_stone_beside_stream_r004_candidate.png` · `6ef75aae6378cd2d7710d937b427b13d8b9180bfe8794cdceec2515d72720cfd`
- upward_gaze_semantic_reference_only: `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S02-L001-B01-I02_end_evening_glade_r004_candidate.png` · `34dfdfd0b299aefbbc897da561f4f86a6b09a06e12ece653e41dcd5d3b1e0040`
- canonical_identity: `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` · `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`

```text
Edit reference 1 (S02-L004 standing at the stone-stream setting) into ONE 16:9 Feltwillow still for S02-L001. USE REFERENCE 1 AS THE COMPLETE SCENE BASE: retain the same background pixels, stone/stream/trees/sunset, camera/lens/crop, light, Milo torso/feet/root position, standing depth and apparent character scale. Keep the SAME acorn physical size and small eaten patch/cap/stem from reference 1. Do not enlarge the acorn and do not resize Milo. Change ONLY Milo head/eyes/gaze toward the fading sky as he finally looks up, preserving compatible head/ear/neck anatomy and intrinsic proportions. Reference 2 supplies semantic upward-look/emotion ONLY; do NOT copy its old background, larger acorn or actor placement. Reference 3 supplies canonical identity. Empty extra space remains unchanged; only one Milo and one acorn, same grip/prop custody. No walking, foot relocation or torso rebuild, no teeth/open still mouth. No text, watermark or corner symbol. This belongs to the same location/setup as the later standing -> crouch -> contact -> release, not a new forest scene. Exact background/root matching must be checked after generation.
```

Current operation SHA-256: `e6a704e8fc6885af47111da62c1ff26f88654635ab31a672f7bd7647c5b0fc33`. The JSON is the exact request authority. S02 reference 1 is the edit base; reference 2 controls upward gaze only.
