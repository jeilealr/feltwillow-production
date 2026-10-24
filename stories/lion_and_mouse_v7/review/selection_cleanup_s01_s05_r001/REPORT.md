# S01–S05 selection and cleanup

44 unique current scene images accepted; 45 uses including L006 reuse. Counts: S01 10, S02 6, S03 10, S04 5, S05 13. Exact hashes and immutable sidecar references in scene_image_selection_s01_s05.json. Original S01–S03 ledger remains unchanged.

Active scene PNG/sidecar directory now contains only 44 selected pairs. 212 superseded image/sidecar source files (213,551,394 bytes) removed from active scene/pose directories and retained in history/retained_sources for source/audit dependencies. They were **relocated, not destroyed**. One regenerable cache was permanently deleted. Current unapproved performance assets for unfinished shots are retained separately and not falsely approved. Canonical/source/selected images and WAVs were not repainted; creation receipts remain historical facts.

Selected-only gallery keeps audio, filters/native-pixel mode, selected performances and canonical measurement access. It explicitly lists 27 planned image keys still missing; existing physical/geometry/portrait warnings remain. No claim of complete S01–S05 video coverage, new motion frames or GPU work.

Validation: current selected PNG decode/hash/sidecar/audio/reuse checks pass; performance planning and audio-visual planning/derive pass; original opening handoff with required audio passes (26 original selections, zero missing WAVs). Twelve focused source-archive/selection/server tests pass. Initial server tests hit sandbox loopback restrictions; rerun with loopback permission passed. Full suite not run per owner cadence; no commit or push.

New permanent code: production/selected_scene_review.py and tests/test_selected_scene_cleanup.py. Explicit read-only source lookup added to audio_visual_plan.py and character_performance.py; allowlisted historical-media handling in serve_scene_review.py; current gallery routes to selected ledger. Exact before/after logical paths/hashes in CLEANUP_MANIFEST.json and history/retained_sources/INDEX.json.

Dependency closure and the explicit historical gallery allowlist identified two rejected PNG outputs with no remaining use; those PNGs and their redundant sidecars (4 files, 4273253 bytes) were permanently deleted after relocation. Immutable receipts remain separate. The provenance archive retains 208 source files required for audit/source continuity or their paired metadata. Exact deletion hashes are in CLEANUP_MANIFEST.json.
