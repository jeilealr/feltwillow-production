# Change log

Dated record of changes to the rules, tools and story packets, newest first within a day.
Each entry says what changed, why, which files, and how it was checked. Owner instructions
are quoted or summarised with their date. Git history has the diffs; this file has the reasons.

## 2026-10-13 — v6 replacement-image owner inputs recorded

- Recorded hash-bound owner approval for the current Milo canonical and hunter-net design as replacement-generation inputs.
- Recorded six owner-selected, hash-bound camera-family anchors and created byte-identical stable snapshots; the original candidate images remain intact.
- Marked three target anchor families for new calibration candidates. Replacement keyframes have not yet been generated; see the second-image audit remediation and anchor review packet.

## 2026-10-13 — second v6 image-audit remediation

Implemented the second audit against starting commit `ce821fc1573c05215fae84ae6672ccf0d32f4645` on `working-cloud-branch`. Prompt identity and cast ratio now come from the v6 visual bible; historical prompt/reference provenance cannot silently become active generation input. The reference, visual and runtime gates now separate active authority blockers from unavailable historical provenance, bind all 96 candidates to an explicit current/stale disposition, and require human-recorded visible-limb/support evidence. Revisions must be newer and have a saved replacement before they clear stale status.

Recorded owner-reported active failures for `s08_p04`, `s10_p02`, `s14_p06` and `s15_p04` against their exact hashes. Ten camera-plan-stale frames are marked for supersession, not rejected. Added the 29-family setup-anchor selection packet and 96-frame remediation inventory. No replacement PNG or owner approval was fabricated; required canonical/atlas, prop, anchor and visual approvals remain blockers.

- **Checked:** all 74 unit tests pass; compileall, Markdown links, `git diff --check`, staging contract (0 errors / 96 frames), and pose coverage (0 errors / 23 definitions / 96 frames) pass. The reference gate reports 277 current-authority blockers and 58 historical warnings; the visual gate reports 114 blockers; runtime preflight reports 391 blockers and writes no files. Video remains blocked pending owner decisions and image review.
- **Files:** `production/keyframe_plan.py`, `production/keyframe_reference_gate.py`, `production/keyframe_visual_gate.py`, `production/revise_keyframe_candidate.py`, `production/staging_contract.py`, `production/v6_runtime.py`, `production/check_keyframe_review.py`; v6 visual bible, plan, review ledger and regeneration contract; tests; `CLAUDE.md`, the keyframe regeneration/creation/prompt/production guides, story review documents and both audit packets.

## 2026-10-13 — v6 keyframe regeneration and continuity remediation

Applied the owner-provided image-generation audit to the native v6 pipeline while
preserving approved canonicals, location masters and liked keyframe pixels.

- Restored `s13_p06` to its exact recoverable r01 candidate because the declared
  r02 bytes were not in the checkout or Git history; removed the unreferenced
  `s07_p03_r03` extra and rebuilt the 16 current contact sheets.
- Added a portable hash-bound regeneration contract, deterministic registered
  crop materializer, root/crop/identity/anchor checks, and revision-tool checks
  for source order, prompt conflicts, dimensions, hashes and superseded-candidate
  provenance. The current candidate and historical reference records are kept
  distinct. External generated-image-cache paths are labeled provenance only.
- Expanded prompt construction with actor identity locks, exact world/light
  clauses, staging-derived height targets, registered camera families and
  closed-boundary mouth metadata. Corrected `tree_day`; added Great Tree dusk
  color locks and explicit speaker portraits for the revised camera coverage.
- Scene 16 matching wides share one staging/anchor family. Ten candidates with
  changed registered crops or views are marked stale for a future saved
  revision. Deterministic `keyframe.py` composition now accepts a story/frame ID,
  exposes background blur, writes source/output hashes and can emit a protected-
  background edit mask.
- Added gate, crop, staging, camera and runtime tests; documented required owner
  approvals and the fail-closed image-review state. Milo's revised canonical,
  pose atlases, props and setup-size anchors remain pending where their source
  records say so; no new image or approval was fabricated.
- **Checked:** all 68 unit tests pass; `compileall`, Markdown links and
  `git diff --check` pass. Staging and pose coverage report zero errors for all
  96 frames. Active PNG inventory, contact-sheet manifest and review links agree.
  Reference validation reports 338 owner/provenance blockers; the visual gate
  reports 96 missing full-size reviews. Runtime reports those 434 blockers and
  zero structural/audio errors, so it remains fail-closed until owner review.

