---
name: consistent-image-prompts
description: Use before writing, editing or sending ANY image, keyframe, plate, expression or video prompt for a story in this repo (stories/<slug>/), before accepting a generated image, and when starting a new story's characters and locations. Keeps every character identical to its canonical (features, colours, brightness), every background identical to its locked plate, and every character size consistent with the story's size lineup and setup anchors, by building all prompts from one visual bible, linting them, and reviewing each result side by side.
---

# Consistent image prompts

**Perceptual-world gate:** Before choosing a crop or writing a scene prompt, name
whose experience must read: the solo/emotional actor's world or a shared bridge
world. Follow [`docs/perceptual-world-staging.md`](../../../docs/perceptual-world-staging.md)
and the story's `PERCEPTUAL_WORLD_POLICY.md` when present. Preserve anatomy,
plate geography, depth and setup anchors; improve small-subject readability
through registered framing, proximity staging or speaker portraits. Review
face/action detail at native size and in a whole-frame delivery preview. A
correct physical ratio alone does not pass narrative readability. Existing
owner selections remain separate from new advisory framing recommendations.

**Completed-review cleanup:** Keep active selected images, hash-bound owner decisions,
current plans and reusable references/layers outside disposable review folders.
Retain the current scene sheets for review tools; remove completed galleries,
alternates and one-off builders after selection. Record removed paths and hashes
with a recoverable Git commit. Historical receipt paths describe their original
run; they are not live generation authorities. Resolve the current selection by
frame ID, never a revision filename copied from an old example. Preserve scoped
exceptions without making them defaults. See the current story handoff before
recovering any archived bytes; owner-rejected images stay excluded.

**Spatial staging gate:** For every visible character, prompts and reviews must name its support surface, depth plane, landmark relation and expected scale; confirm valid contact and occlusion against the story bible. Follow [`docs/spatial-staging-consistency.md`](../../../docs/spatial-staging-consistency.md).

Consistency is the product. A child watching notices a mane that changed colour, a mouse that
grew between two cuts, or a tree that moved. Every rule below comes from such a defect
(`docs/creation-rules.md` CR-11 to CR-18 record the evidence; the reference is
`docs/image-prompts.md`).

**Owner standard, 2026-10-15 — upper-body close-ups and stable props:** For this
and future story work, a character close-up shows head, ears/full mane, shoulders
and upper chest only. Lower torso, tail and feet remain outside the image; a
full-body animal on a blurred background is not a close-up. The owner-selected
v6 example is the current `s15x_p03` selection in `keyframe_plan.json`. Use the same scene state and blur the
registered location. While Leo is trapped, the same connected net rests over
his crown/outer mane and shoulders, leaving eyes, nose and muzzle clear. Keep
knots, mesh connections, perimeter and ground anchors stable when poses change;
allow only deformation caused by the body and gravity. For subtle expression
beats, protect net pixels and edit only the clear face opening. Video endpoints
must not ask the renderer to interpolate two redesigned nets. Record any
necessary prop-state change as an explicit event before rendering.

**Expression-only portrait continuity:** When the beat changes only facial
expression, freeze the selected body's shape, posture, chest, shoulders, neck,
head orientation, ears, complete mane outline, crop and background. Use focused
edits inside the face opening; do not redraw the whole character per expression.
For v6 Scene 15, use the current `s15x_p03` body as the common portrait
reference for `s15x_p01` and `s15x_p05`; Milo stays left and Leo right
throughout the scene. Resolve current revision paths through `keyframe_plan.json`.

