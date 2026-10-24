# FELTWILLOW V7 — LUMI continuation handoff, r005 checkpoint

**Updated:** 24 October 2026, Europe/Berlin
**Repository:** `jeilealr/feltwillow-production`
**Branch:** `wan-new-image-approach`
**Implementation source baseline:** `1a74ab85c605ea864fc249c0346cebbe1e60d8c1`
**Checkpoint commit:** the commit containing this file; obtain with `git log -1 --oneline` after pulling.
**Story:** `lion_and_mouse_v7`
**Current instruction:** save/push progress and continue implementation on LUMI. This is a work-in-progress checkpoint, not a completed film or full engineering sign-off.

## 1. Start here

Read current `AGENTS.md` and `CLAUDE.md`, then this handoff and `stories/lion_and_mouse_v7/review/owner_sequence_feedback_r004/IMPLEMENTATION_STATUS.json`, `TEST_RESULTS.json`, `ADVERSARIAL_REVIEW.md` and `RESUME.md`. Preserve newer owner work; do not reset to the baseline commit.

The owner explicitly authorized saving, committing and pushing the current changes so they can pull on LUMI. This authorization is **Git only**. Zero new paid image calls, GPU jobs, model downloads or retries occurred in this implementation tranche. No spending, rendering, automatic retry, new artwork selection or final assembly is authorized by this checkpoint.

The original r004 assignment remains active after this transfer: implement all unblocked generic code/schema/metadata/docs/CPU checks; prepare reviewable exact-reference art and resource packets; continue independent work when an asset is blocked. Do not replace implementation with another plan or ask settled editorial questions. Finish each remaining engineering task before asking for dependent art/resource decisions.

## 2. Owner editorial decisions — authoritative and already answered

Classify shots on **three independent axes**: temporal relationship `individual|connected`; composition `portrait|body_or_interaction|environment_only|detail`; mouth policy `no_mouth_driver|dialogue_lipsync|diegetic_bite|ambience_only`. Portrait can be individual or connected. Cuts are boundary edges, never a competing temporal classification.

`audio_visual_plan.json.visual_units` is the one authored classification authority. Referenced `production_sequences` owns ordered uses/edges. Existing planned image slots remain null-media historical planning records; source selection comes from exact-hash ledgers, not filename sorting. Current overrides retire obsolete production requirements without falsely filling them or deleting historical slots.

| Interval | Current owner direction |
|---|---|
| S01 L001 | Full 9.96 s forest-only, zero cast. Same approved plate at both intentional endpoints. No Milo reveal or missing walking-start requirement. `s01_opening` is a review alias to one `s01_empty_hold`, never a duplicate film entry. |
| S01 L002/L003; L004 B01/B02 | Independent shots; preserve distinct beat settings and existing stills. No mandatory invented endpoint for completeness. |
| S01 L004 B03 | Connected tiny toothless physical acorn bite, with whole-acorn before/contact/closed-tasted aftermath. Narrator audio does not drive speech mouth. Missing contact/support states remain real source-art dependencies. |
| S02 L001 | Individual shot. Owner likes existing movie; no new start image is required. Positive feedback is not automatic whole-motion/final-take approval. |
| S02 L002 | Independent environment hold with identical selected source/end bytes; no character boilerplate. |
| S02 L003 | Individual Milo speaking portrait, exact 2.04 s audio. Stable face/ears/neck/upper chest; no hand, zoom or new limb. Requires selected safe source then tracked-mouth post-sync. |
| S02 L004 | One connected placement action: B01-I02 → B02-I01 exact alias → B02-I02 contact → B02-I03 released. Four logical uses, three rasters, two meaningful motions. Rise is narrated/offscreen before visible placement by default; no new pre-rise frame. Preserve “beside the stone” narration and repair incompatible on-stone depiction. |
| S03 L001–L008 | One stationary camera/body/root-locked fork group, eight attention states, nominally seven meaningful transitions plus safe holds. Preserve sky→left long route→right shortcut geography. |
| S03 L009–L010 | Connected Milo portrait with separate exact MOUSE line cues and 0.45 s gap. Wide→portrait is an explicit cut. |
| S04 L001–L005 | Five independent single-source shots; obsolete planned I02 endpoints are not image requests. |
| S05 L001–L006 | Independent shots. L005/L006 share one exact raster but are separate editorial uses, not mandatory connected motion. |
| S05 L007/L010/L011 | Independent portraits: MOUSE dialogue / NARRATOR silent mouth / LION dialogue respectively. |
| S05 L008–L009 | Connected rear-paw catch→pitch→support loss→tumble→roll→grounded nose landing. Five selected rasters do not prove all eight meaningful phases. Leo sleeps until the authored awakening. |
| S06 L001–L005 | Connected same-camera two-actor action. Leo lying with raised head/chest, Milo screen-right; later FRONT-paw block differs from S05 REAR-paw trip. Current three anchors + three aliases + seven missing meaningful phases. |
| S07 L001–L002 | Connected Leo portrait dialogue. |
| S07 L003–L005 | Separate connected Milo portrait dialogue; deliberate speaker/view cut after Leo group; accepted nervous expressions preserved. |
| S08 L001–L006 | Individual narrator coverage with safe shared-raster uses. Equal states do not prove a visible head turn. |
| S08 L007–L011 | Connected Leo thoughtful→softened→reassuring portrait acting. L007 narrator never drives lips; L008–L011 Lion cues only. L010 paw-release remains offscreen below crop. |
| S08 L012; L019–L021 | Individual Milo speaking portraits; reuse stills but compute per-line words/audio mappings. |
| S08 L013–L015; L022–L024 | Independent Leo speaking portrait uses by default; no invented in-crop sky/paw gesture. |
| S08 L016–L018 | Independent narrator scene uses of one defective selected raster. Production blocked pending new selected paw repair; preserve r001 history. |
| S09–S16 | Not automatically classified. Preserve causal plan and classify evidence-based forthcoming groups before image proposals. All 161 audio lines already exist; later visual authoring remains incomplete. |

