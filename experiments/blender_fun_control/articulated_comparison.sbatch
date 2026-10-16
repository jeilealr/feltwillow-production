#!/bin/bash
#SBATCH --job-name=fw_articulated_compare
#SBATCH --account=project_465002727
#SBATCH --partition=small-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=7
#SBATCH --mem=128G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_articulated_compare_%j.log
# Six 49-frame low-resolution feasibility clips, sequential on one GCD.
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
srun --ntasks=1 --gpus-per-task=1 bash experiments/blender_fun_control/run_env.sh experiments/blender_fun_control/run_articulated_comparison.py
