# V7 source of truth

[audio_visual_plan.json](audio_visual_plan.json) is the sole authored image-planning authority. [Workflow](../../docs/audio-line-visual-workflow.md) defines audio scenes, lines, beats, views and explicit continuity.

- Current timing: actual local r001 line WAV samples; matching JSON supplies recorded text/speaker/style/hash; versioned timing.json summarizes available scenes.
- Character identity and exact approval scope: [character_library.json](character_library.json). Preserve byte provenance; Leo has an unresolved ledger/actual-byte mismatch, not a new approval.
- Location identity: [location_library.json](location_library.json), families and views. Approved masters remain untouched references; planned views are unapproved.
- Persistent state: authored world_states, world_events and state_rules in the plan. Cuts never reset state.
- Human review: [derived inventory](derived/AUDIO_VISUAL_INVENTORY.md). SCRIPT.md, audio_manifest.json and dialogue_coverage.json are derived references, never competing timing truth.

S01–S12: 98 current line pairs. S13–S16: 63 script lines, no current r001 audio or timed visual readiness. Snapshot provenance and retired paths are in [migration record](AUDIO_VISUAL_MIGRATION.json). Old paired records and historical audio hashes are confined to the dated history snapshot.

Latest owner direction: [scene continuity policy](../../docs/scene-continuity-policy.md). Opening shots may use independent forest places. `fork_decision` (S03-L006–L008) is the first exact-background lock. Earlier background approvals remain historical asset approvals, not new opening selections; the 81-background operation is superseded.
