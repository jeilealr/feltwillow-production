# Character performance, ambient motion and audio

## Keep the story first

Use finalized narration and dialogue to determine visual intention and duration. Preserve the existing Feltwillow audio provenance and speaker IDs. Do not force every line into the same five-second loop, or trim speech merely because a stock animation is shorter. Use framing, reaction and meaningful quiet holds to support comprehension.

For every interval write: start state, one primary action, emotional change, end state, contacts, speaker, prop event, camera and permissible secondary motion. A long explanation can use deliberate portrait cuts and attentive listening, not constant gestures. Silence and stillness are valid performance choices.

## Pose-to-pose before polish

Block key poses and timing in a plain preview. Check silhouette, gaze, weight and attention. Add breakdowns for arcs and contact changes, then interpolation cleanup. Only add secondary motion after the action reads. A generated/retargeted cycle is a starting asset; it still needs staging, timing and contact correction.

Match root travel to the locomotion cycle. Test starts, stops, turns and transitions to sitting/lying/flying/swimming, since isolated loops conceal problems. Do not use an unchanging cycle speed for a character that travels different distances. Separate repeated motion from the narrative action that changes direction or intent.

## Handmade cadence

Do not automatically reduce the whole film to a low FPS because the target is stop-motion-like. Delivery FPS, stepped key exposure, camera movement, motion blur and ambient motion are separate artistic choices. Test a smooth version and a deliberately stepped performance with the owner. Very thin felt fibers and moving cloud cards may alias badly with aggressive stepping. Preserve audio duration exactly regardless of chosen exposure style.

Consider slight asymmetry and restrained timing variation; do not reseed pose noise every frame. Small imperfections should express a handmade object, not technical instability. Keep rig scale fixed through the movement.

## Mouths and faces

Narrator voice-over never activates character speech. Bind one explicit speaker and the relevant audio span. Silent listeners may react with eyes/posture, not accidental mouth motion. Use per-character shape/rig controls, not a universal human lip solution. Verify v6 Milo's no-visible-teeth rule even at wide jaw poses or gnawing contacts.

Respect the current closed-boundary convention for the existing keyframe/lip-sync pipeline. For a new native Blender facial workflow, propose and approve the mapping from audio to rig controls, endpoint rules and export mode before changing production. Do not run the legacy image-mouth compositor on a Blender take that already contains finalized speech animation. Separate a mouth calibration asset from a story boundary frame.

Frame-accurate speech alignment does not by itself create good acting. Keep chest/shoulders/head orientation stable on expression-only portraits where current owner direction requires it. Avoid adding head bobs for each syllable. Validate blinks and eye direction at normal playback speed.

## Ambient motion

Use the environment presets and absolute story time. Neighboring plants can have stable phase offsets around a shared wind direction; a new shot must not restart them at frame one. Water flow continues at the same speed, clouds at the same position, and shadows at the same light state unless an event changes them. Animation is not permission to move fixed landmarks.

Keep a per-shot motion budget: primary action, perhaps breathing/blink, and a few quiet environmental cues. Show an ambient-off comparison when the scene feels busy. Restrained visual motion is particularly important while a child listens to narration.

## Review tests

Review the entire interval with audio, then muted for visual clarity. Sample before/after contacts and the middle of interpolation. Check foot/paw skating, floating, wing/root/prop collisions, eye aim, mouth timing, stable mane/ears, distracting loops, ambient reset and motion blur. Compare shared joins at normal speed and frame-step. Confirm a held pose still has believable support.

Log accepted animation with rig revision, source hashes, timing, control curves and state boundaries. A motion approved for one body plan is not automatically approved for another. Keep character-specific actions and reusable mechanisms distinct.

## Limited use of automatic animation

Auto-rigging or stock motion can save setup for a compatible body plan [A01](sources.md#a01), [A02](sources.md#a02), but game locomotion does not guarantee expressive story performance. First test a small known action; do not upload all actors or purchase a library on an assumption. Record motion asset rights and attribution obligations separately from the software license.

Blender Studio's animation and rigging training [S02](sources.md#s02), [S03](sources.md#s03), [S04](sources.md#s04) are deeper learning paths. Only their publicly accessible outlines were reviewed here, not every paid lesson or exercise. This module is an original production approach, not a reconstructed copyrighted course.
