#!/bin/bash
#SBATCH --job-name=fw_articulated_proxy
#SBATCH --account=project_465002727
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=7
#SBATCH --mem=16G
#SBATCH --time=00:15:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_articulated_proxy_%j.log
# First-run analytic IK / true-depth renderer diagnostic. No video inference.
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
srun bash experiments/blender_fun_control/run_blender.sh experiments/blender_fun_control/articulated_proxy.py