Forest source SHA256: `c57b58a19ad45abe44e5ad4f2085fc7d7523af890694fdc7dcb7ac8f5b01e517`.

Accepted fork first r004 SHA256: `5163cea0a436d27ec4b1ea4a16c857b5ffdb504a0309d587fe34d84a7d2beee6`. Preserve L006 **r001** camera/body anchor SHA256 `7842d9c8a4c2f67848fb38195d11544e985f414a61e6a8f0a4658208bd80fb68`. Accepted fork-turn preparation is a strategy, not a completed clean plate or paid-operation permission.

S08 defective selected L016 r001 SHA256: `516ea912c1a726927232e3e6df83a7e7f9eb3a3f54719e24a148f60c6dd94604`. Block all three L016/L017/L018 uses. Native review finds the top-right distal paw insufficiently readable; reference L001 has a different extended blocking pose, so blind deterministic transplant is not justified. New r002 must preserve four-limb topology, support/occlusion, anatomy, palette, camera and all protected pixels, then obtain exact-hash owner selection before any associations change.

Owner-liked S02 L001 existing movie SHA256: `24408b35b1a0b8343a7d531989f3a643f7e2454435328c5b5a964701545c8cbb`. Parent Mac work folder contains it; Git does not transfer ignored historical videos. Do not call it a new reviewed/selected take from this checkpoint.

## 3. Implemented and checked so far

- `production/visual_grammar.py`: optional, validated three-axis extension; 53 canonical visual units and one sequence review alias. Narration, world events/states and legacy planned slots preserved. Migration snapshot: `EDITORIAL_MIGRATION_BEFORE.json`.
- `production/sequence_plan.py` / readiness: canonical sequence aliases, shared boundaries, exact-hash production blocks and visual-unit/audio bindings. Missing tiny-bite state remains explicit.
- `production/sequence_export.py`: edge-free individual input emits an actual `wan_i2v_single` operation with no last image; intentional environment pairs retain both equal endpoints; adjacent `shared_boundary` aliases emit no redundant model job. `recipe.pieces` can override a named piece's frames/steps/guidance within supported constraints.
- `production/shot.py`: frozen single/pair/static/local method support, optional endpoint, runtime/run/seed/hash identity and receipts. Synthetic frozen CLI→fake backend proves single `last_image=None`, differing piece frame counts and alias suppression. Actual Wan adherence is untested.
- `feltwillow/local_video.py`: CPU static frame holds and reviewed bounded same-canvas mask/target/weight blending, plus FFmpeg encoding with honest provenance. Static mode can cover >81 cells without a model call. Bounded-local-effect generic frozen-CLI integration still needs a dedicated regression before closure.
- `production/sequence_timeline.py`: contiguous integer sample intervals, one cumulative rational frame-cell quantization, exact source hashes, explicit static/video intervals, actual source FPS/frame count checks and reviewed retime/trim/join requirements. Preview helper exists; it does not grant take selection or final assembly. Production exporter/editor allocation integration remains unfinished.
- `production/v7_dialogue.py`: V7-native `inventory`, `compile`, `apply`, exact WAV/metadata/transcript/speaker/take/word/frame/calibration binding, bounded tracking, narrator/silence/boundary preservation, output hash and pending post-sync review. Does not need legacy prompt/visual/timing manifests. Existing `production/lip_sync.py apply --v7-packet ... --out ...` dispatches before legacy loading; without a V7 packet it fails explicitly.
- `feltwillow/portrait_qa.py`: reviewed ROI/protected-body/camera warning metrics; warnings require actual review and never certify paws/teeth semantically. V7 source QA rejects intrusion warnings.
- Character performance library has seven planned portrait mouth families plus one separate tiny-bite contract; no V7 open-mouth candidate is selected. Species/view-specific toothless calibration remains a real dependency.
- Mouth tracker conservative-edge fix preserves subpixel mask fringes, versioned `tracked-mouth-delta-v2-conservative-edge`; actual tracker regressions passed after the change. Historical receipts are not rewritten.
- Existing skills/docs updated for orthogonal grammar, individual defaults, actual endpoint conditioning, portrait crop protection, dialogue-only mouths and four-paw review. Stale active forest→Milo and Leo mismatch prose corrected; dated history preserved.
- Grouped `OWNER_REVIEW.html` generated: one card per canonical unit, expandable logical anchors, exact source/fitted hashes, associated line audio and blockers. 58 local distinct fitted rasters, 22 missing/blocked active logical uses, all 16 audio scene masters inspected. Browser visual QA remains pending. No real forest preview was produced; its linked page states that plainly.

