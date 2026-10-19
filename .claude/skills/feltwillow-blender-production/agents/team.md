# Specialist team and delegation protocol

These are **nine reusable role briefs**, not instantiated background agents, platform-specific agent configs or a claim of independent tests already performed. A capable host may delegate; otherwise one agent executes the roles sequentially and records that limitation.

## Shared protocol

The coordinator supplies a task ID, current source commit/hashes, writable paths, forbidden changes, operation/spend caps, required references, stage gate, expected evidence and stop conditions. Each specialist receives the same authority snapshot. Do not give every role the entire repository or unrelated credentials.

Only one writer may hold an asset/scene at a time. Use separate candidate files and isolated branches/worktrees when available. Avoid parallel saves to the same `.blend` and concurrent mutations of global preferences. Reports may run in parallel; integration and paid budget reservations require a single coordinator or real locking.

The independent reviewer reads the resulting exact revision, not a moving worktree. A builder cannot replace the owner decision with its own approval. Any changed dependency invalidates affected review bindings until rechecked.

## Assignment template

```text
Task: [ID and narrow objective]
Role: [brief path]
Inputs: [paths + hashes + current authority]
Allowed writes: [specific candidate files]
Forbidden: [canon changes / paid calls / deletes / unrelated state]
Budget: [explicit cap; zero by default]
Evidence: [actual views, motion, metrics, test commands]
Stop: [missing authority, repeated failure, permission boundary]
Return: [diff, outputs, hashes, observed vs untested, next action]
```

## Roles
- [Production coordinator](roles/01-production-coordinator.md)
- [Reference and design analyst](roles/02-reference-design.md)
- [Anatomy and rigging specialist](roles/03-anatomy-rig.md)
- [Felt material and look-development specialist](roles/04-material-lookdev.md)
- [Environment and world-building specialist](roles/05-environment-worldbuilder.md)
- [Animation and interaction specialist](roles/06-motion-interactions.md)
- [Camera, lighting and render specialist](roles/07-camera-render.md)
- [Independent continuity and quality reviewer](roles/08-independent-qa.md)
- [Provenance, budget and tool-safety steward](roles/09-provenance-budget.md)

## Escalation and handoff

An identity dispute goes to the owner with a paired comparison. A rig failure returns to anatomy/mesh preparation. A contact failure involves both world-builder and motion specialist. A style failure is separated into shape, material, light and color-transform tests. A memory failure returns to measured asset simplification. A missing license or unpaid authorization stops only the affected external operation, not safe independent research.

Retain one shared risk register; a role may add a risk but cannot silently waive another role's critical blocker. Review artistic and engineering progress separately so good model-building work is not discarded merely because a render backend is unavailable.

## External-library work routing (1.3.0)

Use the existing environment builder for shape/functional need, material specialist for felt adaptation, and provenance steward for source/license/access verification. The coordinator owns download and integration scope. Use one shared shortlist/registry, not independent conflicting libraries. Independent QA compares actual sample renders; source checking is not visual approval.
