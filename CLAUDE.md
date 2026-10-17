# CLAUDE.md: operating manual for agents working in this repo

Read this first. It is the durable memory of the project: what it is for, how
to run things on LUMI without repeating past failures, and where the knowledge
lives. Keep it current: when you learn something that would have saved you
time, add it here or to the doc it belongs in. Order: current state and
standing rules first, reusable guidance next, dated history at the end (where
history and the sections above differ, the sections above win).

## What this repo is

**Feltwillow**: felt-animal fables for children, each with a
kind message, for the monetised YouTube channel of the same name (Made for
kids). Pictures: open video models (Wan 2.2) on the LUMI supercomputer animate
approved still images; the v4 stills were made with GPT's built-in image tool
and the Gemini API (2026-09-30 to 2026-10-02) and are now made by the owner.
Narration and character voices: Gemini 3.8 Flash TTS (`voice/`). Music and
sound effects: none used yet; ElevenLabs is the option kept for later (needs a paid
plan at generation time, see `docs/licensing.md`). Final mix: DaVinci Resolve
(owner).

Repo: `/scratch/project_465002727/jelealro/feltwillow-production` on LUMI
(renamed from `twc_video` on 2026-09-27 and from `big_lessons_little_tales` / Big Lessons, Little
Tales to `feltwillow-production` / Feltwillow on 2026-10-07: package `bllt/` -> `feltwillow/`, settings
`BLLT_*` -> `FELTWILLOW_*`, Slurm job names `bllt_*` -> `feltwillow_*`; `work/` sidecars and git history
keep the old names; GitHub
`jeilealr/feltwillow-production`, private). Cloud sessions check the same
repo out elsewhere (e.g. `/home/user/feltwillow-production`) without
`work/`, the LUMI venvs or Slurm. Current independent Lion and Mouse version: **v6**. All 96 current keyframes are present and owner-selected; technical validation remains pending. Milo uses the owner-selected rebuilt r03 reference atlas and r02 full-body master; the hunter-net design is approved. Read `stories/lion_and_mouse_v6/README.md` and `owner_visual_acceptance.json` for the current handoff and exact selection hashes. See `docs/keyframe-regeneration.md` for the portable reference contract and staged compositor. v5 is retained as separate visual/render production history. Its visual assets, timing plans, clips and renders are not v6 inputs. The exact unchanged English line recordings are the owner-authorized exception: source provenance is v5, runtime copies are staged under the v6 work namespace, and `stories/lion_and_mouse_v6/audio_manifest.json` records the hashes. Ugly Duckling v1 Scenes 1–9 have 126 reviewed render takes; further image and reference issues remain open.
**Cleanup 2026-10-06 (owner):** Lion and Mouse v2, v3 and v4 (stories, character and location
folders) were deleted; they remain in git history (`git show b880c23:<path>`). v4's working records
(`visual_bible.json`, `prompt_manifest.json`, `dialogue_coverage.json`, `timing_plan.json`,
`SCRIPT_REVIEW.md`, `SHOT_PLAN.md`, `TIMING_SHEET.md`) now live in `stories/lion_and_mouse_v5/` with
`lion_and_mouse_v4` paths rewritten to `lion_and_mouse_v5` (v5 images keep v4's file names and
revisions). Not carried over: v4 README, REPAIR_PLAN, GENERATION_PROGRESS, `revisions/`. The tools
used only by v1-v3 or never used were removed too: `production/install_pack.py`, `design.py`,
`compose_keyframes.py`, `edit_image.py`, `character/character.py`, `lora/`, the musubi and Qwen
venv scripts (`lumi/env_musubi.sh`, `env_qwen.sh`, `setup_env_qwen.sh`, `download_musubi_weights.py`,
`convert_dit_bf16.py`) and `docs/reviews/`. `shot.py` still accepts `lora:` and `compose:` (keyframe.py).
`image_prompts.py --story lion_and_mouse_v5 lint` now reports 70 errors, all missing v3 reference
images (deleted history): named by the v4 expression records and, as `staging_only`, by scene
records s10 to s14 (checked 2026-10-08); they matter only for regenerating those images. Plus 8
warnings for owner-renamed v5 files; renders use `export_runtime.py --images`.
Sections below that name v2-v4 paths describe history.

**Temporary run location (owner, 2026-10-16):** Use
`/scratch/project_465002727/jelealro/tmp` for temporary scripts, environments,
logs and run files instead of `/tmp`. Set `TMPDIR` to that scratch directory
for new runs. Project assets and review receipts still belong in the repo.

## Current state (2026-10-16)

**Lion and Mouse v6 — current selection and integration complete:** All 96 keyframes are active, exactly one PNG per frame ID. After the earlier perceptual-world selection (41 replacements, 55 retained), the owner preferred integration trial C and authorized its rollout. 47 slots now use focused finishes (one individually owner-preferred trial and 46 agent-selected under that authorization); 49 retain original bytes. The exact active selection and its basis are in `stories/lion_and_mouse_v6/owner_visual_acceptance.json`. Current comparison, original hashes and processing receipts are in `review/integration_finish/`; original composites are preserved under `interactions/sources/integration_originals/`. The 16 current sheets are rebuilt. Technical approval remains separate. Earlier completed review files were cleaned with a recovery manifest in `image_sources/`. Read the story README and `docs/character-background-integration.md`; start a new scoped review instead of rerunning completed adoption builders.

**Milo follow-up (2026-10-17):** A new neutral r03 identity master is a candidate derived solely from the owner-preferred `s04x_p01`; current r02 remains the approved identity authority. Review `stories/lion_and_mouse_v6/review/milo_scene04_identity_and_lighting/owner_review.html`. The separately requested face-lighting artifact repair is active as `s04_p02_r14_candidate.png`, with r13 preserved and its smooth illumination-only recipe recorded. Do not infer approval of the new identity candidate from the lighting correction. Broad frozen face masks can create bright ovals; inspect native lighting transitions as well as exact pixel support.

Milo uses the selected r02 full-body master and r03 atlas. Use an existing atlas pose first, preserve compact anatomy and no visible teeth. V6 same-depth Milo/Leo standing-equivalent ratio is 0.25 (review range 0.22–0.28); historical v4 ratios below do not apply. `s07_p01` is a shared-composition example. Preserve the scoped s09_p02 scale exception and the explicitly retained tiny-Milo s12_p04 wide. Scene 15 keeps Milo left and Leo right. Close-ups retain full head/ears/mane and upper chest; expression-only edits freeze the body and camera. Preserve Scene 16's selected closing expressions, stable net topology and gnawing on the main knot.

Technical authority, staging/anatomy and measured-scale evidence remains pending, separately from completed owner selection. Read `regeneration_authority_blockers.json` or rerun the gates for current counts. Selected composition receipts describe the chosen image; older planned staging must be reconciled before further generation. No v6 video takes or assembled edit exist. Follow `RUNTIME_CONTRACT.md` before timing/export; do not fabricate review evidence.

The exact 161 unchanged v5 English line WAVs and 16 assembled scene tracks (11:23.7) are owner-authorized v6 inputs, with hashes in `audio_manifest.json`. Do not reuse v5 visuals. A fresh clone needs ignored `work/` audio restored from the workstation/backup/LUMI, plus separately provisioned runtime environments, weights and credentials. The story README records the handoff, visual rules, validation commands and cleanup receipts. Prior chat is not needed for those recorded decisions.

- **Dialogue lip sync (CR-23/24):** for narrated stories, align the finalized line audio to its transcript and apply timed mouth motion after selecting video takes. This is a required workflow for new projects, including Lion and Mouse v6. The current implementation is for chained stories and creates word-timed, broad syllable pulses with approved open/closed mouth shapes; it is not phoneme-level viseme synthesis. Only the explicitly assigned character speaker is animated; `NARRATOR` voice-over never drives character lips, and ambiguous speakers fail closed. Read `docs/lip-sync.md`; final chained edit export rejects dialogue mouth clips without a current hash-bound sync output.