## 4. Independent review and honest verification limits

Separate editorial/source and art/dialogue reviewers actually ran. `art/REVIEW.md` records native S02 rock support, S08 paw overlays, exact source inventories and seven closed portrait family references. `tests/test_v7_dialogue.py` and `tests/test_portrait_qa.py` include real CPU FFmpeg decode/encode and bounded tracker fixtures, not production media approval.

Independent runtime review reproduced four defects (negative static piece frames, failed retime/trim reviews accepted, source FPS ignored, unrecorded end trims); all four were independently rechecked fixed. A fifth target-mapping approval invalidation defect was found afterward. The integrator added target sample/frame/fps binding to the review fingerprint, but the dedicated regression/independent recheck is still pending. Do not erase the report's dated observations or claim unconditional sign-off.

`TEST_RESULTS.json` and `full-tests.log` contain the actual pre-commit run outcome. Earlier 80-case focused run had one mouth-mask regression; do not borrow that as green. After the conservative-edge fix, 23 tracker/dialogue/portrait cases passed. Full suite results supersede those intermediate logs only for the exact checked code. The original r002/r003 107-test count does not certify these changes.

All C01–C52 requirements from r004 remain the acceptance target. Many are covered by new/existing fixtures, but complete ID→case/proof mapping is **not finished**. T00–T20 status in IMPLEMENTATION_STATUS.json is deliberately partial. No new image, real Wan sequence, post-sync production take or final assembly is accepted.

## 5. Next executable engineering work on LUMI

1. Pull this checkpoint, inspect local changes/branch/HEAD, read status and compare input hashes. Preserve accepted source and historical receipts. Do not recreate fork r004.
2. Verify the existing host CPU interpreter, Pillow/Numpy/OpenCV/FFmpeg. Do not install or download implicitly. The Mac interpreter path below is not portable.
3. Run current CPU checks and add target timeline review invalidation regression (changed start/end/rate/fps/cells must invalidate retime/trim approval). Independently recheck after fixing any failures.
4. Add real frozen-CLI bounded-local-effect tests for source/target/mask/weights, positive integer effective frames, outside-mask preservation, resting boundaries and no model load.
5. Finish production exporter/editor integration for reviewed per-piece sample allocations, explicit holds/retimes/trims and full join evidence. Current production exporter still requires piece frame cells to equal its allocated interval; separate timeline helper must not be mistaken for completed integration.
6. Complete strict portrait readiness/review integration and review-surface conformance. Inspect grouped HTML/audio/native/fitted cards; regenerate only affected derived outputs. Preserve old `review/sequence_readiness_r001` as historical evidence.
7. Finish all T00–T20 evidence and C01–C52 coverage mapping, including negative CLI tests, cache invalidation, exact take/mouth scope, unsupported endpoint config, uncertain-job guard and no v6/history changes.
8. Reverify installed LUMI Diffusers/config/model/LoRA/source pins read-only before any approved diagnostic. Source capability is not full-motion fidelity. Reconcile outstanding jobs/claims before proposing operations; missing output never authorizes retry.
9. Only after independent work, prepare the next coherent exact-input art tranche and concrete capped resource packet. Do not ask settled editorial questions or approve unknown future bytes.

## 6. Media/art/timing dependencies to carry forward

