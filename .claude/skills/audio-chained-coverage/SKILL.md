---
name: audio-chained-coverage
description: Use when planning or checking narration-length visual coverage, audio-line visual beats, scene boundaries and joins. V7 uses audio_visual_plan.json; v6 uses keyframe/boundary plans; older stories may use prompt manifests. Route by schema and preserve actual audio authority.
---

# Audio-driven chained coverage (CR-21)


## V7 ordered sequence execution

Read `docs/sequence-production.md` and the current sequence-readiness ledger before proposing video work. `audio_visual_plan.json.production_sequences` owns ordered uses and edges; planned slots keep null media. Resolve selected scene bytes separately. Use a matching reviewed pose/expression as the depiction reference when one exists; do not redraw a different body from a scene thumbnail. Reuse requires compatible state, camera, custody and support. A hold cannot claim new visible motion. Preserve deliberate portraits/inserts as cuts. A/B/C compiles to A→B and B→C; B must reach both actual endpoint calls. Equal-image holds still supply both endpoints. Review native and actual model-fit images and protected pixels; owner selection is not an anatomy/background/contact pass. Exact runtime/run identity and effective settings must survive inventory, renderer, receipts and review. The new path does not use the historical bulk launcher or automatically retry uncertain jobs. No planning command grants spending, media selection, mouth treatment or final assembly authority.

## V7 reusable performances

Read [character performance contract](../../../docs/character-performance-library.md). `character_performance_library.json` is the single versioned performance authority; `audio_visual_plan.json` binds per-image/per-actor pose and expression IDs/variants. Canonical controls identity/anatomy/material; a reviewed performance controls its pose/expression only; shot staging independently controls camera, depth, screen scale, root/contact, light, shadow and occlusion. Performance approval is not scene approval. Planned assets pass planning and block required image-use readiness until real reviewed bytes exist.

Use `production/character_performance.py --story lion_and_mouse_v7 validate`, `derive`, `audit --review s01_s03_r001`, and `proposal --image-id ...`. Proposals are dry JSON only, with no submission route. Ordered references must name canonical identity, reviewed pose, angle/base-compatible expression, an explicitly required location, approved prop and edit base where applicable; include ID/revision/hash and allowed property. Never silently drop critical references for a provider limit. Do not promote scene crops, old v6 atlases or generated candidates to performance approval. Leo identity is reconciled by the current exact-hash owner record; legacy mismatch notes are historical.

Reuse preserves anatomy, not identical scene positions or one pixel height. Compare compatible head/body angles and camera/depth; unknown measurements stay `camera_unknown`. Fixed fork L001–L008 requires one shared root, foot contact and anatomical projection while gaze changes. S03-L004 stays stationary before the decision. Walks need distinct contact/passing/opposite-contact keys; tumble, scramble, paw/trigger/net and rescue actions keep their causal contact phases. Unique interactions may use one-off references. Expression variants preserve full ears/head silhouette and closed toothless still mouths; narration never drives mouths. Reuse never creates automatic line-to-line continuity.

For strict continuity, prefer a reviewed transparent actor layer with an explicit transform/root/occlusion/shadow recipe and protected-background audit. Guidance alone cannot guarantee anatomy or pixel identity. The CPU pilot is synthetic-only; no production composite or new performance image is authorized by this skill. Semantic character-asset names are allowed; scene images retain audio-linked names. The v5/v6 instructions below remain version-local.


**Horizontal consistency:** Follow the proportion skill for torso-panel and cream-patch widths, pelvis/thigh/arm surface bands and angle-compatible facial widths. Vertical agreement alone cannot pass anatomy review; hidden contours remain unavailable. Keep body and material-patch boundaries separate.

**Character-specific ratio profiles:** Use [character-proportion-review](../character-proportion-review/SKILL.md) and the [character proportion framework](../../../docs/character-proportion-framework.md). Create each profile after its first canonical is selected and bind exact canonical bytes. Milo and Leo have separate species-specific landmarks/targets; never transfer ratios between animals. Milo upright comparable-view head fraction is 0.39 ±0.01 absolute; all other unmeasured targets remain null. Bent limbs use visible in-plane joint chains; foreshortening, occlusion and uncertainty prevent a false pass. Portraits inherit compatible skull/ear/eye/muzzle ratios, not full-body fraction. Preserve the reusable checkerboard pose-card HTML gallery with native image links, exact audio IDs, local playback and separate pose/anatomy/scene states.

