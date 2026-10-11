# Feltwillow production — repository consistency and v6 independence audit

**Audit date:** 2026-10-10 (Europe/Berlin)  
**Repository:** `jeilealr/feltwillow-production`  
**Branch:** `working-cloud-branch`  
**Inspected HEAD:** `eac8d388639e6053113b071d7f3e08f3a0cac353` — *improving image and video generation*, 2026-10-10 19:18:37 UTC  
**Primary story:** `lion_and_mouse_v6`  
**Intended repository destination:** `docs/audits/repository-consistency-2026-10-10.md`  
**Audit mode:** read-only repository inspection; only this Markdown report was created outside the checkout. **No production changes, approvals, image generation, audio creation, or GPU renders.**

> **Hard owner acceptance rule.** Lion and Mouse v6 is a genuinely independent production. It must not import, clone, carry, reference, use as a render source, or silently recreate assets or timing from Lion and Mouse v5, v4, or earlier. Relabeling a borrowed image as an `r02` v6 file does **not** make it independent. A MacBook and LUMI must resolve the same logical v6 inputs and give the same validation verdict for the same bytes and review records. Contradictory *active* instructions must be removed/replaced by one authoritative rule. Preserve older versions as separately labeled history, not as v6 inputs. Any future production change requires a separate instruction and is **not** authorized by this audit.

## 1. Snapshot, verification boundary, and immediate decision

### 1.1 What was inspected

The GitHub API returned an untruncated recursive tree of **975 entries**, including **774 tracked blobs**, for the named commit. The audit inspected the active v6 visual bible, manifest (all 167 image rows and 154 shot rows), approvals (54 entries), dialogue coverage (161 lines), saved timing plan (154 rows), current v6 README and LUMI handoff, root README/CLAUDE.md, generic creation and specialist skill instructions, relevant production source files, current repository ignore rules, and top-level manifests for the four other active stories. Exact Git object IDs, filenames and source line numbers are cited below.

**Audit execution environment:** hosted Linux / Python 3.13.5, with Pillow, NumPy, PyYAML and pytest available. The GitHub connector could read tracked UTF-8 files and tree metadata. A direct checkout was **not available** (container network could not resolve `github.com`). The connector could not deliver the multi-megabyte binary PNGs to the test container, so image pixels and ignored Mac/LUMI `work/` contents were not inspected. The remote branch tree does not expose uncommitted/ignored files or the user's current local Git dirty state.

**Platform clarification (owner-confirmed, 2026-10-10):** the **MacBook** ordinarily runs Python in the locally managed `feltwillow` **Conda** environment. **LUMI does not use that Mac Conda environment or require a new user-managed Conda environment.** Its existing production path is `lumi/run_in_container.sh` -> **Singularity** with the pinned ROCm/PyTorch `.sif` at `FELTWILLOW_SIF` -> `lumi/env.sh` -> project Python **virtual environment** at `FELTWILLOW_VENV_GEN` on LUMI scratch, created with `python -m venv --system-site-packages` by `lumi/setup_env.sh`. This venv borrows packages from the container; its exact interpreter and PyTorch import must be checked *inside* the configured container. The repository's optional `WITH_CONDA` variable refers to a shell initialization hook in the container, not to activating or installing the Mac's Conda environment on LUMI. It may be unnecessary in the configured image; verify it rather than inventing a LUMI Conda setup. **Acceptance parity** means identical validation of the same *saved input bytes*, not pixel-identical stochastic image/video generations across different hardware. See CONS-032 and §8.4–8.6.

**Evidence taxonomy:** `verified` = observed in the commit's tracked data/source or reproduced locally from a targeted algorithm; `inferred` = a plausible risk from that source requiring a real end-to-end test; `unverified` = material inputs were inaccessible. A committed name or `accepted` label is not itself proof of pixel quality. Git object identity *does* prove that the committed bytes of two files are identical; it does not establish artistic provenance for different-bytes files.

### 1.2 Executive decision

**NO-GO for approving v6 scene candidates, exporting a v6 pilot, rendering v6 video, or preparing edit handoff.** Foundation assets are not fully independent: **all 10 v6 location plates and both v6 prop PNGs are byte-identical to v5 counterparts**, despite their v6 paths and `r02` names. The approval mechanism does not bind a candidate to the prompt and reference bytes *actually used to generate it*. The saved audio timing is provisional because v6-local WAV/timing/word data were not available in the inspected tree. **No v6 scene keyframe is approved.**

**Safe activity now:** repository audit, code/doc fixes, temporary-copy unit tests, transfer manifest design and owner review of a proposed genuinely native v6 plate/prop design. Do not generate/approve more stills until the relevant fixes, reference changes and approvals are reconciled. Do not simply delete all v5 history: isolate it and remove only its active v6 dependency edges. All deletions/regenerations are delegated to a future explicitly authorized remediation phase.

### 1.3 Severity and evidence classification

| Priority | Count | Operational meaning |
|---|---:|---|
| **P0** | **6** | Independence/approval/timing/required-asset blocker; stop dependent production |
| **P1** | **16** | Likely visible drift, broken review, stale state, or machine-inconsistent handoff |
| **P2** | **10** | Missing validation/coverage, portability or active-document maintenance |
| **P3** | **2** | Repository hygiene/legacy clean-up not itself a v6 gate |
| **TOTAL** | **34** | 34 finding IDs, `CONS-001` through `CONS-034` |

Status is assigned individually. An issue can be a **verified source defect** even though no GPU job or real image was executed to demonstrate a visible failure. Source-proven violations of owner policy are blockers whether or not a script currently catches them.

### 1.4 Positive checks, not readiness claims

- The active v6 `prompt_manifest.json` has **no v5/v4/v3 path in an image target or `ordered_references.path`**; no v6 shot has an active `reuse`, and image records have no active `carried_from`. This is *path-level* isolation, not content-level independence (see CONS-001).
- Exactly 167 unique v6 image targets: 54 `accepted` foundation/expression rows, 42 `candidate` scene rows and 71 `planned` scene rows. Of the 167, **54 accepted targets are committed** and **113 scene targets are not**; no extra tracked nonaccepted target was found.
- The 154 timed v6 pieces cover 16 scenes and total **683.67 s** (11:23.67). Recomputed rounded segment end times are contiguous to 0.002 s; each segment matches its manifest shot/variant frame count and mode. Frames are 49–81 in valid increments of four and are timed at 16 fps. All 161 line IDs appear at least once, and the 37 `mouth` pieces have a matching named speaker rather than a narrator-as-speaker. These are **metadata** checks only; the actual narration has not been checked.
- The scene-to-scene chain specifies 84 image chains and 70 intentional cuts; a comparison of adjacent manifest endpoint IDs found no nominal chain-boundary mismatch. The v6 scene reference graph contains **no cycle**; it does contain 8 backward-in-film-order dependencies that block the promised simple forward generation order (CONS-007).
- No case-insensitive tracked filename collisions were found. The 54 approved v6 target paths appear in the tracked tree; **file-content SHA-256 and visual checks were not independently recalculated** because binary bytes were inaccessible.

## 2. Source-of-truth and policy-authority map

| Fact / gate | Primary authority for v6 | Consumer/enforcer | Conflicts or missing enforcement |
|---|---|---|---|
| **Version isolation** | Owner decision + v6 `README.md:3-5`, `LUMI_HANDOFF.md:5` | `production/image_prompts.py:353-370` | Only scans paths/metadata; missed byte-identical v5 plates/props (CONS-001). Generic instructions and CLI still allow cross-story audio/inheritance |
| Character anatomy/identity/palette | `stories/lion_and_mouse_v6/visual_bible.json` + independently approved v6 canonicals | `image_prompts.py` templates, explicit review | 102 scene acceptance criteria still say “V4 identity roots” (CONS-017); actual appearance unverified |
| Plate, crop, camera, landmarks, lighting | v6 bible `locations`, `setups`, v6 approved PNG and hash | `image_handoff.py`, reviewer | All 10 v6 plate PNGs equal v5 blobs; approval booleans do not prove pixel matching |
| Props and net world-state | v6 bible `prop_states`, `net_rules` + native prop PNGs | prompt templates, human shot continuity review | Both v6 props equal v5 PNGs; current version independence violated |
| Setup scale | v6 bible `cast_scale`, `setups.<id>.numeric_size_targets`, approved setup anchor | `image_handoff.py:119-161`, visual owner review | 11 anchors unapproved; numeric values are self-reported, not measured automatically |
| Image target, order, references and prompts | v6 `prompt_manifest.json` and v6 bible | `image_prompts.py` build/lint/show, `image_handoff.py` | 42 generation prompts and 35 recorded reference sets do not match present records |
| Candidate generation provenance | Each image `result.submitted_positive`, `result.ordered_references` + hashes, source/candidate hashes | **Should be** approval preflight | `approve` does not verify generated-vs-current provenance (CONS-004) |
| Human image approvals | v6 `image_approvals.json`, owner review | `image_prompts.py approve`; `export_runtime.py:154-179` | Approval stamps current spec even if the candidate was generated under an obsolete one |
| Story dialogue and speakers | v6 `SCRIPT.md`, `dialogue_coverage.json` | `chain_plan.py`, `lip_sync.py` | Line WAV and final word timings missing; docs point to v5 recording |
| **Audio bytes and line/scene timing** | `work/stories/lion_and_mouse_v6/audio/en/` + verified WAV/timing.json | `chain_plan.py`, `lip_sync.py` | Audio is not in tracked snapshot; 683.67s plan is provisional (CONS-005) |
| Film order, shot endpoints and retime | v6 manifest + `timing_plan.json`, both validated against final v6 audio | `chain_plan.py`, `export_runtime.py`, `chain_preview.py` | 8 backward generation references; preview/review defects |
| Runtime render inputs | Approved v6 image hashes + v6 manifest shot variants | `export_runtime.py`, `shot.py` | `--images`/`--story` not tightly scoped to same independent version (CONS-015) |
| Selected video take | explicit story-local `takes.yaml` + render receipt/sidecar | `chain_preview.py`, `edit_manifest.py` | No selected v6 takes; strict preview does not error on visibly flagged joins |
| Lip-sync output | finalized v6 audio/words, specific v6 approved mouth references, selected v6 take hash | `lip_sync.py`, `feltwillow/lipsync.py` | Absolute paths and mtimes contaminate cache identity (CONS-014) |
| Edit handoff | `edit_manifest.py` + verified selected source and v6 narration | `production/edit_manifest.py` | Absolute paths not portable; no finished v6 media |
| Machine-independent audit | **Proposed:** canonical JSON/bytes digests, relative logical paths, pinned decoder/tool versions, owner-reviewed image measurements | **No full implementation today** | Mac and LUMI parity not tested; add mandatory golden fixtures and side-by-side outputs |

**Policy precedence proposal:** (1) explicit latest owner decision; (2) story-local versioned `README.md`, `LUMI_HANDOFF.md` and owner-approved asset records; (3) immutable v6 bible/manifest/approval hashes; (4) generic creation rules and reusable skills *only when consistent*; (5) historical dated logs. Once fixed, replace competing active prose with links to the single fact. Do not let older README/CLAUDE snapshots override current v6 records.

## 3. Repository-wide inventory and stage definitions

A **planned image** has a manifest target but no current authorized delivery image; a **candidate** has a recorded output awaiting genuine owner review; an **accepted image** is labeled approved but must still pass current path, exact bytes, generation-spec and reference-provenance checks; **committed target** means Git records a blob at the named path, not that it is artistically approved. A **planned shot** is not a rendered take. `work/` and `.review/` are ignored: the HEAD cannot prove the number of files presently on the Mac or LUMI.

| Story | Manifest images (status) | Tracked manifest target PNGs | Manifest shots | Claimed/known stage; inaccessible data |
|---|---|---:|---:|---|
| **Lion and Mouse v6** | **167**: accepted 54 / candidate 42 / planned 71 | **54/167** | **154** | v6 native *intended*; all 113 scene frames pending, 11 missing sharp anchors, no v6 audio in snapshot, all new renders planned; no selected takes |
| Lion and Mouse v5 | **140**: accepted 140 | **137/140** | **44** | root docs say 186 rendered clips and owner selecting takes (v5 production history); generated clips, recipes and owner picks were not inspectable; v5 separate from v6 |
| Ugly Duckling v1 | **156**: accepted 152 / planned 3 / superseded 1 | **152/156** | **44** | Many assets saved but owner review unresolved per `CLAUDE.md:85-86`; do not equate manifest `accepted` with owner approval |
| Tortoise and Hare v1 | **141**: planned 141 | **0/141** | **42** | Script/shot planning; await approval |
| Boy Who Cried Wolf v1 | **171**: planned 171 | **0/171** | **46** | Script/shot planning; await approval |

**Caveat on v5 shot counts:** `CLAUDE.md:162-170` describes 62 runtime render shots × three seeds = 186 clips, but the present v5 *planning* manifest has 44 shot records. These represent different artifacts/stages and must never be merged into a single v5 count without comparing exported runtime YAML and render sidecars. Similarly, v1 `accepted` labels are not proof the owner approved those visuals.

### 3.1 v6 image inventory by production group

| Group | Count | Current meaning |
|---|---:|---|
| Canonical/pose/reference foundation | 20 | committed, accepted-label; inspect real pixels and provenance |
| Expression studies | 22 | committed, accepted-label; inspect against current canonicals |
| Location plates | 10 | committed, accepted-label; **10 byte-identical to v5** |
| Props | 2 | committed, accepted-label; **2 byte-identical to v5** |
| Scene keyframes / calibration images | 113 | **42 candidate**, **71 planned**, **0 accepted** |
| **Total** | **167** | Exactly 54 accepted + 42 candidate + 71 planned |

### 3.2 v6 scene-frame inventory (all statuses, from current manifest)

| Scene | Candidate / planned | Candidate record IDs (not approved) |
|---|---|---|
| 01 | 0 / 6 | — |
| 02 | 0 / 5 | — |
| 03 | 3 / 4 | `s03_decides_start`, `s03_decides_end`, `s03_decides_open` |
| 04 | 0 / 2 | — |
| 05 | 1 / 8 | `s05_leo_asleep_cu` |
| 06 | 0 / 3 | — |
| 07 | 7 / 0 | `s07_leo_annoyed_start`, `s07_leo_annoyed_end`, `s07_milo_sorry_start`, `s07_milo_sorry_end`, `s07_leo_annoyed_open`, `s07_milo_sorry_open`, `s07_milo_apology_open` |
| 08 | 7 / 2 | `s08_leo_softens_start`, `s08_leo_softens_end`, `s08_milo_surprised_start`, `s08_milo_surprised_end`, `s08_leo_softens_open`, `s08_milo_surprised_open`, `s08_milo_grateful_open` |
| 09 | 0 / 7 | — |
| 10 | 0 / 5 | — |
| 11 | 5 / 4 | `s11_why_wont_it_break_start`, `s11_why_wont_it_break_end`, `s11_call_start`, `s11_call_end`, `s11_leo_worried_open` |
| 12 | 0 / 3 | — |
| 13 | 6 / 5 | `s13_leo_doubtful_start`, `s13_leo_doubtful_end`, `s13_leo_warns_open`, `s13_milo_cu`, `s13_milo_cu_open`, `s13_leo_doubtful_open` |
| 14 | 0 / 12 | — |
| 15 | 13 / 2 | `s15_leo_amazed_start`, `s15_leo_amazed_end`, `s15_milo_modest_start`, `s15_milo_modest_end`, `s15_leo_reflects_start`, `s15_leo_reflects_end`, `s15_milo_sincere_start`, `s15_milo_sincere_end`, `s15_leo_amazed_open`, `s15_milo_modest_open`, `s15_leo_grateful_open`, `s15_milo_sincere_open`, `s15_leo_smiles` |
| 16 | 0 / 3 | — |
| **TOTAL** | **42 / 71** | All 42 are unapproved; `.review/` bytes were inaccessible here |

### 3.3 Video and narration inventory

- **16 scenes**, **154 one-variant shot/pieces**, **154 timing segments** and **161 script/dialogue lines**, all IDs consistent at the metadata level. Piece counts by scene: `01:8, 02:5, 03:10, 04:3, 05:9, 06:8, 07:5, 08:19, 09:5, 10:5, 11:8, 12:7, 13:13, 14:12, 15:24, 16:13`.
- Saved shot modes include **37 mouth-mode** pieces. Their matching speaker metadata excludes narrator-driven visible mouths. **31 narration line IDs feed more than one piece**, by deliberate distribution in `chain_plan.py:179-205`; exact split positions remain provisional until v6 WAVs and word timings are verified.
- Timing-plan frame counts: `49×14`, `53×13`, `57×18`, `61×12`, `65×12`, `69×7`, `73×20`, `77×8`, `81×50`. Saved speed range **0.804–1.230**, subject to final audio verification.
- All 161 `dialogue_coverage.json` rows have `audio_path=null`, `measured_duration_seconds=null` and no `chosen_shot_intervals`. This is an explicit pending state, not a silent coverage failure.
- `stories/lion_and_mouse_v6/story.yaml` and `stories/lion_and_mouse_v6/takes.yaml` are **not tracked at HEAD**, consistent with no approved scene frames or selected v6 renders. Do not infer that LUMI's ignored `work/` is empty; obtain a remote inventory.

## 4. Thirty-four findings, ordered by priority

The reproduction identifiers and commands below are sufficient for a new agent to locate each defect without guessing. Paths are relative to repository root. “Fix” describes a future **authorized** change only. Where code writes, run it on a disposable checkout/temporary fixture during remediation tests.

