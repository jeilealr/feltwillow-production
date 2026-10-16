# Perceptual-world image fixes and continuity tweaks

Open [the before/after review page](owner_review.html) and filter **Latest tweaks**
for the six revised slots from the owner's final reference-pose feedback. The separate
[scene-order page](scene_continuity.html) shows corrected frames together with
retained neighbors so size jumps and dialogue eyelines can be assessed directly.
Every preview is 480×270; click for the native 1920×1080 PNG.

The current proposal contains **41 replacement slots**: all 14 priority frames,
20 fixes from the 22 closer reviews, and seven additional Scene15 continuity
views. Two closer-review originals remain. The four previously selected
compositions retain their exact approved bytes; 37 other candidates await
selection and technical validation. Active production plans, acceptance ledger,
96 selected production PNGs and video-control code remain unchanged.

## Final six corrections

The owner identified six remaining weak views. Native and 480×270 review
supports correcting their readability, with action-specific framing:

| Frame | Final change |
|---|---|
| s04_p02 | Use the selected Milo atlas **row 3, column 3, Crouch**, preserving its natural proportions with uniform scale |
| s08_p06 | Keep s07_p01's standing Leo/shared camera; use atlas **row 2, column 3, Walk Right** for Milo's departure |
| s13_p01, s13_p03 | Compact approach/arrival hold from a uniform crop of the selected s13_p03 composite |
| s14_p03 | Uniform camera crop of the selected gnawing image; preserve original mouth/knot contact and mesh pixels |
| s14_p06 | Compact released-Leo view, retaining his cautious exit pose, trailing net and Milo-left/Leo-right relationship |

A crouch should be lower than a standing pose. Matching body heights would
change its proportions. The previous upper-44% silhouette proxy also included
the running tail, so it overstated head size. Current checks use an upper-35%
head/ear band, with an explicit head window for the crouch to exclude its raised
tail. Native pose inspection and viewing-size review remain necessary; these
measurements are not anatomical calibration.

[Final assessment and recipes](final_reference_corrections.json) record all six
changes. [Reference-pose provenance](final_pose_layers.json) includes the exact
atlas cell selections, prompts and source/output hashes. The net-action crops
preserve the selected composite: actors, ground and rope magnify together.
They are shared medium views; the rear net/tail can extend beyond the right
frame edge while both faces and the active closure loop stay visible.

## Latest owner-directed changes

| Sequence | Correction |
|---|---|
| s04_p02–04 | Tighter p02 crop and larger crouching Milo; all four action views match the selected p01 head scale, with the ground magnified together |
| s06_p02, s07_p01, s08_p04 | Replace retained old wides with the corrected shared camera and matched Milo size; preserve supported four-paw Leo and no pinning |
| s08_p06 | Running departure keeps Milo's shared-view head size instead of reverting to a tiny figure |
| All s15_p01–06 and s15x_p01–06 | Milo left / Leo right; Milo portraits look right, Leo portraits look down-left; forest plates are not mirrored |
| s16_p04 | Restore the earlier open-eyed, closed-mouth expressions at the corrected shared framing |
| s16x_p02 | Same composition and character sizes as x01/x03, with exact shared-hold pixels |
| s12_p04 | Preserve the owner's explicit tiny-Milo distant-wide exception |

The selected knot topology and causal mouth/paw contact remain protected in
the Scene13/14 camera crops. Scene15's released Leo/net layer is oriented consistently
with Milo on the left; the collapsed net stays on the ground. The native image
review also checked complete bodies/tails, grounding and head/ear margins.

The two retained closer-review frames are s05_p04 and the explicit s12_p04
exception. [All 22 decisions](closer_review_22.json) preserve their source hashes
and current reasons. The preceding 37-slot proposal is the immutable
[final correction input](final_reference_input_plan.json); earlier snapshots
remain reproduction history, not the current review inventory.

## Sources, generation and verification

[The complete replacement plan](complete_replacement_plan.json) binds current
paths, source hashes, crops and composition receipts. [Continuity tweaks](continuity_tweaks.json)
records the previous 21-slot update; the final six override it where named. [Continuity layer provenance](continuity_layers.json)
contains the exact built-in ImageGen extraction prompts and input/output hashes,
including the targeted downward-gaze refinement. Earlier layer provenance is
in [candidate_manifest.json](candidate_manifest.json) and [followup_layers.json](followup_layers.json).

Transparent ImageGen layers are placed with the existing native compositor on
registered plate crops. Scene04 action, Scenes06–08 shared views, and Scene16
shared views each have a matched upper-head silhouette-band size. This proxy
accounts for changing pose height; it is checked alongside actual native and
whole-frame previews and does not substitute for neutral-anatomy calibration.
[Scene checks](scene_continuity_verification.json) verify less than 1% spread
within each of these three groups, all Scene15 screen sides and two-shot body
margins, exact closing x01–03 holds, and the untouched s12_p04 exception.

[Batch verification](batch_verification.json) checks the complete inventory,
all candidate dimensions/hashes, unchanged protected background pixels, source
bindings, exact knot-insert reuse, previous expression masks, review links and
all 96 unchanged production hashes. First-four owner selections and existing
technical gates remain separate. Use the normal adoption workflow to reconcile
camera/depth/anatomy, register exact selected assets and rebuild active scene
sheets before production; no approval or technical evidence is inferred.

The [consistent-image-prompts skill](../../../../.claude/skills/consistent-image-prompts/SKILL.md)
states: “Generate the setup's anchor first; dependent frames wait for its approval.”
The owner's selected four compositions supplied the initial framing families;
the latest explicit request authorizes these continuity revisions. Newly
proposed images do not silently become approved technical authorities.

## Reproduction

Temporary scripts, logs and environment files use the requested scratch location.
Run from the repository root with Pillow, numpy and opencv-python-headless:

```bash
export TMPDIR=/scratch/project_465002727/jelealro/tmp
IMAGE_PY=/scratch/project_465002727/jelealro/tmp/perceptual-world/image-env/bin/python
"$IMAGE_PY" stories/lion_and_mouse_v6/review/perceptual_world_fixes/apply_final_reference_fixes.py
"$IMAGE_PY" stories/lion_and_mouse_v6/review/perceptual_world_fixes/check_scene_continuity.py
"$IMAGE_PY" stories/lion_and_mouse_v6/review/perceptual_world_fixes/build_owner_review.py
"$IMAGE_PY" stories/lion_and_mouse_v6/review/perceptual_world_fixes/verify_batch.py
```

The input snapshot makes revisions reproducible; matching existing composites
are reused after recipe/source checks. The older `build_candidates.py`, `build_followup_candidates.py` and
`apply_continuity_tweaks.py` reproduce historical stages and would reset
current proposal metadata. They are not the current entry points.