## 2026-10-11 — v6 individual video keyframes for review

Owner direction: turn the v6 `.review` storyboards and narration-aware visual plan into individual keyframe images under `character/characters/lion_and_mouse_v6/interactions/keyframes/`, with character and location consistency, then present the complete set for review.

- Kept the 16 English audio tracks unchanged. The 70 overview panels plus 22 supplemental detail panels yield 92 individual 1920×1080 keyframe candidates across 52 visual units. `keyframe_plan.json` records their approved plates, crops, staging records, audio lines, prompts, statuses and SHA-256 hashes.
- Generated 16 contact sheets and a scene-by-scene image index in `KEYFRAME_REVIEW.md`. The `.review` boards remain composition references. Revised the Scene 05 sleeping/waking inserts, Scene 06 rise, Scene 04 receding run, and Scene 13–14 net-to-escape continuity after visual review.
- Checked all 92 active PNGs for unique IDs, exact canvas dimensions, recorded hashes and panel mapping; all 16 contact sheets and review links resolve. The staging validator reported zero errors for 92 frames; all six staging tests passed; `git diff --check` passed. Individual images remain pending owner approval, and video takes are not yet rendered.

## 2026-10-11 — v6 audio reconciliation and 16-scene storyboard coverage

Owner direction: reuse v5 English line audio in v6, reconcile text and timing, and generate as many scene boards as needed to cover every voice line for review. Exact v5 WAV bytes were copied under the v6 work namespace; the text and per-line durations were reconciled and recorded with source hashes.

- Reconstructed 16 scene tracks totaling 11:23.7, matching the v5 timing sheet. Mapped all 161 line IDs exactly once across 70 chronological storyboard panels in 16 scene boards. Narration remains voice-over; only assigned character dialogue is staged for character lip-sync.
- Generated v6-native multi-panel storyboard candidates, retained prompt/reference/hash provenance in `scene_plan.json`, and indexed current versions in `SCENE_REVIEW.md`. These are review boards, not final keyframes, generated video, or an edit.
- Accepted v6 character and location foundations are used as visual references. Acorn/net props remain candidates for review. Re-generated affected boards to keep Milo’s ears in frame and Leo’s face clear of net strands.
- Checked audio IDs, byte hashes, timing, scene coverage, prompt references, and candidate image files; all 16 boards are present. Owner review remains open.


## 2026-10-10 — v6 independent LUMI handoff and image gates

Owner direction: keep Lion and Mouse v6 fully separate from earlier versions and prepare the
documentation and code so later scene generation keeps the approved characters, scale, plate
geometry and believable ground contact.

- Removed the inherited packet source and all active older-version image, render and audio links
  from v6. Its 154 pieces are new render jobs. V6 narration files must be staged under the v6
  audio path before audio timing can be verified; saved durations remain a draft planning value.
- Reconciled 54 accepted r02 foundation images with hash-bound records, retained 42 blurred
  portrait candidates, and left 71 scene frames planned. Removed six scene records no shot uses.
  Renamed active v6 scene targets and portrait candidates by their first use in film order.
- Fixed edit-base, locked-plate and size-anchor references; added explicit numeric size and
  walkable-surface targets to the v6 bible. Earlier single-character frames at the tree and trap
  are explicit bootstrap records. The scene reference graph has no cycles.
- Added `production/image_handoff.py` and an approval gate for measured scale, support points,
  candidate/target identity and approved references. Updated the two repository skills,
  `docs/creation-rules.md`, and the v6 README/LUMI handoff.
- Checked prompt lint at 0 errors; the remaining 39 warnings identify scene target files that
  are intentionally absent until generation. The handoff audit reports zero foundation approval
  issues and zero reference cycles; first-frame, tree bootstrap and empty-trap checks pass.

## 2026-10-10 — superseded v6 scene-scale and trapped-net experiment

Owner direction: reduce Milo to half his size in the approved great-tree paw-contact reference,
keep the revised scale through the scene set, make the trapped net physically wrap Leo instead of
reading as a web between him and the viewer, remove the unexplained strand crossing his face, and
keep one review image per candidate.

- Updated v6 `cast_scale` and every scene-wide setup measurement in `visual_bible.json`; the
  tree-dusk two-character reference now targets Milo at 0.105 of frame height. Added a close-up
  net rule with a clear face opening and continuous, supported rope paths.