- **Superseded v6 carryover plan (2026-10-08):** the interim packet that reused v5 visual assets or renders is historical and not operative. Its audio reuse was subsequently authorized as exact unchanged English recordings with v6-local runtime copies and manifest hashes. Current v6 status is in `stories/lion_and_mouse_v6/README.md` and `KEYFRAME_REVIEW.md`; the original dated decision record remains in `docs/changelog.md`.
- **Ugly Duckling lint state:** the later 2026-10-09 audit found 22 missing-reference errors across 18 distinct files (`.review/` raw files and `review/reference_boards/*_character_guide.png`). Earlier zero-error lint results are historical. Re-run lint after restoring exact references or revising dependent records.

**Other version-local work:** the Ugly Duckling v1 scene images and any Lion and Mouse v5 take selection remain confined to their own story versions.
The v4-named bullets further down — **V4 stills**, **Open image issues**, and
**Video and audio** ("no v4 clips") — are retained as **history**: v2–v4 were
deleted (recover from git history, `git show b880c23:<path>`) and v5 clips are
rendered. The guidance bullets (creation rules, prompt templates, per-story
image folders) remain current.

- **Superseded instruction (2026-10-09; superseded 2026-10-11):** the owner asked for an audit before creating v6 images. The later owner request authorized and produced the 92 v6 candidate keyframes listed above. This dated instruction is history, not a present prohibition on their existence or review.
- **Ugly Duckling v1 scenes:** at the owner’s direction, scene keyframes through Scene 10 are generated with built-in ImageGen and saved at manifest targets; all remain pending owner review. Scene 06 has 14 active frames across 6 shots after the owner split `s06_ottie_finds` into a burrow-watch shot and an approach/help shot. The owner renamed the help image to `s06_ottie_approaches_end_r01.png` and duplicated the original start as `s06_ottie_finds_end_r01.png`; the earlier generated hold-end is superseded. Scene 06 contact sheet: `stories/ugly_duckling_v1/review/contact_sheets/scene-06_contact_sheet.png`; Scene 07’s four frames and contact sheet are `stories/ugly_duckling_v1/review/contact_sheets/scene-07_contact_sheet.png`. Scene 08’s six keyframes are generated and pending owner review at `stories/ugly_duckling_v1/review/contact_sheets/scene-08_contact_sheet.png`; its empty spring start is copied from the locked plate, goodbye and flight mouths are closed per shot descriptions. The goodbye prompt’s “snow has nearly melted” state conflicts with the fully snowy locked winter plate and needs owner review. Scene 09’s seven keyframes and contact sheet are `stories/ugly_duckling_v1/review/contact_sheets/scene-09_contact_sheet.png`; its swan lake start/end face in different directions. Scene 10’s ten keyframes and contact sheet are `stories/ugly_duckling_v1/review/contact_sheets/scene-10_contact_sheet.png`; the reflection end is a clear vertical mirror, speech mouth keys are separate from closed-bill expressions, and the swim-together start explicitly keeps all three bills closed. Scene 12’s four frames are generated and pending owner review at `stories/ugly_duckling_v1/review/contact_sheets/scene-12_contact_sheet.png`; bills and mouths are closed per the video variants. Because `s11_ducklings_sorry_end` is missing while Scene 11 is paused, `s11_arrives_home_start` served only as the first Scene 12 frame’s size anchor, with the locked pond plate and canonical-only identity board attached. Scene 11 was started, then paused when the owner identified a head-shape mismatch between Ollie the swan’s canonical and expression/mouth references. An r02 canonical candidate and comparison sheet are staged in `character/characters/ugly_duckling_v1/OllieSwan/canonical/.review/`; generated Scene 11 keyframes must be redone after canonical approval, and `os_open_r01.png` currently duplicates the closed happy expression pending a proper open-mouth replacement. The superseded `s06_ottie_stays_end_r01.png` target file was removed at the owner’s request; its manifest record and raw `.review` source remain for provenance. `s09_ollie_bows_start_r01.png` remains active because the video and end frame use it. Local lint on 2026-10-11 is 0 errors and 0 warnings because ignored reference files exist on this machine; a clean tracked clone still lacks those inputs. Details and outstanding review are in `stories/ugly_duckling_v1/README.md`.
- **Ugly Duckling Scene 03 pond continuity:** on 2026-10-07 the owner flagged pond/nest drift and directed all six frames in `to_the_water`, `ollie_glides` and `honk` to be deleted and recreated. The old files are archived in `character/characters/ugly_duckling_v1/interactions/keyframes/.review/s03_background_drift_before_recreation/`; six replacements were generated with `pond_day_r01.png` attached and saved to the active manifest targets. Their landmarks are visually consistent across the sequence but small background redraw/crop differences remain because ImageGen does not pixel-lock a supplied plate. They are pending owner review; see `stories/ugly_duckling_v1/review/contact_sheets/s03_pond_keyframes_recreated_2026-10-07.png` and `stories/ugly_duckling_v1/README.md`. For exact plate preservation, composite character layers onto the original plate.
- **V4 stills** (counted from `stories/lion_and_mouse_v4/prompt_manifest.json`):
  140 image records, the 118 planned ones (32 foundation: 2 canonicals,
  18 references, 10 plates, 2 props; 86 scene start/end frames) plus 22
  expression studies (`M_EXPR_*`/`L_EXPR_*`, 11 per character). 139 are
  `accepted` and on disk; `s02_place_acorn_end` is
  `missing_after_owner_review` (the owner deleted its r02; later attempts were
  rejected). The `s02_place_acorn_end_r01.png` still on disk is the
  owner-rejected r01: never use it as a reference. "Accepted" means an agent's
  visual review, not owner approval: 63 records still read
  `accepted_pending_owner_review`; the owner reviews them directly (`IMAGE_REVIEW.md`
  was deleted on 2026-10-02).
  Record revisions: r01 94, r02 30, r04 10, r05 6 (r03 was superseded).
  Superseded files were pruned; each record keeps their provenance under
  `superseded`. Tools: GPT's built-in image tool for r01 and the in-place
  repairs after r05; the Gemini API (`character/gemini_image.py`) for r02 to
  r05 and the expressions (214 images, about $13.9 estimated, in
  `revisions/gemini_ledger.csv`).
- **Open image issues** (2026-10-02 audit; owner decisions): the missing S02
  end; S13 Milo framing and size (`s13_milo_confident_*`/`s13_milo_playful_*`
  are `dialogue_close_up` records whose r04 images are wide two-shots with
  Milo about 0.35 of the frame high, while `s13_arrives_*` shows him at about
  0.25 with the same camera and baseline); the v4 Leo-to-Milo ratio was **decided on
  2026-10-02: Milo standing = 0.55 of Leo's mane height** (bible `cast_scale`,
  lineup frame `s05_nose_aftermath_start`); the S13/S14 trap frames, S14 gnaw
  shots, S05/S06/S08 wides and S16 no longer match it. Details: "Open issues" in `stories/lion_and_mouse_v4/README.md`.
- **Video and audio:** no v4 clips, take selections, runtime `story.yaml` or
  GPU task files exist. The English narration was rendered on 2026-10-02 (see
  Voices); `TIMING_SHEET.md` maps its lines to 42 of the 43 coverage shots
  (`s02_place_acorn` is unused there).
- **Still true from the documentation phase:** no render tool
  (`production/shot.py`, `keyframe.py`, `compose_keyframes.py`, `animatic.py`)
  reads `visual_bible.json` or `prompt_manifest.json` (checked 2026-10-02);
  their gates are manual. The known tool gaps (bbox-based pose sizing, stale
  caches, additive negatives, fast-take continuation, animatic fallback) are
  listed in `docs/v4-preflight.md` as read on 2026-09-30; re-check the current
  code before relying on them. Do not mistake planned paths or checked historical
  file lists for approval. Preserve v3 inputs/results. Prompts reduce
  ambiguity; only inspection of actual outputs can establish that a defect is
  fixed. `GENERATION_PROGRESS.md` is a dated log: its "Resume order" and
  "continue with the next record" lines predate the current instruction.
