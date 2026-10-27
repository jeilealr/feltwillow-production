# Resume Mac engineering / future production

Read current AGENTS/CLAUDE, this README, IMPLEMENTATION_STATUS, TEST_RESULTS and the latest independent review. Keep source/selection/history intact; do not restore oldcheckpoints.

Verified Mac CPU commands from repository root:

```sh
/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/audio_visual_plan.py --story lion_and_mouse_v7 validate
/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/check_sequence_requirements.py
/Users/lealroja/miniconda3/envs/feltwillow/bin/python -m unittest tests.test_sequence_package tests.test_sequence_editor tests.test_sequence_timeline tests.test_bounded_local_cli tests.test_portrait_readiness tests.test_v7_lipsync_dispatch -q
/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/sequence_package.py --help
/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/v7_dialogue.py inventory --story lion_and_mouse_v7
```

For a new full evidence run, use a NEW filename with `production/check_sequence_requirements.py --run --out`; existing execution evidence is preserved. Browser review: `production/serve_scene_review.py --gallery sequences --port 8768` is CPU/local only, may require Maclocalhost sandbox permission.

Next dependenttranche: resolve art/selection and reviewedword/physical event markers from BLOCKERS, re-evaluate scoped still/timing gates, freeze a new eligible diagnostic or production packet, then build/verify a portable package using trusted checkout code. Do not execute a package's own verifier before trustvalidation. Record package/results digests outside transferred data. No realpacket is currently ready for GPU submission.

Future host: ordinaryPython/Slurm launchadapter in `lumi/sequence_job.sbatch`, no interactiveCodex. Resources/environment and exactoperation authorization must be verified separately. Keep external journal across restarts, no resubmission of claimed/uncertain jobs, no model downloads. Results collect→verify-results→pending take proposals supports return to Mac without rewriting originalreceipts. Final production or assembly requires actual visualreview and separate ownerauthority.

Current work is intentionally uncommitted: latest request did not grant a new commit/push. No source art/voice/media has changed.