### P0 — immediate production blockers

#### CONS-001 — Twelve v6 approved assets are byte-identical to v5 assets

- **Priority/status:** **P0 / verified**. **Stage:** v6 foundation identity, plates, props, every scene dependent on them.
- **Evidence:** Git tree at HEAD contains 12 pairs with exactly the same Git **blob SHA**, although one filename contains `lion_and_mouse_v5/..._r01.png` and the other `lion_and_mouse_v6/..._r02.png`. All 10 v6 location plates and both v6 props are among them. See the full 12-row identity ledger in §6. These 12 appear as accepted v6 foundation records (`PL_*`, `PROP_ACORN`, `PROP_NET`) in the v6 manifest and approvals.
- **Expected vs actual:** v6 uses independently created, v6-approved images, no earlier-version asset copy. Instead these are literal copies with new folder/revision names. Path-only isolation was insufficient.
- **Impact:** every current v6 scene using those plates/props inherits v5 appearance and world geometry; 12 foundation approvals do not satisfy the explicit independence requirement. An eventual plate replacement invalidates dependent references and visuals. Current v6 scene candidates are already affected.
- **Fix:** classify these 12 approvals as **not admissible for an independent v6 production**; create new v6-native plates (preserving internal v6 geometry consistently, not visually lifting v5 pixels) and both props in an authorized generation phase, review each with the owner, make fresh independent versioned image IDs/hashes and invalidate all transitive dependents. Retain v5 files solely within v5 history. Do not solve by renaming, copying, re-encoding, recoloring or stamping a new `rNN` over old bytes.
- **Regression:** compare binary SHA-256 for every committed active v6 PNG against *all* prior Lion and Mouse version PNGs; refuse any equality. Also run a human similarity/provenance check because different bytes can still represent derivative imagery. Record zero equality conflicts and signed owner approval for every new v6 foundation asset before releasing images.

#### CONS-002 — Every one of 42 v6 scene candidates has an obsolete submitted prompt

- **Priority/status:** **P0 / verified**. **Stage:** image generation provenance.
- **Evidence:** for **42/42** `status=candidate` rows in `stories/lion_and_mouse_v6/prompt_manifest.json`, `result.submitted_positive` is not byte-for-byte equal to current `positive_prompt`. The generation records also contain `submitted_prompt_sha256`, source/candidate files and hashes. **35/42** submitted `result.ordered_references` differ from the manifest's current `ordered_references` in ordered ID, role or path. Example `s08_leo_softens_open` still describes an older edit-base filename in `result.submitted_positive` while current refs target new chronological names.
- **Expected vs actual:** every candidate either has a frozen immutable specification actually used to generate it (and is reviewed against that), or is explicitly stale relative to changed requirements. Present state risks treating old results as current.
- **Impact:** false confidence in plate, crop, anatomy, mouth shape and dependency identity; candidate appearance cannot be certified against the new recipe by a green current-manifest lint.
- **Fix:** mark all 42 candidates `STALE_SPEC_REVIEW_REQUIRED`. Never simply overwrite `submitted_positive` or recorded references with current spec, never silently promote stale images; have the owner either reject/regenerate under the current full specification or explicitly accept a documented deviation if it does not violate independence (but **v5 copied plates may not be accepted for v6**). For scene endpoint/pair generation, favor regenerating after new native plates/props and approved anchors exist.
- **Regression:** approval must reject a candidate if its immutable submitted prompt hash differs from the currently required generated prompt unless a separately hashed, owner-signed deviation is registered and independently authorized. Test both old prompt and ref-order drift.

#### CONS-003 — Thirty-five candidate generation records reference `.review` candidates

- **Priority/status:** **P0 / verified (metadata); original bytes unverified**. **Stage:** image dependency lineage.
- **Evidence:** **35/42** candidate `result.ordered_references` include at least one path under `character/characters/lion_and_mouse_v6/interactions/keyframes/.review/`. Example `s03_decides_start` cites `s03_two_paths_end` at `.review/s03_01_two_paths_end_r02_candidate.png`, generation-ref hash `93408d4d671c66fb541e9ed1d2afaea30c337af92c9aeb815acc9de583aa8dc9`, while the current manifest expects the approved-keyframe location `keyframes/s03_03_two_paths_end_r02.png`. Its result-candidate SHA-256 is `04badcfd0cf58f84529fa370daf6a767c84254bac22b04dd633153aa64c82cdd`.
- **Expected vs actual:** only owner-reviewed, hash-approved target images can enter another generation as edit base, framing, camera/state or scale references (`LUMI_HANDOFF.md:34-36`). Current records document nonapproved, ignored review references at generation time.
- **Impact:** unverified shape and framing errors cascade into later portraits/calibration faces even if downstream images seem attractive.
- **Fix:** quarantine the 35 records and all affected descendants; identify the source candidate, its actual approval state, and any visual defect. For future generations require that each reference has **the exact approved target path plus hash** before invoking ImageGen. Do not allow `/.review/` in an active generation reference list, including hidden “framing” and “world_state” roles.
- **Regression:** test a reference whose ID is approved but whose submitted path is a `.review` copy; **must reject even if the PNG is byte-identical** (wrong evidence chain). Test ref array reordering and ref hash changes.

#### CONS-004 — The image approval gate can stamp a current recipe onto an old-generation candidate

- **Priority/status:** **P0 / verified source path; end-to-end exploit needs disposable fixture test**. **Stage:** image approval and export.
- **Evidence:** `production/image_handoff.py:133-161` (`scene_errors(for_approval=True)`) verifies file presence, candidate-to-target SHA equality, manual `review_checks`, numeric declarations and currently approved parents. It does **not** compare `result.submitted_positive` / `submitted_prompt_sha256` / actual ordered generation refs/hashes to the current record. `production/image_prompts.py:842-872` calls this check but then records **`spec_sha256(rec)` from the current mutable manifest** into the new approval. `production/image_approval.py:8-19` hashes this current record, not the actual submitted recipe. `export_runtime.py:154-179` validates that newly stamped approval and therefore inherits the gap.
- **Expected vs actual:** no image can be promoted unless the actual generation recipe and reference bytes conform to the approved, version-local recipe.
- **Impact:** origin laundering: old-prompt images may become fully hash-approved v6 render inputs without ever having been generated with the current instructions.
- **Fix:** define immutable `generation_receipt_v2` (schema; story slug; model/provider and reported version; requested size; exact submitted positive/negative; digest of canonicalized prompt; ordered reference IDs, roles, exact approved relative path and SHA-256; source SHA; normalized output SHA; timestamp; tool version; owner identity where available). Validate receipt **before copying** candidate or stamping approval. Reject missing receipts by default for new productions. Keep historical unknown fields `unknown`, never fabricate.
- **Regression:** construct a disposable candidate matching its target SHA and true review booleans, but change only `submitted_positive`: `--for-approval` and `approve` must fail. Repeat with ref order, ref hash, and malicious `.review` path. Verify the exported runtime refuses approvals lacking the provenance-bound receipt.

#### CONS-005 — V6-local narration/timing/word evidence is not available in the snapshot

- **Priority/status:** **P0 / verified snapshot limitation; LUMI contents unverified**. **Stage:** audio, shot timing, mouth alignment, video/render.
- **Evidence:** `stories/lion_and_mouse_v6/README.md:3-5`, `LUMI_HANDOFF.md:5,52-54` explicitly say the v6 line/scene WAVs, `timing.json` and word files must be staged separately. `timing_plan.json` records `audio_story="lion_and_mouse_v6"`, `seconds=683.67`, `audio_verification` pending. `dialogue_coverage.json` has 161 empty `audio_path`/measured duration fields. The Git tree does not include these ignored files.
- **Expected vs actual:** every v6 timed segment must derive from final **v6-owned** line audio and its own forced-alignment receipt, not v5 WAVs/word timing or an earlier version's seconds.
- **Impact:** generated clip durations, mouth cues, edit offsets and whole-film coverage may not match the eventual narration. A v5 audio fallback would violate explicit policy, even if its transcript/duration matches.
- **Fix:** stage genuinely v6-owned recordings (`work/stories/lion_and_mouse_v6/audio/en/`), decide the exact final transcript/speaker mapping, hash line and scene WAVs, regenerate `timing.json` and `word_timings.json` under v6, run timing validation and reconcile the plan before rendering. Do not copy or symlink v5 recordings. Investigate LUMI-local files before calling them absent.
- **Regression:** deliberately supply `--audio-story lion_and_mouse_v5` to all v6 timing/align/export entry points; **must hard-fail** independent of whether the path exists. Verify line WAV SHA provenance, sample rate, duration, alignment status, no narrator lips, and final total to frame-accurate tolerance.

#### CONS-006 — No v6 scene keyframes or sharp setup anchors are approved

- **Priority/status:** **P0 / verified**. **Stage:** still approval, pilot and GPU runtime.
- **Evidence:** 113 v6 scene records = 42 candidates + 71 planned; zero accepted; zero scene target PNGs tracked. All **11** sharp setup anchor records are planned and unapproved (complete list §7). `image_handoff.py:119-132` requires appropriate approved anchors before dependent sharp scene generations; `export_runtime.py:154-179` requires current approvals before exporting scene endpoint keyframes.
- **Expected vs actual:** all start/end/mouth endpoints for the chosen pilot are approved, from native version-local roots and valid setup anchors, before video export. They are not.
- **Impact:** the pilot cannot satisfy the promised physical scale/continuity contract. A clean lint would not change this.
- **Fix:** complete upstream v6 plate/prop independence first; approve new native setup anchors with measured size and ground/contact review; then build dependent frames in acyclic dependency order, get owner approval for exact bytes, and only then export individual pilot scenes. Never auto-accept a `.review` file or skip to a render.
- **Regression:** `image_handoff.py ... check <dependent-id>` must fail until the matching owner-approved anchor and parent hashes are available. Pilot export must fail when even one endpoint lacks receipt+approval; `--scenes` may narrow scope, not weaken per-scene gate.

### P1 — visible consistency, handoff, and validation failures

#### CONS-007 — Eight scene-image references point backward from later film frames

- **Priority/status:** **P1 / verified**. **Stage:** generation scheduling and story causality.
- **Evidence:** the current v6 manifest has a directed acyclic graph, but eight edges from an image first used early in the film to one first used later. The full ID→future-ID table is in §7. Examples: `s11_why_wont_it_break_start` depends on `s15_leo_reflects_end`, and `s09_leo_rests` uses `s16_friends_start` as a `size_anchor`. `LUMI_HANDOFF.md:24` says generate in dependency order, while general instructions also say scene images in film order.
- **Expected vs actual:** references are created and approved before the image that uses them, and world-state cannot leak future story events into prior states.
- **Impact:** a forward-only generation agent will be blocked or tempted to use a future placeholder/candidate; use of future world-state images can spoil rope damage/contact chronology.
- **Fix:** resolve each edge by using an approved earlier v6-local reference or generating an independent setup baseline first. For unavoidable future **framing** references, explicitly plan and approve them before film-order passes; never use future *prop-world-state* as current state. Use an explicit topological task order rather than alphabetical or film order when dependencies require it.
- **Regression:** check graph acyclicity, reference approval, first-use ordering and role-specific causal validity. Acyclic alone is not sufficient; fail on earlier world-state referencing future state.

#### CONS-008 — `image_handoff.py audit` reports failures but returns success

- **Priority/status:** **P1 / verified**. **Stage:** CI and gate automation.
- **Evidence:** `production/image_handoff.py:175-196` calculates and prints accepted-asset approval problems, unapproved sharp anchors and scene cycles, then returns normally regardless of counts. Command exit is 0 unless an unrelated exception occurs. No strict exit status distinguishes violations from a clean audit.
- **Expected vs actual:** any programmatic release gate must return nonzero for conditions disallowing the requested next action. A status-printing audit is useful, but must not be interpreted as an enforceable pass.
- **Impact:** shell `&&`, CI and agents could move forward after printing “setup anchors awaiting approval: 11”.
- **Fix:** add explicit `--strict` / `--stage={planning,generate,approve,render}` with documented exit codes and JSON report; strict approve/render should fail on missing approvals, stale receipts, dependency cycles, unsafe cross-version inputs and missing required anchors. Keep an informational inventory mode with clearly labeled advisory output.
- **Regression:** isolated fixtures with one missing approved file, stale ref and one graph cycle each cause nonzero strict audit; clean fixture exits zero. Never infer approval from descriptive counts.

#### CONS-009 — All 54 foundation approvals were rebound after the spec changed

- **Priority/status:** **P1 / verified record, **risk inferred**. **Stage:** review provenance.
- **Evidence:** all **54** current entries in v6 `image_approvals.json` include `previous_spec_sha256`, `spec_reconciled_at` (2026-10-10) and a note explaining they were rebound to changed prompt/bible specifications after an earlier 2026-10-09 owner approval, without new output bytes. Some are the 12 v5-byte-identical foundation files (CONS-001).
- **Expected vs actual:** historical owner approval remains an honest record of exactly what was reviewed. A changed current spec should trigger semantic diff/risk classification; material changes require a fresh owner review, not a mechanically updated receipt.
- **Impact:** an approval can appear current even after identity, color, camera, negative requirements or plate authority changed.
- **Fix:** make approvals append-only; preserve old spec hash and owner review; record an explicit review of **every changed spec field** with material/nonmaterial classification, reviewer and decision. Revoke the 12 copied-asset production approvals for v6. Do not invalidate the other 42 solely because of the word “reconciled”; first inspect changes and their underlying images.
- **Regression:** change a canonical identity rule, plate hash or generation prompt and verify approvals become stale; only nonmaterial metadata changes with recorded approval can retain validity.

#### CONS-010 — Join-review image conversion is incompatible with float32 RGB arrays

- **Priority/status:** **P1 / verified isolated reproduction of the exact array operation**. **Stage:** rendered-video review.
- **Evidence:** `production/chain_preview.py:236-244` creates frames as `np.float32` RGB arrays. It stores them as `j['last']`/`j['first']` at line 269. `join_sheet()` lines 327-330 passes those H×W×3 float arrays to `PIL.Image.fromarray()` without conversion. A local NumPy/Pillow repro raised `TypeError: Cannot handle this data type: (1, 1, 3), <f4`. The actual repository function was not invoked (no checkout/takes).
- **Expected vs actual:** a join contact sheet must be generated from exact rendered comparison frames, correctly cast to 8-bit RGB.
- **Impact:** strict pilot review can fail while building the sheet, or lack a dependable visual difference record.
- **Fix:** `np.clip(frame, 0, 255).astype(np.uint8)` for every thumbnail **after** choosing the correct source frames; pin/check sizes and type; unit-test `join_sheet` with float32 input without actual clips.
- **Regression:** test three synthetic RGB float arrays, ensure JPG/PNG contact sheet saves; compare color and pixel values with an 8-bit baseline on Mac and LUMI.

#### CONS-011 — Join sheet shows the current clip's last frame as its “before” image

- **Priority/status:** **P1 / verified**. **Stage:** boundary continuity review.
- **Evidence:** `production/chain_preview.py:259-269` correctly computes numeric `jump` from `prev['grey_tail'][-1]` to the current first frame, but stores `last=out_frames[-1]` **from the current piece**. `join_sheet()` at lines320-337 labels it as “last frame before” and computes its visual difference against the current piece's first frame.
- **Expected vs actual:** `before = prev['last_out']`, `after = out_frames[0]`. Visual and numeric checks must use the same actual pair.
- **Impact:** reviewers may diagnose a false jump or miss a real mismatch; a visually reassuring sheet need not correspond to the numeric flag.
- **Fix:** bind both numeric and contact-sheet frames to one common typed `Boundary` object. Include previous/current piece IDs, exact source take SHA, retiming/frame indices and an exported pixel checksum.
- **Regression:** synthetic previous clip all red/current clip all blue; sheet must show **red then blue**, never current-last/current-first. Assert numeric and sheet use identical pair hashes.

#### CONS-012 — A flagged join is a warning, not a strict exit failure

- **Priority/status:** **P1 / verified**. **Stage:** render pilot QA.
- **Evidence:** `production/chain_preview.py:199-210` `--require-takes` ensures chosen clips exist and frame counts match, then `:259-269` flags unusually discontinuous joins, but `:306-309` only prints `FLAGGED`; no rejection based on flagged joins.
- **Expected vs actual:** “strict join test” must fail if it finds a disallowed join, or require explicit owner-signed exception for an intended cut/camera transition.
- **Impact:** a script can exit successfully after computing visible discontinuities, enabling unreliable bulk renders or edit export.
- **Fix:** add `--fail-on-flagged-joins` (on by default for strict pilot) and an owner-approved exceptions ledger keyed by previous/current piece hashes, planned transition and reason. Keep heuristics informational when intentionally requested.
- **Regression:** construct two selected fixture takes with an obvious jump: strict fails; legitimate planned cut is exempt only if manifest and review match; repaired join passes.

#### CONS-013 — `export_runtime.py` can be called with cross-story manifest/story/image-set arguments

