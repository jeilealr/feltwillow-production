# v6 background continuity map

This map answers which scenes share a place and when a lighting variant or location change is intentional. The approved plate files listed here are the background authorities. A storyboard panel may change framing, but must preserve the same landmarks and ground layout unless this map explicitly calls out a transition.

**Important:** storyboard boards **and the 92 individual keyframe candidates** were generated with these plates as references, but they may redraw the surroundings. They are not certified pixel-identical plates. For video endpoints, keep the approved plate fixed and composite reviewed characters/props or use controlled crops and focused edits when exact continuity matters. See the [keyframe continuity audit](KEYFRAME_CONSISTENCY_AUDIT.md) and [video boundary plan](video_boundary_plan.json). Do not add an unapproved background.

| Scene(s) | Intended background continuity | Approved plate(s) |
|---|---|---|
| 01–02 | Same stream-bank place; afternoon becomes sunset. This is a lighting change, not a new location. | `stream_afternoon_r01.png` → `stream_sunset_r01.png` |
| 03 | Fork at sunset. Scene 04 leaves for a different path. | `fork_sunset_r01.png` |
| 04 | Shortcut path at dusk. Scene 09 revisits it only as a montage beat. | `shortcut_dusk_r01.png` |
| 05–08 | One continuous encounter beneath the great tree at dusk. Preserve the same tree, path, roots, and clearing layout across all four scenes. | `tree_dusk_r01.png` |
| 09 | Intentional days-passing montage across three existing places; it is not one continuous background. | `shortcut_dusk_r01.png`, `tree_dusk_r01.png`, `home_night_r01.png` |
| 10–11, 13–15 | Same trap clearing and morning plate. Scene 12 briefly follows Milo on a separate path; Scene 13 returns to the same trap background. | `trap_morning_r01.png` |
| 12 | Milo’s run along the separate morning path; then return to the trap clearing in Scene 13. | `run_morning_r01.png` |
| 16 | Later revisit to the great tree in daylight. Same recognizable place/geography as Scenes 05–08, with the approved day lighting variant. | `tree_day_r01.png` |

Character positions, size ratios and movement through depth are in [`CHARACTER_STAGING.md`](CHARACTER_STAGING.md) and [`staging_plan.json`](staging_plan.json).

Full paths, per-panel actions, and ordered reference roles are recorded in [`scene_plan.json`](scene_plan.json). The scene-by-scene outline is [`SCENE_PLAN.md`](SCENE_PLAN.md), and generated candidates are in [`SCENE_REVIEW.md`](SCENE_REVIEW.md).
