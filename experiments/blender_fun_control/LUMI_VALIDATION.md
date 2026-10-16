# LUMI validation — 2026-10-16

**Completed test results:** [2026-10-16 report](RESULTS_2026-10-16.md).
The original plan/assessment below is retained as context.

Historical initial assessment. The owner subsequently authorized tests;
see [execution log](EXECUTION_LOG.md) for actual measurements and current status.
The observations below describe discovery before downloads/jobs.

Initial decision: **GO for read-only planning/input audits; HOLD for control inference
and Blender**. No install, download, model load, render or SLURM submission
was performed. ROCm compatibility and visual benefit are unproven.

## Live evidence

| Probe | Observation | Meaning / limit |
|---|---|---|
| Original checkout | `/scratch/project_465002727/jelealro/feltwillow-production`, clean when inspected, branch `feature/perceptual-world`, commit `6fae81c` | Leave Agent A there |
| New worktree | `/scratch/project_465002727/jelealro/feltwillow-video-control`, branch `feature/video-control`, based on `6fae81c` | Independent checkout; no shared ignored assets |
| Host | `uan02`; host `python3` = 3.6.15; `python3.11` available | Use modern Python or existing container for repository commands |
| `FELTWILLOW_WORK` | Unset | Effective default is this worktree's `work/`; original checkout has a different default |
| Container wrapper, metadata query | Python 3.12.11; torch 2.7.1+rocm6.2.4; diffusers 0.39.0; transformers 4.51.3; flash-attn 2.7.3 | Package versions verified without model/GPU execution; flash-attn installation is not a compatibility result |
| Container | `/appl/local/containers/sif-images/lumi-pytorch-rocm-6.2.4-python-3.12-pytorch-v2.7.1.sif` exists and wrapper executes | Retain baseline venv; do not upgrade it for Control |
| Venv | `/scratch/project_465002727/jelealro/ltx_env/venv`; Python target lives inside container | Host invocation of the venv executable is not the supported path |
| Cache inventory | I2V/T2V Wan2.2, Lightning and other repos under `hf_cache/hub`; no `alibaba-pai` Fun Control entry | Names only: completeness of existing cached snapshots not certified; other locations not exhaustively scanned |
| Blender | `command -v blender` empty; `module spider Blender` reports not found; bounded module availability query has no match | No usable Blender proven, including CPU/headless; no install attempted |
| Scheduler | `sinfo -s`: debug 30 min, dev-g 3 h, small/small-g 3 days, standard/standard-g 2 days, all up | Limits observed, not permission to use full debug time or proof of project entitlement |
| Queue | `squeue -u jelealro` empty | No current jobs at inspection; one ordinary dev job at a time remains the policy |
| Storage | `df -h`: ~314 TB free on shared Lustre; `lfs quota -g project_465002727 /pfs/lustrep4` returned group usage, quota/limit columns 0/default | Shared free space and this quota response do not certify personal/project allocatable headroom; verify project quota and inode budget before staging |
| Read-only v6 preflight | Existing wrapper; exit 1, **1572 blockers**, 81 historical provenance warnings; no files written | Snapshot-specific full gate failure, not 1572 image judgments |

Preflight command used, from this worktree:

```bash
bash lumi/run_in_container.sh python production/v6_runtime.py \
  --story lion_and_mouse_v6 --preflight
```

Output includes pending size-anchor approval and the acorn's pending prop
approval. The new worktree also has no ignored audio copied into its default
work root. The gate count is local-context dependent; rerun with the intended
absolute work root before any later production readiness claim. Missing audio
is tolerated in read-only mode under the runtime contract, but export requires
local bytes. No review fields were filled to make this command pass.

The outer command sandbox fails with Bubblewrap namespace ENOSPC. Approved
unsandboxed commands were used for this inspection; that issue says nothing
about ROCm or model feasibility.

## Backend routes and evidence

