Current audio inventory: all 161 r001 lines are recorded. A line may bind real audio while `planning_status: pending_visual_authoring` and `beats: []` explicitly defer visual work. Missing audio still requires null timing/provenance. The 26 owner-selected S01–S03 scene images are recorded separately in `scene_image_selection.json`; planned endpoints do not automatically inherit those approvals.

Current acorn/setup amendment: S02-L001 and S02-L004 share the standing stone/stream view, actor root/depth/scale and acorn design from S02-L004-B01-I02 r004. L002 environment and L003 portrait are cuts within that physical place. Only L004 is a continuous no-cut placement action. S01 I03 shows the whole acorn before eating; the taste event moves to a planned, ungenerated I04 endpoint. See `stories/lion_and_mouse_v7/review/scene_compositions/acorn_setup_r005/REVIEW.md`.

# Audio-line visual workflow

V7 uses `stories/lion_and_mouse_v7/audio_visual_plan.json` (`feltwillow.audio-line-visual.v1`) as its single authored visual plan. Read the current audio line, plan its semantic visual beats, then declare the minimum meaningful still sequence for each beat. An audio scene is a narration chapter, not one camera setup.

Actual local `voice/narration/lion_and_mouse_v7/en/r001/lines/*.wav` samples own duration. Matching JSON owns recorded text, speaker and performance metadata; the versioned `timing.json` summarizes available audio. Derived indexes never supersede these assets. All 161 r001 lines in S01–S16 are recorded. The 63 lines beyond the currently authored 98 still need visual authoring and phrase alignment; their actual audio durations remain authoritative.

## Authoring

Use stable `SNN-LMMM-B##` beat IDs and `-I##` image IDs. One line can contain multiple ordered beats. Record exact semantic spans, action/emotion, cast, offscreen persistent cast, camera, location family/view, world states, explicit transitions and review status. `single` has one still; `pair` has start/end; `multi_key` has start, intermediate key(s), end; `cut_sequence` has two or more independent ordered single shots. These are planned placeholders, never selected or approved images.

Multiple beats and internal action keys remain `pending_alignment` until actual cadence/phrase alignment is reviewed. A one-beat line may cover the whole measured WAV without claiming phrase timing. Never subdivide a long line into arbitrary equal windows. Future aligned coverage must cover the complete line.

## Locations and continuity

A location family preserves geography, landmarks, material and light logic. A location view is one camera realization: master, close view, low mouse-height view, portrait with blurred background, route emphasis or detail. Plan new views against approved masters without changing master bytes. New views need generation provenance and owner review; existence confers no canonical status. Only genuinely different story geography calls for a new family.

Transitions are explicit: `cut`, `same_location_cut`, `same_state_camera_cut`, `continuous_motion`, `shared_boundary`, `time_change`, `location_change`, `portrait_cut`, `detail_cut`. Adjacent lines do not automatically share images. Connected motion requires a named continuity group, compatible view/state/cast and explicit image relationship. Cuts preserve world state. Only recorded causal events change props, location, time or actor state; the validator replays those events across every cut.

Keep Milo compact and without visible teeth; Leo has rounded golden-cream paws without claws/grey nails. Same-depth two-character standing-equivalent scale is 0.25; portraits change framing, not anatomy. Narrator audio never moves character mouths. Character dialogue is flagged for the later explicit alignment/lip-sync pipeline, with closed still-image boundaries.

## Local checks and review

Run with the existing feltwillow conda Python:

```bash
python production/audio_visual_plan.py --story lion_and_mouse_v7 validate
python production/audio_visual_plan.py --story lion_and_mouse_v7 derive
python production/audio_visual_plan.py --story lion_and_mouse_v7 readiness --gate planning
```

`derive` writes the chronological [owner inventory](../stories/lion_and_mouse_v7/derived/AUDIO_VISUAL_INVENTORY.md), summary, audio/dialogue indexes and future clip candidates. Edit the authored plan, then rederive. `readiness --gate image` and `--gate video` deliberately remain blocked while assets/reviews/timing are pending. Planning does not require nonexistent image bytes.

When new r001 line assets arrive, run `refresh-audio` to preview local availability changes, then `refresh-audio --write` to bind actual metadata/WAVs. Add semantic beats for newly available lines, validate and derive. Refresh does not synthesize audio, invent durations or author beats.

Future Wan intervals can be derived between adjacent approved images in a multi-key sequence; independent cuts stay independent. The current clip-candidate output has no runtime approval or fabricated timing. A later runtime adapter must verify actual approved still bytes, aligned coverage, dialogue and reviewed generated endpoints/takes.

The paired tools are historical and reject the new v7 schema. Exact former records and source utilities are preserved under `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/`, with SHA-256 manifest. V5/v6 keep their own workflows.

## Image filenames and audio lookup

Follow [audio-linked image naming](audio-linked-image-naming.md). New generated files carry line/beat IDs and matching provenance sidecars. `derive` creates AUDIO_IMAGE_INDEX.md and audio_image_index.json alongside the chronological inventory. A shared view keeps one file and lists every use.

## Current opening and reference usage

Follow [scene continuity policy](scene-continuity-policy.md). Independent shots may inhabit different local forest places while sharing style/world identity. S02-L004 is a connected background lock, and S03-L001–L008 share the S03-L006 fork camera/background with stationary Milo. A style reference does not constrain geography; a planned view need not be generated as a separate empty plate. The former 81-background operation is superseded by complete S01–S03 scene compositions for review.

## Character performances

Follow [character performance library](character-performance-library.md). The versioned library owns proposed/reviewed pose and angle-specific expression depictions; the existing audio-visual plan owns per-image actor bindings and shot staging. Reuse/impact is derived from those assignments. Planned references do not grant image readiness or scene approval. Preserve meaningful action phases, prop custody and explicit continuity; pose reuse does not force adjacent shots to share pixels.


## Ordered v7 sequence implementation (24 October 2026)

Use [sequence production](sequence-production.md) for the implemented resolver, scoped gates, endpoint compiler, isolated runtime and review commands. Legacy single-image pilot exports remain historical. No endpoint receipt, still selection or offline test establishes a full-motion or final assembly pass.


## Current r004 contract

Author `visual_units` once beside `production_sequences`: relationship (`individual|connected`), composition and mouth policy are separate axes. Current editorial waivers supersede obsolete pair requirements while legacy planned slots stay unchanged. Independent shots use one selected source; aliases do not duplicate motion jobs. Phrase partitions, complete PCM coverage, pauses and tails require explicit allocation. All 161 r001 lines are available; S09–S16 retain their current visual-authoring/classification backlog.

Read [sequence production](sequence-production.md) for the implemented grammar/runtime contracts and [the current work record](../stories/lion_and_mouse_v7/review/owner_sequence_feedback_r004/README.md) for exact story decisions, evidence and remaining blockers. No source or CPU pass grants artwork selection, spending, GPU execution or final-video approval.
