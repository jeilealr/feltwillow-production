#!/bin/bash
#SBATCH --job-name=fw_baseline_compare
#SBATCH --account=project_465002727
#SBATCH --partition=small-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=7
#SBATCH --mem=128G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_baseline_compare_%j.log
# Longer baseline load/render, kept out of dev-g. Prefer verified storage cache.
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
cache=/scratch/project_465002727/jelealro/models/video_control_baseline_bf16/596658fd9ca6b7b71d5057529bbf319ecbc61d74
extra=()
[ ! -f "$cache/conversion_receipt.json" ] || extra=(--baseline-bf16-cache)
srun --ntasks=1 --gpus-per-task=1 bash experiments/blender_fun_control/run_env.sh experiments/blender_fun_control/run_case.py --case baseline --run-name baseline_smoke_33_smallg --frames 33 --width 416 --height 240 --steps 28 "${extra[@]}"
