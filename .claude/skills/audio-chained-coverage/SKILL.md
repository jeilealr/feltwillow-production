---
name: audio-chained-coverage
description: Use when planning or checking narration-length visual coverage, scene boundaries and joins. First identify whether the story uses a keyframe/boundary plan (current Lion and Mouse v6) or a prompt manifest (legacy chained packets); do not run manifest commands against v6.
---

# Audio-driven chained coverage (CR-21)

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
2. Run `python3 production/staging_contract.py --story lion_and_mouse_v6`
   and `python3 production/keyframe_visual_gate.py --story lion_and_mouse_v6`.
   The visual gate must exit non-zero while any endpoint is unreviewed, stale,
   or rejected. Do not mass-approve the 92 current candidates; `s14_p04` and
   `s14_p05` retain known hash-bound r01 rejections while their active r02
   replacements await full-size review.
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
