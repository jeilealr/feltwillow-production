# Retained source provenance — not active candidates

Owner-directed S01–S05 cleanup moved superseded image/sidecar files out of active scene/pose directories. Their bytes and original hashes are preserved for immutable operation inputs, canonical lineage and visual-audit reproducibility. They are not accepted or selectable scene images.

INDEX.json maps original logical paths to exact retained files. `audio_visual_plan.source_file` is an explicit read-only resolver, verifies archive containment and hashes, and does not redirect normal write paths. Current selected images and canonical bytes are required at their active paths. The loopback review server resolves only explicitly allowlisted historical media URLs; the archive is not served as a browsable directory.

Current production selection is `../../scene_image_selection_s01_s05.json`. Do not regenerate from historical operations or infer approval from these source files. Removal details/hashes are in `../../review/selection_cleanup_s01_s05_r001/CLEANUP_MANIFEST.json`.
