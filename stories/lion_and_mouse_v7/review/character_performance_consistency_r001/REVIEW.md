# Existing-image character consistency audit

All 24 original PNGs decoded and opened at native resolution in this review; image hashes identify the inspected bytes. Original PNGs, sidecars, operation and receipts remain untouched. Findings are advisory; only the owner selects artwork.

Starting branch/HEAD and all pre-change hashes: BEFORE.json. VISUAL_OBSERVATIONS.json contains appended manual evidence; AUDIT.json contains measured pixel evidence and file bindings.

## Findings

- Walking L001 / winding-path / deeper-trail: compactness and leg extension differ, with different gait and oblique projection. Suspected proportional drift in L001 needs matched-view review; camera_unknown prevents a confirmed size verdict. Shared three-quarter screen-right lightstep family is proposed, not approved.
- S03-L004: large head impression is suspected, confounded by projection; stepping also suggests early route commitment. Bind proposed stationary consideration instead of maximizing walk reuse.
- S02-L003: useful startled portrait inspiration, minimal far-ear top clearance confirmed; larger frame occupancy is consistent with portrait framing and does not prove changed anatomy. No portrait-master approval.
- Fixed-fork: approximate foot-root shifts and body extents are visible against a common background. Shared-root contract is unmet. Head turn changes projected extent, so anatomy/scale suspicion remains separate from the confirmed placement/pixel failures.
- No v6 performance atlas was adopted or used as authority.

## Comparable fixed-camera evidence

Manual body+ears boxes exclude tail and whiskers, tolerance about 15 px; foot-root is approximate support midpoint. These are review landmarks, not calibrated anatomy. No metric camera distance is known.

| Image | Body+ears box xyxy | Root xy |
|---|---|---|
| S03-L006-B01-I02 | [466, 277, 831, 814] | [720, 803] |
| S03-L007-B01-I02 | [713, 226, 1115, 826] | [878, 815] |
| S03-L008-B01-I02 | [577, 266, 894, 783] | [749, 775] |

Pixel ROI: native `[0,0,1672,200]`, away from actors/contact shadows. No resize or registration. Against the master, about 99% of pixels differ with mean channel differences only about 5–6/255. This proves lack of byte-identical background pixels, not a large perceptual/geographic change.

## Per-image observations

