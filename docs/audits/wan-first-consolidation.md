# Wan-first consolidation — 19 October 2026

Candidate integration: all captured remote histories and additional local source capture have been merged without conflicts. Engineering validation and publication are pending at this checkpoint. Integration does not approve production images or videos. The complete implementation strategy was supplied in the owner's task message; the named companion file was not separately present locally.

## Inputs and preservation

The refreshed remote refs match the reviewed snapshot: target `6fae81c78ef3143057bc0324103f2cb05c5dce0a`; perceptual `97f0d42d2cf4be300f502054473776c6ae6c5159`; video `44b547a6e4e5b08cd32bc6c7d888222785deb923`; blender `fcea46b788f6df8423f84bf14e54169f15a383e3`. Local target has no unpushed commits; local perceptual/blender refs both started at `fcea46b`. No concurrent agents remain.

Primary checkout had 386 staged paths and ignored work. Its index/worktree were not reset, unstaged, switched or committed in place. Backup refs and an independent APFS clone of the Git directory were made before edits; `git fsck --connectivity-only` passed. Staged/unstaged binary patches and raw status/worktree/ref/ignored inventories remain outside Git. A name/content scan found only a synthetic example.org token test fixture, not an actual credential. No credentials, weights, environments or OS metadata were published.

The owner agreed to `/Users/lealroja/Documents/feltwillow/preservation/wan-first-20261019-082831/`. Saved on-disk capture: 2,483 files/links, 2,899,731,234 bytes, source/archive hashes verified; 63 cache/OS/environment/credential-name exclusions. 333 source paths were captured on `capture/wan-first-20261019-082831` at `d9e7e319033109a267e1c894d496c8a1a6eb322e`, parented to the actual local source `fcea46b`. Large binary candidates, packed textures, GLBs, review media and downloaded originals remain in the agreed archive, not Git. Several Blender files exceed GitHub's normal file size limit. This is a local Mac archive, not an off-machine backup; unsaved application memory was not inspected. Original assets remain in place. Exact paths/hashes/storage and recovery instructions are in `wan-first-local-assets.json`.

## Merge and reconciliation

In an unused clean sibling worktree, inspected `git merge --no-ff --no-commit` stages and recorded normal commits:

1. Perceptual merge `4d1f76c`; current 96 selected paths/hashes and protected authority records checked exact.
2. Captured remote blender head verified as ancestor; no duplicate merge.
3. Video merge `775546a`; experiment code, receipts and existing `docs/lumi.md` changes retained.
4. Local capture merge `5fe4ffa`; one Blender writer/source history retained, no scene edits.

No conflict resolution, squash, cherry-pick-only workflow, `ours` merge or source branch deletion was used. Complete NUL-delimited local diffs, including removals/renames, feed `wan-first-merge-disposition.json`; the 300-entry web cap was not used. Every source path change and meaningful local file has a disposition. Preserved deletions remain deleted; historical fixtures were not restored to active authority.

Separate policy changes add [production direction](../production-direction.md), readiness backlog and routing from entry points; retain research in place; narrow Blender routing; add per-skill Codex symlinks to the existing image/audio sources. Original Blender skill VERSION 1.3.0 and file hashes are captured before its routing-only patch. Source modules remain available; no older skill was installed. Normal Wan modules gain no Blender/control imports. Lightweight CI now also discovers the eight synthetic control-auditor tests and compiles experiment Python without executing GPU/model jobs.

Structural repairs address existing stale links, obsolete `.review` net path in a test, and a test that required the Swift builder despite the portable Python builder. Historical/local unavailable links are code paths with preservation notes, not restored rejected assets or invented outputs. Exact source versions remain in merge ancestry and the archive; historical JSON receipts are unchanged. The original packaged CC0 license bytes are retained, including their original line endings.

## Image/audio protection and validation

`wan-first-image-inventory.json` verifies 96 unique 1920×1080 PNGs against plan, ledger and sheet manifest, current boundary pointers, 16 sheets and unchanged authority records. r03 Milo and `s04_p02_r14_candidate.png` survive. No consolidation-generated images, anatomy changes, approval changes or receipt hash substitution occurred. Individual/delegated/retained selection remains separate from technical evidence. Audio verification found zero blockers for the authorized 161 lines/16 tracks, including original source WAVs under the original work root. No v5 visuals were adopted.

Executed baseline commands/logs are retained under `wan-first-validation-logs/`. Full target suite: 92 tests, one pre-existing broken-link failure, two skipped. The staged perceptual baseline: 100 tests, three failures (links, obsolete net path, Swift-only documentation expectation), two skipped. Text/code-only source snapshots also ran; their missing binary/lumi fixtures caused additional expected failures, so they are explicitly not complete source-baseline passes. Eight separate experimental input-auditor tests passed. Final engineering results are to be recorded after candidate validation.

Read-only gates at `5fe4ffa`: staging/pose pass, perceptual passes with 50 advisory warnings; reference has 127 current authority blockers and 80 historical provenance warnings; visual has 1,736 blockers; runtime has 1,863 blockers and writes no files. Keyframe-review fails on existing evidence/stale planning. These are preserved evidence/reconciliation blocks, not counts of bad images or automatic regeneration orders. No derived contract, adoption builder or mutating verifier was run.

## Remaining production work

No new chronological full-resolution image review was performed. r03 performance-family refresh/revalidation, evidence/anchors/props, selected/planned geometry, actual endpoint compatibility, reviewed timing/native v6 renderer translation and moving-face dialogue remain open. Fixed-patch lip-sync is a known failure, not repaired. Historical missing media is unavailable here; receipts stay immutable. See [the bounded image-first backlog](../../stories/lion_and_mouse_v6/IMAGE_TO_VIDEO_READINESS.md). Start with one upcoming scene's identity/contact/endpoint review, recording hashes and separating defects from evidence gaps.

No paid calls, image generation, new Blender renders/scene edits, model downloads, GPU jobs, MCP/account changes or production publication were performed. Source branches, `main` and unrelated stories remain intact. Final destination SHA must be reported externally after publication; this report cannot contain its own future commit hash.
