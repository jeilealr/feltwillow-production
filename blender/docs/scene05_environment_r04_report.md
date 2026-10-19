# S05 r04 — reference-inspired handmade-world prototype

**Preservation note, 19 October 2026:** Unavailable historical/local media links below are retained as code paths. Recover only exact historical bytes through the cleanup receipts/Git history or the verified local archive; these paths are not active generation authorities. Original dated results remain in source history.

**Craft and layout improved, but the richer-world brief is not yet achieved.**
Style verdict: **needs revision**. Technical verdict: scoped static checks pass.
No owner acceptance or production release is claimed. Shared production skill
VERSION **1.2.0** and its `.agents` symlink were verified; neither was edited.

Open the new shot (`../scenes/lion_and_mouse_v6/s05_environment_r04.blend`), which
relatively links the r04 library (`../assets/environments/great_tree/great_tree_environment_r04.blend`).
The separate reusable craft kit (`../assets/environments/great_tree/great_tree_craft_kit_r04.blend`)
contains the curved-surface tests.

Evidence: actual saved-settings baseline and r04 (`../renders/scene05_environment_r04/baseline_and_r04.png`),
clean views (`../renders/scene05_environment_r04/review_views.png`),
native shader A/B (`../renders/scene05_environment_r04/material_contribution_AB.png`),
existing-height A/B (`../renders/scene05_environment_r04/existing_height_contribution_AB.png`).
Baseline and r04 use their own saved cameras: this is an explicitly designed
composition change, not a claim of camera-matched material improvement. The
material A/B holds camera and lighting fixed. A separate
fixed-new-camera before/after (`../renders/scene05_environment_r04/fixed_camera_before_after.png`)
renders unchanged r03 through the exact r04 establishing camera; r03 retains
its original lights, so this is a combined world-design comparison.

## Intent and changes

The owner's new `reference_inspired` direction supersedes whole-image matching
for this candidate. Prior art guides grandeur, cozy craft, dusk palette and
narrative identity. Exact old rock/cloud/landmark residuals are not vetoes.
See [direction brief](../renders/scene05_environment_r04/direction_brief.md),
[validated direction metadata](../renders/scene05_environment_r04/environment_direction.json)
and [intentional-change ledger](../renders/scene05_environment_r04/intentional_change_ledger.json).

The candidate keeps the support sheet, original safe approach root, rest/paw/
nose anchors, route, .2 m/BU and fixed physical proxy sizes. A new continuous
tree/root mesh replaces the visible r03 tree while its source remains hidden
inside the new library. New curves/material families and authored dressing
replace failed flakes/coins. Geometry, dressing, distant layers, light state,
cameras and diagnostic proxies remain separately organized. Semantic legacy
collection IDs remain for reuse; scene metadata records R04.

## Visual review

| Dimension | Improvement | Remaining problem / next best fix |
|---|---|---|
| Composition and hierarchy | Upward branching, visible canopy framing and quiet supported clearing. Medium/detail views use framing rather than actor enlargement. | Tree still dominates as a smooth generic trunk; introduce authored fork and root rhythms before revisiting camera. |
| Felt recognition and material difference | Heathered stone, short-pile moss and thick cupped leaves read more clearly; continuous matted ground removes coin carpet. | Broad bark/root still molded or rubbery; ground can look airbrushed. Sculpt growth-following folds and tune compressed wool at shot scale. |
| Vegetation and depth | Grouped near/mid/far dressing; fewer frontal tree rows, layered silhouettes. | Bushes repeat pumpkin/bean masses; far scenery is sharp flat cutouts and isolated conifers. Author 2–3 convincing plant clusters and overlapping woodland masses. |
| Root/contact | Original safe root geometry and supported bypass preserved; new hero root moss is coherent. | Approach root remains a laid-on rod with abrupt tip/dark ground seam; moss strips too regular. Sculpt buried contact and asymmetric cushions without breaking clearance. |
| Sky/light/stream | Readable warm/cool dusk and left sunset; stream remains in world. | Pastel illumination lacks cozy drama, stream window is weak, ridge planes feel like placeholders. Author a clearer stream opening and depth/value hierarchy. |
| Actor readability and causality | Geometric proxies show reserved space, unchanged .25 ratio, approach and contact landmarks. | These are space tests, not actor likeness, paw/nose performance or readable final animation. Validate actual approved actor poses in a later scoped task. |