Prefer a pinned **VideoX-Fun Python** route for the first compatibility audit.
The publisher's actual example is
[`examples/wan2.2_fun/predict_v2v_control_ref.py`](https://github.com/aigc-apps/VideoX-Fun/blob/main/examples/wan2.2_fun/predict_v2v_control_ref.py),
using `Wan2_2FunControlPipeline`, a control video and reference-image input.
It exposes start/end variables too; their presence does not prove combined
endpoint preservation. Inspect the pinned pipeline and preprocessing utilities
before adapting. Default example optimizations must be reviewed rather than
blindly copied. Use bf16 and a tested ROCm-compatible attention/offload path;
first disable optional quantization, compile and caching accelerations.
ROCm support for this exact stack has **not** been demonstrated here.

The [official ComfyUI tutorial](https://docs.comfy.org/tutorials/video/wan/wan2-2-fun-control)
provides a reproducible workflow, a start image and already-preprocessed control
video. Its illustrated route uses scaled FP8 models, high/low-noise experts
and an optional acceleration LoRA, measured on NVIDIA. Keep it as a workflow
reference or secondary headless candidate; its timings/kernels are not MI250X
evidence. Reference-image conditioning and a fixed first frame are different
capabilities and must be measured separately. Do not assume baseline style
LoRAs work because a particular acceleration LoRA appears in an official example.

The [publisher setup guide](https://github.com/aigc-apps/VideoX-Fun/blob/main/comfyui/wan2_2_fun/README.md)
lists A14B Control separately from InP and Control-Camera. It lists a **64 GB**
A14B package. That disk size is not an inference VRAM requirement. A newer 5B
Control option is also listed, but it has different timing/training conventions;
consider it only as a separately scoped alternative if A14B fails the budget.
No additional variant weights should be staged speculatively.

## Bounded next test, after owner authorization

First prepare a specific approval packet: exact backend commit/model revision,
file list and total bytes, environment lock, sample asset hashes/license,
attention/dtype/offload choices, supported dimensions/frame counts, project
quota evidence, resource request, hypothesis and stop time.

Planning estimates, **not measurements or submitted requests**:

- Reserve roughly **150 GB** scratch headroom for one ~64 GB package, environment,
  download/transient files and small outputs. Recalculate from actual files;
  avoid duplicating shared encoders/caches without hash proof.
- Start with one process and **one 64 GB GCD**, 7 CPU cores and approximately
  **128 GB host RAM** as a provisional offload envelope. Baseline needs
  ~80–100 GB; new backend may exceed it. Confirm current CPU/GPU/memory allocation
  constraints before requesting; increasing RAM/GCDs requires a revised estimate.
- One short `dev-g` diagnostic, e.g. at most **30 min / 0.5 GCD-hour**, tests
  import, load, precision and control encoding. Stop on unsupported kernels/OOM
  or exhausted budget. Loading itself may consume most of this time; no promise
  of a generated clip. Do not repeatedly resubmit to complete a long render.
- One reference render, when justified, uses **small-g**, provisionally up to
  **4 h / 4 GCD-hours** including cold load. Prefer the selected backend's
  documented reference dimensions/timing; no arbitrary frame truncation.
  Capture load time, peak HBM/host RSS and step throughput. This is a cap, not a
  performance forecast. Stop and re-estimate if throughput misses the cap.
- A later story A/B pair could consume up to **8 GCD-hours** at that cap and
  should be serial on small-g. Do not authorize all three pilots as a batch.
  Existing baseline 720p/81-frame/40-step experience is around two hours, not
  a forecast for the new backend or lower-resolution comparison.

Use the officially compatible sample before any custom guide. To establish
that control matters, change only the control sequence within the same backend
(e.g. stationary versus moving, with all other settings fixed), then compare
the useful configuration to baseline I2V. A single plausible output is not
proof of control. If the diagnostic or reference render cannot fit a genuinely
short test, use small-g from the start. Any later Blender CPU smoke test belongs
on an allocation; CPU bulk rendering belongs on small/standard.

## Current primary references

Checked 2026-10-16; pin implementation revisions before executing:

- [LUMI partitions and permitted purposes](https://docs.lumi-supercomputer.eu/runjobs/scheduled-jobs/partitions/)
- [LUMI-G hardware: one Slurm GPU is one 64 GB GCD](https://docs.lumi-supercomputer.eu/hardware/lumig/)
- [Control model card](https://huggingface.co/alibaba-pai/Wan2.2-Fun-A14B-Control)
- Publisher and ComfyUI implementation links above.