- **Priority/status:** **P1 / inferred bypass risk from verified CLI logic**. **Stage:** render source identity.
- **Evidence:** `production/export_runtime.py:108-125` independently accepts `--manifest`, `--images` and `--story`. `--images` maps another image set, and independence is determined from `stories/<args.story>/visual_bible.json` rather than checked against all three identities. Scene approvals later restrict many endpoints (`:154-179`), but the CLI does not fail immediately when passed `--story lion_and_mouse_v6 --images lion_and_mouse_v5` or mismatched manifest slug; plate/foundation selections and error semantics require an integration test.
- **Expected vs actual:** an independent v6 export rejects any foreign image set, base story, repairs/story mismatch, or source override even if paths happen to resolve.
- **Impact:** operator error or generic scripts can choose unintended bytes or confusing metadata.
- **Fix:** enforce schema `manifest.version/story == requested --story == visual_bible.version == audio_story`; disable `--images` override and cross-version repair sources for `v6_native_assets`, validate every image ID and frozen source relative to v6-approved hash. Resolve roots before filesystem writes.
- **Regression:** negative CLI tests for each mismatched combination; no writes and a distinct `VERSION_ISOLATION_FAILURE` exit.

#### CONS-014 — Lip-sync fingerprint and selected-take validation are machine-path dependent

- **Priority/status:** **P1 / verified source behavior**. **Stage:** MacBook ↔ LUMI parity, cache/handoff.
- **Evidence:** `feltwillow/lipsync.py:41-52` adds **`str(path.resolve())`** to the recipe hash for each file, before hashing contents. `:64-73` also requires exact absolute source filename, size and nanosecond mtime (and likewise output mtime), even though `:74-85` subsequently checks SHA-256. `production/lip_sync.py:364-370` stores those absolute paths and mtimes in the index.
- **Expected vs actual:** identical v6 files and metadata should have identical logical recipe identity and pass the same validation on Mac and LUMI, irrespective of root path, file copy times or host name.
- **Impact:** a copy to LUMI invalidates a valid lip-sync cache even with identical media bytes; moving the repo can change required cache keys and edit acceptance.
- **Fix:** hash a stable ordered mapping of **role + normalized repo/work-relative logical path + SHA-256**, tool/schema versions, algorithm parameters, actual audio/word/clip hashes. Treat mtimes only as an optional local optimization, never as the verdict. Store relative locators and require path containment and checksum validation after transfer.
- **Regression:** build identical fixture trees under `/tmp/mac-clone` and `/tmp/lumi-clone`, change mtimes, assert equal recipe hashes and accepted synced-take verification. Change one byte, assert rejection; forbid `..`/symlink escape.

#### CONS-015 — Inheritance builder's v6 guard depends on the existing bible policy field

- **Priority/status:** **P1 / inferred misuse path from verified code**. **Stage:** accidental v5 → v6 recreation.
- **Evidence:** `production/chain_packet.py:79-116` can localize/copy v5 assets into v6 paths; `main():273-283` refuses to overwrite v6 only when an existing bible advertises `asset_revision_policy == 'v6_native_assets'`. `README` warns not to run it, but alternative setup, removed bible or copied stale source files could bypass the policy check.
- **Expected vs actual:** the **v6 slug itself** must be reserved as an independent story under all configurations; there must be no runtime path that silently recreates it as an inherited packet.
- **Impact:** an agent following the obsolete generic skill may reintroduce exactly the 12-copy problem or overwrite a clean manifest after accidental reset.
- **Fix:** explicit hard-deny list/version registry for `lion_and_mouse_v6` (and other immutable independent projects) in the builder before any copy/write; move reusable inheritance features behind an explicit new-story mode, and add a feature test for missing and malformed bible cases.
- **Regression:** in disposable checkout, invoke builder pointing to v6 with bible present, missing, wrong policy or old chain source; every path must fail before creating files.

#### CONS-016 — Image scale/contact approval uses declared values instead of independent pixel measurements

- **Priority/status:** **P1 / verified validation scope; visual failure unverified**. **Stage:** physical size and ground-plane review.
- **Evidence:** `production/image_handoff.py:143-161` accepts `result.review_checks.measured_size` numeric values and `ground_contact.surface,x,y` written by the reviewer; compares submitted numbers with setup targets, but does not derive a bounding box, contact landmark or support mask from the delivered PNG. The comments at `:8-10` acknowledge that it cannot judge visual anatomy or whether support actually exists.
- **Expected vs actual:** identical image bytes and annotations on Mac and LUMI yield an identical mechanical result; actual visual support, identity and size must be independently reviewed. No boolean `identity_match:true` by itself proves an image matches the canonical.
- **Impact:** an agent may paste the target numbers and `true` flags for an image with wrong head size, three paws or feet in water.
- **Fix:** make reviewer record pixel bounding boxes, relative distances, baseline/support point, plate landmark anchors, depth plane, screenshot and image SHA; independently recompute frame fractions from those boxes in deterministic code. Human reviewer must verify the boxes actually enclose visible anatomy and support. Capture a second reviewer for critical two-character/net scenes.
- **Regression:** seeded fixtures with fabricated `measured_size`, wrong anatomy or impossible ground support must be rejected after independent review; same saved annotation and bytes must produce the same computed fractions on Mac/LUMI.

#### CONS-017 — Live v6 acceptance rules still demand “V4 identity roots”

- **Priority/status:** **P1 / verified**. **Stage:** prompt acceptance, identity review.
- **Evidence:** **102** active v6 image records' `acceptance` arrays contain the literal rule `V4 identity roots; smooth-crown slim Milo and brown eyes where visible`. Example `s03_two_paths_start`. The same v6 manifest/bible targets v6-approved r02 identities. `docs/creation-rules.md:284` also says “Use v4 paths and revision IDs” without a historical warning.
- **Expected vs actual:** agents must compare against **this story's current owner-approved v6 canonicals**, never earlier identity roots.
- **Impact:** automatic/agent evaluations could enforce an obsolete cast specification or reintroduce design drift from old generations.
- **Fix:** replace the repeated active v6 criteria with a **single generated reference to bible-approved v6 canonical IDs/hashes** (or revised tests) and retain old V4 criteria only in a clearly marked historical section. Review after changing a hash-sensitive specification; do not indiscriminately rebind 54 approvals.
- **Regression:** exact-string/AST scan of every active v6 manifest acceptance, review script and template: no V4/v5 identity or version root claims; lint enforces correct current canonical references.

#### CONS-018 — Top-level “current state” docs contradict v6 authority

- **Priority/status:** **P1 / verified**. **Stage:** agent operating instructions and production safety.
- **Evidence:** `README.md:14-20` calls v5 current and describes v6 as preparation. `CLAUDE.md:51-61` describes an old plan with **25 reused v5 renders**, 33 new images, v5 narration and a carried image; `:81-84` acknowledges later full-regeneration intent. Current `stories/lion_and_mouse_v6/README.md:3-12` and `LUMI_HANDOFF.md:5-7` explicitly require 154 **new** v6 renders, version-local audio, 54 approved foundations and 113 not-yet-approved scenes. `LUMI_HANDOFF.md:11` says code/assets are uncommitted local changes, although the audited HEAD includes them.
- **Expected vs actual:** one concise current operating state with dated historical notes clearly labeled, not two competing current workflows.
- **Impact:** a delegated agent may follow an obsolete dependency graph or assume a needed asset is available after `git pull`.
- **Fix:** replace root “current v5/v6” section with a short dated project status table and links to each story's local README; move the prior v5 carryover plan to `docs/history/` or a collapsed “superseded” section with a prominent **not operative for v6** warning. Correct `LUMI_HANDOFF.md:11` to distinguish committed tracked PNGs from ignored candidates/audio.
- **Regression:** grep active docs for `25 pieces reuse`, `audio-story lion_and_mouse_v5` when attached to v6, `v6 carryover`, “v6 current images in uncommitted change”; no conflicting active statements remain.

#### CONS-019 — Reviewed take provenance and visual acceptance are not guaranteed by frame-count checks

- **Priority/status:** **P1 / inferred operational risk based on verified code**. **Stage:** selected takes, joins and edit.
- **Evidence:** `production/chain_preview.py:86-120` can choose a file via arbitrary `takes.yaml` path, seed name or `best_` prefix. `--require-takes` checks existence and decoded frame count (`:199-210`), not whether every selected take's render sidecar binds exact current approved endpoints, manifest variant, seed, model/fast settings, and source clip SHA. `production/shot.py:49-60` does validate existing render inputs **when rendering/reusing** a clip, but selection and preview should independently fail closed after file movement/stale manifests.
- **Expected vs actual:** a selected take should be bound to a receipt signed by owner selection, immutable variant/hash and the exact frozen approved PNG inputs, and validated again on edit handoff.
- **Impact:** a correct-length stale/wrong clip might reach a preview/export without an explicit media lineage check.
- **Fix:** introduce per-take selection receipts with source SHA-256, sidecar SHA and approved endpoint SHA-256; add a shared `validate_selected_take()` used by preview, lip-sync, edit and publishing. Reject missing/conflicting sidecars, wrong variant and cross-story inputs for independent v6.
- **Regression:** rename a wrong-length-matching old video to the expected v6 take name; it must fail, even though duration/frame count match.

#### CONS-031 — The active v6 timing sheet and shot-plan image register are stale

- **Priority/status:** **P1 / verified**, by an ID-by-ID comparison against the 2026-10-10 active v6 manifest. **Stage:** owner/agent handoff and keyframe selection.
- **Evidence:** `stories/lion_and_mouse_v6/TIMING_SHEET.md` contains **154** shot rows; **121/154** row endpoint-filename pairs disagree with `prompt_manifest.json` at the same shot ID; only 33 rows match both endpoints. Example: `TIMING_SHEET.md:31-38` says `stream_afternoon_r01.png` and `s01_01_explores_start_r01.png`, while the active records name `stream_afternoon_r02.png` and `s01_02_explores_start_r02.png`. The `SHOT_PLAN.md:169-202` image register has **33/33** filename entries different from their current manifest image record target. Its shot-order/record *IDs* can still be useful; the embedded filenames are not reliable. `TIMING_SHEET.md:154` retains an old `s07_02_milo_sorry_start_r05.png` for `s06_froze` while the live record uses the new v6 `r02` chronological filename. A reproducible read-only comparison is provided in §9.3.
- **Expected vs actual:** every active generated reading copy must agree with the manifest's *current* paths; revisioned physical filenames must never be guessed from record IDs or obsolete PDF/Markdown plans. Instead two central v6 handoff files present old filenames as current.
- **Impact:** a delegated agent may attach the wrong artwork, falsely report a missing image, or create a file under a superseded name. Manual review would then disagree with the hash-bound manifest; Mac and LUMI may resolve different inputs.
- **Fix:** make `TIMING_SHEET.md` and the image register in `SHOT_PLAN.md` generated artifacts from **`prompt_manifest.json` + `timing_plan.json`**, after v6-native audio timing is validated. Fix `production/chain_plan.py`'s sheet writer or add a dedicated `--check` mode; regenerate docs only after manifest is final. Do **not** hand-edit 121 table rows without adding a perpetual machine-check. Preserve the old sheet in Git history, not as active instructions.
- **Regression/acceptance:** compare all 154 sheet row start/end basenames and all 33 register target basenames to the active records; **0 mismatches** on Mac and LUMI. Verify totals, shot order, duration, frame count and speed are unchanged except where final v6 audio legitimately revises them. For references across scene boundaries, compare by *record ID/first film use*, not assumed scene prefix.

#### CONS-032 — LUMI environment setup can fail before installation when `WITH_CONDA` is absent

- **Priority/status:** **P1 / verified shell behavior with a deliberately unset variable; actual installed LUMI container environment unverified**. **Stage:** setup/portability.
- **Evidence:** `lumi/setup_env.sh:13-15` places `set -euo pipefail` before a bare `$WITH_CONDA` expansion **inside the Singularity container's** `bash -c` script. In an isolated Bash check (`bash -c 'set -euo pipefail; unset WITH_CONDA; $WITH_CONDA'`), exit code was **1**, message `WITH_CONDA: unbound variable`. By contrast `lumi/env.sh:10` uses safe `${WITH_CONDA:-}`. **No evidence suggests LUMI needs a user-created Conda environment:** `setup_env.sh:15-20` uses a Python **venv** with `--system-site-packages` on the existing ROCm/PyTorch container. The configured container might have an internal Conda hook to surface its packaged PyTorch; whether `WITH_CONDA` is set in the owner's actual LUMI session is **unverified**.
- **Expected vs actual:** the existing LUMI **Singularity + scratch venv** setup works even if the optional hook is not set, provided the chosen container Python exposes its required packages. Mac Conda setup remains a separate local workflow.
- **Impact:** first-time/rebuild setup *can* fail at shell expansion, leading agents to mistakenly install their own Conda environment on LUMI or run a different interpreter. This is a **conditional setup risk**, not evidence that the owner's existing functioning LUMI environment is broken.
- **Fix:** first inspect the actual existing LUMI interpreter, venv and container startup **read-only** (§8.4). If no hook is needed for this pinned SIF, retire the redundant `WITH_CONDA` lines entirely; if the container needs it, use a guarded, documented hook and test both set/unset states. Never prescribe `conda create`, `conda activate feltwillow`, or Mac paths **on LUMI**. Record SIF checksum and frozen venv package versions, and retain fail-fast validation that PyTorch and ffmpeg are accessible in the correct interpreter.
- **Regression:** run shell-only missing-variable test; then test a new scratch-venv setup **only with operator authorization and in a disposable path** in the pinned LUMI container. Compare commands/exit codes with the already working environment; no spontaneous reinstallation during an audit.

#### CONS-033 — LUMI bulk render driver skips existing MP4 files without verifying their source receipts

- **Priority/status:** **P1 / verified source logic, end-to-end stale-take effect inferred**. **Stage:** GPU render cache, take reuse.
- **Evidence:** `lumi/render_story.sh:16-27` considers a shot complete whenever each expected `_fast.mp4` path exists. It does **not** open the sidecar, inspect the current frozen PNG hashes, verify recipe settings, or call `production/shot.py:49-60` for those existing files. That stronger check runs only if `shot.py` is invoked, which the bulk driver skips for its supposedly complete jobs. It also scans the literal `work/stories/` path instead of `feltwillow.paths.WORK` (see CONS-034).
- **Expected vs actual:** any run marked complete must match the exact active manifest/approved endpoint hashes, prompt, seed, model and fast setting. An MP4 file's existence is not proof that it was rendered from the current revision.
- **Impact:** a stale/wrong-version take can silently survive a scene rework and be counted as done; partial backups and renames may further hide broken render lineage.
- **Fix:** extract `shot.py`'s receipt verifier into a read-only `production/validate_render.py` CLI/library and call it in `render_story.sh` before skipping. Missing sidecar, hash mismatch, wrong variant/version, truncated frames or unapproved endpoints must yield a distinct **stale** status and block or queue an authorized clean rerender; do not automatically overwrite existing MP4 files during an audit.
- **Regression:** leave the expected MP4 filename in place but alter/remove its sidecar, one approved source PNG, or prompt hash; the driver must **not** report the job done. With all receipts matching, rerun remains idempotent and performs no GPU work.

### P2 — documentation, platform reproducibility and test coverage

#### CONS-020 — `.review` candidates, work review files and audio are not delivered by Git

- **Priority/status:** **P2 / verified Git-ignore policy; physical Mac/LUMI contents unverified**. **Stage:** asset transfer.
- **Evidence:** `.gitignore:1-20,37-38` ignores `work/`, generic WAV/MP4 and all `**/.review/` folders while allowing committed character/location PNGs. `LUMI_HANDOFF.md:9-11` acknowledges the 42 ignored candidate files/contact sheets and v6 audio transfer need. The tracked tree has no `.review` candidate files.
- **Expected vs actual:** a handoff is complete only when a separate transfer inventory supplies every required ignored file by SHA; Git pull alone is insufficient.
- **Impact:** agents on LUMI may rebuild candidates from unapproved roots, work without word timings, or treat a local Mac file as universally available.
- **Fix:** create a version-scoped `v6-transfer-manifest.json` (schema, logical relative path, SHA-256, size, media metadata, approval/owner status, source commit and source machine; no secrets) and a verified rsync/tar procedure with two-way checks. A missing candidate remains missing, not automatically generated or approved.
- **Regression:** run manifest verification both sides; same asset set must produce the same normalized audit JSON; missing/modified files yield explicit nonzero errors. Preserve local/remote snapshots securely.

#### CONS-021 — Critical gates have only two small committed test modules and no observed CI workflow

- **Priority/status:** **P2 / verified test inventory, coverage conclusion inferred**. **Stage:** regression safety.
- **Evidence:** HEAD tracks `tests/test_lipsync_attribution.py` and `tests/test_story_packet_speakers.py`; both focus on speaker/mouth behavior. No tracked `.github/workflows/` was present in the recursive tree. No dedicated regression suites for v6 independence, candidate generation receipts, chronological dependencies, strict handoff, join contact-sheet correctness or Mac/LUMI equivalence were found.
- **Expected vs actual:** independent releases need automated negative tests proving that a broken source of truth cannot accidentally pass.
- **Impact:** a documentation or approval fix can regress silently in a future story.
- **Fix:** add fixture-only tests named `test_v6_independence.py`, `test_image_provenance.py`, `test_dependency_order.py`, `test_chain_preview_joins.py`, `test_portable_lipsync_cache.py`, `test_runtime_identity.py`, plus an OS-neutral CI check. Mirror tests on Mac/LUMI for actual media toolchains. Do not embed real child/voice personal media in public fixtures.
- **Regression:** include deliberate failures: renamed copied v5 plate, `.review` reference, changed prompt hash, missing approval, future-state edge, changed mtime/root, wrong take sidecar, broken join frame.

