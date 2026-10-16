# Perceptual-world image fixes — first review set

Four concrete replacement/anchor candidates were generated on
`feature/perceptual-world`. Open [the before/after review page](owner_review.html).

| Candidate | Change | Status |
|---|---|---|
| s04_p01 r08 | 4× registered local crop; clear running pose; moved planted foot off foreground foliage onto dirt and recalculated depth | Proposed Milo-action anchor |
| s06_p01 r10 | 2.25× shared crop; resting Leo and readable scrambling Milo | Proposed shared-action anchor |
| s07_p03 r09 | True upper-body speaker view; both full ears, no tail; strongly blurred registered ground/root crop | Proposed Milo-speaker anchor |
| s16_p05 r07 | 2.1× shared closing crop; Milo nearer the paw interaction on the same ground | Proposed shared-closing anchor |

These are actual new PNGs, not adopted production replacements. No owner
approval has been inferred. The unchanged active 96-image set, acceptance
ledger and video-control implementation remain intact.

The first full-scene trials improved detail but did not reliably obey the
camera/scale locks. They are explicitly labeled non-authoritative trials.
Final candidates instead use built-in ImageGen RGBA pose layers from canonical
references, actual native-image inspection, and the existing
`production.keyframe.compose` API on deterministically materialized crops.
Each layer's exact prompt and canonical input hash are in
[candidate_manifest.json](candidate_manifest.json). Each final composite has its
own source/pose receipt and edit mask. No trial is reused as a visual authority.

The final images are 1920×1080. Pixel comparison confirms zero mismatches
outside the combined actor/contact masks against the normalized registered
background (including the specified portrait blur). Measured visible pose boxes
are recorded in [composition_verification.json](composition_verification.json).
They are not independent proof of standing-equivalent anatomy: lying/running
poses still need neutral-anatomy calibration. Owner review should also assess
contact integration, eye lines, expressions and adjacent-frame continuity.

## Approval boundary and next work

The repository [consistent-image-prompts skill](../../../../.claude/skills/consistent-image-prompts/SKILL.md)
requires: “Generate the setup's anchor first; dependent frames wait for its approval.”
The new crops cannot borrow old wides' missing/different anchors. Review these
four concrete candidates before propagating their framing to s04_p02–04,
s09_p01, s06x_p01, s07_p02 and the other shared closing views. A choice of
composition is not blanket technical or runtime approval.

After the owner selects a candidate, register only its exact approved scope and
hash, reconcile staged camera/depth/pose sizes, then use the existing revision
workflow and rebuild all active scene sheets if a production image changes.
Do not clear old approvals or technical checks just to enable adoption.

## Reproduction and temporary files

Owner preference, 2026-10-16: temporary runs use
`/scratch/project_465002727/jelealro/tmp`, not `/tmp`.
This run's optional image environment is in
`/scratch/project_465002727/jelealro/tmp/perceptual-world/image-env`.
Run from the repository root:

```bash
export TMPDIR=/scratch/project_465002727/jelealro/tmp
/scratch/project_465002727/jelealro/tmp/perceptual-world/image-env/bin/python \
  stories/lion_and_mouse_v6/review/perceptual_world_fixes/build_candidates.py
```

The reproduction script uses existing compositor/crop code; it does not modify
production implementations, active plans or approvals. It requires Pillow,
numpy and opencv-python-headless. Generated-image tool caches remain in the
normal Codex image cache; all project deliverables are saved inside this repo.