- Tiny bite: approved same-angle toothless tiny opening with one supported acorn, whole-before/tasted-after state, closed/resting end; narrated physical action, not word lip-sync. Existing old teeth pilot remains rejected baseline.
- Dialogue: view-matched selected Milo/Leo closed/open calibration with bounded oral ROI and exact source/selection/anatomy hash records. Generic open mouth or V6 probe cannot grant V7 eligibility. Closed source boundaries; raw teeth/hand/zoom defects must be rejected before compositing.
- S02: selected contact/release art is on top of moss-covered rock; preserve “beside the stone” audio and repair hand/prop/support together. No fabricated pre-rise state needed. Four logical uses still mean only two meaningful distinct transitions.
- Fork: exact clean-region/mask and angle-compatible turn reconstruction; full scene is not actor-free plate. Protect root/body/crop/geography; do not paste one head ellipse over incompatible yaw or infer exact background from a camera label.
- S05: approach, forward pitch and grounded nose landing remain missing/uncertain around five selected rasters. Verify actual rear-paw catch/contact before causal mapping.
- S06: three selected anchors + three aliases + seven missing meaningful phases. Same scale/root/depth, Leo lying, distinct front-paw block.
- S08: exact hash-bound one-paw repair proposal and native overlays in `art/`; no new r002 exists. Rebind L016/L017/L018 only after successful exact-hash selection.
- All scene audio r001 exists. Actual word/action markers are not reviewed. WhisperX unavailable on Mac and no cached aligner verified; CPU synthetic timings prove mapping only. No new narration synthesis is requested.

Important timing: S01 L001 0–9.96 s; S02 L003 12.47–14.51 s and L004 15.21–23.89 s, scene total24.89 s; S03 wide through L008 ends31.15 s, outgoing wide holds through pause to portrait start31.85 s, scene total39.02 s. Exact offsets/PCM checks for all scenes are in AUDIO_AND_FRAME_ALLOCATIONS.json. Interline same-speaker gap0.45 s, speaker-change0.70 s, scene tail1.00 s. Own each gap/tail once on stable closed/settled state.

Wan route: one first image plus optional last image, never arbitrary timed multikey list. Distinct chain anchors must reach adjacent first/last calls. Model pieces5–81 frames, 4k+1,16fps. 81frames encode5.0625s while first-last span5.0s; do not force a2.04s utterance to5s or issue >81 model frames for9.96s forest. Static/local editor coverage is a separate labeled method. At Lightning CFG1 negative text is inactive; positive toothless/cast constraints and all-frame review are still needed.

## 7. Pull and resume commands

From the existing LUMI clone, after checking any local work:

```sh
git status --short
git branch --show-current
git pull --ff-only origin wan-new-image-approach
git log -1 --oneline
command -v python
python -c "import sys; print(sys.executable); print(sys.prefix); import PIL, numpy, cv2; print('CPU dependencies available')"
python production/audio_visual_plan.py --story lion_and_mouse_v7 validate
python -m unittest tests.test_visual_grammar tests.test_r004_runtime tests.test_sequence_timeline tests.test_v7_dialogue tests.test_portrait_qa -q
python production/v7_dialogue.py inventory --story lion_and_mouse_v7
```

These are CPU-only, no network/model/submission commands. If required modules or media are unavailable, record exact host dependencies; do not auto-run setup scripts. On the Mac the verified interpreter is `/Users/lealroja/miniconda3/envs/feltwillow/bin/python`. Parent work is `/Users/lealroja/Documents/feltwillow/work`, not repo-local `work`.

For existing APIs, inspect help before use:

```sh
python production/sequence_export.py --help
python production/sequence_timeline.py --help
python production/v7_dialogue.py compile --help
python production/lip_sync.py apply --help
python production/owner_feedback_review.py --help
```

Freeze new runtime paths and executable on the intended host only. Reusing Mac absolute runtime packets on LUMI is invalid. Never route new jobs through legacy `lumi/render_story.sh` repeated rounds, load weights during ordinary tests, submit unapproved jobs or infer retries from an interrupted conversation.

## 8. Completion and authority

Continue until all independently executable engineering is verified and every remaining operation has a precise external blocker. Keep separate statuses for engineering, still selection, technical edge readiness, real diagnostic, full-motion/join review, post-sync review, owner take and assembly. No source hash, synthetic test, thumbnail or successful model invocation grants a different approval scope.

S09–S16 later authoring remains part of the completion register. An opening pilot is not a finished story. Keep v5/v6, selected rasters, canonicals, narration bytes and historical receipts unchanged. Request only exact art selections or concrete capped provider/GPU authorizations after preparing genuinely reviewable inputs and finishing independent work.

**Checkpoint validation:** focused V7/runtime/dialogue checks: **80 tests passed**. Full suite: **303 tests, 6 failures, 16 errors**; detailed output and limits are in TEST_RESULTS.json/full-tests.log. Do not describe the full suite as green. No source-media or old receipt changes were made.