#### CONS-022 — Edit/output manifests contain machine-absolute paths

- **Priority/status:** **P2 / verified**. **Stage:** Mac/LUMI/DaVinci exchange.
- **Evidence:** `production/edit_manifest.py:81-106` serializes `source_file: str(clip.resolve())`, `audio_file: str(scene_audio.resolve())`; `production/lip_sync.py:136-138,364-370` similarly serializes absolute audio/video/word paths. Hashes accompany some entries but absolute locators bind them to one filesystem root.
- **Expected vs actual:** editing and archive manifests refer to logical version-root-relative assets and content SHA, resolved against an explicit root supplied by the consumer, with path containment checks.
- **Impact:** copying an otherwise valid edit project changes path identity or breaks media relinking.
- **Fix:** version the output schema and use `origin_root`, `logical_path`, `sha256` and, if useful, optional diagnostic `source_machine_path` outside the semantic identity. Provide an explicit relink/verify command for DaVinci Resolve or another editor.
- **Regression:** move the same handoff bundle to two different directories, validate hashes and assert equivalent machine-neutral JSON data.

#### CONS-023 — Image approval spec digest omits potential generation/review fields

- **Priority/status:** **P2 / verified field omission; effect inferred**. **Stage:** immutable image spec.
- **Evidence:** `production/image_approval.py:8-19` lists fields contributing to `spec_sha256`; it includes positive prompt but not `negative_prompt`, generator model revision, raw requested crop/size, transformation settings or submitted generation reference receipts. `image_prompts.py` keeps a `negative_prompt` in many records.
- **Expected vs actual:** every input that can affect generation or review must participate in the immutable recipe digest, with a canonical schema and stable version.
- **Impact:** materially changed image instruction may not stale an approval; different machines may interpret a supposedly identical recipe differently.
- **Fix:** separate **generation recipe SHA**, **visual review spec SHA**, **approved file SHA** and **render endpoint identity SHA**, each with documented canonical JSON and schema version. Include negative prompt if actually sent, or explicitly mark it `review_only` if not sent.
- **Regression:** mutate one applicable recipe field at a time and assert correct cache/approval invalidation; reorder nonsemantic JSON keys and assert identical digest.

#### CONS-024 — Shared narration lines lack chosen film-time subintervals

- **Priority/status:** **P2 / verified metadata, risk inferred**. **Stage:** timing, audio–image alignment.
- **Evidence:** 31 line IDs occur in multiple planned v6 pieces; `production/chain_plan.py:179-205` divides line span among user pieces. All 161 `chosen_shot_intervals` arrays in `dialogue_coverage.json` are empty; real v6 audio/word alignment was unavailable.
- **Expected vs actual:** each word/pause belongs to its actual v6 audio time and shot portion, particularly when a speaker enters/leaves a close-up.
- **Impact:** a piece can switch scenes/crops in the middle of a word, use the wrong mouth anchor or hold an expression through unintended syllables.
- **Fix:** once v6 audio exists, compute/record owner-reviewed split points on word or silence boundaries. Align shots and mouth cues to the verified final transcript; do not treat equal line-time division as a final lip-sync map.
- **Regression:** assert every word belongs to at most one mouth piece for a given visible speaker, no gaps at transitions unless intentionally silent, and 0 narrator-to-mouth assignments.

#### CONS-025 — Documentation and CLI defaults still point to removed/older versions

- **Priority/status:** **P2 / verified**. **Stage:** onboarding and command correctness.
- **Evidence:** `production/shot.py:86` defaults `--story lion_and_mouse_v2` (deleted); `production/image_prompts.py:819` defaults to v5. `README.md:82-95` describes v3/v4 as a LUMI quick-start while invoking v5, and `docs/creation-rules.md:3-5` links old v3/v4 review/repair paths. `docs/lip-sync.md:12-15` explicitly shows `--audio-story lion_and_mouse_v5` for v6.
- **Expected vs actual:** version-targeted commands always require the story slug and fail before work if missing, and every command shown for v6 uses v6-local audio, refs and paths.
- **Impact:** an agent may run the wrong story or alter a retired tree.
- **Fix:** require `--story` for all mutating/export/render commands, update every current example, and separate historical pages into a labeled archive. For independent v6, explicitly reject foreign `--audio-story` at argument validation time.
- **Regression:** execute `--help` and dry-run for each documented current command; no example should depend on a removed v2-v4 folder.

#### CONS-026 — Mac/LUMI equivalence is a requirement but lacks a canonical cross-machine acceptance artifact

- **Priority/status:** **P2 / verified absence in audited gates; end-to-end parity unverified**. **Stage:** reproducibility.
- **Evidence:** `lumi/site.sh:7-17` deliberately centralizes machine-specific model/cache/container locations and `feltwillow/paths.py:13-28` derives repository roots; however `feltwillow/lipsync.py` hashes resolved absolute paths. No shared, committed golden JSON fixture/procedure was found that compares v6 image approval verdicts, pixel-box measurements, source lineage and content IDs between Mac and LUMI.
- **Expected vs actual:** same normalized input bytes/spec/review annotations yield the same signed verdict and hashes on both machines; decoder/tool differences are pinned and disclosed.
- **Impact:** manual review and cache decisions may appear to change after moving the project, even when the artwork does not.
- **Fix:** implement reproducibility contract (§9.6), pinned container/Conda toolchain versions, normalized JSON, strict SHA256 relative-path manifests and golden fixtures; separately record nondeterministic ImageGen output as *new versions*, not as a promise of pixel-equal generation.
- **Regression:** output-equivalence harness with `sha256sum` and JSON diff across Mac and LUMI on the same transferred fixture packet; negative test changes one pixel and must yield an invalidated asset.

#### CONS-027 — Other-story acceptance labels conflict with actual owner-review semantics

- **Priority/status:** **P2 / verified source mismatch, downstream effect inferred**. **Stage:** shared approval contracts.
- **Evidence:** `stories/ugly_duckling_v1/prompt_manifest.json` marks 152/156 images `accepted`, while `CLAUDE.md:85-86` says some recently generated scenes remain pending owner review, with a swan canonical/expressions discrepancy. v5 manifest marks all 140 accepted despite three untracked targets by their current path. Story-specific source and owner review requirements are not uniformly encoded.
- **Expected vs actual:** `accepted` should have a precise, story-version-independent meaning with an explicit owner-review receipt; `candidate`, `agent_reviewed`, `owner_approved`, `stale` and `superseded` must not be conflated.
- **Impact:** future multi-story agents could borrow an image based on an ambiguous label (even within its own version) or skip visual QA.
- **Fix:** introduce shared namespaced stage/approval schema without rewriting older provenance; migrate active new stories carefully and validate all uses of old status strings. Do not treat historical v5/ugly statuses as permission to copy into v6.
- **Regression:** test runtime/export gates against ambiguous or missing owner-review metadata for *new* stories, while allowing explicit legacy read-only inventories.

#### CONS-028 — No end-to-end video/render/device validation was possible in this audit

- **Priority/status:** **P2 / unverified evidence gap, not a claim of broken media**. **Stage:** video physics, performance and reproducibility.
- **Evidence:** current v6 HEAD does not include rendered clips, selected take files or v6 WAVs; `work/` is git-ignored. The available environment could not mount a clone or use the LUMI GPU/container. Wan model revision, fast Lightning LoRA version/checksum, seeds, selected takes and actual frame sizes were therefore not checked end to end. Some v6 negative prompts are marked “review only” because `shot.py:138-140` reports `--fast` bypasses negative conditioning.
- **Expected vs actual:** a future production preflight verifies installed software/model weights and hashes, configured fps/resolution/seed, source frame hash, output metadata, first/middle/last and interaction-critical frames, join quality and model availability on LUMI.
- **Impact:** a plausible text manifest does not establish stable generated motion or that a command will successfully run on the intended GPU.
- **Fix:** once P0s are resolved, execute the bounded pilot protocol in §9.7 and attach actual command transcript, GPU environment, media hashes, frame contact sheets and owner review. Never assert pixel-identical stochastic ImageGen/Wan outputs across different hosts; require reproducible *input identity and validation behavior*.
- **Regression:** pin model/tool versions and test same cached bytes and normalized inspection fixtures on Mac and LUMI; record nondeterminism honestly.

#### CONS-034 — Configurable `FELTWILLOW_WORK` is ignored by backup and batch-render inventory

- **Priority/status:** **P2 / verified source mismatch, actual external-work setup unverified**. **Stage:** Mac/LUMI data portability and backup coverage.
- **Evidence:** `feltwillow/paths.py:15` makes `WORK` relocatable using `FELTWILLOW_WORK`. Yet `lumi/backup_assets.sh:21-35` writes the inventory to `work/backup_files.txt` and searches literal `work/`, while `lumi/render_story.sh:21-26` checks clips under literal `work/stories/<story>/shots`. These do not necessarily refer to `paths.WORK` if the environment override is set. The backup is also invoked by a printed rsync command whose `--files-from` paths assume the repo root.
- **Expected vs actual:** all tools that resolve generated data, enumerate items to back up and check completed jobs must use the same canonical configured work root. A chosen external root must never silently disappear from a backup.
- **Impact:** a Mac or LUMI agent may conclude outputs are absent when they exist elsewhere, or generate an incomplete archive even though the backing work tree contains critical audio/takes/review assets.
- **Fix:** choose one policy: (A) disallow external work roots for current production with an early explicit error; or (B) support external roots throughout by emitting a root-aware transfer inventory with source root, logical path, byte size, SHA-256 and required destination. Do not concatenate external paths into unsafe `rsync --files-from` entries. Validate backup completeness after transfer, including `.review` and v6 narration, with independent SHA checks.
- **Regression:** run read-only inventory tests with default `work/` and two external `FELTWILLOW_WORK` locations; the tool must discover the same logical files and hash set in each. A missing transfer must cause a nonzero validation result.

### P3 — bounded clean-up

#### CONS-029 — Committed platform metadata in repository root

- **Priority/status:** **P3 / verified**. **Stage:** hygiene.
- **Evidence:** recursive tree contains tracked `.DS_Store` at repository root.
- **Fix:** remove from tracking during an authorized cleanup and add `.DS_Store` to `.gitignore`; keep only code/project documentation and intended media in version control. No v6 media dependency is established by this file.
- **Regression:** `git ls-files '.DS_Store' '**/.DS_Store'` produces no results.

#### CONS-030 — Legacy doubled PNG extensions and historical links confuse inventory

- **Priority/status:** **P3 / verified**. **Stage:** v5 history and discovery.
- **Evidence:** v5 tracked paths include `Milo/references/m_back_r01.png.png`, `m_side_l_r01.png.png`, `m_side_r_r01.png.png`; `production/chain_packet.py:62-76` includes a fallback for doubled extensions. Root/generic docs still point to deleted v4/v3 files (see CONS-025).
- **Fix:** leave v5 immutable as history unless a separate owner-authorized v5 migration is approved; make readers robust/explicit for old filenames but do not import them into v6. Clean up obsolete active links and prevent new doubled extensions in new story manifests.
- **Regression:** new-story lint rejects `.png.png` and broken active links, with explicit legacy exemptions.


## 5. Visual-review ledger: inspected versus explicitly unviewed

**A visual opinion cannot be inferred from this audit.** The GitHub connector supplied text/JSON and blob identifiers but rejected binary PNG delivery (`UnicodeDecodeError` for a PNG blob). The hosted container had no direct network access to GitHub, no checkout with tracked PNGs, and no access to Git-ignored `.review` assets or LUMI `work/` clips. Hence **no source art pixel grid or actual movie frame has been reviewed in this audit**, including the owner-approved r02 images. This is an explicit unverified evidence boundary, not a negative artistic judgment. All generated candidate artwork remains `UNVIEWED_BY_THIS_AUDIT` regardless of a saved approval or candidate label.

| Visual population | Tracked/claimed population | Viewed at full resolution here | Viewed at 1280×720 here | Decision and follow-up |
|---|---:|---:|---:|---|
| v6 character canonical/pose/reference PNGs | 20 accepted-label | 0 | 0 | Must inspect each with native character identity checklist; canonical first |
| v6 expression PNGs | 22 accepted-label | 0 | 0 | Must compare 22 against current character canonical/mouth proportions |
| v6 locked location plates | 10 accepted-label | 0 | 0 | **Not admissible as independent v6** because their tracked blobs equal v5 (§6) |
| v6 prop PNGs | 2 accepted-label | 0 | 0 | **Not admissible as independent v6**; replace net/acorn under v6 roots |
| v6 `.review` scene/portrait candidates | 42 manifest records; binary availability on Mac/LUMI unknown | 0 | 0 | Provenance stale; current visual review must not serve as approval without rebuilding current-input lineage (CONS-002/003/004) |
| v6 planned scene frames | 71 records; no accepted targets | 0 | 0 | Not generated/available in committed HEAD |
| v5 tracked artwork | 143 PNG/JPG in tree, incl. historical targets/supplements | 0 | 0 | Separate historical project. Inspect in a distinct v5 audit, **never as v6 creation references** |
| Ugly Duckling v1 tracked artwork | Artifact counts in §3; actual pixels unviewed | 0 | 0 | Owner-review assertions must be reconciled for this story only |
| Tortoise/Hare and Boy/Wolf scene artwork | No tracked manifest-target PNGs | 0 | 0 | Script/planning only by tracked evidence |
| All v6 rendered movie takes, chosen takes, mouth-sync and edit | Not present in Git; LUMI contents unknown | 0 frames | 0 frames | **Cannot assess motion, anatomy persistence, joins, sync, audio or scene physics** |

### 5.1 Mandatory review ledger schema for the next authorized image pass

Keep one immutable review record **per image record ID and exact file SHA-256**, with at least:

```json
{
  "story": "lion_and_mouse_v6",
  "record_id": "<image-id>",
  "stage": "canonical | expression | native_plate | native_prop | size_anchor | start | end | mouth_calibration",
  "file": "<v6-relative-path>",
  "sha256": "<digest-of-delivered-PNG>",
  "source_generation_receipt_sha256": "<immutable-recipe-and-ref-receipt>",
  "canvas_pixels": [1920, 1080],
  "comparison_ids_and_sha256": [{"record_id": "<v6-approved-reference-id>", "sha256": "<digest>"}],
  "setup": "<bible-setup-id-or-null>",
  "landmarks": [{"id": "<fixed-landmark>", "observed_xy": [0.0, 0.0], "reference_xy": [0.0, 0.0]}],
  "cast": [{
    "character": "milo",
    "depth_plane": "<named-depth>",
    "head_bbox_px": [0, 0, 0, 0],
    "whole_body_bbox_px": [0, 0, 0, 0],
    "support_point_px": [0, 0],
    "support_surface": "<walkable-surface-name>",
    "paw_or_foot_count_visible": "<count-and-occlusion-explanation>",
    "identity": "pass | fail | uncertain",
    "ground_contact": "pass | fail | uncertain"
  }],
  "plate_geometry": "pass | fail | uncertain",
  "prop_count_and_state": "<physical-description>",
  "endpoint_continuity": "pass | fail | uncertain | not_applicable",
  "review_at_native_resolution": "pass | fail | uncertain",
  "review_at_1280x720": "pass | fail | uncertain",
  "reviewer": "<authorized-owner-or-reviewer>",
  "reviewed_at_utc": "<ISO-8601>",
  "decision": "owner_approved | owner_rejected | needs_revision",
  "notes": "<specific-visible-facts-and-failures>"
}
```

**This is a proposed review-schema example, not an existing repository schema or approval receipt.** Never fabricate the pixel boxes, `reviewer` identity or a `pass`. The code should derive the measured frame fractions from boxes rather than reading hand-typed answers. Save an immutable contact-sheet locator and a comparison of the exact v6 reference hashes. The owner must verify that an apparent mask/box includes the actual visible anatomy and that occluded anatomy is physically possible; bounding boxes alone do not prove three-dimensional consistency.

### 5.2 Concrete v6 size checks (target values only; zero measured outputs)

Read `stories/lion_and_mouse_v6/visual_bible.json` anew for any changed setup; the values below describe the inspected revision `v6-native-r02-2026-10-10` only. At a **1920×1080** approved frame canvas, screen fractions correspond to these illustrative dimensions:

| Context | Frame fraction from bible | Corresponding vertical pixels on 1080-high still | Interpretation |
|---|---:|---:|---|
| Milo standing, v6 wide/two-character setup | ear tips to planted feet **0.21** | about **227 px** | Same setup/depth; do not apply to sitting, far-depth or portrait |
| Milo head including ears, wide setup | **0.10** | about **108 px** | Preserve intrinsic ear/head proportions |
| Leo mane, tree dusk shared setup | **0.38** | about **410 px** | Depends on pose and the tree-dusk setup |
| Leo mane, trap wide setup | **0.42** | about **454 px** | Compare relative to Milo at a recorded depth plane |
| Leo face, trap-bite close two-shot | **0.50** | about **540 px** | The setup is different; do not compare to unrelated close-up |
| Milo standing, tree-day wide setup | **0.17** | about **184 px** | Explicit setup exception, not a universal v6 target |
| Leo mane, tree-day wide setup | **0.37** | about **400 px** | Review against its own anchor |

