# Lion and Mouse v5: render review (agent, 2026-10-05)

This is the **initial 2026-10-05 review batch**: 62 runtime shots, 3 seeds each, fast mode (Wan 2.2 I2V A14B + Lightning, 4 steps,
CFG 1, 81 frames at 16 fps, 1280x720): **186 clips** in
`work/stories/lion_and_mouse_v5/shots/<shot>_s<seed>_fast.mp4` (+ `.json` sidecar). Rendered
2026-10-04 23:30 to 2026-10-05 09:31 in 7 dev-g jobs (`lumi/render_story.sh`); median
9.2 min per seed after a ~30 min model load per shot (the first jobs ran ~17 min per seed).

The later `s05_tumble` bridge below adds three historically reported takes, so the
tracked runtime plan has 63 shots and 189 expected takes. This checkout lacks the
ignored v5 shot media; current MP4 and sidecar counts remain unverified.

Evidence: one contact sheet per scene, every take on a row, frames 0/20/40/60/80:
`work/stories/lion_and_mouse_v5/review/sceneNN.jpg`. This is a contact-sheet review only:
**watch the clips at normal speed** before choosing (Gate D); trajectories, gait and mouth
timing are not visible on a sheet. Mark chosen takes by renaming with a `best_` prefix.

## Summary

- Identity holds in every clip: Leo's rust-red mane and brown eyes, Milo's smooth crown and
  coral ears, the felt look and the plates. No duplicate characters seen.
- The big v3 problem beats now work: **the net falls on Leo in all 3 `s10_net_falls` takes**,
  and Leo walks out of the opened net in all 3 `s14_step_clear` takes.
- **Scene 15 is the weak scene** (see below): fix the prompt and re-render before choosing.
- Recurring take-level faults: unrequested paw lifts into close-ups; a few takes cut or zoom
  to another framing mid-clip. Most shots have at least one clean take.

## Per scene (problems are per take; "ok" = nothing wrong on the sheet)

| Scene | Shots | Notes |
|---|---|---|
| 1 | explores, acorn | ok; Milo walks cleanly in all explores takes. acorn: very small motion. |
| 2 | notice, stand_with_acorn, place_acorn | ok; wide frame, Milo small, motion subtle. |
| 3 | two_paths, decides | ok; `decides_closed s3` paws rise into frame (frame 60). |
| 4 | shortcut_run | ok, all 3 run cleanly. |
| 5 | leo_sleeps, paw_contact, nose_aftermath | ok; Milo tiny in paw_contact; Leo wakes at the end of nose_aftermath as planned. |
| 6 | barrier | start = end image, so a hold; ok. |
| 7 | leo_annoyed, milo_sorry | leo_annoyed: paws rise into frame in `closed s2`, `mouth s1`, `mouth s2`; others ok. milo_sorry closed: paws come up (wringing) in all 3, mouth opens in `closed s1`; milo_sorry mouth takes ok. |
| 8 | leo_softens, milo_surprised, kindness | leo_softens ok (tail tip shows in some). **milo_surprised: Milo closes his eyes and clasps his paws mid-clip in all 6 takes**, so it reads as gratitude rather than surprise; kindness ok. |
| 9 | milo_hurries, stars, home | ok. |
| 10 | curious_step, net_falls | curious_step: little movement. **net_falls: works in all 3.** |
| 11 | pull_once, why_wont_it_break, call, waits | ok; mouth takes show speech. |
| 12 | hears, runs | ok; Milo very small in the wide. |
| 13 | arrives, milo_confident, leo_doubtful, milo_playful | Milo small at the left edge: his mouth is unreadable in the `mouth` takes (the known S13 framing issue). Leo blinks/winks in some. leo_doubtful ok. |
| 14 | gnaw_fray, sever_R01, milo_clear, opening, step_clear, free_hold | gnaw/sever: motion subtle; check at full speed whether the rope visibly frays and parts. opening and step_clear work; free_hold ok. |
| 15 | leo_amazed, milo_modest, leo_reflects, milo_sincere | **Intrusions.** leo_amazed: paws rise into the portrait in 5 of 6. milo_modest: a leaf lands on Milo's head (s1, s2, mouth s1, s2); `mouth s3` cuts to a wide shot: reject. leo_reflects: a branch/twigs enter over his head in most takes. milo_sincere: leaves on his head in most; `mouth s3` changes framing: reject. |
| 16 | friends | ok. |

## Why scene 15 fails, and the fix

The close-up prompts name things that must stay out of frame: "The overhead branch stays
empty" and "paws and tail stay outside the portrait". Fast mode runs at CFG 1 with no negative
pass, so naming an object pulls it into the picture: Wan drew the branch, its leaves and the
paws (the same mechanism as v2's landmark lesson, `CLAUDE.md` "background:" note).
Fix in the bible/templates (CR-18), not in rendered text: for close-ups, drop the
overhead-branch and net-state clauses and the "outside the portrait" wording, and describe
only what is in frame ("head and shoulders portrait; paws rest low out of view" → better simply
"head and shoulders portrait, still body"). Then re-export and re-render scene 15 (and
optionally the paw-lift close-ups of S03, S07). Owner decision.

## Added after the review

- 2026-10-05, owner: bridge shot `s05_tumble` (Milo trips over the paw and rolls to Leo's nose,
  Leo still asleep), between `s05_paw_contact` and `s05_nose_aftermath`; 3 seeds rendered
  (job 22545089). Endpoints are the existing images, so no new stills.

## Not done (needs the owner)

- Take selection (rename with `best_`).
- Scene 15 prompt fix and re-render; S08 `milo_surprised` expression intent.
- The timing sheet's gaps (scenes 8, 15, 16 need more picture than the shots give).
- No animatic or assembly was made.