- Updated the affected trapped-Leo prompt records and rebuilt their rendered prompt fields.
- Replaced 10 `.review` candidates (the Milo scale reference and nine trapped-Leo close-ups) with
  edited 1920x1080 candidates. Removed all 45 paired `_source.png` files, retaining candidate
  images and their prompt/hash sidecars as requested. The images remain pending owner review.
- Checked the image outputs' dimensions and visually reviewed the Milo scale and net/face openings.
  `image_prompts.py lint` reports 75 size-anchor attachment errors and 19 missing-target warnings;
  those setup/reference links must be corrected before staging a full regenerated scene set.

## 2026-10-09 — Owner image-status follow-up

Owner instruction: mark existing Lion and Mouse v5 missing-after-review output accepted, and do the same for Ugly Duckling v1. The v5 `s02_place_acorn_end` r02 image exists and its SHA-256 matches the recorded accepted result; its v5 record and byte-identical v6 carryover are now `accepted`, with the owner's instruction and digest recorded. The v6 carried-image export gate remains fail-closed for every other non-accepted record.

- Restored the already-accepted v5 `s08_milo_surprised_start`, `s08_milo_surprised_end` and `s12_runs_end` target files from runtime-input copies whose hashes match both the manifest's recorded image result and the frozen runtime inputs. No existing file was overwritten.
- Three accepted v5 Milo reference targets (`M_SIDE_R`, `M_SIDE_L`, `M_BACK`) remain absent; no exact hash-matching source exists in the v5 character assets or runtime keyframes. Their records were already marked accepted. Ugly Duckling v1 has 152 accepted image records and no accepted record with a missing target; its absent Scene 11 images are planned and its deleted `s06_ottie_stays_end` record remains superseded. No status was changed for v1.
- Checked exact SHA-256 values before recording acceptance/restoring files. No new images or media were generated.

## 2026-10-09 — Final approval-state gate and deferred image phase

The owner selected full Lion and Mouse v6 image regeneration as a later phase and instructed that
no images be created before the audit and code work are reported. The current packet remains an
interim baseline with 118 carried v5 images, 22 inherited expression studies, 33 planned new
images and 25 render reuses; it is
not the all-new image packet.

- **Review status is authoritative:** `s02_place_acorn_end` is carried from v5 with status
  `missing_after_owner_review`, although a byte-identical file and a v5 render exist. Runtime
  export now rejects non-accepted carried endpoints even in reused pieces. Edit-manifest export
  checks the same state before selecting takes. A file or hash cannot reverse owner review.
- **Checked:** a focused regression rejected the bad carried image in both exporters; a copied
  manifest with its status changed to `accepted` passed the pure edit check. The failed runtime
  export produced no partial v6 `story.yaml`. No images, audio or video were generated.

## 2026-10-09: v6 readiness audit remediations

Executed the owner-provided v6 readiness audit findings before image generation or the pilot.
No images/audio were generated and no GPU job was launched.

- **Version-local inherited assets:** `chain_packet.py` copies resolved v5 character, location and
  expression assets used by v6 into matching v6 folders and rewrites v6 bible/manifest references;
  the v5 source files remain intact. The v6 manifest and generated `prompts/expressions.md` now index
  all 22 accepted inherited expression studies, so the expression group is visible in the new version.
  Lint identifies inherited records by `carried_from`, preserving their source filenames and provenance.
- **Lip-sync expectation:** the v6 README and production guide state that mouth clips use the approved
  open/closed shapes with generic speech motion; they do not claim word- or phoneme-level sync.
- **Files:** `production/chain_packet.py`, `production/image_prompts.py`, the v6 source, packet and
  generated prompt markdown, CR-21, the chained-coverage skill, production guide and this log.
- **Checked:** 118 carried manifest images and 22 expression studies have v6-local assets matching
  their v5 sources byte-for-byte; only the 33 planned v6 keyframes are absent. Prompt lint reports
  0 errors and 0 warnings; `git diff --check` is clean. No new image generation was run.

- **Prompt consistency:** all 16 v6 open-mouth frames now attach the closed edit base, locked plate, canonical,
  and mouth study in that order; chain lint errors if a v6-owned image lacks its locked plate. The Scene 9
  resting frame now attaches `s16_friends_start` as a size anchor. CR-19 now states that open-mouth anchors
  are required for readable dialogue close-ups; wide shots may keep small mouth motion without extra keyframes.