**Milo anatomy gate:** Follow `docs/character-performance-library.md` and the hash-bound anatomy policy/reviews in the performance registry. Pose/acting selection does not certify body proportions, prop fit or scene continuity. Compare compatible skull/torso, ears, neck and articulated limbs against the owner-preferred berry reference; unknown camera remains unknown. Use uniform whole-actor staging scale, never independently resize head/body/hands. Empty grip spaces require a separate actual-acorn contact/occlusion check. Planning may pass while anatomy review blocks image readiness; guidance alone cannot guarantee anatomy.

## V7 audio-line visual plan (`feltwillow.audio-line-visual.v1`)

Read [audio-line workflow](../../../docs/audio-line-visual-workflow.md). The single authored plan is `stories/lion_and_mouse_v7/audio_visual_plan.json`; character canon and location family/view libraries preserve identity. Run `production/audio_visual_plan.py --story lion_and_mouse_v7 validate` and `derive`. Use actual r001 WAV samples and matching JSON. Missing future audio stays pending with null duration. Segment meaning, never equal time windows; phrase/key timing awaits real alignment.

A line can have multiple beats. Use single, pair, multi_key or cut_sequence images as the story needs. Default cuts do not imply shared pixels. Motion/shared boundaries need explicit continuity groups and compatible states/views. Persistent props, actors and causality survive all cuts. Declare each location reference’s role: style/material only, geography/light, or an exact background/camera lock. New independent places and camera views may be planned without changing master bytes or claiming new approval. Narrator audio never moves mouths; dialogue uses the later explicit lip-sync pipeline with closed still boundaries. Preserve compact toothless Milo, rounded clawless Leo paws and same-depth 0.25 scale where applicable. Milo's apparent size is camera-relative: greater viewing distance makes him smaller, and closer distance, lens/zoom or cropping can make him larger. Compare size only after accounting for camera distance, lens/zoom, crop, subject depth and pose. At the same camera setup and subject depth, anatomical dimensions and scale relative to local landmarks must remain consistent; pose may change his bounding box. Independent wide shots and portraits do not require the same frame fraction. Record intentional camera/depth changes; do not invent measured distances or diagnose drift from screen size alone. Image/video gates remain separate from planning. No generation or spending is authorized by planning. Paired tools are historical and reject migrated v7.

Current owner direction: read [scene continuity policy](../../../docs/scene-continuity-policy.md). S01/S02 can use independent local forest places; the stream master is not a mandatory panorama. State each reference role: style/material only, geography/light, or exact background/camera. Only the words about water/stream stones require water. S02-L004 shares one placement background/camera. The `fork_decision` group now covers S03-L001–L008 using the S03-L006 background/camera, one stationary actor root and fixed anatomical scale; gaze/local acting can change, walking and translation cannot. `independent_scene`, `same_place_new_view` and `locked_background` are explicit authored choices; plot/prop causality survives all cuts. Planned views are not an instruction to generate one empty plate per view: complete scene images may establish independent settings directly. Do not resume the superseded 81-background batch or its seed retry.

For every new v7 image, follow [audio-linked naming](../../../docs/audio-linked-image-naming.md): audio-line/beat prefix, role/subject/revision and matching JSON with exact audio paths/hashes. Build names with `production.audio_visual_plan.image_filename`, validate and derive the audio/image index. Preserve existing canonical/master names; record all uses of a shared view without duplicating its image.

The remaining v6/legacy instructions below apply only to those schemas. In v7, exact locked-plate/camera requirements apply only to explicitly connected shots, not every view of a family.

**Current route:** Read [production direction](../../../docs/production-direction.md). Ordinary work uses approved images and Wan; Blender/control/material tools are optional paused research. Selection, technical evidence and owner approval remain separate. Resolve live frame IDs and the approved r03 Milo master; older performance-family references require refresh/revalidation. Experimental clips are not approved production takes.

For each visible character at a piece boundary and through the action, preserve valid support contact, depth-aware scale, landmark continuity and occlusion under [`docs/spatial-staging-consistency.md`](../../../docs/spatial-staging-consistency.md).

The narration is the timeline. Visual intervals must cover it in order, with
explicit cuts or exact shared image boundaries. The older prompt-manifest
implementation used 49–81-frame pieces; the current v6 packet stores visual
units and scene boundaries in separate plans and has not authorized video
pieces yet. Rules and reasons: `docs/creation-rules.md` CR-21. Every change to the
rules, tools or packets goes into `docs/changelog.md` (what, why, files, how it was checked).

