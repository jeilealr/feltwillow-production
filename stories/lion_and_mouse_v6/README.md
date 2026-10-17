# The Lion and the Mouse v6

The selected set contains **96 active 1920×1080 images, one per frame ID**. The completed perceptual-world selection was followed by 47 focused C-style integration finishes; 49 images retain their original bytes. The owner preferred trial C and delegated the rollout; the agent inspected and selected the remaining finishes. Open [the current scene sheets and full-size images](KEYFRAME_REVIEW.md). [owner_visual_acceptance.json](owner_visual_acceptance.json) binds the decision to the exact active bytes. No v6 video takes or assembled edit exist yet.

## Current image authorities

Read [PERCEPTUAL_WORLD_POLICY.md](PERCEPTUAL_WORLD_POLICY.md) for v6 composition rules and [the generation guide](../../docs/keyframe-regeneration.md) for the workflow. The current visual bible defines identity, approval scope, locations and props; staging defines physical support/depth and proposed generation geometry; the keyframe plan defines selected file paths/hashes. A selected image does not automatically approve a setup-size calibration. When staging differs from a selected composition, reconcile the proposed geometry and its authority before generating again; never replace accepted bytes merely to match an older target.

Milo's selected full-body master is `character/characters/lion_and_mouse_v6/Milo/canonical/full-body_milo_neutral_pose_r02_candidate.png`; his atlas is `Milo/references/m_complete_reference_r03_candidate.png` under that character root. Use the exact existing atlas pose first: crouch is third column, third row; walk is third column, second row. Preserve compact anatomy, both ears, small green eyes and felt material. **No visible Milo teeth**, including gnawing and dialogue. Leo's canonical and expression board remain approved; his consolidated atlas is pending. The hunter-net design is approved; the acorn reference is pending. Exact hash-bound scopes are in [visual_bible.json](visual_bible.json).

At equal depth, neutral standing-equivalent Milo/Leo height targets 0.25, with a 0.22–0.28 review range. A crouch or a lying lion does not change anatomy. Improve readability through camera framing, contact/proximity staging and detailed speaker views; scale the environment with the actor for a camera zoom. Compare head/ear/mane dimensions through a sequence. `s07_p01` is the selected shared-composition example. `s09_p02` retains its separately scoped owner scale exception. `s12_p04` explicitly retains tiny Milo in a large environment. **Scene 15 keeps Milo left and Leo right**, with matching portrait eyelines.

Close-ups show complete head/ears/mane, shoulders and upper chest; lower torso, feet and tail stay outside the crop. For expression-only changes, freeze body, ears, mane outline, posture, crop and background. Preserve the owner's selected Scene 16 closing expressions. Keep a single stable connected net and the same main knot; camera crops of selected gnawing composites preserve mouth-to-knot pixels. A pose change never authorizes redesigning rope topology. Boundary stills are closed-mouth; character dialogue motion is added later, narrator speech never drives lips.

## Completed review and reusable sources

Follow [the reusable integration rules](../../docs/character-background-integration.md) after composing a consistent geometric base. Finishing changes local illumination/material integration, never the registered camera, physical scale or prop topology.

The completed galleries, alternate keyframes, previews, masks, duplicate backgrounds and one-off builders have been removed. [image_sources/cleanup_manifest.json](image_sources/cleanup_manifest.json) records every removed path/hash and a Git recovery commit. No approved active PNG changed during cleanup. Historical Git recovery is provenance only; it does not authorize using an owner-rejected image as a new generation base.

Selected reusable RGBA layers are under `character/characters/lion_and_mouse_v6/interactions/sources/`. Current props and retained style/pose/scale references live outside review directories. [image_sources/](image_sources/) retains selected composition receipts, layer prompts and the owner adoption receipt. Original receipt paths describe generation time; use the cleanup manifest's path aliases for relocated files, or its Git commit for archived derivatives. Receipts do not grant new identity, prop or scale approvals.

The completed integration comparison and exact processing receipts are in [review/integration_finish/](review/integration_finish/README.md); original composites are preserved under `interactions/sources/integration_originals/`. These new finishing records are separate from the earlier cleaned review. The **16 current scene sheets plus their manifest** remain under `character/characters/lion_and_mouse_v6/interactions/keyframes/.review/contact_sheets/current/`. These are reusable and required by the review validator. A future review can start from the current selected images and create a new revision folder; never rerun archived builders that reset current selection records.

Rebuild sheets on Linux or macOS after changing selected image bytes:

```bash
python3 production/build_keyframe_contact_sheets.py --story lion_and_mouse_v6
```

This requires Pillow. The macOS Swift builder remains available. Contact sheets are screening aids; technical review requires full-resolution images.

## Technical gates and continuing production

Visual selection and the authorized integration rollout are complete; individual owner review of the 46 delegated finishes is not claimed. Technical authority, anatomy, measured scale and support evidence remain pending. The current counts are generated in [regeneration_authority_blockers.json](regeneration_authority_blockers.json); do not rely on counts from earlier audits. Preserve these gates before timing/export and video production. Legacy pending-review status fields are compatibility fields, not regeneration orders. Historical prompts and rejection records remain immutable provenance; the current hash-bound owner ledger controls visual selection.

Run from the repository root with Python 3.11 or newer:

```bash
python3 production/staging_contract.py --story lion_and_mouse_v6
python3 production/check_pose_coverage.py --story lion_and_mouse_v6
python3 production/keyframe_reference_gate.py --story lion_and_mouse_v6 --write-contract
python3 production/perceptual_world.py --story lion_and_mouse_v6
python3 production/check_keyframe_review.py
python3 production/keyframe_visual_gate.py --story lion_and_mouse_v6
python3 production/v6_runtime.py --story lion_and_mouse_v6 --preflight
```

Approval gates currently exit nonzero for outstanding technical evidence; do not fabricate passes. Read [RUNTIME_CONTRACT.md](RUNTIME_CONTRACT.md) before explicit timing/export. V6 uses `keyframe_boundary_v1`, not a prompt manifest, legacy timing plan or renderable story YAML. No video-control implementation was changed by the image cleanup.

The 70 overview panels and 26 supplemental images serve 52 visual units across 16 scenes. The owner authorized the exact 161 unchanged v5 English line recordings and 16 assembled scene tracks, totaling 11:23.7; [audio_manifest.json](audio_manifest.json) records hashes. Do not reuse v5 visuals, clips or renders. Ignored `work/` audio must be restored separately from a workstation/backup/LUMI; a Git clone cannot recover it. `FELTWILLOW_WORK` can redirect storage. LUMI environments, model weights, Slurm access and credentials are provisioned separately. Use `/scratch/project_465002727/jelealro/tmp` for temporary LUMI runs.
