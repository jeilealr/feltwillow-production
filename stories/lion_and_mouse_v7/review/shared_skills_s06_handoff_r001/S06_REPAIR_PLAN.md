# S06 bounded repair handoff

Baseline: `4e46daf`. Owner feedback in the current task supersedes earlier technical visual suggestions. All three candidates remain unselected. All other S06 images are to be preserved; “good” feedback does not create canonical, performance, animation or exact-hash scene approval.

## Exact inputs

- `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S06-L001-B02-I01_scramble_descent_r006_candidate.png` — SHA-256 `f385d913f123ff72e1e1480b3acf79767ebf04add06699049974bd63181c9d41`
- `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S06-L002-B01-I01_front_paw_ready_r005_candidate.png` — SHA-256 `4dd4a6307ca7ae60a4865b3b255a629d3fb498989ab019de07d9f1f5f306a85d`
- `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S06-L002-B01-I02_front_paw_descending_r005_candidate.png` — SHA-256 `bd14846ab15e15475cc4ad54a81cabcdcd824d152435e8f45b65dbdc171639c9`
- `character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png` — SHA-256 `c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f`
- `character/characters/lion_and_mouse_v7/Leo/canonical/full-body_leo_neutral_pose_r01.png` — SHA-256 `1c4f773d04c5e6f7229448bfe00caf7f610d427f5dc0d145cba57e7671a59362`
- `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S06-L001-B01-I01_start_rest_nose_r001_candidate.png` — SHA-256 `bc914de64088c20665c254e5e7a84a96bfaf282cb0d12781c42e0a61ff964dfd`
- `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S06-L001-B02-I02_end_path_arrival_r001_candidate.png` — SHA-256 `2933f39200694de8b8ca03b9ece22ea204b5d5aa88e6d3a63ca5c22f63de46b0`
- `character/characters/lion_and_mouse_v7/interactions/scene_compositions/S06-L002-B01-I03_end_front_paw_block_r001_candidate.png` — SHA-256 `c8a49ebe6bfc11eb69e07f307367e6cf6c304f3e8a0ab81e1339e466302fbd19`

## Three proposed operations

1. **Scramble r006: re-create Milo’s incorrect body.** Use the existing scene as edit base, Milo canonical for identity/anatomy, selected S06 rest/nose anchor for starting relationship, and selected path-arrival anchor for destination/projection. Preserve Leo, scene landmarks, sunset/light, camera and valid identity features. GPT must inspect the wrong body at native size and rebuild a coherent whole-body scramble down toward the path, with attached limbs and grounded/transition support. Do not stretch separate body parts to fit. Proposed output: `S06-L001-B02-I01_scramble_descent_r007_candidate.png`.

2. **Paw-ready r005: targeted Leo paw edit.** Use r005 as edit base, Leo canonical for species/anatomy and selected S06 block/path-arrival anchors for forelimb attachment, support and geography. Preserve the owner-liked **image-upper-right paw**, Milo, Leo face/torso, tail, scenery and other valid features. GPT must identify the other mismatched paw(s) with a native labeled comparison before defining a narrow edit support. No guessed anatomical-right mapping or generic rectangular mask. Proposed output: `S06-L002-B01-I01_front_paw_ready_r006_candidate.png`.

3. **Paw-descending r005: targeted Leo paw edit.** Use r005 as edit base, Leo canonical and selected block anchor; include the repaired ready image only after its actual bytes exist and pass the applicable owner review. Preserve Milo and all valid scene/actor features. Establish a plausible lowering trajectory into the selected blocking state; resolve remaining paw mismatch and limb attachment without adding/losing a limb. Proposed output: `S06-L002-B01-I02_front_paw_descending_r006_candidate.png`.

## GPT handoff and owner gate

Use a GPT session with actual native image inspection and editing capabilities. Load exact inputs above and label each reference role. Confirm provider reference limits; do not silently omit authorities. Preserve source PNGs and receipts. Prepare one scoped output per operation with new immutable path, positive prompt, permitted edit support, ordered references and hashes, provenance and native before/after comparison. No automatic retry. Candidate output filenames are proposals: check nonexistence before writing.

Before execution, obtain concrete provider/model, upload and cost/call authorization. This task authorizes preparation only. No model auto-switch is implemented. If the required capability is unavailable, deliver this packet to a capable GPT session. Do not simulate a successful edit.

Owner review remains required for each returned exact-hash scene candidate. Review anatomy, projected scale, every paw connection/support, protected pixels, lighting and ordered S06 continuity. Source-still selection remains distinct from canonical/performance approval and eventual full-motion/join approval.

Smallest next action: review the proposed three-operation scope, then prepare/authorize the scramble body repair and paw-ready edit; freeze the descending operation’s final references after the ready result is reviewed.
