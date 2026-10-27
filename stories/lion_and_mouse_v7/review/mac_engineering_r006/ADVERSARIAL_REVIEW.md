# Independent adversarial package/editor review

Date: 25 October 2026, Europe/Berlin. Reviewer: `/root/editorial`, independent of the implementation writer. Source commit: `67170527de0bde52a375d99329f83f16ecfc9306`; reviewed current uncommitted implementation. This reviewer previously authored r004 grammar/docs, but made no package/editor/runtime changes. Only this report was written in the repository. Reproductions used temporary synthetic plates, CPU FFmpeg clips and fixture packages; no scheduler job, provider, model load, download, Git change or owner artwork selection occurred.

## Actual verification

`/Users/lealroja/miniconda3/envs/feltwillow/bin/python -m unittest tests.test_sequence_package tests.test_sequence_editor tests.test_sequence_timeline -q`

**13 tests passed (2.531 s).** This proves current relocation/preflight/static fixture execution, exclusive repeated-attempt rejection, asset tamper/path escape rejection, selected-take edit binding, allocation invalidation and timeline fixture behavior. It does not prove a trusted remote launch bootstrap, real GPU compatibility, physical joins, speech/art quality or final assembly approval.

## Blocking findings

### A1 — Packaged verifier is executed before it is verified

`lumi/sequence_job.sbatch` directly executes `PACKAGE/payload/production/sequence_package.py`. That Python file contains verification/authorization logic, but is itself mutable package payload. A harmless reproduction built a normal synthetic package, replaced only that worker with `print('UNVERIFIED_WORKER_EXECUTED')`, and called the launcher with a nonexistent operation and missing authorization file using the approved local interpreter. The launcher exited **0** and printed **UNVERIFIED_WORKER_EXECUTED**. Calling the unchanged trusted repository `verify(package)` separately correctly rejected the modified worker. Thus the launcher bypasses its own intended trust root.

Use a trusted host-side launcher/verifier outside the payload, pinned independently to the expected authorized package identity. Validate all executable/importable payload bytes before importing/executing packaged code; do not bootstrap that verification from the same unchecked worker.

### A2 — Unlisted importable Python payload is accepted

`verify()` hashes only manifest-listed files. A new unlisted `payload/production/yaml.py` was added to a valid fixture package; `verify(package)` still succeeded. Python launches with the worker directory on its import path, and `sequence_package.py` imports `yaml` before verifying the package, so an unlisted shadow module can execute before any asset/auth checks. A1's trusted bootstrap must also reject unexpected executable/importable files (and unsafe links), or execute in an isolated complete allowlisted tree. A manifest digest does not protect files absent from its inventory.

### A3 — Join approval survives a changed selected source window

`sequence_timeline.compile_timeline()` binds join review only to the two source-video hashes. A CPU fixture contained two sixteen-frame/16fps MP4s and a passing continuous join review. The first row was changed from source frames0..15 to frames4..11 while retaining its sixteen-cell target; fresh exact trim and retime approvals were supplied. The same old join review remained accepted, although its outgoing source boundary moved from frame15 to11 and the outgoing motion changed. Both fixture clips were solid colors to isolate the contract; this is a review invalidation failure, not a visual-join assertion.

Bind join approval to both exact source windows, their target timing/fps/frame maps, native/decoded boundary evidence and actual join policy. Reordering, trimming or retiming either side must invalidate join evidence even when source files are unchanged. Add an expected-failure regression for this exact case.

All findings were sent directly to the integrator. Current verdict: **existing tests pass; adversarial sign-off blocked on A1–A3**. Preserve the original findings and append fix verification rather than replacing this record.

## Inspected safeguards and limits

Reviewed exact package manifest/file hashes, source runtime hashes, source/code freezing, asset references, relocation materialization, one-seed operation declarations, exact-package authorization fields, exclusive durable operation claims and process-result recording. The worker never submits Slurm itself. The launcher was invoked via local `bash`, not `sbatch`. Host dependencies/model config remain external to the package and require actual host capability verification. Durable-journal correctness depends on operators using the same durable journal; no distributed journal service was tested.

Reviewed editor allocation digests, source-window limits, one meaningful piece once in authored order, settled/resting static holds, separately selected returned takes, actual FFprobe frame count/rate inspection and target-bound trim/retime reviews. Actual PCM phrase/action alignment and native motion/voice review remain external evidence. A package moved after host materialization may need a newly scoped host-runtime destination because absolute relocated paths change immutable runtime bytes; relocation was tested by existing fixtures before materialization only.

## Checked fingerprints

