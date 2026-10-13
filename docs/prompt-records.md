# Prompt records and reproducible handoffs

Historical v4 record contract (written 2026-09-30; status updated 2026-10-02).
The v4 files and some named tools below were removed; use this as provenance,
not as current v6 instructions. Current v6 uses the story-local keyframe and
boundary plans described in [its README](../stories/lion_and_mouse_v6/README.md). Read
[creation-rules.md](creation-rules.md) first. The rendering tools (`shot.py`,
`keyframe.py`, `compose_keyframes.py`, `animatic.py`) do not read or enforce
this schema. `production/image_prompts.py` (templates, lint) and
`production/timing_sheet.py` read the manifest. Image providers are separate:
the built-in OpenAI `image_gen` tool is the default for agent-created images;
`character/gemini_image.py` is an optional Gemini path selected by the owner.
Record the actual tool, prompt(s), references, output path and hash for either.

## Where the exact prompt lives

For v3, `stories/lion_and_mouse_v3/TODO_images.md` has short per-image prompts
and shared style blocks. It is a request list, not a complete record of every
actual generation/edit. Some historical tool prompts are only in conversation
history. Do not label reconstructed text as the actual submitted prompt.

For v4:

- `stories/lion_and_mouse_v4/visual_bible.json`: versioned identity, style,
  geometry, location/motion profiles and prop-state definitions.
- `stories/lion_and_mouse_v4/prompt_manifest.json`: authoritative records
  for individual image and video prompts, including fully expanded text. Since
  generation began (2026-09-30 to 2026-10-02) each image record's `result` also
  holds the accepted output: path, hash, tool, model, ordered references,
  submitted prompt where recorded, review; rejected tries are under
  `result.attempts` and earlier results under the record's `superseded`
  (in-place repairs used `result.superseded` or `result.superseded_results`).
- `stories/lion_and_mouse_v4/prompts/*.md`: readable snapshots of those records,
  grouped by scene and foundation assets. Edit the manifest first and keep
  snapshots consistent; neither is an executed-generation log.
- Execution log, as actually kept: the manifest fields above;
  `stories/lion_and_mouse_v4/GENERATION_PROGRESS.md` (dated log of accepted
  and rejected takes); `revisions/<rev>.json` (the fix texts of the Gemini
  passes r02 to r05); `revisions/gemini_ledger.csv` (every Gemini call) and
  the `.json` sidecar of each Gemini candidate. The `generation_log.jsonl`
  planned here on 2026-09-30 was never created; do not start a parallel log.
- Future `stories/lion_and_mouse_v4/selections.json`: the owner's actual clip
  choices, trims, order and assembly instruction. No default seed counts as a
  selection. No selection has been recorded for v4 (no clip exists yet).

Video records separate `full_prompt_specification` (the exhaustive planning
contract) from `positive_prompt` (the complete, compact runtime candidate).
`runtime_export_candidate` stores action, frozen compact character names/sheets,
background, style and negative separately, so the current renderer's assembly
can be matched exactly. Do not append the long specification to the runtime
candidate or paste the entire candidate into `action` and duplicate its sheets.
The compact identity strings are frozen in the same bible; they are not freely
rewritten per shot. Image prompts remain fully expanded individual instructions.

Before rendering, count actual tokens using the deployed tokenizer and inspect
the effective text-encoder limit/truncation behaviour. The local wrapper does
not set `max_sequence_length`; neither a word count nor an assumed library
default proves the text will fit. If over budget, revise and record the candidate
while preserving action, identity, endpoint/prop state and camera priority.
Never silently truncate or discard critical state constraints. Token counts and
encoder limit remain null until checked on the actual runtime.

**Fast-mode caveat:** `feltwillow/wan.py` configures Lightning guidance 1.0/1.0 and
explicitly documents no negative CFG pass. Negative text is still saved, but
must not be treated as an active fast-mode control. Put the required state in
the positive and approved images (one mouse, closed lips, empty branch, fixed
trunks), then inspect the result. Do not raise Lightning guidance speculatively
to activate negatives; any standard-mode comparison is a separate planned job.

