# Development log — Phase 01, 18 October 2026

Starting state: feature/perceptual-world,
fcea46b788f6df8423f84bf14e54169f15a383e3. No commit or branch change requested;
work remains uncommitted on this existing non-main branch. Five existing
untracked .DS_Store files were left alone.

1. Read repository instructions and current v6 handoff. Full request explicitly
   authorizes read-only Git status/diff checks, superseding CLAUDE's general
   owner-does-Git rule for those checks only. No add/commit/push.
2. Read listed current policy/foundation/staging files and searched for missing
   POSE_REFERENCE_REVIEW/SCENE_REVIEW. Current FOUNDATION_REVIEW/README,
   atlas and KEYFRAME_REVIEW supply their replacement context. Selected sources
   remain v6-local; no historical v5 visuals used.
3. Inspected four Leo image files and nine active Scene 05 images together;
   opened neutral and plate at native detail. Wrote identity/environment
   extraction before geometry. Captured exact hashes in config/authority.json.
4. Installed Blender 5.2.2 confirmed; no add-ons needed. Sandboxed background
   startup crashes before Python (native startup crash). Authorized local
   outside-sandbox execution works. No Blender installation/version change.
5. Native scripted construction: editable sphere/curve forms, chunked spiral
   mane, felt shader, short surface fibers, four two-bone IK chains, neutral,
   walk, low rest, struggle and head-turn controls. Separate environment library
   contains root fan, r02 stumble root, path, stones, stream, hills, canopy and
   repeated foliage. Source image is never used as a rendered background.
6. First Cycles image looked smooth and overlit. Reduced studio energy and
   sheen, darkened mane pigment, added bounded short wool fibers, voxel-welded
   torso/chest/rump with a spinal weight blend. Remaining segmented limb
   topology is explicitly a production limitation.
7. Native render inspection found fibers ignoring rotated limb transforms,
   side-view tail clipping, studio floor geometry entering image, and a broken
   relative linked-library path after save. Corrected world-space fiber sampling,
   enlarged side framing, used a flat studio plane, deferred relative library
   conversion until scene save. Structural tests reopen the files and exercise
   real IK motion, rather than only checking object names.
8. Registered crop cameras share the same perspective center and lens family;
   crop centers are preserved from selected keyframes. They are explicitly
   provisional matches, not assertions that the source 2D perspective is solved.
9. Render actual review views, pose demonstrations and equal-settings engine
   trials. Manifests retain measured timings and exact output hashes. No video,
   audio, production plan or original image changes.

## Continuation

Read final report and comparisons before changing shapes. The next useful
iteration is Leo's side/rear mane silhouette, organic curls, continuous limb
forms and eye/muzzle integration, then set landmark/camera calibration.
Do not infer anatomical correctness from finite matrices or successful rendering.
Owner review remains required. A full rebuild is the reproducibility authority;
individual helper invocations during debugging are not alternative production
recipes. Native mesh/curve contents remain editable in each library.

10. Final camera calibration moved the left stone, right rock and root tip closer
to measured plate positions, localized the sky warm band to the left, and moved
bark ridges onto the variable trunk surface. Added an actual camera-aligned
viewport overlay. Reran final scene renders and 52 structural checks. The art
gaps remain explicit in the report. Orthographic diagnostic camera origins were
raised after contact-sheet inspection found below-floor ray artifacts.

11. Added an evaluated surface-proximity assertion after correcting fiber bone
parent inverse matrices. The final 52/52 checks pass; all character/scene review
images were regenerated from that binding. Render receipts bind both the scene
and any linked library bytes, preventing stale comparisons after library edits.
