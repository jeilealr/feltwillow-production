# S01–S08 selection and continuity status

Prepared 2026-10-28. Initial checkout: branch `wan-new-image-approach`, HEAD `a9878b50b0f6e09353e5b68a224f4ce0d3d2d168`. The pre-existing worktree change was the untracked owner-feedback directory `review/s01_s08_final_visual_feedback_r001/`; it was preserved.

No image pixels, canonical assets, owner-approval records or historical decisions were modified. No generation, Wan/GPU work, external spend, commit, push, merge, reset or deletion occurred.

**Result:** the unambiguous direct bindings are fixed. The resolver currently reports **101 `MATCH`, 2 `MISSING_BINDING`, 4 `CONFLICT` across 107 declared uses and 54 sequences, with zero resolution errors**. All ten distinct S06 scene slots resolve exactly, and S08 L016–L018 all resolve to the approved r005 image. This is not a declaration that all S01–S08 source images are finalized.

## Authority inspected

- Continuation specification: `/Users/lealroja/Downloads/FELTWILLOW_DEEPSEEK_CONTINUATION_HANDOFF_2026-10-28.md`.
- Latest four approvals: [OWNER_FEEDBACK.json](../s01_s08_final_visual_feedback_r001/OWNER_FEEDBACK.json), SHA-256 `7842c30a4d2dfd6792ecdd2e9e8aad251468ad856119192b7fa42e0c107541aa`.
- Earlier accepted repaired depictions: [OWNER_FEEDBACK_20261027.json](../image_repair_s01_s08_r001/OWNER_FEEDBACK_20261027.json), SHA-256 `0df02a5d62ad32d2e9d5e135877fff2c4747309ac34a1462b20b73c6ea2cf964`.
- Current plan: `stories/lion_and_mouse_v7/audio_visual_plan.json`.
- Live resolver: `production/sequence_plan.py::selection_catalog` / `resolve_sequence`.
- Current technical binding map: [SCENE_IMAGE_BINDINGS.json](SCENE_IMAGE_BINDINGS.json).
- Use-level machine audit: [SCENE_USE_MATRIX.json](SCENE_USE_MATRIX.json).
- Technical issue evidence: [TECHNICAL_DIAGNOSTICS.json](TECHNICAL_DIAGNOSTICS.json).

## Four latest owner approvals

All four named files were present and their observed SHA-256 values match the approval record. Scope is source-still visual depiction only.

| Scene use | Bound image / SHA-256 | Result |
|---|---|---|
| `S06-L001-B02-I01` | `S06-L001-B02-I01_scramble_descent_r012_candidate.png`<br>`21415af203daa4ef7bb2e277288a320487a26d1441a018c58e517e5b2522e44c` | `MATCH` |
| `S06-L002-B01-I01` | `S06-L002-B01-I01_front_paw_ready_r007_candidate.png`<br>`b91112d67facfbd833acb59211fa6e26edc9c0040295f9c6a9f569292b187c1c` | `MATCH`; 1671×941 width blocker |
| `S06-L002-B01-I02` | `S06-L002-B01-I02_front_paw_descending_r007_candidate.png`<br>`d2c80afc4b33387fadad5dd2d51836168725f62fae2079d03afab5643e6044c0` | `MATCH` |
| `S08-L016-B01-I01`, `S08-L017-B01-I01`, `S08-L018-B01-I01` | `S08-L016-B01-I01_single_gentle_clear_r005_candidate.png`<br>`9e7bcdfc41a909f86379f65fdfd2fda4f12ce84286679d831cbb4d428d368b8a` | `MATCH` for all three uses |

## Applied technical binding corrections

These pointers are technical mappings to existing owner decisions. The source owner records remain unchanged. Full hashes and authority pointers are in [SCENE_IMAGE_BINDINGS.json](SCENE_IMAGE_BINDINGS.json).

| Slot(s) | Before | Now | Evidence |
|---|---|---|---|
| S06 scramble/paws | r009 for scramble; ready and descending unbound | r012, ready r007, descending r007 | Current four-image owner feedback |
| S06 head raised / freeze / worry / humility | Unbound | Accepted r005/r002/r002/r002 | 27 October owner feedback; bounded-mask verification |
| S08 L016–L018 | Historical r001, production-blocked by missing image-top-right paw | Approved r005 for all three | Current four-image owner feedback |
| S01 tasted aftermath | Unbound | `S01-L004-B03-I04` = tasted r002 | 27 October owner feedback; bounded-mask verification |
| S02 beside-stone contact/release | On-stone r004 images | `I02` r006 and `I03` r007 beside-stone images | 27 October owner feedback; bounded-mask verification |
| S03 fork turns | Six r003 route images | Six accepted locked-local-head r004 images | 27 October owner feedback; outside-envelope pixel verification |

