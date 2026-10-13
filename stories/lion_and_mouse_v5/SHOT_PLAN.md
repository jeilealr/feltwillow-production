# Lion and Mouse v5 shot and image index

Historical v4-derived coverage plan carried into v5, not a selected edit. The
removed v4 repair map is available through Git history at
`stories/lion_and_mouse_v4/REPAIR_PLAN.md`; it is not an active v5 dependency.
Each scene link contains the v5 readable image and video prompts. Foundation
references come first.

The original 2026-09-30 plan had 118 image records, 43 coverage shots and 62
video-mode records before seed candidates. That pre-generation status is historical.

**Current tracked status:** `story.yaml` has 63 runtime shots including the later
`s05_tumble` bridge. The [render review](RENDER_REVIEW.md) records 186 takes in
the initial batch and three for the bridge (189 expected); local media/sidecars
are unavailable in this checkout. Owner take selection remains open. The
2026-10-02 image and no-render claims below are dated history. Each record's
`framing` (creation rules CR-15) and camera setup are in [prompts/](prompts/);
the “Location / geometry” column below is the 2026-09-30 plan.

[Foundation prompts](prompts/foundation.md): canonicals, views, calibrated poses, mouth designs, empty plates and prop material references.

| Order | Shot | Location / geometry | Mouth modes | Draft prompt records |
|---|---|---|---|---|
| 1 | `s01_explores` | stream_afternoon / solo | closed | [scene 01](prompts/scene-01.md) |
| 2 | `s01_acorn` | stream_afternoon / solo | functional | [scene 01](prompts/scene-01.md) |
| 3 | `s02_notice` | stream_sunset / solo | closed, mouth | [scene 02](prompts/scene-02.md) |
| 4 | `s02_stand_with_acorn` | stream_sunset / solo | closed | [scene 02](prompts/scene-02.md) |
| 5 | `s02_place_acorn` | stream_sunset / solo | closed | [scene 02](prompts/scene-02.md) |
| 6 | `s03_two_paths` | fork_sunset / solo | closed | [scene 03](prompts/scene-03.md) |
| 7 | `s03_decides` | fork_sunset / portrait_milo | closed, mouth | [scene 03](prompts/scene-03.md) |
| 8 | `s04_shortcut_run` | shortcut_dusk / run | closed | [scene 04](prompts/scene-04.md) |
| 9 | `s05_leo_sleeps` | tree_dusk / tree_pair | closed | [scene 05](prompts/scene-05.md) |
| 10 | `s05_paw_contact` | tree_dusk / tree_pair | closed | [scene 05](prompts/scene-05.md) |
| 11 | `s05_tumble` | tree_dusk / tree_pair → contact (same camera) | closed | [scene 05](prompts/scene-05.md) — bridge added 2026-10-05 (owner): Milo trips and rolls from the paw to the nose; Leo still asleep |
| 12 | `s05_nose_aftermath` | tree_dusk / contact | closed | [scene 05](prompts/scene-05.md) |
| 13 | `s06_barrier` | tree_dusk / tree_pair | closed | [scene 06](prompts/scene-06.md) |
| 14 | `s07_leo_annoyed` | tree_dusk / portrait_leo | closed, mouth | [scene 07](prompts/scene-07.md) |
| 15 | `s07_milo_sorry` | tree_dusk / portrait_milo | closed, mouth | [scene 07](prompts/scene-07.md) |
| 16 | `s08_leo_softens` | tree_dusk / portrait_leo | closed, mouth | [scene 08](prompts/scene-08.md) |
| 17 | `s08_milo_surprised` | tree_dusk / portrait_milo | closed, mouth | [scene 08](prompts/scene-08.md) |
| 18 | `s08_kindness` | tree_dusk / tree_pair | closed, mouth | [scene 08](prompts/scene-08.md) |
| 19 | `s09_milo_hurries` | shortcut_dusk / run | closed | [scene 09](prompts/scene-09.md) |
| 20 | `s09_stars` | tree_sky / empty | ambient | [scene 09](prompts/scene-09.md) |
| 21 | `s09_home` | home_night / solo | closed | [scene 09](prompts/scene-09.md) |
| 22 | `s10_curious_step` | trap_morning / trap_pair | closed | [scene 10](prompts/scene-10.md) |
| 23 | `s10_net_falls` | trap_morning / trap_pair | closed | [scene 10](prompts/scene-10.md) |
| 24 | `s11_pull_once` | trap_morning / trap_pair | closed | [scene 11](prompts/scene-11.md) |
| 25 | `s11_why_wont_it_break` | trap_morning / portrait_leo | closed, mouth | [scene 11](prompts/scene-11.md) |
| 26 | `s11_call` | trap_morning / portrait_leo | closed, mouth | [scene 11](prompts/scene-11.md) |
| 27 | `s11_waits` | trap_morning / trap_pair | closed | [scene 11](prompts/scene-11.md) |
| 28 | `s12_hears` | run_morning / run | closed, mouth | [scene 12](prompts/scene-12.md) |
| 29 | `s12_runs` | run_morning / run | closed | [scene 12](prompts/scene-12.md) |
| 30 | `s13_arrives` | trap_morning / trap_pair | closed | [scene 13](prompts/scene-13.md) |
| 31 | `s13_milo_confident` | trap_morning / portrait_milo | closed, mouth | [scene 13](prompts/scene-13.md) |
| 32 | `s13_leo_doubtful` | trap_morning / portrait_leo | closed, mouth | [scene 13](prompts/scene-13.md) |
| 33 | `s13_milo_playful` | trap_morning / portrait_milo | closed, mouth | [scene 13](prompts/scene-13.md) |
| 34 | `s14_gnaw_fray` | trap_morning / bite | functional | [scene 14](prompts/scene-14.md) |
| 35 | `s14_sever_R01` | trap_morning / bite | functional | [scene 14](prompts/scene-14.md) |
| 36 | `s14_milo_clear` | trap_morning / trap_pair | closed | [scene 14](prompts/scene-14.md) |
| 37 | `s14_opening` | trap_morning / trap_pair | closed | [scene 14](prompts/scene-14.md) |
| 38 | `s14_step_clear` | trap_morning / trap_pair | closed | [scene 14](prompts/scene-14.md) |
| 39 | `s14_free_hold` | trap_morning / trap_pair | closed, mouth | [scene 14](prompts/scene-14.md) |
| 40 | `s15_leo_amazed` | trap_morning / portrait_leo | closed, mouth | [scene 15](prompts/scene-15.md) |
| 41 | `s15_milo_modest` | trap_morning / portrait_milo | closed, mouth | [scene 15](prompts/scene-15.md) |
| 42 | `s15_leo_reflects` | trap_morning / portrait_leo | closed, mouth | [scene 15](prompts/scene-15.md) |
| 43 | `s15_milo_sincere` | trap_morning / portrait_milo | closed, mouth | [scene 15](prompts/scene-15.md) |
| 44 | `s16_friends` | tree_day / tree_pair | closed, mouth | [scene 16](prompts/scene-16.md) |

Each of these shots has its own start/end image records. The closed/mouth modes can share closed endpoints when motion happens and settles inside the clip; canonical mouth references still constrain the review. The functional nibble/gnaw shots use closed observing coverage as a separate editorial fallback. Empty scenery uses ambient mode.

**Historical planning note (2026-09-30):** full narration timing was pending
when this table was written. The later v5 timing artifacts and render review
supersede that status; this shot index alone does not certify full audio
coverage. Never assemble mouth variants sequentially merely to fill duration.
