# Scene 05 r03 — refinement prototype

**Preservation note, 19 October 2026:** Unavailable historical/local media links below are retained as code paths. Recover only exact historical bytes through the cleanup receipts/Git history or the verified local archive; these paths are not active generation authorities. Original dated results remain in source history.

Status: **needs revision; not an approved scene match**. This is a refinement of
the reusable r02 environment, not a replacement of approved artwork. No owner
approval, production readiness, or successful character performance is claimed.

Review evidence: approved / r02 / r03 board (`../renders/scene05_environment_r03/before_after_board.png`),
50% overlay (`../renders/scene05_environment_r03/comparison_final/overlay_50.png`),
tree/root crops (`../renders/scene05_environment_r03/tree_roots_matched_crops.png`),
ground/rock/stream crops (`../renders/scene05_environment_r03/path_rock_stream_matched_crops.png`).
The full render is environment_wide.png (`../renders/scene05_environment_r03/environment_wide.png`).

## Camera/framing

- Improved: compared the actual linked scene to the geography plate; adjusted
  the visible trunk width, rock heights and path silhouette in
  that shared projection. Supplied fixed-coordinate before/after and overlays.
- Still off: no new solved camera is claimed. The existing 45 mm camera and
  optical center remain; the seven r02 anchor registrations were already
  close, but they do not establish silhouette, horizon or depth fidelity.
  Ten manual image correspondences are supplied with explicit uncertainty,
  not automatic feature detection. The upper branch opening and distant
  skyline remain different.
- Next best fix: annotate actual trunk edges at three heights and the skyline
  in the overlay, then jointly fit camera pitch/lens and trunk/branch shape in
  a clay study. Do not move the camera merely to conceal geometry errors.

## Tree/roots

- Improved: retained and broadened the existing fused hero mesh and base flare;
  replaced short decorative bark cords with medium surface relief.
  Root/trunk moss now follows surface normals and
  has short anchored fibers. Canopy leaf clusters frame more of the opening.
- Still off: the upper branches remain blunt, trunk creases are too regular,
  and local faceting/pinched seams remain visible at full resolution,
  and root taper/contact is simpler than the source. The approach-root tip
  remains shorter than the plate: its attempted extension failed route
  clearance, so the original safe endpoint was restored. Moss does not reproduce
  the plate's sculpted, intertwined growth. This is still procedural art.
- Next best fix: a bounded manual sculpt of the camera-facing trunk fork and
  three principal buttresses, using the plate silhouette as a tracing guide.

## Path/rocks/stream

- Improved: narrower curved path with sampled irregular edges and scattered
  matted growth; lower left/right stone profiles with asymmetry. Raised the
  stream ribbon above the ground sheet so it can actually be visible.
- Still off: path color and relief remain too even; planted rock contact and
  the stream's winding reflective banks differ substantially from the plate.
  Ground specks can still read as separate pieces rather than compressed wool.
- Next best fix: author one continuous ground/path transition mask and sculpt
  the two hero stones and visible stream-bank contour at matched coordinates.

## Vegetation

- Improved: replaced the visible uniform pile with clustered short growth,
  varied compressed wool islands, midground bush transitions, thicker lobed
  canopy leaves and smaller lobes on existing distant crowns. Retained the
  existing acting-lane and route exclusion logic.
- Still off: leaf clumps and crown lobes repeat; distant trees still read as
  assembled blobs, and foreground scale/hierarchy does not match the source.
- Next best fix: make three manually reviewed felt plant/crown modules and
  replace the most visible repeating clusters with authored arrangements.

## Sky/lighting

- Improved: cooler upper sky and warmer low sky, restrained textured cloud
  bands, stronger cool fill separation and a smaller localized warm key.
  Kept the far-left sunset and separate light/geometry collections.
- Still off: the sunset is less luminous and structured than the approved
  image; cloud volume, ridge geography and layered wooded hills remain weak.
  Raising distant crowns is only a silhouette study, not a calibrated hillside.
- Next best fix: fit two ridge silhouettes and the large cloud/value masses
  directly against the plate before adding more background trees. A restricted
  matte alternative would require an explicit representation decision.

## Felt/material fidelity

- Improved: rough nonmetallic shaders with medium/fine object-space relief,
  short moss fibers and leaf thickness reduce some smooth CG surfaces.
  Existing packed height-map usage is preserved; no new maps were generated.
- Still off: smooth wood/stone masses, regular bark fluting and discrete ground
  islands still fall short of a handcrafted needle-felt miniature. Still
  images do not prove fiber or denoising stability in motion.
- Next best fix: test one camera-facing bark/moss swatch with sculpted wool
  relief and sparse fibers under neutral and dusk light. PATINA extraction
  could help bark or stone mesostructure, or path/moss roughness, after a
  specific crop/schema/price/operation is approved. Maps cannot fix silhouettes.

## Preservation, checks and handoff

New files: `great_tree_environment_r03.blend` and linked
`s05_environment_r03.blend`. Existing collection/landmark IDs intentionally keep
their R02 names so library consumers and proxies retain their identities. Only
this new shot points at r03. All original r02 objects remain, with superseded
dressing hidden from beauty. No other scene was migrated.

Source hashes, Blender build, object inventory, exact render settings/timings,
dependency and route checks are in the r03 review directory's JSON receipts.
All ten final structural/preservation checks pass: relative library resolution,
packed images, 66 supported route samples, near-level route normals, ground
steps below 0.02 BU, 0.2714 BU minimum root clearance (threshold 0.06), closed
oak base mesh, hidden proxies, 0.25 proxy ratio and unchanged protected inputs.
These checks do not establish absence of all self-intersections or visual
fidelity. Six final render hashes are bound to the exact delivered pair.
`preserved_sources_before.json` binds all Leo asset files, both r02 inputs and
the geography plate; `validation.json` records the after comparison. Current
r02 authority bindings were reverified against actual source bytes. No selected
image or story acceptance ledger was modified. No git mutation or publishing.

Reproduction, from repository root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/refine_scene05_environment_r03.py
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/review_scene05_environment_r03.py
/Users/lealroja/miniconda3/envs/feltwillow/bin/python blender/scripts/scene05_environment_boards_r03.py
```

Comparison preparation explicitly center-trims the 1672×941 source by 0.25 px
at top/bottom to exact 16:9, then resamples to 960×540. The 1920×1080 candidate
is downsampled for comparison. No landmark warping or color matching. Untagged
display images are explicitly treated as sRGB; originals remain untouched.

Local budget: three visually reviewed refinement stages, with an additional
unrendered trunk-proportion adjustment during the final stage. The first full
render exposed lifted bark ribbons: that layer was disabled and the upper
width transition repaired before delivery; remaining local bark artifacts are
reported rather than declared solved. The local still budget was extended
from 12 to 16 to refresh all evidence after that concrete regression. Cycles CPU,
Blender 5.2.2 LTS; Standard/None, exposure 0, gamma 1. Paid generation, uploads
and external spend: **zero**. Narrow-envelope stills are diagnostic; animation,
large camera travel, final actor contacts and temporal stability remain untested.
