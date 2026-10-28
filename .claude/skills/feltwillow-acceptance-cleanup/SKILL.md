---
name: feltwillow-acceptance-cleanup
description: Prune old Feltwillow candidate images, obsolete review outputs, legacy V6 artifacts and unused experimental character probes after acceptance. Use when the user wants a lean Git working tree or repeats scene-completion cleanup. Once the current checkout is fully committed and exact selection/reference/technical gates pass, delete eligible tracked files and create a local cleanup commit automatically without a second per-file approval. Always retain owner-selected images and their required provenance; never infer approval from revision numbers.
---

# Feltwillow committed acceptance cleanup

## Mandate

The owner has **pre-authorized automatic cleanup of mechanically verified obsolete files** after the accepted source-image and source-of-truth changes are committed. **Do not ask for a second approval of each removal manifest.** The original owner decisions for artistic assets still control which images are selected; this permission never permits new image selections or changing accepted pixels.

Use the actual local branch/working tree. GitHub may lag. **No Git hook runs automatically after every commit**: invoke this skill deliberately after a completed acceptance checkpoint, or have the local coding agent run it as part of that checkpoint. The runner automatically removes and *locally commits* the exact passing subset. It never pushes, rewrites history, deletes untracked files, or runs `git clean`/`rm -rf`.

Read the precise schema, protection rules and failure handling in `references/manifest-and-gates.md`. Use existing project authorities and code; this is not a replacement image pipeline.

## Execution sequence (no additional user permission step)

1. **Freeze current work first.** Inspect branch, HEAD, Git status and selected-use matrix. Commit verified outstanding changes normally, **then** create a fresh cleanup manifest pinned to that HEAD. Do not commit/overwrite unreviewed owner decisions merely to satisfy cleanup. Preserve unrelated untracked files such as `.DS_Store`. If tracked files remain dirty, stop cleanup until they are legitimately committed or restored. The cleanup script refuses dirty tracked/index state.
2. **Resolve authoritative keep set.** Read actual owner-selection/acceptance records, final scene-use resolver, canonical/pose/plate/prop sources, current S01–S08 source-still hashes, Wan start/end/intermediate inputs, active performance metadata and required receipts. Include exact paths+hashes in `keep` and add the current selection and resolver files to `authority_records`. A new filename revision is not proof of selection.
3. **Inventory and classify.** Use `scripts/cleanup_audit.py inventory` (read-only), scoped initially to S07–S08 revisions, then S01–S06. Explicit categories for the executable manifest: `superseded_revision`, `review_derivative`, `legacy_v6`, `chrono_probe`. Each candidate must be **Git-tracked, committed, byte-matched, and within an allowed root**. List exact paths; never use directory globs. Old versions can only be pruned when the selected replacement is independently hash-bound to an owner record. Review history can only be pruned when no retained evidence/reference needs it. V6 and `_chrono_probe` are *conditional*, not automatically obsolete by name.
4. **Prove retained dependencies.** Check current and dynamic references, imports, sidecar ancestry, plans, native/Wan inputs, docs/tests, and relative HTML links. The runner also performs a conservative retained-text search for paths, basenames, hashes and legacy-root references. Search results aren't a complete dynamic dependency proof; **don't include a file in the manifest if a dynamic dependency has not been resolved**. Keep uncertain files and continue with a smaller safe batch; no user review required for the safe subset.
5. **Build the exact manifest outside the repo** using `references/manifest-and-gates.md`; include real scoped test commands (selection/plan/resolver, relevant tests) and correct hashes. Limit each transaction to 250 files. Run `scripts/prune_committed.py --dry-run` and resolve any blockers by correcting legitimate *technical* references in a separate committed change; never waive tests or change owner artwork to get a green report.
6. **Apply automatically.** Once the manifest passes, run `scripts/prune_committed.py --apply`. This rechecks committed Git blob recoverability and current working bytes, runs scoped tests **before and after** the exact-file `git rm`, verifies the accepted KEEP and owner-authority hashes, and makes one **local cleanup commit**. If a post-removal check fails, the runner restores only its staged removals and reports failure. **Do not wait for a per-batch owner response.** Rebuild the next manifest against new HEAD before the next batch.
7. **Finish and report.** Report removed files/working-tree bytes, local cleanup commit, retained exact-hash selected use coverage, tests actually run, files blocked for technical reasons, and any residual artistic decisions. No pushes, history rewrites, aggressive Git GC, external spending, or image generation.

## Allowed automatic removal, and exceptions

- **Allowed after verification:** exact older unselected scene revisions; preview-only gallery/contact-sheet artifacts; old V6 files and `_chrono_probe` files with no remaining active dependencies. Their original committed bytes remain recoverable through Git history. `git rm` **does not reduce `.git` object/history storage**.
- **Never remove:** approved/selected scene PNGs and canonical identity; scene/line/beat/selection registries; owner selections and acceptance ledgers for current V7; any input required to reproduce or validate selected images; scripts/tests still used by any story; currently referenced Wan inputs and sidecars; shared skills and their symlinks. Do not edit owner decisions to declare a candidate obsolete.
- **Stop individual files, not the entire effort:** If the current repository has an unresolved reference, missing blob, Git LFS pointer, ambiguous acceptance, or failing test, retain the affected file and record its precise reason. Correct valid technical bindings and commit them before reconsidering the file. Artistic approval remains with the owner, but no **deletion** approval is required for independently safe paths.
- **If history may be discarded:** Git-only recoverability is not sufficient for a separate Git-history purge or disk-reclaim operation. That requires a distinct backed-up plan. Do not do it here.

## Commands

```bash
# Inside the real Feltwillow Git root; start with a completed committed checkpoint.
python3 .claude/skills/feltwillow-acceptance-cleanup/scripts/cleanup_audit.py inventory \
  --repo . --out ../feltwillow-cleanup-inventory.json --scenes S07 S08

# Agent creates ../feltwillow-cleanup-manifest.json using current owner/hash evidence.
python3 .claude/skills/feltwillow-acceptance-cleanup/scripts/prune_committed.py \
  --repo . --manifest ../feltwillow-cleanup-manifest.json --dry-run
python3 .claude/skills/feltwillow-acceptance-cleanup/scripts/prune_committed.py \
  --repo . --manifest ../feltwillow-cleanup-manifest.json --apply

# Optional external byte-identical archive, not a second approval requirement:
python3 .claude/skills/feltwillow-acceptance-cleanup/scripts/archive_verified.py \
  --repo . --manifest ../feltwillow-archive-manifest.json --out ../archives/cleanup.zip
```

Install the entire `feltwillow-acceptance-cleanup` skill folder under `.claude/skills/`, preserving `.agents/skills` links. Run the synthetic tests before live use:

```bash
python3 -m unittest discover -s .claude/skills/feltwillow-acceptance-cleanup/tests -q
```

Do not declare success if all that happened was an inventory or dry run. State actual local commit or remaining blocker. If safe candidate removals are only a small fraction of total data, explain why and report the *real* measured savings rather than broad promises.
