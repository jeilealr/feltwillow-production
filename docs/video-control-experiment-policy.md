# Video-control experiment boundary

Agent B policy, 2026-10-16. Applies to optional video experiments, not image
creation or staging rules. Entry point:
[experiment README](../experiments/blender_fun_control/README.md).

## Opt-in and separation

Use only explicit experimental commands under `experiments/blender_fun_control/`.
Do not auto-select a control backend from production, change default Wan models,
reuse production output paths, or make legacy rendering depend on experimental
libraries. Keep a separate environment/cache namespace for any new dependencies;
never upgrade the established generation venv to satisfy Fun Control.

Every generated run uses a new directory:

```text
$FELTWILLOW_WORK/stories/<story>/experiments/blender_fun_control/<run_id>/
```

All receipts carry `production_eligible: false` and
`approval: isolated_experiment_not_for_production`. A receipt records provenance;
it is not a visual review. Do not overwrite an existing run or baseline receipt.
Version recipes in Git; keep media, weights, caches, environments and renders
on scratch, off HOME. Back up irreplaceable assets outside temporary scratch.

Consume current keyframe, plate, crop, staging and review data without changing
Agent A's framing/scale policy. Refresh hashes after Agent A merges. A candidate
may be used only as an explicitly labeled non-production test input. Neither
owner selection nor a metadata audit is a technical image approval. Never
interpolate a camera/location cut. Even a same-view label needs compatible
plate, view, crop, actor geometry and actual-pixel review.

## LUMI job purpose

The owner's LUMI email and the [current partition documentation](https://docs.lumi-supercomputer.eu/runjobs/scheduled-jobs/partitions/)
reserve `debug`/`dev-g` for debugging and quick tests. CPU `debug` is not a GPU
partition. Use one ordinary development job at a time; the two-job `dev-g`
allowance exists for heterogeneous-job testing and is not a throughput target.
A job does not become a test by putting it in an experiments directory.

| Work | Partition choice | Required description |
|---|---|---|
| Tiny CPU software/guide smoke test | `debug`, within current limit | One bounded question, expected result, stop time |
| One GPU import/load/kernel/control-input diagnostic | `dev-g`, if genuinely short | One hypothesis, one process/GCD, bounded budget |
| Longer feasibility render or A/B comparison | `small-g` | Explicit resources and wall time; still experimental |
| Routine story renders, seed sweeps, repeated comparisons | `small-g` or efficient `standard-g` allocation | Production/batch purpose |
| Repeated CPU guide rendering | `small` or efficient `standard` allocation | CPU budget and storage estimate |

Check `scontrol show partition` before submission. A partition's maximum time
is a scheduler limit, not an appropriate target for a quick test. Never split
production into repeated test jobs or use a second job to work around limits.
Use allocated compute for inference/rendering, not the login node. LUMI-D
visualization GPUs are not an alternative CUDA inference resource.

**Legacy hazard:** `lumi/run_tasks.sbatch` still defaults to `dev-g`, and
`lumi/render_story.sh` explicitly throttles/submits bulk work there. Do not use
that bulk submission path for production. Inventory-only is safe. A separately
reviewed scheduler migration is needed before bulk use. For a manually reviewed
production task file, an explicit `sbatch --partition=small-g ...
lumi/run_tasks.sbatch <tasks>` overrides the old default; size RAM/CPU/GCDs and
time for the actual workload. This phase leaves scheduler code unchanged.

## Work gates

Read-only discovery and this local audit are authorized. No model downloads,
installs or jobs were performed. The source handoff requires a cost estimate
and owner authorization before expensive downloads/jobs. Prepare a pinned
backend recipe, actual file inventory, quota headroom and bounded job request
before seeking that next decision. Backend proof precedes custom proxy guides;
Blender follows only if those guides demonstrate value.

Production adoption is a separate explicit decision after ROCm validation,
visual A/B review, end-image capability testing and v6 governance. Never infer
end-frame compatibility or reuse style/Lightning LoRAs without a matching test.
