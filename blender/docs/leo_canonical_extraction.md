# Leo: canonical extraction before revision r02

18 October 2026. Interpretation for a **3D candidate**, not new canon approval.
Written after inspecting both source PNGs and the previous prototype renders,
before changing geometry. Exact SHA-256 bindings: `../config/leo_pass_r02_sources.json`.

## Authority and current rules

1. `character/characters/lion_and_mouse_v6/Leo/canonical/full-body_leo_neutral_pose_r01.png`
   is the approved identity authority (hash beginning `6b587c8e`).
2. `Leo/references/l_complete_reference_r01_candidate.png` is supporting,
   pending atlas authority (hash beginning `73aa4429`). Side/rear volume and
   pose behavior are useful hypotheses, not approval for a changed face.
3. Current v6 README, visual bible and owner acceptance ledger distinguish
   selected 2D images from technical/3D readiness. Older v5 descriptions do not
   override these PNGs. The skill's statement about a promising Tripo is a
   historical lead: no such mesh has been located in the searched local areas.

The explicit repository-wide no-visible-teeth owner note is about Milo. For
this Leo task the owner's narrower direction is unambiguous: **neutral closed
mouth, no visible teeth**, no invented mouth interior or facial system. The
atlas's snarling/net pose does not override that neutral expression.

## Observed identity

| Property | Extraction / what must not drift |
|---|---|
| Body | Pale honey-cream/golden tawny needle-felt; lighter warm cream chest, belly and paws. Never use lighting as a replacement for intrinsic pigment. |
| Mane | Warm natural chestnut/golden brown, interspersed honey edges and curl tips; deep brown recesses, neither gray nor a uniform orange ring. |
| Ears | Rounded cup-like honey outer rims, apricot/salmon recessed inner felt; sit high and wide within the mane, not above it like mouse ears. |
| Eyes | Large amber irises, dark round pupils, warm off-white sclera and narrow dark rims, small controlled highlights. Rounded sockets and cheek support; avoid pasted-on protruding eyeballs. |
| Muzzle | Short projecting cream twin oval pads, broad cheek transition and distinct soft cream chin. Small closed Y/soft smile seam, whisker dots and fine pale whiskers on both sides. |
| Nose | Dark warm brown, broad rounded inverted triangle with a slightly lobed upper edge; tactile matte felt, not a tiny sharp black tetrahedron. |
| Expression | Gentle attentive youthful face; lifted inner brow, relaxed mouth, no snarling or tooth shapes. Canonical slight head tilt is expression, not permanent anatomical asymmetry. |
| Proportions | Large head framed by a still larger rounded, slightly bottom-tapered mane; compact substantial barrel body, strong shoulders, short-to-medium sturdy legs. Four distinct grounded paws, front/hind anatomy differentiated. |
| Paws | Broad soft cream pads with four rounded toe lobes and shallow creases, no claws. Forepaws especially substantial; do not substitute narrow flat discs with black stripes. |
| Mane construction | Overlapping thick rolled locks; varied broad S/C turns, a prominent forward forehead sweep, side spirals and heavier under-chin locks. No even concentric rows, thin decorative rings, beads or flat rear disc. Back volume inferred with help from atlas. |
| Tail | One slender golden curved cord from rump, initially dips then turns up, one chestnut teardrop tuft with pointed soft tip. Tuft should read as wool, not an inflated oval cap. |
| Surface | Compressed, looped short wool with subtle flyaways; matte and tactile at miniature scale. Shape first, pigment second, stable attached fibers third. No realistic long lion fur, gloss or knitted stitches. |

Single-view ratios are perspective estimates. The face occupies roughly half
the mane width; the torso length reads near one mane diameter. These are useful
art targets, not surveyed orthographic measurements. Rear lock patterns are
inferred and require owner review. Avoid perfectly mirrored curls while keeping
eyes/paws anatomically coherent. Do not randomize distinctive locks per build.

## Starting-point decision

The only located character mesh is
`blender/assets/characters/leo/leo_canonical_candidate.blend` (previous Phase 01).
The environment and assembled S05 files are not alternative character designs.
Existing review images show a shallow disk mane, protruding eyes, dark/dull
pigments, long cylindrical body, segmented limbs and undersculpted paws/tuft.
Reuse its editable native geometry and 29-bone feasibility rig as a scaffold,
preserve it byte-for-byte, and save r02 separately. It is not a strong likeness
yet. A new paid generation is neither necessary nor authorized for this pass.

Search scope: repository (including ignored files), sibling Documents work areas,
Downloads and local temporary work; searched native/GLB/OBJ/FBX and ZIP leads.
Live Blender contains only a camera and light in an unsaved scene, no Leo mesh.
An off-machine/unlocated Tripo download remained unknown at that inspection.

### Starting-point update after the owner located the FBX

The owner moved the download to `../model.fbx` during this task. Its SHA-256 is
`3ccead17de1785f9c0d0fa8b3d1f3d531ad8b0d433fba31091f601bda883b9b2`.
Intake found a single UV-mapped mesh (48,753 vertices / 48,742 faces) and four
embedded 2048-square PBR maps. Two actual intake renders show markedly stronger
face, muzzle, body and mane silhouette than either the old native prototype or
its attempted r02 revision. **Select this imported mesh for the deliverable.**
Preserve untouched FBX/maps and the unmodified Blender import. Native r02 is a
retained unsuccessful experiment, not the recommended candidate. Rear mane
bead rows, reduced toe definition and smooth body remain visible import defects.
Exact provider model/version, prompt, seed, request ID and license receipt were
not supplied; record those unknowns rather than inventing provenance.
