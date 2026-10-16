# v6 narration-to-visual sequence audit

**Scope:** storyboard/coverage planning. Owner image selection is now complete; current individual images and hashes are in [KEYFRAME_REVIEW.md](KEYFRAME_REVIEW.md) and `keyframe_plan.json`. Board-only generation prompts and dialogue mouth poses are historical planning material, not production-boundary instructions. Read [README.md](README.md) before a new review.

**Result:** 16 audio tracks become **52 visual units** and **96 individual keyframe candidates**. The tracks and words do not change. A visual unit may switch camera angle or crop while keeping the same approved location plate. The 70 existing storyboard panels remain overview art; six original supplemental layout boards guide 26 individual supplemental frames; the new action and dialogue views are present as individual PNGs. Review the video-source images in [`KEYFRAME_REVIEW.md`](KEYFRAME_REVIEW.md).

`video_boundary_plan.json` now orders the 96 candidates chronologically and names the proposed start/end image for each audio scene. Its `camera_cut` edges are view changes, not character growth or a continuous zoom. Only explicitly marked shared boundaries reuse the exact previous end image; all are pending full-resolution visual review and, for long lines, word-level timing. See [`README.md`](README.md).

The narration is checked line by line. Scene 04 names three landmarks along one shortcut path, so it has separate views of the stone, branch and stump on the same background. Scene 05 stays at the great tree; Leo’s spoken line has a closer view of that same plate. Added views also unpack Scene 01’s foods, Scene 12’s running obstacles, Scene 15’s speaker turns and Scene 16’s closing narration. Scene 09’s overview board has been corrected to use only approved plates. Scene 05 now includes a near-paw stumble and a separate mid-roll beat before nose contact; Scene 06 has a grounded rise bridge. Leo’s Scene 05 question uses a closed-mouth close view with strongly blurred Great Tree context. Scene 07 adds one similarly blurred face view per speaker, with medium two-shots retaining the shared geography. These face shots are intentional camera cuts and do not alter the physical cast ratio.

**Timing:** each listed unit starts and ends at a measured line boundary in the assembled audio. One long line can contain several visual cutaways; those internal edit points need word alignment before final timing. Narration remains voice-over.

| Audio track | Visual units | Approved place(s) | Extra review views |
|---|---:|---|---|
| 01 | 2 | stream_afternoon | yes |
| 02 | 1 | stream_sunset | — |
| 03 | 2 | fork_sunset | — |
| 04 | 5 | shortcut_dusk | yes |
| 05 | 4 | tree_dusk | yes |
| 06 | 2 | tree_dusk | yes |
| 07 | 2 | tree_dusk | yes |
| 08 | 6 | tree_dusk | — |
| 09 | 4 | shortcut_dusk, home_night, tree_dusk | — |
| 10 | 2 | trap_morning | — |
| 11 | 2 | trap_morning | — |
| 12 | 3 | run_morning | yes |
| 13 | 6 | trap_morning | — |
| 14 | 3 | trap_morning | — |
| 15 | 5 | trap_morning | yes |
| 16 | 3 | tree_day | yes |

## Visual units

### Audio Scene 01

- **v01a** · S01-L001–S01-L003 · 0.00–24.35s · `stream_afternoon`: Introduce Milo on the stream bank, then show the berry bush, hollow log and his longer-than-usual wander.
- **v01b** · S01-L004 · 24.35–40.19s · `stream_afternoon`: Food montage within this long narrator line: seeds in grass, berries beside the stream, then the acorn.

### Audio Scene 02

- **v02a** · S02-L001–S02-L004 · 0.00–24.41s · `stream_sunset`: Same stream-bank geography at sunset; Milo notices the light, speaks, and leaves the acorn by the stone.

### Audio Scene 03

- **v03a** · S03-L001–S03-L008 · 0.00–31.49s · `fork_sunset`: Establish both routes around the boulder; Milo looks from left meadow branch to right shortcut.
- **v03b** · S03-L009–S03-L010 · 31.49–39.06s · `fork_sunset`: Milo chooses the right branch and speaks without moving to a new background.

