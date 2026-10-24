# Resume on LUMI

From the existing repository clone, preserve any local work before updating:

```sh
git status --short
git branch --show-current
git pull --ff-only origin wan-new-image-approach
git log -1 --oneline
```

Continue on `wan-new-image-approach`; do not reset or overwrite divergent work. Read `AGENTS.md`, `CLAUDE.md`, `LUMI_CONTINUATION_HANDOFF.md` and this folder's implementation/test/adversarial records.

Verify the active **CPU** interpreter first (the Mac conda path is not portable):

```sh
command -v python
python -c "import sys; print(sys.executable); print(sys.prefix); import PIL, numpy, cv2; print('CPU dependencies available')"
python production/audio_visual_plan.py --story lion_and_mouse_v7 validate
python -m unittest tests.test_visual_grammar tests.test_r004_runtime tests.test_sequence_timeline tests.test_v7_dialogue tests.test_portrait_qa -q
python production/v7_dialogue.py inventory --story lion_and_mouse_v7
```

These commands are CPU-only and perform no downloads/model loading/submissions. Missing dependencies or unavailable media are actual host blockers; use the documented existing environment rather than running setup/install scripts automatically. Do not use the Mac-generated absolute runtime paths on LUMI. Recompile host-local packets only after scoped art, timing and capability gates pass.

Next engineering work: target-review invalidation regression; bounded local-effect frozen-CLI tests; production allocation/editor integration; complete C01–C52 mapping and browser board QA. Preserve old review/sequence_readiness_r001 and all historical receipts. Never run `lumi/render_story.sh` for new sequence jobs or retry an uncertain operation.

**Checkpoint validation:** focused V7/runtime/dialogue checks: **80 tests passed**. Full suite: **303 tests, 6 failures, 16 errors**; detailed output and limits are in TEST_RESULTS.json/full-tests.log. Do not describe the full suite as green. No source-media or old receipt changes were made.
