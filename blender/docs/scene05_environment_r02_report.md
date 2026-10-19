# Scene 05 — first reusable Great Tree environment pass

18 October 2026. **First environment prototype. Structurally usable for basic
proxy blocking; visual fidelity to approved artwork remains incomplete.**
Nothing here replaces approved images, Leo, production plans or prior prototypes.

## Open and review

- Scene assembly: `../scenes/lion_and_mouse_v6/s05_environment_r02.blend`
  SHA256 `e16fc48b5355f635a0884dc4775e67d2ac83005383983a63fc62dcda30a00a50`.
- Reusable library: `../assets/environments/great_tree/great_tree_environment_r02.blend`
  SHA256 `c80c5bd871c678a9f1c323da79db86a2c4b64f76ecd516655c22746d0fa74b46`.
- Review directory: `../renders/scene05_environment_r02/`.
- Contract: [scene05_environment_contract.md](scene05_environment_contract.md).

Open the scene assembly, then Render → Render Image for the saved dusk view.
Proxies are hidden by default in viewport and beauty; enable the named local
`S05_PROXIES_DIAGNOSTIC_ONLY` collection for layout work. The scene links the
permanent geometry, cameras and dusk-light collections using a relative path.
Keep the repository's blender folder structure together when moving files.
The reused felt height texture is embedded; no texture download is needed.

## 1. Files inspected and authority reconciliation

Read the repository skill, relevant environment/world-state/rendering guidance,
AGENTS/CLAUDE and the current v6 README. Inspected visual_bible.json,
scene_plan.json, staging_plan.json, keyframe_plan.json, visual_sequence_plan.json,
owner_visual_acceptance.json, BACKGROUND_CONTINUITY.md and the perceptual-world
policy. Read earlier Blender extraction/report and construction code. Opened
both previous environment/scene .blend files read-only. Measured preserved
Leo r04's main surface: 1.5 BU, from ground to mane top. No Leo edit was made.

Screened all nine active Scene 05 images, the selected S06x transition, nearby
S04/S07/S08 examples, dusk master, accepted day master, distinct sky reference
and retained Scene 05 environmental style swatch. The nine Scene 05 selections
were resolved from the current owner ledger and their actual hashes verified.
`config/scene05_environment_r02_authority.json` enumerates 28 source hashes,
selected IDs and competing crop proposals. `existing_asset_inventory.json`
records old files/cameras and scale measurement. The context snapshot disables
all Git calls to comply with the owner's Git rule. No Git commands were run.

Current geography is **Great Tree dusk r02**, with the diagonal low root.
Scenes 05–08 share one persistent clearing; 09 revisits it in a montage.
Scene 16's day r01 remains accepted; day r02 root correction is still pending.
The upward tree-sky plate is a distinct view, not the wide-clearing camera.

Scene 05: Leo sleeps with supported mane/body and a forepaw across the lane;
Milo approaches around the visible root, catches the forepaw in the selected
trip insert, tumbles gently to the nose, and Leo wakes. Root and forepaw are
separate causal landmarks. No net/acorn/extra special prop belongs here.
Scene 05's current style standard requires brighter golden highlights and
readable shadows while retaining the established far-left sunset direction and
cool/neutral dusk ambient. The swatch does not govern layout or actor pigment.

Stale board references to dusk r01/Milo r01 were not followed. Legacy planned
crops and newer proposed-camera crops differ; this pass registers the master
wide and a clearly labeled current proposed p02 crop STUDY. It does not rewrite
or approve production cameras, nor claim exact reproduction of selected acting.

## 2. Built reusable kit and organization

`ENV_GreatTree_R02` contains grouped permanent hero geometry, ground/path,
dressing, far relief, sky/clouds, named anchors and hidden kit templates.
Separate `GT_DUSK_LIGHT_R02` and `GT_CAMERAS_R02` collections keep lighting and
framing outside permanent geometry. Dressing uses fixed seed 18102651.

