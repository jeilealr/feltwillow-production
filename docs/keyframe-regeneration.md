# Keyframe regeneration and continuity controls

The manifest-backed prompt workflow remains separate from the native v6
keyframe pipeline. For Lion and Mouse v6 and future stories using
`keyframe_boundary_v1`, `staging_plan.json` and its portable regeneration
contract are the source of generation geometry and image authority.

## Perceptual-world planning before regeneration

Choose whose world the frame should inhabit using
[perceptual-world staging](perceptual-world-staging.md) and, for v6, the
[story policy](../stories/lion_and_mouse_v6/PERCEPTUAL_WORLD_POLICY.md) and
[hash-bound audit](../stories/lion_and_mouse_v6/WORLD_SCALE_AUDIT.md).
Resolve a tiny-subject or shared-shot imbalance in the planned camera/crop
before rendering. New framing requires consistent registered geometry and
matching anchors; a readability goal never authorizes independent anatomical
rescaling. Use live approved authorities for missing slots, keeping rejected
or owner-deleted images historical. Advisory findings do not replace current
owner selection, technical evidence or the authority gates below.

## Authority order

Every new candidate starts from the registered location plate and normalized
crop. Attach one identity-root canonical for each visible actor, followed by
the owner-approved same-setup size anchor and any required approved prop or
pose authorities. A generated candidate can be an edit base only when it is
separately reviewed and hash-bound; it never replaces the plate, canonical or
size anchor. Store the exact prompt, ordered reference paths, SHA-256 for every
input and output, crop, camera family and revision history. Historical inputs
stay labeled as provenance and are never silently treated as live references.

The canonical also controls each actor's intrinsic felt pigment and fiber
density/scale. A scene style swatch controls illumination, exposure and the
environment's finish; it cannot recolor Leo's honey-cream coat or chestnut mane,
or Milo's neutral-grey wool. Sunlight may warm the illuminated side and rim,
while soft midtones and shaded fibers must still read as the canonical material.
Compare close and medium candidates at full size against their canonical and
another accepted screen example before adoption. An image edit that improves
pigment but changes paws, pose, scale, crop or fixed background remains a
calibration sample, not an active replacement.

The reference gate checks these records and the actual bytes. It does not grant
visual approval. Canonicals, location masters, anchors and props keep their
existing owner approval state; the tools do not promote a candidate to
approved. Current candidate prompts and source roles are rebuilt from the
visual bible and staging contract. Earlier prompts and reference stacks remain
under explicitly historical fields for provenance; they are not active inputs.

## Build and check the contract

After changing a story's staging or visual bible, rebuild the proposed contract
and run the checks from the repository root:

```bash
python3 production/keyframe_plan.py --story lion_and_mouse_v6
python3 production/keyframe_reference_gate.py --story lion_and_mouse_v6 --write-contract
python3 production/staging_contract.py --story lion_and_mouse_v6
python3 production/check_pose_coverage.py --story lion_and_mouse_v6
swift production/build_keyframe_contact_sheets.swift "$PWD"
python3 production/check_keyframe_review.py
python3 production/keyframe_reference_gate.py --story lion_and_mouse_v6
```

The per-scene contact sheets are the required keyframe review presentation.
Rebuild all 16 sheets whenever an active candidate is added, replaced, revised,
or removed. The three-column sheets show chronological candidates with frame
and revision labels; `manifest.json` binds every thumbnail to the active PNG
path and SHA-256. `check_keyframe_review.py` fails if the manifest, the active
plan, the full-resolution PNG hashes, the review-table links, or any scene
sheet disagree. A sheet is a review aid, not visual approval: owners still
review each candidate at full resolution.

The contract uses `normalized_crop.v1`, rebuilt directly from its approved
plate, so no ignored `work/` crop is needed. The cropper records the source
plate hash, normalized rectangle, integer pixel bounds, resulting crop hash and
the no-resampling rule in a receipt.

## Deterministic base composition

For continuity-critical wide or medium frames, `production/keyframe.py` can
take a story and frame ID and derive its crop, staged actor contacts, anatomical
height targets, camera focus and anchor ID. Pass an isolated character still
for each visible actor:

```bash
export TMPDIR=/scratch/project_465002727/jelealro/tmp
mkdir -p "$TMPDIR"
python3 production/keyframe.py \
  --story lion_and_mouse_v6 --frame s16_p01 \
  --char leo=approved_or_reviewed_leo_pose.png \
  --char milo=approved_or_reviewed_milo_pose.png \
  --out "$TMPDIR/s16_p01_base.png" --write-edit-mask
```

