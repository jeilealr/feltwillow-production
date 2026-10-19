# Feltwillow Blender Production - skill package

**Version 1.3.0 | Asset-library terms checked 2026-10-19; earlier production research retained**

Start with `SKILL.md`. This is one modular production skill with nine specialist role briefs, a source-backed knowledge library, pending-state templates and portable advisory checks. It supports character and environment work across future fables without treating all characters as humans or quadrupeds.

The package does not contain or install Blender, a Tripo model, PATINA output, credentials, proprietary training materials, running agents or a finished film. It does not modify the production repository. It is intended to guide an agent that has the appropriate local tools and approved source assets.

## Entry points

- [Install and first prompt](references/installation.md)
- [Research synthesis](references/research.md)
- [Source register](references/sources.md)
- [Architecture](references/architecture.md)
- [Specialist roles](agents/team.md)
- [Pilot plan](references/pilot-plan.md)
- [Validation and limitations](references/validation.md)

## First task

Audit the user's existing Tripo Leo and local Blender workspace, reconcile current repository authorities, then run a bounded Leo + S05 pilot. Do not generate a new Leo or apply historical cleanup instructions by default. Establish faithful shape, deformation, felt appearance, mode-appropriate set design and quiet motion before expanding.

## Tests

From this skill directory:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m compileall -q scripts tests
```

Python 3.10+ is needed; the optional contact-sheet test/helper uses Pillow. Production-helper, shared-installation, image-comparison and safe-update tests were executed in packaging. Exact counts and limits are in `references/validation.md`. Blender-dependent operations still require local validation. See the validation report for the distinction.

All included workflow prose, templates and helper code are newly authored for this task. Referenced third-party material, source art and paid-course assets are not included. Their licenses and terms remain separate. No font files are bundled.

## 1.0.1 installation update

Keep one source in `.claude/skills/feltwillow-blender-production/` with a relative
link from `.agents/skills/feltwillow-blender-production`. The safe installer
preserves local edits and rejects conflicting copies. No character, environment,
animation, material, approval, or source-authority rules were changed.

## 1.1.0 environment fidelity update

Use [environment image matching](references/environment_image_matching.md) whenever an environment needs to reproduce approved artwork. The workflow separates blockout from calibrated composition and visual fidelity, then prioritizes hero geometry, early lighting, terrain, vegetation layers, sky and felt surface detail. Use the scene-match review template and diagnostic overlays; no image statistic grants visual approval.

Use [safe repository updating](references/installation.md#upgrade-an-existing-shared-installation) for the already-installed single source. Downloaded updates do not edit your Mac automatically. The new updater checks the previous release hashes, preserves local-only work, refuses overlapping edits and backs up the source outside the repository. It does not change .blend assets, MCP configuration or Git history.

Read [changelog](CHANGELOG.md) for scope and retained requirements. The actual S05 Blender fidelity pass remains a separate local task.

## 1.2.0 environment art-direction update

Choose [environment direction](references/environment-art-direction.md) first. `plate_match` retains exact-image reconstruction; `reference_inspired` allows a richer interpretation under declared invariants; `original_design` starts from a new approved brief. None permits changing character identity or physical scale to improve a composition. Design freely inside the authorized candidate scope; freeze the reviewed environment revision for shots.

[Material evidence](references/material-evidence.md) distinguishes an API result, an image loaded in Blender, an upstream material connection, a rendered effect, and a visually successful felt surface. A packed height map alone is not a full environment look-development pass. The material audit helper does not generate textures or modify scenes.

Use the same single-source updater to migrate an unmodified 1.1.0 package. The new archive includes baseline hashes from that exact release; local conflicts stop before writes. This update does not edit a local repository automatically.

## 1.3.0 external-asset discovery and adaptation

Read [external asset intake](references/external-assets.md) and the dated [source catalog](references/asset-sources.md) before sourcing third-party material. Add a small shortlist, exact acquisition/license evidence, immutable raw and adapted assets, a render-versus-source-redistribution decision, and felt-style sample renders. The source leads are Kenney, Poly Haven, ambientCG, Quaternius and Blendkit; per-file checks remain mandatory.

Use `scripts/asset_intake.py` with the new record template for offline metadata/hash checks. It neither downloads anything nor authenticates licensing or authorizes production. Keep `reference_inspired` for the current S05 exploration, rather than reverting to exact plate matching. All existing anatomy, rigging, calm motion, continuity, spending and owner-review rules remain.

The updated release manifest supports safe migration from the distributed **1.2.0** package. Earlier packages need sequential updates or a local agent's reviewed merge. Do not force-overwrite overlapping local edits. This ZIP does not change a Mac or repository automatically.