- **Safe packet rebuild:** `chain_packet.py` preserves a new image's result, approval, review, hash and extra
  provenance fields when its structural specification is unchanged. If a record with production state changes,
  rebuild stops until the owner explicitly names it with `--invalidate <image-id>`; the old record is retained
  under `superseded` in the regenerated manifest.
- **Approval gate:** `image_prompts.py approve` records the exact manifest target, image SHA-256,
  rendered-prompt/specification SHA-256, ordered reference paths and hashes, reviewer and time.
  `export_runtime.py` refuses v6-owned endpoint images without a matching approval file and all hashes.
  Carried v5 assets retain their original approval/provenance path; selected v6 files come from the
  approval record, not highest-revision lookup.
- **Pilot gate and repair:** `chain_preview.py --require-takes` checks every chosen clip exists and has the planned
  frame count before encoding. Join motion and pace use the retimed preview frames. `chain_repair.py` records the
  exact preceding selected take and hash; runtime export creates a separately named continuation candidate, and
  `shot.py` resolves and hash-checks the source without replacing the original keyframe or render. It also works
  when the preceding chosen piece is a v5 reuse.
- **Edit handoff:** `edit_manifest.py` exports a hash-bound film-order contract with exact selected clips, retiming,
  transitions and narration intervals for external editing. It does not render the final film; DaVinci assembly
  remains the production boundary.
- **Planner robustness:** `chain_plan.py` now rejects duplicate/missing line IDs, timing mismatches, invalid line or
  scene durations, and duplicate/non-contiguous piece order values with named errors.
- **Close-up silhouette lock:** new v6 dialogue-video prompts use face-only portrait descriptions and an explicit
  endpoint crop/silhouette lock; lint checks the prompt and rejects body-part mentions outside that crop.
  Reused v5 clips retain their original prompts. Added CR-22 and updated the chained-coverage skill.
- **Files:** `production/chain_packet.py`, `image_prompts.py`, `image_approval.py`, `export_runtime.py`,
  `chain_preview.py`, `chain_repair.py`, `edit_manifest.py`, `chain_plan.py`, `shot.py`, the v6 source/packet
  and prompt skills, CR-19/CR-21, `CLAUDE.md`, `docs/production-guide.md`, and this log.
- **Checked:** documented v6 lint and chain timing checks; legacy lint summaries unchanged; Python compilation;
  strict preview missing-take failure; approval file/spec/reference hash creation and mismatch rejection;
  packet-state preservation and changed-spec refusal; chain-repair/export integration for both new and reused pieces;
  edit-manifest serialization and source/audio hash handoff (frame probe stubbed); malformed planner-input cases;
  `git diff --check`.
  CPU-only preview remains available;
  no image generation, audio generation or GPU rendering was run.

## 2026-10-08: Lion and Mouse v6, audio-driven chained coverage

Owner, 2026-10-08: the v5 audio is far longer than the 5 s clips; for v6, create as many
prompts, images and clips as the narration needs, so the video lasts as long as the audio, and
the end of one scene is the beginning of the next, keeping the consistency skills. Landscape
clips (e.g. the stream plate) cover narration with nothing happening. A cut is fine where it
makes sense (a face close-up, day to night). `continue_from` stays a repair option. Add a test
of how the joins work together once the inputs exist. Make the changes one at a time and
record them. Defaults taken by the agent (no owner answer yet): reuse the v5 English narration
(no new TTS) and reuse v5 images wherever they fit the chain.

### 1. Rule CR-21: audio-driven chained coverage

- **What:** new rule in `docs/creation-rules.md`: the narration is the timeline; pieces of 49 to
  81 frames; chain by shared image records; marked, checkable cuts (`film_start`, `close_up`,
  `camera_change`, `time_change`, `location_change`); no same-setup cut; landscape pieces and
  entrance pieces; holds; talking chains; boundary-image review; reuse of earlier renders; the
  join test, with `continue_from` as the repair.
- **Why:** the owner's request above; clips longer than 81 frames are quadratic in cost and
  drift (`docs/lumi.md`), so length comes from more pieces, not longer clips; trimming a clip
  would cut off the shared end image, so frame counts are chosen per piece instead.
- **Files:** `docs/creation-rules.md` (CR-21), `docs/changelog.md` (new).
- **Checked:** text only; the tools it names are the next entries.

### 2. Lint: chain, cut, frame and landscape rules (`production/image_prompts.py`)

