# Leo r03: muzzle repair and finer felt

18 October 2026. Review candidate; owner visual approval pending.

Open `../assets/characters/leo/leo_canonical_tripo_candidate_r03.blend`.
SHA-256: `e337d6708236f8b57da8853b59f9dcc6edc9643392ffbe52e5135cffedc21fa2`.
Source r02, raw FBX, canonical PNG and the user's interactive Blender session
were preserved. Frame 1 is neutral; Material Preview and the review camera
are saved. F12 renders the studio. This denser groom makes the file about
153 MiB and viewport playback may be slower. Hide `Leo_attached_wool_r02`
in the viewport for easier posing; that retained object name is compatibility
with the existing rig audit, not an indication that the old groom remains.

## Muzzle correction

The owner correctly identified an angular dark spot and two smaller remnants.
A matched color/clay diagnostic isolated two problems: three tiny repair caps
had UV corners sampled from unrelated atlas islands, and a slight local pinch
remained. A closed/manifold mesh did not reveal the UV failure. This corrects
an incomplete aspect of the previous repair.

Faces 48508, 48510 and 48511 now sample nearby cream muzzle regions, using a
single small local atlas patch for each cap rather than interpolating across
unrelated UV charts. The original color image was not repainted or replaced. Exposed final renders
caught residual beige staining from shaded old-root pigment. Restricted anchor
selection to clean nearby cream, refreshed nearby groom UVs, then feathered a
small sampled cream pigment correction over .010–.032 BU around each root.
The same rest-space mask suppresses the imported normal map's baked root marks;
continuous PATINA relief remains. This local shader healing removes the seams
without modifying the source atlas or relying on the wool to hide them.
Fairing touched 43 local vertices (ten restrained iterations); maximum movement
was .0027463 BU, about .55 mm at the miniature's .2 m/BU scale. Vertex and face
counts/connectivity are unchanged: 48,552 vertices, 48,554 faces, zero boundary
or nonmanifold edges. The six separate cream whisker curves remain head-bound.

See `../renders/leo_tripo_canonical_r03/muzzle_repair_comparison.png`: matched
color and clay renders with the groom/cream whiskers hidden to expose the area.
`muzzle_final.png` shows the actual final groom and cream whiskers.

## Felt changes and reference comparison

Reused the already-generated PATINA height/roughness/luminance maps. No upload,
paid call, new image generation or additional charge occurred. The original
trial's estimated $0.15–$0.16 cost remains an estimate; its actual charge was not
returned. Its full provenance remains in the r02 report and
`../assets/materials/leo_felt_patina_trial/patina_trial_01_receipt.json`.

The r02 groom had 42,966 coarse short strands and excluded nearly the whole
muzzle. R03 has **144,990 finer attached strands**, including 5,473 in admitted
facial skin regions, with ten points per strand and fixed seed 18102618.
Eye/nose/lip masks protect the features. A macro review caught 1,023
strands whose endpoints crossed the lower eye region; a whole-strand
transparent material now clears that envelope without altering binding indices.
143,967 strands remain visible. Both roots and endpoints are considered for
this feature-clearance mask, rather than trusting root exclusion alone. Shorter face wool and restrained raised
loops maintain the silhouette; this is needle-felt look development, not long
lion fur. Native mesh groom: 4,349,700 vertices. Skin weights and UV pigment are
interpolated from each source triangle; the seed/pattern is fixed through time.

An initial trial was too dark/angular. Its candidate, operation receipt and
previews are preserved as material trial 01. The second trial increased curve
resolution, softened the light response and protected eyes/nose. Its first
highlight setting was too orange, so final fiber reflectance is bounded to
1.45 times source color with a 20% neutral-luminance component, 25% translucency,
retained matte roughness remap .86–.98 and sheen .50. The strand
roughness default is .68, but the inherited connected map controls its effective
value; that default is not the rendered roughness. These are artistic scattering approximations for
the fiber material, not measured physical wool parameters. The surface pigment
atlas remains unchanged; only the requested local muzzle healing overrides its
old-root stains. Reduced PATINA height relief to strength .32/distance
.0022 BU and imported normal strength to .25, reducing the engraved appearance.

