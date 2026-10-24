# V7 selected S01–S05 images

Current authority: [scene_image_selection_s01_s05.json](../scene_image_selection_s01_s05.json). The owner accepted all current images on 23 October 2026. It contains **44 unique selected images / 45 scene uses**: S01 10, S02 6, S03 10, S04 5, S05 13; L006 reuses L005 exactly with its own WAV.

The active scene PNG folder now contains only those 44 selections. Filenames retain their original revision/candidate creation names so hashes and receipts remain traceable; the current ledger owns selection status. Selected scene bytes, canonical images, performance source pixels and WAVs were not changed. Historical sidecars still describe generation-time candidate status; do not rewrite receipts as owner approval.

Rebuild the selected-only gallery with the documented feltwillow interpreter:

```bash
/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/performance_review_gallery.py --story lion_and_mouse_v7
```

Gallery: `http://127.0.0.1:8765/stories/lion_and_mouse_v7/review/character_performance_consistency_r001/pose_library/review.html` (defaults to selected scenes; use the menu for selected reusable performances). Audio playback, filters, native-pixel mode and canonical measurement page remain available.

[SHA256SUMS](SHA256SUMS) identifies every selected original image. [IMAGE_REUSE.json](IMAGE_REUSE.json) records L006 reuse. [COVERAGE_GAPS.json](COVERAGE_GAPS.json) lists **27 authored keys still missing selected images**. Available selections are not a complete audio-aligned motion sequence or approved Wan clips. Existing contact/anatomy/portrait-clearance and geometry limitations remain documented.

The original S01–S03 selection ledger and LUMI handoff remain byte-for-byte compatible. Do not assume that handoff now renders S04/S05 or that missing endpoints have been created. No new generation or GPU job is authorized by this cleanup.

Superseded images/sidecars required to trace source lineage are in `history/retained_sources/`, outside active production folders. Read-only resolvers check their original hashes; active selected images must exist at their real paths. Current unapproved performance references for unfinished shots remain pending, not silently promoted or deleted.
