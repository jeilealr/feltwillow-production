# Environment image matching: blockout is not visual fidelity

## Contents
1. Scope and source authority
2. Baseline and linked-file intake
3. Representation decision and feasibility
4. Measurable composition before detail
5. Ordered refinement passes
6. Evidence, review and stop rules
7. PATINA and other external assets
8. Persistent world and motion regression
9. Specialist handoff and smallest next action

## 1. Scope and source authority

Use this workflow only when the selected environment mode is `plate_match`: reproducing specific approved scenery or promising an image-matched set. A weak environment render alone does not imply that exact matching is the objective. When the owner requests a richer interpretation, follow [environment direction](environment-art-direction.md) instead; retain useful craft/technical checks here but remove obsolete landmark-error acceptance. Apply it to forests, rooms, villages, rivers and future fable worlds, not just S05. Read environments, camera-light-color, materials and quality-and-risks alongside this module.

Do not confuse four milestones: **blockout**, **camera-calibrated candidate**, **look-development candidate**, and **owner-accepted environment for specified shots**. A reusable tree/path/rock inventory only proves the first milestone. A beautiful unrelated forest fails the reference-match task. The target is the approved miniature felt artwork, not low-poly game art and not generic photographic realism.

Resolve current source files and hashes from the actual checkout. Separate geometry authority, appearance reference, lighting variant, story state and acceptance scope. A later owner-selected frame can be a style reference without redefining the approved world. Keep older accepted look references when explicitly assigned a role. Report conflicts before choosing arbitrarily. Never use an old audit's filename as proof of the current plate.

Retain the established character/anatomy and owner-approval requirements. Do not enlarge a character, delete a root, change the time of day or recolor the entire set to conceal a mismatch. An image can contain impossible perspective or contradictory lighting; document what can be reconstructed, what must be interpreted and what needs owner direction.

## 2. Baseline and linked-file intake

Open only a working copy, with automatic script execution disabled for unfamiliar assets. Inspect actual Blender contents when tools allow it; otherwise report screenshot-only evidence. List linked .blend libraries, packed/external textures, fonts, geometry-node groups, modifiers, caches, renderer, Blender version and missing dependencies. A shot file alone may not contain the environment library. Do not replace missing linked assets with guessed shapes and call that inspection.

Save the original render or make a baseline with unchanged settings, then bind the reference, baseline, shot file and linked library revisions by SHA-256. Record frame/time, camera transform/lens/shift, image dimensions and pixel aspect, engine, samples, denoising, exposure, view transform/look, world/lights and compositing. Store paths relative to the repository, not a Downloads folder. Do not copy bulky source art into the skill.

Create a review from `assets/templates/scene-match-review.md` and a mismatch backlog before modeling. Rank problems by visible impact and story interaction. A low-impact leaf should not displace a wrong trunk silhouette, root contact or horizon.

## 3. Representation decision and feasibility

Choose the smallest representation that preserves the approved look **and** supports planned cameras/actions:

| Need | Preferred starting option | Must prove |
|---|---|---|
| Fixed distant sky, mountains, far foliage | Approved matte or shallow layered cards | No double lighting, alpha fringe or camera-envelope failure |
| Modest parallax background | Low-relief reconstruction or separately projected layers | Correct depth ordering and uncovered regions at envelope extremes |
| Hero tree, root, doorway, rock with contact | Reviewed 3D geometry and material regions | Shape, support, shadows and close-view fidelity |
| Ground under characters | Actual terrain/support geometry, possibly projected texture | Feet/shadows meet visible surface; no camera-only illusion of support |
| Broad camera travel or relighting | More complete 3D assets | New angles/lighting preserve the same landmark identity |