Same-depth anatomical relationship targets are **Milo standing height ≈0.55 × Leo mane height** and **Milo head+ears ≈0.42 × Leo face height**. These *ratios* are not substitutes for recording actual depths/crops; the scene can legitimately show a different screen ratio if one actor stands nearer the camera. The current `image_handoff.py:156-159` code allows up to 0.020 frame fraction difference for `height/mane/face` and up to 0.015 for other dimensions; that is approximately 22 px and 16 px on a 1080-high frame. These are gate tolerances, **not claims that any PNG has been measured**. If the owner elects a tighter rule, change the bible/validator and version the approval contract explicitly.

### 5.3 Fixed landmark and contact inventory for future v6-native plates

These named coordinates are **the inspected bible's current design brief**, not confirmation that an available image actually matches them. Since current plates are copies of v5, new independent v6-native artwork must be measured and its landmark geometry re-approved rather than assumed equal. The following examples help a second agent locate the intended surfaces, determine whether a pose is supported, and flag unauthorized drifts:

| Place ID | Existing plan's fixed landmark examples (normalized) | Valid support and critical interactions |
|---|---|---|
| `stream_afternoon` / `stream_sunset` | Feeding stone around **(0.60, 0.60)**; stream band **y=0.44–0.60**; right trunk x=0.70–0.79; hollow log x=0.80–1.00 | Clear grass lane is walkable. Acorn must rest on stone or be in a paw; neither stream surface nor bush crowns support Milo |
| `fork_sunset` | Sun **(0.185, 0.255)**; large trunk x=0.63–0.70; boulder near **(0.58,0.44)** | Milo's feet must meet the visible dirt fork at his actual depth; preserve left/right path direction |
| `shortcut_dusk` | Setting sun near **(0.215,0.30)**; fallen branch x=0.38–0.78, y=0.50–0.66 | Distinct running legs/feet, intact single tail and stable floor/branch occlusion |
| `tree_dusk` | Trunk x=0.58–0.87; roots y≈0.50–0.62; grey rock near **(0.435,0.605)** | Leo has **four** paws, Milo two upright feet and two front paws; paw/nose touch causality, support shadow and Leo's whole lion body must make sense |
| `tree_day` / `tree_sky` | Tree-day rock **(0.435,0.605)**; sky view sun near **(0.16,0.85)** | Do not equate a sky cut with a ground-camera shot; restore tree geometry where intended and verify rest/sitting support |
| `home_night` | Door around **(0.31,0.55)**; lantern **(0.40,0.47)**; stream on right lower half | Milo travels to a grounded doorway; lantern remains fixed, no waterwalking |
| `trap_morning` | Left rock x=0.12–0.27; right rock x=0.68–0.87; edge trunks x=0.00–0.12 / 0.88–1.00 | Net must be attached overhead before fall and around Leo **after** fall, with continuous rope connections and intact-to-broken causality; face remains visible |
| `run_morning` | Arch branch **(0.40,0.38)→(0.93,0.52)**; mossy rock x=0.25–0.45, y=0.42–0.62 | Upright running on the dirt lane at a stable depth, feet visible unless clearly occluded |

### 5.4 Mandatory visual-review order (not yet executed)

1. Authorize truly native v6 plate/net/acorn designs, then individually inspect their generated full-resolution PNGs and record real hashes; reject any v5-derived copy or visually copied derivative. First validate the empty plates and each prop's topology/material design.
2. Verify the two current v6 canonicals and 18 other pose/references against the owner's actual accepted v6 identity. Count Leo's four limbs/paws, mane topology and tail; count Milo's two legs, two arms, feet/toes, single tail and five whiskers on each side when visible. Do not infer a hidden limb failure from mere occlusion without reviewing pose context.
3. Verify 22 expressions against the approved canonical head geometry and mouth studies. Expressions may change eyes/brows/mouth but not species, ears, felt palette, stitches, head volume or muzzle placement.
4. Generate/inspect each of the 11 sharp setup anchors in §7; measure the actual anatomical boxes, baseline and approved floor. Check both actors in a shared anchor when both are visible. For close-ups use setup-specific head/crop rules; do not force the wide-shot 0.21 target onto portraits.
5. Review **every** candidate/scene frame and both ends of every pilot pair. On each pair overlay landmarks, camera/crop, actor depth/size, ground contact, light direction, prop count/holder, tail/paw state and join direction. At a transition, inspect both adjacent frames, not just the source shot.
6. Special scene 10–15 pass: make one physical net-state table (`overhead_intact → triggered → wrapped_on_Leo → gnawed_at_specific_rope → split_strand_ends → widened_gap → freed_Leo/net_left_behind`). Check actual rope attachment and front/back occlusion at every stage, including paw-to-strand contact and the exact sever location. **A flat screen of ropes in front of Leo is not sufficient.**
7. Later, inspect each selected v6 video take at the first, middle and last frames **plus** contact frames; check silhouette drift, duplicated paws/tails, strobing, auto-added props, rope motion, actor/plate scale, close-up mouth states and audio-to-action alignment. Inspect and sign every flagged chain join. Neither a good starting PNG nor a correct number of frames proves video consistency.

A delegated visual agent must write the asset ID, exact SHA, full-resolution file/contact-sheet or timecode locator and one of `PASS`, `FAIL`, `UNCERTAIN`, `NOT_VIEWED` for *every* artifact it claims to have reviewed. The present audit contains no `PASS` visual verdicts.

## 6. Dependency map, duplicate-byte ledger, and stale-data impact

This section is the **operational invalidation map**. It is not a suggestion to delete files immediately. An agent must work from the immutable reviewed HEAD, produce a proposed change list, obtain separate approval for destructive actions, and then reconcile every dependency. A copied path under the v6 tree is still an imported v5 asset if the committed file bytes match a v5 asset.

### 6.1 Complete proven v5/v6 identical-file ledger

The following pairs were compared by their **Git blob OIDs** in the recursive tree of commit `eac8d388639e6053113b071d7f3e08f3a0cac353`. Matching object IDs in the same Git object database establish byte-identical content (not merely same dimensions or filename). Prefix both filenames with `character/locations/` to obtain the exact repository-relative paths. Every v6 file below is a tracked, `accepted` foundation image at HEAD. These are the **12** v6 foundation records that require independence remediation; do **not** count the old files as v6-approved because they have a v6 folder name.

| V6 manifest ID | V6 tracked file | Byte-identical v5 tracked file | Common Git blob OID |
|---|---|---|---|
| `PL_run_morning` | `lion_and_mouse_v6/forest_run/run_morning_r02.png` | `lion_and_mouse_v5/forest_run/run_morning_r01.png` | `76fb8cbd000ecd00c4617d8f9a43d6c03ef728ab` |
| `PL_fork_sunset` | `lion_and_mouse_v6/fork/fork_sunset_r02.png` | `lion_and_mouse_v5/fork/fork_sunset_r01.png` | `e9e994fc8add2b5b1fa777db2d282f87c405e8a1` |
| `PL_tree_day` | `lion_and_mouse_v6/great_tree/tree_day_r02.png` | `lion_and_mouse_v5/great_tree/tree_day_r01.png` | `7d436ef9325d6d56f3b7366c9630eb380c0d0f2a` |
| `PL_tree_dusk` | `lion_and_mouse_v6/great_tree/tree_dusk_r02.png` | `lion_and_mouse_v5/great_tree/tree_dusk_r01.png` | `5f759fadc7f55a7a67e677577d08a9102fb8dacf` |
| `PL_tree_sky` | `lion_and_mouse_v6/great_tree/tree_sky_r02.png` | `lion_and_mouse_v5/great_tree/tree_sky_r01.png` | `9c59c83e6c06ce9a4eb351e11e654c09641e4176` |
| `PL_home_night` | `lion_and_mouse_v6/milo_home/home_night_r02.png` | `lion_and_mouse_v5/milo_home/home_night_r01.png` | `ad4804c80fac53095f29020669f7ac0b8af4d872` |
| `PROP_ACORN` | `lion_and_mouse_v6/props/prop_acorn_r02.png` | `lion_and_mouse_v5/props/prop_acorn_r01.png` | `5b427ebbdc470e0115c8703be6b5a0129b4` |
| `PROP_NET` | `lion_and_mouse_v6/props/prop_net_r02.png` | `lion_and_mouse_v5/props/prop_net_r01.png` | `9b37a474a9dee295f3c3f28bf0a887c9a444c9c4` |
| `PL_shortcut_dusk` | `lion_and_mouse_v6/shortcut/shortcut_dusk_r02.png` | `lion_and_mouse_v5/shortcut/shortcut_dusk_r01.png` | `4d1959bbb76087b2063f696a0176ad7182098` |
| `PL_stream_afternoon` | `lion_and_mouse_v6/stream_bank/stream_afternoon_r02.png` | `lion_and_mouse_v5/stream_bank/stream_afternoon_r01.png` | `852e8ca88f66a953126ac6c843ec13393fe8cfae` |
| `PL_stream_sunset` | `lion_and_mouse_v6/stream_bank/stream_sunset_r02.png` | `lion_and_mouse_v5/stream_bank/stream_sunset_r01.png` | `ee8025e584b552a1be6632da872930065099f269` |
| `PL_trap_morning` | `lion_and_mouse_v6/trap_path/trap_morning_r02.png` | `lion_and_mouse_v5/trap_path/trap_morning_r01.png` | `5f2e0f45c28347d828bc6eb4c5289cc3a38eb752` |

**Re-check after updating HEAD:** inspect actual SHA-256 for source and deliverable bytes, not just Git OID. Scan *all* active v6 manifest targets against every earlier-version Lion and Mouse tracked image, not only the filenames in this table. The current tree-level scan found these 12 byte-identical pairs and no additional v5-identical v6 PNGs among the **54 currently tracked v6 images**. This is a test of exact equality, not proof that the other 42 are visually original or independently sourced.

### 6.2 Transitive impact: changing those 12 foundation roots

Using all `images[].ordered_references[].id` links, the transitive closure of the ten plate roots and two prop roots reaches **all 113 v6 scene image records**: **42 candidates and 71 planned records**. Every one of the **154 planned v6 shots** consumes one or more of those images/plate records, directly or by their dependency chain. This is an *impact graph*, not an assertion that 113 scene PNG files exist. None is owner-approved at present, and the 42 untracked candidates already have other provenance problems. Therefore it is not viable to repair only one scene and then consider the remainder immune to the plate/prop replacement.

Single-root blast-radius examples (counts are **transitive graph references**, may overlap, and are not additive):

| Root | Downstream scene-image records | Candidate records within closure | Film pieces touched by root or descendants |
|---|---:|---:|---:|
| `PL_stream_afternoon` | 11 | 0 | 14 |
| `PL_stream_sunset` | 5 | 0 | 5 |
| `PL_fork_sunset` | 7 | 3 | 10 |
| `PL_shortcut_dusk` | 4 | 0 | 4 |
| `PL_tree_dusk` | 51 | 15 | 77 |
| `PL_tree_day` | 4 | 0 | 13 |
| `PL_tree_sky` | 2 | 0 | 2 |
| `PL_home_night` | 2 | 0 | 1 |
| `PL_trap_morning` | 52 | 24 | 65 |
| `PL_run_morning` | 3 | 0 | 5 |
| `PROP_ACORN` | 10 | 0 | 11 |
| `PROP_NET` | 37 | 9 | 44 |
| **Union of the 12 roots** | **113 / 113** | **42 / 42** | **154 / 154** |

These counts are computed from the currently declared reference graph and shot endpoints, not from physical asset-content inspection. A future agent must recalculate closures after every change, and must not assume an unreferenced file is safe merely because it is not in this graph: it could be consumed by an ignored local script or out-of-band LUMI job.

**Required invalidation rule:** changing a root image's bytes or its identity/camera/geometry specification makes its current `image_approvals.json` receipt invalid, then invalidates all descendants, then any runtime export/frozen keyframes, rendered takes, mouth-sync recipes and edit handoffs that used the affected IDs or SHA-256s. This is a *non-destructive `stale` state transition first*. A separate authorized worker later removes/replaces stale generated outputs after backing up useful provenance. Never update hashes in an approval ledger just to make an old image pass.

### 6.3 Non-root invalidation rules that must be implemented

| Change | Invalidate or re-check | Required evidence to clear |
|---|---|---|
| Native canonical identity, palette, eyes, paw/ear/mane geometry | Pose studies, facial expressions, mouth calibration, all scene images showing that character, associated renders | New v6 canonical owner approval; precise descendant hash set; revised visual check for each affected derivative |
| Expression study or mouth design | Scene faces that reference it, open/closed mouth pairs, mouth-motion calibration and composited video | Current immutable generation receipt, same crop/identity verification, new exact-image approval |
| Locked plate, camera, light, horizon or terrain | All keyframes on that plate, their setup anchors, adjacent joins, downstream video | New approved plate and measured landmarks; plate-geometry overlays; current-start/end approval |
| Prop/net topology or state timeline | Every scene containing/depending on prop; net severing and release chain, body occlusion | State-by-state net topology contact sheet with one physical net and consistent broken ends |
| Sharp setup anchor or numeric scale target | All dependent start/end frames in same setup and any chains referring to them | Actual pixel measurement at native/delivery resolution; approved anchor and reported actor depth |
| Line transcript, speaker, audio or line ordering | `dialogue_coverage`, word timings, timing-plan spans, variants, mouth pieces and edit offsets | V6-local line-WAV hashes, transcript and speaker equality, no narrator lip motion; updated timing-plan check |
| Video positive prompt, mode, frames, seeds, model/LoRA version, any endpoint bytes | Affected runtime recipe, existing render cache and take selections | Exact render-input sidecar/hash match; new owner-selected take receipt for any changed render |
| Selected take/retiming/alignment/mouth mask | Lip-sync output, chain joins, edit handoff for affected piece | Signed selection, correct source SHA, recipe SHA, word timing and post composite output SHA |
| Toolchain/measurement implementation | Previously computed measurement verdicts when semantics/thresholds changed | Golden-fixture comparison, explicit validator version recorded alongside prior and new results |

The current `image_approvals.json` contains 54 `previous_spec_sha256` reconciliation records. Those remain **evidence of historical owner decisions**, but cannot waive new independent-asset requirements. Preserve original review metadata in read-only history and issue new approvals only following the new rules.

### 6.4 Generation-order conflicts: eight future-used scene references

Eight **scene-to-scene** generation dependencies point to a reference whose *first use in film order* comes later. The graph is acyclic, so topological generation is possible in principle, but the existing instruction “generate scene images in film order” is not sufficient. The parent record may need approval earlier than its narrative debut. The three apparent extra future-use edges from `PL_run_morning` are **not** counted here: a plate has no narrative first-use requirement and may be consumed before its first empty-plate shot.

| Dependent record | Role / later reference record | Why it matters and smallest approved repair |
|---|---|---|
| `s05_leo_asleep_cu` | `framing` → `s07_leo_annoyed_start` | Uses a later Leo close-up as an earlier shot's framing guide; replace with a v6-approved independent crop template/early approved portrait, or explicitly schedule parent first |
| `s05_milo_lands_wide` | `size_lineup` → `s05_nose_aftermath_start` | References the next beat for scale; should prefer an earlier approved same-setup paired anchor when available |
| `s08_kindness_start` | `world_state` → `s08_milo_surprised_end` | Imports a future emotional/world state; check story causality rather than simply moving work earlier |
| `s09_leo_rests` | `size_anchor` → `s16_friends_start` | Uses later scene 16 as scale authority; enforce an approved current-v6 tree-day setup anchor before scene 9 |
| `s11_why_wont_it_break_start` | `size_anchor` → `s15_leo_reflects_end` | Trapped Leo close-up uses scene 15 face scale; replace with approved setup-specific early anchor |
| `s11_waits_start` | `world_state` → `s11_call_end` | World state travels backward within scene 11; inspect whether the proposed pose/camera is actually temporally valid |
| `s11_call_start` | `size_anchor` → `s15_leo_reflects_end` | Same later-portrait dependency as above; one shared v6-local early anchor is preferable |
| `s13_milo_cu` | `framing` → `s15_milo_modest_start` | Scene 13 face crop guided by scene 15; use a previously approved version-local crop standard or mark generation parent prerequisite explicitly |

**Do not delete a legitimate narrative shot** simply to remove an arrow. Resolve the *reference edge* or schedule the independent parent correctly. Any replacement reference changes the rendered prompt and must invalidate affected candidates; never rewrite an already submitted prompt in the recorded generation receipt. A correct topological build order is derived from `ordered_references`, separate from film order; all parents must have accepted, hash-bound current versions before a child is generated.

### 6.5 Hard separation of v5 and v6 is an invariant, not a rename

The following are **forbidden active v6 inputs** even if they appear behind a symlink, in `work/`, inside a sidecar, or via a convenience CLI parameter: v5 canonical/plate/prop/keyframe PNGs, v5-image-derived composites, v5 scene WAVs or word timings, v5 video clips or selected takes, inherited approval hashes, `reuse` or `carried_from` declarations, `base_story` builders, and timestamps/durations treated as a finalized v6 audio source. Historical prose may mention older versions if clearly marked historical and never linked as required v6 production material.

The future code checks must examine (1) story-relative paths, (2) resolved symlink/real paths, (3) hashes of active image/audio/video bytes against known historical assets, (4) full nested manifests/sidecars/repair overrides/tasks, (5) producer invocation arguments including `--story`, `--images` and `--audio-story`, and (6) the complete immutable generation-receipt chain. For a newly independent story in a different project, the same rule applies to its declared forbidden ancestor/source set rather than hard-coding the string `lion_and_mouse_v5` into a generic library.

