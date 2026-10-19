# Current selected keyframe sheets

These sixteen scene sheets and manifest are reusable presentation files. The completed owner review is closed; historical galleries and alternatives were removed. Selected paths/hashes come from `stories/lion_and_mouse_v6/keyframe_plan.json`, with owner decisions in `owner_visual_acceptance.json`. Sheets do not grant technical approval.

From the repo root, rebuild on Linux or macOS with Pillow:

```bash
python3 production/build_keyframe_contact_sheets.py --story lion_and_mouse_v6
```

On macOS the Swift builder also works: `swift production/build_keyframe_contact_sheets.swift "$PWD"`. Review full-size selected images for technical evidence.