- **Prompts are templates (2026-10-02, CR-18):** every v4 prompt is rendered from
  `visual_bible.json` (canonical identities with hex colours, measured setup sizes with
  anchors, plates, shared blocks) by `production/image_prompts.py`; `lint` reports 0
  errors. Edit the bible or a record's template, never a rendered prompt; `revisions/*.json`
  are history. Each prompt names its attached references and their roles.
- **Before any new image** (whoever makes it): read `docs/creation-rules.md`
  from CR-11 on. CR-13: whole bodies, side-by-side identity gate, edit an
  approved same-setup frame instead of regenerating a character, scale as
  frame fractions, V3 images staging-only, continuity cascades. CR-14,
  CR-16 and CR-18: sizes as frame fractions from the bible's `setups`, with one
  v4 story-wide lineup (Milo = 0.55 of Leo's mane height; this is historical for v6); dialogue close-ups in the `s15_leo_reflects` format with faces from
  `character/characters/lion_and_mouse_v4/<Name>/expressions/`. CR-15: every scene record has
  `framing` (`dialogue_close_up` / `close_two_shot` / `scene_wide` /
  `empty_plate`); follow its close-up recipe. CR-17: freeze the setup first,
  repeat the full identity in every prompt, review against canonical, lineup,
  previous shot and plate.
- **V5 images (owner, from 2026-10-02):** the owner makes a second still
  iteration by hand. Folders mirror v4: `character/characters/lion_and_mouse_v5/{Leo,Milo}/`
  (canonical, references, expressions), `character/characters/lion_and_mouse_v5/interactions/keyframes/`,
  `character/locations/lion_and_mouse_v5/<place>/`; each v5 root has a README with the file name for
  every record (same stem as v4, `_r01`). Prompts are still the v4 records.
- **Image folders are per story (2026-10-04, owner):** `character/characters/<story>/<Name>/`,
  `character/characters/<story>/interactions/`, `character/locations/<story>/<place>/`, with
  `<story>` = the `stories/` slug (Lion and Mouse: `lion_and_mouse_v2` to `_v5`; v3 plates in
  `character/locations/lion_and_mouse_v3/`). All references in stories/, docs and code were
  rewritten (one-off script, 6,778 references in 92 files); `work/` sidecars keep old paths.
- **Scene keyframe file names carry per-scene chronological order (owner, 2026-10-08; CR-20):**
  opt-in per story via bible `"keyframe_chrono_naming": true`. Each scene keyframe file is
  `sNN_CC_<shot-name>_<start|end|open>_rNN.png`, `CC` restarting at 01 each scene in shot order,
  so the stills sort in story order on disk. Only the file name changes; record `id` stays
  `<shot>_<which>`. `story_packet.py` sets the flag and emits these names for every new story;
  `image_prompts.py lint` enforces them when the flag is on. Lion and Mouse v5 is converted (flag
  on); Tortoise/Boy-Who-Cried-Wolf/Ugly-Duckling are grandfathered (flag off, old names) until
  the owner asks to convert them. Out of scope: `work/` review videos (git-ignored) and per-line
  narration audio (`SNN-LNNN.wav`, already ordered).
- **V5 clips (owner request 2026-10-04):** runtime story `stories/lion_and_mouse_v5/story.yaml`,
  generated by `production/export_runtime.py` from the v4 manifest's 62 video variants and the
  v5 images (frozen copies in `work/stories/lion_and_mouse_v5/keyframes/`, hashes in
  `runtime_inputs.json`); `shot.py` uses its `prompt:`/`negative:` verbatim. Prompts 124-346
  umT5 tokens (limit 512, none truncated). Rendering in fast mode, 3 seeds each, with
  `lumi/render_story.sh lion_and_mouse_v5` (log `$FELTWILLOW_PROJECT/tmp/render_v5.log`); clips in
  `work/stories/lion_and_mouse_v5/shots/`. Owner selects takes; no animatic.
  **Initial batch done 2026-10-05 09:31: 186 clips** (62 shots x 3 seeds);
  a later three-seed `s05_tumble` bridge makes 189 historically expected. Review in
  `stories/lion_and_mouse_v5/RENDER_REVIEW.md` (contact sheets `work/.../review/sceneNN.jpg`).
  Measured: ~30 min model load per `shot.py` call, median 9.2 min per fast seed (the first
  jobs ~17); 3 shots per task line can overrun 3 h, the catch-up round finished the one late
  shot. Finding: in fast mode (CFG 1) naming an absent object pulls it in ("the overhead branch
  stays empty", "paws stay outside the portrait" put a branch, leaves and paws into the S15
  close-ups): describe only what is in frame.
- **Bridge shot `s05_tumble` (owner, 2026-10-05):** the cut `s05_paw_contact` -> `s05_nose_aftermath`
  jumped Milo from the paw to the nose. Added to the v4 manifest as a shot with `"bridge": true`
  (start = `s05_paw_contact_end`, end = `s05_nose_aftermath_start`, no new images; lint skips the
  image-pair rules for bridge shots); Leo wakes only in `s05_nose_aftermath`. Scene 5 lines in
  `dialogue_coverage.json` now map in story order (L001-4 sleeps, L005-7 paw, L008-9 tumble,
  L010-11 eyes open). `timing_sheet.py` takes `--audio-story lion_and_mouse_v5` (the v4 audio's
  folder).
- **Ugly Duckling voices (owner, 2026-10-06):** cast in `stories/ugly_duckling_v1/voices.yaml`
  (narrator Cheery Tale Keeper 2; Ollie, Ottie and three duckling designed voices in
  `voice/cast/ugly_duckling_v1/`; Mama = prebuilt Gacrux, Swan = prebuilt Algieba, used by name).
  Ducklings: one voice, duckling_3 (the three voices spoke at different speeds; chosen by pitch
  and steady pace); the unused takes are in `lines/unused_duckling_voices/`.
  `narrate_scenes.py --voices-file`; a speaker with a list of voices gets one file per voice
  (`lines/<ID>_v1.wav`...) and a mix in the scene file. Narration rendered 2026-10-06 (65 lines, 73 calls, 10.1 min; TIMING_SHEET.md built) into
  `work/stories/ugly_duckling_v1/audio/en/`.
- **Ugly Duckling clips, scenes 1-9 (owner, 2026-10-06):** runtime story
  `stories/ugly_duckling_v1/story.yaml` from `export_runtime.py --manifest
  stories/ugly_duckling_v1/prompt_manifest.json --story ugly_duckling_v1 --scenes 1 ... 9`
  (no `--images`: the manifest targets are the files; seeds 1-3 and 1280x720 by default):
  33 shots, 42 clips, 126 takes, rendered by `PER_TASK=2 lumi/render_story.sh ugly_duckling_v1`
  (log `$FELTWILLOW_PROJECT/tmp/render_ugly_duckling.log`). Fixed on the way: the
  `s06_ottie_finds_closed_r01` clip pointed at the superseded `s06_ottie_stays_end`. Scenes 10-12
  wait for images; rerun the export with all scenes, then the same driver (it skips done takes).
  **Done 2026-10-07: 126 takes**; review in `stories/ugly_duckling_v1/RENDER_REVIEW.md` (sheets
  `work/stories/ugly_duckling_v1/review/sceneNN.jpg`). Finding: several `_closed` close-ups open the beak
  mid-clip (prompts saying "speaks", and fast-mode drift); `s04_decision_closed` throws its wings up.
- **Next stories (owner, 2026-10-04), narration 7-10 min each, narrator reused
  for now:** *The Tortoise and the Hare* (`stories/tortoise_and_hare_v1/`: 84 lines,
  about 9 min, 42 shots, 141 image records) and *The Boy Who Cried Wolf*
  (`stories/boy_who_cried_wolf_v1/`: 78 lines, about 8.5 min, 46 shots, 171 image
  records, gentle ending); *The Ugly Duckling* (`stories/ugly_duckling_v1/`: 65 lines,
  about 7.7 min, 43 shots, 153 image records; two Ollie canonicals, cygnet and swan).
  Documentation packets ready, lint 0 each.
- **Open-mouth key frames for readable dialogue close-ups (owner, 2026-10-05; CR-19):** because Wan only
  interpolates between a clip's two key frames, every readable dialogue close-up with a `mouth` variant in
  these three stories now has a `<shot>_open` record — an edit of the closed start frame that opens
  only the mouth to the character's one approved `*_OPEN` speech shape — and the `mouth` variant
  ends on it (per-variant `start_image`/`end_image`). So the open mouth stays identical across
  renders instead of being invented each time. Added 13 (Ugly Duckling), 15 (Tortoise and Hare) and
  17 (Boy Who Cried Wolf); `production/story_packet.py` emits them for future stories. Lion and
  Mouse v4/v5 are deliberately excluded (clips nearly final). The Ugly Duckling script and shot
  order were approved by the owner on 2026-10-05; the owner asked the agent to
  create the canonical images using built-in OpenAI `image_gen` (Gemini optional).
  `SWANS_CANON`, `OLLIE_SWAN_CANON`, `OTTIE_CANON`, `MAMA_CANON`, `OLLIE_CANON`
  and `DUCKLINGS_CANON` are owner-approved. Their identities were rewritten in
  the bible and prompts rebuilt. `LINEUP` is owner-approved and measured; the cast scale and all setup sizes
  were updated. `O_SWIM` and `O_WALK_R` were created at the owner’s direction and await review. At the owner’s latest direction, all 23 remaining foundation records from `stories/ugly_duckling_v1/prompts/foundation.md` (six pose studies, ten mouth studies, seven plates) were generated at their manifest targets and await owner review. After the owner flagged pond-scene drift, pond morning/day were revised as direct lighting edits from the sunset master; the owner renamed the corrected files to r01 and scene references now target those files. The original morning plate had no image reference and later times were separately regenerated from it. CR-06 and the image-prompt skill now require each first approved location plate to serve as the explicit master for all variants. Contact sheets are at `stories/ugly_duckling_v1/review/foundation_characters_contact_sheet.png`, `.../foundation_plates_contact_sheet.png` and `.../expressions_contact_sheet.png`; all 22 expression records were generated at manifest targets from their ordered closed-mouth portrait and canonical references and are pending owner review. Prompt rebuild and lint pass (0 errors, 0 warnings). The Gemini API is an
  optional image provider, not the default; `character/gemini_image.py` now
  accepts `--story <slug>` when the owner selects Gemini. Tortoise and Hare and
  Boy Who Cried Wolf still await CR-01 review. Start from each story's README.
- **Next:** owner reviews all generated Ugly Duckling foundation and expression images and their three contact sheets. When approved, continue with the next production step in story order. When asked, derive the runtime story and render a small clip pilot
  (`docs/v4-preflight.md` gates C-E).

## The owner's standing instructions

- Goal: professional, consistent videos (same characters and places across
  shots). Iterate until the result is genuinely good; show evidence (contact
  sheets) for every judgement.
- Everything used must be **licence-clean for a monetised channel**. Check a
  model's licence or service terms before using it; record it in
  `docs/licensing.md`. Rejected so far: HunyuanVideo (excludes the EU),
  MusicGen (CC-BY-NC), Stable Audio Open (revenue cap), RMBG 1.4/2.0
  (non-commercial); ElevenLabs-voice clones (third-party voices).
- **Git: the owner does all git** (add, commit, push). Agents do not run git
  commands unless the owner explicitly asks in that session (owner,
  2026-09-27). Such a request covers that one commit or push; it does not
  change this rule. Leave the tree ready for
  `git add . && git commit && git push`.
- **Historical owner task (2026-10-02, superseded by later v6 requests):** the owner created v4 images personally;
  agents did not generate images, clips, audio or GPU jobs without a request (see
  "Current state"). Also superseded: the 2026-09-30 task
  (documentation first for v4, no images, video or audio; read the complete v3
  notes and v4 repair plan; owner reviews script/shot sequence before the next
  images) and the earlier 2026-10-02 task (finish and repair v4 still images
  under the manifest with the built-in image generation tool; preserve v3
  assets; no clips, runtime YAML, animatics, audio or GPU jobs; replace pruned
  frames at the active manifest target without accumulating revisions, now
  CR-17). Both were carried out (r01 to r05).
- Milo's v4 crown has no separate top tuft. The old smaller-tuft fixes and v3
  sheet are superseded for v4. All derivatives must follow the approved new
  canonical, with brown eyes and slender proportions; Leo retains the full
  canonical rust-orange mane. Never mix v3 identity text into v4 prompts.
- For this and every future story, freeze prop-free character canonicals and
  a same-depth cast size lineup before scene images. Lock each location plate
  and camera. Record actor head/mane and full-body frame boxes, baseline and
  depth for each setup; compare adjacent shots and paired endpoints at the
  same depth. A pose change cannot shrink a head or mane. Repeat every visible
  character's complete identity, anatomy counts, size anchor and prop state
  in every individual prompt, even when repetitive. Review saved images
  against canonicals, the size lineup, prior scene and exact plate. See
  CR-16 and CR-17 in `docs/creation-rules.md` and `docs/v4-preflight.md`.
- Render individual clips first. Owner reviews/selects exact takes; assembly
  is a separately requested job afterward. Never auto-run an animatic after
  each batch, and never use a default `take` as evidence of owner selection.
- Fast Lightning uses CFG 1 with no negative conditioning pass. Write critical
  desired states positively and encode them in anchors; exclusions remain review
  criteria. Check actual runtime prompt token length and truncation before jobs.
- Every image/edit and video mode gets its own full expanded prompt record,
  reference roles, revision, pair/state checks and later actual execution log.
- Only run GPU jobs when you are sure they are ready: dry-run first (see
  "Before a GPU job").
- Keep the docs as a guide a person can learn from: why, measured results,
  images.
- Voices: one sample line per voice only; do not generate audio the owner has
  not asked for.

## Where the knowledge is

| Need | Read |
|---|---|
| **Rules for scripts, images and shots (start here)** | **`docs/creation-rules.md`**: the one guide to read before writing a script, generating an image or describing a shot |
| **Writing or changing an image/video prompt; starting characters and places** | **`.claude/skills/consistent-image-prompts/SKILL.md`** branches by pipeline. Manifest-backed stories use `docs/image-prompts.md` and `production/image_prompts.py`; current v6 uses its keyframe/staging plans and visual gate. CR-18 and CR-29 apply to both. |
| **Video as long as narration; boundaries and strict joins** | **`.claude/skills/audio-chained-coverage/SKILL.md`** branches by pipeline. Current v6: `staging_contract.py`, `keyframe_visual_gate.py`, `v6_runtime.py --preflight`. Legacy manifest chains: `chain_plan.py`, `chain_preview.py --require-takes --fail-on-flagged-joins`, `chain_repair.py`, `edit_manifest.py`. `chain_packet.py` is retired. |
| Lion and Mouse (v6): candidate review, second-image audit, setup-anchor selections, regeneration contract, boundaries and runtime preflight | `stories/lion_and_mouse_v6/README.md`, `KEYFRAME_REVIEW.md`, `README.md`, `VIDEO_BOUNDARIES.md`, `RUNTIME_CONTRACT.md`, `docs/audits/lion-and-mouse-v6-second-image-audit-remediation-2026-10-13.md`, `docs/audits/lion-and-mouse-v6-size-anchor-review-2026-10-13.md`, `docs/keyframe-regeneration.md`; candidates in `character/characters/lion_and_mouse_v6/` |
| Why a rule or tool changed (dated, with checks) | `docs/changelog.md` |
| Lion and Mouse (v5): script, shot order, readable prompts, render review | `stories/lion_and_mouse_v5/`: `SCRIPT_REVIEW.md`, `SHOT_PLAN.md`, `prompts/*.md`, `RENDER_REVIEW.md` |
| Identity, camera setups, size anchors; image/video records | `stories/<slug>/visual_bible.json`; manifest-backed stories use `prompt_manifest.json`, current v6 uses its keyframe/staging/boundary plans |
| V4 image history (deleted 2026-10-06, in git history) | `git show b880c23:stories/lion_and_mouse_v4/GENERATION_PROGRESS.md`, `.../revisions/` |
| Prompt provenance and review gates | `docs/prompt-records.md`, `docs/v4-preflight.md` |
| **Image generation**: default ImageGen rules in the repo skill; optional Gemini workflow and history | **`.claude/skills/consistent-image-prompts/SKILL.md`**, `docs/gemini-images.md`, `character/gemini_image.py` |
| Narration timing: which shot covers which line | `stories/<slug>/TIMING_SHEET.md`, `timing_plan.json` (audio on LUMI under `work/`) |
| Writing any shot prompt, with evidence | `docs/prompting.md`: every measured rule, a checklist, results log |
| Every problem found and its fix; gaps and risks | **`docs/findings-and-risks.md`** |
| The whole pipeline, story to shots | `docs/production-guide.md` |
| Voices (Gemini TTS) | **`voice/README.md`** |
| Handing a story to publishing (separate repo `jeilealr/feltwillow-publishing`) | `docs/publishing-handoff.md`, `production/export_handoff.py`, `production/contracts/README.md` |
| LUMI jobs, times, solved gotchas | `docs/lumi.md` |
| Licences and service terms | `docs/licensing.md`, `docs/google_gemini_terms_question.md` |
| Where code came from | `docs/provenance.md` |
| Story facts and runtime export | the bible and manifest are the authority; the runtime `story.yaml` is exported from them by `production/export_runtime.py` |
| The owner's story text | `stories/<slug>/SCRIPT_REVIEW.md` (or `SCRIPT.md`) and its line list `dialogue_coverage.json` |
| Character, scene and location images | `character/characters/<slug>/<Name>/`, `character/characters/<slug>/interactions/keyframes/`, `character/locations/<slug>/` |

## Layout and paths

```
stories/<slug>/     visual_bible.json, prompt_manifest.json, dialogue_coverage.json, prompts/,
                    runtime story.yaml + runtime_inputs.json (exported), voices.yaml
production/         image_prompts, story_packet, export_runtime, shot, keyframe, timing_sheet, animatic,
                    chain_plan, chain_packet, chain_preview, chain_repair, edit_manifest (chained stories, CR-21)
character/          gemini_image.py (optional Gemini stills);
                    one folder per story (since 2026-10-04): characters/<story>/<Name>/ and
                    characters/<story>/interactions/ (scene frames), locations/<story>/<place>/
voice/              Gemini TTS tools; cast/<role>/ and narrators/<name>/ (voice.yaml + samples)
feltwillow/               package: paths, media (ffmpeg), wan (model wrapper), post (RIFE/ESRGAN/grade)
lumi/               site.sh, env.sh, run_in_container.sh, run_tasks.sbatch, task_exec.sh, render_story.sh, setup_env.sh
docs/               guides; docs/img/ evidence images
work/               everything generated (git-ignored); every output has a .json sidecar
```

- **Paths never depend on the repo's folder name.** Python derives them from
  `feltwillow/paths.py` (`REPO`, `WORK`, `story_work(slug)`, `story_audio(slug,
  lang)`); shell scripts from `lumi/site.sh`, the only file with
  machine-specific locations (project dir, venvs, HF cache, container, Slurm
  account, log dir). Moving or renaming the repo needs no edit; another
  machine or project needs `lumi/site.sh` plus the `#SBATCH` account/output
  lines in `lumi/run_tasks.sbatch`.
- **Everything runs from the repo root.** `run_in_container.sh` cd's there;
  task-file lines are written relative to it (`python production/shot.py ...`);
  submit `sbatch` from the repo root (the script checks).
- Per-story generated files: `work/stories/<slug>/` = `design/` (plates,
  props, installed canonicals), `characters/<name>/` (pack, pack16x9, poses,
  shots), `keyframes/`, `shots/`, `audio/<lang>/sceneNN.wav` (narration, for
  the animatic), `animatic*.mp4`. Task files: `work/tasks/` (old ones in
  `work/tasks/archive/`, with pre-rename paths). Old LoRAs (v1/v2 characters): `work/lora/`.
- V4 images are not in `work/`: they are tracked PNGs under `character/`
  (allowed by `.gitignore`). Gemini candidate takes (`character/**/gemini/`)
  are git-ignored.
- Outside the repo (in `$FELTWILLOW_PROJECT`, `/scratch/project_465002727/jelealro`):
  venvs `ltx_env/venv` (generation; legacy name, do not move: venvs hold
  absolute paths), `gemini_env/venv`; `hf_cache/`, `slurm_logs/`. Left over from
  the removed LoRA tools: `musubi_env/`, `models/`, `ext/musubi-tuner`.

## Running things

```bash
cd /scratch/project_465002727/jelealro/feltwillow-production
W=lumi/run_in_container.sh                     # LUMI PyTorch ROCm container + venv
$W python production/shot.py --story lion_and_mouse_v5 --scene 1 --shot s01_explores --fast --dry-run
source voice/gemini_env.sh && python voice/list_voices.py   # voices, no container
```

- **One container venv** + one plain venv. `ltx_env/venv`:
  diffusers 0.39, transformers 4.51 (generation, keyframes, post).
  `gemini_env/venv`: google-genai, outside the container.
  `character/gemini_image.py` needs only Python 3 and Pillow
  (`docs/gemini-images.md`).
- Pass `--story` explicitly: some tools default to v2 or v3.
- **GPU work = a task file + `lumi/run_tasks.sbatch`**, one command per line,
  one GCD each, from the repo root:
  `sbatch --ntasks=3 --gpus-per-node=3 --mem=330G lumi/run_tasks.sbatch work/tasks/<name>.txt`
  Logs: `$FELTWILLOW_LOGS/feltwillow_tasks_<job>_<task>.log`.
- **Fast mode (Wan2.2-Lightning, `--fast`) is the default way to iterate**:
  ~9-16 min per clip instead of ~2 h 10, same look (docs/prompting.md "Fast
  mode"). Several seeds of one shot in one task share one model load (first
  seed ~17 min incl. load, then ~9 min each).
- Compute: `dev-g` only in practice (**2 jobs per user, pending ones count;
  3 h each**). `standard-g`/`small-g` start days later (sbatch --test-only,
  2026-09-27). **Host RAM, not VRAM, limits Wan**: ~100-110 GB per task, four
  tasks per 512 GB node. The login node has no GPU; keyframe composing
  (BiRefNet, Real-ESRGAN crops) runs there but slowly (~3 min per keyframe,
  15 min per upscaled crop, cached).

## Before a GPU job

Follow **all gates in `docs/v4-preflight.md`** for v4; the quick checks below
are insufficient alone. Review the positive and the combined negative together
(older `shot.py --dry-run` printed only the positive; fast mode never applies
the negative). A draft manifest is not accepted by the renderer.

1. `--dry-run` every script that has one; read the assembled prompt.
2. Check every input file exists (keyframes, canonicals, pose stills).
3. Look at every composed keyframe (and end keyframe) before rendering.
4. Will it fit in 3 h? Wan model load 10-25 min; fast clip ~9 min per seed;
   40-step 81-frame shot ~2 h 10; 49-frame pose ~1 h (fast ~15 min); LoRA
   1000 steps ~50 min.

## Mistakes already made (do not repeat)

- **`srun --overlap` into another job is not a place for real work.** When that
  job's own tasks finish, the job ends and kills the overlap steps (a LoRA run
  died at step 365/1500). Submit every workload as a task of its own job.
