---
name: character-proportion-review
description: Plan and review reusable Feltwillow character anatomy with dimensionless ratios, articulated joint measurements, compatible portrait views and the local pose-review gallery. Use for character generation preflight or proportion consistency review; does not generate assets or grant approvals.
---

# Character proportion review

## Current visual grammar (r004, 24 October 2026)

Classify before proposing any new image: temporal `individual|connected`, composition `portrait|body_or_interaction|environment_only|detail`, and mouth policy are separate axes. Read the actual audio/speaker, causal event, selected hashes and neighboring camera relation. Author classification once in `audio_visual_plan.json.visual_units`; derive displays. Follow [sequence production](../../../docs/sequence-production.md). Independent shots normally need one selected image, not a fictional pair end. Connected groups may span lines; retain every meaningful intermediate as actual adjacent endpoint input. Shared aliases emit no extra motion job; cuts never interpolate incompatible views.

Protect portrait head/ears/mane/neck/upper chest and crop: no newly entering hands, paws, legs or zoom. Different compatible closed expressions are allowed. Character speech uses the V7 tracked-mouth adapter with exact WAV/word mapping and same-view, actor-specific toothless calibration; NARRATOR and silence never drive lips. A physical tiny bite is a separate contact event, never narrator lip-sync. Put small toothless felt-mouth design in positive prompts; CFG-1 Lightning has no active negative conditioning. Inspect every output frame for teeth, limbs/cast and contacts; automated warnings cannot certify anatomy. Account for every required paw, its attachment/occlusion and support without inventing a fifth paw.

Preserve selected bytes and receipts. New revisions require exact-hash selection; historical selection can coexist with a current technical block. Ask only a grouped material art/intent or bounded resource question after completing independent work. No provider/GPU request, model download, automatic retry or Git action follows from this skill. Story-specific decisions and pending evidence live in [the current r004 review](../../../stories/lion_and_mouse_v7/review/owner_sequence_feedback_r004/README.md); do not generalize its scene map to future stories.


Read [the framework](../../../docs/character-proportion-framework.md) when defining anatomy targets, preparing character image requests or judging possible proportion drift. Resolve the current story's performance registry and exact reference hashes. Never replace canon with an arbitrary ratio or apply Milo's numbers to Leo.

Create each character's own profile after its first canonical is selected, with metrics chosen for that animal. Bind ID/revision/path/hash; derive only visible, comparable measurements. Canonical replacements require recalibration. Milo and Leo have separate mouse/lion profiles; Leo's identity bytes are reconciled by the current exact-hash owner record; retain species-specific, compatible-view measurement requirements. An approved performance reference may clarify projection, but does not replace the canonical baseline. Null targets can coexist with measured reference baselines: report projected observations and uncertainty separately from adopted targets. Never rename a visible-face or surface-axis proxy as a hidden skull or joint length. The owner identity reconciliation does not automatically adopt every measured ratio as a target or certify later scene anatomy.

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