| Image | Verdict | Evidence / limitation |
|---|---|---|
| S01-L001-B01-I02 | suspected_defect | Bent/lifted trailing leg and more forward torso make this walker look shorter than the straighter winding-path walker. Head/body balance may differ, but oblique pose and unknown camera prevent a confirmed anatomy verdict. Short sturdy limbs and curved orange tail remain readable. Compare head-to-torso landmarks at matched head angle, not total pixel height; walking family proposal is three-quarter screen-right. |
| S01-L002-B01-I01 | not_comparable | Unique reaching pose: near hand lifts to berries, both feet planted, torso angled toward branch. A valid one-off requirement, not a walking reference. Inspect hand/berry contact and retain canonical torso/ear construction; no performance approval inferred. |
| S01-L002-B02-I01 | not_comparable | Crouched/leaning log inspection with hands at rim and bent legs; body height cannot be compared to upright walkers. Pose-specific ground and rim contact review needed. |
| S01-L002-B03-I02 | not_comparable | Three-quarter walker facing right, lifted forward foot and relatively upright torso. Appears longer-legged than L001, with different gait phase. Camera_unknown; do not normalize the entire mouse to one height to infer anatomy. |
| S01-L003-B01-I02 | not_comparable | Right-facing explorer with two low visible feet and straighter upright posture than L001. Tail curves behind left. Shared lightstep family is plausible after view review. Independent environment/camera; physical size comparison unavailable. |
| S01-L004-B01-I01 | not_comparable | Native PNG inspected: felt mouse/action or environment is visible. No defensible cross-shot anatomical measurement was established for this independent pose/framing. camera_unknown; retain pending owner review. |
| S01-L004-B01-I02 | not_comparable | Native PNG inspected: felt mouse/action or environment is visible. No defensible cross-shot anatomical measurement was established for this independent pose/framing. camera_unknown; retain pending owner review. |
| S01-L004-B02-I01 | not_comparable | Native PNG inspected: felt mouse/action or environment is visible. No defensible cross-shot anatomical measurement was established for this independent pose/framing. camera_unknown; retain pending owner review. |
| S01-L004-B03-I03 | not_comparable | Native PNG inspected: felt mouse/action or environment is visible. No defensible cross-shot anatomical measurement was established for this independent pose/framing. camera_unknown; retain pending owner review. |
| S02-L001-B01-I02 | not_comparable | Native PNG inspected: felt mouse/action or environment is visible. No defensible cross-shot anatomical measurement was established for this independent pose/framing. camera_unknown; retain pending owner review. |
| S02-L002-B01-I02 | not_comparable | Environment-only shadow cutaway, no visible actor; no pose or anatomy comparison applies. camera_unknown; retain pending owner review. |
| S02-L003-B01-I01 | confirmed_defect | Portrait ear clearance is minimal at the top edge (far-ear fuzz reaches the border region); full-head/ear margin needs review. Rounded muzzle, green eyes and closed mouth remain recognizable; no teeth seen. The face is larger because this is deliberately a portrait. Exact anatomy comparison with neutral canonical is not proven by the crop; expression-base inspiration only. |
| S02-L004-B01-I02 | not_comparable | Native PNG inspected: felt mouse/action or environment is visible. No defensible cross-shot anatomical measurement was established for this independent pose/framing. camera_unknown; retain pending owner review. |
| S02-L004-B02-I03 | confirmed_defect | Acorn sits ON the mossy stone; narration says beside a stone. The preceding standing shot has a different stone/camera arrangement. Contact-chain and story placement defect, separate from anatomical scale. |
| S03-L001-B01-I02 | not_comparable | Native PNG inspected: felt mouse/action or environment is visible. No defensible cross-shot anatomical measurement was established for this independent pose/framing. camera_unknown; retain pending owner review. |
| S03-L002-B01-I02 | not_comparable | Native PNG inspected: felt mouse/action or environment is visible. No defensible cross-shot anatomical measurement was established for this independent pose/framing. camera_unknown; retain pending owner review. |
| S03-L003-B01-I02 | not_comparable | Native PNG inspected: felt mouse/action or environment is visible. No defensible cross-shot anatomical measurement was established for this independent pose/framing. camera_unknown; retain pending owner review. |
| S03-L004-B01-I02 | suspected_defect | Head/ears read large above narrow torso, but foreshortening and lifted forward step confound anatomical inference. The stepping silhouette also suggests entering the shortcut before the decision. Use stationary route-considering performance; camera_unknown, head-size defect remains suspected rather than confirmed. |
| S03-L005-B01-I02 | suspected_defect | Lifted stepping foot and body directed into the dark route can imply premature commitment. Prefer stationary route emphasis before decision; no universal screen-size target. |
| S03-L006-B01-I02 | confirmed_defect | Compared with L007/L008, foot/root placement changes in the same fixed-camera fork setup. Full body is left of L007 and head angles up. Confirmed contract failure: shared root/contact not retained. Head projection changes with gaze; anatomical resizing remains suspected, not measured as physical truth. |
| S03-L007-B01-I02 | confirmed_defect | Actor is substantially farther right than L006/L008; ear-to-foot extent grows. Gaze/body angle turns left. Root shift is confirmed under declared lock; size suspicion needs head-angle-aware measurement. Background pixel lock fails in top ROI. |
| S03-L008-B01-I02 | confirmed_defect | Actor moves back left and feet sit higher on the canvas than L007; gaze turns right. Root/depth contract failure, not legitimate free camera variation. Background pixel lock fails in top ROI. |
| S03-L009-B01-I01 | camera_explained | Portrait crop intentionally shows a much larger face/upper body than the fork wide shots; screen-size difference alone is not a defect. Background retains more detail than the requested strong blur. Camera distance is not measured; framing explains screen occupancy only, not a proof of anatomical identity. |
| S03-L010-B01-I01 | camera_explained | Portrait with fuller ear margin and softer background than L009; slight determined/hopeful facial change, mouth closed, no teeth. Separate cut permits crop/scale change; still requires a compatible reviewed portrait-expression base. |

## Review pack

Open review.html using the local loopback server. Full-line WAV controls remain unchanged. Toggle native size or overlays; browser verdict selectors are unsaved discussion placeholders and grant no approval. Contact sheets use complete-frame fit, never normalized actor height. The original canonical is shown separately; a crop/lighting match is not owner acceptance.

Performance requirements: ../../derived/PERFORMANCE_REQUIREMENTS.md. All current registry references are planned; zero generated/approved performance assets.
