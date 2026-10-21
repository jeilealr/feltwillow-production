# Character proportion profiles and review

Create a **separate, versioned proportion profile after selecting each character's first canonical identity image**. Bind it to the exact canonical ID/revision/path/hash. Calibrate anatomy from that character, with additional matched-angle canonical views only when needed. A mouse and lion have different anatomy and different useful measurements; never copy Milo's numbers, body landmarks or tolerance bands into Leo's profile. The active profiles are authored once under `character_performance_library.json` → `anatomy_policies.<actor>.ratio_profile`; reports and galleries are derived.

## Canonical → profile → performance → scene

1. Select the canonical identity and reconcile its actual bytes with the owner ledger. Preserve the original.
2. Annotate visible anatomical landmarks at native resolution, recording uncertainty, occlusion and head/body angle. Keep hidden joints unknown. A single image cannot reveal true 3D limb lengths or anatomy hidden by a mane.
3. Calculate character-specific projected ratios and review the target/tolerance with the owner. Distinguish a measured canonical baseline, a requested design target and an uncalibrated metric. Do not turn an approximate measurement into an invented exact baseline.
4. Before generating a performance, attach its canonical, proportion reference and compatible reviewed pose/portrait references. Include only the applicable calibrated ratio targets in the concrete prompt. No extra generation is authorized by a profile.
5. Compare the candidate at compatible view, articulation and projection. Preserve source hashes, measured coordinates, uncertainty, applicable/not-comparable reasons and the result. Owner acceptance of acting and pose is separate from anatomy/prop/scene readiness.
6. At shot staging, apply only uniform whole-character scale/translation. Independent camera views may show different pixel sizes. Fixed camera and standing depth share root/contact and anatomical scale. Never repair a failed ratio by shrinking the head, stretching legs or enlarging hands separately.

A canonical replacement invalidates its profile calibration and dependent anatomy reviews; it does not silently transfer approvals. An approved pose may provide clearer comparable-view evidence, but it does not replace canonical identity. Leo's unresolved canonical ledger/actual-byte mismatch blocks numerical calibration; profile definitions can still be planned.

## Definitions and uncertainty

All lengths are dimensionless **ratios of measurements from the same character in a compatible projection**. Keep left/right and near/far measurements separate. Do not normalize a feature using the entire PNG, tail span, ear-tip span, lifted arm or changing pose bounding box. Do not infer physical viewing distance from pixel height.

Milo's current owner-requested **projected head fraction** is:

`(skull crown to chin, excluding ears) / (skull crown to supporting sole)`

The target is **0.39 ±0.01 absolute ratio units**, or **0.38–0.40**. This interprets the owner's “±1” as one percentage point, not ±1 whole ratio unit or ±1% relative. The owner updated the earlier 0.37 target to 0.39 after seeing the approximate canonical baseline. Native-image surface landmarks and conservative uncertainty intervals are documented in [the calibration report](../stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/MEASUREMENTS.md); these are projected measurements, not exact 3D anatomy or automatic passes. Apply it to a comparable upright Milo view with matched head pitch and support—not to crouches, rolls, jumps, tilted heads or portrait crops.

For uncertain lengths, report a conservative ratio interval:

`lower = max(0, numerator − numerator_error) / (denominator + denominator_error)`

`upper = (numerator + numerator_error) / (denominator − denominator_error)`

Use `within_band` only when the whole interval lies inside the band; `outside_band` when intervals are disjoint; `uncertain` when they overlap; `not_comparable` when projection/occlusion is unsuitable. An outside-band projected measurement flags review, not automatic regeneration or proof of a 3D defect. A point estimate rounded to 0.39 cannot pass a ±0.01 band if annotation uncertainty is wider. The earlier ±20-pixel landmarks are screening evidence and require refinement for this tighter target.

## Milo: mouse-specific profile

The head-fraction design target is owner-selected. The calibration report now supplies visible canonical reference measurements and intervals for applicable ratios; targets/tolerances for other metrics remain pending owner review. Hidden joint ratios remain null, with separately named surface proxies rather than invented skeleton measurements.

