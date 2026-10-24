**Current S06/S07 staging:** S06 is connected on the selected S05 camera/plate: Leo remains lying, raises head/chest, then places a FRONT paw beside Milo. Milo stays on viewer screen-right, looks up-left and is not grabbed/pinned. The S05 trip used a REAR paw. S07 uses separate matched portrait families: Leo L001/L002 looking down-right; Milo L003–L005 looking up-left. No full-standing Leo event. See review/character_performance_consistency_r001/s06_s07_pose_planning_r001/REVIEW.md.

**Current S05 staging:** Follow the latest [owner sequence](review/scene_compositions/s05_owner_sequence_through_trip_r003/REVIEW.md). L005–L006 Milo only at root, L007 Milo portrait, first joint appearance L008 contact; stop for size/obstruction review before further sequence images. L001 sleeping Leo is selected; old joint L005 is superseded. Later historical summaries below do not override this direction.

**S04–S05 candidates:** [Current review](review/character_performance_consistency_r001/s04_s05_pose_planning_r001/REVIEW.md): 15 transparent Milo pose candidates saved; one forward-pitch request has an unresolved connection failure, with no retries. Leo identity bytes are owner-reconciled in [the exact-hash record](owner_leo_canonical_reconciliation_r001.json); his pose generation remains a separate proposed operation. All new poses await review, and scene-contact/anatomy measurements remain pending.

**S04–S05 next pose pass:** [Requirements](review/character_performance_consistency_r001/s04_s05_pose_planning_r001/PERFORMANCE_REQUIREMENTS.md) and [exact Milo proposal](review/character_performance_consistency_r001/s04_s05_pose_planning_r001/OPERATION.md) plan 16 new Milo pose variants, with four Leo sleeping/portrait requirements held on canonical-byte reconciliation. No generation submitted. S04 is independent per line; S05-L001 reveals Leo, L002–L004 cut to sleeping details, L005–L009 share one planned locked background, L008 has four keys, and L010–L011 share portrait body geometry. S01–S03 selected bytes remain unchanged.

# V7 character staging

The [audio-line plan](audio_visual_plan.json) selects shots and explicit continuity; [character_library.json](character_library.json) preserves canonical identity, hashes and approval provenance. Location freedom changes camera, never anatomy.

Milo is a compact felt mouse without visible teeth, including later gnawing action unless an explicit approved design change exists. Leo is the approved felt lion with rounded warm golden-cream paws, no sharp claws or grey nails. Same-depth standing-equivalent Milo/Leo scale is 0.25; do not apply it mechanically to single-character portraits. Review anatomical dimensions, physical support, contacts, occlusion and perspective for each new view.

Narrator voice-over never drives character mouths. Character dialogue requires the explicit later dialogue/lip-sync pipeline; stills keep closed mouths rather than arbitrary baked speech shapes. Close-ups preserve identity and do not resize anatomy.

World-state events preserve acorn custody, sleeping/waking Leo, the blocking paw, grounded paws under the net, trigger/net/rope causality and offscreen cast through cuts. S05 tumble/roll/landing and S06 scramble require later contact/pose review; planned staging is not image approval.

Known readiness blocker: Leo canonical actual hash `1c4f773d04c5e6f7229448bfe00caf7f610d427f5dc0d145cba57e7671a59362` differs from ledger hash `6b587c8ee2739767bb7af056ee3176ec3d2e698a5bed0e013263814ee8059545`. The actual transparent derivative and inherited source approval are preserved. Reconcile with the owner before treating those bytes as approved. Milo provenance remains unchanged.

## Camera-relative size

Milo's apparent size is camera-relative: greater viewing distance makes him smaller, and closer distance, lens/zoom or cropping can make him larger. Compare size only after accounting for camera distance, lens/zoom, crop, subject depth and pose. At the same camera setup and subject depth, anatomical dimensions and scale relative to local landmarks must remain consistent; pose may change his bounding box. Independent wide shots and portraits do not require the same frame fraction. Record intentional camera/depth changes; do not invent measured distances or diagnose drift from screen size alone.

S03-L006–L008 locks camera and standing depth, so compare stable head/body landmarks against that shared setup. A mismatch there remains a review issue, not a confirmed anatomical defect without this comparison.

## Performance planning and review

The [versioned performance library](character_performance_library.json) owns reusable pose/expression requirements, while the existing audio-visual plan owns per-image bindings. Read the [contract](../../docs/character-performance-library.md), [derived requirements](derived/PERFORMANCE_REQUIREMENTS.md) and [native-image audit](review/character_performance_consistency_r001/REVIEW.md). Three Milo foundation candidates are generated and pending owner review; no performance asset is approved; existing scene candidates keep their original bytes and review status. Identity, performance approval, shot staging and scene approval are distinct. Leo identity bytes remain unresolved; S13–S16 audio remains pending.
