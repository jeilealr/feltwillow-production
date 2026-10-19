# Environment image-match review

Status: unreviewed. Technical success is not visual acceptance.

## Scope and source bindings
- Story, scene, environment ID:
- Requested milestone: blockout / calibrated candidate / look candidate / scoped release
- Current repository branch and HEAD:
- Geometry authority: path, SHA-256, owner decision/scope:
- Appearance/lighting authority: path, SHA-256, role:
- Baseline render: path and SHA-256:
- Candidate render: path and SHA-256:
- Shot .blend plus ALL linked libraries: paths, SHA-256, missing items:
- Tool availability and actual file inspection performed:
- Allowed edits; protected assets; rollback; cost/time/render limits:

## Comparison conditions
- Exact width/height/pixel aspect, camera transform/lens/shift/focus:
- Renderer/build, device, samples, denoising, exposure, view transform/look:
- Frame/global time, lights/world, compositing, alpha/color encoding:
- 3D / 2.5D / matte representation and approved camera envelope:
- Inferred geometry or ambiguous perspective:
- Landmarks, normalized top-left coordinates and uncertainty:

## Perceptual review - no averaging away failures
| Dimension | Observation and evidence path | Status | Highest-value correction |
|---|---|---|---|
| Camera/framing/negative space | | unreviewed | |
| Hero tree/building/landmark silhouette | | unreviewed | |
| Interaction roots/steps/support | | unreviewed | |
| Terrain/path/rocks/water margins | | unreviewed | |
| Vegetation/prop hierarchy and density | | unreviewed | |
| Sky/background layers and distance | | unreviewed | |
| Light/value/color relationship | | unreviewed | |
| Handmade felt/material scale | | unreviewed | |
| Envelope parallax, occlusion and shadows | | unreviewed | |
| Motion/texture stability | | unreviewed | |

Use `needs_revision`, `candidate_for_owner_review`, `owner_accepted_for_scope`, or `blocked_missing_evidence`; record why not applicable rather than pretending a check passed.

## Pass log
For each pass: hypothesis; one bounded change; actual command/tool; old/new library hash; settings changed; unchanged comparison settings; full-frame, overlay and matched crop files; observed improvement; new regressions; next action.

## Technical checks - report separately
- Linked files/texture dependencies:
- Support and route clearance:
- Environment/character size calibration:
- Frozen dressing seed / story-clock phase:
- Read-only source and Leo hashes preserved:
- Metadata/tool tests actually executed:

## Final decision
- Largest remaining perceptual mismatch:
- Unresolved interaction or camera-envelope failure:
- Accepted scope and actual owner decision, if any:
- Why more of the same approach would or would not help:
- One next bounded action:
- Paid calls and actual receipts (none by default):