Version the bible and the manifest together. Each manifest prompt is an expanded
snapshot of the named bible revision. An identity change invalidates all affected
snapshots; update both source records and readable views before generation.
Never quietly edit shared identity words in one individual record.

## Required image record

| Field | Required content |
|---|---|
| ID/revision/status | unique image ID, prompt revision, explicit draft/approval state |
| Purpose | exact story beat, role (canonical/view/plate/prop/endpoint), consuming shot IDs |
| Target | repository-relative v4 path, expected dimensions/aspect, future candidate path |
| Bible | exact revision used to expand the prompt |
| References | ordered IDs, explicit paths, identity/geometry/pose/material role for each |
| Counts | number of each character/prop; anatomical counts and known occlusions |
| Geometry | camera profile, framing, depth, position, standing-scale calibration and foot contacts |
| Scale anchor | approved same-setup image and hash; normalized head/mane and whole-body boxes, ground baseline and depth plane for every actor; same-depth cast ratio; planned start/end depth change |
| Identity checklist | fully expanded canonical features for every visible character, including nose/muzzle, eyes, ears/mane, torso, limb and tail counts, seams, colours and exclusions, even if repeated in adjacent records |
| Plate lock | approved plate and hash; crop, light, ground plane and at least three protected landmarks |
| State | expression, mouth/eyes, prop state, contact and occlusion order |
| Pair/parent | source image ID and hash; paired shot; approved edit base |
| Edit scope | allowed regions/features; protected character and background regions |
| Positive prompt | full text, already expanded; no implicit references to chat history |
| Exclusions | separate undesirable outcomes, reviewed for contradiction with desired state |
| Acceptance | observable pass/fail checks, including semantic filename match |
| Result | exact submitted text, reference/output hashes, engine/settings, returned path, selected path, reviewer/date |

`result` is null until execution. Future reference paths and planned coordinates
are not evidence of approval. Missing sources, null measurements and unapproved
canonicals prevent execution. Seed is null/unknown if the image tool exposes none.
Keep reference labels distinct: an interaction scene is not a neutral identity
reference; a scene with Leo in it is not an empty plate onto which another Leo
can safely be pasted.

## What an exhaustive image prompt says

1. Output type and canvas, then reference roles and the intended scene.
2. Exact count and full frozen identity of each visible character.
3. Camera, ground plane, framing, screen position/facing and relative size.
   Give the approved size anchor, numeric frame fractions and each character's
   depth plane; for a multi-character shot state their same-depth ratio.
4. Body pose, expression, eyes, mouth, limb contacts, tail location/occlusion.
5. Prop count, material, holder, position, attachments, damage and layer order.
6. Lighting, depth of field and the exact protected background.
7. The sole intended change from the parent frame, with every invariant explicit.
8. Style/material requirements and exclusions appropriate to this state.

Put strong constraints in the actual tool prompt, not only the record's metadata.
If the tool has no negative field, append a labelled constraints section. For
Wan, keep desired motion in the positive prompt and assemble explicit negative
text separately. Avoid contradictory positives/negatives; more words do not
resolve an image that contradicts its prompt.

## Required video record

In addition to image-record provenance:

- Stable shot name, scene/beat, draft editorial order and previous/next handoff.
- Start/end image IDs, paths, hashes, approval states and shared camera profile.
- Exact prompt, exact negative, cast, story style and location/background text.
- One main action; normalised timeline: initial hold, event/contact, settle.
  Times are targets to review, not timing guarantees from the model.
- Actor path, gait and depth, camera mode, ambient-motion profile.
- Prop state before/after; persistent world state through cuts/occlusions.
- `closed`, `mouth`, `functional` or `ambient` mode. Record which closed reaction
  provides backup for a functional mouth action.