**Choose the story's pipeline before running commands.** Current Lion and Mouse
v6 uses its `visual_bible.json`, scene/staging/keyframe/boundary plans and
`keyframe_visual_reviews.json`; it has no `prompt_manifest.json`. For v6, use
`docs/keyframe-regeneration.md` and run `staging_contract.py`,
`keyframe_reference_gate.py`, `check_keyframe_review.py` and
`keyframe_visual_gate.py` before rendering. The regeneration gate checks the
approved plate/crop, each visible actor's canonical, owner-approved setup-size
anchor, input hashes, actor terminology, mouth policy, staging freshness and
recoverable historical provenance. `production/keyframe.py --story <slug>
--frame <id>` can compose a deterministic base from staging; its optional edit
mask marks the actor and contact-shadow area while protecting the plate outside
that region. Owner approvals are never inferred from a matching filename or a
passing metadata check. V6 audio is staged in its own namespace from the exact
unchanged v5 English recordings under the recorded owner-authorized hash
provenance; visual references and renders remain v6-local.

The manifest template and approval procedure below applies only to stories
that actually have `prompt_manifest.json` (v5 and Ugly Duckling, for example).
`chain_packet.py` was retired; do not rebuild v6 from another version.

**V6 owner cleanup:** If the owner deletes a generated keyframe because it is
visually unacceptable, that image is historical provenance only. Do not restore
it from Git or reuse it as an edit base. Rebuild the missing slot from the
approved plate/crop, canonicals, current size anchor, approved pose/expression/
prop authorities and surviving reviewed continuity references. Missing active
PNGs are expected to fail final inventory/contact-sheet checks until replacements
are adopted; do not bypass the gate.

For v6 speaking beats, prefer a registered close speaker view with a strongly
blurred version of the same approved location whenever physical interaction does
not require a two-shot. Boundary keyframes remain closed-mouth; open-mouth
material is later lip-sync calibration, not a replacement endpoint.

**One source of truth for manifest-backed stories.** For a story `stories/<slug>/`:

| File | Holds |
|---|---|
| `visual_bible.json` | `characters` (canonical `identity` text, `sheet`/`short` for video, `mouth` design, palette with hex, proportions, review checklist, drift phrases, canonical image and record), `cast_scale` (same-depth size lineup), `locations` (one locked plate each: description, landmarks, light), `setups` (camera, background treatment, measured character sizes and the size-anchor record per camera setup), `blocks` (shared text: style, light and colour, studio, edit rules, world-state rules), `reference_roles` (what each kind of attached image is for, in plain words) |
| `prompt_manifest.json` | one record per image: `prompt_kind`, `label`, `setup`/`framing` and `frame` for scene frames, `counts`, `ordered_references`, `prompt_template`; one entry per video shot with variant templates |
| `prompts/*.md` | readable copies, generated |

Prompts are **templates**. Shared facts enter only through placeholders:

| Placeholder | Becomes |
|---|---|
| `{{identity:<char>}}` | the full canonical description (image prompts, video full specification) |
| `{{short:<char>}}` | the one-sentence description (video runtime prompt) |
| `{{mouth:<char>}}` | the approved open-mouth design (open-mouth studies and `<shot>_open` talking key frames) |
| `{{setup:<id>}}` | camera, background (plate text, blurred for close-ups) and measured sizes |
| `{{plate:<loc>}}` | location description, fixed landmarks and light |
| `{{block:<name>}}` | shared text, e.g. `style`, `cast_scale`, `light_and_colour`, `net_world` |
| `{{refs}}` | every attached reference, numbered in attachment order, with its role and file name |
| `{{frame}}` / `{{frame:<record>}}` | what this frame shows (the record's `frame`), or another record's |

The record's own words describe only what is unique to that frame: pose, position, expression,
action, prop state. **Never write a character's colour or body feature in a record** (not in
the template, `frame` or `label`): that is a second description that competes with the
canonical. Lint rejects any sentence that pairs a colour word with a body-feature word outside
the bible's character text.

Tool: `production/image_prompts.py` (`lint`, `build`, `show`, `md`, `review`, `new-story`;
`--story <slug>`, default `lion_and_mouse_v5`).

## A. Starting a new story (before any scene image)

