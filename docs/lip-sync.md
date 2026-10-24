# Timed dialogue mouth animation

**Owner acceptance, 22 October 2026:** Both r007 tracked-mouth results are accepted as good enough for provisional use. Keep the unchanged fallback frames in the reviewed outputs and retain the technical flags. [Exact-hash owner selection](../experiments/lipsync_probe/evidence/tracked_20261022_r007_owner_selection.json). The reviewed MP4s are preserved under `work/reviews/mouth_tracking_20261022_owner_selected/`. The playback label `64 / unchanged` identifies the last boundary frame; the selected method is tracked mouth delta. No new generation or lip-sync application is implied by this acceptance.

**Tracking repair trial (22 October 2026):** The compositor now tracks local muzzle features with forward/backward optical flow and a bounded affine fit. It warps only the mouth-change delta, selects the connected dark oral opening to exclude unrelated chin lighting, and leaves zero-activation and boundary frames untouched before encoding. Low feature support, excessive deformation, changed mouth appearance or occlusion blocks production output; diagnostic replay leaves rejected frames unchanged and reports them. This remains a technically partial repair; the owner accepted both reviewed r007 tracked results for provisional use on 22 October 2026. [Exact diagnostic receipt](../experiments/lipsync_probe/evidence/tracked_20261022_r007.json).

The original fixed patch failure is preserved in the 2026-10-17 probes. CPU replay job **23069849** completed on those same source hashes, without generation. Milo passed tracking on 12/13 active frames; frame 48 was rejected for changed mouth appearance (the source itself opens into a smile). Leo passed 14/18; frames 39, 40, 42 and 45 had insufficient affine inlier support. All 99 zero-activation/boundary raw frames were pixel-identical to their sources. Ten regression checks passed, covering known motion geometry, occlusion/lost-face rejection, silence, mouth-mask isolation, speaker attribution and cache invalidation. Feature fit is not independent anatomical tracking accuracy. Lossy MP4 encoding is not pixel-exact.

Playback comparisons (columns: source / historical fixed patch / tracked) are in `/scratch/project_465002727/jelealro/tmp/mouth_tracking_20261022_r007/{milo,leo}/comparison_with_audio.mp4`, with mouth crops and per-frame receipts alongside. The source/calibration assets originated as experimental fixtures. The owner watched both r007 comparisons and accepted the tracked results, including unchanged fallback frames, as good enough for now. This scoped acceptance does not adopt those fixtures as character canon or certify the five rejected tracking frames. Future takes still require their own listening/playback review. Do not lower confidence thresholds solely to make them pass. A source take that opens its mouth during silence still needs rejection or a separate source repair; preserving source pixels does not force it closed.

`feltwillow/mouth_tracking.py` implements the bounded tracker. `production/lip_sync.py` uses it in compatible manifest-backed runtimes; `feltwillow/lipsync.py` fingerprints compositor/tracker code and sorted calibration roles so historical fixed-patch caches are not reused. V7 still needs explicit selected-take/audio mapping and approved calibration assets before application; the S01–S03 animation jobs do not apply lip sync.

Replay with `TMPDIR=/scratch/project_465002727/jelealro/tmp bash lumi/run_in_container.sh python experiments/lipsync_probe/tracked_probe.py --out /scratch/project_465002727/jelealro/tmp/<new-run>`. Use a CPU allocation; outputs must be in a new directory. Original probe assets and immutable receipts stay unchanged. Superseded/duplicate videos generated during this repair were removed after the shared scratch filesystem filled; r007 is the current comparison.

The recorded line WAVs and speaker labels remain the timing source. For each project, forced-align the exact approved transcript to each line recording, review alignment exceptions, then apply mouth animation only to owner-selected video takes whose `mode: mouth` variant names the speaking character. `NARRATOR` lines are voice-over and must never drive a character's mouth, even when the narrator describes speech or a call. During narration, keep the approved mouth pose still. Distant wide shots also keep their mouth poses still because the mouth cannot be reliably masked or reviewed at that scale. The separate compositor preserves each take's first and last frames. A chained dialogue take must have closed-mouth boundary images and a separate approved open-mouth calibration image edited from one of those closed frames. It changes only the named speaker's mouth region during that speaker's aligned words; silent gaps preserve the selected source frames, which must already have an acceptable closed-mouth pose. Open-mouth boundary frames are rejected because preserving them would cause a mouth to open during a pause. A piece without one explicit character speaker is rejected; mixed speakers must be split or explicitly select the visible character whose line is being animated, leaving other speakers' intervals closed.

## Lion and Mouse v6 status (2026-10-11)

The unchanged v5 English line recordings are intentionally staged under the
v6 work namespace, with source and runtime hashes in `audio_manifest.json`.
They are valid v6 audio provenance; do not rerecord them merely because the
source was v5. The current v6 packet has a scene/keyframe/boundary plan and
97 candidate images, but no approved video endpoints, selected takes or
runtime `story.yaml`. The existing `production/lip_sync.py` implementation
expects a manifest-backed chained runtime with `timing_plan.json`, variant
records and `takes.yaml`; it is **not yet a runnable v6 instruction**. V6
runtime/preflight and a compatible lip-sync mapping must be established before
using it. Preserve the rule that only the explicitly assigned visible
character speaker receives mouth motion; `NARRATOR` is voice-over.

When a compatible runtime exists, verify v6-local WAVs against the audio
manifest, align the exact transcript, review alignment exceptions, then apply
mouth animation only to selected approved takes. The post-sync join gate must
use `--require-takes --fail-on-flagged-joins`; any flagged join blocks handoff.
The current-plan preflight is
`python3 production/v6_runtime.py --story lion_and_mouse_v6 --preflight` and
must remain non-zero while image reviews are missing or rejected.

## Scope and accuracy

WhisperX provides word-level timestamps through forced alignment. The compositor uses each word interval and vowel groups to create broad opening pulses, warping the pixel difference between the approved closed/open images through the local muzzle track, within the configured mouth ROI. It is a controlled approximation, not phoneme-level viseme synthesis: it does not create distinct /m/, /f/, /o/ or /ee/ mouth shapes. Reviewers should reject clips where the single open shape looks wrong for the line or where the mask includes anything beyond the mouth. If the approved endpoint or calibration images are missing, mismatched, or produce an ambiguous mask, the compositor stops instead of guessing. A changed timing plan, prompt manifest, visual bible, dialogue coverage, word alignment, line audio or approved mouth image invalidates the cached lip-sync output and edit handoff until `apply` runs again.

For another project, provide line-level WAVs, exact transcript/speaker metadata, a `timing_plan.json`, `dialogue_coverage.json`, a prompt manifest with matched open/closed endpoints and `mouth_character` markers, and `mouth` variant rows with one explicit character `speaker`. Run the same two steps after narration is finalized and after takes are selected. Preserve the timing and sync manifests with the edit handoff. Review that narrator-only intervals leave the character mouth unchanged and that another character's line never opens the selected speaker's mouth.