- **What:** when the bible has `"chained_coverage": true`, `lint` runs `lint_chain`: one variant
  per piece; every piece has a bible `setup` and `lines`; endpoints are scene records of that
  setup or the setup's own empty plate (landscape and entrance pieces); `join_in: chain` starts
  on the predecessor's end image; `join_in: cut` needs a `cut_reason` that is true for the two
  setups (`close_up`, `camera_change`, `time_change`, `location_change`; the first piece is
  `film_start`); a cut inside one setup is reported as a jump cut; `transition` is `cut`,
  `crossfade` or `dip`; frames are 4k+1 within 49 to 81; start = end only with `hold: true` or
  mode `ambient`; ambient pieces have no cast; `reuse` must name an earlier variant with the same
  endpoints, runtime prompt and frame count. The start/end pair rules (same setup, an end frame
  edits its start) now apply where an image first appears in the chain, since one image is the
  end of one piece and the start of the next. New chained images are named `sNN_KK_...` by first
  use in the scene (`chain_chrono_names`); images reused from an earlier version keep their names.
- **Why:** CR-21 (entry 1); the lint is the gate every prompt passes (CR-18).
- **Files:** `production/image_prompts.py`.
- **Checked:** lint output of all four existing stories is byte-identical before and after
  (Lion and Mouse v5: 70 errors, 8 warnings; Ugly Duckling v1: 22 errors; Tortoise and Hare v1
  and Boy Who Cried Wolf v1: 0). A test manifest built from v5 records passes clean, and a
  broken copy reports each planted fault: a wrong first piece, a broken chain, a false
  `cut_reason`, an 83-frame clip, a same-setup cut with endpoints from another setup, and an
  unflagged hold.
- **Found, not caused:** Ugly Duckling v1 lint reports 22 errors (missing `.review/` raw files
  and `review/reference_boards/*_character_guide.png` references), although `CLAUDE.md` says 0.
  Not changed here.

### 3. Planner: `production/chain_plan.py` (new)

- **What:** times a chained story's pieces from the narration. Each line owns the span to the
  next line's start (pause included; the last line also owns the 1 s scene tail), so spans add
  up to the scene audio exactly. A piece lists its `lines`; a line shared by consecutive pieces is
  split evenly. Each piece gets the Wan frame count (4k+1, 49 to 81) closest to its seconds and a
  retime speed within 0.80 to 1.25, so a piece covers 2.45 to 6.33 s. `suggest` lists every line
  and how many pieces it needs; `check` reports uncovered lines, out-of-order or non-consecutive
  lines and out-of-bound pieces; `apply` writes the frame counts into the manifest variants and
  writes `TIMING_SHEET.md` and `timing_plan.json` (start, length, frames, speed, join, endpoints
  of every piece; nothing held or stretched).
- **Why:** CR-21; `timing_sheet.py` (kept for unchained stories) can only stretch a fixed shot
  list over the audio. Frame counts below 81 replace trimming, which would cut off the shared end
  image.
- **Files:** `production/chain_plan.py`.
- **Checked:** `suggest` on the v5 narration: 11:23.7 in 16 scenes, at least 108 pieces and
  about 135 at full length (scene 15 alone 17 to 20); frame selection gives 49 frames at
  1.25 speed for 2.45 s, 81 frames at 1.00 for 5.06 s and 0.80 for 6.33 s.

### 4. CR-21 and lint amended while planning v6: `dissolve`, same-place camera change, empty scene frames

- **What:** new `cut_reason` `dissolve` (time passes; requires `transition` crossfade or dip; the
  only cut allowed inside one setup). `camera_change` now means the same place (the plate's
  folder), not the same location profile, because the great tree's dusk wide, close-ups and
  upward sky view are separate profiles of one place. A landscape piece may also hold on an
  approved empty scene frame of its setup, when a prop belongs in the view.
- **Why:** found while planning v6: the film should end on the empty tree after the friends
  (same camera, time passes), the tree's sky cutaway is a camera change, and the trap path's
  bare plate has no net, so a landscape of the trap needs the net drawn in.
- **Files:** `docs/creation-rules.md` (CR-21 items 4 and 5), `production/image_prompts.py`.
- **Checked:** lint output of the four existing stories still byte-identical to the baseline.

### 5. Packet builder `production/chain_packet.py` (new) and the Lion and Mouse v6 packet