Matching S06 aliases inherit these exact pointers. The old S06 r009 acceptance remains preserved as history, and the old S08 r001 production block remains scoped to those historical bytes; it does not apply to the new r005 hash.

## All declared scene uses

Hashes are shortened to 12 characters here; exact 64-character hashes, paths, selection records, native sizes and blockers are in [SCENE_USE_MATRIX.json](SCENE_USE_MATRIX.json).

| Sequence | Uses: hash prefix (disposition) |
|---|---|
| `s01_empty_hold` | `S01-empty-start` = `c57b58a19ad4` (MATCH); `S01-empty-end` = `c57b58a19ad4` (MATCH) |
| `s01_l002_b01` | `S01-L002-B01-I01` = `cf31d66837db` (MATCH) |
| `s01_l002_b02` | `S01-L002-B02-I01` = `3d1f1a92fffc` (MATCH) |
| `s01_l002_b03` | `S01-L002-B03-I02` = `48b18b39677f` (MATCH) |
| `s01_l003` | `S01-L003-B01-I02` = `937612f07bb4` (MATCH) |
| `s01_l004_b01` | `S01-L004-B01-I02` = `c0fc399b0522` (MATCH) |
| `s01_l004_b01_notice` | `S01-L004-B01-I01` = `5544e449cbd0` (MATCH) |
| `s01_l004_b02` | `S01-L004-B02-I01` = `0d53eba873f3` (MATCH) |
| `s01_opening` | `S01-empty-start` = `c57b58a19ad4` (MATCH); `S01-empty-end` = `c57b58a19ad4` (MATCH) |
| `s01_tiny_bite` | `I01` = MISSING; `I02` = MISSING; `I03` = `4888ccf00b2f` (MATCH); `I04` = `7bfdc59f5a4a` (MATCH) |
| `s02_acorn` | `I02` = `612291f41781`; `I03` = `d9d300f567c4`; boundaries `B01-I02`/`B02-I01` = `6ef75aae6378` (all MATCH) |
| `s02_line_001` | `S02-L001-B01-I02` = `3d2febc8ae47` (MATCH) |
| `s02_line_002` | `S02-L002-B01-I02` and shadow hold = `0cd775bbf05e` (MATCH) |
| `s02_line_003` | `S02-L003-B01-I01` = `d56253919398` (MATCH) |
| `s03_fork` | Six accepted r004 turns = `bd4d70047755`, `01393c480f54`, `dc7d65a9213f`, `2fbe9fa98a3e`, `476cab8a5691`, `b73c9e74b434`; boundary r004/r001 = `5163cea0a436`, `7842d9c8a4c2` (all MATCH) |
| `s03_portraits` | `S03-L009-B01-I01` = `e3abec717e92`; `S03-L010-B01-I01` = `dbe435cf3f87` (MATCH) |
| `s04_line_001` | `S04-L001-B01-I01` = `285e020adb64` (MATCH) |
| `s04_line_002` | `S04-L002-B01-I01` = `08eaef0c1a80` (MATCH) |
| `s04_line_003` | `S04-L003-B01-I01` = `09cc6e86a326` (MATCH) |
| `s04_line_004` | `S04-L004-B01-I01` = `47065c316a8b` (MATCH) |
| `s04_line_005` | `S04-L005-B01-I01` = `7c0690e9cc54` (MATCH) |
| `s05_line_001` | `S05-L001-B01-I01` = `70e65df59a39` (MATCH) |
| `s05_line_002` | `S05-L002-B01-I01` = `94302082c30c` (MATCH) |
| `s05_line_003` | `S05-L003-B01-I01` = `1974103c60ee` (MATCH) |
| `s05_line_004` | `S05-L004-B01-I01` = `2c64e1cd799e` (MATCH) |
| `s05_line_005` | `S05-L005-B01-I01` = `20cbd4d6cfb1` (MATCH) |
| `s05_line_006` | `S05-L006-B01-I01` = `20cbd4d6cfb1` (MATCH) |
| `s05_line_007` | `S05-L007-B01-I01` = `97ff6d146c67` (MATCH) |
| `s05_line_010` | `S05-L010-B01-I02` = `f3ee9f2030ae` (MATCH) |
| `s05_line_011` | `S05-L011-B01-I01` = `2edd8ea64340` (MATCH) |
| `s05_trip` | `S05-L008-I01` = `931524d8d9fe`; `I02` = `f0fc9cea1bfe`; `I03` = `7d2559b53235`; `I04` = `a7f5009ae804`; `S05-L009-I01..I04` = `f94ceb152de7`, `0d461578cc92`, `271dc07c6995`, `1212d2cb1d80` (all MATCH; contact blocker remains) |
| `s06_interaction` | All 13 uses MATCH. Distinct rasters: `I01/B01`=`bc914de64088`; head=`d5f82c7dc769`; scramble=`21415af203da`; arrival=`2933f3920069`; ready=`b91112d67fac`; descending=`d2c80afc4b33`; block=`c8a49ebe6bfc`; frozen=`9b2873da9c1c`; worried=`ceedf7650249`; humbled=`a3c8044b114c` |
| `s07_leo_portraits` | `S07-L001`=`ef44e984d565`; `S07-L002`=`ea1baf9e1a54` (MATCH) |
| `s07_milo_portraits` | `S07-L003`=`8cce3ae6f09d`; `S07-L004`=`ff19fba7854b`; `S07-L005`=`79763a465591` (MATCH) |
| `s08_leo_portraits` | L007 I01/I02 and L011 MATCH; L008, L009, L010 I01/I02 are `CONFLICT` because their aliases change declared state or `location_view` |
| `s08_line_001` | `S08-L001-B01-I01` = `a5f2dff0e0bb` (MATCH) |
| `s08_line_002` | `S08-L002-B01-I01` = `a5f2dff0e0bb` (MATCH) |
| `s08_line_003` | `S08-L003-B01-I01` = `a5f2dff0e0bb` (MATCH) |
| `s08_line_004` | `S08-L004-B01-I01` = `a5f2dff0e0bb` (MATCH) |
| `s08_line_005` | `S08-L005-B01-I01` = `a5f2dff0e0bb` (MATCH) |
| `s08_line_006` | `S08-L006-B01-I01` = `a5f2dff0e0bb` (MATCH) |
| `s08_line_012` | `S08-L012-B01-I01` = `fc8c4cc61fd8` (MATCH) |
| `s08_line_013` | `S08-L013-B01-I01` = `363ebb719394` (MATCH) |
| `s08_line_014` | `S08-L014-B01-I01` = `363ebb719394` (MATCH) |
| `s08_line_015` | `S08-L015-B01-I01` = `363ebb719394` (MATCH) |
| `s08_line_016` | `S08-L016-B01-I01` = `9e7bcdfc41a9` (MATCH) |
| `s08_line_017` | `S08-L017-B01-I01` = `9e7bcdfc41a9` (MATCH) |
| `s08_line_018` | `S08-L018-B01-I01` = `9e7bcdfc41a9` (MATCH) |
| `s08_line_019` | `S08-L019-B01-I01` = `6d4d9bb3e6dd` (MATCH) |
| `s08_line_020` | `S08-L020-B01-I01` = `6d4d9bb3e6dd` (MATCH) |
| `s08_line_021` | `S08-L021-B01-I01` = `6d4d9bb3e6dd` (MATCH) |
| `s08_line_022` | `S08-L022-B01-I01` = `363ebb719394` (MATCH) |
| `s08_line_023` | `S08-L023-B01-I01` = `363ebb719394` (MATCH) |
| `s08_line_024` | `S08-L024-B01-I01` = `363ebb719394` (MATCH) |

