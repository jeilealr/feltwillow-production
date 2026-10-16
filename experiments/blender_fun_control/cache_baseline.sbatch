#!/bin/bash
#SBATCH --job-name=fw_baseline_cache
#SBATCH --account=project_465002727
#SBATCH --partition=small
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=00:30:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_baseline_cache_%j.log
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
srun bash experiments/blender_fun_control/run_env.sh experiments/blender_fun_control/cache_baseline_bf16.py