- **Do not assume GPU index k inside an overlap step is task k's GPU.** It
  held once in a 2-task job and failed in a 4-task one (two pose tasks ran out
  of memory). Measure with `torch.cuda.mem_get_info` if you must.
- **accelerate + multi-task Slurm steps:** Cray sets `PMI_SIZE` etc.;
  accelerate reads it as an MPI world and aborts ("MASTER_ADDR"). `lora/musubi_env.sh`
  unsets PMI/PMIX/OMPI/MV2 variables for every musubi script.
- (LoRA lessons below: the tools were removed on 2026-10-06; see git history.)
- musubi-tuner: `--timestep_boundary` is an integer 0-1000 in training;
  generation takes `--lora_weight` / `--lora_weight_high_noise`, not
  `--network_weights`; `--save_path` is a directory; merging a LoRA on the GPU
  runs out of memory, so use `--blocks_to_swap 10 --lazy_loading`; bitsandbytes
  is broken in the container, so use `--optimizer_type adamw`; fp16 weights force
  fp16 training, so use the bf16 conversions in `models/wan22_musubi/`.
- deepspeed/apex/aiter in the container break imports: the default venv shadows
  them with stubs, the musubi venv hides them with `sitecustomize.py`
  (`lumi/stubs/`).
- ffmpeg `concat` after `trim` silently fell back to 25 fps and made a whole
  video judder (the old channel intro). **Count repeated frames on deliverables**, not just
  duration.