This skill checks coverage and transitions. Every image and prompt still follows the repo skill
`consistent-image-prompts` (identity, sizes, plates, review gate): read it before writing any image
record or accepting an image.

## Current Lion and Mouse v6 (`keyframe_boundary_v1`)

The source is `stories/lion_and_mouse_v6/`:
`audio_manifest.json`, `scene_plan.json`, `visual_sequence_plan.json`,
`staging_plan.json`, `keyframe_plan.json`, `keyframe_visual_reviews.json`,
`video_boundary_config.json`, and `video_boundary_plan.json`. It has no
`prompt_manifest.json`, `timing_plan.json`, or `story.yaml`. Do not create
empty stand-ins or use retired `chain_packet.py` to inherit old images/renders.

1. Check all 161 audio lines and 16 scene spans against the visual sequence
   and boundary plan. Use v6-local WAV paths; `audio_manifest.json` records the
   authorized unchanged v5 English source recordings and hashes.
2. Run `staging_contract.py`, `keyframe_reference_gate.py`,
   `check_keyframe_review.py` and `keyframe_visual_gate.py` for
   `lion_and_mouse_v6`; see `docs/keyframe-regeneration.md` for the exact
   commands and image-source hierarchy.
   The visual gate must exit non-zero while any endpoint is unreviewed, stale,
   or rejected. Do not mass-approve the 96 current selections. Resolve current paths/hashes
   through the live keyframe plan; historical rejection records bind only their
   original bytes and do not certify newer replacements.
3. Review every cut/shared boundary in `video_boundary_plan.json`. A shared
   scene start is the exact previous scene end image bytes; a crop, plate or
   incompatible geometry change is a cut. Check actor scale, support contacts,
   landmarks and prop state on both sides. Word timing must be settled before
   a render interval can be frozen.
4. Run `python3 production/v6_runtime.py --story lion_and_mouse_v6 --preflight`
   before export or render. It consumes the current story-local plans and
   hash-bound approvals and exits non-zero while blocked. Export later needs
   explicit reviewed piece timing with `--export --timing <JSON>`; it writes
   a v6 `runtime_plan.json`, not a legacy `story.yaml`. See
   `stories/lion_and_mouse_v6/RUNTIME_CONTRACT.md` for the reviewed timing
   schema and acceptance checks.
5. After approved renders and exact take selection, run a join command with
   `--require-takes --fail-on-flagged-joins` only when the selected runtime
   format is supported. A flagged join blocks edit handoff.

## Manifest-backed chained packets (historical implementation)

The following commands require an actual `prompt_manifest.json`,
`timing_plan.json` and compatible runtime schema. They are **not** commands
for the current v6 packet. The one-off `chain_packet.py` v5→v6 copy tool was
retired and must not be used to build an independent story.

## Tools

| Step | Command (from the repo root) |
|---|---|
| How many pieces each line needs | `python3 production/chain_plan.py --story <slug> --audio-story <audio slug> suggest` |
| Check the current story's image handoff | `python3 production/image_handoff.py --story <slug> audit --strict`; `check <image-id>` before generating |
| Render prompts, check them | `python3 production/image_prompts.py --story <slug> build`, then `lint` (0 errors), then `md` |
| Time the pieces, set frame counts, timing sheet | `python3 production/chain_plan.py --story <slug> --audio-story <audio slug> apply` |
| Join test without clips (CPU) | `lumi/run_in_container.sh python production/chain_preview.py --story <slug> --stills [--until S]` |
| Record a reviewed image approval | `python3 production/image_prompts.py --story <slug> approve <image-id> --reviewed-by <name>` |
| Runtime story for the GPU | `python3 production/export_runtime.py --manifest stories/<slug>/prompt_manifest.json --story <slug> [--scenes ...]` |
| Strict join test with chosen takes | `lumi/run_in_container.sh python production/chain_preview.py --story <slug> --until S --require-takes --fail-on-flagged-joins` |
| Align narration words (after audio is final) | `bash voice/setup_lipsync_env.sh`, then `.venv-lipsync/bin/python production/lip_sync.py align --story <slug> --audio-story <audio slug> --lang <lang> --device cpu` |
| Apply timed mouth animation after take selection | `python3 production/lip_sync.py apply --story <slug>` (use the isolated `.venv-lipsync/bin/python`) |
| Repair a bad join from the selected previous take | `python3 production/chain_repair.py --story <slug> --piece <later> --previous-piece <earlier>` |
| Export complete edit handoff | `python3 production/edit_manifest.py --story <slug>` |

