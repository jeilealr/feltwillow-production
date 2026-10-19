# Leo imported r02: whisker repair, rig trial and felt material

18 October 2026. **Reviewable refinement candidate with an initial rig.**
Open `../assets/characters/leo/leo_canonical_tripo_candidate_r02.blend`.
Final candidate SHA-256: `7d60fb0c9aa96c89458152d09e5e6c88e7566507d58ff9e2a8daef0042a5768a`.
Source r01, raw FBX, maps and approved 2D images are preserved. This revision
does not constitute owner approval or full animation readiness.

## Requested corrections

The supplied screenshots correctly identified another set of whiskers in the
FBX. An isolated color/clay render confirmed three thin dark geometric branches
joined to the cheek. Removed those branches, repaired and smoothed their roots,
and retained the six separate cream curves (three per side). No eye, nose,
mouth-expression or body-proportion redesign was introduced.

The main imported surface went from 48,753 vertices / 48,742 faces with 41
non-manifold edges (40 boundary) to **48,552 vertices / 48,554 faces with zero
boundary and zero non-manifold edges**. Cleanup removed 138 identified branch
vertices, 59 vertices in microscopic islands, and four residual loose vertices;
tiny holes were filled. UVs were retained/interpolated locally. Watertightness
does not establish that every internal self-intersection or joint loop is ideal.

Paws received shallow toe-separation grooves and restrained support corrections.
Their four resolved lowest supporting regions now share Z=0. This preserves the
imported stance and footprint; it is not a complete four-toe resculpt. Rear mane
received shallow fixed rolled creases in 1,373 vertices. An additive curl trial
read as separate rings and was rejected. The delivered surface uses incised
detail instead, protecting the front and overall head silhouette. **The rear
still has a regular rounded-lock arrangement** and would benefit from a later
artist-guided sculpt if a closer canonical rear is required.

## Controlled rig evidence

Added a fitted **25-bone initial quadruped rig** with body/head/tail chains and
four paw IK targets. Skin weights blend the continuous surface; cream whiskers
follow the head. Rebuilt 42,966 attached short wool strands, transferring their
source-triangle weights and source UV colors. The groom is native mesh geometry,
not a simulation or an external hair dependency.

The first body-lift trial exposed insufficient reach in the nearly straight
front chains. Preserved that candidate/audit, refitted the elbows with more
bend reserve, and repeated the same test. The successful test measures every
frame from 1–49: neutral, +12-degree head yaw, neutral, -12-degree yaw, neutral,
then .02 BU pelvis lift with .006 BU lateral shift and return. At .2 m/BU this
is a 4 mm lift of the miniature. The actual motion is stored as an editable action.

`controlled_rig_audit.json` binds current measurements and limits to the saved
candidate hash. All 11 limited checks passed. Maximum measured paw drift was
2.14e-7 BU; sampled wool roots stayed within .000583 BU of their deformed
source triangles, and facial landmark pair distances varied by approximately
0.000101%. It checks main-surface closure, normalized weights, four paw
regions, contact drift, sampled facial rigidity, 80 groom-root attachments,
neutral deformation, preserved r01 bytes, six bound whisker curves and packed
images. Final values/check verdicts are machine-readable there; these are
limited technical checks, not automatic artistic approval.

Thirteen rendered motion samples (frames 1,5,…,49) form
`controlled_rig_preview.gif`, approximately 2.2 s at 6 fps. All 49 frames were
measured; only those thirteen were rendered. The comparison board also shows
the body shift from the side and the head turn in portrait. Walk, lie-down,
crouch, full facial controls, extreme range and full self-collision clearance
remain untested. Do not use the trial as a finished performance or walk cycle.

## Felt and the approved PATINA trial

The owner approved the exact initial trial and allowed up to five attempts if
needed. **Only one generation was submitted.**

- Endpoint: `fal-ai/patina/material/extract`.
- Request ID: `01a14f67-38b6-75c2-a13d-7bbacd6ce06c`.
- Input: a 120×120 crop of canonical body wool, rectangle (285,715,405,835).
  Crop SHA-256: `e4fdc1b3b5831255930894b4ce04ae303a3975d004752202b66cae7666a44856`.