- A reframing step once produced an image of empty floor, and nothing
  downstream noticed. Tools must **assert** their results (see
  `production/design.py reframe`); look at every contact sheet.
- Colour matching a pasted character to its background turned a white chest
  green. Never change a character's hue; brightness only.
- A wait loop on `pgrep -f "<pattern>"` matched its own shell and never ended.
  Wait on output files (timestamps) or PIDs.
- dev-g's 2-job limit counts **pending** jobs: `--dependency` submissions are
  refused while two jobs exist. Submit follow-ups from a waiter after the job ends.
- `lumi/env.sh` and `env_musubi.sh` are sourced inside the container; a variable
  they `export` overrides the caller's. Use `${VAR:-default}`.
- `pkill -f "<pattern>"` in a command also kills that command's own shell when
  the pattern appears in it (it cut a deletion short on 2026-09-27).
- The same goes for `ps | awk '/pattern/'` then `kill`: any word of the pattern
  in your own command (even a log file name) kills your shell. Kill by a PID
  you have looked at.
- A `yaml` value with a colon inside (`language: en (xx, yy: zz)`) breaks the
  file: quote such values.
- Edits on this scratch filesystem (sed -i, scripted rewrites) left files at mode 600 on 2026-10-07,
  so `lumi/run_in_container.sh` lost its execute bit ("Permission denied"). After bulk edits run
  `find . -path ./work -prune -o -type f -perm 600 -print` and restore (`chmod 750` scripts, `640` files).
