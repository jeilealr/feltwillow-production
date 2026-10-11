# lion_and_mouse_v6 video scene boundaries

**Status:** planning only. The listed PNGs are unapproved candidates; no video is render-ready from this table. Run `python3 production/keyframe_visual_gate.py --story lion_and_mouse_v6` before video export.

The start image is the first boundary of that audio scene and the end image is its last boundary. At a shared entry, the previous scene's **exact end PNG** becomes the next scene's start PNG; its first own keyframe is the next motion target. A change of crop is a cut unless a separate zoom path is approved. Internal cuts and chronological frame order are in [`video_boundary_plan.json`](video_boundary_plan.json).

| Scene | Entry | Start boundary | First own image | End boundary | Ordered images |
|---|---|---|---|---|---:|
| 01 | Story opening | `s01_p01` | `s01_p01` | `s01_p04` | 7 |
| 02 | Same bank, approved afternoon-to-sunset lighting change | `s02_p01` | `s02_p01` | `s02_p03` | 3 |
| 03 | New fork location | `s03_p01` | `s03_p01` | `s03_p04` | 4 |
| 04 | Fork-to-shortcut location change | `s04_p01` | `s04_p01` | `s04_p04` | 7 |
| 05 | Shortcut-to-great-tree location change | `s05_p01` | `s05_p01` | `s05x_p04` | 8 |
| 06 | Same tree, close-to-wide camera change | `s06_p01` | `s06_p01` | `s06_p03` | 3 |
| 07 | Same tree, close-to-medium camera change | `s07_p01` | `s07_p01` | `s07_p04` | 4 |
| 08 | Exact shared image from Scene 07; same plate and crop | `s07_p04` | `s08_p01` | `s08_p06` | 6 |
| 09 | Days-passing location montage begins | `s09_p01` | `s09_p01` | `s09_p04` | 4 |
| 10 | New morning trap location | `s10_p01` | `s10_p01` | `s10_p03` | 3 |
| 11 | Exact shared image from Scene 10; same plate and crop | `s10_p03` | `s11_p01` | `s11_p04` | 4 |
| 12 | Cut from trap to Milo's separate run path | `s12_p01` | `s12_p01` | `s12_p04` | 7 |
| 13 | Cut from run path back to trap clearing | `s13_p01` | `s13_p01` | `s13_p06` | 6 |
| 14 | Exact shared image from Scene 13; same plate and crop | `s13_p06` | `s14_p01` | `s14_p06` | 6 |
| 15 | Same trap clearing, wide-to-medium camera change | `s15_p01` | `s15_p01` | `s15_p06` | 12 |
| 16 | Later daytime great-tree visit | `s16_p01` | `s16_p01` | `s16x_p03` | 8 |

Each internal transition in the JSON also has explicit candidate `start_image` and `end_image` paths. On a camera/location cut, the outgoing endpoint remains its own image and `next_start_image` begins the next view; never morph the two views. `same_view_motion_candidate` uses the next PNG as its proposed end. Its actual pixels, identity, scale, landmarks and ground contact must still pass review. See [`KEYFRAME_CONSISTENCY_AUDIT.md`](KEYFRAME_CONSISTENCY_AUDIT.md).

Cuts within a long narrator line need word-level timing before clip durations or edit points are final. Only character dialogue gets lip-sync.