Built: fused oak trunk/branch/root structure; low diagonal approach root;
continuous visible ground and shallow winding path; left mound; center-left
stone; large right rock; moss and bark folds; hand-cut leaf/fern/bush modules;
short anchored ground pile; midground wool crown/pine modules; cloth stream
ribbon with bank stones; far hill relief; sky, sunset disk and cloud bands.
Repeated leaf and moss modules share mesh data where practical. Templates,
landmark IDs and source script make this a reusable kit, not a painted one-off.

Scale/support IDs include `SURF_CLEARING`, `SURF_PATH`, `ROOT_APPROACH_A`,
`OAK_MAIN` and named paw/nose/rest/route anchors. Those actor-contact anchors are
provisional layout targets; they must be fitted to the actual future lying pose.
The diagnostic Leo volume is a space reservation, not a faithful sleeping model.
Milo is an eyeless labeled .375 BU capsule, not a character asset. Its physical
neutral-height ratio to measured Leo is .25; no independent readability scaling.

The linked scene adds only local proxy/route controls. Both existing prototypes
and Leo r04 are preserved. New asset sizes are approximately 7.1 MiB library
and .29 MiB scene; no copies of Leo's dense groom were embedded in the set.

## 3. 3D, 2.5D and deferred decisions

Full 3D: hero tree, structural roots, contact ground/path, rocks/mound, foreground
foliage, moss and stream banks. Low-detail 3D: midground tree/foliage masses and
pines. These support nearby parallax without turning to face the camera.

2.5D: broad fixed far-mountain relief strips, matte sky, sunset disk and separate
cloud silhouettes. Their reviewed beauty envelope is the wide/crops plus
±.25 BU lateral camera offsets with fixed world geometry. A large reverse or
free-roaming camera is not qualified. The overview deliberately exposes the
set's construction and is a diagnostic, not a new approved landscape angle.
No approved full plate is projected over the render to hide missing geometry.

Deferred: upward sky shot, detailed unseen tree backs, navigable deep forest,
daytime release, realistic water/wind/volumes, actor posing/animation and full
collision setup. No Milo build, Wan, extra location, or paid generation was used.

## 4. Interaction and ambient readiness

A seven-anchor route leads around the foreground root tip into the paw/nose
reservation and toward a screen-right exit. Sixty-six polyline samples hit the
visible ground/path. Maximum sampled support step is .009 BU (1.8 mm at this
miniature scale); support normals exceed .99 in Z. Minimum sampled centerline
clearance from the visible approach-root surface is .27142 BU, exceeding the
.06 BU diagnostic threshold. These are geometric route checks, not whole-body
Milo collision, a tested tumble or actual paw/nose contact. The rendered smooth
blue route is an illustrative overlay of the anchors.

**Sufficient for a first simple proxy approach/blocking test: yes. Sufficient
for a finished Leo/Milo interaction: no.** Leo's r04 rig does not yet validate
a sleeping/lying transition. The real pose, eye closure, forepaw placement,
nose contact, anatomy and later performance still need their own work.

No extensive animation was added. Recommended presets are stored in
`config/great_tree_ambient_presets_r02.json`: default still evening; optional
slow cloud drift without in-frame wrap or illumination changes, tiny anchored
leaf/grass-tip motion, and a restrained stream-highlight ripple. All major
roots, trunk, rocks, path, banks, canopy boundary, hills and sun stay fixed.
Future motion must evaluate from common story time/seed rather than reset at
camera cuts. These are plans, not implemented or motion-qualified systems.

## 5. Review renders, checks and actual limits

Nine actual final renders: empty wide, provisional interaction crop, root detail,
construction overview, two camera-envelope extremes, neutral-light diagnostic,
and two proxy/route diagnostics. `plate_comparison.png` places the approved
master beside the actual render; `environment_review_board.png`,
`interaction_proxy_board.png`, `camera_envelope_board.png` and
`route_landmark_overlay.png` organize the evidence. No character beauty or
full animation sequence is claimed.

