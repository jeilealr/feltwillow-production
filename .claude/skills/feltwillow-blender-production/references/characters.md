# Character intake, identity and mesh preparation

## Begin with the actual asset

Use the already promising Tripo Leo as the first candidate rather than paying to regenerate it or rebuilding it from primitive spheres. Preserve its raw downloaded file, all maps, provider task/request ID and settings when available. Missing provenance is recorded honestly; do not invent a seed or generation prompt. Make a separate Blender working revision. [T03](sources.md#t03)

Inspect in neutral lighting from front, both sides, rear, top/bottom where relevant, and intended story cameras. Include clay, material, wireframe and silhouette views. A rotating preview does not reveal reliable topology, UV quality, internal shells or rig suitability. Open the actual model to check them. Missing Leo whiskers may be an inexpensive curve repair; the rear mane needs deliberate wool-lock shape, not repeated bead rows. These are user-reported leads, not new visual verdicts made by this skill.

## Write an identity sheet before changing the mesh

Bind exact reference files and approval scopes. List mass/silhouette, head-to-body proportions, face landmarks, distinctive asymmetries, material regions, eyes, ears, muzzle/beak, mouth, limbs, appendages, accessories and forbidden changes. Separate measurable landmark distances from qualitative character recognition. Record unknown backside details as inferred and pending review.

Use anatomy profiles in `anatomy.md`. Ask whether the character must grasp, perch, fly, crawl, swim, coil, speak, wear clothing, change posture or interact with a prop. Required actions determine topology and controls. A neutral beautiful sculpture is not yet an animation asset.

## Intake audit

Check object transforms and unit interpretation; parent/root hierarchy; negative scale and mirroring; material slots; normals; holes; disconnected components; non-manifold regions; duplicate internal shells; extremely thin parts; self-intersection; face density around bends; UV seams/overlap; texture resolution relative to shot size; and external files. Do not delete every disconnected island: whiskers, eyes, wing feathers and mane locks may intentionally be separate.

Map semantic parts to objects, vertex groups or bones. Four mesh objects do not prove four paws, and one mesh object can contain an entire valid animal. Separate anatomical existence from camera occlusion. Mark whether a part should be visible in each review camera. Never add a duplicate far limb merely because it is naturally hidden in the source view.

## Repair decision

| Condition | Preferred experiment |
|---|---|
| Shape good, one small feature missing | Local controlled repair, compare before/after |
| Face good, body deforms poorly | Preserve visible silhouette; retopologize deformation zones |
| Dense but static background sculpture | Keep as static candidate; optimize only after render benchmark |
| Baked shadows painted into color | Separate material/lighting issue; inspect albedo before repainting |
| Incorrect unseen anatomy across multiple views | Prepare consistent approved views, then evaluate a new candidate only with spending approval |
| Repeated failures on the hero face/rig | Request targeted artist input or change method, not endless blind generations |

Quad output is an option, not a deformation certificate. Proper edge flow and volumes at joints matter more than the percentage of quads. Tripo H3.1 and the tutorial's P2 pipeline are not interchangeable products; discover supported parameters for the chosen endpoint. [T03](sources.md#t03), [T04](sources.md#t04)

## Parts: use selectively

The one-hour tutorial's part strategy is useful for replaceable accessories and localized control [Y01](sources.md#y01). For Feltwillow, split at defensible seams: eye components, mane versus body, hat, basket, rigid beak or hoof sections as design permits. Avoid cutting continuous deforming skin into overlapping chunks that open during a turn. Check attachment motion and shadow discontinuities. Never regenerate each part independently without the same shared character references.

Keep sculpt/high-detail source separate from the production mesh. Establish topology, UVs and material regions before final shape keys and grooming. Later topology edits invalidate dependent weights, facial shapes and curve attachment evidence; do not silently propagate them. Shape keys assume a stable vertex correspondence [B03](sources.md#b03). Baking can move shading detail to a lighter mesh, but cannot preserve a silhouette that has been removed [B05](sources.md#b05).

## Neutral scale calibration

Choose a documented unit system. Record neutral landmark distances in world units after evaluated transforms. Normalize once at the asset/root level before rigging; preserve that convention thereafter. Store separate visible pose bounds for render QA, not as the physical-scale source. Include a common-depth lineup and a same-depth set landmark for the initial approval. A tail raised above the head, a giant hat or a strand of wool must not redefine standing height.

Do not apply `milo.scale = leo.scale * 0.25`. Object-scale numbers do not compare different source meshes. Measure the two anatomical reference distances, solve the required uniform scale factor, apply in the planned normalization stage, then verify from independent landmarks. Once animation begins, reject unexplained root or bone scale animation.

## Exit evidence

Deliver untouched input, candidate `.blend`, dependency manifest, neutral comparison sheet, semantic-part map, repair log and a decision: suitable for rig trial / needs targeted repair / not suitable. Do not call it canonical until the owner selects the new 3D interpretation. Keep inferred geometry and unseen forms explicitly reviewable.
