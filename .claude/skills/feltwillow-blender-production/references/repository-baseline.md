# Repository baseline and precedence

**Inspected remote snapshot:** `jeilealr/feltwillow-production`, `working-cloud-branch`, commit `6fae81c78ef3143057bc0324103f2cb05c5dce0a`, committed 2026-10-16. Research date: 2026-10-18. This is a snapshot, not a permanently current specification.

The inspected remote root did not contain `blender/`. The user's Blender/MCP/Tripo work may exist locally or on another branch; inspect it before creating or replacing anything. No current `.blend`, rig, Tripo GLB or live Blender session was available for runtime testing in this research pass.

## Current decisions that supersede old chat

The current story README records all 96 v6 story images as owner-selected: 12 final corrections explicitly accepted, 84 retained by the owner's final correction list. `owner_visual_acceptance.json` binds these decisions to current images. Technical checks remain incomplete and are separate from visual selection. Do not treat old pending compatibility statuses or October 13-15 audits as a new mandate to delete or regenerate accepted images. [R01](sources.md#r01), [R02](sources.md#r02)

Milo now uses `Milo/canonical/full-body_milo_neutral_pose_r02_candidate.png` and `Milo/references/m_complete_reference_r03_candidate.png` under `character/characters/lion_and_mouse_v6/`. The r02 neutral master recorded in the inspected bible has SHA-256 `7773f2dc4e48aad5623f4bcf51709bfdcad1298796e398758bed04243bfac070`. Verify bytes locally. Milo has no visible teeth, including speech and gnawing; work on the main net knot using the approved mouth crease. Leo's canonical/expression authority remains approved while his combined atlas has a separate status. The net design is approved; acorn and some calibration dependencies remain pending. [R01](sources.md#r01), [R03](sources.md#r03)

The current cast target is 0.25 for Milo's neutral upright ear-tip-to-foot height divided by Leo's neutral quadrupedal mane-top-to-supporting-front-paw height, with a recorded review range 0.22-0.28. This belongs to this cast, not to future stories. Read the current bible, staging exceptions and measured evidence; do not impose it on a bird, human or different fable. [R04](sources.md#r04)

The story preserves an explicit S09 p02 world-scale/perspective exception. S12 closer shots magnify actor and environment together. Owner exceptions must remain explicit when translating the 2D production to 3D; do not erase them to make a simplistic metric pass. [R01](sources.md#r01)

## S05 pilot

S05 belongs to the Great Tree dusk location. Use the current plate and selected camera references, not an invented forest. The preserved `interactions/keyframes/.review/history/s05_p01_r01_candidate.png` is a brightness/felt style reference; the active opening is r03 in this snapshot. That historical style file is intentionally useful, not rubbish to delete. Start with Leo lying/resting as the story requires, then the paw/nose encounter. A standing or walking rig test is a separate diagnostic, not automatically the new S05 action. [R01](sources.md#r01), [R04](sources.md#r04)

Current close-up direction is head, full ears/mane, shoulders and upper chest, excluding lower body/tail/feet. A full-body character against blurred scenery is not a portrait. The accepted expression-body example `s15x_p03_r03_candidate.png` keeps the same torso/crop across expression-only changes. [R05](sources.md#r05)

## Audio and pipeline

Current v6 is `keyframe_boundary_v1`, not a legacy prompt-manifest story. Do not manufacture `prompt_manifest.json`, `story.yaml` or a legacy timing plan. Reuse only the explicitly authorized unchanged English line audio: 161 lines, 16 scene tracks, about 683.67 seconds, with manifest hashes. Missing ignored audio cannot be recovered by `git clone` alone. No v6 video takes or assembled edit existed in the inspected handoff. [R01](sources.md#r01)

The remote handoff reports 86 current authority dependencies and 81 historical provenance warnings, not 86 visually bad images. These numbers are historical observations for this snapshot; rerun applicable current checks locally rather than hardcoding them into assertions. The repository skills contain older statements in places; property-specific current owner decisions take precedence while technical gates remain intact.

## Read before every implementation

Inspect `AGENTS.md` if present, `CLAUDE.md`, story README, visual bible, staging, current keyframe/pose/boundary plans, owner-selection and technical-review ledgers, and relevant existing skills. Read any local Blender docs and manifests. Preserve the distinction between a 2D authority and a new 3D candidate. Do not claim a selected 2D canonical approves an inferred backside, mesh topology, animation rig or newly generated texture.

This skill writes no production JSON automatically. Any future adapter from these plans to Blender must be explicitly designed, tested and reviewed in the repository.