`chain_preview.py` and `animatic.py` assemble pictures: run them when the owner asks for a preview or
join test, never automatically after a render (CR-01).

## Historical manifest-piece planning details

1. **Start from the rendered narration** (`work/stories/<audio slug>/audio/<lang>/timing.json`). Run
   `suggest`: every line's span (the line plus the pause after it; the last line also owns the 1 s
   scene tail) and how many pieces it needs alone. A piece covers **2.45 to 6.33 s** (49 to 81
   frames at 16 fps, retimed 0.80 to 1.25).
2. **Write the shot plan in the manifest-backed story's manifest.** An independent story such as
   Lion and Mouse v6 owns its bible, images, narration and render plan; never
   rebuild it from an older version. Each legacy piece: id
   (`sNN_<name>`), scene, setup, start and end image ids, `lines`, one action sentence, mode
   (`closed`, `mouth`, `ambient`), and either `join="chain"` (default) or a cut.
3. **Fit the lines.** Consecutive pieces may share a line (its span is split evenly). If a piece
   comes out too short, give it a neighbouring line; too long (a line over 6.33 s), split the line
   over two pieces. Prefer to change the plan, not the bounds.
4. **One action per piece**, reachable from the start image to the end image. Long narration with
   nothing happening gets a **hold** (start = end: breathing, blinking, ears, tail tip) or a
   **landscape** (mode `ambient`, no cast, start = end = the plate `PL_<loc>`, or an empty scene
   frame when a prop must show). Avoid long runs of holds on one image; alternate with a close-up,
   a landscape or a small action.
5. **Entrances and exits.** A character never pops in on a fixed camera: chain an entrance piece
   from the empty plate to a frame with the character just inside the edge, and an exit piece to the
   empty plate.
6. **Cuts** (`join="cut"`, `cut=<reason>`, optional `transition`): `close_up` (into or out of a
   close-up or close two-shot), `camera_change` (another setup at the same place), `time_change`
   (same place, another light: use `crossfade`), `location_change`, `dissolve` (time passes on the
   same camera; needs `crossfade` or `dip`; the only cut allowed within one setup). The first piece is
   `film_start`. Lint checks that each reason is true; any other same-setup cut is a jump cut.
7. **Talking chains.** Every clip starts and ends on approved closed-mouth frames. A `mouth`
   variant uses one separate approved `_open` calibration image edited from one of its closed
   endpoints (CR-19, CR-23/24). Use `mode: mouth` only when a covered audio line is explicitly
   assigned to the visible character; give the variant one `speaker` matching that character's
   `voice_speaker` in the bible. Narrator voice-over never moves a character's mouth, even if it
   describes speech or a call. Keep mouths closed during narration, other characters' lines and
   silent pauses. Mixed-speaker pieces sync only the named visible character, or split into
   speaker-specific shots. Wide shots keep mouths still because they are too small to review.
   Forced-align final audio, then run the timed mouth compositor on owner-selected takes.
   `edit_manifest.py` requires a current hash-bound result for every `mouth` variant. Review
   speaker timing and joins. See `docs/lip-sync.md` for the single-shape approximation.
8. **Reuse only within the same approved asset version.** A reuse entry imports the earlier
   render and its character design. For Lion and Mouse v6, every piece is a new v6 render;
   no older-version `reuse`, `carried_from`, or base-story path is allowed.
9. **Video prompts describe only what is in frame** (fast mode, CFG 1: a named absent object is drawn
   in; v5 scene 15). In dialogue close-ups, use `{{portrait:<char>}}` and lock the approved crop and
   visible silhouette from the endpoint frames. Do not include full-body identity text or mention body
   parts outside the crop. `image_prompts.py lint` enforces this for new close-up variants (CR-22).
10. Build, `lint` 0 errors, `md`, `apply`. Read `SHOT_PLAN.md` and `TIMING_SHEET.md` as the owner will.
    Log the change in `docs/changelog.md`.

## New images in a chain

