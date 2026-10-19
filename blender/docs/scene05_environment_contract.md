# Scene 05 Great Tree environment contract — candidate r02

18 October 2026. Reusable environment pass, not a replacement of selected 2D
frames. All world depths and hidden forms below are reconstruction hypotheses.
Z up; +Y deeper into the wide set; X to wide-camera right; 1 BU = .2 m.
Leo's preserved r04 surface measures 1.5 BU standing mane-to-ground; Milo proxy
is .375 BU, exactly .25 at equal depth. A lying-pose box is not a scale ruler.

## Authority reconciled before modeling

Current v6 README, visual bible, staging/keyframe/scene/visual-sequence plans,
owner_visual_acceptance.json, BACKGROUND_CONTINUITY and perceptual-world policy
were read. All nine selected S05 frames were resolved through the current
ledger and their actual bytes verified. Nearby S06–08 story actions and the
selected S06x transition were inspected. Existing environment and s05 .blend
files were opened read-only; their old report correctly calls them coarse,
visually unsuccessful prototypes. Keep them, build a separate r02 library.
Source inventories/hashes: `../renders/scene05_environment_r02/`.

- Geography: **tree_dusk_r02.png**, approved composition master; r01 is history.
- Scene: The sleeping lion. Leo lies on the grass/path beneath the oak, mane
  on grass and forepaw across the path. Milo approaches around the visible low
  root, trips at the forepaw in selected s05x_p05, tumbles gently to the nose,
  then Leo wakes. Tree roots cannot replace the forepaw story contact.
- Lighting: preserve the established far-left sunset direction and cool/neutral
  dusk ambient. Current Scene 05 owner style standard additionally requires
  luminous golden highlights/readable shadows and environmental felt finish;
  its retained swatch controls tone/material only, not layout or actor pigment.
  It supersedes a dim interpretation, not the registered geography or light side.
- Scene family: Scenes 05–08 form one continuous Great Tree dusk encounter.
  Scene 09 revisits it in a montage. Scene 16 has accepted DAY r01 geography;
  root-corrected DAY r02 remains pending. Do not silently approve that variant.
  Upward tree_sky is a distinct camera reference, deferred in this pass.
- No acorn, net, hunter, burrow or extra special prop belongs to Scene 05.
- Current owner image selections prevail over stale generated-board references
  to dusk r01/Milo r01 and compatibility pending-review fields.
- Camera conflict: legacy planned crop_rect and newer proposed_camera crops
  differ on p02/p03/p04. Selected images are composition evidence, not unique
  3D calibration. Preserve both in the source inventory. Build the plate wide
  and a clearly provisional p02 crop study; do not rewrite production plans.

## Required kit and dimensionality

| Element / stable ID | Construction | Roles / boundary |
|---|---|---|
| OAK_MAIN / root fan | Full 3D fused sculpted trunk, branches and primary roots | Main silhouette, fixed landmark, occlusion; crafted felt ridges, not realistic bark |
| ROOT_APPROACH_A | Full 3D low diagonal root | Explicit contactable obstacle beside Milo route; no arbitrary root scattering |
| SURF_CLEARING / SURF_PATH | Continuous terrain mesh and shallow path layer | Walkable/contact areas; level reserved resting/contact lane |
| MOUND_LEFT | Low-detail 3D moss mound | Fixed framing, not default character support |
| STONE_CENTER_LEFT / ROCK_RIGHT | Full 3D irregular felt stone | Fixed landmarks, foreground occlusion; not default standing surfaces |
| Moss / ferns / grass | Instanced full 3D felt modules | Foreground/hero dressing; excluded from route and contact reservation |
| Midground rounded foliage / pines | Low-detail 3D modules | Parallax and framing; fixed seed/IDs |
| Stream glimpse | Shallow 3D cloth ribbon plus small banks/stones | Visible far left, nonwalkable; no fluid simulation |
| Far hills / tree line | Fixed 2.5D shallow relief silhouettes | Limited wide/crop camera envelope; no character access |
| Sky / sunset disk / cloud bands | Fixed matte sky plane and layered felt silhouettes | No volumes; clouds structured for later bounded drift, static now |
| Deep unseen forest / tree backs beyond view | Deferred | No invented navigable forest or all-scene build |
| Leo/Milo | Optional clearly labeled geometric proxies in shot | No character model/rig redesign or production performance |

## Landmarks, routes and story state

Plate-normalized top-left observation targets are estimates, not surveys:
oak base (.69,.59), center-left stone (.26,.69), right rock (.94,.67), left
mound (.055,.66), diagonal root (.03,.67) → (.49,.86), stream (.14,.53).
Set anchors are world-space objects with stable IDs; exact candidate coordinates
and rendered projections are written after build. Do not move them per crop.

Reserve the front clearing for Leo's supported side-rest envelope and his paw/
nose contact area; keep ground contiguous and remove decorative grass from the
route. Register Milo approach, root bypass, paw-near point, nose-near point and
exit toward screen-right. Proxies indicate scale/space, not a validated sleeping
Leo or Milo animation. The r04 rig has no validated lie-down transition; do not
force it to imitate the selected image for this environment task.

Story props are absent. Persistent roots/rocks/path remain fixed across later
shots. Paw placement, nose contact and Leo posture are actor state outside the
permanent library. Surface normals/ray contacts and route clearance must be
checked against visible ground and root geometry, not invisible giant colliders.

## Cameras and 2.5D envelope

Wide: 16:9 low animal view; candidate 45 mm at (0,-8,1.55), looking toward
(0,4,.725), fitted to the plate landmarks at a measured miniature actor scale.
These are inferred calibration choices. Crop cameras share its optical center;
no character/environment scaling for readability. Register the newer proposed
p02 crop as an interaction STUDY, not approved replacement camera. Diagnostic
root and elevated views may lie outside the matte-backed beauty envelope.

Initial beauty envelope to test: primary wide and registered crops, plus lateral
camera offsets ±.25 BU with fixed world landmarks and target. Cards stay fixed,
never rotate to face arbitrary cameras. Distant mattes may be unsuitable for
large reverse views; promote only required layers to deeper geometry later.
Do not call unseen backs or a bird's-eye overview production-ready scenery.

## Ambient plan — prepared, not animated

Preset `still_evening_r02`: default static; fixed seed 18102651, common global
story-time origin 0, 24 fps. No shot-local reseeding or resetting wind phase.

- Cloud bands: optional .015 BU/s world +X drift, no wraps within reviewed view;
  no cloud shadow or exposure modulation. Disable drift for strict plate hold.
- Leaf tips: optional max .7° bend, 8–13 s periods, anchored bases. Hero canopy
  boundary, trunk, branches and major root positions remain fixed.
- Grass tips: optional max 1.5°, 6–10 s periods; disable in support/contact lane.
- Stream: optional cloth highlight ripple amplitude .0015 BU, 9 s period;
  banks/waterline fixed. No displacement under contact surfaces or fluid solver.
- Rocks, mound, path, mountains, major foliage groups and sun: static.

These are recommended later presets, not an implemented motion qualification.

## Bounded build / review

One native kit pass plus at most two evidence-driven art/composition corrections.
CPU review 960×540 (small previews first), 24–48 samples; root detail and one
broader overview, empty environment, composition/crop and camera-envelope
checks, diagnostic route overlay. Zero external spending/uploads. Save reusable
library separately from scene assembly, with relative linking. Preserve all old
.blend files, source images, production JSON, selected keyframes and live UI.
Root Git policy overrides skill Git snapshot calls; snapshot collects file
hashes with Git explicitly disabled. No production approval inferred from tests.
