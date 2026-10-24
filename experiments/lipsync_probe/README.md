# Isolated two-character lip-sync diagnostic

**22 October 2026 update:** `tracked_probe.py` replays the original moving-face sources without generation and compares source / historical fixed patch / tracked mouth. See [current status](../../docs/lip-sync.md) and [exact receipt](evidence/tracked_20261022_r007.json). It preserves 99/99 silent/boundary raw frames; 26/31 active frames pass tracking checks and five are rejected. The owner has watched and accepted both r007 tracked results for provisional use; see [exact-hash selection](evidence/tracked_20261022_r007_owner_selection.json). Technical flags remain and future takes require playback review. The sections below describe the original fixed-ROI experiment.

Owner requested real audio/mouth movement tests using one Milo and one Leo
blurred-background close-up. This is Agent B video work on `feature/video-control`;
no production policy, approvals, image/staging files or runtime contracts change.

The current compositor (`production/lip_sync.py`) uses forced word alignment and
broad vowel-group opening pulses, blending an open/closed image difference in a
**fixed ROI**. It is not a learned animal lip-sync model or a phoneme/viseme system.
It does not animate eyes/brows. Static versus subtly animated Wan sources test
whether the mouth patch stays aligned while the face performs small expressions.

## Frozen inputs

Experiment root:
`work/stories/lion_and_mouse_v6/experiments/lipsync_probe/20261017/`.

| Character | Close-up | Recorded line |
|---|---|---|
| Milo | `s08_p03_r06_candidate.png` | S08-L012: “You're... letting me go?” (3.12 s) |
| Leo | `s08_p02_r05_candidate.png` | S08-L010: “Go home, little one.” (2.92 s) |

Audio is read from the primary checkout's **v6-local** work namespace and copied
only after checking the SHA against this branch's dialogue coverage. Its v5 origin
is intentionally registered in v6's audio manifest; no new cross-story reuse is
invented. Both close-up candidate paths/hashes match the primary checkout.
No registered matched open-mouth calibration pair for either chosen close-up was
found, and v6 word timings were absent.

The imagegen skill's built-in image_gen tool created two **unapproved isolated
open-mouth candidates**, preserving original story assets. Raw outputs and exact
prompts are retained under `inputs/`; originals remain in the generated-images
cache. Prompts requested a small toothless felt opening and no other changes.
The generator returned a different canvas size; standard Wan fitting normalizes
both candidates/source to768×432. A prompt does not establish pixel invariance:
alignment preflight measures nonmouth drift and saves the mouth mask. ROI use
limits application, but does not approve the reference or guarantee naturalness.
Milo's no-visible-teeth policy is retained. No production image approvals are set.

## Stages

1. CPU debug: `align_probe.sbatch`,15 min/16 GiB. Reuse existing CPU
   torch2.8/torchaudio/WhisperX3.8.6 packages read-only through the container Python.
   The old CPU venv interpreter symlink is stale; wrapper does not use/repair it.
   English Wav2Vec2 alignment checkpoint may be downloaded to isolated scratch
   model storage (~360 MB), never HOME or the ROCm generation environment.
   Align exact transcripts, require matching tokens/valid intervals, fit candidate
   mouth pairs and validate the existing compositor's difference-mask gate.
   Results remain `aligned_needs_listening_review`; no timing is fabricated.
2. GPU dev-g: `probe.sbatch`,one GCD,7 cores,96 GiB,30 min,afterok CPU preflight.
   First exercise static-source compositing and no-cue controls. Then load the
   pinned normal Wan2.2 I2V/Lightning once and generate two subtly expressive
   closed-mouth close-ups (four steps/CFG1,seed43,65 frames,768×432,16 FPS).
   Reuse verified equivalent bf16 storage cache in this process only.
   Composite each speaker's shifted word cues using existing `render_piece`
   through explicitly unapproved, in-memory experiment fixture metadata.
   Do not call production `apply` or manufacture a v6 runtime/take selection.

