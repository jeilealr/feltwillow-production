# Implemented contract

The maintained specification and actual CLI examples are in [sequence production](../../../../docs/sequence-production.md). Implementations are `production/sequence_plan.py`, `sequence_readiness.py`, `sequence_export.py`, `sequence_review.py`, plus the exact-take helper `sequence_take.py` and the existing renderer/inventory/dialogue/preview consumers.

Validated source/fitted boards: [S01 opening](s01_opening/review.html), [empty hold](s01_empty_hold/review.html), [S02 acorn](s02_acorn/review.html), [S03 fork](s03_fork/review.html), [S05 trip](s05_trip/review.html). These boards display blockers, not approvals. The [new local fork candidate](local_fork_foundation_r001/review.html) is now owner-selected at exact r004 bytes.

`cpu_fixture_r005/TRACE.json` is the current retained synthetic integration proof. It records known red→green and green→blue input pixels reaching two actual renderer entrypoint invocations under a fake backend. Native captures/encoded tiny fixture clips and receipts live in that fixture folder. No real Wan model was used. Earlier fixture revisions are historical; do not treat their code hashes as current.

No runnable real-media production packet was emitted: required G2/G3 gates do not pass yet. Do not construct one by copying synthetic reviewer flags or by deleting blockers.