## S01–S03 reconciliation

**S02 placement:** `I02` and `I03` now bind to the owner-accepted beside-stone contact r006 and release r007. Bounded verification reports zero changed pixels outside the recorded masks. Mask interiors, hand/acorn contact quality, background exactness inside those masks and animation joins remain technical/visual review items.

**S03 fork:** The six accepted local-head r004 images now replace the older r003 route endpoints. Their declared broad head envelope has zero changes outside it, but exact interior background and the head/body seam remain unresolved; this remains a technical continuity gate.

**S01 bite:** The tasted closed-aftermath r002 is now bound to `I04`. The other accepted raster, `S01-L004-B03_key_tiny_toothless_contact_r002_candidate.png` (`fb69e499c3d32b51672999de92156f8b4be6f08945a375fd4e7a63c329752dbe`), has no declared image slot. `I03` is the selected whole-acorn pre-bite; `I01` and `I02` remain unbound. Assigning the contact raster would require a sequence/key decision, so it was not guessed.

## Residual diagnostics

**Background preservation — blocked/partial.** The latest S06 descending r007 has an explicit technical-preservation failure in `complete_s06_r001/QA.json`; the S06 scramble r012, ready r007 and S08 r005 do not have an exact-pixel preservation result, and no approved final masks were found. S01 tasted aftermath, S02 placement and S03 head-turn candidates have the narrower provenance results described above. See [TECHNICAL_DIAGNOSTICS.json](TECHNICAL_DIAGNOSTICS.json).