The compositor writes a sidecar with portable source labels and SHA-256 hashes.
RGBA character and prop layers retain their supplied alpha, including transparent
holes between limbs or net strands. RGB studio stills continue to use the matte
extractor. The Python composition API accepts per-layer `shadow` and `light`
settings; use `shadow: 0` for an overhead/rope overlay and `light: 0` when the
generated layer already has the reviewed canonical illumination. Materialize and
normalize the registered crop to 1920×1080 before applying delivery-space blur.
For a puppet with planted paws at different depths, a layer can supply
`contact_shadows: [{"u": 0.3, "v": 0.98, "rx": 0.07, "ry": 0.012, "blur": 0.008}]`.
Coordinates and radii are fractions of the trimmed alpha bounding box; `u,v`
identify the actual support point. Supply one entry per planted contact, leaving
airborne feet unshadowed. The compositor mirrors these anchors with a flipped
layer and protects the plate outside the combined actor/contact regions.
The optional edit mask marks the character/contact-shadow regions white and
the protected registered background black. Pixels outside the white area are
verified unchanged by the compositor. A later focused image edit should use
that mask and the same approved source stack; mask use does not replace review.
`--blur SIGMA` is available for portraits and other intentional defocused
backgrounds. Staged portrait views carry their blur calibration in the staging
plan.

## Camera, lighting and mouth continuity

Owner standard (2026-10-15), applicable to current and future work: close-ups
show head, full mane/ears, shoulders and upper chest, with lower body, feet and
tail below/outside the crop. the current `s15x_p03` selection in `keyframe_plan.json` is the selected v6
framing example. A blurred full-body shot fails this composition standard.
Register an intentional camera crop and its framing reference; do not resize
anatomy to make an actor fit. `camera_center_xy_on_plate` can aim a portrait
above its unchanged physical support point.

For trapped Leo, preserve the same net over the crown, outer mane and shoulders,
with an unobstructed face. Carry a single connected knot/diamond layout across
poses; fixed ground anchors stay fixed and body-supported rope can deform only
with the body. Expression edits should freeze the surrounding net. Boundary
config `prop_continuity_rules` are carried into video transition records so
motion planning retains these constraints. Different crops are cuts, not a
morph between net layouts. Endpoint stability reduces interpolation ambiguity;
only a rendered motion review can establish temporal stability.

Camera-family changes are explicit cuts in `video_boundary_plan.json`; a crop
changes screen occupancy, not character anatomy. Scene 07's blurred speaker
portraits calibrate the Scene 08, 12 and 15 dialogue coverage. Scene 16's
identical wide setups share one anchor ID. Dusk location clauses preserve cool
ambient color and the approved warm rim direction, and prohibit a global orange
grade. Production boundary frames use closed mouths; speaker and emotion stay
in metadata for later lip-sync.

Each visual review records the planned camera family, the matching
owner-approved anchor ID and hash, a canonical SHA-256 for every visible actor,
and measured same-depth size evidence. The v6 same-depth standing-height ratio
comes from `visual_bible.json` (0.25, with a 0.22–0.28 review range); the
staging plan supplies each frame's depth, contact, crop and target height. Do
not use historical v4 0.55/1:3 direction as a v6 generation target.

Full-resolution visual approval remains a separate human decision tied to the
exact candidate SHA-256. Review records must include all required visual checks
and, for each visible actor, the expected and observed visible paw count,
confirmation that no limb is missing or duplicated, and a written support
contact observation. This is recorded evidence for human review; the gate does
not infer anatomy from pixels. The runtime preflight stays blocked until every
active endpoint passes that review.

`keyframe_visual_reviews.json` also binds every active candidate to its current
staging state and explicit disposition. A stale camera-plan frame is marked
`supersede_for_camera_plan`; that is a regeneration state, not a visual
rejection. A rejected candidate remains rejected for its recorded hash. Adopt a
new PNG with `production/revise_keyframe_candidate.py` only after required
canonical, prop and setup-anchor authorities are approved. The command requires
a genuinely newer revision and an existing replacement PNG before clearing
stale status, and it retains the old hash and review history.

## Current v6 owner-review blockers

The v6 data intentionally records Milo's revised body foundation and combined
pose atlases as pending owner hash-bound review. Setup anchors and the acorn/net
prop references also remain pending where noted in their source records. The
generation and revision gates stop on those missing approvals instead of
guessing. The restored `s13_p06_r01` candidate is a recoverable prior image;
the declared r02 bytes were not found in the checkout or Git history. The
original unreferenced `s07_p03_r03` file was removed and contact sheets rebuilt.

The 13 October second image audit records four active hash-bound rejections
(`s08_p04`, `s10_p02`, `s14_p06`, `s15_p04`) and ten frames that need fresh
camera-plan candidates. All other active candidates remain pending visual
review. See the [remediation report](audits/lion-and-mouse-v6-second-image-audit-remediation-2026-10-13.md),
the [active keyframe review inventory](../stories/lion_and_mouse_v6/KEYFRAME_REVIEW.md),
and the [29-family anchor selection packet](audits/lion-and-mouse-v6-size-anchor-review-2026-10-13.md)
for exact hashes and owner decisions.

Historical generated-image cache paths have been moved into labeled,
non-actionable provenance fields. Missing old image inputs are reported as
historical provenance gaps; they are not usable as current generation inputs.


**Owner rule — Milo teeth (2026-10-15):** Milo has no visible teeth in any future artwork, including smiles, speech and gnawing. Mouth-to-knot contact uses soft felt lips and a small mouth crease. Never add exposed incisors, white tooth shapes or fangs. This explicit owner rule overrides tooth shapes in historical candidates.
