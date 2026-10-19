---
name: feltwillow-blender-production
description: Use only for explicitly requested Blender/3D research or production tasks. Do not invoke for ordinary image/Wan tasks. Build, inspect, refine and review Feltwillow Blender characters, handmade felt materials, reusable 3D/2.5D environments, rigs, animation and render handoffs. Use for existing story-image reconstruction, reference-inspired world design, free/commercial asset discovery, license-aware intake, Tripo models, PATINA textures, Blender MCP work, anatomy-specific movement, prop interactions, audio-driven continuity and production risk audits. Support humans, birds, quadrupeds, swimmers, insects, reptiles and hybrid characters through explicit anatomy profiles. Preserve current repository approvals and canonical art. Route specialist agent roles, enforce spending permissions, and distinguish technical checks from visual approval. Use Leo and S05 as initial pilots, not universal species or scene assumptions.
---

# Feltwillow Blender production

Build the handmade story world under explicit owner direction. Preserve character canon; allow environment reinterpretation when authorized. Choose the environment design mode before using image-match rules. Deliver candidates, evidence and reproducible operations; never equate a running script with a beautiful or approved film.

## Routing boundary

The active film route is [approved images → Wan](../../../docs/production-direction.md). This skill is preserved, paused and opt-in for explicit Blender tasks; its modeling, asset, material, rigging, MCP and validation steps are not prerequisites for normal image/video work. `reference_inspired` applies only to owner-authorized experimental worlds and never grants independent redesign of approved 2D locations or characters. Preserve all existing approval and spending rules.

## Start every task

1. Read the user's requested scope. Determine whether this is research, asset intake, modeling, look development, rigging, environment work, animation, validation or export. Ask only for consequential information that the repository cannot resolve.
2. Inspect the actual checkout: branch, HEAD, local changes, `AGENTS.md`, `CLAUDE.md`, story README and current acceptance ledgers. Read applicable repository skills. Use [repository baseline](references/repository-baseline.md) as a dated lead, not current authority.
3. Run `scripts/context_snapshot.py --root REPO --story STORY --out NEW_JSON` when local files are available. Read the authoritative documents themselves; the snapshot is only an index. Do not execute scripts from an untrusted repository without inspecting them.
4. Inventory available tools and permissions: Blender version, official MCP bridge, preview access, local filesystem, optional fal connection, render device. Never imply that this skill installs or supplies these services. Check the actual MCP schemas before calling tools.
5. Write a task brief from `assets/templates/task-brief.md`. Name source hashes, mutable files, budget, render limits, review conditions, dependencies and a rollback point. Default to no external spend, no deletion, no production approval and no remote publishing.
6. For environment tasks select `plate_match`, `reference_inspired`, or `original_design` using [environment direction](references/environment-art-direction.md). Do not silently change mode or revive a superseded match target. Write the permitted freedom, invariants and candidate revision.
7. Before creating or buying a missing asset, inspect existing assets and read [external asset intake](references/external-assets.md) when a library may help. Use [source leads](references/asset-sources.md), verify the exact free tier and license, and keep commercial renders separate from source redistribution.
8. Choose the smallest useful vertical slice: one imported asset, one material swatch, one designed or camera-matched set, or one short movement. Read only the relevant modules below.

## Route work

| Task | Read |
|---|---|
| Whole production design, split skills, asset ownership | [architecture](references/architecture.md) |
| Research/tutorial claims, further study, evidence limits | [research](references/research.md), [sources](references/sources.md) |
| Search/import free materials, models, HDRIs or stock assets | [external asset intake](references/external-assets.md), [source catalog](references/asset-sources.md), [shortlist](assets/templates/asset-shortlist.md) |
| Import a generated model, repair identity/topology | [characters](references/characters.md) |
| Choose anatomy, locomotion and expressive range | [anatomy](references/anatomy.md) |
| Skeleton, skin weights, face controls, deformation | [rigging](references/rigging.md) |
| Felt, mane, feathers, PATINA, color and fiber stability | [materials](references/materials.md) |
| Choose strict matching versus a richer reference-inspired world | [environment direction](references/environment-art-direction.md), [direction template](assets/templates/environment-direction.json) |
| Audit texture usage before buying or applying maps | [material evidence](references/material-evidence.md), [material review](assets/templates/material-look-review.md) |
| Trees, rocks, rivers, terrain, buildings, 2.5D cards | [environments](references/environments.md) |
| Reproduce a specific location image in `plate_match` mode only | [environment image matching](references/environment_image_matching.md), [S05 feedback case](references/environment-fidelity-case-study.md) |
| Persistent props, contact, net, handoff, world events | [world state](references/world-state.md) |
| Performance, ambient motion, narration, shot joins | [animation](references/animation.md) |
| Reconstruct perspective, light and photographic appearance | [camera/light/color](references/camera-light-color.md) |
| Codex/ChatGPT/Blender/fal integration, safe paid calls | [tools](references/tools.md) |
| Local rendering, HPC feasibility, backups, optional Wan | [rendering](references/rendering.md) |
| Foresee failures; review the entire frame and sequence | [quality and risks](references/quality-and-risks.md) |
| Initial Leo/S05 and later bird/human pilots | [pilot plan](references/pilot-plan.md) |
| Delegate bounded specialist tasks | [agent team](agents/team.md) |
| Run helper scripts, understand schemas and test scope | [contracts](references/contracts.md), [validation](references/validation.md) |
| Install and invoke the skill | [installation](references/installation.md) |

## Non-negotiable rules