- **What:** `chain_packet.py <source>` writes a chained story from a source file and a base story:
  the base bible with `chained_coverage` and `keyframe_chrono_naming` on, the base image records
  (marked `carried_from`; the expression-study records stay in the base story and are attached
  by path), the new image records (CR-18 template order; a chain frame edits its neighbour with
  the new block `edit_chain_frame`, an open-mouth frame follows CR-19 with `edit_open_mouth`),
  one shot per piece, the line list mapped to pieces, `SHOT_PLAN.md` and `README.md`. A `reuse`
  piece copies the base variant verbatim. New video prompts describe only what is in frame (the
  v5 scene 15 lesson). Carried records whose files the owner renamed after v5 (three `.png.png`
  references, two `s08_milo_surprised` frames now r01, `s12_runs_end` now r02) are resolved
  through the v5 image-set READMEs, as `export_runtime.py --images` does; the old name stays in
  `base_target`.
- **The plan** (`stories/lion_and_mouse_v6/chain_source.py`): 154 pieces cover the v5 English
  narration (11:23.7) exactly; 25 reuse v5 renders, 129 need new renders; 48 are holds or
  landscapes (opening stream landscape, fork, dusk sky, empty lanes, the trap with the net set,
  and four tree, trap and stream landscapes in the closing narration). 33 new images: 16
  open-mouth frames for the talking chains, 3 entrance frames (Milo at the stream, Milo at the
  fork, Leo back at his tree), the empty trap with the net, and 13 frames for new beats (Milo at
  the feeding stone, Milo looking at the sky, Leo's sleeping face, the tumble ending in the wide
  shot, Leo lifting his head, Milo at the net, a Milo close-up for his S13 lines, the frame before
  the first bite, the gnawing seen wide, Leo sitting, Leo bowing, Leo's smile, the friends
  resting). Frame counts 49 to 81, speeds 0.80 to 1.23.
- **Lint changes made for it** (`production/image_prompts.py`): records with `carried_from` skip
  the reference-file check (their story's lint covers them); in a chained story the "end frame
  edits its start" rule applies to new images only; new role `empty_copy` (copy a frame without
  its characters) may show characters absent from the frame; `edit_chain_frame` counts as an
  edit block.
- **Files:** `production/chain_packet.py`, `production/image_prompts.py`,
  `stories/lion_and_mouse_v6/` (source, bible, manifest, line list, `SHOT_PLAN.md`, `README.md`,
  `prompts/`, `TIMING_SHEET.md`, `timing_plan.json`), the empty folder
  `character/characters/lion_and_mouse_v6/interactions/keyframes/`.
- **Checked:** `image_prompts.py --story lion_and_mouse_v6 lint`: 0 errors, 0 warnings;
  `chain_plan.py ... apply`: 154 pieces cover 11:23.7 of 11:23.7, 0 errors; video prompts 75 to
  218 words (v5 measured up to 346 umT5 tokens for similar prompts, limit 512); the other four
  stories' lint output unchanged. Fixed on the way: the plate attached twice on entrance frames,
  a colour word and a body word in one action sentence, Milo counted in Leo's solo frame.
- **Found, not caused:** `CLAUDE.md` says the 70 v5 lint errors are all expression-record
  references; they also include `staging_only` references to deleted v3 images in scene
  records (s10 to s14). v5 is unchanged.

### 6. `production/export_runtime.py`: reused pieces are not exported

- **What:** a piece with `reuse` is left out of the runtime story and listed under `reused:` in
  `story.yaml`, so `lumi/render_story.sh` never re-renders it.
- **Checked:** a test export of v6 scenes 2 and 4 (the scenes that need no new image) gave 5
  runtime shots with planned frame counts (61, 77, 81, 77, 81) and seeds, and 3 reused pieces;
  the test `story.yaml`, `runtime_inputs.json` and frozen keyframes were removed afterwards (no
  runtime story exists for v6 yet). A full export stops, as designed, on the 33 images not yet
  made.

### 7. Join test `production/chain_preview.py` (new)

- **What:** plays a stretch of a chained film against its narration. `--stills`: the planned
  images, each piece blending from its start to its end image, not-yet-made images as labelled
  grey cards (no clips, no GPU). Default: the owner's chosen takes (`takes.yaml` or the `best_`
  prefix; reused pieces from the base story's `shots/`), others shown as stills and listed, or
  `--any-seed N` captioned UNSELECTED. Planned crossfades and dips are applied at cuts. For each
  chain join between two clips it reports `jump` (last frame vs next first frame), `motion`
  (median frame-to-frame change around the join), their ratio (flagged above 3) and `pace`, and
  writes a join sheet (last frame, first frame, difference).