| Ratio | Landmarks / purpose | Applicability |
|---|---|---|
| Head fraction | Crown–chin / crown–supporting sole | Upright, matched head pitch; excludes ears |
| Head-to-torso | Crown–chin / neck base–pelvis center | Torso readable, compatible pitch; not hidden under bowed head |
| Torso-to-leg | Neck base–pelvis / hip–knee–ankle chain | Compare joint chains, not compressed crouch height |
| Upper/lower arm | Shoulder–elbow / elbow–wrist | Same arm, joints visible and approximately in image plane |
| Total arm-to-torso | Shoulder–elbow + elbow–wrist / neck base–pelvis | Bent and extended arms can share a chain length |
| Upper/lower leg | Hip–knee / knee–ankle | Same leg, compatible projection and articulation |
| Hand-to-head | Palm width / skull width excluding ears/whiskers | Open palm and matched head yaw; closed fists are separate views |
| Tail-to-torso | Tail centerline arc / torso length | Entire tail visible; record out-of-plane/hidden sections |
| Tail thickness | Tail diameter at registered segment / torso length | Same tail segment, no tapered-tip substitution |
| Ear-to-skull | Ear major diameter / skull width | Near/far ears separate; matched head yaw/pitch |
| Eye-to-skull | Eyeball aperture width / skull width | Near/far eyes separate, open neutral eyes |
| Eye spacing | Eye-center distance / skull width | Matched head yaw; no front-to-three-quarter comparison |
| Muzzle-to-skull | Muzzle width / skull width | Matched angle and expression |

Milo's teeth remain invisible, with the approved felt anatomy, palette and materials. A ratio pass does not override these identity rules.

## Horizontal bulk and cream-patch coverage

Height alone cannot establish a consistent build. The canonical report now measures Milo's **upper, middle and lower visible torso panels**, lower-body pelvis band, near-thigh band and near-arm band, plus the **cream patch** at the same three torso levels and its height. These measure different properties: a broad cream patch may make Milo look rounder even when the body panel is unchanged. Track both independently. The mid-belly panel is approximately 220 pixels, the cream patch there 135 pixels, and the canonical head width 417 pixels: panel/head ≈0.53 and patch/panel ≈0.61 in this particular view. Native endpoints, uncertainty and definitions are the authority, not rounded numbers alone.

Torso width stations are registered near 0.23, 0.51 and 0.80 along the visible neck-base→pelvis surface axis. Locate homologous stations in a candidate; do not use the same PNG row or whole-image percentage. Match body yaw, lean and articulation before comparing. Head-normalized spans additionally need compatible head yaw/pitch; use torso-local ratios when the head view differs. A bent arm cannot count as a wider torso. Hand/prop occlusion cannot prove the patch boundary. Crossed, crouched or foreshortened thighs are not directly comparable to the neutral standing thigh section. Portraits cannot provide belly or hip measurements.

Milo's hanging arms hide parts of the full torso contour. The measured panel starts at visible arm/body seams, not an invented hidden back outline. The pelvis-band span includes stance-dependent upper-leg outlines and is **not skeletal hip width**. Likewise, a visible thigh section is not its true 3D diameter. Full chest width, full belly circumference and hidden hip breadth remain unavailable. Exclude tail, arms, isolated wool fibres and changing limb bounding boxes from torso measurements. Never widen/narrow one body part through independent pixel scaling to force a pass.

Leo uses his own visible hindquarter panel, near hind-thigh section, foreleg shaft and exposed cream chest span, together with his existing paw/face/mane measures. His cream patch is partially hidden by mane and forelegs; do not call the exposed span the full patch or chest. These are local-byte observations pending his canonical hash reconciliation, not adopted lion design targets.

New width ratios remain canonical **reference baselines with annotation intervals**, with numerical design tolerances awaiting review. Annotation uncertainty is not an allowed art-drift band, and no universal ±0.01 width tolerance is implied by the separate head-fraction decision. A failed or non-comparable width review blocks an anatomy pass even if the head-height fraction is acceptable. An updated profile hash invalidates older profile-bound anatomy passes.

