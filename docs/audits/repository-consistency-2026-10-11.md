> **Snapshot, not a live readiness verdict.** This external audit inspected tracked commit `1c29c2e` on 2026-10-11. Use the current repository files, gates and remediation disposition for production decisions. The report below is preserved verbatim as the evidence and work register supplied for this remediation.

# Feltwillow Production — Repository Consistency Audit

**Repository:** `jeilealr/feltwillow-production`  
**Audited branch:** `working-cloud-branch`  
**Remote branch snapshot:** `1c29c2e96ee53890ca72c20b5d695e9471041bd0`  
**Audit date:** 2026-10-11  
**Audit basis:** [`docs/repository-consistency-audit-prompt.md`](https://github.com/jeilealr/feltwillow-production/blob/working-cloud-branch/docs/repository-consistency-audit-prompt.md)  
**Scope:** repository-wide tracked state, current story packets, shared production code, LUMI scripts, tests, skills, rules, READMEs, active v6 planning artifacts, historical/current status claims, cross-version boundaries, and tracked documentation links.

> This report consolidates the requested repository audit, issue register, remediation plan, and verification runbook into one Markdown file. No production files, generated media, approvals, story records, or GitHub repository files were changed by this audit.

---

## 1. Executive decision

### Overall status: **NO-GO for Lion and Mouse v6 video export/render**

The current branch is substantially safer and more coherent than the 2026-10-10 snapshot, but it is **not yet production-ready for v6 video**.

Two blockers are decisive:

1. **The 92 v6 individual keyframes are still candidates, with 0 hash-bound visual approvals and 2 current hash-bound known rejections.** The repository's own gate is deliberately fail-closed.
2. **The documented v6 pre-render toolchain does not match the current v6 data model.** The current v6 packet uses `scene_plan.json`, `keyframe_plan.json`, `staging_plan.json`, and `video_boundary_plan.json`, but the shared workflow still tells operators to use `prompt_manifest.json`, `timing_plan.json`, and `export_runtime.py`. Those files do not exist in the v6 story folder, and `export_runtime.py` contains additional schema assumptions that do not match the current v6 `visual_bible.json`.

The branch **is GO for read-only audit, code fixes, documentation fixes, tests, and construction of a new fail-closed v6 runtime adapter/preflight**. It is **NO-GO for v6 pilot GPU rendering, bulk rendering, final take selection, edit export, or publishing handoff** until the blockers and P1 defects below are closed.

### Current v6 facts confirmed from tracked state

- 161 English audio lines.
- 16 audio scenes.
- 683.67 seconds / 11:23.7 of assembled audio.
- Owner-authorized exact reuse of the unchanged v5 English recordings, copied under the v6 work namespace; the tracked `audio_manifest.json` records the source relationship and hashes.
- 52 visual units.
- 92 individual 1920×1080 keyframe candidates.
- 0 entries in `keyframe_visual_reviews.json.images`.
- 2 hash-bound known rejections: `s14_p04` and `s14_p05`.
- No tracked v6 `prompt_manifest.json`.
- No tracked v6 `timing_plan.json`.
- No tracked v6 `story.yaml`.
- No tracked v6 `runtime_inputs.json`.
- No tracked v6 `takes.yaml`.
- No v6 video takes or assembled edit claimed by the current v6 README.
- 154 tracked v6-related PNG blobs and **0 Git-blob SHA overlaps with tracked Lion/Mouse v5 PNGs**.
- 0 duplicate Git-blob groups within the 154 tracked v6 PNGs.

Stable snapshot link:  
<https://github.com/jeilealr/feltwillow-production/tree/1c29c2e96ee53890ca72c20b5d695e9471041bd0>

---

## 2. Evidence boundary and audit limitations

The audit was performed against the **remote tracked branch** through the GitHub repository connector. This gives exact tracked paths, Git blob IDs, text file contents, branch metadata, and JSON/Markdown source material, but it does not expose every local-machine fact.

### Evidence inspected

- Remote branch tree: 877 tracked files and 205 tracked directories.
- 120 tracked Markdown files.
- 57 tracked JSON files.
- 19 tracked YAML files.
- 45 tracked Python files.
- 449 tracked PNG files.
- All tracked Markdown files were scanned for repository-relative links.
- Current v6 story metadata and planning JSONs were parsed.
- Shared production Python, LUMI shell scripts, active skills, root docs, story READMEs, and current tests were inspected.
- Tracked v5/v6 PNG Git object IDs were compared for byte identity.

### Evidence that could **not** be independently inspected in this environment

1. **Local dirty state.** A remote branch cannot prove whether the owner's MacBook or LUMI checkout has modified tracked files.
2. **Untracked/ignored files.** A remote branch cannot prove what exists under ignored `.review/`, `work/`, model caches, LUMI scratch, or local archives.
3. **Generated WAV/MP4 bytes under `work/`.** The tracked `audio_manifest.json` is inspectable; the actual ignored WAV bytes are not remotely available here.
4. **The 92 PNG pixels.** The GitHub connector used here rejects binary Git blob downloads. Therefore I did **not** independently view the keyframes. Their paths/hashes/statuses were audited, and the repository's own tracked visual-audit conclusions are reported, but I do not claim pixel-level verification.
5. **Local test execution.** A local clone could not be materialized in the execution container, so tests/CLI commands were not independently run here.
6. **Large multi-megabyte prompt manifests.** The connector returned metadata but not full content for some very large manifests (notably v5 and Ugly Duckling). Findings for those files are therefore grounded in their tracked README/review/status documents, tree paths, and code contracts rather than a complete reparse of every manifest record.

These are **evidence limitations**, not evidence that the missing state is good or bad. The closing runbook gives commands to complete the local-only checks.

---

## 3. Repository inventory and active production states

### 3.1 Top-level tracked areas

- `.claude/skills/`
- `character/`
- `docs/`
- `feltwillow/`
- `lumi/`
- `production/`
- `stories/`
- `tests/`
- `voice/`
- `README.md`
- `CLAUDE.md`

### 3.2 Story state map

| Story | Current tracked state | Audit interpretation |
|---|---|---|
| `lion_and_mouse_v6` | New v6-native visual foundations; 16-scene audio/story coverage; 92 individual keyframe candidates; boundary planning; no video | **Active current Lion/Mouse production. NO-GO for video.** |
| `lion_and_mouse_v5` | Historical runtime/render production; story/runtime/timing files; render review; owner take selection incomplete | Historical but still operationally relevant for retained audio provenance and v5 take review. |
| `ugly_duckling_v1` | Extensive generated stills; scenes 1–9 have a tracked render review for 126 takes; Scene 11 canonical problem; later scene-image work exists | **Not merely “in preparation.”** Status documentation is inconsistent. |
| `boy_who_cried_wolf_v1` | Script/shot plan/prompt packet; README says nothing generated | Preparation; owner CR-01 review still required. |
| `tortoise_and_hare_v1` | Script/shot plan/prompt packet; README says nothing generated | Preparation; owner CR-01 review still required. |

### 3.3 Test/CI inventory

Tracked tests:

- `tests/test_keyframe_visual_gate.py`
- `tests/test_lipsync_attribution.py`
- `tests/test_staging_contract.py`
- `tests/test_story_packet_speakers.py`
- `tests/test_video_boundary_plan.py`

No tracked `.github/` workflow path was present in the audited branch.

---

## 4. Source-of-truth map

The repository now has **two distinct production data models** and needs to state that explicitly.

### 4.1 Manifest-backed stories

Examples: v5, Ugly Duckling, Tortoise/Hare, Boy Who Cried Wolf.

Primary authority:

- `visual_bible.json` — character/place/setup rules.
- `prompt_manifest.json` — image/video records.
- `dialogue_coverage.json` — lines/speakers.
- `timing_plan.json` / `TIMING_SHEET.md` — where generated.
- `story.yaml` / `runtime_inputs.json` — runtime render inputs where exported.
- Story README/review documents — owner/review state.

### 4.2 Current Lion and Mouse v6

Primary authority is different:

- [`visual_bible.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/visual_bible.json)
- [`audio_manifest.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/audio_manifest.json)
- [`dialogue_coverage.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/dialogue_coverage.json)
- [`scene_plan.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/scene_plan.json)
- [`visual_sequence_plan.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/visual_sequence_plan.json)
- [`staging_plan.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/staging_plan.json)
- [`keyframe_plan.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/keyframe_plan.json)
- [`keyframe_visual_reviews.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/keyframe_visual_reviews.json)
- [`video_boundary_config.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/video_boundary_config.json)
- [`video_boundary_plan.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/video_boundary_plan.json)
- Story-local review Markdown, especially `KEYFRAME_CONSISTENCY_AUDIT.md`, `KEYFRAME_REVIEW.md`, and `VIDEO_BOUNDARIES.md`.

**Critical consistency rule:** generic docs/skills must not pretend the current v6 packet is already a `prompt_manifest.json`/`timing_plan.json` chained packet. It is not.

---

## 5. Positive controls and fixes confirmed since the 2026-10-10 audit

These are important because the previous audit is no longer an accurate current-state summary.

### 5.1 Cross-version visual byte reuse is no longer present in tracked v6 PNGs

The 2026-10-10 audit found 12 byte-identical v5/v6 visual assets. At the audited 2026-10-11 branch snapshot:

- 143 tracked Lion/Mouse v5 PNGs were compared with 154 tracked Lion/Mouse v6 PNGs by Git blob SHA.
- **Cross-version identical tracked PNG count: 0.**
- Duplicate Git-blob groups within v6: **0**.

This is strong evidence that the current tracked v6 visual files are not simple byte copies of tracked v5 PNGs.

### 5.2 The owner-authorized audio exception is now tracked explicitly

Current v6 docs state that the unchanged English recordings from v5 are intentionally retained and copied into the v6 work namespace. `audio_manifest.json` records:

- `story = lion_and_mouse_v6`
- `source_story = lion_and_mouse_v5`
- 161 line records
- 16 scenes
- 683.67 seconds total
- source and v6 collections
- per-line provenance/hashes

This replaces the obsolete idea that **all** cross-version input is prohibited. The correct current rule is:

> **Visual assets/clips/renders remain version-isolated. Exact unchanged v5 English audio is an explicit owner-authorized provenance exception, staged under the v6 work namespace and hash-recorded.**

### 5.3 A proper hash-bound v6 visual gate now exists

[`production/keyframe_visual_gate.py`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/production/keyframe_visual_gate.py) checks:

- candidate file exists;
- actual SHA-256 matches `keyframe_plan.json`;
- known rejection hash;
- per-image review exists;
- review hash matches current PNG;
- reviewer/date present;
- size anchor and evidence present;
- all eight visual checks are explicitly true.

It exits non-zero when blockers exist.

### 5.4 Boundary planning is explicit and tested

The v6 boundary plan includes all 16 scenes. Shared-boundary entries exist only for:

- Scene 8 from Scene 7
- Scene 11 from Scene 10
- Scene 14 from Scene 13

Those shared entries use the exact preceding scene end path as the next scene start boundary. Crop/location changes are modeled as cuts rather than implicit size morphs.

### 5.5 Prior `chain_preview.py` defects appear fixed in current code

The current implementation:

- converts float image arrays to `uint8` before `PIL.Image.fromarray`;
- uses the previous output's last frame and current output's first frame in join sheets;
- supports `--fail-on-flagged-joins`.

The remaining problem is **workflow invocation**: the active skill's command called “strict join test” does not include that failure flag. See FWA-003.

### 5.6 Cross-story runtime argument checks were hardened

`export_runtime.py` now verifies the manifest belongs to the requested story and enforces same-story image set usage for independent stories. That closes a prior class of cross-story invocation error, although the current v6 packet still cannot use this exporter for different reasons (FWA-002).

### 5.7 The prior LUMI `WITH_CONDA` unbound-variable defect appears resolved

Current `lumi/env.sh` activates the configured venv and no longer contains the previously reported unguarded `WITH_CONDA` access.

---

# 6. Current findings

## Summary register

| ID | Severity | Status | Finding |
|---|---:|---|---|
| FWA-001 | P0 | VERIFIED | All 92 v6 keyframes remain unapproved; two current hashes are explicitly rejected. |
| FWA-002 | P0 | VERIFIED | The documented v6 runtime/export path is structurally non-runnable against the current v6 data model. |
| FWA-003 | P1 | VERIFIED | Active “strict” handoff/join commands are not fail-closed for all blockers. |
| FWA-004 | P1 | VERIFIED | `lumi/render_story.sh` skips existing MP4s on filename existence and bypasses receipt/hash validation. |
| FWA-005 | P1 | VERIFIED | LUMI render and backup scripts ignore configurable `FELTWILLOW_WORK`. |
| FWA-006 | P1 | VERIFIED | Current authority documents contradict each other on v6 audio/status and contain a stale “no v6 images” instruction. |
| FWA-007 | P1 | VERIFIED | Ugly Duckling state is internally inconsistent and not reproducible from the tracked clone alone. |
| FWA-008 | P2 | VERIFIED | Repository-wide docs contain 22 broken relative-link occurrences plus stale removed-version defaults/claims. |
| FWA-009 | P2 | VERIFIED | The 2026-10-10 audit is materially stale but is still linked as if current. |
| FWA-010 | P2 | VERIFIED | Critical gates have only five tracked tests and no observed CI workflow. |
| FWA-011 | P2 | VERIFIED | v5 status/count/shot-plan documents drift from current tracked render history. |
| FWA-012 | P1 | VERIFIED | Shared skills/rules still model v6 as a prompt-manifest chained story even though current v6 uses a different planning pipeline. |
| FWA-013 | P2 | EVIDENCE GAP | Ignored/local `work/` evidence and local dirty state are not independently reproducible from Git. |
| FWA-014 | P3 | VERIFIED | `chain_packet.py` retains legacy v5→v6 copy machinery behind guards, increasing maintenance and misuse risk. |

---

## FWA-001 — All 92 v6 keyframes remain unapproved; two are known rejected

**Severity:** P0  
**Evidence:** VERIFIED metadata/gate state; pixel-level review not independently performed in this audit.

Current v6 tracked status explicitly says the 92 individual PNGs are candidates, not video-approved frames. `keyframe_visual_reviews.json` has an empty `images` map and two current hash-bound rejections:

- `s14_p04` — SHA-256 `93abc605530d0c61f777d7c11f066fe416d0794bb6484ae2baeb9fa9d1a504cc`
- `s14_p05` — SHA-256 `4d61b32eada6e4fbec9ad9c7dad7258948280c371b21a37a52454821ffb2bf12`

Tracked rejection reason: Leo appears despite a one-animal insert plan and his face drifts from the approved canonical.

Evidence:

- [`KEYFRAME_CONSISTENCY_AUDIT.md`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/KEYFRAME_CONSISTENCY_AUDIT.md)
- [`KEYFRAME_REVIEW.md`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/KEYFRAME_REVIEW.md)
- [`keyframe_visual_reviews.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/keyframe_visual_reviews.json)
- [`keyframe_visual_gate.py`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/production/keyframe_visual_gate.py)

### Remediation

1. **Do not approve around the two rejection records.** Create new revisions for `s14_p04` and `s14_p05`; never overwrite the rejected bytes.
2. Update their planning prompt/staging source so the insert is genuinely one-character:
   - Milo only where the plan requires Milo;
   - Leo fully off-camera;
   - trap/net state must match adjacent Scene 14 frames;
   - maintain the same approved `trap_morning` plate/crop.
3. Save the replacement candidates with new revision filenames.
4. Update `keyframe_plan.json` only through the plan-generation workflow; preserve the rejected hashes in the review ledger for provenance.
5. Run full-resolution human review over **all 92** current candidate hashes, not only the two known rejects.
6. For every accepted candidate, write a `keyframe_visual_reviews.json.images[frame_id]` entry containing:
   - exact SHA-256;
   - reviewer;
   - review date;
   - exact same-setup size anchor;
   - measured size evidence;
   - `identity = true`;
   - `approved_plate = true`;
   - `anatomical_scale = true`;
   - `same_depth_landmark_scale = true`;
   - `ground_contact = true`;
   - `visible_animal_count = true`;
   - `world_state = true`;
   - `adjacent_continuity = true`.
7. Review all shared scene boundaries and every `same_view_motion_candidate` as paired endpoints, not as isolated attractive images.
8. Re-run the gate.

### Exit criteria

```bash
python3 production/keyframe_visual_gate.py --story lion_and_mouse_v6
```

must exit `0` and report `0 blockers; 92 candidate keyframes`.

Also require an owner-signed review of all 92 hashes before any runtime export.

---

## FWA-002 — The current v6 runtime/export path is structurally non-runnable

**Severity:** P0  
**Evidence:** VERIFIED.

This is the most important code/data contract defect.

The current v6 story folder has **no**:

- `prompt_manifest.json`
- `timing_plan.json`
- `story.yaml`
- `runtime_inputs.json`
- `takes.yaml`

Yet the root README and active chained-story skill instruct users to run `image_prompts.py`, `chain_plan.py`, and `export_runtime.py` against a v6 prompt manifest.

`export_runtime.py` itself hardcodes:

```text
stories/<story>/prompt_manifest.json
```

and then, for an independent story, requires:

```python
bible.get("version") == args.story
bible.get("asset_revision_policy") == "v6_native_assets"
```

But the current v6 bible begins with:

```json
{
  "revision": "v6-scene-coverage-2026-10-11",
  "version": "v6",
  "status": "foundations_approved_keyframe_candidates_pending_owner_review"
}
```

There is no `asset_revision_policy` top-level field, and `"v6"` is not equal to the story slug `"lion_and_mouse_v6"`.

Even if a new prompt manifest were added tomorrow, the current exporter would still fail the bible-version/policy checks unless this contract is reconciled.

Evidence:

- [`export_runtime.py` around its story/manifest checks](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/production/export_runtime.py#L129-L205)
- [`visual_bible.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/visual_bible.json)
- [`README.md` generic pipeline](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/README.md#L36-L60)
- [`audio-chained-coverage` skill](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/.claude/skills/audio-chained-coverage/SKILL.md)

### Remediation — choose one architecture explicitly

**Recommended:** keep the new v6 keyframe/boundary model and build a dedicated adapter/exporter. Do not force the story backward into the old inherited prompt-manifest representation just to satisfy old tools.

1. Define a tracked v6 runtime schema, for example:
   - `video_piece_plan.json` or `runtime_plan.json`;
   - one clip unit per timed interval;
   - exact start image path/hash;
   - exact end image path/hash;
   - scene number;
   - audio interval/line IDs;
   - speaker/mouth mode;
   - cut/shared-boundary semantics;
   - approved review receipt IDs.
2. Build it from:
   - `audio_manifest.json`
   - `dialogue_coverage.json`
   - word timings when final
   - `keyframe_plan.json`
   - `keyframe_visual_reviews.json`
   - `video_boundary_plan.json`
3. Make the exporter call `keyframe_visual_gate.validate(...)` and refuse any unapproved/currently rejected image.
4. Add a **story identity field with one meaning**. Recommended:
   ```json
   "story": "lion_and_mouse_v6",
   "version": "v6"
   ```
   Then validate `bible["story"] == args.story`; do not compare a short version label to a story slug.
5. Either add a general policy field such as:
   ```json
   "asset_revision_policy": "independent_native_visuals"
   ```
   or remove the special hardcoded string `v6_native_assets` and derive isolation from the explicit story/version policy.
6. Represent the audio exception precisely:
   - runtime namespace owner = `lion_and_mouse_v6`;
   - provenance source = `lion_and_mouse_v5`;
   - exact source/v6 byte hashes must agree with the tracked audio manifest.
7. Generate `story.yaml` (if `shot.py` remains the renderer) only from the new validated runtime plan.
8. Generate a hash-bound runtime input receipt before GPU submission.
9. Update all docs/skills to show **two workflows**:
   - manifest-backed stories;
   - current keyframe-plan v6 pipeline.
10. Add tests that assert the current tracked v6 packet can reach the runtime-export preflight once reviews are populated, without requiring a fictitious `prompt_manifest.json`.

### Minimum tests to add

- current v6 bible identity is accepted;
- wrong story slug fails;
- missing visual review fails;
- known-rejected hash fails;
- wrong candidate hash fails;
- audio namespace/provenance mismatch fails;
- boundary plan missing image fails;
- unapproved shared boundary fails;
- runtime generation never writes partial output after a preflight error.

### Exit criteria

A **read-only preflight** on current v6 inputs should reach exactly one failure class before reviews are complete: visual approvals. After review fixtures are supplied, it should succeed without requiring deleted/absent legacy files.

---

## FWA-003 — “Strict” handoff/join commands are not fully fail-closed

**Severity:** P1  
**Evidence:** VERIFIED.

### A. The active skill's “Strict join test” is not strict about flagged joins

The skill says:

```bash
production/chain_preview.py --story <slug> --until S --require-takes
```

but `chain_preview.py` only exits non-zero for measured flagged joins when **both** review conditions are enforced through:

```bash
--fail-on-flagged-joins
```

`--require-takes` verifies chosen clips and frame counts; it does not make a visual jump flag fatal.

### B. The active handoff skill uses informational `audit`, not `audit --strict`

`image_handoff.py audit` prints blockers but returns success unless `--strict` is passed. The skill's tool table lists the non-strict form first as the current handoff check.

### Remediation

1. Change the active skill's strict join command to:
   ```bash
   lumi/run_in_container.sh python production/chain_preview.py \
     --story <slug> --until S --require-takes --fail-on-flagged-joins
   ```
2. Change any readiness/preflight instruction from:
   ```bash
   python3 production/image_handoff.py --story <slug> audit
   ```
   to:
   ```bash
   python3 production/image_handoff.py --story <slug> audit --strict
   ```
3. Preserve non-strict reporting by renaming/documenting it as an informational report:
   - `audit` = report only;
   - `audit --strict` = gate.
4. Add a test that creates one flagged join and asserts the documented strict command exits non-zero.
5. Add a test that injects one missing image approval and asserts `audit --strict` exits non-zero.
6. Never rely on printed words such as `BLOCKED` or `FLAGGED` if the process exit code remains zero.

### Exit criteria

Every command labeled “strict,” “gate,” “preflight,” or “ready” in active docs must return a non-zero status for every blocker it reports.

---

## FWA-004 — LUMI bulk renderer can skip stale existing MP4s without receipt validation

**Severity:** P1  
**Evidence:** VERIFIED.

`production/shot.py` has a strong `check_existing_render(...)` function that checks a sidecar and refuses stale/unrecorded render inputs.

But `lumi/render_story.sh` decides whether work is missing with this logic:

```python
if any(not (d / f"{s['name']}_s{k}_fast.mp4").is_file() for k in s["seeds"]):
    print("python production/shot.py ...")
```

If all expected MP4 filenames exist, the bulk driver does **not invoke `shot.py` at all**, so its stronger sidecar/hash verification is bypassed.

Evidence:

- [`lumi/render_story.sh`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/lumi/render_story.sh#L17-L27)
- [`production/shot.py` receipt check](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/production/shot.py#L41-L60)

### Remediation

1. Extract receipt checking from `shot.py` into a reusable pure function/module, e.g. `feltwillow/render_receipt.py`.
2. Add a read-only command:
   ```bash
   python3 production/shot.py --story ... --scene ... --shot ... --audit-existing --fast
   ```
   or a separate `production/render_receipt_audit.py`.
3. Change `render_story.sh`'s inventory step:
   - “complete” only if MP4 exists **and** sidecar exists **and** expected recipe/input hashes match;
   - “stale” if MP4 exists but receipt mismatches;
   - “missing” if MP4 absent.
4. Never silently overwrite stale output. Move/quarantine stale output only under an explicit operator action.
5. Log stale reasons into the task inventory before any GPU job.
6. Add tests:
   - MP4 + no sidecar => stale/fail;
   - MP4 + wrong keyframe hash => stale/fail;
   - MP4 + wrong model/settings => stale/fail;
   - MP4 + exact sidecar => complete;
   - partial seeds => only missing/stale seeds queued.
7. Make the bulk driver exit non-zero if stale existing media is found, unless an explicit `--rerender-stale` policy is selected.

### Exit criteria

An existing filename alone can never cause a render job to be considered complete.

---

## FWA-005 — `FELTWILLOW_WORK` is ignored by rendering and backup scripts

**Severity:** P1  
**Evidence:** VERIFIED.

Python path authority is:

```python
WORK = Path(os.environ.get("FELTWILLOW_WORK", REPO / "work")).resolve()
```

But:

- `lumi/render_story.sh` hardcodes `work/stories/...` and `work/tasks/...`.
- `lumi/backup_assets.sh` hardcodes `work/backup_files.txt`, `find work`, and `work/lora/...`.

This can cause the renderer to inspect the wrong directory and, more seriously, the backup tool to omit the real generated assets when `FELTWILLOW_WORK` is overridden.

Evidence:

- [`feltwillow/paths.py`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/feltwillow/paths.py)
- [`lumi/render_story.sh`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/lumi/render_story.sh)
- [`lumi/backup_assets.sh`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/lumi/backup_assets.sh#L21-L33)

### Remediation

1. Resolve the work root once through Python:
   ```bash
   WORK_ROOT="$(python3 -c 'from feltwillow.paths import WORK; print(WORK)')"
   ```
2. Use that value for:
   - shot inventory;
   - task files;
   - LoRA generated data;
   - backup list file.
3. Decide whether the backup manifest contains:
   - absolute paths, or
   - paths relative to a stable rsync root.
   Prefer an explicit pair: `backup_root` + relative file list.
4. Make the script print the resolved `FELTWILLOW_WORK` before doing anything.
5. Add a smoke test with a temporary override:
   ```bash
   FELTWILLOW_WORK=/tmp/feltwillow-work-test ...
   ```
   and assert no file under repository `work/` is consulted.
6. Add a backup dry-run mode that prints the exact included roots and count without invoking rsync.
7. Update `docs/lumi.md` to explain the work-root resolution.

### Exit criteria

Setting `FELTWILLOW_WORK` to an alternate directory changes **all** render inventory, task, generated-media, and backup paths consistently.

---

## FWA-006 — Current authority docs contradict v6 audio/status

**Severity:** P1  
**Evidence:** VERIFIED.

`CLAUDE.md` currently says, near the top, that v5's “assets, audio, timing and renders are not v6 inputs,” then later correctly records the 2026-10-11 owner authorization to reuse the exact v5 English line audio in v6.

It also retains an “Owner's current instruction (2026-10-09)” saying no v6 images were authorized/created before the audit, while the same branch now tracks 92 v6 keyframe candidates and a 2026-10-11 changelog entry for them.

This is dangerous because `CLAUDE.md` is explicitly presented as an operating manual for agents.

`feltwillow/version_policy.py` also says an independent story “requires its own audio,” which is operationally true only if “own” means **runtime namespace**, not **original provenance**. The wording can mislead a future maintainer into rerecording valid owner-retained audio.

Evidence:

- [`CLAUDE.md` current-state section](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/CLAUDE.md#L24-L58)
- [`CLAUDE.md` stale 2026-10-09 instruction](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/CLAUDE.md#L58-L75)
- [`feltwillow/version_policy.py`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/feltwillow/version_policy.py)
- [`audio_manifest.json`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/lion_and_mouse_v6/audio_manifest.json)

### Remediation

1. Replace:
   > v5 assets, audio, timing and renders are not v6 inputs
2. With:
   > v5 visual assets, timing plans, clips and renders are not v6 inputs. The exact unchanged English line recordings are the owner-authorized exception: their provenance is v5, their runtime copy is staged under the v6 work namespace, and hashes are recorded in `audio_manifest.json`.
3. Move the 2026-10-09 “no v6 images” instruction into a **Historical/Superseded instructions** subsection with an explicit superseded date of 2026-10-11.
4. Change `version_policy.py` wording from “requires its own audio” to “requires audio staged in its own runtime namespace; approved provenance reuse may be allowed by the story's audio manifest.”
5. Add a tiny policy test:
   - v6 runtime path points to v6 namespace;
   - source provenance may be v5 only when `owner_authorized_reuse` and matching hashes are present.
6. Ensure root README, v6 README, SCRIPT, CLAUDE, creation rules, lip-sync docs, and skills use the same provenance-vs-runtime language.

### Exit criteria

A search for `v5.*audio.*not.*v6` and equivalent claims finds no live authority text that contradicts the owner-authorized exception.

---

## FWA-007 — Ugly Duckling state is inconsistent and not reproducible from the tracked clone

**Severity:** P1  
**Evidence:** VERIFIED for tracked documentation/tree; local ignored assets unavailable.

There are multiple conflicts:

1. Root `README.md` groups Ugly Duckling with “next stories in preparation,” but:
   - its own README records extensive generated foundation/expression/scene frames;
   - `CLAUDE.md` records scene images through Scene 10/12 and a paused Scene 11;
   - `RENDER_REVIEW.md` records **126 takes** for 42 runtime clips across Scenes 1–9.
2. The Ugly README first says prompt lint is 0 errors, then in “Still open” records a newer 2026-10-09 audit with **22 missing-reference errors for 18 distinct files**.
3. Eleven Markdown link occurrences point to review/contact-sheet files that are not tracked in the branch. They may exist locally in ignored folders, but a clean clone cannot follow those evidence links.
4. Scene 11 is explicitly paused because the Ollie-swan canonical head shape disagrees with dependent expression/mouth references; generated Scene 11 keyframes must be redone after canonical approval.
5. `os_open_r01.png` is documented as duplicating a closed happy expression and needs a true open-mouth revision.
6. Scene 8 has a known narrative/plate mismatch: “snow has nearly melted” versus a fully snowy locked winter plate.

Evidence:

- [`ugly_duckling_v1/README.md`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/ugly_duckling_v1/README.md)
- [`ugly_duckling_v1/RENDER_REVIEW.md`](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/stories/ugly_duckling_v1/RENDER_REVIEW.md)
- [`CLAUDE.md` Ugly section](https://github.com/jeilealr/feltwillow-production/blob/1c29c2e96ee53890ca72c20b5d695e9471041bd0/CLAUDE.md#L65-L90)

### Remediation

1. Correct root README status:
   - Tortoise/Hare and Boy Who Cried Wolf may remain “in preparation.”
   - Ugly Duckling must be listed separately as an **active generated/rendered production with unresolved image/reference issues**.
2. In the Ugly README, make the newest lint state the top-line state. Do not say “lint 0” without a historical qualifier.
3. Restore the 18 missing exact reference files from the owner archive **if the same bytes are available**.
4. If exact references cannot be restored:
   - do not invent substitutes under the old IDs;
   - create new reference revisions;
   - update affected manifest records;
   - invalidate/re-review all dependent generated outputs.
5. Decide how review evidence is transported:
   - commit contact sheets if safe/appropriate; or
   - link to a tracked review index containing hashes and an explicit local/archive retrieval path; or
   - stop using relative Markdown links to ignored files.
6. Resolve Ollie-swan canonical:
   - owner approves r02 canonical;
   - rebuild dependent expressions/mouth references;
   - create a real open-mouth study;
   - regenerate every Scene 11 frame derived from old identity;
   - re-review and rehash.
7. Resolve Scene 8 snow state by owner decision:
   - either change the story line/prompt to fully snowy;
   - or create/approve a nearly-melted registered plate and regenerate affected frames.
8. Re-run prompt lint and record the actual current counts at the top of README.
9. Reconcile scene/render status with `RENDER_REVIEW.md`.

### Exit criteria

- 0 missing active reference errors.
- No README “0 errors” statement contradicts a newer lint result.
- Every review link resolves in a clean clone or is explicitly labeled local-only with retrieval instructions.
- Scene 11 identity dependency is rebuilt from the approved canonical.
- Scene 8 state mismatch has an owner-recorded decision.

---

## FWA-008 — 22 broken Markdown link occurrences and stale removed-version defaults

**Severity:** P2  
**Evidence:** VERIFIED across all 120 tracked Markdown files.

### Broken relative-link occurrences

1. `docs/character-consistency.md:8` → `../stories/lion_and_mouse_v4/README.md`
2. `docs/findings-and-risks.md:5` → `reviews/lion_and_mouse_v3_owner_notes_2026-09-30.txt`
3. `docs/findings-and-risks.md:6` → `../stories/lion_and_mouse_v4/REPAIR_PLAN.md`
4. `docs/findings-and-risks.md:8` → `../stories/lion_and_mouse_v4/README.md`
5. `docs/findings-and-risks.md:31` → `../stories/lion_and_mouse_v4/README.md`
6. `docs/findings-and-risks.md:32` → `../stories/lion_and_mouse_v4/TIMING_SHEET.md`
7. `docs/production-guide.md:13` → `../stories/lion_and_mouse_v4/README.md`
8. `docs/prompting.md:6` → `../stories/lion_and_mouse_v4/README.md`
9. `docs/prompting.md:325` → `reviews/lion_and_mouse_v3_owner_notes_2026-09-30.txt`
10. `docs/prompting.md:329` → `../stories/lion_and_mouse_v4/REPAIR_PLAN.md`
11. `stories/lion_and_mouse_v5/SHOT_PLAN.md:3` → `REPAIR_PLAN.md`
12. `stories/ugly_duckling_v1/README.md:12` → `review/foundation_characters_contact_sheet.png`
13. `stories/ugly_duckling_v1/README.md:12` → `review/foundation_plates_contact_sheet.png`
14. `stories/ugly_duckling_v1/README.md:12` → `review/expressions_contact_sheet.png`
15. `stories/ugly_duckling_v1/README.md:14` → `review/contact_sheets/scene-08_contact_sheet.png`
16. `stories/ugly_duckling_v1/README.md:14` → `review/contact_sheets/scene-09_contact_sheet.png`
17. `stories/ugly_duckling_v1/README.md:14` → `review/contact_sheets/scene-10_contact_sheet.png`
18. `stories/ugly_duckling_v1/README.md:14` → `review/contact_sheets/scene-12_contact_sheet.png`
19. `stories/ugly_duckling_v1/README.md:14` → `review/contact_sheets/scene-06_contact_sheet.png`
20. `stories/ugly_duckling_v1/README.md:14` → `review/contact_sheets/scene-07_contact_sheet.png`
21. `stories/ugly_duckling_v1/README.md:16` → `review/contact_sheets/s03_pond_keyframes_recreated_2026-10-07.png`
22. `stories/ugly_duckling_v1/README.md:64` → `review/contact_sheets/scene-08_contact_sheet.png`

The current v6 Markdown files had no broken repository-relative links in this scan.

### Additional stale version/tool examples

- `production/shot.py` example names removed `lion_and_mouse_v3`.
- `production/shot.py --story` defaults to removed `lion_and_mouse_v2`.
- `docs/production-guide.md` explicitly says v2-v4 folders were removed, then still says “current work is v4.”
- `docs/character-consistency.md` calls v4 current work despite the top-level historical scope note.
- `stories/lion_and_mouse_v5/SHOT_PLAN.md` is titled `# V4 shot and image index`.
- That same v5 shot plan links to removed `REPAIR_PLAN.md` and contains pre-render wording that no longer describes the v5 render history.

### Remediation

1. Make `production/shot.py --story` **required** instead of silently defaulting to a deleted story.
2. Replace v3 example with an existing story or generic `<story>`.
3. For historical v4/v3 links:
   - either link to a stable Git commit URL where the file existed; or
   - render them as historical paths in backticks, not clickable current links.
4. Fix `docs/production-guide.md` to distinguish:
   - current general pipeline;
   - historical v1-v4 examples.
5. Rename v5 shot plan heading to v5 and add a “historical imported from v4” note.
6. Remove/replace its broken repair-plan link with a Git-history permalink if the record matters.
7. Handle Ugly contact-sheet links as described in FWA-007.
8. Add a repository Markdown link checker test.

### Exit criteria

A clean-clone link scan reports 0 unintended broken repository-relative links. Any intentionally local-only link must be labeled as such rather than appearing as a normal tracked relative link.

---

## FWA-009 — The 2026-10-10 audit is materially stale but still presented as current evidence

**Severity:** P2  
**Evidence:** VERIFIED.

`docs/audits/repository-consistency-2026-10-10.md` is a valuable historical audit, but major conclusions changed within a day:

- prior 12 v5/v6 identical PNGs → current tracked overlap 0;
- no v6-local audio evidence → current tracked `audio_manifest.json`;
- no individual v6 keyframes → now 92 candidate keyframes;
- old `chain_preview` dtype/join-sheet/strict-mode defects → code changed;
- prior LUMI `WITH_CONDA` problem → current env script changed;
- old v6 prompt-manifest packet → current v6 is a different keyframe/scene-plan architecture.

The root README still links the old audit without a prominent superseded warning.

### Remediation

1. Add a top banner to the 2026-10-10 report:
   > **Historical snapshot. Superseded for current readiness by the 2026-10-11 repository consistency audit. Do not use old finding status as current production authority without revalidation.**
2. Preserve the old audit unchanged below the banner.
3. Link this current audit beside it.
4. Add a short disposition table for major old findings:
   - resolved;
   - still open;
   - superseded by new architecture;
   - evidence unavailable.
5. Ensure agents are told to use the newest dated audit for readiness, while old audits remain evidence/history.

### Exit criteria

No current README/skill presents the 2026-10-10 finding state as the latest readiness decision.

---

## FWA-010 — Critical gates have limited tests and no tracked CI

**Severity:** P2  
**Evidence:** VERIFIED.

There are five test modules and no tracked `.github/workflows/`.

The current tests are useful, especially for staging, video boundaries, and the visual review gate, but they do not cover several high-risk contracts found in this audit.

### Missing/high-value regression tests

1. Current v6 runtime/export adapter preflight.
2. v6 story slug versus short version label.
3. v6 audio provenance exception versus runtime namespace isolation.
4. `render_story.sh` stale MP4/sidecar detection.
5. `FELTWILLOW_WORK` override for rendering.
6. `FELTWILLOW_WORK` override for backup.
7. Markdown relative-link integrity.
8. Active skill command strictness.
9. `image_handoff audit --strict` exit behavior.
10. `chain_preview --require-takes --fail-on-flagged-joins`.
11. Root/story current-status parity.
12. No deleted-story default in executable CLI help/examples.

### Remediation

1. Add focused unit tests first.
2. Add a small CI workflow that runs on PRs:
   ```bash
   python -m unittest discover -s tests -p 'test_*.py'
   python -m compileall feltwillow production
   ```
3. Add read-only repository consistency checks:
   - link checker;
   - v6 plan/review hash schema validation;
   - no missing tracked paths referenced by active docs;
   - no current CLI default points to a removed story.
4. Do not require GPU, image generation, model downloads, or private `work/` media in baseline CI.
5. Use tiny fixtures for render receipts and path-root behavior.

### Exit criteria

Every P0/P1 code contract in this report has at least one regression test, and those tests run automatically on repository changes.

---

## FWA-011 — v5 status/count and shot-plan documents drift

**Severity:** P2  
**Evidence:** VERIFIED.

Tracked documents tell different versions of the v5 render history:

- root README: 186 rendered clips;
- `RENDER_REVIEW.md`: 62 runtime shots × 3 = 186 clips, then records a later added `s05_tumble` bridge with 3 seeds;
- v5 README: 63 shots, 3 seeds each, and later refers to 189 existing takes.

The most consistent tracked interpretation is **186 initial + 3 bridge = 189**, but the actual ignored `work/` directory was unavailable here, so this report does not substitute a guessed runtime inventory for a local count.

Additionally, `stories/lion_and_mouse_v5/SHOT_PLAN.md` still says “V4 shot and image index,” links a removed repair plan, and contains pre-render status text.

### Remediation

1. On the machine with v5 `work/`, compute:
   - current runtime shot count from `story.yaml`;
   - expected seed count;
   - actual MP4 count;
   - valid sidecar count;
   - stale/no-receipt count.
2. Write a small tracked `render_inventory.json` receipt containing counts and the audit timestamp, not the media itself.
3. Reconcile root README, v5 README, and RENDER_REVIEW summary to that inventory.
4. Preserve the historical 186 review as:
   > initial 62-shot batch: 186; later bridge: +3.
5. Update v5 SHOT_PLAN heading and status note.
6. Do not imply old v5 clips are reproducible from missing/deleted prompt references; the v5 README already documents known lint gaps.

### Exit criteria

All current-status docs agree on the expected/actual valid v5 take count, and historical batch counts are clearly labeled.

---

## FWA-012 — Shared skills/rules still treat current v6 as an old prompt-manifest chained story

**Severity:** P1  
**Evidence:** VERIFIED.

The active `.claude/skills/audio-chained-coverage/SKILL.md` explicitly says it applies to “Lion and Mouse v6 onward,” then instructs:

- `chain_plan.py`
- `image_handoff.py`
- `image_prompts.py`
- `prompt_manifest.json`
- `export_runtime.py`

and says each piece is written in the current story's manifest.

The current v6 packet, however, has moved to:

- scene boards;
- visual units;
- individual keyframe plan;
- staging plan;
- boundary plan;
- visual review ledger.

The root README has the same split personality: its “Where to find things” section correctly tells v6 users to start from the keyframe audit and says generated prompts are historical provenance, while the earlier generic “Consistent images” section still gives `image_prompts.py --story lion_and_mouse_v6 build/lint/md/review`.

`docs/creation-rules.md` CR-21 also describes v6 as manifest pieces, while current `video_boundary_plan.json` explicitly calls itself a planning contract pending visual review and word timing.

### Remediation

1. Define explicit story pipeline modes, for example:
   ```json
   "pipeline": "keyframe_boundary_v1"
   ```
   versus:
   ```json
   "pipeline": "prompt_manifest_v1"
   ```
2. At the top of both active skills, branch instructions by pipeline.
3. For current v6, replace old commands with:
   - staging validation;
   - keyframe plan integrity;
   - visual gate;
   - boundary plan review;
   - word timing;
   - new runtime adapter from FWA-002.
4. Keep `chain_packet.py`/prompt-manifest commands only for stories that actually have that schema.
5. Remove the root README's v6-specific `image_prompts.py build` example unless v6 is deliberately converted back to a manifest packet.
6. Update CR-21 to say its old manifest implementation is one implementation of audio-driven coverage, not the only representation.
7. Add a test/doc check: any command shown with `--story lion_and_mouse_v6` must have all required tracked input files.

### Exit criteria

A new agent following only README + skills can execute the documented **read-only v6 preflight** without immediately encountering a missing `prompt_manifest.json` or schema mismatch.

---

## FWA-013 — Local/ignored production evidence is not reproducible from Git alone

**Severity:** P2  
**Classification:** EVIDENCE GAP, not proof of a production defect.

The repository intentionally keeps generated media under ignored `work/`, but current readiness decisions depend on facts that are not independently available in a clean remote checkout:

- actual v6 WAV bytes copied from v5;
- `timing.json`;
- future `word_timings.json`;
- v5/other-story MP4s;
- render sidecars;
- local contact sheets in ignored paths;
- local dirty/untracked changes.

This is acceptable for large media if the repository keeps **small, tracked, hash-bound receipts**. The current v6 `audio_manifest.json` is a good example of that pattern and should be extended to other stages.

### Remediation

1. Add a generic tracked receipt schema for ignored production assets:
   - logical ID;
   - relative runtime path;
   - SHA-256;
   - byte size;
   - duration/frame count where applicable;
   - generating tool/version;
   - source input hashes;
   - review/selection status.
2. Track receipts, not large media.
3. Add a read-only verifier that checks local `work/` against receipts.
4. Have LUMI and MacBook write the same schema.
5. Record whether validation ran on Mac, LUMI, or both.
6. For contact sheets that are relied on in tracked README evidence, either track them or store a tracked hash/index plus retrieval location.

### Exit criteria

A clean clone can say exactly which ignored artifacts are required and their expected hashes, and an operator can validate a local/LUMI work tree without guessing.

---

## FWA-014 — Legacy v5→v6 copy machinery remains in `chain_packet.py`

**Severity:** P3  
**Evidence:** VERIFIED.

`chain_packet.py` still contains functions that remap `lion_and_mouse_v5` paths into `lion_and_mouse_v6` and copy older assets into v6-local folders. The current entry point has guards that refuse the independent v6 story, which is good, but keeping story-specific v5→v6 migration machinery in a general active tool creates maintenance and accidental-use risk.

### Remediation

1. Keep the hard guard permanently.
2. Move one-off v5→v6 migration code into:
   - a historical migration script under an archive/tools-history area; or
   - remove it once Git history is sufficient.
3. Generalize any reusable functionality so it does not hardcode Lion/Mouse v5/v6 paths.
4. Add a test asserting `chain_packet.py` refuses every story marked independent.
5. Update its module docstring to emphasize that it is **not** part of current v6.

### Exit criteria

No active general-purpose production tool contains story-specific code that could silently recreate the superseded v5→v6 inheritance path.

---

# 7. V6 visual evidence ledger

## 7.1 Independent visual-review disclosure

**Independent images viewed by this audit: 0 / 92.**

Reason: the GitHub connector exposed tracked paths and hashes but not binary PNG bytes. I therefore did not claim visual identity/scale/grounding review.

**Repository-authored visual evidence inspected:** `KEYFRAME_CONSISTENCY_AUDIT.md`, `KEYFRAME_REVIEW.md`, `keyframe_visual_reviews.json`, staging/boundary plans.

**Known current rejected hashes:** 2 (`s14_p04`, `s14_p05`).

**All other entries:** still require full-resolution hash-bound visual review before video.

## 7.2 Exact active keyframe hash inventory

| Scene | ID | Candidate file | SHA-256 |
|---:|---|---|---|
| 1 | `s01_p01` | `s01_p01_r02_candidate.png` | `a465b073f5c0fba26474821e300d2fa2534b2e1d0c074961083d2e51ed6580b8` |
| 1 | `s01_p02` | `s01_p02_r02_candidate.png` | `ef6a1c389e1b7f915d3707a98cc9c86d03c3ed4b8345da92146e8b36c9d9d372` |
| 1 | `s01_p03` | `s01_p03_r02_candidate.png` | `1e561bc6808c31f6ade6a1b3f059194b791f3f872c3606bf574f58ffa69a27fc` |
| 1 | `s01_p04` | `s01_p04_r02_candidate.png` | `bdbd5175e4cd86ca2313290dd727da794a924b2215c10dfeb95338b94e94581f` |
| 2 | `s02_p01` | `s02_p01_r01_candidate.png` | `7586087fe870e237f31c2f92572ce5c2cd8249dd76675a39a17153892177dcbf` |
| 2 | `s02_p02` | `s02_p02_r01_candidate.png` | `e890692698af2e5ecd60b4728862dcee6872ce8ab8bd02a9250556be4e45cac7` |
| 2 | `s02_p03` | `s02_p03_r01_candidate.png` | `6cf9f93e8ed9b713555f54f6a5f6c2d22ad1655a09ae0144b6b1e82a821c333b` |
| 3 | `s03_p01` | `s03_p01_r01_candidate.png` | `82f23e9edd68eab25286f0a109bf96741079009ac1c5af1493df01b94f183fe2` |
| 3 | `s03_p02` | `s03_p02_r01_candidate.png` | `24d7b5a3ccc49a7eee53cdf109b72013f0d8222944f5b62f24d449b4ae7cd53b` |
| 3 | `s03_p03` | `s03_p03_r01_candidate.png` | `7cb12ef07cb04ef2f2fe7a700abe3d297cff09c8c8a6251631527eb846de7357` |
| 3 | `s03_p04` | `s03_p04_r01_candidate.png` | `527ec61eb3afcb9838612d3f9532a7457cd6e90ca7169df7d508ad31ef2046f2` |
| 4 | `s04_p01` | `s04_p01_r01_candidate.png` | `2c3a602de2ecc385a196b9507e9bebde6aa46ec6adca5b2e65b1a9be73647355` |
| 4 | `s04_p02` | `s04_p02_r01_candidate.png` | `eefe0f027244596717419457c7a5318d065a95972289d5e3126f79e0cd0b3134` |
| 4 | `s04_p03` | `s04_p03_r01_candidate.png` | `9fec78932553bd7800cf37daaf2521562ddd0935a311f36079216173d81fad02` |
| 4 | `s04_p04` | `s04_p04_r02_candidate.png` | `938acad5bfb2a73e6da3d12d6314f6476cdfbe8cc9a0b2b026e908ceb7fbe1f0` |
| 5 | `s05_p01` | `s05_p01_r01_candidate.png` | `0009c8ce44fb26cb9f67a87b30346d740612a495bbfa6ef469b01783d67f27d6` |
| 5 | `s05_p02` | `s05_p02_r01_candidate.png` | `e9572aa5d6cf8d2e4e78c26bdd4b2cc3c0c8ac9763378ef8affa5a8f8b1f7625` |
| 5 | `s05_p03` | `s05_p03_r01_candidate.png` | `fa776f0863a22e62c622cd7a33403cd373b1f74dda90f15a1d3db5b88650fe69` |
| 5 | `s05_p04` | `s05_p04_r02_candidate.png` | `3931c2e7cd8178f70cead46f63d30fa2beff9a3765e077f56762a7d766019e62` |
| 6 | `s06_p01` | `s06_p01_r02_candidate.png` | `557c69471b9773359b2453ac18af082387f9a359c7b4707305cd60ca9c747c6a` |
| 6 | `s06_p02` | `s06_p02_r02_candidate.png` | `625f930a477d1ae60a448ccf1e36830f880d69379ce0a37dc8df346b2c27aa61` |
| 6 | `s06_p03` | `s06_p03_r01_candidate.png` | `e0ca0407810e298a1e65cea7f2d44f44401bd2dc776d1b8b77f16ae4bc5f971c` |
| 7 | `s07_p01` | `s07_p01_r01_candidate.png` | `3012bf04bbe0bb8f29c220ad5df433a452f7a404a6ce10623e8bd36e38cb0456` |
| 7 | `s07_p02` | `s07_p02_r01_candidate.png` | `28f089b2ac0f9531bfb28b8e4d20f9abd2da5b2d47e621704df64fdea10a4766` |
| 7 | `s07_p03` | `s07_p03_r01_candidate.png` | `5b87a398b75b07eb52eab783a6be6264d1b9f1238896118fbc007c39ccbdf869` |
| 7 | `s07_p04` | `s07_p04_r01_candidate.png` | `71cf932369966d1b23eafb51cd5a1f4bc353fb45dd767b4eb85beb417264117b` |
| 8 | `s08_p01` | `s08_p01_r01_candidate.png` | `fe5b93002c5661843fd3b85f50df264e8293a240648e9901de0621cbe6c34e13` |
| 8 | `s08_p02` | `s08_p02_r01_candidate.png` | `d13e993d01a2e24f27e0f5d0f9f1e9a053fd6d452208f52e3844124c87cbb6a9` |
| 8 | `s08_p03` | `s08_p03_r01_candidate.png` | `1d20768b98407d330de29075b138094b89ab0371b4dd8e598c1d2ca121a8d488` |
| 8 | `s08_p04` | `s08_p04_r01_candidate.png` | `bc8e7a76bccdc6acea2e015267d5cc4449d77e3add1effc407f770559db74234` |
| 8 | `s08_p05` | `s08_p05_r01_candidate.png` | `62f74531925c7322d20f879d136d0ec8dfa3a10ef4574738bfd4c35bd591e6a6` |
| 8 | `s08_p06` | `s08_p06_r01_candidate.png` | `9feb925f5e9e1458a32c3d4ae834afd64a5def559dcbb24a7f8cf420436cff2b` |
| 9 | `s09_p01` | `s09_p01_r01_candidate.png` | `e3cc58927d6165fb69a2a49167d4a9b08a32a61e83b2c9d8ff9a0e669b8f41d9` |
| 9 | `s09_p02` | `s09_p02_r01_candidate.png` | `4da028375bcbe1f915f330f722d9df2b04c315cf9ebca7f5ec2addb2d125f696` |
| 9 | `s09_p03` | `s09_p03_r01_candidate.png` | `9704f3940833d8edbcd8e695a50ca241702c52abee7263d2099dcb917b141442` |
| 9 | `s09_p04` | `s09_p04_r01_candidate.png` | `f374683976a52e0d0a4135e1417ceb78a763fcc34ecb70b194cb87fe10ef7d4f` |
| 10 | `s10_p01` | `s10_p01_r01_candidate.png` | `e6429965b692c29d9411dac9c0058eae64fc9becf69cc149a197cdfadd542cd1` |
| 10 | `s10_p02` | `s10_p02_r01_candidate.png` | `11119ea9cd394a711fa09087a212424042d4535d02e8163b30ac17ca193865dd` |
| 10 | `s10_p03` | `s10_p03_r01_candidate.png` | `853b54d8a588579edbdbb92bd305bdd383418ab1583d043f0a873353d6d6105b` |
| 11 | `s11_p01` | `s11_p01_r01_candidate.png` | `4d472be441e48ca4f28743b0123e69b4f25630c67fc5ede24b74df2bfa8cf52c` |
| 11 | `s11_p02` | `s11_p02_r01_candidate.png` | `cce4f43fbe82578e24c9458d0c6716812d0c745030a6aebffdbc3085993d526b` |
| 11 | `s11_p03` | `s11_p03_r01_candidate.png` | `e1fbfb5b8f92fa861e58bb1f0dc8ce3bb795b1c77910d8b818953cae4d12f7fc` |
| 11 | `s11_p04` | `s11_p04_r01_candidate.png` | `13f362affea5a5bfa022a0591e698f616c7a37dc44f838a8c96338038b572d65` |
| 12 | `s12_p01` | `s12_p01_r01_candidate.png` | `1fc50d42f34960b140e525fd1fe2a2456caa0e6c4752b4b3a0692cfc26dd6c74` |
| 12 | `s12_p02` | `s12_p02_r01_candidate.png` | `ec9d8829e8c55fb79e8c1cc74684b04796c296e406eb7ba7b8934933b1f99f19` |
| 12 | `s12_p03` | `s12_p03_r01_candidate.png` | `18ddb529d9143e7a26951e829f86ddeeb6b5728e09a7d02766d72fa20366c3ee` |
| 12 | `s12_p04` | `s12_p04_r01_candidate.png` | `4ab8ca9034f1f108af394df1479b51dcf05a030c7dab0461b1ddebbdfab03e52` |
| 13 | `s13_p01` | `s13_p01_r01_candidate.png` | `40325649f5e2e58466113bf90ec2804014cece0258d256f6cd3088d80a2989be` |
| 13 | `s13_p02` | `s13_p02_r02_candidate.png` | `31617b01bba858d738d960f904bd9e888f19b36de2e6344203d02dfc6e2d7290` |
| 13 | `s13_p03` | `s13_p03_r02_candidate.png` | `a03ac9d5d34139f381b2c50cf3c23cbb8cbfd5dc1a1f8b26d3ce52316e85684e` |
| 13 | `s13_p04` | `s13_p04_r02_candidate.png` | `d2297bcf1330712e4c9446d13b85a9f96ed41d6393cee6c0b8e068a6e370d083` |
| 13 | `s13_p05` | `s13_p05_r02_candidate.png` | `3703b2fb43d90dcf2bb7bcc6ed971f6915a4ea80323685c7a94dfa1ccc947f24` |
| 13 | `s13_p06` | `s13_p06_r01_candidate.png` | `4d4df233dd9c140810313d986d9e7eb62b53d78e19f15f0e1072255a87f95e7d` |
| 14 | `s14_p01` | `s14_p01_r02_candidate.png` | `47f71cdc18ef74539bea0f2fcd178b203b4a3d652830579d343a15ff375198a3` |
| 14 | `s14_p02` | `s14_p02_r01_candidate.png` | `819044f9f0801830b4ef7071f575f60ca1c143f760a34705afe4ca587257517b` |
| 14 | `s14_p03` | `s14_p03_r02_candidate.png` | `2a9a948ef6b56a43896eb604700d033c7b193241ce61431896055f1b3c548ec5` |
| 14 | `s14_p04` | `s14_p04_r01_candidate.png` | **`93abc605530d0c61f777d7c11f066fe416d0794bb6484ae2baeb9fa9d1a504cc` — KNOWN REJECTED** |
| 14 | `s14_p05` | `s14_p05_r01_candidate.png` | **`4d61b32eada6e4fbec9ad9c7dad7258948280c371b21a37a52454821ffb2bf12` — KNOWN REJECTED** |
| 14 | `s14_p06` | `s14_p06_r02_candidate.png` | `f6e6b1503858a1aa4ca5475e4cbcdecc224038ba68f749a092addbefba627680` |
| 15 | `s15_p01` | `s15_p01_r01_candidate.png` | `a5478c2a083648d3c1848a295b451e6da52125a9f297d3e1b0e875d36969b89d` |
| 15 | `s15_p02` | `s15_p02_r01_candidate.png` | `7d4162e97c2c065bc682fb2a61fbc93cf1c2c13d9717c92c33e516ce53f5056f` |
| 15 | `s15_p03` | `s15_p03_r01_candidate.png` | `af7dc659d7eae1c6a6309400c84bc7a37b9288d70d2dc4a27795c15b3159ddf6` |
| 15 | `s15_p04` | `s15_p04_r01_candidate.png` | `912d1dcd7358c5da73127de1a877dc26ac5017559dc6ce3ec463563eefcd3309` |
| 15 | `s15_p05` | `s15_p05_r01_candidate.png` | `39e9563baf98a94576f4cd231e766cfde6d1657152f1219c880d6543286e0b4b` |
| 15 | `s15_p06` | `s15_p06_r01_candidate.png` | `bd5a4dfa906571fb43c44658df45094cacbb8bc583717b5e6f905044397dceb3` |
| 16 | `s16_p01` | `s16_p01_r01_candidate.png` | `9251376cd2a93aa795694b7cb69b5c1ee31118502c00aa21f6a8bb78a168ff1d` |
| 16 | `s16_p02` | `s16_p02_r01_candidate.png` | `7ba326ecc129932798c7e2a4c8a210aec22303f80baf56c7ec0b1f5576240728` |
| 16 | `s16_p03` | `s16_p03_r01_candidate.png` | `9c30604fc882081bd4b3986d33e80da80e919617d4562e029000a1b481e75fe1` |
| 16 | `s16_p04` | `s16_p04_r01_candidate.png` | `642e6b4a9408cdb123b71f46100f4e2f5b2c28f6ee446b9d37e3a98752f47903` |
| 16 | `s16_p05` | `s16_p05_r01_candidate.png` | `f9d5532f57cd4a9b5b2c6e67c71a99f8b19f7eeb028e1686ff0c008bdcd3b20d` |
| 1 | `s01x_p01` | `s01x_p01_r02_candidate.png` | `47412d1463a362f79de00134865840d2c3ff1f60355219a9f8bef9e611306207` |
| 1 | `s01x_p02` | `s01x_p02_r01_candidate.png` | `1188dfc2e42f3b90671141ae2e9e8d88c05bfa64e0a2fd0a8983fc728a87250b` |
| 1 | `s01x_p03` | `s01x_p03_r01_candidate.png` | `880c498038eac6f3546c55100aad041a32839f01050b3e0c23dc67d20b33d982` |
| 4 | `s04x_p01` | `s04x_p01_r01_candidate.png` | `e18ec1720d3b38f0063d3a74c6f12cf276a0449df1beb0c3ea6a3b2b5357f689` |
| 4 | `s04x_p02` | `s04x_p02_r02_candidate.png` | `1ea795bcf25ffda7554ac41baa81a0499cb67047b73d765dbed4ab154aa5231f` |
| 4 | `s04x_p03` | `s04x_p03_r01_candidate.png` | `8c8aaa628a1c0b77d93424acd118dfed1083639b10f26b713746156f8a10b909` |
| 5 | `s05x_p01` | `s05x_p01_r02_candidate.png` | `b93713aec61e69dcb5d0289955bb9bd87e5876393492595e654e86e04b9d8978` |
| 5 | `s05x_p02` | `s05x_p02_r02_candidate.png` | `37a3e46df80f7919a6c7f0b3273d8f7ab3d28dabf363753d4fa93b8fcf3ffb28` |
| 5 | `s05x_p03` | `s05x_p03_r02_candidate.png` | `c039b93adc92c28820b67f76a9ed518c207acbde1584cbb1ad787424fe36e208` |
| 5 | `s05x_p04` | `s05x_p04_r02_candidate.png` | `071f8690490af10ae3e9b548661f9939d126c5834c2c5e7d67ca7789fd6ece9b` |
| 12 | `s12x_p01` | `s12x_p01_r01_candidate.png` | `868047a7e60881a7f591e528b296a63d615d68810c2162357626e364893a47a3` |
| 12 | `s12x_p02` | `s12x_p02_r01_candidate.png` | `4ecb2d842f84086ae5aec81c911eb5e150b90daa20d047d0c6a97ed3c05cc6e4` |
| 12 | `s12x_p03` | `s12x_p03_r01_candidate.png` | `6c617cae10ee5892a5a18388642dfe874a992179e5122bd24547347c7d845d68` |
| 15 | `s15x_p01` | `s15x_p01_r01_candidate.png` | `4ee3dd971c93ed49970376307bfb9957e98bb01c362001f39eaaab717329340f` |
| 15 | `s15x_p02` | `s15x_p02_r01_candidate.png` | `f222cf6b50ef9350b1f36d03427e21140e72b526ee7d30bb7091f3c46a707332` |
| 15 | `s15x_p03` | `s15x_p03_r01_candidate.png` | `938b0d2a211d18dabed8976f2e8306fcd5c08040530e38f9ea4231141429c275` |
| 15 | `s15x_p04` | `s15x_p04_r01_candidate.png` | `6a38ed5315747ce86ecea6a4ce13d44f1a6310bdf272da5a7e3adfbcffb7116a` |
| 15 | `s15x_p05` | `s15x_p05_r01_candidate.png` | `4edf404c683c397ebf5cdead88d882e5f7f40928486fa9494e3d6a0afad3479d` |
| 15 | `s15x_p06` | `s15x_p06_r01_candidate.png` | `07e01587dbced777a7cc7258ab6bce0f6e1b0ddb739e357e8a576fe57535053e` |
| 16 | `s16x_p01` | `s16x_p01_r01_candidate.png` | `37e051360244961a595cceb019905bdf4afb9e73567b1ced186bccdcaac69b1c` |
| 16 | `s16x_p02` | `s16x_p02_r01_candidate.png` | `4e7c69502131151066a3a792aa6dc00bf8d3181ee18714d440cd67057eb28398` |
| 16 | `s16x_p03` | `s16x_p03_r01_candidate.png` | `43f549fd3ec6932bc04ff4285bb50927352d021a9481457b26230e65f96125f0` |

---

# 8. V6 boundary/continuity contract

The tracked boundary plan contains 16 scene entries. Three scene entries are explicit shared-boundary candidates:

| Scene | Shared from | Exact start boundary | First own target |
|---:|---:|---|---|
| 8 | 7 | `s07_p04_r01_candidate.png` | `s08_p01_r01_candidate.png` |
| 11 | 10 | `s10_p03_r01_candidate.png` | `s11_p01_r01_candidate.png` |
| 14 | 13 | `s13_p06_r01_candidate.png` | `s14_p01_r02_candidate.png` |

This is a good design: the next scene begins on the exact previous end image, then moves to its first own target.

However, the plan status is:

```text
candidate_plan_pending_visual_review_and_word_timing
```

Therefore it is not a render authorization.

### Required transition validation before runtime generation

For every internal transition and every scene join:

1. Confirm both endpoint hashes still match `keyframe_plan.json`.
2. Confirm both images have current visual-review receipts.
3. If same-view motion:
   - same plate;
   - same crop;
   - compatible actor scale;
   - compatible support contacts;
   - compatible world state.
4. If crop or plate differs:
   - cut, do not morph.
5. If scene start is shared:
   - exact previous end bytes are used for the new scene's start;
   - first-own target remains separately reviewed.
6. Add word-level timing so a cut does not split spoken words arbitrarily.
7. Runtime exporter must carry the boundary type into the shot/edit plan.

---

# 9. Cross-version isolation audit

## 9.1 Visual isolation

**PASS for tracked v5/v6 PNG byte identity:** 0 overlapping Git blob SHAs.

This does not prove visual similarity is absent, but it does prove the tracked files are not byte-for-byte copies across those two versions.

## 9.2 Audio exception

**PASS as an explicit policy exception in tracked metadata, subject to local byte verification.**

Do not “fix” the repo by rerecording audio merely because it originated in v5. The current owner decision explicitly retained those recordings.

The required invariant is:

- v6 visual identities/plates/keyframes/render outputs are v6-local;
- v6 runtime audio files are staged under the v6 namespace;
- their source provenance may be v5 only under the recorded owner-authorized exception;
- hashes must prove exact retained bytes.

## 9.3 Timing/render reuse

No current v6 render reuse is authorized. Current v6 docs say no older images, clips, or renders are reused.

---

# 10. Documentation consistency audit

## 10.1 Current authoritative docs that are mostly correct

- v6 README
- v6 SCRIPT
- v6 KEYFRAME_REVIEW
- v6 KEYFRAME_CONSISTENCY_AUDIT
- v6 VIDEO_BOUNDARIES
- root README v6 project-status row
- 2026-10-11 changelog entries

## 10.2 Docs requiring correction

Highest priority:

1. `CLAUDE.md` — v5 audio contradiction and stale “no v6 images” instruction.
2. Root README — v6 generic prompt-manifest commands and Ugly Duckling status.
3. `audio-chained-coverage/SKILL.md` — wrong current v6 pipeline assumptions and non-strict join command.
4. `consistent-image-prompts/SKILL.md` — prompt-manifest-centered authority must distinguish current v6 plan mode.
5. `docs/creation-rules.md` CR-21 — implementation language should distinguish generic audio-driven policy from the old manifest representation.
6. `docs/production-guide.md` — says current work is v4 after saying v4 was removed.
7. `docs/character-consistency.md` — historical file still points to v4 as current.
8. `docs/findings-and-risks.md` / `docs/prompting.md` — broken historical links.
9. v5 SHOT_PLAN — stale V4 title/status/link.
10. 2026-10-10 audit — needs superseded banner.

---

# 11. Dependency-ordered remediation plan

## Phase A — stop misleading operators before touching media

**Owners:** repository/docs maintainer + production maintainer.

1. Fix `CLAUDE.md` audio exception language.
2. Mark 2026-10-09 no-image instruction superseded.
3. Correct root story status for Ugly Duckling.
4. Remove v6-specific `image_prompts.py` command examples unless a v6 manifest is reintroduced.
5. Update both active skills to distinguish pipeline mode.
6. Update strict commands to include `audit --strict` / `--fail-on-flagged-joins`.
7. Mark 2026-10-10 audit historical/superseded.
8. Fix `shot.py` removed-story default/examples.
9. Repair historical links.

**Exit:** a new operator cannot be directed into a missing v6 prompt manifest or an informational-only gate.

## Phase B — repair v6 runtime architecture before GPU work

**Owners:** production Python maintainer.

1. Choose v6 runtime schema.
2. Add unambiguous story slug identity.
3. Reconcile/remove `asset_revision_policy` mismatch.
4. Build runtime adapter from current keyframe/boundary/audio plans.
5. Bind runtime endpoints to visual review receipts.
6. Bind audio to v6 namespace + tracked provenance.
7. Add fail-closed preflight.
8. Add tests.

**Exit:** current v6 tracked plans can reach a complete dry-run/preflight without missing legacy files.

## Phase C — fix render/backup infrastructure

**Owners:** LUMI/production maintainer.

1. Make render inventory receipt-aware.
2. Make work-root resolution use `FELTWILLOW_WORK`.
3. Make backup use the same root.
4. Add tests/smoke fixtures.
5. Document resolved work root.

**Exit:** stale MP4 is never silently skipped and alternate work roots are fully honored.

## Phase D — complete v6 visual approvals

**Owners:** owner/visual reviewer.

1. Replace rejected `s14_p04/p05`.
2. Review all 92 current hashes full-resolution.
3. Record all required visual evidence.
4. Run gate to 0 blockers.
5. Freeze approved review ledger.

**Exit:** 92/92 active keyframe hashes pass the gate.

## Phase E — word timing and runtime piece plan

**Owners:** audio/timing maintainer + production maintainer.

1. Verify v6-local WAV bytes against `audio_manifest.json`.
2. Produce/verify word timing receipts.
3. Build clip intervals from audio + boundary plan.
4. Check every cut/shared boundary against word timing.
5. Build runtime story inputs.

**Exit:** all 683.67 seconds are covered without ambiguous timing or unauthorized mouth movement.

## Phase F — controlled v6 pilot

**Owners:** LUMI operator + owner.

Only after A–E:

1. Export a 1–3 scene runtime plan.
2. Audit exact endpoint hashes/receipts.
3. Render limited seeds.
4. Owner selects exact takes.
5. Run:
   ```bash
   chain_preview.py ... --require-takes --fail-on-flagged-joins
   ```
6. Repair any flagged join with a hash-bound continuation workflow.
7. Re-run strict preview.

**Exit:** pilot has 0 unresolved flagged joins and explicit selected-take receipts.

## Phase G — whole-film render and edit

Only after pilot approval:

1. Bulk render with receipt-aware driver.
2. Verify all outputs/sidecars.
3. Apply lip-sync only to explicit dialogue speakers.
4. Re-run strict full-chain preview.
5. Produce hash-bound edit manifest.
6. Owner final visual/audio sign-off.
7. Publishing handoff.

---

# 12. Go / no-go matrix

| Action | Decision | Required before GO |
|---|---|---|
| Repository read-only audit | **GO** | None |
| Documentation/code/test fixes | **GO** | Preserve history; no media overwrite |
| v6 full-resolution image review | **GO** | Owner/reviewer access to actual PNGs |
| Replace known rejected v6 keyframes | **CONDITIONAL** | Explicit owner authorization for image revision |
| Approve current 92 keyframes as-is | **NO-GO** | Two are known rejected; 90 others have no current review receipts |
| v6 runtime export | **NO-GO** | FWA-002/FWA-012 resolved + FWA-001 closed |
| v6 1–3 scene GPU pilot | **NO-GO** | Runtime path works; 92 relevant endpoints approved; timing frozen |
| v6 bulk GPU render | **NO-GO** | Pilot passed; render receipt driver fixed |
| v6 edit manifest | **NO-GO** | Chosen takes + strict joins + lip-sync receipts |
| v6 publishing handoff | **NO-GO** | Final edit/review/selection receipts |
| v5 take review of existing media | **CONDITIONAL** | Local media/sidecars audited; stale receipt risks understood |
| Ugly Duckling continued Scene 11 generation | **NO-GO** | Canonical r02 decision and dependent reference rebuild |
| Boy/Hare first image generation | **CONDITIONAL** | Owner CR-01 script/shot-order approval |

---

# 13. Local completion runbook for evidence unavailable remotely

Run these on the actual `working-cloud-branch` checkout before closing this audit.

## 13.1 Capture exact checkout state

```bash
git rev-parse HEAD
git branch --show-current
git status --short
git ls-files -o --exclude-standard
git diff --check
```

Expected remote reference for this report:

```text
1c29c2e96ee53890ca72c20b5d695e9471041bd0
working-cloud-branch
```

If local HEAD differs, treat this report as a snapshot and re-run changed-file checks.

## 13.2 Run tracked unit tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

Record Python version and platform.

## 13.3 Check v6 visual gate

```bash
python3 production/keyframe_visual_gate.py --story lion_and_mouse_v6
```

At the audited snapshot, a non-zero result is expected because reviews are empty and two hashes are known rejected.

## 13.4 Check staging contract

```bash
python3 production/staging_contract.py --story lion_and_mouse_v6
```

This checks metadata/staging consistency, not image pixels.

## 13.5 Verify audio bytes locally

Write/use a read-only verifier that for every `audio_manifest.json.lines[]` entry:

1. opens the declared v6 runtime WAV;
2. hashes it;
3. compares to recorded v6 hash;
4. if source v5 file is available, hashes source and compares;
5. verifies sample rate/channels/sample width;
6. verifies duration within declared tolerance.

Do not rewrite audio during this check.

## 13.6 Verify v5 render inventory

On a machine with v5 `work/`:

- count MP4s;
- count sidecars;
- verify every sidecar's source hashes if present;
- distinguish initial 186 from later bridge takes;
- record stale/no-receipt media.

## 13.7 Verify Ugly Duckling missing references

Run the current lint command documented by that packet and save exact output/exit status. Resolve only after distinguishing:

- missing exact original references;
- intentionally ignored review evidence;
- truly stale active references.

---

# 14. Acceptance checklist for closing this audit

The repository should not be declared production-consistent until all P0/P1 items below are checked:

- [ ] `s14_p04` replacement reviewed and old rejected hash preserved.
- [ ] `s14_p05` replacement reviewed and old rejected hash preserved.
- [ ] 92/92 active v6 keyframes have current hash-bound review entries.
- [ ] v6 visual gate exits 0.
- [ ] v6 runtime plan is generated from the current keyframe/boundary model.
- [ ] v6 runtime exporter does not require nonexistent legacy inputs.
- [ ] story slug/version/policy semantics are unambiguous.
- [ ] owner-authorized v5→v6 audio provenance is represented without weakening visual isolation.
- [ ] strict join command includes `--fail-on-flagged-joins`.
- [ ] readiness handoff audit uses `--strict`.
- [ ] LUMI existing-render inventory checks sidecars/hashes.
- [ ] LUMI rendering honors `FELTWILLOW_WORK`.
- [ ] backup honors `FELTWILLOW_WORK`.
- [ ] Ugly Duckling top-level status/lint/reference state is reconciled.
- [ ] root README no longer calls Ugly Duckling merely “in preparation.”
- [ ] broken tracked relative links are fixed or explicitly historical/local-only.
- [ ] no executable default points to removed Lion/Mouse v2-v4.
- [ ] 2026-10-10 audit carries a superseded banner.
- [ ] P0/P1 regression tests exist.
- [ ] CI runs read-only test/integrity checks.

---

# 15. Suggested issue decomposition

If these are delegated, use separate tasks so fixes remain reviewable.

### Issue A — v6 current-pipeline runtime adapter
Covers FWA-002/FWA-012.

### Issue B — v6 visual approval completion
Covers FWA-001.

### Issue C — strict gate semantics
Covers FWA-003.

### Issue D — LUMI render receipt validation
Covers FWA-004.

### Issue E — configurable work root
Covers FWA-005.

### Issue F — current-state documentation reconciliation
Covers FWA-006/FWA-008/FWA-009/FWA-011.

### Issue G — Ugly Duckling reproducibility/state cleanup
Covers FWA-007.

### Issue H — regression CI
Covers FWA-010.

### Issue I — tracked production receipts for ignored media
Covers FWA-013.

### Issue J — legacy chain packet cleanup
Covers FWA-014.

---

# 16. Final readiness statement

At commit `1c29c2e96ee53890ca72c20b5d695e9471041bd0`, the repository has made major progress:

- v6 visual bytes are no longer tracked duplicates of v5;
- the v5-audio exception is documented and hash-manifested;
- v6 has a coherent 92-keyframe plan, staging contract, visual gate, and scene-boundary plan;
- several prior code defects were fixed.

But current production readiness is still blocked by **unapproved/rejected v6 endpoints and a mismatch between the current v6 planning model and the legacy runtime/export workflow described by shared authority docs**. The LUMI bulk-render/backup path also needs receipt and work-root hardening before large production work.

**Decision:** keep v6 video/export/render at **NO-GO** until FWA-001 through FWA-005 and FWA-012 are closed, then run a small hash-bound pilot before any full-film render.

