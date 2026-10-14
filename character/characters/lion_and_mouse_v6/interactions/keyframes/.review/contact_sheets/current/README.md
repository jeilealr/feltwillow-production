# Current Lion and Mouse v6 keyframe review

Open `scene01_keyframes.png` through `scene16_keyframes.png` for the **active**
candidate sequence. Their exact paths and SHA-256 hashes are in `manifest.json`.

Open [`material_color_comparison.png`](material_color_comparison.png) to compare
the new Leo color/texture trials for `s05x_p04` and `s08_p01` with their active
frames. **The right-hand trials are not active replacements:** their character
or background geometry changed, so they failed continuity review. Their source
and trial hashes are in [`material_color_comparison.json`](material_color_comparison.json).
The Scene 05 and 08 active sheets intentionally continue to show the left-hand
versions.

To rebuild the supplementary comparison after editing its source manifest:

```sh
clang -fobjc-arc -fno-modules -framework AppKit \
  production/build_keyframe_material_comparison.m \
  -o /private/tmp/build_keyframe_material_comparison
/private/tmp/build_keyframe_material_comparison "$PWD"
```

If an active source hash changes, the builder stops instead of displaying a
stale comparison. Rebuild the 16 active sheets with
`swift production/build_keyframe_contact_sheets.swift "$PWD"` when an active
candidate changes.
