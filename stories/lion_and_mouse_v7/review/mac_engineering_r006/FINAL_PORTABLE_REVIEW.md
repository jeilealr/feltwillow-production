# Independent final portable CPU review

25 October 2026. Reviewer: `/root/portable_final_review`, separate from the implementation author. Base commit: `67170527de0bde52a375d99329f83f16ecfc9306`; review covers the current uncommitted files fingerprinted below. Read current leading AGENTS/CLAUDE directions and the preserved A1–A5 report. This reviewer changed only this evidence file. No network, model load, GPU/scheduler job, Git mutation, owner-media change or final assembly occurred.

**Scoped pass:** no remaining blocking issue found in the reviewed portable package, result transport, editor allocation, join invalidation and exclusive-claim code under the documented trusted checkout/interpreter, trusted execution host, independently recorded digests and shared external durable-journal assumptions. This is a CPU contract review, not real host/GPU compatibility, visual/mouth acceptance or final-film approval.

## Actual independent checks

Verified `/Users/lealroja/miniconda3/envs/feltwillow/bin/python` reports that exact executable and prefix `/Users/lealroja/miniconda3/envs/feltwillow`.

Ran:

```text
/Users/lealroja/miniconda3/envs/feltwillow/bin/python -m unittest tests.test_sequence_package tests.test_sequence_editor tests.test_sequence_timeline -q
Ran 20 tests in 3.553s
OK
```

Separately exercised a temporary synthetic static CPU package with an external exact-package authorization/journal; no owner assets or actual production operation were used. Actual outcomes:

- Successful ordinary-Python worker execution, collection, movement of results to a new directory and `verify_results` with the independently retained package and collection digests: passed. The focused suite additionally moved the package before worker execution and used a path containing spaces.
- Correct result packet with an intentionally wrong trusted results digest: rejected with `result manifest/package differs from trusted collection digest`.
- Fabricated valid-schema, correctly self-hashed result with empty files/operations and the expected package digest: rejected with `invalid or empty results schema`. The suite separately rejects the original wrong-schema forgery.
- Edited host runtime prompt, recomputed adjacent marker runtime hash, and edited returned receipt prompt/runtime hash together: collection rejected with `nonidentical immutable destination: .../host_runtime/runtime.yaml`. The collector reconstructs the exact local materialization from the immutable package template before trusting its runtime/recipe. This check ran after the integrator added that guard.

The reproduction used real CPU encoded bytes and boundary files. Its temporary fixture was removed through the test fixture cleanup.

## Source inspection

Checked the A1–A5 paths: the scheduler calls the trusted checkout verifier; worker trust/authorization checks precede packaged code execution; full payload/assets inventory rejects unlisted Python and symlinks; runtime/output guards enforce containment; original runtime/operation identity determines the exclusive external journal claim; result verification requires a separately trusted collection digest plus package digest, nonempty schema and byte/native-boundary/decode checks. Collection compares expected recipe and input-fit evidence before producing its digest, and now refuses a rewritten host runtime/marker pair. The collection digest must actually be retained through a trusted host connection; reading a digest from the received result packet itself supplies no independent trust.

`join_digest` includes both source hashes, mappings, sample boundaries/frame cells, sample rate, output FPS and declared policy. Existing regression tests reject a stale join after changing a source window. Editor review binds render allocations and exact returned selected source bytes; transported takes remain unselected until owner review. No additional serious package/join/claims blocker was found. This does not independently certify crash durability of the host filesystem, concurrent hostile mutation of files during checking, or operators changing journals to bypass a recorded attempt.

## Reviewed SHA256 fingerprints

```text
5707421e3f7ede0b5db1655bd807c357dcdd192a7290a77788154bcc3da8bb11  production/sequence_package.py
285968c5025d607f91e90d03049c4936731839bffe6d720c0bb13641f6f65811  production/sequence_editor.py
410779f149563493da5e42956d444e005f02707724cff0d352b30b6d8ed46657  production/sequence_timeline.py
afb8a7396611a1b87441b1250ba1a0141382567baf20cd6b9f7e0d402f50bbd2  lumi/sequence_job.sbatch
1608794b48841791c79b82d68bb41b9860a1e651dd813f63c2e8b7a825959784  tests/test_sequence_package.py
f25635f791f0f777decb09ea3648c60f3f107917de162ae4617642318c9e73c8  tests/test_sequence_editor.py
24be779529abacc148b52080989ff411c88a2edf286ebbac03cb0ee6ca269819  tests/test_sequence_timeline.py
b758c4d2ee34307ba3748d5ac150f1f5b67b3a3841ad1a3c5163030efe6d8740  feltwillow/render_receipt.py
```
