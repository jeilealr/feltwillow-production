**Update — r004 accepted:** Owner selected S03-L001-B01-I02 r004 (`5163cea0a436d27ec4b1ea4a16c857b5ffdb504a0309d587fe34d84a7d2beee6`). Current ledger now points to r004; original r003 and creation-time records remain preserved. Next work is the compatible dependent fork tranche. Earlier pending-selection statements below describe the preparation snapshot.

# Resume this run

Repository: `/Users/lealroja/Documents/feltwillow/feltwillow-production`, branch `wan-new-image-approach`, starting/current committed HEAD `5214e701697498ab272f317e28c1ace47c7835e3`. Working-tree implementation is uncommitted. Preserve it; do not reset, switch branches, stage, push or publish without a new applicable instruction.

Read `COMPLETION.md`, `IMPLEMENTATION_STATUS.json`, `DECISIONS.md` and `BLOCKER_PACKET.md` first. These records do not grant spending or selection authority.

**Next dependent action:** review [the one local fork foundation](local_fork_foundation_r001/review.html), S03-L001 r004, SHA256 `5163cea0a436d27ec4b1ea4a16c857b5ffdb504a0309d587fe34d84a7d2beee6`. Old r003 remains selected. Do not reuse the superseded paid fork card. After a new exact owner decision, refresh affected selections/uses/edges and prepare the smallest dependent repair tranche. S02 support/rise and real phrase alignment remain separate blockers.

Verified Mac interpreter: `/Users/lealroja/miniconda3/envs/feltwillow/bin/python`. The following are CPU-only and do not submit or retry jobs:

```sh
cd /Users/lealroja/Documents/feltwillow/feltwillow-production
/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/audio_visual_plan.py --story lion_and_mouse_v7 validate
/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/audio_visual_plan.py --story lion_and_mouse_v7 readiness --sequence s01_empty_hold --stage realization
/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/sequence_plan.py --story lion_and_mouse_v7 --sequence s03_fork
/Users/lealroja/miniconda3/envs/feltwillow/bin/python stories/lion_and_mouse_v7/review/sequence_readiness_r001/offline_fixture.py --out stories/lion_and_mouse_v7/review/sequence_readiness_r001/cpu_fixture_r005
```

The last command verifies/reuses the existing matching CPU fixture and repeats no calls. If code or retained files differ, it fails and requires a fresh unused revision; never overwrite old evidence. Synthetic renderer argv records are not LUMI commands and must not be executed outside the fake-backend harness.

Only when actual source/media changes require fresh evidence, the following CPU command recomputes hashes, audio PCM, native/fitted boards and full historical video decode; it writes this run's derived evidence:

```sh
/Users/lealroja/miniconda3/envs/feltwillow/bin/python stories/lion_and_mouse_v7/review/sequence_readiness_r001/refresh_evidence.py --baseline-decode
```

Source/fit pages and the candidate comparison are linked from the preferred selected-scene gallery. Restart an older running review server after code changes if it predates the new allowlist; the tested current server registers sequence pages explicitly and supports video range requests. Localhost binding may require the tool sandbox exception. This is not GPU authorization.

Real media are often Git-ignored. On a repo-only/other machine, verify exact PNG/WAV/MP4 availability using the manifests; metadata does not supply missing bytes. The parent's `/Users/lealroja/Documents/feltwillow/work` contains the downloaded 26 historical pilots. Frozen Mac absolute paths must not be silently rewritten into LUMI paths. Compile a real run on its intended execution host after inputs/reviews are ready.

**Do not rerun:** `prepare_local_foundation.py` (already completed, refuses overwrite), old single-image pilot exports, the superseded paid fork request, uncertain historical forward-pitch requests, `lumi/render_story.sh` for a new sequence, setup/install/download scripts, or GPU commands. No new ready/authorized production run exists. A baseline decode or matching receipt is not a full-motion pass, selected take or final assembly approval.
