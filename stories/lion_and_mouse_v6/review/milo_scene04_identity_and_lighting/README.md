# Milo Scene 04 identity proposal and lighting repair

The owner preferred the natural Milo in `s04x_p01_r01_candidate.png` over the
current canonical-derived actor and identified a circular bright patch on the
face in `s04_p02_r13_candidate.png`.

Open [owner_review.html](owner_review.html) for matched comparisons and full-size
images. The owner-approved master (accepted 2026-10-18) is
`character/characters/lion_and_mouse_v6/Milo/canonical/full-body_milo_neutral_pose_r03_candidate.png`.
It was generated from the preferred scene alone, with a neutral stance and broad
neutral light for reusable identity evaluation. The previous r02 master was
compared afterward, not attached as a competing identity reference. The r03 master has real transparency. Its approval is hash-bound in the
visual bible and `../../image_sources/milo_r03_owner_adoption.json`; the previous
r02 master and its family remain historical. Dependent reference-family refresh
is pending; no keyframe identity rollout has been performed.

The lighting repair is active as `s04_p02_r14_candidate.png`. The prior r13 is
preserved under `interactions/sources/lighting_repairs/`. A fresh built-in
ImageGen edit supplied lighting guidance. Its geometry and scenery were excluded:
a smooth, bounded RGB illumination field is applied to original actor pixels,
including the face. All pixels outside the selected actor alpha remain exact.
This removes the previous frozen-face/body lighting mismatch while preserving
pose, expression detail, scale and placement. The current scene sheet, selection
ledger, plan and boundary data point to r14. Production technical approval is
still separate.

`proposal.json` records the identity candidate and exact attachment roles.
`inputs.json` binds source hashes, retaining the original generation path for the
relocated r13. `canonical_prompt.txt` and `lighting_prompt.txt` are the exact
instructions sent through built-in ImageGen. `lighting_receipt.json`, the raw
suggestion, edit mask and builder preserve the finishing recipe. The completed
lighting builder refuses to overwrite the adopted repair. The identity proposal
and lighting repair are independent: selecting the new identity would require a
separate decision about its dependent family and any further scene changes.

The second comparison in the owner's message repeats the same filename on both
sides. Clarification was requested; no unidentified second image was assumed.
Temporary work uses `/scratch/project_465002727/jelealro/tmp`.

The comparison image preserves its pre-selection captions as owner decision evidence. The master labeled “proposed r03” there is now approved. Completed comparison builders refuse to overwrite the approved selection record.
