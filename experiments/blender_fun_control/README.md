# Blender / Wan control experiments

Status: completed feasibility tests; [results and decision](RESULTS_2026-10-16.md).
All three stages ran on LUMI. Existing I2V remains the default recommendation.
No production integration. Agent B branch: `feature/video-control`.

Read in order:

1. [Current video state](../../docs/video-control-current-state.md)
2. [Experiment policy](../../docs/video-control-experiment-policy.md)
3. [LUMI validation and cost gate](LUMI_VALIDATION.md)
4. [Pilot selection](PILOT_SELECTION.md)
5. [Artifacts and proposed sidecar contract](ARTIFACTS.md)
6. [Risk register and comparison template](EVALUATION.md)

## Allocated experiment tools

The owner authorized inference and conditional Blender tests after the planning
phase. `run_env.sh` selects the isolated control environment; `run_case.py`
requires a SLURM allocation and writes a unique run directory/receipt.
`prepare_story.py` freezes source bytes and generates cheap Canny motion guides
on allocated compute. `blender_guide.py` tests an optional CPU image-plane mesh.
`inspect_comparison.py` creates contact sheets and diagnostic motion metrics.
All live results and job IDs belong in the execution log. Longer/native renders
use `comparison.sbatch` on small-g; short diagnostic scripts have hard caps and
are not bulk render drivers.

## Available local tool

From this worktree root, using Python 3.9+ (host `python3` here is only 3.6):

```bash
python3.11 experiments/blender_fun_control/audit_inputs.py \
  --start s01x_p03 --end s01_p04
```

It prints JSON to stdout, checks registered same-view/hold metadata and hashes
selected bytes plus planning documents. Exit 0 means only metadata/input
consistency; `production_eligible` remains false. It does not run the v6 gate,
inspect pictures, load model libraries, write files, or start a job. The real
v6 preflight remains independently required for production.

## Proposed implementation order

| Module under this directory | Responsibility | Gate |
|---|---|---|
| `audit_inputs.py` (implemented) | Read-only endpoint/geometry/hash audit | No GPU |
| `wan_control.py` (proposed) | Pinned external backend, capability report, explicit control tensor preprocessing | Approved backend feasibility job |
| `proxy_motion.py` (proposed) | Deterministic silhouettes/edge source and transform ledger | Backend consumes a reference control correctly |
| `blender_motion.py` (proposed) | Optional calibrated CPU/headless guide generation | Proxy comparison shows benefit and Blender adds value |
| `control_shot.py` (proposed) | Explicit experiment manifest, validation, non-overwriting run receipts | Proven backend and approved bounded pilot |

Keep new imports and environment setup local. Do not create placeholder
production modules that imply working inference. A future adapter must report
supported control types, image roles (reference/start/end), resolutions, frame
rules, dtype and attention path; unsupported options fail before allocation.
Future orchestration records failed attempts and resource use, with no silent
fallback that labels I2V output as controlled. Baseline rendering uses the
established `wan` API through an isolated experiment runner; a v6 image must
not be made renderable by inventing a production `story.yaml`.

Agent A owns framing and staging. Merge these additive experiment files after
its policy review, refresh pilot hashes, and re-evaluate suitability. There is
no integrated framing-policy conclusion here; no Agent C work was undertaken.

## Validation of this phase

```bash
python3.11 -m unittest discover -s experiments/blender_fun_control -p 'test_*.py' -v
```

Eight safeguard tests pass. All three selected pilots pass the local byte/hash
and geometry audit. A real camera cut (`s01_p01 → s01_p02`) and a conflicting
same-view candidate (`s15_p03 → s15x_p04`) exit 1 as expected. The independent
v6 preflight remains blocked (see LUMI note). No generated video has been
reviewed; there is no claim of successful control or Blender rendering.