The preferred gallery includes combined numbered/W-labeled diagrams covering all old and new measurements, native-pixel quantity definitions and ratio intervals. Keep these beside the pose cards and local audio; originals and historical reviews remain intact.

For a future `matched_reviewed_reference` anatomy decision, `anatomy_review.horizontal_review` must name `scope` (`body` or `portrait`), a path/hash `evidence` record and `checks`. Body checks are `body_bulk`, `cream_patch`, `limb_bulk`; portrait checks are `head_width`, `ear_width`, `eye_spacing`. Each needs `matched_in_compatible_view`. Missing or `not_comparable` checks cannot certify an anatomy pass; retain planning validity while gathering suitable evidence. The outer anatomy review still binds exact candidate, reference and current profile hashes. This is separate from owner art/scene approval.

## Leo: lion-specific profile

Leo's profile is bound to his own canonical hash. Visible-face/mane/ear/eye/paw observations are now measured from the actual local bytes and labeled non-authoritative pending hash reconciliation. Adoption as canonical targets stays blocked; observations do not silently change the identity ledger. The mane obscures skull/neck/shoulder landmarks, so a visible silhouette or approved additional view may be needed; do not invent the skull boundary under the mane.

| Ratio | Landmarks / purpose | Applicability |
|---|---|---|
| Head-to-trunk | Visible skull length / shoulder–hip trunk axis | Matched lateral/three-quarter view; skull must be identifiable |
| Mane-to-head | Mane outer diameter / visible skull dimension | View-specific; mane volume is separate from skull size |
| Muzzle-to-skull | Muzzle length or width / corresponding skull dimension | Matched head angle; length and width are separate metrics |
| Eye-to-head | Visible eye aperture / visible skull width | Near/far eye and neutral eyelid state separate |
| Ear-to-head | Visible ear major diameter / skull width | Ear visible outside mane; no inferred hidden extent |
| Trunk-to-shoulder-height | Shoulder–hip axis / shoulder–support plane | Comparable standing quadruped; invalid while lying asleep |
| Forelimb segments | Shoulder–elbow / elbow–wrist | Approximately in-plane, visible joints |
| Hindlimb segments | Hip–knee / knee–hock | Separate anatomy from forelimbs; visible joints |
| Paw-to-forelimb | Paw width / forelimb chain length | Compatible load/contact; do not compare a foreshortened lifted paw |
| Tail-to-trunk | Visible tail arc / trunk length | Entire tail visible; account for curl/occlusion |

Sleeping Leo is a pose variant with persistent anatomy, not a new proportion baseline. Preserve rounded golden-cream paws and no sharp claws/grey nails. The inherited same-depth Leo/Milo standing-equivalent 0.25 relationship is **inter-character staging**, not either character's internal ratio profile, and does not apply mechanically to portraits.

## Bent limbs and perspective

For an in-plane arm, measure `shoulder→elbow + elbow→wrist`; do not use the shoulder→wrist chord. Example: two 40-pixel segments at a right angle have an 80-pixel chain, although their endpoint chord is about 57 pixels. The same logic applies to articulated legs. A bent hand may hide an elbow; mark it occluded rather than estimating its location to obtain a pass.

These remain **2D projected lengths**. An arm reaching toward the lens may appear short despite correct anatomy. Record `foreshortened` / `not_comparable`, use a compatible reference or a separately approved view, and do not stretch it to hit an in-plane target. Tail length follows the visible centerline arc, not tip-to-root chord. Curled/occluded tails cannot establish complete anatomical length.

## Portraits inherit facial anatomy

Portraits use the same character's angle-compatible ear/skull, eye/skull, eye spacing and muzzle/skull ratios as full-body images. More pixels or a tighter crop does not authorize a larger skull, different ear roots, new muzzle or changed eye placement. Preserve full ears, shoulders and upper chest in the established portrait framing.

Head-to-whole-body fraction is **not applicable** when the body is cropped out. Tilted ears/heads and near/far perspective need matching views; facial expression changes eyelid aperture, so compare eye construction with expression-specific references rather than requiring every blink to match neutral aperture. Closed still mouths and later dialogue lip-sync remain separate.

