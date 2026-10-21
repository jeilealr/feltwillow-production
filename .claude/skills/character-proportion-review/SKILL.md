---
name: character-proportion-review
description: Plan and review reusable Feltwillow character anatomy with dimensionless ratios, articulated joint measurements, compatible portrait views and the local pose-review gallery. Use for character generation preflight or proportion consistency review; does not generate assets or grant approvals.
---

# Character proportion review

Read [the framework](../../../docs/character-proportion-framework.md) when defining anatomy targets, preparing character image requests or judging possible proportion drift. Resolve the current story's performance registry and exact reference hashes. Never replace canon with an arbitrary ratio or apply Milo's numbers to Leo.

Create each character's own profile after its first canonical is selected, with metrics chosen for that animal. Bind ID/revision/path/hash; derive only visible, comparable measurements. Canonical replacements require recalibration. Milo and Leo have separate mouse/lion profiles; Leo's unresolved canonical byte mismatch blocks his numerical calibration. An approved performance reference may clarify projection, but does not replace the canonical baseline. Null targets can coexist with measured reference baselines: report projected observations and uncertainty separately from adopted targets. Never rename a visible-face or surface-axis proxy as a hidden skull or joint length. Leo local-byte measurements remain non-authoritative until hash reconciliation.

- Separate identity, pose/acting acceptance, anatomy evidence and scene/prop readiness.
- Use the actor's authored ratio profile; null targets need calibration, not guesses. Milo's upright comparable-view head fraction is 0.39 ±0.01. Uncertain landmarks cannot pass this narrow band merely because the rounded estimate is 0.39.
- Compare compatible view/head pitch/depth before screening projected ratios. Sum shoulder–elbow–wrist and hip–knee–ankle segments for in-plane bent limbs; hidden joints or out-of-plane foreshortening stay not comparable. Never use shoulder–wrist chord as arm length.
- Portraits inherit compatible skull/ear/eye/muzzle ratios; do not apply a full-body head fraction to a bust crop or paste faces across head angles.
- Review horizontal bulk as well as vertical height: use each canonical's own visible torso-panel, lower-body/hip-band, near-thigh and arm widths plus cream/material-patch width and height. Body outline and colour-patch outline are separate. Register torso levels relative to neck-base/pelvis surface axis; never reuse a canonical pixel row in a different pose. Exclude arms, tail, mane, props and loose fibres from torso width. If they hide the contour, measure only a labeled visible panel or mark the full span unavailable. Same yaw, lean, support and limb roll are required; 2D spans are not circumference or hidden bone breadth. See the width diagrams and uncertainty in the current canonical report. Do not assign an invented universal ±0.01 tolerance to these new observations.
- Feed ordered canonical/proportion/pose references and the applicable targets into the concrete generation proposal. Guidance is not a geometric guarantee. Preserve the existing paid-request approval rule.
- Keep original PNGs and creation receipts unchanged. Bind annotations/review to exact hashes; uniform whole-actor scaling only. Actual props require grip/occlusion/size review.
- Present results using `production/performance_review_gallery.py`: checkerboard pose cards, exact pose/revision and audio-linked image IDs, native-image links, available line audio, comparison notes, ratio uncertainty and separate approval states. Do not replace the favored gallery with a text-only report or imply that view-fit images have equal anatomical scale.
- Keep one combined annotated canonical image per character in the active gallery: all older numbered landmarks plus horizontal W spans, cream patch and paw/hand measurements. Retain complete ratio/coordinate tables and native-size links. Near/far and frontal/side paw projections remain separate; closed hands cannot calibrate open-palm grip, and an exposed partial paw is never its full width.

CPU commands (existing feltwillow conda Python):

```bash
python production/character_proportions.py --story lion_and_mouse_v7 validate
python production/character_proportions.py --story lion_and_mouse_v7 derive
python production/performance_review_gallery.py --story lion_and_mouse_v7
```
