# Leo canonical Blender development: first serious imported candidate

18 October 2026. **A promising prototype now exists. It is neither approved
canonical nor ready for production animation.** Recommended file:
`../assets/characters/leo/leo_canonical_tripo_candidate_r01.blend`.

Candidate SHA-256:
`69d4c29d2b6442eee9bb8de9cfb2289657aeec315bf99790756a2be5a67b0ac9`.
Blender 5.2.2 LTS, build d13f752e3b9c; isolated local background execution,
automatic script execution disabled. Existing unsaved interactive Blender was
inspected and left untouched. No paid generation, uploads, commits or pushes.

## Sources inspected and starting asset

Read `AGENTS.md`, `CLAUDE.md`, the requested skill and its character, material,
anatomy, rigging, camera/light/color, tool, rendering, baseline, validation and
quality/risk references; task/review templates and inspected helper scripts.
Read current v6 README, Leo visual-bible identity and current acceptance-ledger
context. The explicit no-visible-teeth repository owner rule is Milo-specific;
this task independently requires a closed, tooth-free neutral Leo. No snarling
atlas frame was used to redesign his neutral mouth.

Visually inspected the approved full-body PNG and pending consolidated atlas,
then the old native model's comparison renders. Inventoried existing native
Leo, environment and S05 libraries, build/pose/render scripts, manifests and
Phase 01 documentation. The environment/S05 paths were inventoried, not modeled
or migrated. The old Leo library was actually opened and inventoried.

Initial searches did not locate Tripo. A native scaffold revision was attempted
and its real preview rejected: it retained weak face likeness and a conspicuous
mane gap. That experiment is preserved as `leo_canonical_candidate_r02.blend`
with `leo_pass_r02.py` and `renders/leo_canonical_r02/first_preview.png`;
**do not use it as the preferred candidate**.

The owner then located `../model.fbx`. Actual two-angle intake renders showed
substantially stronger likeness, so work switched to that mesh. Its raw hash:
`3ccead17de1785f9c0d0fa8b3d1f3d531ad8b0d433fba31091f601bda883b9b2`.
Untouched FBX, four extracted embedded maps and an unmodified Blender import
are preserved under `assets/characters/leo/imports/tripo_owner_model/`.
The original 2D sources remain strongest authority; exact reference hashes are
in `leo_pass_r02_sources.json`, the candidate metadata and delivery manifest.

## What changed in the selected candidate

- Uniformly normalized the imported mesh to 1.5 BU surface height, grounded its
  lowest vertex and rotated import +X forward to repository -Y forward. One BU
  remains .2 m: an approximately .30 m miniature. This provisional physical
  scale does not alter any story staging or cast-scale record.
- Preserved imported vertex/face topology, shape and UV atlas. Index-by-index
  comparison to the import confirms normalization error below 1.4e-7 BU.
- Preserved base-color/normal maps and packed all four original 2048-square maps.
  Wool uses metallic 0, roughness .92, restrained specular/sheens and normal
  strength .55. Original roughness/metal maps remain preserved but disconnected
  from the candidate shader. No global color grade or anatomy repaint.
- Added short stable surface wool, separately organized from the source mesh,
  plus three fine cream whiskers per side. No realistic long fur or dynamic groom.
- First fiber trial produced dark mottling. Preserved it under `iteration_01/`
  and `leo_tripo_fiber_iteration_01.blend`; corrected converted-strand palette
  association using nearest-surface UV interpolation, reduced fiber thickness
  and length, and placed whisker roots by actual muzzle ray intersections.
- Added an asset root, separate removable studio and provisional non-rendering
  rig-plan landmarks. **No deforming rig, weights or facial controls** were
  applied to this mesh. See `leo_tripo_rig_plan.md` for the concrete next test.

## Actual visual comparison

Review files: `../renders/leo_tripo_canonical_r01/`.
`comparison.png` compares canonical, normalized original import and candidate.
`turnaround.png` contains the canonical and eight neutral views.
`atlas_comparison.png` keeps the pending atlas's support status explicit.
`shape_diagnostics.png` exposes clay, wire, silhouette and illustrative lighting.
Full-resolution source PNGs and renders were also inspected separately.

| Feature | Visually observed strengths | Remaining difference |
|---|---|---|
| Face | Recognizable Leo: amber eyes, apricot ears, gentle brows, cream muzzle/chin and closed smile. Much stronger than native scaffold. | Eyes read smaller/flatter and face less plush than canonical; eyelid/highlight detail partly depends on texture. No separate eye mechanism established. |
| Mane | Correct broad head frame, front rolled curls and distinctive forehead sweep; real side/back volume. | Side/rear locks become smooth rounded bead rows. Front locks are heavier/simpler, less organically rolled than canonical. This is the main shape defect. |
| Body | Coherent quadruped, substantial shoulders, cream underside and plausible head/body balance. | Firmer/angular leg transitions and a leaner torso than the canonical's soft felt bulk. The asymmetric imported stance has not been neutralized through a rig. |
| Paws | Four paws exist and are visible across front/side/rear evidence; light toes read clearly. | Toe lobes are simplified/fused, often reading as three rather than the canonical's four rounded lobes. Pads/contact surfaces need shaping; small ground gaps remain. |
| Tail | One curved golden tail and one matching brown tuft; correct broad silhouette. | Tuft looks somewhat like a folded leaf, with too sharp a tip and insufficient wool volume. |
| Silhouette | Canonical-like from the front and preferred three-quarter side; no generic spherical-cartoon rebuild. | Rear mane rows and fore/hind leg contour differences remain exposed in side/rear views. |
| Felt | Matte surface, restrained short fibers, stable intrinsic color atlas and no plastic shine. | Body still reads as smooth textured sculpture/velvet, not the canonical's dense looped wool. Some fine flecks remain close up. Temporal stability is untested. |
| Identity | Promising, recognizably derived from current Leo. | Does not yet match the canonical's warmth, softness, eye proportions and tactile finish closely enough for approval. |

