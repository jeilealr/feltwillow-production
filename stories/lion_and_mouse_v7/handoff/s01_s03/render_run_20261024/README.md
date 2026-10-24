# Completed S01-S03 LUMI pilot run — 24 October 2026

All 26 original selected-image animation pilots completed. Each has a receipt matching its selected input and decoded as 81 frames at 1280×720, 16 fps. [Exact output hashes and receipt index](manifest.json). This is technical completion, not owner video-take selection or a narration-aligned final edit. New GitHub image coverage is separate.

The videos remain outside Git at `/flash/project_465002727/jelealro/feltwillow-production-results/work/stories/lion_and_mouse_v7/shots/`. The initial scratch runs timed out with quota/LLVM write errors. A 64 MiB flash write test and all dry runs passed before rendering there. Inputs, model weights and Lightning revisions stayed fixed. Models were read offline from the existing cache; outputs, logs, bytecode, MIOpen and compiler caches used flash.

The single-GCD profile (job 23111311) took 51 min 30 sec including model loading (~35 min 37 sec), generation (~15 min 16 sec) and encoding (~13 sec). Python process peak host RSS was 94.7 GiB, peak GPU allocation 36.7 GiB (43.4 GiB reserved). Two concurrent profiled clips (job 23112337) completed in 46 min 23 sec within a shared 256 GiB host allocation. Separate profiles are retained under `profiles/`; these are measured results for these exact recipes, not timing guarantees.

The remaining clips completed two at a time on dev-g at the owner's explicit direction. The controller (23118532) verified each pair's receipts and decoded frames before releasing the next; all completed at 09:20:58 EEST on 24 October. Scheduler accounting/QOS and time limits still apply. Routine future bulk work belongs on the ordinary production partitions unless explicitly directed otherwise.

`pilot_runtime.yaml` and `execution_snapshot/` preserve the historical run, not an active replacement for the newly authored image/audio plan. Snapshot scripts contain old paths/job IDs; do not execute the controller against completed jobs. The accepted provisional tracked-mouth diagnostic is documented separately in [lip-sync](../../../../../docs/lip-sync.md); it has not been applied to these 26 clips.
