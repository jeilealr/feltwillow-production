# Reusable handcrafted environments and ambient systems

**Select the design mode first:** Read [environment direction](environment-art-direction.md). Use [environment image matching](environment_image_matching.md) only for `plate_match`; evaluate `reference_inspired` and `original_design` against their authorized brief. A blockout can be structurally valid while failing the handmade look.

## Contents

1. Environment contract
2. Choosing 3D versus 2.5D
3. Reusable component kit
4. Building and validating a location
5. Calm ambient presets
6. Season, light and growth variants
7. Reuse and agent handoff

## 1. Environment contract

Treat a location as a persistent world asset. Record selected plate/reference hashes; landmark IDs and positions; camera envelope; ground/support surfaces; paths and exclusion regions; interaction anchors; material palette; visible extent; dressing seed; ambient behavior; lighting variants; and hidden/inferred geometry needing review. Separate source appearance from measurable reconstruction decisions.

A tree trunk, root fan, stream bank or doorway can be a landmark, collision surface, support and narrative object at once. Register all relevant roles. A pretty environment that cannot support the character actions is not ready. Use a common coordinate convention and physical scale across adjacent sets or explicitly document scale transitions.

## 2. Choosing 3D versus 2.5D

Full geometry is warranted for silhouette-changing camera moves, contact objects, important shadows/reflections, foreground occlusion and substantial parallax. Camera-projected cards, shallow relief and layered scenery can be appropriate for distant mountains, sky, clouds, tree masses and fixed-camera background detail. Do not build invisible surfaces simply for completeness.

Every 2.5D choice has an approved view envelope: camera positions/orientations, focal lengths, resolution and permitted motion. Test the envelope extremes, not only the source view. Check card edges, parallax mismatch, disocclusion, depth of field, alpha fringes, reflections, shadows and geometry behind silhouettes. Do not silently billboard trees toward every camera; turning foliage can change shadows and landmarks. Promote a card to 3D when it becomes interactive or fails the planned view.

A Tripo whole-scene reconstruction can be a useful blockout or restricted diorama. It is not automatically a complete navigable set. Hidden backs and flat backing structures must be inspected. Prefer separately controllable hero tree/root, rocks and foliage modules where multiple cameras or interactions demand it. Do not separate every leaf into a paid generation task.

## 3. Reusable component kit

| Component | Construction options | Required checks |
|---|---|---|
| Ground/path | Sculpted or modeled terrain, simple felt layers, authored route | Continuous walkable surface, no decorative foliage supports |
| Trees/roots | Stable trunk and root geometry, reusable branch/leaf clusters | Root contacts, bird perch anchors, mane/wing clearance |
| Rocks/stumps | Reviewed static meshes with crafted materials | Scale, silhouette, collision proxy agrees with visible top |
| River/pond | Stylized surface/ribbons, animated coordinates or gentle shape motion | Stable banks, waterline, crossings and reflections |
| Grass/flowers | Instanced clumps, stable IDs, optional anchored tip bend | Exclude footpaths, avoid intersections and camera pop |
| Clouds | Felt cards or simple volumes at planned depths | Slow drift bounds, no abrupt reset or lighting change |
| Mountains/distant trees | Cards, low relief or simple geometry | Camera envelope, horizon match and parallax |
| Buildings/doors/bridges | Modular visible geometry plus contact/support forms | Doorway clearance, step heights, crossings, prop scale |
| Interior dressing | Shared craft materials, reusable objects | Graspable items, character seating, occlusion and light continuity |