- A `google-genai` client created inline and discarded (`genai.Client().x()`)
  closes itself before the call: keep it in a variable.

## Verification habits

- **Lion and Mouse v6 keyframe handoff:** all 16 scene contact sheets in
  `.review/contact_sheets/current/` are required. After any active candidate
  change, run `swift production/build_keyframe_contact_sheets.swift "$PWD"`
  and `python3 production/check_keyframe_review.py`; hand off the sheets with
  the matching full-resolution candidates. A sheet never substitutes for
  full-resolution owner approval.
- Every clip: a contact sheet (frames 0/20/40/60/80, or every 8th) and look at
  it before judging; full-size frames for faces and contact.
- Every still: reopen the saved file at full size, beside its canonical, its
  plate and the setup's size anchor (`docs/creation-rules.md` CR-13, CR-16, CR-17).
- Cuts and flashes: mean luma per frame by frame index, not `-ss` seeking.
- Deliverables: 0 repeated frames, exact duration, PCM 48 kHz audio in `.mov`.
- Voice lines: transcribe (Whisper) and compare with the text.

## Voices: Gemini 3.8 Flash TTS (owner decision 2026-09-27)

- **Everything is in `voice/`** (read its README): `gemini_env.sh`,
  `list_voices.py` (-> `voices_list.json`), `speak.py` (one line -> WAV +
  json), `save_voice.py` (record a designed voice: id, exact prompt, expiry,
  Google's sample), `render_samples.py` + `sample_lines.yaml` (the sample
  lines in every language), `narrate_scenes.py` (a story's narration, one WAV
  per scene). No GPU, no container.
- **API key: only in `~/.config/gemini/env`** (owner-written, chmod 600,
  `GEMINI_API_KEY=...`). Never print, copy, log or commit it.
- **Voices** (designed "prompted" voices, expire 2027-09-27; recreate from
  the prompt saved in each `voice.yaml` before then):

  | Role | Voice | Folder |
  |---|---|---|
  | **Lion and Mouse v2 narrator** | Moonlight Storyteller 1, `voice_v5bpq98uj7qh` | `voice/narrators/moonlight_storyteller_1/` |
  | Leo | The Noble Lion 1, `voice_zdbgqrcerxqu` | `voice/cast/leo/` |
  | Milo | The Brave Little Mouse 1, `voice_vf2w20rcys8a` | `voice/cast/milo/` |
  | alternative narrators | Golden Hour Storyteller 3 `voice_g00mo8cbdefq` (first pick), The Fireside Grandfather 2 `voice_4rdl7hydi35v`, The Cheery Tale Keeper 2 `voice_8tnxrhfqk3ur`, Bright Trail Narrator 2 `voice_tcrjw3ney7q8` | `voice/narrators/<name>/` |

  The v2 story maps them in `stories/lion_and_mouse_v2/story.yaml` (`voices:`,
  paths relative to `voice/`); `voice/narrate_scenes.py` defaults to the
  narrator, Leo and Milo voices above (`--voices` overrides).