**Exact-byte equality is a clear violation but not the only one.** A recolored, re-encoded, rotated or edited v5 plate can differ in SHA-256 yet still be a prohibited inherited input. An owner-reviewed original design and generation history are necessary to establish that a visually similar forest is newly authored rather than copied. Machine comparisons test byte-level consistency, *not* authorship of newly generated art.

## 7. Delegation-ready remediation plan — ordered phases, owners, exits and rollback

**Work authorization:** This document authorizes **only assessment/reporting**. The steps below are a detailed work order for a **future, explicitly authorized** agent. In that future run, do not delete assets, change approvals, produce images/TTS, submit GPU jobs or merge changes without the corresponding phase approval. No remediation has been committed by this audit.

### 7.0 Before any change: immutable baseline and quarantine

**Role:** repository maintainer + independent auditor. **Inputs:** actual Mac checkout, LUMI checkout/inventory, branch HEAD, user decisions. **Deliverables:** immutable baseline manifest, separate backup of ignored candidate/audio/clip data, proposed change list.

1. `git fetch origin && git checkout working-cloud-branch && git pull --ff-only`; capture `git rev-parse HEAD`, `git status --porcelain=v1 --untracked-files=all`, `git ls-files`, `git status --ignored --short` and the configured `FELTWILLOW_WORK`. Do not assume checkout is clean. **If HEAD differs from `eac8d388`, rerun all counts and validate changed finding locations before edits.** Never reset or clean a dirty owner's checkout automatically.
2. Snapshot `stories/lion_and_mouse_v6/{visual_bible.json,prompt_manifest.json,image_approvals.json,dialogue_coverage.json,timing_plan.json,README.md,LUMI_HANDOFF.md,SCRIPT.md,SHOT_PLAN.md,TIMING_SHEET.md}` plus all v6 tracked assets, `.review/` candidates and sidecars, `work/stories/lion_and_mouse_v6/` if present, and any remote LUMI-only files. Store a file list with logical path, byte count, SHA-256, machine/source location, time and owner; exclude secrets/private tokens. Record inaccessible sources as `NOT_MOUNTED`, not empty.
3. Freeze the 42 candidate generation result objects exactly as found. Do **not** replace `result.submitted_positive`, reference list or original source SHA. Record old approved foundation spec hashes and historic owner review notes. Do **not** copy candidate PNGs to active target names as a shortcut.
4. Compare Git state on Mac and LUMI with the same commit and hashed tracked inputs. Any mismatch must be resolved as a **transfer or provenance problem**, not worked around by silently choosing whichever image happens to exist locally. Version large ignored assets with their own transfer index.
5. Create an authorized work branch such as `fix/v6-consistency-audit-2026-10-10`, never push destructive updates directly over active branch or modify v5 production history. Prepare one reviewable commit group per phase and a rollback reference. Use small PRs with test evidence, not one wholesale rewrite.

**Entry gate:** a repeatable independent input inventory exists. **Exit:** every active v6 asset is either `current_and_verified`, `stale`, `planned`, or `unknown_input`; all existing provenance is preserved before changing anything. **Rollback:** reset the *agent's disposable worktree/branch* to recorded base, not the owner's working tree.

### 7.1 Phase A — correct sources of truth and retire competing active claims

**Role:** documentation/code maintainer. **Primary findings:** CONS-017, 018, 025, 030, 031. **Files to edit:** root `README.md`, `CLAUDE.md`, `docs/creation-rules.md`, `docs/lip-sync.md`, both `.claude/skills/*/SKILL.md` entries, `stories/lion_and_mouse_v6/{README.md,LUMI_HANDOFF.md,SHOT_PLAN.md,TIMING_SHEET.md}`, associated generated `prompts/*.md`, and CLI usage/help text as applicable.

1. Document in **one v6 policy heading**: independent story with no other-version assets/timing/reuse, 54 accepted-label foundations of which **12 are independence-blocked**, 42 candidates **stale pending provenance resolution**, 71 planned scene images, zero approved scene frames, 11 sharp setup anchors pending, 154 v6-only planned renders, 161 lines and v6 audio not verified here. These numbers are *snapshot data*, not permanent magic constants: generate future status summaries from manifests.
2. Replace root README's “v5 is current / v6 in preparation” phrasing with separate dated entries for **v5 history** and **v6 current independent plan**. Mark CLAUDE's 25-v5-render/33-new-image/borrowed-v5-audio packet clearly **SUPERSEDED — NOT OPERATIVE FOR V6**. Link to story-local current files. Do not remove valid technical lessons from other stories.
3. Replace 102 `V4 identity roots` acceptance strings in v6 active image rows with v6 canonical authority via a **generated rule**/stable IDs, not 102 hand-maintained duplicate specifications. Ensure v6 rule precedence is explicit in generic creation rules and skills. Historical V4 notes may remain under `docs/history/` but must not be a required v6 step. Document why any previously accepted spec digest changes; invalidate before reapproval, never silently reconcile.
4. Replace `--audio-story lion_and_mouse_v5` in active v6 lip-sync examples with `lion_and_mouse_v6` and remove active examples that imply v6 reuse. Change mutating command defaults to *require an explicit story ID*, or enforce active independent-policy validation at the entrypoint.
5. Make `SHOT_PLAN.md` image register and `TIMING_SHEET.md` endpoint filenames **generated views** of v6 manifest IDs/targets and saved timing data. Add nonmutating `--check`/CI assertions so every row is reproducible. Keep the human-oriented prose, but never maintain a separate contradictory image path table manually. Changing doc text is not evidence that currently pending audio is finalized.
6. Correct `LUMI_HANDOFF.md:11`: 54 foundation PNGs/code/JSON are committed in audited HEAD; `.review/` candidates, review sheets and narration are ignored/not tracked and need separate verified delivery. Do not claim these ignored files are present on a particular machine without checking.

**Acceptance:** automated read-only scan finds **zero active** v5/v4 identity/root/reuse/audio instructions attached to v6 and **zero mismatched** v6 shot-plan/timing-sheet target names. Existing v5 and other-story work still points to its own version and remains untouched. **Rollback:** revert only phase A branch changes and regenerate derived docs from the previous manifest; no assets should have been modified yet.

### 7.2 Phase B — make the independent-version rule fail closed in shared code

**Role:** production Python maintainer. **Findings:** CONS-001, 005, 013, 015, 023, 025. **Primary files:** `production/image_prompts.py`, `production/image_handoff.py`, `production/export_runtime.py`, `production/chain_packet.py`, `production/chain_plan.py`, `production/lip_sync.py`, `production/edit_manifest.py`, optional `feltwillow/version_policy.py` and a dedicated new test module.

1. Add a single **`story_policy(story)`** loader from that story's bible/manifest; for `asset_revision_policy="v6_native_assets"` require exact story slug throughout all v6 content and consumers, not merely v6 string matching in one lint command. Apply the policy at entrypoints *before* opening, copying or overwriting any image/audio/video.
2. Validate canonical/resolved paths against repository and version-local roots. Reject path traversal, foreign story manifests, foreign asset sets, symlinks to older-version PNGs and alias paths that resolve to another version. Reject `--images lion_and_mouse_v5` when targeting independent v6, `--audio-story lion_and_mouse_v5`, `base_story`, `carried_from`, `reuse`, `reused_from`, and cross-version `repair_overrides`/take paths. Retain legacy code only behind **explicit policy for legacy stories**; no permissive fallback for v6.
3. Build a **historical-hash denylist** of active earlier-version Lion and Mouse assets, or an equivalent searchable provenance index. For v6 image approvals, compare submitted/native output SHA-256 to this database. **Reject the 12 proven copies**; do not trust target pathname, declared `revision`, or an owner review checkbox as proof of independence. For derivative/modified copies, require an independent-origin receipt and human provenance assessment, not merely a different SHA-256.
4. Make byte-content receipt IDs machine neutral: logical paths must be normalized POSIX-relative identifiers; hash file bytes plus canonical JSON of the *semantic* parameters. Do not include temp directory, absolute Mac/LUMI root, host name, file mtime or process-specific counters in identities or acceptance decisions.
5. Reject an independent v6 timing plan if the observed final audio is missing, under an older story directory, or fails line IDs/transcript/duration/word-timing provenance. Leave a safe read-only `--show-plan` mode that can describe provisional metadata without exporting/rendering.
6. Gate all independent v6 runtime and edit operations through the same version/approval contract, including `export_runtime.py --images`, `edit_manifest.py`, `chain_preview.py`, `lip_sync.py` and publishing preflight where applicable. Enforce manifest/story pair identity; avoid divergent copies of the policy code.

**Acceptance:** negative tests for *every* bypass return nonzero with a specific actionable reason **before writing**. v5 legacy story remains operable in its own sandbox. Content-identical v5/v6 plate fixture fails. **Rollback:** phase B changes revert without changing any approved media; no destructive action is needed.

### 7.3 Phase C — bind image approval to the actual generation event, not mutable current instructions

**Role:** image pipeline/test engineer; owner is required for actual artistic approvals. **Findings:** CONS-002, 003, 004, 008, 009, 016, 023.

1. Introduce immutable, schema-versioned **generation receipts**. A receipt must include `story`, `record_id`, full exact submitted positive/negative text or content-addressed prompt bytes, current manifest/bible revision or canonical digests, ordered **actual** attached reference IDs+roles+resolved logical paths+SHA-256s, tool/model and version if available, requested/returned dimensions, raw source output hash and normalized candidate PNG hash. Mark truly unknown model metadata `unknown`; never invent a seed for ImageGen when none is exposed.
2. Store the receipt and output digest with the candidate, then compare it to current *required* generation inputs. If any semantic input differs, set `STALE_SPEC` or `STALE_REFERENCE` and **block approval**, even if `review_checks` says `identity_match=true` and the copied target bytes equal the candidate. A revised explicit owner decision can authorize a documented non-independence-violating deviation; no waiver may import v5 plates/audio.
3. Enforce **approved-reference-only** before image generation: any `.review/` path, missing target, unapproved parent, outdated hash, forbidden version, or role/order mismatch is a hard stop. Do not permit an ID/path split where `id` resolves to a currently approved target but `result.ordered_references` proves the generation used a different candidate.
4. Make `image_handoff.py audit` have two deliberate modes: `--report` for informative inventory and `--strict` for readiness. `--strict` returns **nonzero** on stale, missing, cycle, invalid provenance or unapproved dependencies. Do not cause a report-only command to silently imply readiness by printing problems and exiting 0.
5. Derive numerical fractions from traceable coordinates/boxes on the **actual inspected image**, not from arbitrary hand-written `review_checks.measured_size` values. Treat the dimension measurement as provisional until a human verifies that the bbox includes ears, paws, tail and visible support and that the actor is at the declared depth plane. Require confidence/evidence locator for manual points.
6. Do **not** implicitly migrate existing 54 approvals; preserve original and reconciled spec fields in history. Mark any now-disallowed plate/prop approval stale first. Require new signed review for changed roots; a legacy approval must never satisfy the new provenance gate solely because someone re-hashed the current prompt.

**Acceptance:** inject wrong submitted prompt, changed reference order, changed reference SHA, `.review` parent, copied earlier-version asset, missing image, fabricated numeric value and altered canonical: every fixture fails *at the appropriate gate*. A valid native fixture with immutable evidence, real candidate hash and owner review passes. **Rollback:** switch receipt validator only in new-test sandbox until migration/owner review is ready; never weaken it to accommodate invalid active data.

### 7.4 Phase D — remove v5-derived foundations by versioned replacement, not in-place overwrite

**Role:** owner + creative/image engineer. **Findings:** CONS-001, 006, 009. **Requires a separate generation authorization.**

1. Create an owner-reviewed v6 scene visual brief using the current **v6** character canonicals, identity/style rules, narrative geography, and new independent design choices. A forest may contain trees and rocks; it must not be edited from or modeled by attaching a prior v5 plate, and no previous-version prop/reference may be used as the generation source.
2. Generate **10 independently authored v6 location plates** and **two v6 props**. Treat the trap net as a structural object with recorded attachment, drape, biteable strand, cut point and post-release state, not a decorative overlay. Capture genuine generation receipts for every image and the physically delivered bytes. This is an explicit future task, **not performed in this audit**.
3. Inspect original-size and standardized delivery-size plates for fixed landmarks, sky/horizon and lighting coherence **within v6**; select an independent v6 geometry baseline, then update `visual_bible.json` landmark/camera/support data to match the selected art where justified. A newly generated plate need not coincide pixel-for-pixel with v5's earlier layout. Freeze approved native plate hashes before making dependent scene images.
4. Assign **new revisions or immutable asset IDs** to replacements. Do not overwrite `..._r02.png` and leave the old approval ledger apparently valid; mark older v6 copy invalidated, preserve a nonproduction historical receipt for audit evidence, update `images[].target`, ordered references and generated prompts, and retire the old active v6 file/path only after a backup and dependent graph check. **Never delete v5's historical copy.**
5. Recompute the entire 113-record scene dependency closure. Mark all 42 preexisting candidates invalid for the newly independent source inputs; they may be kept as clearly tagged stale provenance in a controlled archive, but **never as seed/edit-base/approval candidates**. Regenerate current-prompt reading copies; do not reset signed old review dates in place.

**Acceptance:** twelve original copy roots are no longer active; every approved v6 foundation has real own-version receipt and owner review; scan reports zero content-identical copies to forbidden earlier story artwork; no unresolved foreign reference edges. **Rollback:** restore prior recipe documentation in an audit archive, not the forbidden copies into active v6 production.

### 7.5 Phase E — approve the 11 size anchors and rebuild the 113 scene-frame graph

**Role:** image generator + independent visual reviewer + owner for final acceptance. **Findings:** CONS-002, 003, 006, 007, 016. **Only after** Phase D native foundations are approved.

