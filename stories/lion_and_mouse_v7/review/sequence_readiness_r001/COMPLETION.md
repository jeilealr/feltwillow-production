**Update — r004 accepted:** Owner selected S03-L001-B01-I02 r004 (`5163cea0a436d27ec4b1ea4a16c857b5ffdb504a0309d587fe34d84a7d2beee6`). Current ledger now points to r004; original r003 and creation-time records remain preserved. Next work is the compatible dependent fork tranche. Earlier pending-selection statements below describe the preparation snapshot.

# Feltwillow v7 sequence integration — implementation report

**Source:** `wan-new-image-approach`, starting/current committed HEAD `5214e701697498ab272f317e28c1ace47c7835e3`. Changes remain local and uncommitted. No stage, commit, push, model download, paid request or GPU submission occurred.

The generic local sequence pipeline is implemented. It resolves exact scoped selections separately from planned slots, normalizes aliases/holds, checks scoped readiness, compiles ordered endpoint pairs into immutable runtimes/commands, carries runtime/run/hash identity through inventory/render/receipt/dialogue/preview, preserves model-native boundaries, and presents ordered native/fitted/audio review boards. Actual film production remains gated by artwork, alignment, selection and authorized resources.

## Concrete result to review

[New local S03-L001 fork foundation r004](local_fork_foundation_r001/review.html), SHA256 `5163cea0a436d27ec4b1ea4a16c857b5ffdb504a0309d587fe34d84a7d2beee6`.

This deterministic candidate uses the selected L006 setup and only L001's local facial attention. It applies no translation, independent scaling, body redraw or paid generation. All pixels outside the recorded face alpha remain exactly the base, including background/root/feet. Native and model-fitted views were inspected; no obvious patch boundary was observed. This is still a **new unselected candidate**, with no automatic anatomy/integration/video certification. Original selected r003 and all ledgers remain unchanged. The earlier paid fork proposal is superseded and must not be submitted.

## Implementation and evidence

- New `sequence_plan.py`, `sequence_readiness.py`, `sequence_export.py`, `sequence_review.py`, and exact-take helper `sequence_take.py`; implemented contracts/CLI examples are in [sequence production](../../../../docs/sequence-production.md).
- `shot.py` now accepts isolated runtime/run/digest inputs, validates effective frames/size/settings/seed/hash/fit/environment before loading, records code/config provenance and native boundaries, and refuses an already claimed uncertain attempt. Historical composition dry-run behavior remains available when sequence flags are absent.
- Inventory emits exact one-seed argument arrays and requires a reconciled operation journal before proposing missing jobs. No new sequence is routed through the historical bulk launcher's repeated rounds.
- Dialogue/preview consumers can resolve exact reviewed/selected run paths and hashes; post-dialogue outputs require new exact review/selection. Narrator audio never drives mouths. No dialogue treatment or assembly was performed.
- Planned image slots keep their null-media lifecycle. Existing authored plan fields, text/audio records, world events/states and causal ordering equal the starting source; only the optional production sequence section was added. See `PRESERVATION.json`.
- **81 selected logical scene uses / 59 unique rasters** through S08 were verified unchanged. All **161** actual line WAVs match their scene-master PCM slices; pauses/tails were verified silent and counted once. S02 master is **24.89 s**; S03 is **39.02 s**, with L008 ending at **31.15 s** and L009 beginning at **31.85 s**. Phrase/action markers are still pending review.
- All **26** downloaded historical pilots match recorded full hashes and decode at their recorded dimensions/frame counts/fps. All historical receipts have no end image. No new full-motion visual pass is inferred from decode or receipts.
- Fresh strict background screens reproduce **7 fork failures + 1 acorn failure**. These comparisons use the original conservative exclusions, not approved production masks or anatomical measurements. The new local candidate's separate protected-face-mask check passes with **zero changed protected pixels**.
- All 27 historical gaps are classified. Eight explicit aliases avoid duplicate assets; S03 L001 now has an explicit editorial establishment hold, while its old planned I01 remains unfilled. Missing walks, pickup/taste/rise/trip/landing coverage is not hidden by arbitrary aliases.
- Read-only SSH inspected installed LUMI Diffusers **0.39.0** source and the pinned cached A14B model index. The installed constructor defaults to `expand_timesteps=False`, and the cached configuration supplies no contrary override. This supports an endpoint probe, not a behavioral guarantee. Source/config hashes are archived; no weights/framework were loaded remotely.

## Verification

The final focused integration run passed **83 tests**, and the performance group passed **24 tests**: **107 distinct cases, zero skips**. Commands, node IDs and logs are in `TEST_RESULTS.json`, `COLLECTED_TEST_IDS.json`, `focused-tests.log` and `performance-final.log`. Focused checks include actual renderer command argv/entrypoint → fake backend → native capture/encoded fixture → receipt/review, plus a real small CPU video decode test. No Wan model is used by them.

The retained current proof is `cpu_fixture_r005/TRACE.json`; its exact source hashes and RGB A→B/B→C observations are recorded alongside tiny synthetic clips/receipts. Earlier fixture revisions remain historical. CLI/help, planning validation, expected blocked readiness, formatting/lint and `git diff --check` results are recorded separately. The full suite was not run because no commit was requested.

Several existing tests contained earlier production totals/coverage assumptions or real binding hashes inside synthetic fixtures. These were corrected while preserving causal/audio/hash/approval/containment assertions; see `test_coverage_mapping.md`. Historical failures are explicitly superseded, not silently called passes. Three delegated specialists were unavailable due to workspace quota, so no independent specialist sign-off is claimed.

## Decision table

| Outcome | Current decision |
|---|---|
| Plan reconciled | Explicit opening/cut/hold/alias structure implemented; S02 support/rise depiction still needs resolution against unchanged narration. |
| Still sequence ready | **No.** New fork foundation awaits selection; other strict-background/physical-phase/crop issues and missing states remain. |
| Runtime ready | **Offline engineering checks passed.** Installed endpoint source/configuration inspected. No complete real-media execution packet clears its gates yet. |
| Diagnostic demonstrated | **Not run.** No authorized GPU probe or actual Wan continuity result. |
| Aligned production reviewed/selected | **Not run.** Phrase alignment, repaired selected artwork and real take review remain required. |
| Final assembly approved | **Not requested or performed.** |

Every F01–F24 and T00–T16 row has a separate implementation/evidence status in `IMPLEMENTATION_STATUS.json`. Later S04–S16 dependencies and next actions are in `LATER_COVERAGE.json`; opening work is not whole-film completion.

## Handoff

Start with [the candidate comparison](local_fork_foundation_r001/review.html), [ordered boards](SEQUENCE_BOARD.md), [decisions](DECISIONS.md) and [consolidated blockers](BLOCKER_PACKET.md). `RESUME.md` contains verified CPU-only commands and identifies what must not be rerun. `CHANGED_FILES.json`, `SOURCE_CONTENT_HASHES.json` and `ARTIFACT_MANIFEST.json` identify the final working content. Media can be Git-ignored: a repo-only agent must verify bytes against manifests and report unavailable assets, not infer visual passes.
