# Timed dialogue mouth animation

**Current limitation (19 October 2026):** [image-first Wan policy](production-direction.md) retains dialogue requirements. The fixed closed/open reference and fixed mask can visibly fail on moving faces; zero activation still composites the closed reference on interior frames. Preserved probes are diagnostic, not a repair. Next task: tracked muzzle/mask, no-cue pixel preservation before encoding, confidence/occlusion handling and owner playback review.

The recorded line WAVs and speaker labels remain the timing source. For each project, forced-align the exact approved transcript to each line recording, review alignment exceptions, then apply mouth animation only to owner-selected video takes whose `mode: mouth` variant names the speaking character. `NARRATOR` lines are voice-over and must never drive a character's mouth, even when the narrator describes speech or a call. During narration, keep the approved mouth pose still. Distant wide shots also keep their mouth poses still because the mouth cannot be reliably masked or reviewed at that scale. The separate compositor preserves each take's first and last frames. A chained dialogue take must have closed-mouth boundary images and a separate approved open-mouth calibration image edited from one of those closed frames. It changes only the named speaker's mouth region during that speaker's aligned words; silent gaps stay in the approved closed pose. Open-mouth boundary frames are rejected because preserving them would cause a mouth to open during a pause. A piece without one explicit character speaker is rejected; mixed speakers must be split or explicitly select the visible character whose line is being animated, leaving other speakers' intervals closed.

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

WhisperX provides word-level timestamps through forced alignment. The compositor uses each word interval and vowel groups to create broad opening pulses, blending only the pixel difference between the approved closed/open images in the configured face ROI. It is a controlled approximation, not phoneme-level viseme synthesis: it does not create distinct /m/, /f/, /o/ or /ee/ mouth shapes. Reviewers should reject clips where the single open shape looks wrong for the line or where the mask includes anything beyond the mouth. If the approved endpoint or calibration images are missing, mismatched, or produce an ambiguous mask, the compositor stops instead of guessing. A changed timing plan, prompt manifest, visual bible, dialogue coverage, word alignment, line audio or approved mouth image invalidates the cached lip-sync output and edit handoff until `apply` runs again.

For another project, provide line-level WAVs, exact transcript/speaker metadata, a `timing_plan.json`, `dialogue_coverage.json`, a prompt manifest with matched open/closed endpoints and `mouth_character` markers, and `mouth` variant rows with one explicit character `speaker`. Run the same two steps after narration is finalized and after takes are selected. Preserve the timing and sync manifests with the edit handoff. Review that narrator-only intervals leave the character mouth unchanged and that another character's line never opens the selected speaker's mouth.