Each clip is4.0625 s. Audio starts0.5 s in, with silence padded to the same total
length; no recorded speech is sped up/truncated. Static and Wan modes each save
silent composite, empty-cue control, original padded WAV, audio-muxed composite,
and labeled original/composite side-by-side review **with audio**. Silent source
and composite remain available for DaVinci. MP4 review audio uses AAC; the padded
PCM WAV is the exact timing companion for editing.

Evaluate opening/closing against speech and pauses, mouth shape/identity, mask
spill onto nose/whiskers, expression preservation and sliding on the moving face.
Receipts record cue/alpha arrays, hashes, silence-control differences and rough
mouth-region accumulated optical flow. These metrics do not establish perceived
sync, anatomy or approval. Listen/play full review movies before deciding benefit.
Raw first/last frames are preserved by existing algorithm; lossy encodings are
not guaranteed pixel-exact. Fixed ROI drift is a specific expected failure mode.

Production remains blocked until proper mouth calibration review, selected takes,
reviewed timing and v6 runtime integration exist. These outputs are candidate
experiments, not production-ready lip-synced takes.

## Execution — 2026-10-17

CPU preflight job22929090 completed exit0 in7m10, ~819 MiB step MaxRSS.
CPU torch/torchaudio2.8 and existing WhisperX packages worked through the container
without installs/upgrades. Startup was slow; direct process inspection showed
Lustre synchronous I/O wait. Downloaded361 MiB English alignment checkpoint,
SHA256 `488fd4f16de84438ffc945334278c1b9fb9b7159a806c1080b16111a958c945d`.
Three existing speaker-attribution/closed-boundary tests pass; new Python and
batch syntax pass. Raw alignment, input manifest and exact image prompts are
retained under `evidence/`; all PNG/WAV/media outputs remain ignored scratch data.

Both four-word transcripts align exactly. Milo's “You're...” interval is
0.382–0.644 s and “letting” begins1.973 s in the original WAV, leaving a useful
long intra-line pause. Audio/cues gain the same0.5 s padding in review exports.
Word scores range0.802–0.913 for Milo and0.860–0.916 for Leo; these are aligner
scores, **not owner-confirmed temporal accuracy**. Listening review remains.

Mask areas: Milo0.492%,Leo1.292% of frame. Generated reference nonmouth mean
absolute difference after fitting:4.035/255 Milo,6.100/255 Leo. Thus these are
not exact all-other-pixels-preserved edits. Agent inspected both masks; they are
confined to configured lower-face regions, with Leo's jaw region broader than
Milo's. That does not establish visual correctness. References remain unapproved.

GPU job22929108 is queued on dev-g with afterok22929090,30-minute cap,96 GiB.
Accounting reports CPU completed while controller still reports COMPLETING
cleanup; dependency is retained. GPU runner revalidates alignment and source
hashes before using them. No pending small-g request changed by this work.
Expected outputs are `static_milo`, `static_leo`, `wan_milo`, `wan_leo`, each
containing `review_with_audio.mp4`, `synced_with_audio.mp4`, `synced_silent.mp4`
and `padded_audio.wav`. Video results are pending; no lip-sync quality success
or expression preservation is claimed from successful alignment alone.

### First playable outputs available

Job22929108 has started on dev-g. Its static-source Milo and Leo composites
completed,65 frames at16 FPS each. Output hashes verified against per-case
receipts, now retained in `evidence/static_{milo,leo}_22929108.json`. Both
`review_with_audio.mp4` files are ready in the static case directories.

Silent-frame whole-frame mean absolute difference from the no-cue control:
Milo0.0168/255,Leo0.0791/255 (lossy codec differences). These values and closed
alpha outside cues are technical checks, not a perceptual synchronization score.
Animated-face generation/compositing remains running; owner playback and visual
quality assessment of all outputs remain pending. No production approval inferred.
