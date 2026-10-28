# Committed automatic cleanup manifest

## Source of authority

Cleanup is **pre-authorized for exact committed superseded files** that pass technical checks; the owner does not need to approve a manifest twice. This is NOT permission to select images, alter artwork, reinterpret story beats, bypass locked-camera checks, or rewrite historical owner decisions. A successful Git commit and a clean tracked working tree are necessary but **not sufficient** to prove a file obsolete.

The agent must inspect actual local owner-selection records and resolved scene-use matrices before constructing a manifest. Protect all selected images, immutable authority records, canonical performance, source plates, current Wan sources, and required provenance. **Dynamic runtime dependency analysis cannot be fully automated by a string scan**; keep any ambiguous file.

## Automatic removal manifest (must be outside repo)

This format is read by `scripts/prune_committed.py`. Use current actual paths/hashes, never placeholders. Each SHA refers to **the full Git-tracked file bytes**, not a Git blob ID.

```json
{
  "schema": "feltwillow.cleanup-committed.v1",
  "source_branch": "wan-new-image-approach",
  "source_head": "<current 40-hex commit>",
  "authority_records": [
    {"role": "owner_selection", "path": "<committed owner selection ledger>", "sha256": "<sha256>"},
    {"role": "scene_use_resolution", "path": "<committed active-use resolver/index>", "sha256": "<sha256>"}
  ],
  "keep": [
    {"path": "<exact currently selected source image>", "sha256": "<sha256>"}
  ],
  "files": [
    {
      "path": "<exact superseded rNNN_candidate.png>", "sha256": "<sha256>",
      "category": "superseded_revision",
      "replacement": {"path": "<exact accepted rMMM_candidate.png>", "sha256": "<accepted sha256>"},
      "owner_record": "<authority_records.owner_selection.path>"
    },
    {"path": "<exact unused V7 review contact sheet>", "sha256": "<sha256>",
     "category": "review_derivative"}
  ],
  "validation_commands": [
    ["python3", "-m", "unittest", "tests.test_sequence_pipeline", "-q"],
    ["python3", "production/audio_visual_plan.py", "--story", "lion_and_mouse_v7", "validate"]
  ]
}
```

Authority roles additionally accept `performance_registry` and `source_plan`. At minimum one current `owner_selection` and one independent `scene_use_resolution` file are mandatory, both exact hash-checked. `keep` is the exact-hash retained set including all selected images/dependencies in the scope, not merely a single image. The runner checks keep bytes again after staged removal. A superseded revision's owner record must contain both the replacement hash and its filename/path. For V7 preview-only review artifacts use `review_derivative` without `replacement`/`owner_record`; for `stories/lion_and_mouse_v6/` use `legacy_v6`; for `character/characters/_chrono_probe/` use `chrono_probe`.

**Manifest is an agent-generated technical plan, not an owner approval.** The script validates supplied evidence but cannot establish artistic correctness or prove that every dynamic dependency has been discovered. The agent must check the complete selected-use resolution, and refuse to add any file still needed by tests, scripts, sidecars, or video.

## Mechanical gates in the runner

- Clean **tracked** working tree and index; branch/HEAD pinned. Untracked files remain untouched. No local or remote push.
- Each deletion is within a narrow permitted class, exact Git-tracked path, regular file without symlink traversal, SHA-256 matched, byte-for-byte recoverable from `HEAD:path` (not an LFS-only pointer).
- Current owner selection and scene-use authority hash-matched; exact selected replacement is retained and listed by the bound owner record; V7 owner approval/selection records cannot be deleted.
- No direct path, distinctive basename, old SHA or static HTML/Markdown backlink from any **retained tracked text**; no legacy-root token reference survives when retiring V6 or `_chrono_probe`. This is a **conservative lead test**, not perfect proof of dynamic references.
- At least one actual scoped unittest/production-validator command, run both before and after. Committed selected images and authority hashes must remain unchanged. No new tracked modifications; staged diff must be exactly the deletion manifest.
- If checks pass, exact-file `git rm` and **local commit** execute without further owner approval. If postchecks fail before commit, only newly staged removals are restored automatically. No `rm -rf`, `git clean`, reset, push, history rewrite or aggressive garbage collection.
- Maximum 250 files per manifest. Rebuild against the new HEAD for the next independent batch; do not reuse stale manifests or forcibly mark blocked items as safe.

## Distinguish cleanup from storage reclamation

`git rm` reduces working-tree files and future checkout footprint but **old bytes remain in Git commits**. The local history could disappear with loss of the disk when commits are unpushed; an off-machine backup or push is more durable, but neither is performed automatically by this skill. A full historic Git-size reduction is a separate exercise that can destroy recovery and is never inferred from this pre-authorization.

When desired, `archive_verified.py` can create an external byte-verified ZIP using its separate `feltwillow.cleanup-archive.v1` manifest. The archive does not need an additional owner sign-off but must be explicitly placed on a suitable volume. It is optional when recoverability from committed Git bytes is verified; the cleaner does not call it implicitly.

## Examples that must remain BLOCKED

- Newest `r008` is guessed accepted from filename instead of current owner selection.
- An old roll still serves as source lineage or Wan transition input.
- Active docs or tests refer to a legacy V6 pathname or `_chrono_probe` dynamic root.
- The requested candidate is selected by exact hash even if it has `candidate` in its filename.
- The only recoverable committed data is an LFS pointer without available content.
- A validator/test fails after removal; restore exact targeted files rather than altering test expectations or approvals.
- A read-only scan finds no reference but an active runtime builds the path dynamically; the agent must keep it.
