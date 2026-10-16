# Perceptual-world image fixes — complete review set

Open [the before/after review page](owner_review.html). It contains all **36
requested decisions: 14 priority replacements, nine additional replacements,
and 13 retained originals**. Filter to “19 new candidates” to see the images
added after the four compositions you already liked. Click any 480×270 preview
for its native 1920×1080 PNG.

The actual replacement PNGs are saved in
`character/characters/lion_and_mouse_v6/interactions/keyframes/.review/perceptual_world_fixes/`.
[The complete replacement record](complete_replacement_plan.json) lists each
path/hash, source selection, crop, actor placement and composition receipt.
The first four selections retain the owner's exact approval scope and bytes.
The 19 new candidate slots await review. Active keyframe plans, acceptance
ledger, current 96 PNGs and video-control implementation have not been changed.

## What changed

| Coverage | Result |
|---|---|
| s04_p01–04 | Local rightward action views; p02 retains the overhead branch, p03/p04 retain the stump and clear dirt lane |
| s06_p01, s06x_p01 | Compact shared scramble; Leo progresses from resting toward four-paw support |
| s07_p02–04 | Apology, explanation and reassuring promise as stable upper-body Milo portraits |
| s06_p03, s08_p01 | Milo's fearful response gets readable facial coverage; neighboring shared/Leo views retain context |
| s09_p01, s12_p03 | Clearer careful steps and running silhouette on registered local path crops |
| s13_p06 | Playful answering portrait, looking toward offscreen Leo |
| s14_p01 | Exact reuse of selected s14_p02 knot insert; preserves existing rope topology and mouth/paw contact |
| s15_p03–04 | Readable reassuring Milo portraits |
| s15_p06 | Compact released-Leo/Milo view with the collapsed net extracted from the existing selected frame |
| s16_p01/p04/p05, s16x_p01/p03 | Shared closing composition; explicit narration holds and restrained happy expression variation |

All 22 uncertain frames were inspected at native resolution and at 480×270.
[The decision record](closer_review_22.json) explains each of the nine fixes and
13 retentions. Retained frames: s05_p04, s06_p02, s07_p01, s08_p04, s08_p06,
s12_p04, s13_p01, s13_p03, s14_p03, s14_p06, s15_p01, s15_p02, s16x_p02.
These either prioritize Leo, establish geography, show a broad action, or have
adjacent portraits supplying subtle emotion. s12_p04 preserves the owner's
explicit distant-wide instruction.

s04_p02 deliberately uses a wider contextual crop than p01/p03: a tighter crop
would remove the overhead branch required by the action. It asks the running
silhouette to carry passage, with adjacent local views carrying facial detail.
No actor is independently enlarged to compensate for a large environment.

## Generation and checks

Built-in ImageGen produced transparent pose/expression layers from the canonical
references and selected anchor layers. Exact prompts and reference hashes are in
[candidate_manifest.json](candidate_manifest.json), [followup_layers.json](followup_layers.json)
and the individual `*_layer_prompt.txt` files. The existing compositor assembles
these on exact registered plate crops; no production implementation was edited.
The final portraits retain the selected body/ears/shoulder silhouette, with
expression inserts constrained to the face opening. [Expression receipts](expression_continuity.json)
record the alignment, face masks and unchanged outside-face pixels/alpha.

[Batch verification](batch_verification.json) checks complete 14+22 coverage,
all candidate dimensions/hashes, all source bindings, exact knot-image reuse,
zero changed background pixels outside 22 composition masks, six expression
locks and all 96 unchanged active image hashes. Native and small-preview visual
review checks framing, expression, gaze, support and local landmarks. These
checks do not substitute for standing-equivalent anatomical calibration or
owner selection. Pose bounding boxes alone cannot prove the Milo/Leo ratio.

The original scene trial images remain non-authoritative history. Do not reuse
them as identity/scale references. The current native production pipeline still
has unresolved setup/plate/prop authority and structured visual evidence gates.
Use the normal revision/adoption workflow to register exact selected crops,
reconcile camera/depth/anatomy, update active paths and rebuild scene sheets;
do not clear checks or invent approvals to enable adoption.

The [consistent-image-prompts skill](../../../../.claude/skills/consistent-image-prompts/SKILL.md)
requires: “Generate the setup's anchor first; dependent frames wait for its approval.”
The owner's selection of the initial four compositions authorized this follow-up
family. Newly proposed compositions retain pending review status and do not
silently become reusable technical authorities.

## Reproduction

Use `/scratch/project_465002727/jelealro/tmp` for temporary runs as requested.
The optional local environment is `tmp/perceptual-world/image-env`; it needs
Pillow, numpy and opencv-python-headless. Run from the repository root:

```bash
export TMPDIR=/scratch/project_465002727/jelealro/tmp
IMAGE_PY=/scratch/project_465002727/jelealro/tmp/perceptual-world/image-env/bin/python
"$IMAGE_PY" stories/lion_and_mouse_v6/review/perceptual_world_fixes/build_followup_candidates.py
"$IMAGE_PY" stories/lion_and_mouse_v6/review/perceptual_world_fixes/build_owner_review.py
"$IMAGE_PY" stories/lion_and_mouse_v6/review/perceptual_world_fixes/verify_batch.py
```

The first four approved candidate bytes are preserved. Their original
`build_candidates.py` is historical reproduction code for that first set;
rerunning it also resets its manifest's review status. Do not use it to reset
recorded owner selections.
