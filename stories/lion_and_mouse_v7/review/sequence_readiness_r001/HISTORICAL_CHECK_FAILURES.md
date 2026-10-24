# Superseded check failures

During implementation, focused runs exposed stale assumptions and fixture issues:

- Historical sidecar paths moved by the prior approved cleanup: fixed by the existing hash-checked archive lookup.
- Earlier performance totals/visual-role snapshots, a fixed audio-file count, and real binding hashes left inside a reset synthetic fixture: corrected with preserved behavioral assertions and coverage mapping.
- macOS `/var` versus `/private/var` temporary paths in a new test: compare resolved paths; the containment check itself remains strict.
- Localhost binding denied by the sandbox: rerun using the specific authorized sandbox exception, without GPU/model activity.

The latest authoritative runs are `focused-tests.log`, `performance-final.log`, `CHECKS.json` and `TEST_RESULTS.json`. Earlier failing logs and older retained CPU fixtures are historical evidence, not current passes or current blockers. No selected artwork/audio, historical receipt or video was changed to satisfy a test.