- **Samples**: every voice folder has `google_sample.wav` and ONE sample line
  in en/es/fr/de/ru/uk (narrators: Scene 1; Leo: "You frightened me... Go on
  your way"; Milo: "Thank you..."). English files have no suffix, others
  `_es _fr _de _ru _uk`. Translations in `sample_lines.yaml` are assistant
  drafts: native check before the full scripts. Gemini audio: ~-70 dB noise
  floor; en and es verified word for word (Whisper).
- **Terms**: outputs owned by the user ("Google won't claim ownership"); price
  ~$0.0135/min of audio in 2026, ~$0.027 from 2027 (25 audio tokens/s; free
  tier rate-limited); SynthID watermark; EEA gets paid-tier data terms. Open:
  the Age Requirements ("API Clients" directed at under-18s) vs a Made-for-kids
  channel; the owner's question to Google is drafted in
  `docs/google_gemini_terms_question.md`. Never clone Gemini voices into
  another model (terms forbid replicating components of the Services).
- **Narration v4 done (2026-10-02)**: all 16 scenes, 161 lines, **11:23.7**
  (en), by `voice/narrate_scenes.py`: `sceneNN.wav` + `lines/` + `timing.json`
  in `work/stories/lion_and_mouse_v5/audio/en/` (rendered as v4; the folder became v5 on 2026-10-04). Gemini 3.8 Flash TTS Tier 1
  limits: **100 requests/day** (resets 09:00 Germany), 10/min, 10K tokens/min;
  past the daily limit calls hang instead of erroring, so the script waits 8 s
  between calls and tries a line at most twice. A 160-line story needs two days.
  `production/timing_sheet.py --story lion_and_mouse_v4` ->
  `stories/lion_and_mouse_v4/TIMING_SHEET.md` + `timing_plan.json`: which shot
  covers which line; 42 shots give 3.4 min at normal speed, 8.0 min need
  slow-downs, stills or extra shots (scenes 8, 15, 16 most).
- Chatterbox/Parler were tried and **removed** 2026-09-27 (Parler produced a
  hum; Chatterbox clones were noisy and drifted between lines); they are in
  git history before that date.
- Owner plan: narration first, video fitted to it; languages en, then es, fr,
  de, ru, uk. The narration renderer exists:
  `voice/narrate_scenes.py --lines <lines.json> --story <slug> --lang <lang>`
  reads a line list in the v4 `dialogue_coverage.json` format (JSON; it does
  not read v2's `narration/<lang>.yaml`), speaks each line with the story's
  voices and joins them per scene into
  `work/stories/<slug>/audio/<lang>/sceneNN.wav`. `production/timing_sheet.py`
  then plans the picture coverage; `production/animatic.py --lang <lang>`
  times the pictures to it, only as a separately requested assembly.

## Data lifetime

The LUMI project's data is deleted around **30 March 2027**. `work/` (designs,
poses, keyframes, shots, LoRAs, the v4 narration audio) is git-ignored and
exists only on scratch: remind the owner to back it up
(`bash lumi/backup_assets.sh`, then the printed rsync on their computer; see
`docs/findings-and-risks.md` B1). Gemini candidate takes
(`character/**/gemini/`) are git-ignored too and exist only where they were
made. Gemini voices expire 2027-09-27 (recreate from the prompts in `voice/`).

## Publishing handoff (proposed 2026-10-07)

- Production does not publish. The only thing it gives the publishing repository is a handoff tar
  built by `production/export_handoff.py` from an explicit, committed `stories/<slug>/handoff_selection.yaml`.
  A handoff is not a publication approval.
- Agents may run `export_handoff.py --dry-run` (read-only on the repo; writes only to `--out`, which must be
  outside the repo, e.g. `/scratch/project_465002727/jelealro/tmp/`). Agents do not run a real export,
  move packages, or import them unless the owner asks in that session.
- A handoff carries images, audio (WAV/FLAC master) and video; never MP3/M4A, never reading text (publishing
  writes the reading edition). Video needs ffprobe (LUMI: `module load LUMI/25.09 partition/L
  FFmpeg/7.1.3-cpeGNU-25.09`).
- Never edit files under `production/contracts/`; they are a pinned copy of the publishing contract
  (`CONTRACT.lock`). Never write a selection with patterns or "latest"; name each file.
- Uncommitted files are recorded in every handoff (names only). Do not leave stray files, and avoid spaces
  in file names: such a path blocks a real export (`DIRTY_PATH_UNREPRESENTABLE`).

## Character and scene design: reusable guidance

The following workflow principles are supported both by this repo's measured
results (see `docs/prompting.md` and `docs/character-consistency.md`) and by
Neolemon's [How to Create Consistent Characters in AI Videos](https://www.neolemon.com/blog/how-to-create-consistent-characters-in-ai-videos-complete-guide/)
(Sachin Kamath, 12 February 2026; accessed 26 September 2026). The article is
published by a character-generation vendor, so treat its tool comparisons,
pricing, timelines, and claims of perfect consistency as vendor claims. Use
the workflow ideas below; the project's measured rules take precedence.

### Define and freeze character identity

- Before generating, write a compact character specification. In this repo,
  freeze story facts in the versioned bible and expand them into each recorded
  prompt; export supported fields to `stories/<slug>/story.yaml` for execution:
  include name and story role, silhouette/body proportions, distinctive face
  features, fur/felt colours and materials, signature features or props,
  default costume/accessories if any, personality and safe emotional range,
  relative scale, and details that must never change. For felt animals,
  translate the article's age/vibe and hair/skin anchors into animal-appropriate
  traits such as age impression, fur/felt texture, ear shape, and muzzle.
- Keep a short, repeatable palette and a fixed style bible. Ensure the written
  sheet matches the approved canonical image. If the image wins over a detail
  (as with the historical v1 black-eye design; current Leo has brown irises), settle that discrepancy once by updating
  the sheet or selecting another canonical; do not carry conflicting text and
  image references downstream.
- Treat each intentional costume or accessory change as a separate visual
  state with its own canonical/anchor and pose references. Do not casually add
  clothing or props in shot actions.
- Generate and approve a neutral, full-body canonical first, alone against a
  plain contrasting felt backdrop. Build only the useful pack for the story:
  side/three-quarter/back views, expressions, and reusable action poses. The
  article's front, three-quarter, side, face, expression, and action coverage
  is a useful completeness checklist; the existing `packs/<character>.yaml`
  and LUMI budget determine what to make, not a fixed image count.
- Create every main character separately before composing a cast. Use the
  story's character sheets, canonicals and pose stills to keep designs distinct.
  For a multi-character keyframe, specify each character's position, scale,
  facing, and interaction in `compose:`; keep the scale relation from the
  story bible and exclude absent characters with `negative_extra`. If one
  character's small gesture is hard to read, make a close-up keyframe for that
  character rather than asking a camera move to find it.

### Design the set and storyboard the story

- Treat each location as a reusable empty background plate. Give it a frozen
  sheet with materials, palette, landmarks, time of day/light direction, and
  staging needs. Design the set edge to edge, with no studio table/backdrop,
  and leave clear open ground where characters must stand or travel. Keep
  story-specific landmarks consistent; a landmark associated with a character
  should not appear empty immediately after that character was established
  there unless the story shows them leaving.
- Design needed props as their own simple entities with a clear silhouette,
  distinctive material/colour, and a contrasting design background. Keep the
  prop's appearance stable in the story bible and compose it into keyframes
  when exact placement matters.
- Break a story into short, modular shots. The article suggests noting shot ID,
  duration, framing, camera movement, one main action, emotion, prop, and
  background. `story.yaml` already stores most of this through scene/shot IDs,
  `frames`, `action`, `characters`, `keyframe`/`compose`, and location/props;
  make missing staging or framing explicit in the action or composition.
- Keep each shot to one legible character action and a fixed camera for the v4 baseline. An intentional camera move
  needs separately reviewed matching anchors; never accept accidental scene zoom. Generate a keyframe for the exact composition before animation, then
  animate that still. This project's 81-frame Wan shots are about five seconds;
  the article's generic 3–6 second suggestion is not a reason to change the
  project's measured Wan frame settings.
- For continuity, start a shot from its approved canonical/pose-based keyframe
  or a chosen frame from the prior take (`continue_from`). Carry forward
  character scale, screen position, facing, prop side/holder, lighting/time of
  day, and the emotional state required by the story. Use transition or
  background/prop-only shots when they help story pacing or bridge a difficult
  cut; they are optional editing tools, not a substitute for correct anchors.
- Prefer a simpler action or shorter shot when identity, felt texture, or
  staging drifts. Reuse the same plate and locked style language; check the
  contact sheet across the full clip, not only its first frame. For critical
  multi-character beats, use the repo's composited keyframe pipeline; the
  article likewise notes that animating a whole cast together is faster but
  can drift more than composing/controlling elements separately.

### Apply these principles to this codebase

The current pipeline implements the same separation of design, composition,
and motion (the design, pose and LoRA tools named in older notes were removed on
2026-10-06): `production/keyframe.py` and each
shot's `compose:` recipe place pose stills on a location plate; and
`production/shot.py` animates the composed keyframe with Wan image-to-video.
For v4 the stills (canonicals, plates and the scene start/end frames) were
made with image models and recorded in the manifest instead of being
composed by `keyframe.py`.
The v4 primary planning records are the versioned visual bible and full prompt
manifest; runtime story recipes are derived later. Do not keep the only prompt
record in an ad hoc script or conversation. Keep decisions and measured outcomes in the relevant
`docs/` file and link it here when the guidance becomes too detailed for this
manual.

## History (dated snapshots)

Kept for the record. Where a snapshot differs from the sections above, the
sections above are current.

### V4 documentation phase (snapshot 2026-09-30, superseded)

*Its "no v4 media" statement and its "Next" were overtaken by the image
passes of 2026-09-30 to 2026-10-02 (see "Current state").*

The owner rendered v3 and supplied `work/shots/notes.txt`. A verbatim durable
copy was at `docs/reviews/lion_and_mouse_v3_owner_notes_2026-09-30.txt`
(removed; recover from Git history).
The source clips were not present in this checkout during documentation work;
reported visual defects are owner observations, not a fresh video inspection.
The two local v3 neutral canonicals were visually inspected for current identity.

Read `stories/lion_and_mouse_v4/README.md`, then its repair/shot plan. The packet
contains 118 planned image records and 62 video-mode records across 43 coverage
shots, with complete expanded prompts for all 16 scenes. It is a draft coverage
plan, not a complete timed 8–10 minute edit. Canonical approval, measured geometry,
script/voice timing and any additional line coverage remain future work.

No v4 media, selections, runtime story YAML or GPU task files were created.
`visual_bible.json` / `prompt_manifest.json` were documentation schemas; the
snapshot's tool-gap warnings (bbox-based pose sizing, stale caches, additive
negatives, fast-take continuation, animatic fallback; null hashes and planned
paths are not approval; preserve v3) are carried into "Current state".