- One 1024-square output; requested normal/roughness/height; seed 18102604;
  eight steps; strength .6; both-axis tiling; no upscale; PNG; safety on;
  prompt expansion requested off. Exact submitted and returned descriptions,
  inputs, source/output hashes and the approval scope are in the trial receipt.
- Published estimate about **$0.15–$0.16**, authorized budget $0.20 for the
  concrete trial. **Actual charge was not returned**. No further attempts used.
- Only the approved small swatch was uploaded. The complete character images
  and FBX were not uploaded for this operation.

All four returned images (extracted texture and three maps) were downloaded
and preserved under `assets/materials/leo_felt_patina_trial/`. Provider schema
and pricing were checked against the current official model page:
https://fal.ai/models/fal-ai/patina/material/extract . It was marked commercial
use when checked; the earlier FBX's generation/license receipt is still unknown.

The candidate uses PATINA height and roughness as restrained surface detail
in stable rest coordinates, with .25 BU tiles. Its normal map is preserved
for a future UV-specific test; it is not incorrectly treated as a world/box
normal map. The extracted texture provides fine wool luminance variation,
normalized around its measured linear mean and bounded to **0.88–1.12** times
the original atlas color. Leo's original UV color atlas remains the pigment
source. No whole-character honey swatch or new global color grade was applied.

An initial groom looked too much like dark isolated curls. The final correction
makes strand lengths/radii 70% of that trial and mixes 40% thin-fiber translucency
into their shader. The first material trial is preserved separately. Stable
surface/UV coordinates and inherited skin weights keep the material and fibers
attached through the small motion test.

Visually, this is a more tactile matte finish, with finer fuzz and felt relief.
**It still does not reproduce the canonical's dense luminous tangled wool
exactly.** Macro detail can read as short curls/velvet rather than fully packed
needle-felt. PATINA supplies useful surface structure, but dense silhouette wool
still depends on geometry, scattering and lighting. The existing color texture
also includes baked eye/highlight/shading information; it is not measured pigment
reflectance. Another seed alone would not solve those limitations, so the
remaining authorized generation attempts were not spent.

## Review and opening

The final review directory is `../renders/leo_tripo_canonical_r02/`:

- `whisker_repair_comparison.png`: source artifact versus final repair.
- `refinement_comparison.png`: r01/r02 three-quarter and rear.
- `felt_material_comparison.png`: local and PATINA material, same geometry,
  groom, color source, camera and illumination.
- `turnaround.png`: eight neutral diagnostic angles.
- `controlled_rig_comparison.png` and `controlled_rig_preview.gif`: actual trial.
- `render_manifest.json`: 29 final still/frame paths, hashes and settings.
- `operations.json`, `controlled_rig_audit.json`, `felt_refinement.json` and
  `delivery_manifest.json`: exact geometry/test/material/output evidence.

The file opens at frame 1, with Material Preview and overlays hidden. Frame 1
is neutral. The timeline's 1–49 action is the small trial; Space plays it, with
viewport speed dependent on hardware. Use F12 for the saved studio render.
No interactive Blender session or user selection was overwritten.

## Reproduction

Using the existing installed Blender 5.2.2 executable from repository root:

```sh
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_tripo_refine_r02.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_r02_rig_felt.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_r02_felt_tune.py -- --apply
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_r02_review.py
python3 blender/scripts/leo_r02_boards.py
```

Pillow is needed only for boards/GIF. The preserved approved PATINA files are
local inputs; rebuilding does not generate, upload or spend. Do not reapply the
fiber refinement to an already-refined groom; its script rejects that state.
Keep the raw import and r01 sources. Generated r02 outputs can be rebuilt, so
preserve a new revision before intentional edits. Test manifests bind actual
candidate bytes; regenerate evidence after any asset change.

## Status and next action

G0 authority: resolved for this scope. G1: improved, owner review pending;
posterior lock pattern and toe forms remain approximate. G2: the bounded
head/plant trial has technical evidence, not broad animation approval. G3:
useful PATINA/native felt comparison and short-motion evidence; canonical
material match remains open. G4/G5: outside this Leo-only task. G6: not released.

Next: review the felt comparison and the short rig clip in context. Keep the
current shape while refining wool density/scattering and checking a longer
turn under grazing light. Expand the rig to a slow supported step only after
that review; a finished walk or advanced face system is premature. No further
Tripo generation is indicated by this work.