Separate read-only reference/design and material reviewers inspected exact
final stills and independently returned **refinement prototype**. Their
findings are preserved in `independent_review.md`; they did not sign for the
owner. No image-difference score was used as beauty acceptance.

## Tests, preservation and performance

All **13** scoped checks pass: 27 protected input hashes unchanged; relative
r04-only library link resolves; file images packed; 66 route samples supported
with normals above .99; approach-root clearance 0.2714 BU (>0.06); hero-tree
route clearance 3.7464 BU (>0.15); nine rest-support samples; proxy ratio .25;
proxies hidden by default; selected mode recorded; fused oak base mesh closed.
These checks do not establish all collisions/self-intersections or beauty.
The proxies include a rest envelope, Milo size marker and floating paw/nose
position markers; they are explicitly not modeled/posed actors.

Existing Leo files, all prior `.blend` revisions, approved location image and
production authority records remain unchanged. Selected image hashes are
checked separately against the existing owner ledger. No other scene was
migrated. No production gates, audio, mouth rules, props or story events changed.
Milo still rounds the root and trips at Leo's forepaw before gentle nose
contact; a root never substitutes for that story event. S05 remains prop-free.

Budget stopped at **two corrective passes and 16 local still renders of 16
allowed**: one unchanged-settings baseline, two kit lights, two layout studies,
nine final/diagnostic stills, one existing-height trial, one fixed-new-camera
r03 comparison. No extra ambient pass:
stills are not sufficiently promising for temporal qualification. No paid
generation, retries, uploads, remote jobs, installation or spend. The new scene
is not mixed with approved images/Wan shots as a seamless sequence.

Runtime: Blender 5.2.2 LTS, Cycles CPU, Standard/None, exposure 0, gamma 1,
fixed seed 510400, denoising. Final establishing: 1600×900/48 samples, about
33.7 s; medium/detail 1280×720/40 samples, about 21–22 s. These are measured
local still timings, not film throughput or memory estimates. Still lateral
envelope ±.25 BU showed no obvious card boundary exposure; reverse views,
camera travel, parallax in motion and fiber stability remain untested. Far
scenery is deliberately restricted shallow geometry.

## Reproduction and handoff

Scripts in `blender/scripts/`: `intake_scene05_environment_r04.py` (read-only
safe-copy audit/baseline), `craft_scene05_r04.py` (kit recipes),
`kit_scene05_environment_r04.py`, `build_scene05_environment_r04.py`,
`correct_scene05_environment_r04.py`, `finish_scene05_environment_r04.py`,
`review_scene05_environment_r04.py`, `map_contribution_scene05_r04.py`,
`fixed_baseline_scene05_r04.py`, `boards_scene05_environment_r04.py`.

Executed with local Blender:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/SCRIPT.py
```

Order: intake → kit/visual review → build/preview → correction1/preview →
correction2 → final review → existing-height render-only trial → fixed-camera
r03 comparison → boards.
Review's `-- --preview` renders one layout study; `-- --audit-only` skips renders.
Boards use the existing `feltwillow` Python environment with Pillow. Creator
scripts reject occupied new-revision paths and repeat corrections; preserve
these candidate files rather than rerunning over them. Full paths, hashes,
render settings/timings and command logs are in the delivery manifest/review
directory. No commit or push.

Next smallest useful action: a manual, camera-facing root/trunk sculpt plus
two reviewed vegetation modules. More scatter or a new texture service is not
the next fix supported by the evidence.