Portrait retains head, ears and mane, but its oblique view includes upper flank
and a small tail segment at the left edge; it is an honest diagnostic rather
than a perfected production portrait. Neutral orthographic cameras are diagnostic
angles, not a recovered lens solve for the perspective canonical. No numerical
pixel similarity score or claimed owner selection is substituted for likeness.

## Evidence and technical limits

Sixteen 768x768 / 40-sample Cycles CPU stills: eight neutral views (front, both
sides, rear, front/rear three-quarter, elevated three-quarter, portrait), three
same-camera import baselines, clay front/rear, wire side, silhouette and one
warm-key/cool-rim study. Story-light study uses the same materials and exposure;
it is not a Scene 05 reconstruction. Final measured render time totals 94.353 s,
individual images 3.414–8.527 s, excluding build/startup. No film throughput claim.

`render_manifest.json` binds all images to the saved candidate hash, settings,
camera transforms and timings. `board_manifest.json` hashes each board/input.
`technical_audit.json` records **12/12 limited structural checks passing**:
source preservation, normalized shape preservation, UV presence, packed maps,
no external libraries/scripts, non-metal material, whisker count, ground/height
datum and the explicit unbound status. These checks do not certify beauty,
anatomy, rigging or topology fitness.

Surface: 48,753 vertices, 48,742 faces, including 48,713 quads, 23 triangles and
6 n-gons. There are **41 non-manifold edges (40 boundary)** and six connected
components: one 48,694-vertex component plus five tiny islands totaling 59
vertices. Do not equate six components with six anatomical parts. Repair these
in context before rigging. Approximate paw-region low points are .00054–.00899
BU above the datum (.11–1.80 mm at this miniature scale). No claim that all four
plantar surfaces have perfect support.

UV overlap, geometric self-intersections, wall thickness, deforming weights,
joint collapse and animated fiber stability remain untested. Added wool and
whiskers currently follow the asset root only: they must be rebound with the
skin before animation. Mostly quad topology alone does not justify rigging
approval. Stale original FBX unpacked-path warnings appeared during raw/import
shader reads; packed image data was retained. The final candidate reopens with
all four maps packed and portable local map labels, and produced the actual
review renders without relying on those missing historical unpacked folders.

## Stage gates and recommendation

- G0 authority: passed for this bounded candidate; rear interpretation pending.
- G1 shape: **not passed** for canonical release; rear mane and paws need work.
- G2 deformation: not tested; guide/rig plan only.
- G3 look: not passed for final felt match; useful matte baseline established.
- G4 set / G5 sequence: not applicable to this Leo-only task.
- G6 release: not passed; no owner 3D selection or production approval.

**Next best step: more mesh refinement.** First fix confirmed topology defects,
replace posterior bead rows with irregular rolled locks, and refine four toe
lobes/shoulder transitions while protecting the face. Then perform the small
head-turn/planted-paw rig test in the rig plan. Improve felt density after shape
and deformation work. No present evidence warrants a new Tripo/fal multiview
generation or an advanced facial system.

## Files created, modified and preserved

New: selected candidate, raw FBX/maps/import, native experiment and fiber trial;
four scripts (`leo_fbx_intake.py`, `leo_tripo_canonical_pass.py`,
`leo_review_boards.py`, experimental `leo_pass_r02.py`); canonical extraction,
task brief/context, two input inventories, source bindings, rig plan, this report,
render/audit/board manifests, sixteen final stills, four boards and preserved
iteration evidence. `delivery_manifest.json` enumerates exact files/hashes.
Existing `blender/README.md` receives a scoped entry pointing to this candidate.

Preserved: approved canonical/atlas PNG bytes, previous native Leo and its
scripts/renders, environment/S05 libraries, story plans and owner ledgers.
Repository-wide refactors, Milo, set work, full animation, Wan/HPC and publishing
were outside scope. No original artwork or provider source file was overwritten.
No paid request or upload was made: new external spend **$0**. Provider generation
endpoint/version, seed, prompt, request ID, historic cost and license receipt
were not supplied for the owner's FBX; they remain unknown. New local additions
use native Blender/Python only. No approval or rights receipt is fabricated.

## Reproduction and verification

From repository root (use the installed Blender executable):

```sh
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_fbx_intake.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python blender/scripts/leo_tripo_canonical_pass.py
python3 blender/scripts/leo_review_boards.py
```

All three were executed successfully (exit 0); board script needs Pillow. The
preserved raw import permits the second command without `../model.fbx` being
present. Intake itself expects the owner's source path and refuses a conflicting
raw-copy hash. To regenerate only reviews use `-- --review-only`; to reopen and
run the structural audit use `-- --audit-only`. Scripts bind both PNG authorities
and the raw FBX hash. A source change stops rebuilding for a new authority review.
Deterministic geometry/seed/settings are recorded; byte-identical `.blend`
serialization across machines is not promised. Existing candidate revisions
should be preserved before future builds because the named candidate output
is regenerated. The prior source mesh is never regenerated or overwritten.