Next (then): owner reviews the proposed sequence; on a later image-production
request, create the smooth-crown Milo root, review both canonicals and mouth
designs, calibrate references and pairs, then render the pilot.

### V4 image passes r01 to r05 (2026-09-30 to 2026-10-02)

r01 (2026-09-30 to 2026-10-02) was made with GPT's built-in image tool and
logged in `stories/lion_and_mouse_v4/GENERATION_PROGRESS.md`. Then the owner moved v4
still generation from GPT to the Gemini API
(`character/gemini_image.py`, guide `docs/gemini-images.md`). Models:
Nano Banana 2 for 16:9 scenes, Lite for square studio references, Pro
to escalate (it can replace the plate: check it). After r03 **all 118 v4 image
records were accepted** (74 r01 GPT, 40 r02 and 4 r03 Gemini), new ones
`accepted_pending_owner_review`; fixes in `stories/lion_and_mouse_v4/revisions/`,
every API call in `revisions/gemini_ledger.csv` (`gemini_image.py ledger` =
images and cost per model). The lessons became `docs/creation-rules.md`
**CR-13** (whole bodies, side-by-side identity gate, edit an approved same-setup
frame instead of regenerating a character, scale as frame fractions, V3
images staging-only, continuity cascades) and **CR-14** (measured sizes in the
S14 setup, Milo ≈ Leo's mane diameter there; dialogue close-ups in the
`s15_leo_reflects` format with faces from
`character/characters/lion_and_mouse_v4/<Name>/expressions/`, 11 each). r04 (owner's third
review): s07 brows, s08/s13 Milo smaller, S15 Milo close-ups. **CR-15**: every
scene record has `framing` (`dialogue_close_up` / `close_two_shot` /
`scene_wide` / `empty_plate`); follow its close-up recipe. r05: s05 Milo face,
s07 Leo/Milo as dialogue close-ups. The "Next" of that day (owner decides s08
Milo and s13 Milo framing and the s08_leo_softens pair, wide start and
close-up end) was partly settled afterwards: in-place repairs with the
built-in image tool made both `s08_leo_softens` ends and the `s08_milo_surprised`
pair close-ups, repaired the S07 Milo muzzle, and recomposed S06 barrier and
S08 kindness with Leo at the S05 scale (CR-16). The owner deleted
`s02_place_acorn_end_r02`; two later attempts were rejected. S13 Milo framing
is still open (see "Current state").

### The Lion and the Mouse v2 (2026-09-27)

**2026-09-27**: the owner's retelling (`stories/lion_and_mouse_v2/story.txt`,
moral: "Kindness does not create a debt. It creates more kindness.") with an
owner-made character pack made following neolemon's consistency guide.

Authority, in order:
1. Canonicals: `character/characters/lion_and_mouse_v2/{Leo,Milo}/canonical/*.png` (identity
   authority; text follows the image, never the reverse).
2. The rest of the owner's pack (views, expressions, actions) in the same folders.
3. `stories/lion_and_mouse_v2/story.yaml`: sheets (DNA corrected to the
   canonicals), locations, scale, voices, 12 scenes with the owner's narration.
4. Review frames in `work/stories/lion_and_mouse_v2_review/`: **layout guides
   only**, never character references.

How it is made (and why); the tool notes still apply to the runtime pipeline:
- **Owner-made canonicals**: `production/install_pack.py` pads them to 16:9
  (edge-repeat, blurred) into `work/stories/<slug>/design/<name>/canonical.png`,
  copies the pack to `characters/<name>/pack/` (`.png.png` fixed in copies
  only) and 16:9 versions of views/actions to `pack16x9/`. Originals are
  never modified.
- **Scale: Milo = 1/3 of Leo's standing height** (Rule 2.12). In the clearing:
  Leo standing 0.52 of frame; asleep 3/4 h 0.312; sphinx 3/4 0.361; Milo 0.17.
- **Start + end keyframes** (`end_keyframe:` / `end_compose:`): Wan animates
  between two composed stills. Close-ups: the owner's expression images as
  start/end, `blur` background, `background:` text instead of the location
  sheet (Rule 2.13). Continuations from a cropped frame also need an end
  keyframe (Rule 2.14).
- **Leo in 3/4 view** for sleeping and lying (owner request): pose clips from
  `pack16x9/views__leo_view_3q_01.png`; eyes closed in a separate short shot
  (a pose change and a face change in one shot fail).
- Everything from v1 still holds: fixed camera for locomotion, one action per
  shot, close-up crops for small gestures, no LoRA in shots, positive wording,
  several seeds (fast mode makes 3 cheap).

### Archived production snapshot (2026-09-27 to 2026-09-29)

**Owner-made images (2026-09-29):** the owner generates the v3 images on
another machine (N-07/08/09 included); do not generate them here.
`production/edit_image.py` (Qwen-Image-Edit-2511, Apache-2.0, 54 GB in
`hf_cache`) exists but is **untested**: its first run failed because the
generation venv's transformers 4.51 cannot load its Qwen2.5-VL text encoder;
it needs its own venv with transformers >= 4.57 (not created then; since then
`lumi/setup_env_qwen.sh` and `FELTWILLOW_ENV=qwen` define it, with no recorded build
or test run).

**v3 planning (2026-09-27; v3 was later rendered and reviewed on 2026-09-30)**:
the owner's longer dialogue script
(`stories/lion_and_mouse_v3/script_dialog_en.txt`, ~1,160 words, 8-10 min,
narrator + lion + mouse lines). The owner will generate the images; the list
is `stories/lion_and_mouse_v3/ASSETS.md` (58 images, to-do list with prompts in `TODO_images.md`: 10 location plates, one normal-height view per place (owner: no low angles),
new Leo/Milo poses and expressions, Leo-in-the-net states, 8 two-character
interactions, a beat-by-beat shot map), location DNA in
`stories/lion_and_mouse_v3/locations_dna.yaml`. The owner's verdict on every
v2 clip is in `stories/lion_and_mouse_v2/owner_review.yaml` (files kept;
`reject` = never use). Key v2 lesson: every shot where Wan had to draw Leo in
a new state (the net) went off-model; the best shots start and end on
owner-made images. v3 = owner-made start/end images for every shot, a plate
per camera angle and lighting.

Lion and Mouse v2 (2026-09-27): **every scene has a take**; takes are in
story.yaml (`take:`), clips in `work/stories/lion_and_mouse_v2/shots/`
(fast-mode files end in `_fast`; the animatic finds both).
- **Animatic**: `work/stories/lion_and_mouse_v2/animatic.mp4`, 1 min 46 s,
  12 scenes, 22 shots, placeholder timing (no narration yet).
- Takes: s01 3/4 1111, s02 3/4 2111, s03 3/4 3112, s04 Milo trembles 4101,
  s04 Leo softens v2 4203, s05 nod v2 5106, s06 smiles 6101, thanks 6201,
  leaves v2 6305, s07 walks 7101, net falls 7202, tugs 7303, s08 hears 8101,
  runs v2 8204, s09 arrives 9102, can help 9201, s10 gnaws v2 10112
  (PROVISIONAL), steps free 10201, s11 Leo amazed 11101, Milo smiles 11201,
  s12 friends 12101.
- **Open: the gnawing shot.** v1 drifted (camera pulled back); v2 (end
  keyframe = start frame) held the framing but Milo only stands at the rope:
  pinning both ends to the same frame also freezes the action. Next try: a
  tighter crop with Milo larger, his paws on the rope, and an end keyframe
  that differs (a composed frame with the rope parted), or accept the beat
  with the narration carrying "gnaw".
- Places: plates clearing 3003, trap_site 3104, forest_run 3204; net = prop.
- Next: fix the gnaw (owner's call); narration with the Gemini voices when
  the owner asks (write the narration renderer, see Voices); then
  `animatic.py --lang en` times the pictures to it; post (1080p30) and edit.
- Removed 2026-09-27 (owner): v1 story and its generated files, fox tests,
  The Webtoons Corner intro/LTX/felt/music code, Chatterbox. Kept: LoRA
  outputs (`work/lora/`, 86 GB) and old intro renders (`work/intro_v4/`).
