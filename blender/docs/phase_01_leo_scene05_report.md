# Phase 01 — Leo and Scene 05 Blender feasibility report

18 October 2026. **Technical prototype created; visual success criteria not yet
met. Needs revision and owner review. No asset is newly approved.**

Blender provides a reproducible scene/rig/camera foundation. These renders do
**not** yet demonstrate a sufficiently faithful reproduction of Feltwillow's
approved Leo or its Great Tree set. Another tightly scoped art pass is warranted
before extending this approach to Milo or the rest of the story.

## Repository state

- Starting and ending branch: `feature/perceptual-world` (existing non-main).
- Starting commit: `fcea46b788f6df8423f84bf14e54169f15a383e3`.
- No commits made; HEAD unchanged. Owner retains commit/push control.
- New work is under `blender/`; the only existing tracked file edited is
  `.gitignore`. Original five untracked .DS_Store files remain untouched.
- Production image/video behavior, story plans and source images remain intact.
  Source hashes are checked against `config/authority.json`.

## Blender environment

Blender **5.2.2 LTS**, build `d13f752e3b9c`, macOS **26.7.1**, arm64.
Cycles CPU and Eevee tested. No add-ons or external generation dependencies.
Sandboxed native startup crashed; approved local execution outside the sandbox
worked. No Blender version or installation changed.

Standard view transform, look None, exposure 0, gamma 1. RGB PNG / sRGB output;
procedural shader colors are approximate linear RGB. No global orange grade.
Comparison-board dependency only: Python >=3.11 with Pillow.

## Leo

Sources: approved v6 neutral full-body canonical and expression board; current
consolidated atlas and trapped-expression sheet were inspected as provisional
support only, because their approval remains pending. All four exact image
hashes and current authority data are recorded in `config/authority.json`.
[Pre-model extraction](identity_and_environment_contract.md) records identity,
proportions, materials and the source-authority distinctions.

Modeling: editable ellipsoidal forms, native curve locks, rounded felt nose,
cream muzzle/chin, amber eyes, inset ears, toe seams, whiskers and one tufted
tail. Native voxel welding removes torso/chest/rump intersections; spinal
weights blend torso motion. Separate articulated limb segments remain.
Materials use roughness, short noise bump, slight pigment variation, sheen and
bounded, surface-sampled short curve fibers. No realistic fur or hair simulation.

Rig: **29 bones**, four two-bone no-stretch IK chains with independent paw and
pole controls; hips/spine/chest/neck/head and three tail bones. Paws follow
controls and stay planted under a tested body displacement. Five pose presets
are rendered: neutral, walk contact test, low rest, struggle and head turn.
These are control demonstrations, not approved animation, a walk cycle or net
interaction. Mouth stays closed. Eyes can close for the rest preset.

Topology: hybrid prototype. The welded torso is voxel-derived, not final quad
animation topology; limbs/face/mane retain component meshes or curves with
segment or head binding. Joints need continuous retopology, blended weights and
deformation testing before production. Mane follows the head rigidly so it
cannot randomly change shape. No complex face rig.

Eight controlled diagnostic views: front, left, right, rear, front/rear three-
quarter, elevated three-quarter and neutral portrait. Portrait shows complete
mane/ears, shoulders and upper chest. Review:

- [Canonical versus all eight views](../renders/reference/leo/comparison.png)
- [Pose controls](../renders/diagnostic/rig_comparison.png)
- [Cycles versus Eevee](../renders/diagnostic/engine_comparison.png)

Observed discrepancies after visual comparison: face is too flat and regular;
small nose, protruding eyes and round raised ears need closer matching. Mane is
too disk-like in side/rear views and its repeated ring curls lack the approved
thick organic rolled-wool locks and forehead sweep. Body reads longer and more
segmented; paw shapes and shoulder transitions are less sculpted. Tail is thin
and its tuft too simple. Honey/cream/brown approximations remain duller and less
luminous than the canonical. Fibers now read at portrait scale but are sparse
and uneven at wide scale; some areas still look like molded toy surfaces.
Handmade asymmetry is insufficient. This is recognizably derived from Leo's
features, but **not visually close enough to approve as canonical**.

## Scene 05 environment

Authority: approved **Great Tree dusk, tree_dusk_r02.png**; r02's low diagonal
stumble root is required. Scene 05 p01 is the representative wide sleeping-Leo
reference. All nine active Scene 05 keyframes were inspected and hash-recorded.
The current keyframe plan resolves selected paths/crops; staging is a physical
proposal and does not supersede owner selections. Scenes 05–08 share this set;
Scene 04 is another location, Scene 09 is a montage and Scene 16 uses daylight.
No Scene 05 net/acorn was invented.

Created: central-right oak trunk and branches, exposed root fan, diagonal
foreground root, left mound, center-left stone, right rock, clear ground/path,
far-left stream, background hills/trees, canopy and repeated foliage. Repeated
geometry uses fixed per-asset random seeds. Felt/cloth bark, ground, stone,
leaf and water materials are native. The beauty render is actual 3D geometry;
the approved plate is only a hidden reference and camera viewport overlay.

Lighting: cool sky, neutral fill and limited warm area source from far left.
Sky has a localized left warm band and violet field. The plate's rich sunset,
fabric texture, contrast and depth have **not** been reproduced accurately.
No destructive grade was used to disguise this mismatch.

