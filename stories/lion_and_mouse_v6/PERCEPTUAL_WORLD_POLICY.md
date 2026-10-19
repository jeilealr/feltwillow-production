# Lion and Mouse v6 perceptual-world policy

Agent A, 2026-10-16. Read the [generic rule](../../docs/perceptual-world-staging.md)
and [current audit](WORLD_SCALE_AUDIT.md). This policy governs future image
planning. The completed owner review supersedes earlier correction proposals.

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
  landscape. The current s05_p02 and s05_p03 selections demonstrate readable proximity to the
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
planning recommendations, except s12_p04, which the owner explicitly retained
as a tiny-Milo landscape exception during this completed review. The selected corrected s16 closing views are accepted; future wide views need
their own geographic purpose and readable companion rather than inheriting an exception.

s09_p02 has a **pre-existing owner-approved** `owner_scale_override` in
staging_plan.json. Resolve its active image through keyframe_plan.json.
Keep that exact scope. It is not permission to rescale Milo elsewhere.
Scene 12 owner close views magnify character and environment together.

## Generation and review workflow

1. Consult `perceptual_world_plan.json` and the current owner ledger. Select a mode,
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

## Current advisory metadata

`perceptual_world_plan.json` covers all 96 current selections, preserving the
world/subject/composition strategy and hash bindings. Owner-accepted corrected
or deliberately retained compositions supersede the original screening failures;
the original findings remain available in Git through the cleanup manifest.
Owner visual selection never substitutes for structured technical evidence.

`production/perceptual_world.py --story lion_and_mouse_v6` is read-only metadata
lint. It checks freshness and warns about provisional occupancy targets and
shared dialogue. It does not inspect pixels or generate images. Warning targets
are not automatic rejection thresholds and do not reopen completed selections.

Before any new generation, resolve current assets by frame ID and current hashes,
reconcile the selected camera with proposed staging, then pass the source-authority
gates. See the story README for retained source assets and a fresh review workflow.