Use Geometry Nodes for repetition where it reduces work. Fix instance identities and seeds [B09](sources.md#b09). Do not make scattering depend on a vertex index that changes during later topology edits without migration. Keep hero landmarks outside random scatter. Store intentional missing/cleared patches as part of the environment contract.

## 4. Building and validating a location

Read the current scene list and hardest interaction. Identify a primary camera, establish rough dimensions with character proxies, match or intentionally design landmarks according to the selected mode, then test nearby camera views. Refine hero geometry and materials only after composition and scale work. Record which depth interpretation is inferred: one image cannot uniquely define the entire world.

For S05, use the latest owner-selected design mode. Reconstruct the selected plate in `plate_match`; in `reference_inspired`, create a richer Great Tree candidate informed by its mood/craft/narrative identity without enforcing every old coordinate. Do not invent a photoreal forest or silently replace accepted v6 imagery. Separate a world-space tree/root setup from the scene camera. Establish an actual supported resting area for Leo and a plausible Milo approach/contact route. Test that the nose encounter works at the intended physical ratio before adding hundreds of plants.

Define stable named surfaces and anchors, for example `SURF_Path`, `SURF_Root_A`, `PERCH_Branch_01`, `WATER_Stream_01`. Keep collision proxies aligned to visible geometry; invisible giant colliders cannot justify floating paws. Include a rendered route/clearance overlay and a clean beauty frame.

## 5. Calm ambient presets

Create presets as versioned parameter sets, not independent animations regenerated per shot. Suggested names are `gentle_breeze`, `river_gentle`, `clouds_slow`, and `still_evening`; these names are proposed, not existing repository tools. State amplitude, period, direction, phase convention, affected region, exclusions, global story-time origin and seed. Calibrate amplitude visually at delivery size; no universal numeric preset is asserted here.

Use low-amplitude, low-frequency changes with local variation around a shared wind direction. Bend grass/leaf tips about anchored bases. Major trunks, root landmarks and mountains remain static unless the story explicitly moves them. Water motion stays inside the bank and avoids a realistic ocean look. Clouds move slowly and wrap only outside camera coverage or with a reviewed continuity method. Keep illumination stable even while clouds move unless an intentional light event exists.

Use `scripts/ambient_motion.py` only as a tested mathematical building block for deterministic phase, not a ready-made Blender node network. Apply rotations/deformations in a proper local frame in the implementation. Allocate a motion budget per shot: usually one primary character action and a few quiet environmental cues. Don't combine excessive breathing, swaying, flicking, nodding, drifting and camera motion.

## 6. Season, light and growth variants

Day and dusk should reference the same geometry revision when only lighting changes. Snow coverage, autumn leaves, flood state, fallen tree or damaged bridge are explicit world variants with declared geometry/material differences. Do not recolor or move everything casually between time-of-day shots. A leaf dropping or a branch breaking is an event; it changes state and may affect later collisions.

Maintain environmental scale when characters change species or a fable intentionally contrasts sizes. A bird landing on a tree branch needs usable thickness and clearance; a human approaching the same tree must not receive a silently rescaled copy. Stylized world-scale exceptions require owner direction and documented camera/context boundaries.

## 7. Reuse and handoff

Publish a candidate environment library with named collection, surface/landmark inventory, camera envelope, lighting variants, ambient configuration and performance figures from actual tests. Link it into shots; keep stateful props and scene timing outside permanent geometry. Let the world-builder own the library and the shot assembler own placement overrides. Independent QA must check both a clean environment and the actor interaction.

Potential future library names: `ENV_Stream`, `ENV_GreatTree`, `ENV_Fork`, `ENV_Shortcut`, `ENV_Trap`, `ENV_Home`. Resolve actual story/location IDs before naming. These are examples, not preexisting assets.

Source basis: linked-library behavior [B06](sources.md#b06), stable procedural IDs [B09](sources.md#b09), and stylized production choices from Blender Studio [S01](sources.md#s01). All environment decomposition, motion-budget and camera-envelope rules above are original Feltwillow recommendations.

## External asset discovery and adaptation (1.3.0)

Use [external-assets](external-assets.md) and [source leads](asset-sources.md) when existing resources or a small verified free kit can fill a demonstrated gap. Import only reviewed candidates into isolated test files. Adapt useful mesh structure to the felt medium; do not replace the world with an unrelated stock scene. Build support/contact geometry where required, preserve scale and seeds, and publish immutable environment revisions after review.
