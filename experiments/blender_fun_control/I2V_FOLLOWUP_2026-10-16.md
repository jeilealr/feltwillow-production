# Four-step I2V longer-shot and continuity follow-up

Owner authorized this follow-up after preferring the normal four-step panel of
the first comparison. Blender is parked; the saved 2.5D guide experiment remains
available. No rigged 3D mouse was built. Fun Control consumed Canny frames from
an animated textured image plane, not a 3D asset.

## Recipe and question

Run `i2v_followup.sbatch` from this checkout. One regular `small-g` job, one GCD,
7 CPU cores, 128 GB host RAM, 90-minute hard limit. Three sequential clips share
one model load. No downloads or environment changes. All temporary data inherit
scratch `tmp` settings from `run_env.sh`.

Use the existing pinned Wan 2.2 I2V A14B and Lightning adapters through the
unchanged production API, with the previously verified equivalent bf16 storage
cache overridden in this experiment process only. Four steps, guidance 1/1,
832×480, 81 frames, 16 FPS: 5.0625 seconds per encoded clip. This is **480p**, not
a native 720p validation. Duration and resolution both increase relative to the
33-frame 416×240 pilot; this comparison does not isolate their individual effects.

1. `long_81`: same prompt and original source illustration as the first pilot,
   seed 43. Does natural acting and morphology survive a longer, larger render?
2. `continue_generated`: use the exact lossless final PNG from case 1, seed 44.
   Does a second clip continue motion and preserve identity without accumulating
   distortion? No MP4 recompression is introduced into the conditioning image.
3. `restart_keyframe`: same seed 44 and prompt as case 2, but condition on the
   frozen existing next story keyframe (`s01_p04_r02_candidate.png`). Does a new
   image restore intended appearance/pose and enable a useful next shot?

The next keyframe visibly changes Milo's size and pose. It is an **intentional
new-shot cut**, so a seamless pixel match is not its success criterion. No video
interpolates between the two images. Compare identity, anatomy, action and
background across both options; report cut visibility separately. Equal seeds
for cases 2/3 share the same backend/settings but different conditioning.

All prompts use the same gentle feeding action to avoid changing two factors at
once between the second-shot variants. This tests two adjacent feeding clips,
not complex multi-action storytelling, walking, or endpoint anchoring.
Only one extension is tested; it cannot establish long-chain stability.

Inputs are frozen from the prior non-production experiment, independently
hashed, fitted from the original images at the new output dimensions and never
written back to canonical files. Keyframe/staging/image approvals remain unchanged.
No final-image conditioning, Control or Blender is used in these renders.

## Outputs and assessment

Local output root:
`work/stories/lion_and_mouse_v6/experiments/blender_fun_control/i2v_followup_20261016/`

Each case saves output MP4, exact first/last PNGs, five full-size snapshots,
an all-81-frame contact sheet, hashes, inference duration and peak allocated GPU
memory. MP4 frame count, dimensions and FPS are checked after encoding.
`continuity_comparison.mp4` shows the same first clip on both sides followed by
extension on the left and keyframe-cut shot on the right. No crossfade hides the
boundary. Master receipt retains failures and records model/cache/script/input
provenance; all outputs explicitly remain ineligible for production.

Assess facial/ear shape, paws/acorn contact, spontaneous acting, camera/subject
size drift, background identity, boundary discontinuity, extension degradation,
and compute cost. Contact sheets are agent-visible evidence; owner playback
judgment remains distinct from technical receipts or production approval.

## Execution

- Job `22914092` submitted to `small-g`, 90-minute cap. Results pending.
