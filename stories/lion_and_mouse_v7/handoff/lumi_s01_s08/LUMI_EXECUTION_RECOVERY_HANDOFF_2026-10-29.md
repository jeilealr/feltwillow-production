# Feltwillow V7 S01–S08: LUMI execution diagnosis and next-agent handoff

**Prepared:** 2026-10-29 · **Mac checkout:** `wan-new-image-approach` at `ebff6ee`, clean when inspected.  
**LUMI report supplied by owner:** `/flash/project_465002727/jelealro/video_execution_20261029`, checkout `ebff6ee`. Its host/runtime observations below are **reported by the LUMI agent**, not independently run on LUMI in this Mac session.

## What the production inputs actually are

`INPUT_MAP.json` in this directory is derived from `audio_visual_plan.json` plus current exact-hash scene selection/bindings. It names **53 actual S01–S08 sequences**, **68 line WAVs**, ordered still uses, aliases, cuts, prompts, speaker and three-axis visual classification. `s01_opening` aliases `s01_empty_hold`; render that opening once. The map has 90 selected exact image uses, 13 alias uses and two missing/unselected S01 tiny-bite pickup uses. Its local verifier passed on Mac and, per LUMI's report, passed on LUMI after the WAVs were transferred. The 68 WAVs are already on LUMI according to that report; do **not** retransfer them without a fresh verifier failure.

Use the **selection resolver**, not the highest `rNNN` filename. A revision number identifies an attempt, not owner approval, camera compatibility or an audio/visual phase. Current examples: S03-L001 uses selected r004; S03-L006 keeps its selected r001 anchor; S05-L008-I02 uses r006 after the owner's latest choice; S05-L008-I04 uses r003; S06 ready/descending use r008. Other selected scene sources may live outside `scene_compositions`. The technical binding manifest in `review/s01_s08_source_bindings_r001/SCENE_IMAGE_BINDINGS.json` supersedes old ledger rows without rewriting historical approvals. `production.sequence_plan.selection_catalog` applies that binding. Do not use a blanket “latest file wins” rule in future runs.

`INPUT_MAP.json` is an **input inventory**, not a ready-to-run job list: it does not certify native/fitted stills, edge/portrait geometry, phrase timing, model capability, GPU execution, whole motion or take selection. For S01 L001 and S02 L002, each *different* forest source is paired with itself for its own environment hold. They are not first/last images for one transition. Character dialogue requires stable raw takes and the V7 mouth workflow; narrator audio never drives lips.

## Verified Mac finding: the missing archive bytes are here, but Git ignored them

I checked the eight names in LUMI's `MISSING_PROVENANCE.json` against `stories/lion_and_mouse_v7/history/retained_sources/INDEX.json`. **All eight archive PNGs exist on Mac and match their recorded SHA256.** The complete index contains 167 PNG entries; all 167 files exist locally. **59 archived Milo PNGs are not Git-tracked** (about 87 MB in their directory), because the root `.gitignore` contains `*.png`. By contrast, the archived scene-composition PNGs were explicitly tracked after a prior cleanup fix. This explains why a Git pull can yield a passing selected-input map while historical pose PNGs remain absent on LUMI. The eight required hashes from the LUMI report are:

| Missing basename | SHA256 |
|---|---|
| `milo_run_duck_default_3q_r001_candidate.png` | `52cb7003a9332646d2bf4f87f9bb8aa44711865990f68d6371577897546c3d40` |
| `milo_trip_rear_paw_paw_contact_3q_r001_candidate.png` | `57e21c52da787a31d43e53d67514902237ac02651327c6fb9ce5068223099ceb` |
| `milo_trip_rear_paw_paw_contact_3q_r002_candidate.png` | `672923654105f1d59ac97688f76112095ca41ef91d8adf6a25d6c2a1f2374ed3` |
| `milo_trip_rear_paw_paw_contact_3q_r003_candidate.png` | `9213a6b8c18be22ceb14663a2b0b5a684f8437534f439c789a0dc9bd928007b6` |
| `milo_trip_rear_paw_trip_3q_r001_candidate.png` | `07407db61abd193319078fab8d0803c49e81f6e9e42312167caf3714cba8d2b1` |
| `milo_tumble_flank_to_face_roll_3q_r001_candidate.png` | `1dfac13eb95f0ab2d0cd0736a8d1020fcc08f52b651b48fdb6bb9d966686d327` |
| `milo_tumble_flank_to_face_support_lost_3q_r001_candidate.png` | `4e7db2fdbc3e37f09b1b1e4177e9546c049cbeb02bce177fcbf3a3ec0b966653` |
| `milo_tumble_flank_to_face_tumble_3q_r001_candidate.png` | `51d3737bd9547a443fbd8314ad2ca525eef209494d021f80dc0f600ccebe706a` |

**Immediate data repair:** use LUMI's exact `MISSING_PROVENANCE_FILES.txt` with `rsync --files-from` from the Mac repository root to the same relative paths on LUMI, as its report proposes. Compare each received SHA256 with `MISSING_PROVENANCE.json` and the archive index. Do not regenerate, rename, replace with r002, or alter selected artwork. LUMI already recovered 52 exact-hash historical references from Git/backup according to its report; reconcile those existing bytes and the eight missing paths before transferring more. Preserve `PROVENANCE_RECOVERY.json` as a receipt.

