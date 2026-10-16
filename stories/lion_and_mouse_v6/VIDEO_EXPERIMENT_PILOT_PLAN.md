# V6 isolated video experiment plan

Agent B, 2026-10-16. Status: planning and read-only input tooling; no renders.

The complete [pilot selection](../../experiments/blender_fun_control/PILOT_SELECTION.md)
proposes three candidates: Milo/acorn same-view pose (`s01x_p03 → s01_p04`),
Milo dialogue portrait hold (`s08_p03`), and the user-liked shared close hold
(`s05_p03`). All remain explicitly non-production and subject to current
technical reviews and Agent A's framing-policy assessment.

Read the [current-state audit](../../docs/video-control-current-state.md),
[experiment boundary](../../docs/video-control-experiment-policy.md),
[LUMI feasibility report](../../experiments/blender_fun_control/LUMI_VALIDATION.md),
[artifact proposal](../../experiments/blender_fun_control/ARTIFACTS.md) and
[stop/go scorecard](../../experiments/blender_fun_control/EVALUATION.md).
The runtime contract, staging, image prompts and approval ledgers are unchanged.
A control experiment never grants permission to export or replace story media.

Next action after a reviewed cost/resource decision: prove the separate backend
with an official reference input on LUMI ROCm before custom guides or Blender.
Use debug/dev-g only for a genuinely short diagnostic. Longer comparisons and
production runs use suitable small/standard partitions. No downloads or jobs
were performed by this phase.