## Paws, feet and closed hands

Milo's canonical supplies separate near/far **closed-hand spans/heights** and supporting **foot spans/heights**. His near foot is more front-facing, while the far foot's horizontal span includes its side-view heel-to-toe extent: do not force those two projected widths to agree. Reference foot aspect, foot/head, foot/pelvis and closed-hand/arm ratios only under matching orientation and support. A closed-hand outline is not open palm capacity or an anatomical finger-length measurement; the open-palm/grip metric remains unavailable.

Leo's own profile adds near forepaw, near hindpaw and far forepaw visible heights/aspects, far forepaw span, exposed far hindpaw span, fore/hind paw comparison, visible foreleg height and shaft thickness, and a visible tail-shaft thickness reference. Forepaws and hindpaws are different structures. The far hindpaw is partly hidden by the near foreleg, so its measured exposed span must never become a full-paw breadth. Preserve the canonical's rounded felt toe construction and warm cream paws, without sharp claws. Leo's observations still do not resolve the canonical hash mismatch.

The single combined annotated canonical diagram for each actor contains every original landmark, all horizontal W spans and the newer hand/paw measurements. The separate numbered-landmark and width-only diagrams remain derived history, not competing active views. The gallery retains all ratio/coordinate tables and uncertainty.

## Acorn and contact ratios

After selecting one exact acorn design, calibrate acorn width / usable palm span and acorn height / hand length at the same local depth. Bind design/hash and reviewed dimensions independently of Milo's anatomy. Test held/picked/lowered/released phases with real contact and hand occlusion. Do not automatically shrink the acorn, enlarge hands or alter Milo's ratios to fit empty grip spaces. Until actual prop-fit evidence exists, report pending.

## Keep the preferred HTML review format

Run `production/performance_review_gallery.py --story lion_and_mouse_v7`. It derives a read-only gallery from the current library and audio-visual assignments, using the responsive card layout the owner liked: checkerboard transparency, native image links, semantic pose and exact audio-linked image IDs, per-line local WAV controls, approval/readiness notes and comparisons. Keep historical batch galleries and receipts intact.

The reusable gallery supports filtering body/portrait/expressions and scene uses, and shows each actor's own ratio profile. Fit-to-card display is not anatomical normalization. Comparison panels must state their uniform normalization method, reference hashes and uncertainty; do not present distorted overlays or automatic verdicts as owner decisions.

## Current canonical measurement data

The authored manual coordinates are in `stories/lion_and_mouse_v7/canonical_proportion_landmarks.json`. Rebuild their quantities, ratio intervals, numbered annotation images, combined horizontal/vertical/paw diagrams and tables with `python production/canonical_measurements.py --story lion_and_mouse_v7`. The report supplies 36 visible Milo ratios and 29 Leo visible-surface ratios. True joint/skull metrics that cannot be located remain explicitly unavailable; surface-path and visible-face metrics have distinct names. Source actual SHA-256 values are checked before rebuilding, and do not modify canonical identity/approval hashes. No annotation baseline is automatically an owner-approved tolerance.

## CPU tooling

```bash
python production/character_proportions.py --story lion_and_mouse_v7 validate
python production/character_proportions.py --story lion_and_mouse_v7 derive
python production/performance_review_gallery.py --story lion_and_mouse_v7
```

The ratio helper calculates distances and conservative screening intervals from supplied annotations. It does not automatically segment character anatomy, recover 3D lengths or generate/repair assets. Planning accepts pending calibration. Image readiness remains blocked by missing anatomy, prop or staging evidence. Use the repository-local [character-proportion-review skill](../.claude/skills/character-proportion-review/SKILL.md); the two existing image/audio skills route here for this work.

The gallery renders only the current registry file for each variant; superseded candidates are preserved in `pose_library/HISTORY_INDEX.json` and omitted from current cards. An earlier comparison sheet is hidden automatically when its source path/hash differs from a replacement. New revision bytes start pending owner review; old art approvals do not transfer.
