# Material evidence: present, connected, visible, successful

## Contents
1. Distinguish evidence levels
2. Inspect a saved Blender scene
3. Test on the rendered asset
4. Build a differentiated felt environment kit
5. PATINA scope and failure modes

## 1. Distinguish evidence levels

Never equate 'fal connected', 'PATINA generated', 'texture loaded', 'shader connected' and 'looks like felt'. Report them separately:

1. **Provenance:** endpoint, submitted parameters, source/job/output hashes and authorized request receipt. A folder named patina is a clue, not verified account billing history.
2. **Availability:** actual images, dimensions, colorspaces, external paths or packed bytes. One loaded image is not evidence of a complete PBR set.
3. **Graph/assignment:** map connected upstream of an active material output and assigned to the intended geometry/instances. Keep disconnected nodes, old materials and unassigned assets distinct.
4. **Rendered contribution:** a controlled A/B on the same object and camera with that contribution enabled/disabled. A connected input can be muted, multiplied to zero or invisible in the shot.
5. **Visual success:** wool-like form, relief, edge response and silhouette at the actual delivery scale under the intended light, without distracting flicker.

A model or material name is not a pass. Procedural shaders may meet the look without PATINA. Conversely, a correctly downloaded map may contribute almost nothing at wide-shot scale.

## 2. Inspect a saved Blender scene

Use the existing read-only inventory and `scripts/blender_material_audit.py` in the user's supported Blender runtime on a working copy with automatic script execution disabled. The material helper records node/link inventories, images and material-slot users. It does not execute paid services, rewrite shaders, re-render, save the scene or authenticate provider receipts.

Report output-reachable node paths as **potential contributions**, not pixel evidence. Group trees, shader switches, muted nodes, multiple outputs, Geometry Nodes material assignment, object visibility and camera occlusion may require deeper Blender inspection. Never infer active camera visibility from material user counts alone.

Keep diagnostics under work/review storage; hashes bind reports to exact .blend bytes. Resolve missing libraries before declaring a complete audit. Avoid disclosing credentials, arbitrary text-block contents or unrelated custom properties.

## 3. Test on the rendered asset

Use one material on a curved object, a shallow patch and an edge at the planned camera distance. Render under neutral and story lighting, at intended output resolution and a useful detail crop. Hold exposure, color transform, camera, samples and denoising fixed during an A/B. A thumbnail texture cannot prove successful asset shading.

Compare macro shape, medium fiber clumps and fine relief separately. Bump changes shading normals, not the silhouette; true displacement moves geometry and needs appropriate mesh support [B19](sources.md#b19). Sheen supplies a grazing fiber-like reflection, not actual hair geometry [B20](sources.md#b20). Add small amounts of stable geometry/curves where silhouette fuzz is important, not an expensive hair coat everywhere.

Do not blindly increase bump strength, map resolution or fiber count. Wrong coordinate scale, oversized clumps, noisy silhouettes, clipped highlights, tangents, low-contrast light or denoising can all defeat the intended effect. Use a simple baseline to isolate the cause. Do not disable denoising for the whole production without comparison.

Test material features relative to the actor and environment scale. Use consistent units/material coordinates rather than independently scaled textures on every object. During deformation or camera motion inspect texture swimming, aliasing and flicker. Retain rest coordinates/UVs and stable random seeds.

## 4. Build a differentiated felt environment kit

Do not use one coarse noise recipe on bark, path, leaves and rocks and assume naming differentiates them. Aim for distinct construction within one medium:

| Element | Candidate craft treatment | Avoid |
|---|---|---|
| Trunk/root | Compressed wool ridges following growth, recessed folds, embedded wool moss | Rubber tubes, random pits, long fur on bark |
| Moss/grass | Soft irregular cushions, short restrained tufts, matted paths | Pebble/coin carpet or identical jagged chips |
| Leaves/canopy | Varied rounded felt shapes with thickness, layered clusters, subtle edge fiber | Uniform flat shards or repeated low-poly tree balls |
| Rocks | Dense heathered felt, coherent rounded/asymmetric form, modest edge softness | Glossy smooth blobs or metallic mineral scans |
| Path | Compressed earthy felt, subtle wear, integrated softened vegetation boundary | Featureless colored ribbon or knee-high grass in foot zones |
| Distance/sky | Lower-detail soft crafted silhouettes, layered color depth and restrained cloud shapes | Every distant element equally sharp or uniformly fuzzy |

Start with a convincing small kit and distribute it by region. Richness comes from arrangement, material scale and hierarchy, not simply thousands of objects. Keep actors readable and routes clear.

## 5. PATINA scope and failure modes

Choose `/patina` for maps from a clean swatch, `/patina/material` for a new tileable surface and `/patina/material/extract` for isolating a material from a scene [P01](sources.md#p01), [P02](sources.md#p02), [P03](sources.md#p03). Verify current endpoint schemas and quote the exact cost before approval. No paid request is authorized by this module.

Do not pass an entire scenic illustration as if it were a ready-to-tile bark texture. Do not overwrite a character's color atlas with a generic repeating felt material. Preserve color regions, use data maps as non-color, verify normal orientation, and keep felt nonmetallic. Generating all five outputs is optional; omit unnecessary maps. Height stored through a Bump node is not geometric displacement.

For each proposed paid swatch, state the observed problem and why existing procedural/map assets cannot address it cheaply. Run one authorized test, preserve raw maps and receipts, wire the intended surfaces, and compare before scaling out. Without output/node/visual evidence report PATINA use as unverified, partial, or visually ineffective rather than success.