Fastest start: copy a story's `packet_source.py` (e.g. `stories/tortoise_and_hare_v1/packet_source.py`)
to `stories/<slug>/packet_source.py`, write the script lines, characters, places, camera setups and
shots there, and run `python3 production/story_packet.py stories/<slug>/packet_source.py`. It writes the
bible, every prompt record, the narration line list and SCRIPT/SHOT_PLAN/README; then build, lint, md.
Use it only until the first image is accepted; afterwards edit the bible and records directly. The
steps below say what each part must contain.

New stories get `"keyframe_chrono_naming": true` in the bible, so every scene keyframe **file** is
named `sNN_CC_<shot-name>_<start|end|open>_rNN.png` — `CC` is a two-digit counter that restarts at
01 each scene and counts shots in story order, so the stills sort chronologically on disk. Only the
file name carries it; the record `id` stays `<shot>_<which>`. `story_packet.py` emits these names
and `lint` enforces them when the flag is on (CR-20). Do not hand-name a scene keyframe target
without the `_CC_` segment while the flag is on.

1. `python3 production/image_prompts.py --story <template story> new-story <slug>` creates
   the bible skeleton and an empty manifest, copying the generic blocks, reference roles and
   lint settings.
2. **Characters.** For each character, approve one prop-free, neutral, full-body canonical on a
   plain studio backdrop, and add it as a manifest record (`canonical_record`). Write
   `characters.<id>` **from the image, never from memory or an older version**:
   - `identity`: 180–260 words, positively worded. Cover silhouette and proportions as ratios,
     head and crown, ears, eyes (iris colour, sclera, highlight, size relative to head), brows,
     nose shape and colour, muzzle, mouth, cheeks, whiskers on both sides, seams, torso, belly,
     limbs, paws and toes, tail root, length and tip, mane or hair, surface texture, feature
     counts. Name each colour once, with the hex sampled from the canonical, and use the same
     colour word everywhere. End with the brightness rule: intrinsic colours stay the same;
     only scene light tints them.
   - `sheet` (one predicate line) and `short` (`"<Name> is <sheet>..."`) for video prompts.
     They may only use colour words that also appear in `identity` (lint enforces this).
   - `mouth`: the open-mouth design (interior, tongue, which teeth may show), from the
     approved mouth study.
   - `palette`, `proportions`, `checklist` (12–20 checkable review items) and `drift_phrases`
     (observed or likely drift, e.g. "cool grey", "crimson"; lint rejects any prompt that
      contains one).
   - **Identity-set consistency gate:** before creating or accepting any expression, mouth,
     pose, portrait or other character reference, compare it side by side at full size with the
     approved canonical and the character's existing `expressions/` and `references/` images.
     Check head silhouette and proportions, eye size and spacing, eye patches, brows, muzzle or
     bill shape, material and stitching, intrinsic colours, saturation and brightness. The
     canonical is the identity authority; expression images may change only their named facial
     expression, and pose/view references may change only their named pose or view. A filename
     or manifest role does not prove a match. If any feature differs, stop using the mismatched
     image as a reference. Rebuild it as a focused edit of the approved canonical (or its
     approved parent); if the canonical itself needs revision, get owner approval and then
     rebuild the dependent expression and reference set from that approved revision. Do not
     generate scene keyframes for that character until this comparison passes.
3. **Size lineup** (`cast_scale` and `blocks.cast_scale`). Put all characters side by side at
   the same depth, or measure them against a shared reference. Record standing heights and head
   or mane widths as ratios between every pair. A pose change never rescales a head, mane or limb.
   For a new story, fill `staging_plan.json` before scene images: the `new-story` command creates
   its draft and `image_prompts.py lint` checks each scene image record against a frame with the
   same ID. Run `python3 production/staging_contract.py --story <slug>` to validate cast ratio,
   approved plate, walkable contact point, depth-derived size and camera view. On a fixed camera,
   interpolate size smoothly as the actor moves forward or backward; a camera crop is an explicit
   view change and does not alter anatomy. See CR-29 in `docs/creation-rules.md`.