- A frame that first appears as the **end** of a piece is an edit of that piece's start
  (`edit_base` first, `edit_chain_frame` wording, the locked plate next). Lint enforces it for the
  story's own new images.
- A **boundary image** serves two clips: review it against the earlier piece's start and the later
  piece's end (the pose must be reachable by one small action from both), plus the usual gate
  (canonical, size anchor, plate) of `consistent-image-prompts` D.
- For every sharp-background scene endpoint with visible characters, `size_anchor` is mandatory on
  both start and end. Keep the same-setup approved anchor in the actual attachment list after any
  provider reference limit; preserve the edit base first and drop optional staging references first.
  Measure the generated character bounds and shared-cast ratio against the setup target and anchor
  before staging. Missing anchor or failed size check means the endpoint is not ready for the chain.
- New images are named `sNN_KK_<name>_rNN.png`, `KK` = first use in the scene (lint checks it).
- An empty view that must keep a prop where a scene frame has it (the net in the branches) uses the
  role `empty_copy` on that frame, not `edit_base`.

## Before rendering

- `export_runtime.py` refuses while any endpoint image is missing; use
  `--scenes` for a pilot of scenes whose images exist.
- Run `chain_preview.py --stills` first: pacing, cuts and the chain against the narration, minutes on
  a CPU.
- Render a **pilot of the first scenes**, let the owner choose takes (`takes.yaml`: `piece: seed` or
  a file, or the `best_` prefix), then run `chain_preview.py --until <end of pilot>`. A flagged join
  (jump/motion > 3) or a pace far from 1 is repaired by re-rendering the later piece with
  `continue_from` the chosen take's last frame, or by fixing the boundary image. Only then render
  the rest (`lumi/render_story.sh`).

### Connected stationary shots and portrait bodies

When a connected actor is planted, lock the same root/foot contact, standing depth, anatomical scale, camera/crop and selected background across all assigned images. Gaze or local body acting is not permission to walk, slide, resize or relocate. Use protected plate/layer recipes for exact locks; prompt guidance is insufficient evidence.

For related close-up portraits, choose one visible upper-body reference and keep shoulder/chest construction, visible extent, scale, head/neck relationship and crop identical while changing angle-compatible expression/gaze. A blurred background does not permit torso or framing drift. Apply only within the declared setup, not universally across unrelated portraits. Current v7 S03-L009/L010 use S03-L010-B01-I01 r002 as the body/crop reference.

### Persistent edible props and articulated continuity

Bind an edible story prop to an exact size/design reference relative to the actor, accounting for camera, depth and prop orientation. A taste/bite event changes the prop once; keep the same missing-area topology and extent across later cuts until another event changes it. This never authorizes visible Milo teeth. For no-cut stand-to-crouch actions, reuse the shared standing frame, preserve camera/support depth, part lengths and body bulk, articulate hips/knees/arms, and distinguish held -> contact -> released. Do not shrink the actor or rescale the prop to fit hands. Crouched bounding height may change. Verify foreground contacts and protected background independently; image guidance is not proof of a smooth video.

## V7 action-specific facial acting

For every visible actor/key image, author emotion, effort and eyeline from the actual audio/action: hurry and concentration, alarm at contact, panic through a fall, and stunned recovery are different performances. Do not carry the same pleasant neutral face through all actions. Bind a versioned expression asset in the actor's `expressions/` directory; keep its skull, ears, eyes, muzzle and neck geometry canonical and portrait-base compatible. Narrator audio never creates speech mouths or new teeth.

Body-only acceptance does not approve the face or establish measured anatomy. Keep scoped owner feedback tied to exact hashes without rewriting original receipts. An expression binding does not change pixels: record whether it has been applied. Before a focused face edit or composition, verify local yaw, pitch and roll against the expression view; author a local variant when incompatible. Preserve retained body geometry, support and prop contact. Do not paste a forward portrait indiscriminately onto a crouching or tumbling head. Review readable acting and unchanged anatomy at native size. Generation still requires approval of its concrete operation.

## V7 matching-pose reuse gate

Follow [matching prepared performances](../../../docs/character-performance-library.md#matching-prepared-performances-must-be-used): use the compatible reviewed pose as the depicted body reference with exact revision/hash in actual inputs. Reject visible anatomy/paw-color drift even if it was attached. Repair a defective pose before scene use; explain any necessary local variant. Scope face acceptance separately. This does not force cuts, camera/size or world-state changes.