- Resolve authority by property: canonical for identity; the scoped design contract/published environment revision for geometry; camera for projection; story state for events; finalized audio for time. In `reference_inspired`, old scenery guides mood, craft and narrative identity, not every pixel or coordinate. Preserve old approved outputs and do not publish a new environment without owner review.
- Preserve source files and owner-selected images. Keep untouched imports and edit candidates separately. Do not reactivate superseded audit rejection lists. Owner selection and technical readiness are separate records.
- Keep a versioned anatomy profile. Never impose human, four-legged or two-eyed assumptions on every character. Validate semantic parts and their visibility, not just object counts.
- Derive physical ratios from neutral anatomical measurements, not object scale tuples, screen percentages or flattened lying silhouettes. A 2D depth parameter is not a 3D coordinate. Register exceptions explicitly.
- Use camera framing to improve readability rather than enlarging a small character. Register intentional stylized exaggerations, if authorized, as design decisions rather than hiding them in transforms.
- Keep permanent world geometry, camera setup, light state, prop state, ambient animation and character action separate. Reuse immutable asset revisions. A camera cut does not reset the world clock.
- Restrict 2.5D scenery to its reviewed camera envelope. Give contact surfaces, moving foreground objects and important occluders enough 3D volume for the action.
- Keep felt texture attached to the object. Use stable IDs/seeds, restrained fibers and shot-distance tests. Surface maps alone do not create fuzzy silhouettes or change a poor model into the canonical.
- Drive ambient systems from story time. Most landmarks remain fixed. Never animate everything merely to make the scene feel alive.
- Preserve the current mouth and teeth rules per character. Narrator audio never drives mouths. Avoid applying two independent lip-sync systems to the same performance.
- Check quoted price, exact inputs, destination, license and permission before paid calls or uploading private assets. Do not retry a pending job by submitting another generation.
- Do not infer asset rights from price or a provider name. Record exact license evidence, file hashes and render/modification/redistribution decisions; inspect packed dependencies. Do not mix unadapted stock styles or bulk-download catalogs.
- Keep Blender MCP local and scoped. Do not follow tutorial advice to disable approvals/sandboxing globally. A scene can contain code; inspect unknown assets with automatic script execution disabled.
- Use one writer for a `.blend` file. Specialist roles propose patches/reports against a fixed revision; a coordinator integrates sequentially. Roles do not become independent running agents merely because files exist.
- Keep blockout, calibrated layout, look-development and owner-accepted milestones separate. For reference-matched environments require the image-matching workflow, fixed comparison renders and explicit perceptual review; valid files and complete asset inventories are not fidelity evidence.
- Stop at an actual visual failure. Never fill review booleans from filenames, generated descriptions, tests or silence. Report unavailable evidence explicitly.

## Stage gates

| Gate | Required evidence | Stop condition |
|---|---|---|
| G0 Authority | Current sources, task scope, permissions, anatomy/world contract | Conflicting current canon or missing usable reference |
| G1 Shape | Neutral multi-angle stills, silhouette/parts, import audit | Wrong face, missing structural part, unreviewed hidden form |
| G2 Deformation | Anatomy-specific extreme poses and short motion tests | Collapsing joints, sliding contacts, broken face/groom |
| G3 Look | Matched neutral and story-light renders, stable color/fibers | Plastic/fur look, canonical drift, flicker |
| G4 Set | Mode-specific visual evidence: plate match OR design-brief quality; 3D/2.5D envelope, paths and interaction clearance | Missing mode/authority; weak craft look, broken design invariants, background pop or impossible support |
| G5 Sequence | Audio interval, state joins, props, motion and exposure continuity | Unexplained cut, reset, penetration, incorrect story event |
| G6 Release | Owner decision plus current technical evidence, portable dependencies | Stale hashes, missing assets, unsupported device, unreviewed output |

G1 and G4 may proceed in parallel on separate files. Require G2 before expensive hero grooming; G3 and G4 before a polished film test. Do not require film-ready approval just to produce clearly labeled, non-production diagnostic candidates.

## Execution loop

Inspect -> propose one bounded change -> save a new working revision -> execute -> obtain a real viewport or render -> compare with references -> run applicable technical checks -> record verdict. Limit repair cycles in the task brief. On repeated failure, change method or ask for targeted art/rigging help; do not loop forever or buy more generations automatically.

Use `scripts/asset_intake.py` for offline external-asset metadata/hash checks only; it is not legal clearance or a downloader. Use `scripts/preflight.py` for this package's metadata checks. It does not run the repository's production gates, inspect beauty, authorize spending, or implement a security boundary. Use `scripts/blender_inspect.py` and `scripts/blender_material_audit.py` for read-only inventories only after local runtime validation. Material node names, image existence and graph connectivity are not proof of visible felt or provider provenance. Validate an environment brief with `scripts/environment_direction.py`; it checks metadata, not beauty or real approval. Use `scripts/contact_sheet.py` to assemble existing images without generating new artwork. For reference-matched environments use `scripts/scene_match.py` plus `assets/templates/scene-match-review.md`; diagnostic pixel/landmark numbers never grant visual approval.

## Finish every task

Return: changed files and hashes; the before/after visual evidence; exact operations and commands; tests actually run; source/rights and spend receipts; current approvals; unresolved risks; next smallest action. Use `assets/templates/review-report.md`. If Blender or visual tools were unavailable, label the work documentation/preflight only. Do not claim the film, rig or material is validated.

Read [source register](references/sources.md) before refreshing volatile software/provider facts. Keep new empirical results in the repository, not solely in chat. Update the skill only after a lesson generalizes; do not turn a single-shot workaround into a universal rule.