- **Checked:** `--stills --until 64` on v6 (scenes 1 and 2): 1550 frames at 24 fps = 64.58 s,
  narration 64.60 s, voice from 0.27 s; contact sheet looked at (landscape opening, placeholder
  cards, the sunset crossfade). Takes mode with a temporary `takes.yaml` that put a v5 clip
  before the reused `s01_explores`: the join was flagged (ratio 7.3; Milo jumps from x=0.55 back
  to 0.30), as it should be; test files deleted. Kept:
  `work/stories/lion_and_mouse_v6/review/chain_preview_0-64_stills.mp4`.

### 8. Skills: new `audio-chained-coverage`, section F in `consistent-image-prompts`

- **What:** a new repo skill for planning and checking chained stories (tools table, the planning
  steps: lines and bounds, holds and landscapes, entrances and exits, cut reasons, talking chains,
  reuse, in-frame-only video prompts; new images in a chain; the pilot and join test before the full
  render). The image-prompt skill gets section F: boundary-image review, chain frame edits, landscape
  pieces and `empty_copy`, chained file names.
- **Why:** the owner asked for the skills to carry the new way of working; the consistency rules stay
  in the existing skill and the new one points to them.
- **Files:** `.claude/skills/audio-chained-coverage/SKILL.md`,
  `.claude/skills/consistent-image-prompts/SKILL.md`.
- **Checked:** every command in the new skill's table was run in this session (entries 3 to 7).

### 9. `CLAUDE.md` and `docs/production-guide.md` point to the new way of working

- **What:** `CLAUDE.md`: a v6 bullet at the top of "Current state" (what v6 is, numbers, defaults to
  confirm, where to start, next steps), the lint states found today (Ugly Duckling 22 errors; the v5
  70 errors include v3 `staging_only` references in scene records), three rows in "Where the knowledge
  is" (the new skill and tools, the v6 folder, this change log), the new tools in the layout.
  `docs/production-guide.md` section 9: the narration-first planning and its tools.
- **Files:** `CLAUDE.md`, `docs/production-guide.md`.
- **Checked:** recounted the new image records in `chain_source.py`: 33 total (16 open-mouth,
  3 entrance, 1 empty-trap and 13 beat frames); the totals match `CLAUDE.md`, the v6 README and
  the generated shot plan. `image_prompts.py --story lion_and_mouse_v6 lint` reports 0 errors
  and 0 warnings; `chain_plan.py ... check` covers all 154 pieces and all 11:23.7 with 0 errors;
  `git diff --check` is clean.


### 2026-10-09 — Word-timed mouth animation for chained stories

- Added isolated WhisperX forced alignment and a post-render mouth compositor. The timing comes from the exact line WAVs and dialogue transcript; the compositor uses approved open/closed endpoint images, preserves first/last frames, and stores hash-bound outputs separately.
- Chained previews prefer current lip-sync clips; final edit handoff refuses unsynced `mouth` variants and validates source/output hashes.
- Added reusable workflow documentation and wired Lion and Mouse v6 to align its reused v5 narration and process dialogue takes.
- The compositor currently makes broad syllable-timed openings from one approved mouth shape. It is not phoneme/viseme-accurate and requires visual review.
- Checked Python syntax and CLI help, reviewed commands/docs, and checked the worktree diff. Audio alignment and rendered clips were not generated here because WhisperX and its model are not present in the current environment.


### 2026-10-09 — Production environments and v6 audio preparation

- Prepared the requested checkout in `/scratch/project_465002727/jelealro/feltwillow-production`; this path is the same checkout as the active `/pfs/lustrep4/...` path, so no duplicate clone was needed.
- Installed isolated CPU PyTorch 2.8.0 + WhisperX 3.8.6 and bundled FFmpeg in `.venv-lipsync`; downloaded the English wav2vec2 alignment model.
- Created the LUMI Wan render venv at `/scratch/project_465002727/jelealro/ltx_env/venv` using the configured ROCm container. The Wan 2.2 I2V and Lightning model snapshots were already cached.
- Generated v6 word timings from the v5 English line audio: 161/161 lines and 1,238 words aligned; no review flags.
- `image_prompts.py lint`: 0 errors, 0 warnings. LUMI renderer dry-run reached prompt assembly; a video cannot run until v6 image approvals are exported into runtime `story.yaml` and keyframes. No images or videos were generated.