Matched neutral body renders show finer overlapping wool and a softer surface
than r02's sparse dark curls. The full figure remains recognizable with its
existing facial expression, proportions, mane masses and closed tooth-free
mouth. **This is still a material approximation**, not an exact match to the
approved image. The canonical has more luminous loose intertwined wool,
especially around mane silhouettes; r03 remains comparatively compressed and
plush. The regular rear mane forms and baked shading in the imported color
atlas remain. Camera/pose/light also differ in the canonical comparison board.
Do not use a pixel difference between these views as a calibrated match score.

This is improvable in Blender: denser visible fibers, their scattering and the
underlying pigment/lighting determine the result. PATINA maps alone cannot
reproduce loose silhouette strands. A future scoped pass should concentrate
on selected mane/outline curls and separating baked color shading, with another
slow grazing-light turn. More PATINA seeds are not the immediate bottleneck.

## Controlled test and limits

Re-ran the existing bounded rig audit on the final saved bytes. All 11 checks
passed over all 49 frames: small +/-12-degree head turns, .02 BU pelvis lift
and .006 BU lateral shift, return to neutral. Maximum paw drift 2.1348e-7 BU;
maximum sampled groom-root distance .00033844 BU; maximum relative facial
landmark pair variation 1.0075e-6; rest-pose mesh difference 5.5618e-7 BU.
All file images are packed. Original r01/r02/canonical/FBX hashes are preserved.
The audit samples 80 groom roots, not every strand or tip. The longer strands'
tips are not independently collision-validated. Walking, lying, crouching,
advanced facial controls, all self-collisions and full performance range remain
untested. This is not production animation approval.

Rendered thirteen samples (frames 1,5,...,49) at 512 px/24 samples for the short
GIF/contact sheet, and ten diagnostic/neutral/story-light stills. The final
23-render manifest binds settings/cameras/hashes to the candidate. Renders use
Blender 5.2.2 LTS d13f752e3b9c, Cycles CPU, denoising, fixed seed 18102606,
Standard/None, exposure 0/gamma 1. No interactive scene was overwritten.

## Review files and reproduction

`../renders/leo_tripo_canonical_r03/` contains:

- `muzzle_repair_comparison.png`: actual matched color/clay repair evidence.
- `felt_refinement_comparison.png`: r02/r03 body, same camera/light/resolution.
- `canonical_comparison.png`: approved 2D and actual r03, differing view/pose.
- `front_three_quarter.png`, `front.png`, `right.png`, `rear.png`, `portrait.png`.
- `body_detail.png`, `muzzle_final.png`, `story_light.png`.
- `controlled_rig_preview.gif`, `motion_contact_sheet.png`, thirteen motion PNGs.
- `operations.json`, `controlled_rig_audit.json`, `render_manifest.json`,
  `delivery_manifest.json`: exact operations, checks, hashes and source preservation.

From repository root, with the installed Blender executable and existing local
PATINA maps (no external generation):

```sh
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_r03_diagnose.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_tripo_refine_r03.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_r03_finish.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_r03_patch_color.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_r03_blend_patch.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_r03_eye_clearance.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_r03_review.py -- --audit
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_r03_review.py -- --resume
python3 blender/scripts/leo_r03_boards.py
```

Pillow is needed for boards/GIF; NumPy is bundled in Blender. macOS executable:
`/Applications/Blender.app/Contents/MacOS/Blender`. Background processes require
the local runtime permission used for earlier candidates. No Git operation,
canonical replacement, publication or broader scene integration occurred.
G0 resolved; G1 local repair evidence; G2 limited rig evidence; G3 material
candidate/visual review pending; G4/G5 out of scope; G6 not released.
