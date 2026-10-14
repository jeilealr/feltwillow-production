# v6 keyframe contact sheets

Use [`current/`](current/) to browse scene thumbnails. They were built from the
active `keyframe_plan.json` candidates and each tile names the exact revision.
The supplementary [`current/material_color_comparison.png`](current/material_color_comparison.png)
shows new Leo material trials beside their active originals. Its right-hand
tiles are explicitly rejected calibration images, not active keyframes.
Open the linked full-size PNG in `KEYFRAME_REVIEW.md` before making a visual
decision. A contact sheet is a navigation aid, not approval.

Older sheets were removed to keep this folder unambiguous. Rebuild `current/` whenever any active keyframe changes.

After revising a candidate on macOS, from the repository root run:

```sh
swift production/build_keyframe_contact_sheets.swift "$PWD"
python3 production/check_keyframe_review.py
```

The manifest in `current/` records the candidate paths and hashes represented
by the sheets, so the checker detects stale previews and Markdown links.
