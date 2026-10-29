# Retained source provenance — not active candidates

Owner-directed S01–S05 cleanup moved superseded image/sidecar files out of active scene/pose directories. Their bytes and original hashes are preserved for immutable operation inputs, canonical lineage and visual-audit reproducibility. They are not accepted or selectable scene images.

INDEX.json maps original logical paths to exact retained files. `audio_visual_plan.source_file` is an explicit read-only resolver, verifies archive containment and hashes, and does not redirect normal write paths. Current selected images and canonical bytes are required at their active paths. The loopback review server resolves only explicitly allowlisted historical media URLs; the archive is not served as a browsable directory.

Current production selection is `../../scene_image_selection_s01_s05.json`. Do not regenerate from historical operations or infer approval from these source files. Removal details/hashes are in `../../review/selection_cleanup_s01_s05_r001/CLEANUP_MANIFEST.json`.

## Superseded scene-composition revisions

Keep the exact currently selected scene still and its sidecar in the active
`character/characters/lion_and_mouse_v7/interactions/scene_compositions/` folder.
After an exact-hash owner selection replaces an earlier revision of the same
image ID, run the archive command from the repository root:

```bash
python -m production.archive_superseded_scene_compositions --repo .
python -m production.archive_superseded_scene_compositions --repo . --apply
```

The first command is a dry run. The second moves only verified older PNG/JSON
pairs and adds their original paths and hashes to `INDEX.json`. Unselected
newer candidates stay in the active folder for review. Historical records are
not rewritten; use `production.audio_visual_plan.source_file` for read-only
access to an archived original path. Active selected assets must still exist at
their declared paths. Do not delete the archive until its recorded dependencies
and owner decisions have been rechecked for the final production version.
The local `.gitignore` exception in the archived scene folder ensures copied
PNG bytes are included when committing the move; check that Git tracks both
the PNG and JSON before treating the archive as portable.