Camera: provisional 39 mm perspective wide at `(0,-13,3.5)`, looking at
`(0,4,1.55)`. Registered source crops become lens/shift variants from the same
optical center. Distinct selected medium centers remain explicit offsets within
a family. Projection tests verify the crop math, not artistic camera accuracy.
The scene stores a camera-aligned viewport plate overlay for further matching.

[Plate and selected p01 versus reconstruction](../renders/reference/s05/comparison.png)
contains both empty environment and sleeping-Leo comparison. Other s05 renders
are **camera crop tests of the same sleeping pose**, not recreations of p03/p04
acting or the awake portrait. No Milo performance is claimed.

Projected landmark diagnostics (normalized top-left origin, geometric center
samples; source positions are approximate visual estimates, not survey data):

| Landmark | Source estimate | Candidate projection |
|---|---|---|
| Oak base | (.69, .59) | (.7052, .6462) |
| Left stone | (.26, .69) | (.2872, .6891) |
| Right rock | (.94, .67) | (.9258, .6845) |
| Foreground root tip | (.49, .86) | (.4358, .8458) |

The set retains the broad landmark arrangement, but it is still a **coarse
reconstruction**, with simplified branches, cloudless sky, geometric pines,
sparse ground cover, coarse rocks and smooth bark. Stream/hills/canopy depth
and path edges need substantial refinement. Leo occupies too little of the
wide composition and rests upright rather than fully on his side with mane on
grass. Character-to-tree calibration and the resting pose need another pass;
independent anatomical scaling is not an acceptable shortcut. Camera matching
is provisional and fails a close compositional comparison.

## Reproducibility

See [README](../README.md) for executable commands. Artifacts:

- `assets/characters/leo/leo_canonical_candidate.blend`
- `assets/environments/great_tree/great_tree_dusk_candidate.blend`
- `scenes/lion_and_mouse_v6/s05.blend`
- `scripts/build.py`: native deterministic asset/scene construction.
- `scripts/poses.py`: control presets with unchanged anatomical scale.
- `scripts/render.py`: diagnostic, scene, pose and engine tests plus manifests.
- `scripts/compare.py`: labeled source/render review boards.
- `tests/validate.py`: reopens real libraries and checks source hashes, evaluated
  IK, planted paws, unit ratio, links, cameras and optical crop projections.

The environment is linked using a repository-relative library path. Leo is
appended once for scene posing, with its source-library path recorded. Rebuild
the scene after character changes. No Downloads assets or absolute machine
paths are required. One Blender unit = .2 m, Z up, clearing ground at Z=0.
Milo_SCALE_PROXY is hidden and explicitly non-production, with height exactly
.25 of measured neutral Leo and at the same staging depth. No Milo asset.

Final structural validation: **52/52 checks pass** in
[validation.json](../renders/validation.json). This does not certify visual
anatomy, production deformation or owner approval. Complete builds and targeted
per-library reruns were exercised; each asset resets its own deterministic seed.
Cross-machine byte-identical .blend serialization is not promised.

## Performance

Base geometry counts, excluding final curve tessellation:

| Asset | Mesh faces | Curve splines | Other |
|---|---:|---:|---|
| Leo | 42,338 | 60,039 | 40,736 vertices, 68 meshes, 29 bones |
| Great Tree | 96,712 | 90 | 1,453 objects including lights/camera/reference |

Approximately 60,000 short fibers, not millions; remaining Leo splines are
mane locks, tail, face and toe detail. Final render polygon counts are higher
because native bevelled curves tessellate at render time. No caches, baked
hair simulations or image textures are required.

Actual 640×640, 24-sample Cycles CPU engine trial: **3.58 s**; Eevee with the
same scene/resolution: **1.524 s**. These are small-scene local timings, affected
by startup/shader cache and concurrent prototype work, not throughput promises.
Full timing/hash records are in `renders/*_manifest.json`. Scene reference
renders are 960×540; diagnostic views 640×640; rig tests use 16 Cycles samples.
No motion sequence was rendered.

Eevee is promising for layout/iteration; Cycles is the current reference choice
for soft contact/indirect light. The two outputs have similar identity/style
limitations. A final renderer decision should follow a successful felt-material
close-up and repeatable isolated timing trials, not these small timings alone.

## Recommendations and Phase 01 disposition

1. Continue **one bounded Leo/set art pass**: Blender's deterministic geometry,
   rig and camera layer works and render costs are practical for iteration.
   Current visual quality is insufficient to green-light story-wide conversion.
2. Leo needs stronger organic modeling, side/rear mane depth, natural wool curls,
   face integration and continuous limb topology. Felt materials need more work.
3. Great Tree needs detailed bark/foliage/ground, correct lighting/sky, better
   landmark calibration, character/environment scale and sleeping-pose matching.
4. Defer production Milo modeling until Leo and this set meet owner review;
   retain the verified .25 scale system.
5. No demonstrated issue warrants a paid external generation tool. These are
   modeling/material/camera problems to resolve in Blender before considering
   external tools. Do not introduce PATINA, Tripo, fal.ai or a new pipeline here.

Deliverables exist and are reviewable; the visual Phase 01 success criteria
remain open. Owner review is required after revision, not inferred from saved
files, passing tests or completed renders.
