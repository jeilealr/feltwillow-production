# Feltwillow — autonomous committed cleanup (updated owner policy)

## New authorization

The project owner has explicitly changed the cleanup policy: **do not ask for a second deletion approval after every requested cleanup batch**. Once source-image selections and relevant files are genuinely committed, the local coding agent may remove mechanically verified obsolete files using the installed `feltwillow-acceptance-cleanup` skill and its fail-closed script, then create a **local cleanup commit**. No remote push, history rewrite or image generation is authorized.

This supersedes the old handoff's `Phase 2 — only after my explicit path/hash approval`, `Stop after inventory`, and `No commits` instructions **for safe cleanup transactions only**. It does not waive owner authority for artistic selection, new images, performance decisions, camera changes or deletion of active inputs.

## Instruction to the local DeepSeek High agent

Work in `/Users/lealroja/Documents/feltwillow/feltwillow-production` on `wan-new-image-approach`.

1. **Install the supplied updated skill** under `.claude/skills/feltwillow-acceptance-cleanup/` (replace the prior cleanup skill's files only; preserve sibling skills and `.agents/skills` link). Check the current worktree before copying so nothing unrelated is overwritten. Read its `SKILL.md` and `references/manifest-and-gates.md`; run its synthetic tests. Commit only the validated skill update and any already-verified current production work needed for a clean tracked worktree. Ignore unrelated untracked `.DS_Store` and never delete it automatically.
2. Verify live local branch/HEAD, S01–S08 selected exact hashes, owner records, scene-use resolution and source lineage. Protect accepted stills/canonicals, sidecars needed for reproducibility, current Wan inputs, props, plates, and selected approvals. Do not assume the highest `rNNN` revision is accepted.
3. Start with `S07` and `S08` superseded scene candidates and preview-only review files, then `S01`–`S06`, then `stories/lion_and_mouse_v7/review`, `stories/lion_and_mouse_v6` and `_chrono_probe` as separate dependency-scoped transactions. Batch at most 250 exact tracked paths. Some old review records still provide active approval/provenance and must survive.
4. Create a manifest **outside** the repo in `feltwillow.cleanup-committed.v1` schema, with exact current branch/HEAD, owner-selection and scene-use authority records, `keep` path/hashes, file paths/hashes/categories, selected-replacement authority for superseded revisions, and real focused validation commands. The script does NOT safely derive selected hashes by itself; use live resolver and owner records.
5. Run `prune_committed.py --dry-run`. If blocked, leave only blocked files; resolve valid technical stale references in a **separately tested local commit** if possible, then reconstruct the cleanup manifest for the new HEAD. Never weaken a test to force deletion; do not remove assets with unresolved dynamic references. Continue with independent, safe subsets **without asking me for deletion approval**.
6. Run `prune_committed.py --apply` for each passing manifest. It checks committed Git byte recoverability, exact original hashes, protected keep/authority files, retained textual links, and scoped tests before/after. It runs exact-path Git removal and **commits the removals locally automatically**. Failed posttests restore the staged target files; report the failure, not success.
7. Report exact cleanup commits, deleted tracked paths/bytes, selected-image hashes preserved, tests, and remaining blocked files. **Do not push, force-push, merge, rewrite Git history, run Git GC or delete untracked/ignored directories.** No image generation, new artistic decisions, GPU/Wan, external provider calls or credit spend.

### Commands (from Git root)

```bash
python3 -m unittest discover -s .claude/skills/feltwillow-acceptance-cleanup/tests -q

python3 .claude/skills/feltwillow-acceptance-cleanup/scripts/cleanup_audit.py inventory \
  --repo . --out ../feltwillow-cleanup-inventory.json --scenes S07 S08

# Prepare ../feltwillow-cleanup-manifest.json from actual local authority.
python3 .claude/skills/feltwillow-acceptance-cleanup/scripts/prune_committed.py \
  --repo . --manifest ../feltwillow-cleanup-manifest.json --dry-run

python3 .claude/skills/feltwillow-acceptance-cleanup/scripts/prune_committed.py \
  --repo . --manifest ../feltwillow-cleanup-manifest.json --apply
```

### Safety and storage note

Git committed files can be recovered from the local commit history (the runner verifies the actual bytes for each removal). Removing them via `git rm` saves *working-tree* space and cleans future latest checkouts, but **does not remove the original large blobs from `.git` history**. Local unpushed commits are not an off-device backup. This task does not include deep history purification or a promise of total repository-size reduction.

The exact manifest protects selected art only if its keep/authority evidence is complete; textual reference scanning cannot detect all dynamically generated references. The agent must verify those separately and leave uncertain paths untouched. This is a cautious automatic cleanup, not a magical proof that every unused file can be found safely.