**Paw-ready width — blocked.** The approved image is 1671×941; the locked scene contract is 1672×941. Its resolver fit crop is `[0,0,1671,940]`. Whole-frame/top/left probes against r005 favoured x offset 0, suggesting rightmost-column occupancy loss, but an upper-right probe favoured offset 1 and no side-specific production receipt exists. The edge is therefore not certified. The approved file and hash were preserved; no crop, pad, resize or test waiver was applied.

**S05 rear-paw contact — blocked / GPT visual work.** The selected `S05-L008-B01-I02` remains r004 (`f0fc9cea1bfe…`). The later r006 candidate is unselected, and existing evidence does not prove the advancing foot visibly catches at Leo’s rear-paw edge. `s05_trip` remains not render-ready. Exact GPT inputs and preservation bounds are recorded in [TECHNICAL_DIAGNOSTICS.json](TECHNICAL_DIAGNOSTICS.json).

## Validation actually run

| Check | Result |
|---|---|
| Shared-skill link/drift check | PASS |
| `python -m unittest tests.test_v7_current_assets tests.test_selected_scene_cleanup` | 9 tests PASS, including a new fail-closed technical-binding override/hash test |
| `python -m unittest tests.test_sequence_pipeline` | 21 tests PASS; expected negative-case CLI text appeared inside the passing module |
| `python -m unittest tests.test_audio_visual_plan` | 32 tests PASS in 173.809 s |
| `python production/audio_visual_plan.py --story lion_and_mouse_v7 validate` | Planning PASS |
| `python production/audio_visual_plan.py --story lion_and_mouse_v7 derive` | Generated index refreshed; planning PASS |
| Full S01–S08 resolver matrix | 107 uses / 54 sequences; 0 resolver errors; 101 MATCH / 2 MISSING / 4 CONFLICT |
| Latest approval file hashes and dimensions | All four hashes match; dimensions 1672×941 except ready r007 at 1671×941 |
| Full unit-test suite | NOT RUN, per focused-validation instruction |

## Changed files

- `production/scene_image_bindings.py`: validates current technical bindings against exact owner-authority records and fails closed on stale hashes.
- `production/sequence_plan.py`: applies current technical bindings after historical selection discovery.
- `tests/test_v7_current_assets.py`: adds override and tamper rejection coverage.
- `stories/lion_and_mouse_v7/derived/sequence_realization_index.json`: regenerated from the live resolver.
- `stories/lion_and_mouse_v7/derived/audio_visual_summary.json`: refreshed selected-use/raster counts.
- `stories/lion_and_mouse_v7/review/s01_s08_source_bindings_r001/SCENE_IMAGE_BINDINGS.json`: 17 direct technical bindings.
- `stories/lion_and_mouse_v7/review/s01_s08_source_bindings_r001/SCENE_USE_MATRIX.json`: complete use-level audit.
- `stories/lion_and_mouse_v7/review/s01_s08_source_bindings_r001/TECHNICAL_DIAGNOSTICS.json`: residual issue evidence.
- This report.

The pre-existing untracked `review/s01_s08_final_visual_feedback_r001/OWNER_FEEDBACK.json` remains unchanged.

## Next action

| Priority | Work | Responsible |
|---|---|---|
| 1 | Decide how the accepted S01 tiny-contact raster enters the four-key bite sequence, or explicitly waive the extra state | Owner |
| 2 | Review/repair exact background preservation for the four latest accepted images against their locked anchors; retain current accepted hashes until a reviewed replacement exists | GPT visual work, then owner |
| 3 | Decide whether the approved 1671×941 ready image is acceptable under a revised camera contract or requires a separately named 1672×941 candidate; never silently alter the accepted bytes | Owner; GPT only if new pixels are required |
| 4 | Resolve the S05 rear-paw contact with the exact bounded handoff in the diagnostics and submit its new bytes for owner review | GPT visual work, then owner |
| 5 | Decide whether S08 L008–L010 should remain aliases despite changing declared state/location view, or receive explicit per-line bindings/cuts | Owner, then DeepSeek binding fix |

After any approved replacement, DeepSeek should update the technical manifest, regenerate the use matrix and rerun the focused tests.