### Audio Scene 04

- **v04a** · S04-L001 · 0.00–2.37s · `shortcut_dusk`: Milo enters and hurries along the established shortcut path.
- **v04b** · S04-L002 · 2.37–4.86s · `shortcut_dusk`: Separate view of Milo passing the left mossy stone, feet on dirt lane.
- **v04c** · S04-L003 · 4.86–7.63s · `shortcut_dusk`: Separate view of Milo ducking under the fallen branch, same plate.
- **v04d** · S04-L004 · 7.63–9.96s · `shortcut_dusk`: Separate view of Milo curving around the stump, same plate.
- **v04e** · S04-L005 · 9.96–14.96s · `shortcut_dusk`: He runs toward the distant opening and gradually recedes in scale.

### Audio Scene 05

- **v05a** · S05-L001–S05-L004 · 0.00–20.52s · `tree_dusk`: Establish Leo asleep; show mane on grass, closed eyes and paw blocking path as details of one tree clearing.
- **v05b** · S05-L005–S05-L007 · 20.52–25.73s · `tree_dusk`: Milo rounds the root and blurts out his startled line.
- **v05c** · S05-L008–S05-L009 · 25.73–37.35s · `tree_dusk`: Trip over the paw, one tumble, and landing against Leo’s nose.
- **v05d** · S05-L010–S05-L011 · 37.35–44.21s · `tree_dusk`: Leo’s eyes open; cut closer on his face for his spoken question while tree geometry remains behind him.

### Audio Scene 06

- **v06a** · S06-L001–S06-L002 · 0.00–18.70s · `tree_dusk`: Leo lifts his head and places a paw beside Milo, blocking the same path.
- **v06b** · S06-L003–S06-L005 · 18.70–36.76s · `tree_dusk`: Hold the scale contrast as Milo freezes; both remain grounded.

### Audio Scene 07

- **v07a** · S07-L001–S07-L002 · 0.00–10.87s · `tree_dusk`: Leo speaks from his existing position, Milo listens.
- **v07b** · S07-L003–S07-L005 · 10.87–23.77s · `tree_dusk`: Milo apologizes and explains; Leo listens without lip motion.

### Audio Scene 08

- **v08a** · S08-L001–S08-L007 · 0.00–27.88s · `tree_dusk`: Leo considers his strength and softens while Milo waits.
- **v08b** · S08-L008–S08-L011 · 27.88–40.57s · `tree_dusk`: Leo speaks gently and lets Milo leave.
- **v08c** · S08-L012 · 40.57–44.39s · `tree_dusk`: Milo reacts in surprised relief and speaks.
- **v08d** · S08-L013–S08-L018 · 44.39–63.79s · `tree_dusk`: Leo reassures him; then narration holds on Milo’s reaction.
- **v08e** · S08-L019–S08-L021 · 63.79–72.75s · `tree_dusk`: Milo thanks Leo and promises to pass kindness on.
- **v08f** · S08-L022–S08-L024 · 72.75–83.37s · `tree_dusk`: Leo sends Milo home; reveal the open path and evening light.

### Audio Scene 09

- **v09a** · S09-L001–S09-L003 · 0.00–7.47s · `shortcut_dusk`: Milo heads home more carefully on the known shortcut.
- **v09b** · S09-L004–S09-L005 · 7.47–14.05s · `home_night`: Days pass; Milo resumes routine on the path to his burrow.
- **v09c** · S09-L006 · 14.05–18.22s · `tree_dusk`: Leo rests again beneath the established great tree.
- **v09d** · S09-L007 · 18.22–23.66s · `shortcut_dusk`: Empty established shortcut path foreshadows the next meeting; no newly designed forest.

### Audio Scene 10

- **v10a** · S10-L001–S10-L002 · 0.00–11.22s · `trap_morning`: Leo approaches a hidden trigger on the same trap path; his small step causes only a small size change.
- **v10b** · S10-L003–S10-L004 · 11.22–24.03s · `trap_morning`: Trigger and net action; mesh falls around his body with face and paws clear.