### 2026-10-09 — Character-only lip-sync enforcement

- Added CR-24 and updated the chained-coverage skill: narrator voice-over never drives character mouths; only audio lines explicitly assigned to one visible character can be lip-synced. Silent narration shots hold the approved mouth pose, and mixed-speaker shots sync only the explicitly selected speaker.
- The readiness check found four unsafe v6 variants: three narrator-only pieces and one piece covering both Leo and Milo. Changed the narrator pieces to silent mouth holds, removed the unused call open-mouth image, and explicitly assigned the mixed close-up to Leo; Milo's line now leaves Leo closed. After checking dialogue-frame scale, wide-shot character lines were set to keep mouths still; the close Leo line gained a separate approved mouth anchor that does not alter chain start/end frames. The final plan has 33 new images, including 16 dialogue mouth anchors.
- Added `mouth_character` to generated endpoint records (required by the compositor), made packet generation reject ambiguous `mode: mouth` speakers, and made the compositor reject missing speaker metadata and always exclude `NARRATOR`/other-character lines.
- Rebuilt v6 prompts and timing sheet; lint reports 0 errors and 0 warnings, and the 154-piece timing plan reports 0 errors.

## 2026-10-09 — Lip-sync boundary and attribution audit

- Fixed selected-variant speaker lookup and stale alignment reuse; narrator and other-character lines cannot provide mouth cues, and changed line recordings fail closed.
- Replanned Lion and Mouse v6 dialogue so all 37 mouth clips have closed chain endpoints and separate open-mouth calibration images. This removes open-mouth boundary poses during silent pauses without adding image jobs.
- Bound synced-take reuse and edit handoff to the current timing, speaker metadata, line audio and approved mouth images. Added checks for open-mouth boundaries and focused attribution tests.
- Regenerated the v6 packet, prompts and timing sheet; v6 prompt lint reports 0 errors/0 warnings and timing covers 11:23.7 with 0 errors. V5 source still regeneration remains unverified because its prompt lint reports 70 errors/8 warnings from missing deleted v3 references. No v6 media was generated.

The owner selected full v6 image regeneration for a later phase. The current 33-new-image packet and carried v5 assets/renders remain an interim audit baseline; image migration and generation await the completed audit report. No images were created during this pass.

## 2026-10-10 — Scene character-scale anchor gate

- Added CR-25: sharp-background scene frames require the same-setup size anchor on both endpoints, kept in the actual provider reference set, plus a measured visual scale and shared-cast ratio check before staging.
- Updated the consistent-image-prompts and audio-chained-coverage skills. Prompt lint now rejects sharp-background scene frames without their setup anchor or when the anchor does not show each visible character; packet builders attach the anchor to generated starts and ends.
- Checked Python syntax and prompt lint behavior; v6 still needs its deleted scene anchors restored or regenerated before its sharp-background frames can pass lint.

## 2026-10-10 — v6 scene scale and ground-contact review

- Added a skill and creation-rule gate that checks actual walkable surfaces, planted foot baselines,
  contact shadows and support; water, flowers and bush canopies are not standing surfaces by default.
- Reset v6 wide/two-character Milo scale to the size selected in the scene-1 review image (0.21 of
  frame height), and rebuilt the rendered image prompts. Close-up crops retain their framing.
- Re-review and regenerate wide-frame candidates for scale, ground contact and paired-character
  continuity before presenting the revised scene set.


## 2026-10-10 — Adopted spatial staging and grounding policy

- Added `docs/spatial-staging-consistency.md` as the standing policy for walkable support, character grounding, depth-aware scale, landmark placement, occlusion and continuity.
- Linked the policy from creation rules, prompt guidance, the image-prompt and chained-coverage skills, the repository audit prompt, and the v6 story README.
- Added all required spatial metadata to the eight v6 location masters and registered their composition-master records. Accepted the empty location seeds after consistency review.
- Derived stream sunset and great-tree daytime candidates directly from their accepted masters; both remain in `.review` for owner approval.
- Corrected Milo's turnaround proportions against the approved neutral canonical, retained the elongated prior version under `references/superseded/`, and updated the foundation review.
- Checked JSON validity, image dimensions, and `git diff --check`; no scene frames, audio, or video were created. The LUMI handoff was left untouched per the owner's earlier instruction.
