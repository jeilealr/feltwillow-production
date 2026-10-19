# Leo r04 — final eye cleanup

18 October 2026. Owner expressed satisfaction with r03's appearance, requested
remaining felt over the left eye and optional feature inspection. "Milo" was
interpreted as Leo in the ongoing Blender task; no Milo asset was changed.
This records the owner's stated satisfaction, not a broader canonical release
or approval of untested animation behaviors.

Open `../assets/characters/leo/leo_canonical_tripo_candidate_r04.blend`.
SHA256 `6dd932b97536a96925edcb4d76a1f87ed18464b35b13fedf637253d59d891302`.
Source r03 preserved at SHA256
`e337d6708236f8b57da8853b59f9dcc6edc9643392ffbe52e5135cffedc21fa2`.
User's live Blender session and canonical images untouched. No external calls,
uploads or additional spending. Original PATINA/FBX provenance and broader
remaining limitations remain in the r03 report.

## What changed

An actual frontal macro render confirmed strands crossing the iris on the
viewer's left. The earlier absolute-X eye mask assumed a symmetric head,
whereas this character's posed eyes have different offsets and heights.
Located each eye from the existing orthographic front image, ray-cast onto
the surface, then checked every vertex along each strand in a small local
elliptical eye envelope. Cleared 125 additional whole strands (104 near the
viewer's left eye and 21 near the right); 143,842 strands remain visible.

Reused the existing transparent feature-mask material, preserving all geometry,
vertex indices, UV colors, skin weights and rig bindings. No surface geometry,
face proportions, pigment, expression, lights or material look was redesigned.
Both enlarged before/after views show the local clearance. The face inspection
did not justify further feature enhancement: retain the current eyes, eyebrows,
nose, muzzle and friendly closed-mouth expression rather than reopen lookdev.

## Evidence and checks

`../renders/leo_tripo_canonical_r04/eye_cleanup_comparison.png` shows actual
matched enlarged renders. `portrait.png` and `full_body.png` show the result
at normal viewing distance. `head_left.png` and `head_right.png` check the two
small head turns; `controlled_rig_audit.json` measures the same bounded 49-frame
head-turn/plant test used in r03. Main surface remains closed/manifold, weights
normalized, paws planted within the existing tolerance, 80 sampled groom roots
attached, six cream whiskers head-bound, and all file images packed. This is
limited technical evidence, not a walk, crouch, facial-animation or collision
qualification. No new continuous motion sequence was rendered; only the two
head-turn stills and existing 49-frame numerical audit were rerun for this edit.

`operations.json` records the per-eye centers/envelopes and strand counts.
`render_manifest.json` records four final still settings and hashes;
`delivery_manifest.json` binds all review outputs, operations and implementation
to the saved asset and source hashes. Before/after pair settings: Cycles CPU,
1000×800, 40 samples, denoising, fixed seed 18102606, Standard/None, exposure 0,
gamma 1, matching frontal face camera. It is a geometry-visibility cleanup, not
an image repaint. Rendering used Blender 5.2.2 LTS d13f752e3b9c.

The file opens at neutral frame 1, Material Preview and the existing review
camera. Use Render → Render Image for saved studio lighting. No additional
facial changes are recommended for this finishing pass. The r03 report's
canonical wool/atlas limitations remain; this version retains the appearance
the owner liked.

## Reproduce without paid services

From repository root, using the installed Blender executable:

```sh
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_r04_eye_tidy.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_r04_review.py
python3 blender/scripts/leo_r04_boards.py
```

On this Mac: `/Applications/Blender.app/Contents/MacOS/Blender`; Pillow is needed
only for the comparison board. No Git commands or production-image changes.