All ten limited checks pass in `validation.json`: closed/manifold main oak,
visible route support, low slope, small ground steps, .25 scale ratio, resolving
relative link, authored landmark projection, root-route clearance, hidden
proxies in default beauty, packed image dependencies. The main oak has zero
nonmanifold edges and 20 horizontal section rays hit continuous structure.

The anchor projection check is mathematical: authored world anchors were placed
from approximate plate UV observations. It does not certify silhouette shape,
physical depth, camera accuracy or visual agreement with selected keyframes.
Full watertightness of every dressing mesh, all self-intersections and complete
character collision volumes were not tested. Thin leaf sheets are intentional.

Initial renders revealed an overly wide path/high canopy and later a trunk
opening caused by open-ended tube fusion. Those trials were preserved; closed
structural tubes and section tests corrected the opening. A packaging check
caught a lazily loaded height map that had not packed; it was forced to embed
and verified after reopening the linked scene. Tests were not marked passed
until that correction. Main and proxy renders now have separate manifests.

Blender 5.2.2 LTS d13f752e3b9c, Cycles CPU, denoising, Standard/None, exposure 0,
gamma 1, 960×540, 32–48 samples. Final render calls took about 7.8–21.1 seconds
each under this run's concurrent workload; these are small review timings,
not film throughput estimates. Approximately 6,167 library objects and 497,575
mesh faces, excluding render-time curve tessellation. Peak memory was not
measured. The height map is reused from the previously approved local PATINA
trial, with no new requests, uploads or additional spend.

## 6. Visual verdict, strengths and missing work

Strengths: persistent named landmarks, separate geometry/light/shot layers,
relative linked assembly, grounded route, measured proxy scale, narrow camera
envelope evidence, repeatable dressing and complete source preservation.

**Artistic match is not achieved.** The main tree remains simplified and its
bark folds too cord-like; root/moss shapes need more intentional sculpting.
Rocks are too smooth, ground pile/leaf shapes are too angular and repetitive,
path edges are too clean, and the stream's cloth appearance is rough. Distant
trees read as simple clumps, hills lack the approved geography's richness, and
cloud bands/sky are flat and insufficiently tactile. Dusk hues, contrast and
light distribution differ from the luminous master. The trunk/canopy/root
silhouettes and physical depths are inferred, not a calibrated reconstruction.
The kit is functional, but these issues prevent calling it a matched production
set. Passing structural tests does not override that visual verdict.

Recommended next step: one focused hero-tree/root/ground art refinement against
the comparison sheet, then a short proxy approach-to-paw-anchor test. Do not
expand to a giant forest or final character performance while this look gap
remains. The existing contract/IDs make refinement possible without discarding
the world layout and route work.

## 7. Created/modified files and reproduction

Created: the two new .blend files; contract and this report; authority and
ambient JSON; inspect/build/review/pack/finalize/board scripts; source inventories,
validation, manifests and review renders under the r02 review directory.
Modified: `blender/README.md` to add the current environment entry. Exact paths,
file sizes and hashes are in `delivery_manifest.json`; inspected source paths
are in the authority JSON. No production image/JSON, prior prototype, Leo,
external service or live Blender scene was changed. No canonical approval or
release was inferred.

From repository root with existing local dependencies (Blender and Pillow):

```sh
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/scene05_environment_inspect.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/build_scene05_environment_r02.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/pack_scene05_environment_r02.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/review_scene05_environment_r02.py -- --resume
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/review_scene05_environment_r02.py -- --proxies --resume
python3 blender/scripts/scene05_environment_boards_r02.py
```

On this Mac the executable is `/Applications/Blender.app/Contents/MacOS/Blender`.
Rebuilds use the repository's existing helper and local PATINA height file;
opening the delivered linked scene needs neither Python scripts nor a network.
