**Sequence integration, 24 October 2026:** Local endpoint-chain implementation and blocked real-media boards are in [sequence readiness](review/sequence_readiness_r001/COMPLETION.md). Read [the implemented contract](../../docs/sequence-production.md). Selected stills, technical compatibility, render authorization and reviewed video takes remain separate. Earlier dated production statuses below are historical.

**Current S01–S05 selection and cleanup, 23 October 2026:** All 44 current scene images are owner-selected at exact hashes in [scene_image_selection_s01_s05.json](scene_image_selection_s01_s05.json). Read [selected_images/README.md](selected_images/README.md). Active scene folder/gallery contain selected images only; 212 superseded image/sidecar files moved to hash-checked source history, not active candidates. Canonical/current performance/selected scene/audio bytes and the S01–S03 handoff remain unchanged. Twenty-seven authored keys still lack selected images; selection so far does not mean complete video coverage. Earlier statuses below are historical.

**S04–S05 candidates:** [Current review](review/character_performance_consistency_r001/s04_s05_pose_planning_r001/REVIEW.md): 15 transparent Milo pose candidates saved; one forward-pitch request has an unresolved connection failure, with no retries. Leo identity bytes are owner-reconciled in [the exact-hash record](owner_leo_canonical_reconciliation_r001.json); his pose generation remains a separate proposed operation. All new poses await review, and scene-contact/anatomy measurements remain pending.

**S04–S05 next pose pass:** [Requirements](review/character_performance_consistency_r001/s04_s05_pose_planning_r001/PERFORMANCE_REQUIREMENTS.md) and [exact Milo proposal](review/character_performance_consistency_r001/s04_s05_pose_planning_r001/OPERATION.md) plan 16 new Milo pose variants, with four Leo sleeping/portrait requirements held on canonical-byte reconciliation. No generation submitted. S04 is independent per line; S05-L001 reveals Leo, L002–L004 cut to sleeping details, L005–L009 share one planned locked background, L008 has four keys, and L010–L011 share portrait body geometry. S01–S03 selected bytes remain unchanged.

**S01–S03 handoff, 21 October 2026:** The owner selected all 26 current images at exact hashes in [scene_image_selection.json](scene_image_selection.json). Read [LUMI handoff](handoff/s01_s03/README.md) for verified image inputs, separate WAV transfer and CPU-only pilot preparation. Single-image animation tests are possible; complete audio-aligned endpoint sequences are not yet ready. All 161 r001 lines are recorded locally; S13–S16 remain pending visual authoring. Previous dated candidate/pending descriptions below are historical.

# V7 source of truth

[audio_visual_plan.json](audio_visual_plan.json) is the sole authored image-planning authority. [Workflow](../../docs/audio-line-visual-workflow.md) defines audio scenes, lines, beats, views and explicit continuity.

- Current timing: actual local r001 line WAV samples; matching JSON supplies recorded text/speaker/style/hash; versioned timing.json summarizes available scenes.
- Character identity and exact approval scope: [character_library.json](character_library.json). Preserve byte provenance; Leo has an unresolved ledger/actual-byte mismatch, not a new approval.
- Location identity: [location_library.json](location_library.json), families and views. Approved masters remain untouched references; planned views are unapproved.
- Persistent state: authored world_states, world_events and state_rules in the plan. Cuts never reset state.
- Human review: [derived inventory](derived/AUDIO_VISUAL_INVENTORY.md). SCRIPT.md, audio_manifest.json and dialogue_coverage.json are derived references, never competing timing truth.

S01–S16: all 161 current line pairs. The 63 later lines need visual authoring and phrase alignment. Snapshot provenance and retired paths are in [migration record](AUDIO_VISUAL_MIGRATION.json). Old paired records and historical audio hashes are confined to the dated history snapshot.

Latest owner direction: [scene continuity policy](../../docs/scene-continuity-policy.md). Opening shots may use independent forest places. `fork_decision` (S03-L006–L008) is the first exact-background lock. Earlier background approvals remain historical asset approvals, not new opening selections; the 81-background operation is superseded.

## Performance planning and review

The [versioned performance library](character_performance_library.json) owns reusable pose/expression requirements, while the existing audio-visual plan owns per-image bindings. Read the [contract](../../docs/character-performance-library.md), [derived requirements](derived/PERFORMANCE_REQUIREMENTS.md) and [native-image audit](review/character_performance_consistency_r001/REVIEW.md). Current generated/selected performance status is recorded at exact hashes in the library and scoped acceptance ledgers. Earlier foundation-pending/no-approval descriptions are historical; performance selection remains separate from scene and anatomy readiness. Identity, performance approval, shot staging and scene approval are distinct. Leo identity is reconciled by the exact-hash owner record; later visual authoring and sequence readiness remain pending.
