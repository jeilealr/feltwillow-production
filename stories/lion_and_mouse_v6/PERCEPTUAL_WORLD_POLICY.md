# Lion and Mouse v6 perceptual-world policy

Agent A, 2026-10-16. Read the [generic rule](../../docs/perceptual-world-staging.md)
and [current audit](WORLD_SCALE_AUDIT.md). This policy governs future image
planning and records recommendations for the selected story set.

## Three character worlds

- **Milo-world:** default for Milo alone, his dialogue and his emotional/action
  beats. Prefer detailed environmental mediums and registered upper-body
  portraits. Keep ears, eyes, gaze and paw action legible. Scenes 01–03 and
  s01x/s04x supply composition examples, not blanket identity/scale authorities.
- **Leo-world:** default for Leo alone and his emotional beats. Preserve the
  successful Leo solo framing, body, material and location scale. Existing
  Leo close-ups already provide useful face readability.
- **Shared-world / bridge-world:** default whenever both characters matter.
  Prioritize their interaction rather than fitting all of Leo and the entire
  landscape. s05_p02/r06 and s05_p03/r19 demonstrate readable proximity to the
  paw/face. Preserve physical ratios and grounded staging; do not enlarge Milo
  independently to imitate their composition in another setup.

Empty s03_p01 and s09_p04 are environment views. Offscreen listeners do not turn
speaker portraits into shared shots. Shared dialogue should use the existing
speaker close-ups (s07x, s08, s13, s15x, s16) for facial beats, with two-shots
reserved for interactions that actually need both actors. Timing remains a
separate task under the runtime contract.

## Detail floor and exceptions

Provisional warning targets for *full-body planning*, not measured acceptance:
Milo solo standing-equivalent height below **0.25** of the frame; shared Milo
below **0.18**. These values are starting points for a composition trial, not
universal standards. The selected early-scene wides show that strong contrast,
simple silhouette and adjacent detailed views can work below them. They require
inspection rather than automatic rejection. Portraits and action inserts use
face/action readability instead of a full-body threshold.

At the usual 0.25 same-depth cast ratio, a Milo height of 0.18 implies a Leo
standing-equivalent height around 0.72. A pose change or close crop may therefore
be necessary; demanding an entire standing lion and broad landscape can make
the brief impossible. Replan the camera/pose before requesting generation.

A wide exception records its geographic purpose and a named detailed companion.
Suggested existing companions: s01_p01/p03 → s01x_p01–03; s02_p01 → s02_p02–03;
s04_p01–04 → corresponding s04x; s12_p03–04 → s12_p02 and s12x. These are
Agent A planning recommendations, not retrospective owner approvals of an
exception. Repeated wide closing frames in s16 do not each gain an exception
just because they are wide; retain one geographic view and design a readable
shared closing composition for the relationship beat.

s09_p02 has a **pre-existing owner-approved** `owner_scale_override` in
staging_plan.json. Its source is historical r02 and its active image is r04.
Keep that exact scope. It is not permission to rescale Milo elsewhere.
Scene 12 owner close views magnify character and environment together.

## Generation and review workflow

1. Consult `perceptual_world_plan.json` and the hash-bound audit. Select a mode,
   subject and composition strategy. Read recommendations before writing a prompt.
2. Reconcile the proposed camera with staging, crop, depth, support, plate and
   same-setup anchor. Existing plan actions such as “keep him small within the
   wide landscape” cannot coexist with a new close-view brief. Change the source
   plan deliberately before building any new prompt; never patch historical
   candidate text into a runnable instruction.
3. Resolve required canonical, plate, prop and anchor approvals through
   [keyframe regeneration](../../docs/keyframe-regeneration.md). For a missing
   slot, reconstruct from live approved authorities and surviving reviewed
   continuity sources. Owner-deleted/rejected PNGs stay historical; do not
   recover them from Git as generation bases. Current inventory has no missing
   slots; missing-frame receipts describe earlier work.
4. Compose a candidate at the registered camera and record the exact prompt,
   ordered reference roles/hashes, crop, inputs, output and revision. Milo has
   no visible teeth, including gnawing. Preserve canonical compact anatomy,
   felt pigment and fiber scale; close-ups retain full ears/mane and upper chest.
   Trapped/released net state and connected knot topology remain authoritative.
5. Review native detail and the whole-frame 480×270 preview. Name expression,
   gaze, action, support and shared relationship evidence. Measure visible
   actor/head boxes if needed; planned height numbers are not observations.
6. Resolve readability defects, then use the existing revision/adoption and
   owner review workflow. Rebuild all scene sheets only if active PNGs change.
   Keep this advisory audit separate from keyframe_visual_reviews.json and
   owner_visual_acceptance.json. Run existing technical gates before export.

## Minimal metadata implementation and patch plan

Implemented a separate advisory `perceptual_world_plan.json` covering all 96
active frame IDs. It contains source path/hash and staging snapshot hashes,
`perceptual_world`, `subject_priority` (actor ID list), `composition_strategy`,
`detail_floor_actor`, `detail_floor_min_frame_height_fraction`, failure labels,
review scope, findings, remediation and priority. `observed_world` is an audit
observation; `perceptual_world` is desired planning intent. Neither grants
approval. No existing production JSON schema, crop or approval record changes.

`production/perceptual_world.py --story lion_and_mouse_v6` is an opt-in read-only
lint. It checks inventory and hash freshness and warns about planned occupancy
and shared dialogue. It neither examines pixels nor generates images. Warnings
exit zero; invalid or stale bindings exit nonzero. No production module imports
it. Other native stories can adopt the same actor-ID-based sidecar pattern.

Future small implementation steps, after reviewing the proposed compositions:

| File/function | Proposed change and prerequisite |
|---|---|
| `staging_plan.json` frames/views/setup_anchors | Register chosen new crops and correct depth/support targets; obtain matching anchor authority before dependent images |
| `production/keyframe_plan.py:build` | Read desired world clauses only after reconciling action/camera; emit them beside placement/identity locks; retain authority ordering |
| `production/keyframe_reference_gate.py` contract builder | Carry world metadata in proposed generation receipts, keeping physical geometry and approvals authoritative |
| `production/image_prompts.py` manifest workflow | For future manifest stories, derive the world clause from one setup/record field and lint coverage; v6 has no prompt manifest |
| `keyframe_visual_reviews.json` schema/gate | Consider optional hash-bound readability evidence after trial reviews; keep subjective checks human-reviewed before any hard gate |

This branch implements the audit, policy and optional lint first. Production
prompt builders and video-control code remain untouched. The generation skill
and regeneration guide now require consulting the policy, so new work encounters
it before a prompt is written. Reusable rules live centrally; Milo-specific
thresholds, examples and the s09 exception remain local to this story.