1. Freeze a graph of `image id → all ordered parent id/hash/role`, detect nonexistent IDs and cycles; build a topological queue. Resolve the eight scene backward-first-use edges in §6.4, replacing improper future emotional/world-state references with approved earlier v6 data. Film order remains a separate editorial property.
2. In the queue, build each required **sharp setup anchor** first, unless the setup declares an explicit owner-reviewed **bootstrap** sequence; generate those bootstrap records from approved native plates/canonicals and numeric v6 size rules, not an unapproved future anchor. Compare the actual scene against the native setup plate before approval.
3. Required sharp anchors, exact IDs from current bible: `stream_afternoon_wide → s01_milo_at_edge`; `stream_sunset_wide → s02_notice_start`; `fork_wide → s03_milo_at_fork_edge`; `shortcut_run → s04_shortcut_run_start`; `tree_dusk_wide → s05_paw_contact_start`; `tree_dusk_contact → s05_nose_aftermath_start`; `home_night_wide → s09_home_start`; `trap_wide → s13_arrives_start`; `trap_bite → s14_milo_holds_rope`; `forest_run → s12_hears_start`; `tree_day_wide → s16_friends_start`.
4. Bootstrap caveat: `tree_dusk_wide` currently names `s05_leo_sleeps_start/end` as bootstrap records and `trap_wide` names earlier `s10_*` and `s11_*` single-character states. These require **numeric-size and ground-support visual approval** before the later two-actor setup anchor exists. Do not bypass reference approval merely because the image is called a bootstrap.
5. For each scene endpoint: run the current manifest `build --check`, `lint`, and `image_handoff check <id>`; verify **all ordered references are approved exact native v6 files**. Generate one candidate using those exact ordered bytes; save immutable receipt; review at native resolution and 1280×720; compare identity, original plate landmarks, measured silhouette, depth and support, occlusion and prop state. Copy the exact reviewed PNG to its revisioned manifest target only after it passes, then run `check <id> --for-approval` and human approval. Repeat in the dependency graph order, never from an unapproved output.
6. Create closed-mouth paired endpoints and separate `_open` mouth calibrations where specified. An open image must be a focused edit of its *approved* closed-frame version and must not become a chain start/end. Generate only new v6 images; do not reuse v5 render endpoints or accidentally accept duplicated actor body parts.
7. Review joins with neighbouring frames, including the non-image chain semantics (camera change, entrance/exit direction, grounded feet, acorn's single-object trajectory and net state). If a defect is found, reject it and invalidate descendants first; repair with a new revision and re-review all consumers.

**Acceptance:** all **113** v6 scene image records have native current-byte approvals, all **11** anchors have measured reviewer-confirmed geometry, all `.review` references are absent from generation receipts, no nonv6 PNG hashes are accepted, and both endpoints plus 37 mouth calibrations where required are approved for their uses. Every image's reviewer evidence is present, not a programmatic auto-pass. **Rollback:** mark outputs stale and return to a previous approved native root; never promote historical candidates as a fast workaround.

### 7.6 Phase F — produce and validate genuinely v6-owned narration and timing

**Role:** owner/audio engineer + timing/linguistic reviewer. **Findings:** CONS-005, 024, 025. **Separate audio-generation authorization is required.**

1. Freeze the exact **161 v6 line IDs, text and speaker labels** from the approved `SCRIPT.md`/`dialogue_coverage.json`, including any deliberate line splits; choose v6-owned voices and performance directions. Do not copy/symlink/retime v5 WAVs to make them look v6-native.
2. Produce or import separately authorized original v6 recordings. Put exact line WAVs and scene WAVs under the v6-local audio root, then capture SHA-256, sample rate, sample format, channels and measured duration per line. Verify all 16 final scene WAVs, no missing IDs, no duplicate/foreign files and all planned pauses/tails.
3. Validate the new `timing.json` against line list using `production/chain_plan.py --story lion_and_mouse_v6 --audio-story lion_and_mouse_v6 check` **before** any write-generating `apply`. If durations differ from 683.67 s (very possible), adjust shot splits, frame count and speeds within the supported range, then recalculate `timing_plan.json`, `TIMING_SHEET.md`, and shot-variant frames under an authorized update. Rerun full image/prompt dependencies when new edits would change endpoint semantics.
4. Force-align **v6 WAV bytes to v6 transcript**, save `word_timings.json` under v6 only; flag unsupported/uncertain word timings for a human reviewer. `NARRATOR` lines stay voice-over and never drive visible character mouth motion. Distinguish a multi-piece line's actual within-line intervals; do not infer boundaries solely from the `candidate_coverage_shots` list.
5. Re-run metadata gates: all line IDs covered, no time gaps/overlaps after edit retime, exactly one explicit speaker for mouth variants, no obsolete v5 path/string in executable audio records. Freeze an audio/timing bundle digest for both Mac and LUMI.

**Acceptance:** actual v6 audio hashes, `timing.json`, word timings, script/transcript and current manifest match; full narration duration equals the accepted timed film plan to the specified frame tolerance; 37 mouth pieces have eligible speaker words. **Rollback:** keep previous v6 candidate recordings tagged rejected, not as final; regenerate derived timing only from the newly approved line versions.

### 7.7 Phase G — fix portable validation, joining, selection and media provenance

**Role:** Python/media engineer. **Findings:** CONS-010, 011, 012, 014, 019, 022, 026, 033, 034.

1. Correct `chain_preview.py` join-sheet conversion by consistently converting float32 RGB arrays to clipped uint8 before constructing Pillow RGB images. For each chain join, compare **previous piece's last output frame** to current piece's **first** output frame; ensure the stored sheet and numeric `jump` metric refer to exactly the same pair. The current variable `out_frames[-1]` is the current piece's last frame, *not* the earlier piece's last.
2. Add `--strict-joins` (or equivalent) with an owner-configured threshold and acceptance record. A flagged or unreviewed join must stop pilot acceptance; provide a documented override only for a reviewed intentional cut/dissolve, never for a nominal `chain` join without evidence.
3. Strengthen take selection: every `.mp4` must have a matching sidecar/receipt for exact story, manifest variant, approved endpoint hashes, prompt, model/LoRA, seed, render settings, decoded frame count and source SHA. Put one portable content-based selection receipt in `takes.yaml` or a companion JSON; never accept a clip merely because a `best_` filename, integer seed or external `takes.yaml` path happens to resolve.
4. Change `feltwillow/lipsync.py:45-51` to hash canonical logical paths + file bytes and stable semantic recipe JSON, not `Path.resolve()` absolute strings. Change `resolve_synced_take` to use SHA-256 of source/output, not the current absolute path equality or nanosecond mtimes as authenticity requirements. Size/mtime can remain **non-authoritative local performance hints**; moved unchanged files must remain valid after verifying bytes and recipe. Mismatched audio/timing/word/closed-open images must still invalidate.
5. Replace absolute `source_file`/`audio_file` in portable edit/handoff receipts with logical story-relative locators and hashes. Resolve the actual storage path on each machine using `feltwillow.paths.WORK` and a deliberately configured media root. Refuse a resolved path that escapes the authorized story root or points to another version.
6. Refactor LUMI `render_story.sh` to validate existing output sidecars and current approved recipe before deciding a shot is complete. A stale clip must be reported and scheduled only in an authorized render run, never silently re-used or overwritten.
7. Make backup inventory respect `FELTWILLOW_WORK` consistently across Mac and LUMI. Include ignored `.review` candidate ledgers, v6 audio, rendered takes, lip-sync index/output, provenance JSON, selected takes, and edit deliverables, in addition to tracked foundation artwork; separately track files excluded deliberately. Restore from a test backup and compare SHA counts, not simply the rsync exit code.

**Acceptance:** all read-only negative tests in §8 pass, strict join sheets show the correct boundary pair, unchanged media moved from Mac to LUMI retains valid content identity, stale take/media changes are caught, and backup/restore matches the inventory. **Rollback:** disable new production export until verification succeeds; do not revert to accepting stale cached media as a workaround.

### 7.8 Phase H — controlled 1–3 scene GPU pilot, then whole-film qualification

**Role:** LUMI render operator + owner/visual reviewer. **Findings:** CONS-006, 019, 028, 032, 033. **Requires separate render authorization** and completion of native image/audio gates.

1. Verify the existing **LUMI Singularity/ROCm container and Python venv** (not a Mac-style Conda environment), model revision/LoRA hashes, GPU availability, Python/ffmpeg/Pillow/NumPy versions, runtime image hashes, seed list, fps and output resolution. Fix the **optional `WITH_CONDA` shell hook** only if the set/unset tests and this particular SIF confirm a defect; capture executable digests. Use `lumi/run_in_container.sh` from the intended repo commit; do not create an ad hoc LUMI Conda environment or re-install packages between pilot takes.
2. Pilot only scenes **1–3**, covering roughly the first **103.66 s** at the currently *provisional* timing revision; recompute window after finalized v6 audio. Export runtime only for those scenes with current approval-bound endpoints. Exercise `production/shot.py --dry-run` for every pilot variant before submitting any GPU job; no scene with missing inputs may reach `sbatch`.
3. Generate/read a **stills-only** preview using native approved scene frames and the final v6 audio before any GPU time. Review film timing, visible actor scale, cuts, start/end image joins and action feasibility. No grey placeholder card may be accepted as proof of a reviewed scene.
4. Render a bounded number of seed takes for first scenes (not the complete 154-piece batch). Verify each sidecar against exact current inputs, inspect every take's first/middle/last frames, repeated-frame behaviour, limb/paw counts, camera/plate continuity, net/prop physical states where applicable, and actual encoded frame count. If a wrong take appears, quarantine it; never rename it to `best_` as a workaround.
5. Have the owner explicitly select takes, record content-bound selection receipts, then run strict selected-take chain preview and owner-review every flagged join. Verify lip-sync on speaking pilot pieces from final v6 word timings, keeping silent/narrator intervals closed and endpoint poses unchanged. Apply repairs only as new versioned takes.
6. Only after the pilot meets all gates, repeat the same procedure scene by scene through scene 16 and produce a final edit handoff. Each future scene must be tested against previous scene's ending and the physical world-state timeline. Never run a bulk job simply because metadata counts equal 154.

**Acceptance:** a scene-by-scene signed visual ledger, exact source/render/take SHA chain, strict successful joins, v6-local audio, no cross-version inputs, full duration/word attribution and independent reproducible validation on Mac/LUMI. The presence of 154 `.mp4` files is **not sufficient** for acceptance.

### 7.9 Phase I — institute regression CI and portable acceptance fixtures

**Role:** shared-toolchain/QA owner. **Findings:** CONS-008, 021, 023, 026, 027. **Files:** new `tests/test_image_provenance.py`, `tests/test_v6_isolation.py`, `tests/test_chain_preview_joins.py`, `tests/test_portable_lipsync.py`, `tests/test_docs_manifest_parity.py`, `tests/test_render_receipts.py`, optional `production/preflight.py`, CI workflow and fixtures. Test filenames are **proposals**, not currently tracked files.

1. Define a small, legally shareable/test-safe image/audio fixture packet with its own v6-style fictional story slug (avoid production or personally recorded voice bytes), canonical PNGs, 2 frames, one speaker line, one video clip/sidecar, deliberate mismatches and expected error codes. Include canonical JSON fixtures with no absolute machine path.
2. Add pure, deterministic unit tests for version policy, DAG ordering, prompt/ref generation receipts, approval fail-closed behaviour, numeric/visual-review annotations, SHA invalidation, line-to-speaker mapping, crossfade boundary rendering and content-addressed lip-sync identity. Include a **fresh** independent story and an explicit **legacy** story fixture to prevent regressions in v5/other stories.
3. Add CI on pull request: JSON schema, source/manifest integrity, doc parity, independent-story path and hash scan, `image_prompts build --check`, `lint`, strict preflight and Python tests. Keep GPU renders outside CI; provide owner-reviewed manual quality gates as signed external artifacts.
4. Run the *same* golden image/audio/approval fixture through the Mac and LUMI validators. Produce normalized, sorted JSON decision/measurement output with stable algorithm+schema versions and verify equality. Test a one-pixel image change, moving the identical files to another absolute directory, renaming a source file without changing its logical ID, and changing a semantic prompt/reference role.
5. Pin separate environment sources (**MacBook** Conda lock or explicit Mac packages; **LUMI** Singularity SIF digest + Python venv lock, ffmpeg and image measurement code). Do not assume or introduce a Mac Conda interpreter on LUMI. Differences in numerical measurement due to decoder/resize versions must be reported and resolved **before** a new toolchain is production-approved. The image/video generation models may be stochastic; compare validated **saved artifact bytes and decisions**, not expected pixel-identical generation across hardware.

**Acceptance:** tests run nonmutating in a clean checkout; negative fixtures fail for deliberate violations; Mac/LUMI signed report digests are equal for identical inputs; a changed actual content byte invalidates old approval; CI blocks contradictory active v6 documentation. **Rollback:** do not merge a replacement gate unless both machine fixtures pass. Historical story exceptions must be explicit and remain fenced to their own versions.

### 7.10 Deletion/retirement decision register (authorization required)

The instruction to “delete everything that clashes” must be interpreted as **remove conflicting active authority and disallow invalid sources**, not to erase historical evidence or destroy work before backups. Use the following register to authorize precise changes:

| What | Recommended future action | What not to delete | Gate before retiring |
|---|---|---|---|
| 12 copied v6 plate/prop `r02` active files | **Replace with genuinely native versioned v6 assets**; remove the copied files from the active v6 set after descendants and approvals are migrated | v5 originals, old immutable audit receipts, unrelated story assets | New owner-approved roots, full SHA inventory, transitive-dependency update, successful restore test |
| 42 unapproved v6 `.review/` candidates and generation data | Mark **stale/nonproduction** and archive or delete candidate PNGs *only after* the owner approves a retention policy and hashes are backed up | Immutable generated-prompt/actual-ref metadata needed to explain failures | Native root and new-prompt regression tests pass; backup verified |
| 54 reconciled approval entries | Preserve historical owner decisions; invalidate **only those no longer admissible or whose spec changed** and issue new signed receipts when justified | Original reviewed-by/at, previous hashes, owner notes | Fresh spec+reference+pixel/visual checks; no auto-rebinding |
| Obsolete active v5/v4 references in v6 docs | Delete/replace active instructions with version-specific policy and generated links | Clearly labeled history and lessons not used as current v6 input | Read-only doc scan and independent-version tests return zero conflicts |
| Stale timing/shot-plan filename tables | Replace regenerated *current views* and add invariant tests | Story text, shot/line identities, audit history | 154 timing row and 33 register comparisons yield zero mismatch |
| Legacy v5 build fallback code | Fence behind legacy story policy or deprecate after migration | Current v5 production data and needed story-specific tooling | V5 behavior tested; v6 cannot call it to inherit assets |
| Stale/wrong cached MP4s and sync outputs | Quarantine and version, then rerender only under separate instruction | Signed selection records, render sidecars and diagnostic evidence | Content-recipe mismatch report, owner repair authorization and backup |
| Root `.DS_Store`, stale historical links, doubled extensions | Git hygiene/removal from active new workflows | Valid old linked content without owner decision | New-story tests pass and historic refs remain traceable |

### 7.11 Task closure receipt required for every delegated agent

Each future work item must finish with a short Markdown/JSON completion record: `task_id`, `finding_ids`, `start_HEAD`, `end_HEAD`, `files_changed`, `files_retired`, `old/new_sha256`, `dependency_graph_before_after`, `tests_attempted_with_exit_codes`, `fixture_and_machine_identity`, `human_visual_evidence`, `remaining_blockers`, and `rollback_instructions`. A task is **not complete** if the code is changed but its docs, dependent approvals, test fixtures, portable transfer manifest, and downstream hash invalidations have not been reconciled. The reviewer must independently sign off on changes to identity, native plates, scale rules or world-state continuity.

## 8. Command and test log, platform runbook, and unresolved evidence

### 8.1 Exact audit commands and results — what ran versus what did not

This section prevents future agents from confusing a structural/connector inspection with a successful production test. `GitHub API success` means the tracked source or metadata was actually fetched and parsed. `NOT RUN` means **no** exit code exists; it must not be reported as `0`. The audit was limited to the branch snapshot and local isolated reproductions. No owner media were rendered, generated, altered or deleted.

| Probe | Environment and observed result | Status and meaning |
|---|---|---|
| `GET /repos/jeilealr/feltwillow-production/branches/working-cloud-branch` | GitHub connector returned `eac8d388639e6053113b071d7f3e08f3a0cac353` (commit timestamp 2026-10-10T19:18:37Z) | **PASS** — branch snapshot pinned, not proof the Mac checkout has the same HEAD |
| `GET /git/trees/working-cloud-branch?recursive=1` | GitHub connector parsed 975 entries, 774 blobs; no truncation was reported | **PASS** — committed tree inventory |
| `GET /git/blobs/02f00af1b2926d7e85593e27278e3d345165d864` | Connector parsed 2,851,000+ characters of v6 `prompt_manifest.json` | **PASS** — full active v6 manifest inspected, not a truncated `fetch_file` response |
| JSON-based v6 row/approval/reference/shot inspection | 167 unique images; 54 accepted, 42 candidates, 71 planned; 154 shots, 161 coverage lines, 11 unapproved sharp anchors | **PASS** — tracked metadata only; pixel and human-approval meaning still require verification |
| Candidate actual-submission versus live spec/reference comparison | 42 of 42 different prompt strings, 35 of 42 different recorded reference arrays, 35 of 42 generated using `.review` references | **FAIL** — confirmed provenance defects; CONS-002/003/004 |
| Tracked v5-v6 image Git-object intersection | Twelve cross-version identical Git blob IDs: 10 plates + 2 props; see §6.1 | **FAIL** — confirmed native-content independence violation; CONS-001 |
| V6 timing plan versus live manifest and dialogue coverage | 154/154 shot/variant/mode/frame identities matched; 161/161 lines covered; 0 nominal chain endpoint gaps; 683.67 seconds saved plan | **METADATA PASS** — audio and clip bytes **not** checked |
| `TIMING_SHEET.md` filename-pair comparison | 121/154 rows disagree with the manifest | **FAIL** — confirmed active handoff drift; CONS-031 |
| `SHOT_PLAN.md` image-register comparison | 33/33 registered filenames disagree with manifest targets | **FAIL** — confirmed active handoff drift; CONS-031 |
| `timeout 12s git ls-remote https://github.com/jeilealr/feltwillow-production.git refs/heads/working-cloud-branch` | Hosted container `git`: `Could not resolve host: github.com`, exit **128** | **BLOCKED** — cannot obtain local repository checkout or invoke native repository scripts |
| Attempt to fetch a PNG via GitHub connector | Binary blob decode rejected with `UnicodeDecodeError` on PNG header | **BLOCKED** — 0 actual v6 image pixels independently viewed/measured |
| `python3 -V`; import Pillow/NumPy/PyYAML/pytest | Hosted test shell: Python **3.13.5**, Pillow **12.3.0**, NumPy **2.3.5**, PyYAML **6.0.3**, pytest **9.0.2** | **PASS** — hosted tools, **not** the Mac or LUMI production environment |
| Isolated missing-hook shell reproduction | `bash -c 'set -euo pipefail; unset WITH_CONDA; $WITH_CONDA'` => `WITH_CONDA: unbound variable`, exit **1** | **FAIL by design** — confirms conditional shell error; does **not** establish the hook is missing on actual LUMI |
| Isolated join-image dtype reproduction | `PIL.Image.fromarray(np.zeros((216,384,3),dtype=np.float32))` => `TypeError: Cannot handle this data type: (1, 1, 3), <f4`; converting to `uint8` succeeds | **FAIL by design** — reproduces incompatible image-array conversion; CONS-010 |
| `python production/image_prompts.py --story lion_and_mouse_v6 build --check` | No checkout containing the script and its imports | **NOT RUN** — obtain checkout then run on Mac/LUMI, record exit and changed-field count |
| `python production/image_prompts.py --story lion_and_mouse_v6 lint` | No checkout containing script and manifest | **NOT RUN** — do not claim zero errors/warnings |
| `python production/image_handoff.py --story lion_and_mouse_v6 audit` | No checkout containing script/images | **NOT RUN** — when run, parse reported problems as well as process status; current code returns success even after printing issues |
| `python -m unittest discover -s tests -v` | No checkout | **NOT RUN** — speaker tests and future remediation regression suite outstanding |
| Read/measure original PNGs, `.review` candidates and final 1280x720 images | Binary assets/ignored files not mounted | **NOT RUN** — visual and scale signoff remains with owner/authorized reviewer |
| Read/probe v6 WAVs, word alignment, Slurm renders, takes and edit | Remote ignored `work/` not accessible | **NOT RUN** — no inference of motion, audio, voice or visual continuity |
| Actual MacBook-vs-LUMI parity run | Neither user's Mac environment nor LUMI Slurm/container session was accessible | **NOT RUN** — acceptance requirement remains open |

To independently reproduce the **two isolated, non-production tests** in a shell (no repository writes):

```bash
python3 - <<'PY'
import numpy as np
from PIL import Image
x = np.zeros((216, 384, 3), dtype=np.float32)
try:
    Image.fromarray(x)
except TypeError as exc:
    print('EXPECTED FLOAT RGB FAILURE:', exc)
else:
    raise SystemExit('Unexpected: float32 RGB was accepted')
Image.fromarray(np.clip(x, 0, 255).astype(np.uint8))
print('PASS: explicit RGB uint8 conversion works')
PY

# Deliberately trigger the optional variable problem without calling LUMI:
bash -c 'set -euo pipefail; unset WITH_CONDA; $WITH_CONDA'
# Expected nonzero exit with: WITH_CONDA: unbound variable
```

**Do not** interpret the second command's nonzero exit as a reason to install or activate Conda on LUMI. This tests unsafe optional-shell-variable expansion only.

### 8.2 Read-only commands to repeat in the MacBook's existing environment

MacBook setup is separate from LUMI. Use the **existing** locally configured Conda environment; the name below is an example from the repository instructions. If the real environment has a different name, substitute it. Do not create/reinstall an environment merely to satisfy an audit command.

```bash
cd /path/to/feltwillow-production

git branch --show-current
git rev-parse HEAD
git status --short
python3 --version
conda env list

# Use the already working Mac environment. Check it before assuming a name.
conda run -n feltwillow python -V
conda run -n feltwillow python production/image_prompts.py --story lion_and_mouse_v6 build --check
conda run -n feltwillow python production/image_prompts.py --story lion_and_mouse_v6 lint
conda run -n feltwillow python production/image_handoff.py --story lion_and_mouse_v6 audit
conda run -n feltwillow python production/image_handoff.py --story lion_and_mouse_v6 check s01_milo_at_edge
conda run -n feltwillow python -m unittest discover -s tests -v

git status --short
```

**Rules for recording results:** note Mac architecture, OS version, Conda environment prefix and Python version; log stdout/stderr and numerical findings alongside exit codes. These are read-only `--check`/`lint`/`audit`/`check` calls and tests; if the named tests unexpectedly write outside a temporary directory, stop and investigate before running them against valuable local data. `image_handoff audit` currently returning exit 0 must **not** count as a clean gate if it prints approval problems. `check s01_milo_at_edge` only validates declared prerequisites: it does not make a new image or approve any file. Check `git status` afterward. Do **not** run `build` without `--check`, `md`, `approve`, `chain_plan apply`, `export_runtime`, `shot.py` or image generation during this audit.

A portable dependency/provenance spot-check (run in either already-working Python environment) can be performed without producing output files:

```bash
python - <<'PY'
import hashlib, json
from pathlib import Path
repo = Path.cwd()
folder = repo / 'stories/lion_and_mouse_v6'
man = json.loads((folder / 'prompt_manifest.json').read_text())
images = {r['id']: r for r in man['images']}
assert len(images) == len(man['images']) == 167
assert len(man['shots']) == 154
candidates = [r for r in man['images'] if r['status'] == 'candidate']
print('candidate count:', len(candidates))
print('submitted prompt != active prompt:', sum(
    (r.get('result') or {}).get('submitted_positive') != r.get('positive_prompt')
    for r in candidates))
print('submitted reference entries differ:', sum(
    [tuple(x.get(k) for k in ('id','role','path'))
     for x in (r.get('result') or {}).get('ordered_references', [])]
    != [tuple(x.get(k) for k in ('id','role','path'))
        for x in r.get('ordered_references', [])]
    for r in candidates))
print('generated with review ref:', sum(
    any('/.review/' in x.get('path','') for x in
        (r.get('result') or {}).get('ordered_references', []))
    for r in candidates))
# Compare actual bytes, not just names, when files are present.
for slug in ('lion_and_mouse_v5','lion_and_mouse_v6'):
    roots = [repo/'character/characters'/slug, repo/'character/locations'/slug]
    paths = [p for rt in roots for p in rt.rglob('*.png') if p.is_file()]
    print(slug, 'local PNG count:', len(paths))
PY
```

This code **reports** the data; it does not automatically sign off artwork. The expected committed snapshot counts are `42`, `42`, `35`, `35`, while local ignored working files may add files beyond Git's tracked inventory. On a future commit, expected counts must be recomputed and documented rather than hardcoded as acceptable.

### 8.3 Do not conflate a clean v6 JSON check with a clean visual gate

A future agent must produce separate evidence for each layer, in this order: (1) manifest/schema/path/version consistency; (2) actual submitted generation prompt and all ordered reference **hashes**, with v6-native provenance; (3) source PNG bytes, image dimensions and canonical/plate comparison; (4) human anatomical/prop/contact/scale review against the frozen v6 criteria; (5) approval receipt; (6) video take receipt and decoded frames; (7) timing/audio/word alignment; (8) selection/join/lip-sync/edit receipts. Each layer must fail closed if upstream data changed. Successful lint cannot turn a `candidate` into `accepted`.

### 8.4 Read-only LUMI runbook — **Singularity + existing scratch Python venv; NO Mac Conda**

This is the critical platform distinction confirmed by the owner. The established LUMI entrypoint in the tracked source is `lumi/run_in_container.sh`, which sources `lumi/site.sh`, uses `singularity exec -B "$FELTWILLOW_BINDS" "$FELTWILLOW_SIF" ...`, then sources `lumi/env.sh`; the latter activates `$FELTWILLOW_VENV_GEN/bin/activate`. `lumi/setup_env.sh` **creates a Python venv** using `python -m venv --system-site-packages`. `FELTWILLOW_VENV_GEN` is currently a legacy-named `.../ltx_env/venv` directory on scratch and is **not** a Conda environment. `WITH_CONDA` is an optional internal startup hook, not a directive to create a separate LUMI Conda env. Do not run `conda create`/`conda activate feltwillow` on LUMI.

The following commands only inspect the environment that has **already** worked for prior LUMI renders. Run them from the existing LUMI checkout, not a recreated test installation:

```bash
cd /path/to/the/existing/lumi/feltwillow-production

git branch --show-current
git rev-parse HEAD
git status --short
source lumi/site.sh
printf 'repo=%s\nproject=%s\ncontainer=%s\nvenv=%s\n' \
  "$FELTWILLOW_REPO" "$FELTWILLOW_PROJECT" "$FELTWILLOW_SIF" "$FELTWILLOW_VENV_GEN"
test -f "$FELTWILLOW_SIF"
test -x "$FELTWILLOW_VENV_GEN/bin/python"

# This invokes the existing image and Python venv; it does NOT initialize Conda on LUMI.
lumi/run_in_container.sh python - <<'PY'
import sys, importlib.metadata as md
print('interpreter:', sys.executable)
print('Python:', sys.version)
for package in ('torch', 'diffusers', 'transformers', 'numpy', 'Pillow', 'PyYAML'):
    try:
        print(package, md.version(package))
    except md.PackageNotFoundError:
        print(package, 'MISSING')
import torch
print('PyTorch import:', torch.__version__)
PY

lumi/run_in_container.sh python production/image_prompts.py --story lion_and_mouse_v6 build --check
lumi/run_in_container.sh python production/image_prompts.py --story lion_and_mouse_v6 lint
lumi/run_in_container.sh python production/image_handoff.py --story lion_and_mouse_v6 audit
lumi/run_in_container.sh python production/image_handoff.py --story lion_and_mouse_v6 check s01_milo_at_edge
lumi/run_in_container.sh python -m unittest discover -s tests -v

git status --short
```

If a command fails at the container or interpreter stage, **inspect the error first**: missing Slurm/module/container access, missing scratch venv, missing bind mount and optional container hook are different problems. The existing working venv/ROCm image must not be replaced just because a Mac-specific tool suggests Conda. If `WITH_CONDA` is unset, investigate whether the pinned SIF's Python/PyTorch actually need an internal hook; only then choose to remove it or guard it in future authorized code changes. Do not run `lumi/setup_env.sh` as an audit step: it creates/updates packages and is **mutating**. Running on a LUMI GPU compute node is optional for CPU lint but mandatory later for authorized real rendering tests.

**Cross-machine meaning:** the paths to binaries, scratch storage, caches and Conda/venv installations can differ. The **logical v6 asset identity** (version ID, relative path, SHA-256 of bytes, image review measurements, immutable prompt/reference receipt, required authorizations) and the validation verdict must not differ. If there is a difference, fix the validator or pinned dependencies, not the asset by silently moving its ground line or altering the canonical to make a check pass.

### 8.5 Portability fixture protocol: exact equality claims agents must test

1. Build a **test-only** small story fixture under a temporary test directory, not `stories/lion_and_mouse_v6/`: a synthetic plate, independent synthetic canonical, one two-frame pair, approved reference/hash records, a short *nonpersonal* WAV, one dummy correct-length MP4 and one take receipt. Give it a unique story slug and no real production approvals.
2. Create one **canonical fixture manifest**: relative POSIX-style asset paths, sorted explicit reference arrays that preserve semantic order, SHA-256 of each media blob, canonical JSON digest, schema revision, size boxes measured in normalized 0–1 coordinates, closed-mouth speaker identity, clip dimensions/fps/frame count and expected pass/fail codes. Use no absolute pathname or modification time in the receipt digest.
3. On Mac, run inspection under the **existing local Conda environment**. On LUMI, run the same fixture under the **existing Singularity + Python venv**. Collect tool versions; re-read the fixture files after copying and compare raw SHA-256 before comparing reports.
4. Compare both **sorted machine-normalized JSON** reports byte-for-byte after excluding declared nonsemantic host identity (`host`, `absolute_root`, `mtime`, `log_time`). Fail on mismatches in `accepted`, errors, measured bounding boxes, reference order, file hashes, decoded frames, speaker and shot timing. If decoders give slightly different numerical results, pin their versions or explicitly standardize the image normalization algorithm and record its version; never widen tolerances silently.
5. For negative controls on **both** platforms: change one pixel; change an image without changing path; preserve bytes while moving to a different absolute root; switch reference order; replace an approved reference with `.review` path; change prompt text; copy a previous-version plate to a new v6 path; supply an unsupported ground; swap Milo/Leo speaker; change one WAV byte; change selected take's sidecar; supply a wrong-length take; change a video frame at a chain join. Every such fixture must produce the **same expected fail-closed error** on both systems, and moved identical media must retain valid content-based identity.
6. Record a signed comparability receipt with branch commit, logical fixture ID, all input SHA-256 digests, validation code digest, codec/tool versions, Mac results, LUMI results, pass/fail delta and owner/reviewer. A native v6 plate still needs visual owner review: parity of automatic checks does not establish that a model drew the correct felt lion or mouse.

**Important reproducibility boundary:** image-generation tools and Wan video inference may be nondeterministic across GPUs, driver versions and implementations even for equal seeds and prompts. The hard invariant is that **every saved output is independently judged using the same identity/plate/size/anatomy/prop and approval rules on either machine**, not that two generators necessarily produce pixel-identical artwork.

### 8.6 LUMI-only facts and artifacts the next agent must collect before claiming production readiness

| Required evidence | Current state at audited commit | Operator action (read-only unless explicitly authorized) |
|---|---|---|
| `work/stories/lion_and_mouse_v6/audio/en/timing.json`, `lines/*.wav`, `sceneNN.wav`, `word_timings.json` | Ignored/unavailable via Git; plan provisional | Inventory actual LUMI scratch/other backup files with logical paths, file sizes, duration and SHA; distinguish v6-authored from renamed v5 audio |
| 42 `.review/` candidate PNGs, generated sources and saved contact sheets | Generation result metadata exists; candidate bytes ignored and unavailable | Read-only inventory and checksum by record ID; do **not** use as approved references; compare against source/candidate hashes and current requirements |
| 54 tracked accepted foundation PNGs | Git file names/blobs known; no pixels checked | Recompute local SHA-256 against approval JSON, inspect canonical/poses/expressions, classify 12 copied plates/props inadmissible until replaced |
| All 11 sharp setup anchors | `planned`; not approved | Generate only in later authorized independent-v6 work, save real measurements and owner signoff, then approve with hardened receipt checks |
| Any v6 runtime `story.yaml` and `runtime_inputs.json` | Not tracked at HEAD; current stage incomplete | If present on LUMI, treat as out-of-band, verify version, input digests, creation commit and status before any use |
| Rendered fast/nonfast MP4s, JSON sidecars, `takes.yaml`, repair overrides | Not tracked at HEAD; no selected v6 take in manifest | Inventory actual media and hash sidecars; reject correct-filename/wrong-recipe takes; no automatic GPU render as audit |
| Lip-sync manifest, speaker alignment and `edit_manifest.json` | Missing from tracked v6 snapshot | Verify v6-local narration and reference hashes; remove machine-specific cache identity; confirm narrator does not animate mouths |
| LUMI `.sif`, Python venv and run environment | Code paths known; actual session not accessed | Inspect current working SIF/venv/imports; record exact versions; do **not** build a Mac-style Conda environment on LUMI |
| Backup/restoration of Git-ignored assets | Not performed | Verify inventory against a separate backed-up copy including `.review`, audio, takes, provenance and edit outputs; capture SHA equality and restore results |
| Actual image/video QA | **0 images and 0 video frames viewed in this audit** | Explicit authorized human review on image pixels and decoded video. Record each tested image/take ID and timestamp, or mark `UNVIEWED` |

### 8.7 Open questions and rules for resolving them (without guesswork)

**Questions answered by latest owner requirements:** v6 must not use *any* older-version creative media as its active input; the same validated artifact must receive the same consistency/inspection verdict on Mac and LUMI; contradictory *active* instructions are to be retired. **LUMI does not use the Mac Conda environment**. These must **not** be sent back to the owner as repetitive clarification requests.

**Evidence the agent must obtain from filesystem/operator access:** (a) Does the current LUMI checkout match HEAD `eac8d388`? (b) Are the 42 ignored candidate images present and backed up? (c) Is v6 narration really absent, or present only in separate LUMI/backup storage? (d) Which `FELTWILLOW_WORK` root is active on each device? (e) Which exact Singularity image and scratch venv have worked for previous LUMI videos? (f) Does the container provide `WITH_CONDA` internally, or is it a stale hook? (g) Do candidate source SHA-256 hashes actually match their files? (h) Have any true v6 video takes been created outside Git despite missing local manifests? Record results with commands, paths, hashes and exit codes, **without changing** production state.

**Decisions that genuinely require the owner:** (1) review and approve newly created, genuinely v6-native plate/prop appearances and redesigned landmarks; (2) authorize, separately, generation of the native foundations and downstream stills; (3) authorize independent v6 narration recording/voice selection and final timing; (4) sign off on pilot clips, repaired joins and selected takes; (5) authorize retirement or destruction of backed-up stale candidate PNGs. Agents must not use a historical `accepted` flag to infer any of these decisions.

## 9. Explicit go/no-go matrix at snapshot HEAD

| Operation | Current verdict | Findings / minimum release evidence |
|---|---|---|
| **Read-only audit, code review and temporary fixture tests** | **GO** | No production writes; preserve baseline, record exact exit status and provenance (§8, CONS-021) |
| **Create genuinely independent replacement v6 plates and props** | **NOT AUTHORIZED BY THIS AUDIT** | Next production phase may proceed only with **separate owner authorization**, a frozen native design and plan, saved outputs/receipts, a fresh owner review and prior backup; never derive from v5 (CONS-001, CONS-009) |
| **Generate dependent v6 scene stills / mouth calibration images** | **NO-GO** | Native v6 plates/props and their valid approvals first; generation provenance enforcement fixed; previous `.review` dependencies quarantined; topological dependency order; approved size anchors (CONS-001/002/003/004/006/007/016) |
| **Approve any of the 42 existing scene candidates** | **NO-GO** | Their submitted spec/references do not match active manifest and 35 used `.review` sources; 12 shared v5 roots violate independence. Fresh lineage, visual evidence, owner decision and hardened approval required (CONS-001/002/003/004/006/009) |
| **Export v6 pilot runtime / queue scenes 1–3** | **NO-GO** | All used scene endpoints explicitly approved against native v6 assets; v6-local audio and timing checked; runtime story/manifest/image-set identity enforced; current handoff docs agree with manifest (CONS-005/006/013/031) |
| **Run 1–3 scene GPU pilot** | **NO-GO** | Requires separately authorized LUMI renders from new images, verified SIF/venv/recipe, exact closed/open semantics, valid source sidecars, and join review without false/incorrect contact sheets (CONS-005/006/010/011/012/019/032/033) |
| **Render all 154 v6 pieces in bulk** | **NO-GO** | Pilot signed off, **all** endpoint approval receipts valid, independent v6 narration/mouth timing frozen, no false `already complete` MP4s, all hashes/source clips proven, Mac/LUMI validation parity tested (CONS-001/005/006/019/026/028/033) |
| **Select/edit/export full v6 video or publishing handoff** | **NO-GO** | 154 selected validated takes, no flagged unresolved joins, 37 mouth pieces have valid speaker-specific v6 lip-sync, portable and hash-bound edit manifest, matching scene audio/duration; owner final take approvals (CONS-005/011/012/014/019/022/024/026/028) |

**Final authorization boundary:** this report identifies how to correct the system and test it. **It does not authorize deleting legacy records, erasing current review assets, regenerating stills, submitting LUMI Slurm jobs, producing audio or making releases.** Future work must follow §7 task order, keep one authoritative v6 source of truth, explicitly mark unresolved inputs, and produce the task receipt in §7.11. When an agent completes an actual remediation stage, publish a new dated audit against the **new HEAD** rather than quietly altering the evidence attached to this `eac8d388` snapshot.