**Durable fix for review:** either deliberately track the 59 hash-verified archived Milo PNGs (with a narrow ignore exception and Git validation), or move them into a separately versioned, hash-bound transfer artifact that LUMI must verify before full-story provenance validation. Do not silently force-add 87 MB or delete the index. Test a *fresh clone/checkout* or package extraction, not merely the current Mac worktree. The archive index must not point to bytes that only exist on one developer machine. Also add a preflight that audits every index entry and reports all missing archive files in one pass.

## Why two different checks disagree

LUMI reports `INPUT_MAP` verification `PASS`: selected stills, 68 WAVs, audio metadata and plan match their hashes. `production.sequence_plan.resolve_sequence` also invokes whole-story validation. The performance-library validator follows historical pose references via `production.audio_visual_plan.source_file`; absent archive bytes become `global_schema_errors`. `production.sequence_readiness.evaluate` currently prepends **all** `global_schema_errors` to every packet's blockers. Thus even environment-only `s01_empty_hold` and `s02_line_002` can be blocked by an unrelated historical Milo pose. This is a validation-scope issue as well as a transfer issue. The first LUMI count of 18 errors was one exposed error per branch, **not** a complete missing-file count. Its complete archive audit later found eight absent PNGs after recovery.

For the engineering fix, keep a separate complete whole-story provenance audit, but make **sequence render eligibility** depend on exact transitive inputs for that sequence. Preserve hard failures for relevant selected sources, aliases, hashes, camera/portrait/geometry evidence and stale review. Do not remove `global_schema_errors` from packets as a shortcut or mark historical files approved. Add CPU tests: unrelated missing historical pose does not block an empty-forest hold; a directly required missing pose still blocks; whole-story audit still reports the former; stale hashes and conflicting selections fail closed.

## Pilot and execution state reported by LUMI

- Checkout `/flash/project_465002727/jelealro/feltwillow-production`, branch/HEAD `ebff6ee`, map verifier pass, 68 WAVs present. Existing container runs Python with PyTorch `2.7.1+rocm6.2.4`, ROCm `6.2.41134-65d174c3e`, Diffusers `0.39.0`. **No model weights were loaded and no GPU jobs submitted** during that investigation. Cache completeness, deployed Wan class/config, `expand_timesteps`, actual endpoint fidelity, RAM and GPU memory are unproven.
- Codex/Bubblewrap may fail with namespace `ENOSPC` before Bash; approved host commands and ordinary container Python worked. Do not investigate `/flash` free space based on that error or run Codex inside a compute allocation. Use the normal Python/Slurm package worker.
- LUMI saved a pre-recovery `READINESS.json`, refreshed pilot packets, `PROVENANCE_RECOVERY.json`, `MISSING_PROVENANCE.json`, two fitted previews and a local recovery helper in its results/scratch paths. Re-run readiness after provenance transfer; the original scan is stale evidence.
- The two proposed *diagnostic* holds each use one selected forest PNG twice: 1280×720, 81 frames, 16 fps, four Lightning steps, guidance 1/1, seed 1. One operation is about 5.06 encoded seconds; it does **not** cover S01 L001's full 9.96-second narration. The S01 native plate has a faint bottom-right mark requiring explicit disposition. Equal endpoints do not guarantee no invented cast or objects in intermediate Wan frames.
- No frozen eligible package, reviewed allocation, capability/cache proof, GPU job or real video existed at the time of LUMI's report. Do not describe the 53 mapped sequences as execution-ready. S01 tiny bite, S02/S03/S05/S06/S08 physical and visual gates, portrait mouth calibration, and exact audio/event timing remain separate per-sequence dependencies.

## Next-agent work order

1. Read this file, `INPUT_MAP.json`, `AUDIO_FILES.txt`, `docs/portable-sequence-production.md`, current owner bindings, and **fresh** LUMI evidence. Verify Mac/LUMI HEAD, worktree and hashes. Do not re-audit old reviews indiscriminately.
2. Resolve the eight missing provenance bytes by exact-hash transfer, then audit all index entries on LUMI and rerun scoped `s01_empty_hold`/`s02_line_002` resolution/readiness. Distinguish recovered bytes from actual selected art.
3. Propose and test the global-versus-scoped validator change on CPU; do not weaken directly relevant dependency gates. Produce a small fresh-clone/package portability test for all archive references and a reproducible transfer manifest for Git-ignored media.
4. For each pilot, prepare actual native/fitted still/edge review, corner-mark disposition, diagnostic timing, installed model/LoRA/config evidence and exact package. Run `sequence_package.py` build/verify and CPU worker preflight. State blockers precisely; never fabricate `reviewed: true`.
5. Present the two exact package/operation identities, cost/resource estimate and durable journal policy for **separate owner GPU authorization**. Only then submit bounded `dev-g` tests using `lumi/sequence_job.sbatch`, zero auto retries/requeue. Do not run the legacy bulk renderer or submit a 53-sequence batch.
6. Verify returned hashes/decode/fps/frame counts and watch full clips/joins with audio. Only reviewed, selected takes may feed dialogue compositing and later scene assembly. Preserve the distinction between diagnostic clips and a complete S01–S08 film.

**Question for the next agent:** Is a sequence-scoped validator plus a versioned provenance/media package the right durable design, or does the existing validator require the complete 59-file Milo archive to remain present on every execution host? Compare the smallest safe implementation and fresh-host tests before choosing. Do not assume “highest revision” or a passing input map answers this.