Camera projection is a valid tool, not a claim of a universally correct 3D world. Blender provides projection onto UVs [B17](sources.md#b17); test its limitations on the installed version. Never stretch the entire reference image over one plane and present it as a reusable navigable set. Keep projected regions explicitly labeled, tied to a fixed projection camera and approved view envelope. Do not move that projector with the shot camera to hide failures.

For projected/matte regions, distinguish appearance already containing shadows from a surface intended for relighting. Avoid multiplying baked sunset shadows with new scene lights or grading a display-referred plate twice. Test shadow catching, ground contact and foreground occlusion separately. Prefer real geometry in interaction zones. A high-fidelity 2.5D fallback is preferable to pretending a poor full-3D reconstruction matches the plate; ask before changing the agreed deliverable.

## 4. Measurable composition before detail

Record 8-15 meaningful correspondences when visible: trunk edges at several heights, root endpoints, rock silhouettes, path edges/bend, horizon landmarks, stream banks, canopy openings and sun position. Fewer are acceptable when justified. Do not invent measurements on occluded or absent landmarks. Separate observed pixel locations from inferred world coordinates.

Use normalized image coordinates with top-left origin, consistent with `assets/templates/scene-match-landmarks.json`. Record uncertainty and semantic meaning. Measure height/width of hero silhouettes and the proportion of clear path, vegetation and sky, not just object centers. The helper only reports supplied point discrepancies; it does not detect landmarks or solve the camera.

Fit lens/camera, ground orientation and large forms with simple materials and fixed neutral diagnostics; also retain a story-light comparison. Disable DOF, ambient motion and heavy fibers for calibration. Keep sufficient resolution to read silhouettes. An organic scene is not guaranteed to have usable parallel lines for a unique camera solve [B18](sources.md#b18). Preserve inferred-versus-measured labels.

Do not allow independent per-shot landmark scaling. Establish the environment coordinate system once. Convert existing 2D contact/depth plans through a calibrated projection and actual support surfaces, not by copying normalized values into Blender coordinates. Use the approved character assets or neutral-size proxies as rulers; never edit their proportions to compensate.

## 5. Ordered refinement passes

### A. Camera, silhouette and negative space
Match trunk framing, root spread, canopy openings, horizon, path and key rock arrangement. Render actual camera views and overlay them before expensive surface work. Reopen this pass after any later silhouette or camera change. Keep a before/after with identical comparison settings.

### B. Early light/value block-in
Establish the large dark/light/color masses early: sky gradient, key-light direction, shadow shape, canopy shade and distance separation. Lock color management and expose a material swatch under neutral and story light. Do not postpone every lighting decision until the end, but do not use a global orange grade to conceal incorrect materials. AgX and other view transforms change displayed highlights/color; record the selected transform, do not prescribe one universally [B12](sources.md#b12).

### C. Hero tree and interaction roots
Match overall silhouette first, then medium-scale form: asymmetric trunk taper, branch forks, broad root flare, embedded versus exposed roots, coherent bark flow and moss placement. Roots should grow out of the trunk with plausible continuity, not look like uniform sausages glued on. Noise/bump cannot repair the wrong silhouette. Test Milo/Leo routes and future species clearance before dense dressing.

Use an existing good mesh when available. Escalate a persistently crude primitive tree to a targeted sculpt/curve mesh, a vetted reusable asset or a separately approved generation only after showing what failed. Do not make every environmental object a separate paid request. Keep static major branches distinct from animated leaf-tip groups.

### D. Terrain, path, rocks and water edges
Break ruler-straight path boundaries with authored masks and varied transitions while preserving route width and support. Make root-to-ground and stone-to-soil contact convincing. Use a few recognizably asymmetric hero rocks, not randomly placed identical smooth blobs. Match bank contours and the visible stream reflection/glint where the source shows water. Exclude foliage from planted paw zones and designated travel lanes.

### E. Layered vegetation and depth
Build a small family of reviewed felt tufts, moss patches, broad-leaf clusters and canopy clusters. Distribute by authored region, density, scale and orientation with stable IDs/seeds; preserve clearings and hero placements. Vary clustering at large, medium and small scales. More instances of one coarse leaf do not create better grass. Avoid a uniform confetti carpet, identical tree-ball rows, accidental neon patches and excessive micro-noise.

Match density and edge silhouettes at foreground/midground/background distances. Keep distant contrast/detail appropriately restrained as an artistic match, not through arbitrary heavy fog. Geometry Nodes can provide reusable generators and scatter control; the Blender Studio course supports that workflow, not a claim that its low-poly examples are final Feltwillow assets [S06](sources.md#s06).

### F. Sky, distance and final light/material match
Refine cloud silhouettes, sunset position/gradient, distant hill layers and tree-line shape. Keep a restrained warm key/cool ambient relationship appropriate to the selected plate, not a story-global sunset recipe. Sky may be a matte/2.5D solution. Expose each layer's camera and motion limitations. Do not assume the sky must be generated again or built as simulated volumetric clouds.

Match material detail at three scales: large color regions, medium wool/bark/moss forms, and fine fibers/roughness. Tune real-world texture scale; use surface maps for relief response and sparse geometry/curves for meaningful silhouettes. Avoid glossy clay, smooth rubber bark, metallic felt, exaggerated displacement and realistic shaggy fur. Freeze texture coordinates to assets. Re-enable DOF only after geometry passes; blur cannot be used to hide failed hero details.

## 6. Evidence, review and stop rules

For every consequential pass, save: clean full-frame render, reference, 50% overlay or alternating comparison, and at least two matched-coordinate hero-region crops. Retain an earlier good candidate for regression. Include the full view so crops cannot hide a new horizon or path failure.

Use `scripts/scene_match.py` for diagnostic overlay, split, difference and supplied landmark-error reports. Inputs must be equally sized, opaque, 8-bit display images; the helper does not silently crop, warp, resize or color-match them. Convert embedded ICC profiles to sRGB where possible; require an explicit sRGB assumption for untagged files. Do not compare raw scene-linear EXR to a display PNG. Difference pixels and landmark statistics are diagnostics, not an aesthetic score, renderer validation or owner approval.

Review each dimension separately: composition; hero shape; support/contact; terrain; vegetation hierarchy; sky/depth; light/color; felt material; camera-envelope behavior; temporal stability. Statuses are `unreviewed`, `needs_revision`, `candidate_for_owner_review`, `owner_accepted_for_scope`, or `blocked_missing_evidence`. A mean score cannot cancel a failed root interaction or obvious wrong tree. Technical validation can pass while look remains `needs_revision`.

The task brief must name a pass limit and time/render/spend budget. After two successive passes that fail to improve the same high-impact mismatch, stop and change method or request targeted human art input. This is a suggested escalation default, not a promise of completion in two passes. Report what was tried and why another identical attempt is unlikely to help. Never label a blockout final because the budget ended.

## 7. PATINA and other external assets

A whole landscape is not a single material swatch. For a clean existing surface use `fal-ai/patina`; for a new tileable swatch use `/material`; for isolating bark, moss or ground from a scene use `/material/extract` after approval [P01](sources.md#p01), [P02](sources.md#p02), [P03](sources.md#p03). Provider documentation describes inferred maps, not measured material truth. Verify current schemas/prices before any paid operation.

Choose one region and one swatch test first. Preserve body/landmark color regions and UVs. Use color textures as color and data maps as non-color; check tangent-space normal convention and strength. Treat felt/soil/stone as nonmetallic unless the approved design says otherwise. Inspect tile boundaries, texture scale, baked directional shadows, roughness and height artifacts. A successful API response does not authorize applying the maps to the entire set. Keep A/B renders with and without the new material and save source/job/output hashes. This skill update does not authorize any paid call.

## 8. Persistent world and motion regression

Keep geometry, dressing, lighting, cameras, ambient systems, character action and prop state separate. Do not modify a shared published environment revision in place and accidentally alter other scenes. Inventory dependents, create a new candidate library revision and update only the scoped shot links until approved. Preserve backups and test missing linked-file handling.

After a still candidate passes visual review, test a short preview at start/middle/end plus the relevant maximum camera displacement. Check parallax, card exposure, texture swimming, thin-leaf/fiber flicker, denoising instability, root support and foreground occlusion. Keep global story time for wind/water/clouds and preserve static major landmarks. Render an ambient-off diagnostic and a restrained ambient-on candidate. Do not start full animation merely because one frame looks convincing.

## 9. Specialist handoff and smallest next action

Coordinator owns scope/authority/budgets. Reference/design reviewer annotates the source and uncertainty. Camera specialist fits projection/light. World builder refines geometry/dressing. Material specialist prepares swatches. Independent reviewer compares exact images without changing the scene. Use one writer per .blend file; perform these as explicit sequential roles when no subagent facility exists.

For the submitted S05 comparison, use the specific case study only as a starting hypothesis. Re-read current local files before choosing a plate or editing the root. Start with baseline dependency verification and a camera/hero-silhouette pass, not full regeneration, new animals or a giant scattering script. Report the largest unresolved fidelity gap and one next bounded correction.