- For speech coverage: speaker, quiet lead/tail, opening limit, planned movement
  interval and eventual observed usable interval. Exact speech line/duration is
  pending the approved script; do not claim generated lip-sync.
- Intended duration/frame count/fps, model revision and all exposed settings;
  candidate seeds and revisioned output paths; actual tool command when run.
- Whole-clip and boundary review; result, rejection reason, owner choice, trim.

The current Wan path is 81 frames at 16 fps (~5.06 s), usually fast mode with
three seeds per mode. Use a small pilot first. Alternate mouth modes are distinct
shot names (for example `s07_leo_annoyed_closed_r01` and
`s07_leo_annoyed_mouth_r01`), not seed 1 versus seed 2 of one prompt. Mode changes
must update endpoints and effective negatives as well as action text.

## Pair and adjacent-shot record

The manifest `continuity_sources` names the latest world-state endpoint and,
where needed, an older wide image used only for camera geometry. The latest
endpoint controls cumulative rope damage; an older intact wide reference must
never restore a broken strand. Ordered reference roles make this priority explicit.

Record both image hashes, a comparison/overlay path, the stable landmarks and
character measurements, and the exact permitted delta. Then record the intended
cut type: continuous action, deliberate close-up cut, time ellipsis or location
change. Adjacent shots carry character facing, depth, pose/contact, props, net
state, light and ambient direction. An ellipsis never repairs broken rope or
teleports a character without an explicit new state.

The closed speech default changes expression only. For a mouth alternative the
open-mouth reference is an auxiliary design reference; current Wan only consumes
first and last images. It has no automatic middle-mouth-reference input. Use the
reference to author matching endpoints and judge intermediates; if mouth form
drifts, reject that alternative and retain the closed coverage.

## Runtime export contract (future step)

After the owner approves the script order and references, derive a v4
`story.yaml` and shot commands from approved records. Do not copy v3 recipes
wholesale. Map supported fields only: `name`, `characters`, `frames`, `seeds`,
`action`, `negative_extra`, `keyframe`, `end_keyframe`, `compose`, `end_compose`,
`background` and `size`. Keep the complete review/state record in the manifest.

`shot.py` builds ACTION + character sheets + background/location + style. Read
its assembled prompt to ensure it matches the reviewed runtime candidate.
Use `runtime_export_candidate` fields and the frozen runtime identity/style
from the bible; retain the full specification as the acceptance contract. Global
negative text must be universally valid; per-shot `negative_extra` can only add
terms, not remove global ones. Teeth/mouth exceptions therefore cannot be fixed
by merely adding a positive sentence at shot level.

`--dry-run` checks some paths and prints the assembled prompt (the 2026-09-30
version printed only the positive, so check whether yours shows the combined
negative). It does not inspect image content/identity, net state, mode
variants, stale caches or owner selection. Review those independently.
For a current manifest-backed packet, pass its existing story slug explicitly;
v4 was removed and is not a runnable default. Do not run draft manifests as story YAML.

## Execution ledger example (template, not an actual result)

The fields below are what an attempt must record. In practice v4 keeps them in
the manifest record's `result` (and `attempts`), not in a separate file.

```json
{
  "record_kind": "image_attempt",
  "asset_id": "s02_notice_end",
  "prompt_revision": "r01",
  "bible_revision": "v4-draft-2026-09-30",
  "submitted_positive": "REPLACE_WITH_EXACT_SUBMITTED_TEXT",
  "submitted_constraints": "REPLACE_WITH_EXACT_SUBMITTED_TEXT",
  "ordered_references": [{"path": "PATH", "role": "edit_base", "sha256": null}],
  "engine": null,
  "seed": null,
  "output_path": null,
  "output_sha256": null,
  "review": {"status": "not_run", "reviewer": null, "issues": []}
}
```

After executing, replace nulls only with observed facts, keep the actual returned
file as a candidate, inspect it, then select it. Archive failed candidates when
useful; never silently overwrite the evidence of a failure and mark it solved.