### Audio Scene 11

- **v11a** · S11-L001–S11-L007 · 0.00–21.17s · `trap_morning`: Leo tests the ropes and speaks in frustration while remaining at the same trap position.
- **v11b** · S11-L008–S11-L009 · 21.17–30.78s · `trap_morning`: He calls for help; closer face view then echo over the same forest path.

### Audio Scene 12

- **v12a** · S12-L001–S12-L003 · 0.00–11.33s · `run_morning`: Milo hears the call, recognizes Leo and speaks on the morning run path.
- **v12b** · S12-L004–S12-L007 · 11.33–20.73s · `run_morning`: Run montage over roots, between bushes and under branches, each a view of the one approved path.
- **v12c** · S12-L008–S12-L010 · 20.73–32.07s · `run_morning`: Milo continues toward the bright opening and recedes smoothly as narration explains his purpose.

### Audio Scene 13

- **v13a** · S13-L001–S13-L002 · 0.00–8.47s · `trap_morning`: Milo arrives at the same trap clearing and sees Leo in the net.
- **v13b** · S13-L003–S13-L005 · 8.47–19.07s · `trap_morning`: Leo warns Milo about the ropes; Milo listens.
- **v13c** · S13-L006–S13-L009 · 19.07–37.24s · `trap_morning`: Milo studies the mesh and moves toward the single closure loop.
- **v13d** · S13-L010–S13-L011 · 37.24–44.27s · `trap_morning`: Milo proposes using his teeth.
- **v13e** · S13-L012 · 44.27–47.09s · `trap_morning`: Leo asks about the teeth.
- **v13f** · S13-L013–S13-L014 · 47.09–52.58s · `trap_morning`: Milo answers playfully before any rope is cut.

### Audio Scene 14

- **v14a** · S14-L001–S14-L008 · 0.00–29.88s · `trap_morning`: Milo steadies and gnaws the one closure strand; intercut close details without shifting Leo or the plate.
- **v14b** · S14-L009–S14-L010 · 29.88–38.10s · `trap_morning`: Fibres fray and the same rope parts.
- **v14c** · S14-L011–S14-L014 · 38.10–53.61s · `trap_morning`: Milo steps clear; opening widens; Leo exits and net falls behind him.

### Audio Scene 15

- **v15a** · S15-L001–S15-L005 · 0.00–22.68s · `trap_morning`: Freed Leo thanks Milo and Milo jokes; hold their established left/right places.
- **v15b** · S15-L006–S15-L008 · 22.68–37.22s · `trap_morning`: Leo asks why Milo returned; Milo answers; Leo suggests repayment.
- **v15c** · S15-L009–S15-L010 · 37.22–43.38s · `trap_morning`: Milo rejects the debt idea; Leo asks what he means.
- **v15d** · S15-L011–S15-L015 · 43.38–61.44s · `trap_morning`: Milo explains kindness and the hope that it passes onward.
- **v15e** · S15-L016–S15-L023 · 61.44–103.47s · `trap_morning`: Leo reflects silently; use a face detail and a grounded shared view for his smile.

### Audio Scene 16

- **v16a** · S16-L001–S16-L006 · 0.00–24.33s · `tree_day`: Later at the great tree, the friends rest, joke and laugh in daylight.
- **v16b** · S16-L007–S16-L010 · 24.33–44.93s · `tree_day`: Hold the friends beneath the same tree as the narrator recalls and states the kindness lesson.
- **v16c** · S16-L011–S16-L012 · 44.93–56.74s · `tree_day`: Closing gentle view of the pair and tree; no extra destination or narrator figure.

The machine-readable line ranges, exact whole-line timing, plate paths, current overview panel links and supplemental board records are in [`visual_sequence_plan.json`](visual_sequence_plan.json). Character positions and depth sizing are in [`CHARACTER_STAGING.md`](CHARACTER_STAGING.md) and [`staging_plan.json`](staging_plan.json).