4. **Locations.** One approved empty plate per place, camera and light, each its own record.
   Record `description`, at least three `landmarks` with frame positions, `light` (direction,
   time of day, colour temperature) and `plate`. A new light state reuses the same geometry.
   For a new location/camera, the first plate is the seed and is the only plate generated with no
   location-image reference, because no approved master exists yet. After owner approval, register
   its record ID as `composition_master_record` in the location entry; its manifest target path is the composition master. Every same-location/camera variant must attach
   that master as `edit_base` in `ordered_references`, even when only time of day changes; always
   derive variants directly from the master, not from one another. If the master is omitted, stop
   and repair the record—text describing a plate is not an image reference. No reference means a
   fresh scene, never an implicit link to an earlier image. Compare the result beside the master
   and check its landmarks. If season or camera changes intentionally alter geometry, register a
   distinct profile and state the allowed changes.
5. **Setups.** Every camera setup (location + framing) gets `camera`, `background_treatment`
   for close-ups, `size` (measured frame fractions per character at its depth plane, plus a
   comparison sentence such as "Milo's whole body is about as tall as Leo's mane is wide") and
   `anchor_record`, the approved frame the numbers were measured on. Use the four framings of
   CR-15: `dialogue_close_up`, `close_two_shot`, `scene_wide`, `empty_plate`.
   - Every scene image with visible characters against a sharp or recognizable environment must
     attach that setup's approved `anchor_record` with role `size_anchor`, on **both start and end
     frames**. The anchor must use the same camera/setup and show every visible character whose scale
     it locks. A self-reference, different setup, blurred portrait, or frame already known to have a
     scale defect is invalid. If no valid anchor exists, stop and create/review one before dependent
     frames.
   - Keep the anchor in the actual attachment list after applying the generator's image-reference
     limit. Drop optional staging/pose references first; never silently drop the anchor. For end-frame
     edits, retain the edit base first and include the same setup anchor as another reference.
   - Before staging a result, measure each visible character's bounding box on the review grid and
     compare it with the setup's frame-fraction target and approved anchor. Reject any material scale
     or Leo:Milo ratio mismatch. Record the measured fractions and comparison in the review note;
     prompt numbers alone do not pass this gate.
6. Make the expression set before close-ups: one studio head study per needed emotion, each an
   edit of the approved closed-mouth portrait (only brows, eyelids, gaze and mouth change). Approve
   the single open-mouth study `*_OPEN` per speaking character too (`characters.<id>.mouth`): it is
   the one speech-mouth shape every talking clip reuses (CR-19).

## B. Writing or changing a prompt

1. Edit the bible (shared text) or the record (`prompt_template`, `frame`, `label`,
   `ordered_references`), never the rendered `positive_prompt`.
