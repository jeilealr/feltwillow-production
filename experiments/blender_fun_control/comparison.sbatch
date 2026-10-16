#!/bin/bash
#SBATCH --job-name=fw_control_compare
#SBATCH --account=project_465002727
#SBATCH --partition=small-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=7
#SBATCH --mem=128G
#SBATCH --time=06:00:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_control_compare_%j.log
# Explicit serial experiments: stop on failure. No production outputs.
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
for test_case in "$@"; do
  srun --ntasks=1 --gpus-per-task=1 bash experiments/blender_fun_control/run_env.sh experiments/blender_fun_control/run_case.py --case "$test_case"
done
