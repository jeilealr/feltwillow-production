# The Lion and the Mouse v6

Current handoff, reconciled 2026-10-16. All **96 current 1920×1080 story images are present and owner-selected**. Open the [complete gallery](review/complete_story_images/owner_review.html) or [scene contact sheets and full-size links](KEYFRAME_REVIEW.md). There are no missing image slots. No v6 video takes or assembled edit exist yet.

The owner accepted the final twelve corrections after the Milo canonical rollout: Scene 04 p01–03; Scene 05 p02–04 and x_p05; Scene 09 p02; Scene 12 p01 and x_p01–03. The other 84 images were retained through the final correction list. [The acceptance ledger](owner_visual_acceptance.json) binds every selection to its current path and SHA-256 and distinguishes explicit final-set acceptance from retained selection inferred from the conversation. It does not claim a separate technical inspection of every frame.

## Current authorities and standing visual rules

Milo's owner-selected family is the early-scene rebuild: `Milo/canonical/full-body_milo_neutral_pose_r02_candidate.png` and `Milo/references/m_complete_reference_r03_candidate.png`, under `character/characters/lion_and_mouse_v6/`. Exact foundation hashes and approval scopes are in [visual_bible.json](visual_bible.json); [MILO_CANONICAL_REVIEW.md](MILO_CANONICAL_REVIEW.md) explains the selection. Leo's canonical and expression board remain approved; his consolidated atlas remains pending. The hunter-net design is hash-bound approved; the acorn reference remains pending.

Keep Milo compact, neutral grey and finely needle-felted, with small green eyes, a modest cream belly and a moderate rust tail. **No visible teeth**, including gnawing and dialogue. Composite characters at the planned scale with convincing contact, occlusion and grounding. Preserve the liked expressions and movement; avoid flattening Milo onto the background. Keep Leo's established body shape, color and felt texture. Expression close-ups show the head, ears, shoulders and upper chest with a stable body silhouette. Keep net topology stable between poses; Milo works on the main knot. Same-depth scale follows staging; pose-sheet cell sizes are not screen-scale authorities.

Scene 09 p02 has an explicit hash-bound Milo-world perspective scale exception in [staging_plan.json](staging_plan.json). Scene 12 close views magnify character and environment together; the wide p04 retains a small Milo. Scene 05 contact and body placement were corrected without globally redrawing the plate. The preserved [Scene 05 style reference](../../character/characters/lion_and_mouse_v6/interactions/keyframes/.review/history/s05_p01_r01_candidate.png) controls brightness and felt texture; the current opening frame is r03.

## What is finished and what remains

Owner image selection is complete. Structured technical validation remains incomplete: the reference gate currently reports **86 current authority blockers** (74 setup-scale, eight daytime-plate and four prop approval dependencies), plus 81 historical provenance warnings. These are dependency counts, not counts of bad images. The visual evidence gate currently reports 1,486 unmet requirements. Full-resolution check fields, actor anatomy/support evidence and measured scale evidence still need reconciliation by inspection. Owner liking the story images does not automatically approve setup calibration assets or fill those checks. Preserve those gates before explicit timing export and video production. Historical rejection hashes concern superseded revisions; none matches the current 96-image selection.

The native pipeline is `keyframe_boundary_v1`. Use [keyframe_plan.json](keyframe_plan.json) for active files/hashes, [keyframe_visual_reviews.json](keyframe_visual_reviews.json) for technical evidence and owner-selection links, [pose_reference_plan.json](pose_reference_plan.json) for poses, and [video_boundary_plan.json](video_boundary_plan.json) for chronological boundary assignments. Legacy `candidate_generated_pending_owner_review` plan statuses remain compatibility fields used by the generation tools; the separate hash-bound owner-selection ledger records the latest owner decision. Do not treat legacy status text as a request to regenerate accepted images. Dated October 13–15 audits describe history; this handoff and current hashes take precedence.

The 70 overview panels and 26 supplemental images serve 52 visual units across 16 scenes. The owner authorized exact reuse of the 161 unchanged v5 English line recordings and text; 16 assembled scene tracks total 11:23.7. See [SCRIPT.md](SCRIPT.md), [audio_manifest.json](audio_manifest.json) and [dialogue_coverage.json](dialogue_coverage.json). Narrator remains voice-over; character speech receives later timed mouth motion. Do not reuse v5 visuals, clips or renders.

## Continuing from a fresh checkout

Read this file, [CLAUDE.md](../../CLAUDE.md), [RUNTIME_CONTRACT.md](RUNTIME_CONTRACT.md) and the current plans before acting. The image selection, visual rules, hash bindings and cleanup receipts are in the repository; prior chat is not required for the recorded decisions. The final correction provenance is retained under `character/characters/lion_and_mouse_v6/interactions/keyframes/.review/final_owner_staging/`.

`work/` audio and runtime outputs are ignored by Git. Restore the exact WAVs and scene tracks from the current workstation, backup or LUMI according to `audio_manifest.json`, and verify its hashes. `FELTWILLOW_WORK` can redirect work storage. A clone alone cannot recover these bytes. Do not rerecord audio as a substitute. LUMI environments, model weights, Slurm access and external-service credentials are also provisioned separately; repository instructions live in `CLAUDE.md` and `lumi/`. No secrets belong in this handoff. Native v6 preflight tolerates absent ignored audio; later export requires it.

Run from the repository root:

```bash
python3 production/staging_contract.py --story lion_and_mouse_v6
python3 production/check_pose_coverage.py --story lion_and_mouse_v6
python3 production/keyframe_reference_gate.py --story lion_and_mouse_v6 --write-contract
python3 production/check_keyframe_review.py
python3 production/keyframe_visual_gate.py --story lion_and_mouse_v6
python3 production/v6_runtime.py --story lion_and_mouse_v6 --preflight
```

Approval gates currently exit nonzero for the outstanding technical evidence above. Do not mark checks passed merely to make export run. There is no v6 prompt manifest, legacy timing plan or renderable story YAML; later explicit timing follows the runtime contract.

## Review presentation and cleanup

The 16 contact sheets in `character/characters/lion_and_mouse_v6/interactions/keyframes/.review/contact_sheets/current/` bind thumbnails to active paths and hashes. Rebuild after any image change with `swift production/build_keyframe_contact_sheets.swift "$PWD"`, then run the review validator. Contact sheets do not replace full-resolution checks.

Obsolete before/after galleries and temporary scripts were removed after owner acceptance. The [cleanup summary](review/complete_story_images/cleanup_summary.json) and [deletion manifest](review/complete_story_images/cleanup_manifest.json) record what was removed. Referenced historical style/scale inputs and generation provenance remain intentionally. Do not delete them solely because they are inside `.review/`.