2. A scene template contains, in this order: the frame line (canvas, start/end of which shot,
   the setup's label); `{{refs}}`; for an end frame `{{block:edit_end_frame}}`; the cast line
   with exact counts; one `{{identity:...}}` per visible character; `{{block:cast_scale}}`
   when two or more characters share the frame; exactly one `{{setup:...}}`;
   `{{block:light_and_colour}}`; the world-state blocks of the props in this place and one
   sentence for the current prop state; `This frame shows: {{frame}}.`; `{{block:style}}`;
   `{{block:final_check}}`.
3. `frame` says only the pose, position (x/y fractions of the frame), facing, expression
   (named by brows, eyelids, gaze and mouth), contacts and prop state.
4. **References.** `ordered_references` is the exact list a generator attaches, in this order:
   the edit base or the previous accepted frame first, then the locked plate, the canonical of
   **every** visible character (and never of an absent one), pose, expression, mouth and prop
   references, the setup's size anchor, framing and staging references. Each has a `role` from
   `reference_roles`; `{{refs}}` writes the list into the prompt in plain words, so the prompt
   itself says which image is which and what to take from it. An older version's image may only
   be `staging_only`, `expression` or `camera_geometry`. An end frame's first reference is its
   start frame (role `edit_base`).
5. Positive wording only: fast video mode has no negative pass, and image models follow positive
   specifics better. Exclusions live in `negative_prompt` as review criteria.
6. Sizes are numbers plus a comparison and come from the setup; never estimate them per record.
   Lint requires the setup anchor on every eligible scene frame; size text without an attached
   anchor is incomplete.
7. `python3 production/image_prompts.py build && python3 production/image_prompts.py lint`
   must end with **0 errors**. Then `md` refreshes `prompts/*.md`; `show <record>` prints one.
8. **Dialogue close-ups need a separate open-mouth calibration image (CR-19).** Every
   `mouth` variant starts and ends on approved closed-mouth scene frames. Create a scene record
   `<shot>_open` as an edit of one closed boundary frame (`{{block:edit_open_mouth}}`, first
   reference `edit_base`) that opens only the mouth to the character's approved speech shape.
   Attach the closed frame, locked plate, canonical (`identity_root`) and the character's
   `*_OPEN` study (`mouth_design`), with `{{mouth:<char>}}`. Mark its `mouth_character` and set
   `mouth_open_image` on the `mouth` variant. Assign exactly one audio `speaker` matching the
   visible character's `voice_speaker` in the bible. Narrator-only close-ups get no mouth
   variant. `story_packet.py` emits this structure for new stories; keep it when editing by
   hand (Lion and Mouse v4 is exempt — its clips are nearly final).

## C. Generating

- The owner remains the default image maker. When the owner asks the agent to create an image,
  use the built-in OpenAI `image_gen` tool by default. Gemini is an optional provider; use
  `character/gemini_image.py` only when the owner chooses Gemini and API access is configured.
- Send the rendered `positive_prompt` and only its `ordered_references`, in order. Do not add
  unstated character, scene or reference details. If an image needs a correction, record the
  correction as a separate edit prompt with its parent image and tool in the manifest result;
  do not leave generation or edit prompts undocumented. Changes to the intended image prompt
  itself go into the bible or record template first, then `build` and `lint`.
- Built-in `image_gen` saves generated files under `$CODEX_HOME/generated_images/`; copy the
  selected output as one candidate in the record's `.review/` folder. Copy it to the manifest
  `target` only after visual review passes; `approve` checks that target and reviewed candidate
  have the same SHA-256. Preserve a materially different raw source only when needed for review.
  Record the tool, model/version when exposed, exact prompt(s), ordered reference paths and hashes,
  output hash, normalization and review note. Never leave a project-referenced image only in
  the generated-images cache.
- Keep one review PNG per record: the latest candidate. Do not leave a visually redundant
  `_source.png` beside its `_candidate.png`; record source path/hash and edit history in the
  Markdown sidecar. Retain a separate source image only when it materially differs and is needed
  for review, or when the owner asks for side-by-side comparison.
- `character/gemini_image.py gen --story <slug>` is the optional API workflow; it refuses to run
  while lint has errors. Gemini candidates and accepts stay within the selected story's target
  folders and manifest.
- Never pass a rejected or unreviewed image as a reference.
- Before generating a scene image, run `python3 production/image_handoff.py --story <slug> check <record>`.
  The command verifies approved reference files, their hashes, the locked plate, and the setup's
  approved size anchor. Generate the setup's anchor first; dependent frames wait for its approval.
  If the first scene frames show only one character and the planned anchor shows both, list those
  earlier frames under `setups.<id>.bootstrap_records`. They use numeric size targets and visual
  review without the future anchor; after approval, create the shared-cast anchor. Never attach
  a future or self-referential scene frame as a size reference. Lint rejects reference cycles.
- One change per edit. To change an expression or a pose, edit the approved same-setup frame;
  do not regenerate the character.
- If the tool cannot keep the plate, use a focused edit or a reviewed isolated layer on the
  locked plate (CR-17); never accept a moved background.

## D. Review gate (every image, before it becomes a reference)

`python3 production/image_prompts.py review <record> --image <candidate>` writes
`work/review/<record>.jpg`: the canonicals, expression references, setup size anchor, plate and
previous shot's end above, the candidate with a 0.1 grid below. Check at full size and at
delivery size:

1. **Identity:** every item of `characters.<id>.checklist` against the canonical (nose and muzzle
   shape, eye size and colour, brows, whiskers on both sides, ears or mane, seams, limb and tail
   counts, colour temperature and brightness).
2. **Size:** read the character boxes on the grid against the setup's `size` numbers and the
   anchor. Same depth and camera mean the same anatomical size: a jump without a depth move or
   recorded camera change fails. Compare one nearby landmark on the same ground plane; a crop
   enlarges the landmark and character together. Sitting/lying changes pose height, not head,
   mane, ear, torso or paw size. A shared frame keeps the lineup ratio. A number in a prompt or
   staging file does not certify the rendered pixels; follow the measured-image gate in
   `docs/spatial-staging-consistency.md` Rules 9–10.
   For individual keyframes, fill the story's `video_boundary_config.json` with
   chronological order and cut/shared-boundary decisions; run
   `production/video_boundary_plan.py --story <slug>`. `new-story` scaffolds this
   config and an empty `keyframe_visual_reviews.json`. Keep the review empty until
   actual full-resolution, hash-bound visual inspection passes; runtime export
   blocks unreviewed candidate keyframes.
3. **Background:** the landmarks sit where the plate has them, with the same light and crop.
   For close-ups, the plate is blurred but not replaced.
4. **Pair:** the end frame equals the start except for the stated change.
5. **World state and counts:** props, damage, contacts; exactly the counted characters; two
   eyes and two brows each; one tail each; no text.
6. **Ground contact and support:** identify the actual walkable surface in the locked plate before
   placing a character. Every planted foot must meet that surface at the correct depth and baseline;
   use a shadow and occlusion that agree with the plate. Do not place feet on water, flower heads,
   bushes, or other decorative foliage unless the action explicitly shows climbing or perching on a
   stable surface. For sitting, lying, climbing, jumping, or touching a prop, verify the stated body
   or paw contact is physically supported. Reject floating, sinking, or vegetation-top placement.

**Scale gate:** for sharp-background scene frames, measure every visible character's full silhouette
on the grid and compare it with the setup's size fractions and attached same-setup anchor. Shared
frames must preserve the measured Leo:Milo ratio. A mismatch fails review and must be corrected
before staging or use as a reference.

**Ground-contact gate:** before staging a scene image, compare each visible foot/paw contact with the
locked plate and the frame's walkable-surface map. The support surface must be plausible and
continuous at that depth. Verify contact shadows and occlusion; reject a character standing on water,
the top of a bush or flower, or any surface not explicitly established as walkable. Record the
surface and normalized contact point in the review note.

For a sharp scene frame, save the measurements in `result.review_checks` before approval:
`identity_match`, `plate_match`, `pair_match` as true after visual inspection;
`measured_size.<character>` with the applicable `height`, `head`, `mane` or `face` frame fractions
from `setups.<id>.numeric_size_targets`; and `ground_contact.<character>` with a named `surface`
and normalized `x`,`y` support point. `image_handoff.py check <record> --for-approval` checks
these fields and the candidate/target hash; `image_prompts.py approve` enforces the same gate.
Numbers and a passed script check do not replace visual review of anatomy, occlusion and support.

Record the result in the manifest (tool, model, the references actually sent with their
hashes, the prompt actually sent, output hash, review note), and if an identity, plate, size or prop state changed
upstream, mark dependent frames stale and redo them in story order. For chained stories, only after the review
passes and the exact candidate has been copied to its manifest `target`, record the human approval:

```bash
python3 production/image_prompts.py --story <slug> approve <record> --reviewed-by <name> --note "<review note>"
```

This writes `stories/<slug>/image_approvals.json` with the target path, image SHA-256, rendered prompt/specification SHA-256,
and SHA-256 values for every ordered reference. Runtime export checks all of them;
changing or replacing the approved file requires review and a new approval.

## E. Pitfalls already paid for

- A second description of a character in a record (e.g. "his rust mane" in shot text) made
  frames disagree. Lint's identity-conflict check now blocks it.
- Correction texts appended at generation time (revision files, `--extra`) made the sent prompt
  differ from the recorded one and attached references the prompt never mentioned.
- Older-version references leaked their identity (red, short V3 mane; tufted V3 Milo).
- A canonical attached for a character who is not in the frame drew that character in.
- End frames re-enlarged a character that the start had fixed; compare each end with its start.
- Expressions drift to a smile unless brows, eyes and mouth are named.
- Canonical and expression/reference images for Ollie the swan disagreed in head and face design;
  that identity drift carried into close-ups and scene frames. Audit each character's complete
  canonical, expression and reference set against the approved canonical before building
  keyframes; stop and reconcile mismatched assets first.
- A wide start with a close-up end becomes a zoom in video; keep one framing per shot.
- Numeric size instructions without a valid same-setup reference did not hold character scale: some
  anchors were self-referential, oversized, or showed only one character, and no post-generation
  measurement blocked the result. Require the approved size anchor on every sharp-background start
  and end frame, preserve it under attachment limits, and measure generated silhouettes before
  staging. A missing anchor or failed measurement is a hard stop.
- An end frame's start image does not replace its locked location plate. Keep the start first
  as `edit_base`, then attach the same locked plate as `locked_plate` on every frame, including
  end frames. The pond sequence drifted when end records referenced only their composite start;
  the model redrew the nest and water while changing character poses. If a generated frame still
  changes plate geometry, do not accept it as fixed: composite reviewed isolated character layers
  over the plate and compare the result against the fixed landmarks.
- A talking clip with no separate approved open-mouth calibration image has no stable speech
  shape. Give the `mouth` variant a `mouth_open_image` edited from a closed endpoint and the one
  approved `*_OPEN` study (CR-19), with the locked plate attached after the edit base. Keep the
  clip boundaries closed so the mouth stays still during narration and silent pauses.

## F. Chained stories (CR-21)

A story with narration-driven coverage uses the repo skill
`audio-chained-coverage`. The following detailed `edit_chain_frame` and manifest
rules describe the historical prompt-manifest implementation; current v6 uses
its keyframe/boundary plans and visual-review ledger instead. In a compatible
manifest-backed chained packet:

- One image is the end of one clip and the start of the next. Review a **boundary image** against both
  pieces that use it (the earlier piece's start, the later piece's end): one small action must reach it
  from each side.
- A new chain frame is an edit of the frame before it in the chain (`edit_base`, block
  `edit_chain_frame`), with the locked plate attached next; mouth calibration images follow B.8
  and are never chain boundaries.
- Landscape pieces use the approved plate itself (`PL_<loc>`) as start and end. When a prop must be in
  the empty view, make an empty scene frame with the prop's frame attached as `empty_copy`.
- New keyframe files are `sNN_KK_<name>_rNN.png` with `KK` = first use in the scene; lint checks it.


**Owner rule — Milo teeth (2026-10-15):** Milo has no visible teeth in any future artwork, including smiles, speech and gnawing. Mouth-to-knot contact uses soft felt lips and a small mouth crease. Never add exposed incisors, white tooth shapes or fangs. This explicit owner rule overrides tooth shapes in historical candidates.
