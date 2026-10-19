# Rendering, portability and optional Wan

## Local first, measured performance

Develop and preview on the user's local machine. Detect the actual CPU/GPU, RAM, Blender version, engine and available backends. Do not infer that a recent Mac will render a full film quickly, or that a PyTorch-compatible HPC GPU supports Blender Cycles. Current Blender documentation distinguishes backend/device support [B13](sources.md#b13); an AMD MI250 system requires its own tested path, not a casual assumption based on consumer HIP cards.

Render one neutral still, one story-light still and one short motion at target delivery dimensions before budgeting the whole film. Record engine, samples, denoising, resolution, frame time, memory and output size. Measure the heaviest expected groom/environment shot too. Estimate total frames times measured cost, then add explicit allowances for revisions and overhead. Do not present a 1-2 week production estimate without this evidence.

## Eevee versus Cycles

Compare only the same calibrated art, camera and light intent. Engines differ in features and appearance; switching is not simply a speed toggle. Inspect felt silhouette, transparency, shadows, reflections and DOF. Select the cheaper engine only when it meets the review target. Keep version-specific engine enums out of copied timeless snippets; discover available engine identifiers from the installed build.

Hair/curve count, subdivisions, displacement, texture size and dense scatter can dominate memory. Start with the least complexity that survives the planned view. Do not bake away the very silhouette quality the owner values. Inspect temporal denoising/noise stability with motion, not a single clean frame.

## Render output and restartability

Render an image sequence rather than a long fragile direct movie encode. Use scene-linear EXR when appropriate for compositing and an explicitly transformed review output. Package frame numbers, rational FPS, color settings, audio references and hashes. Check missing, corrupt and duplicate frames before encoding. Encode once after review; do not repeatedly compress masters.

Distributed frame rendering requires portable linked assets and finished simulation/groom caches. Sequential simulations need a baked state for arbitrary frame access [B10](sources.md#b10), [B11](sources.md#b11). Do not assume cached results survive Blender version changes. Pin versions and test a representative frame on the destination machine against the local result; stable seeds do not guarantee bit-identical output across GPU backends or releases.

## Headless workflow

Use the installed Blender CLI help and current manual [B14](sources.md#b14) before constructing commands. A read-only inventory command is conceptually:

```bash
blender --background --disable-autoexec /path/to/candidate.blend \
  --python-exit-code 1 --python /path/to/blender_inspect.py \
  -- --out /path/to/new_inventory.json
```

The helper writes only the requested new JSON report, not the scene. Test on a disposable asset first. Automatic script execution disabled may prevent trusted custom drivers from evaluating; do not approve animation based on that incomplete evaluation. For final rendering, review and explicitly permit required trusted code in an isolated environment.

Batch render only on allocated HPC resources, never a heavy login-node job. Use site-specific Slurm policy and storage. Do not auto-install packages or expose an interactive MCP server on a compute node. Render from packaged `.blend`/dependencies and scripts; the local authoring agent need not be permanently connected to the farm.

## Backup and portability

Record external image paths, linked library files, fonts if any, caches and code dependencies. Do not promise that a `.blend` or Git clone contains all of them. Pack assets when appropriate, or ship a relative-path bundle with hashes and a restore test. Keep source scene, asset versions and selected outputs in backed-up storage independent of temporary scratch. Record LUMI expiry/retention from current project policy, not an old copied date.

## Wan is an optional branch, not a required enhancer

A good Blender render is already a complete visual output. Ordinary image-to-video conditions on an image; it is not a generic filter that preserves an entire supplied Blender animation. To test Blender-guided generative video, identify an actual compatible video/control-conditioned pipeline, supported representations and preprocessing. Depth, normals, poses, masks and RGB are not interchangeable inputs. [W01](sources.md#w01)

Keep the baseline Blender sequence and compare identity, motion, scale, geography, props and felt texture through the full interval. A beautiful first frame does not justify later drift. Human-motion models may be inappropriate for quadrupeds, wings or unusual appendages. Do not add Wan to compensate for missing rig capabilities without making the compromise explicit.

Select outputs by reviewed shot, but check that mixing Blender and generated footage does not create a visible style discontinuity. No promised automatic "best of both" result is part of this skill. The initial Leo/S05 pilot should establish whether Blender alone reaches the owner's target before adding a new runtime dependency.