- `production/sequence_package.py`: `fc7870d7d1f537acdebd48da047d5b51dcbd1567b6fd181e4112feaed53f3b30`
- `lumi/sequence_job.sbatch`: `2b66ae827dde2e5b4a1d9bb3ba9e3251a421fcb4e323e05818c9e831d9d532f8`
- `production/sequence_editor.py`: `a713c5784776b9cfd832781570d0d05a12026324f0c3864739ea8e8eceeab54f`
- `production/sequence_timeline.py`: `bce912460ee749c55495f72d6b092308d8d7ae3bc47aeb94cdf5a79009e88fba`
- `tests/test_sequence_package.py`: `84dbac20b5e76a108d6a130a2e916ea430db84b311a4e6d3309398f867074ffa`
- `tests/test_sequence_editor.py`: `aa42c59bc5ebb60f895e6ac4a24ab1b13e2ac3987d2f802ad3d73f96006a02a4`
- `tests/test_sequence_timeline.py`: `e36eb4baeca7080e02dde95ca53e441de59b0371127823a28437832047135ec9`

## Independent fix recheck

Re-ran the three harmless original adversarial fixtures after integrator fixes:

- A1 now exits1 with `PACKAGE_BLOCKED: package file changed: payload/production/sequence_package.py`; the replaced worker's marker never executes. Launcher uses the trusted `FELTWILLOW_REPO` entrypoint.
- A2 now rejects the unlisted shadow module with `unexpected or missing package payload file`. Verification inspects the complete assets/payload inventory; child execution disables bytecode writes. CPU preflight requires a separately supplied expected package digest; execute checks exact package authorization before child execution.
- A3 now rejects the stale source-window join with `continuous video join requires actual native/decoded boundary review`. `join_digest` binds both actual source mappings, target samples/frame cells, rates and policy.

Re-ran `/Users/lealroja/miniconda3/envs/feltwillow/bin/python -m unittest tests.test_sequence_package tests.test_sequence_editor tests.test_sequence_timeline -q`: **15 tests passed, 2.654s**. Original A1–A3 findings are fixed for the tested cases. No new unchecked-code execution route was found within the trusted-checkout/interpreter assumption.

### A4 — Host runtime directory symlink escapes the package

A valid synthetic package was augmented with `host_runtime` as a directory symlink to a fresh temporary directory outside the package. `materialize(package)` accepted it and wrote `runtime.yaml` and `packet.json` into that outside directory (both actual files verified). `worker()` invokes materialize before expected-package/auth checking, so this causes out-of-namespace writes during nominal preflight even without authority for execution. The payload/assets symlink prohibition does not cover runtime/output namespaces.

Reject symlinked runtime/output directories and validate resolved destination containment before creating files. Cover host_runtime (materialization) and outputs (execution) in expected-failure fixtures. This narrow path guard remains the current sign-off blocker and was sent to the integrator.

Recheck code fingerprints:

- `production/sequence_package.py`: `fc7870d7d1f537acdebd48da047d5b51dcbd1567b6fd181e4112feaed53f3b30`
- `lumi/sequence_job.sbatch`: `2b66ae827dde2e5b4a1d9bb3ba9e3251a421fcb4e323e05818c9e831d9d532f8`
- `production/sequence_timeline.py`: `bce912460ee749c55495f72d6b092308d8d7ae3bc47aeb94cdf5a79009e88fba`

## Path-guard and result-transport recheck

Re-ran A4 with a valid synthetic package whose `host_runtime` symlink points to a fresh outside directory: now rejected with `package output path escapes namespace`, and the outside directory contains zero files. Inspected `contained_output`, pre-materialization trust/authorization checks, external journal/auth requirements and output-tree symlink rejection. Original A4 is fixed for the reproduced case.

Latest package/editor/timeline suite: **17 tests passed (3.324 s)**. This includes the new path/launch/inventory guards and source-window join regression. No actual production operation was run; tests use isolated CPU fixture packages.

### A5 — Result verification can accept a fabricated empty completion

Independent minimal reproduction created `results.json` containing a wrong schema (`not-even-result-schema`), caller-expected package SHA as a plain string, invented run/runtime IDs, empty files and operations, and its correctly recomputed self-hash. `verify_results(folder, expected_package_sha256)` accepted it and returned the invented run ID. The expected package SHA is only compared to an untrusted metadata value; the verifier has no trusted operation/runtime manifest against which to validate completeness, identity or recipe. Therefore a self-consistent but incomplete/substituted result packet can be called verified. No real result/receipt was altered in this reproduction.

Require the trusted execution package/manifest (validated against its independently supplied expected SHA), or an independently trusted returned-results digest. Validate result schema and exact operation set/count, run/runtime, shot/seed and source/effective recipe against that authority; verify every declared clip/receipt/native boundary. Preserve original raw receipts and relocation path maps. A nonempty result set and schema check alone would close the minimal reproduction but would not bind returned operations to the intended package. Finding sent to the integrator; result-transport sign-off remains pending.

Current recheck fingerprints:

- `production/sequence_package.py`: `038fceafb7a8e926cc9e7b369f2f9e8a4a976b3b92ec22e4326c0862ef5f251e`
- `production/sequence_timeline.py`: `bce912460ee749c55495f72d6b092308d8d7ae3bc47aeb94cdf5a79009e88fba`
- `tests/test_sequence_package.py`: `b530fe5fd5dc0e10faf1bc141f47172fcea395acf72e801c1e05170316f82180`
