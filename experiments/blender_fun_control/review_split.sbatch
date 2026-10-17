#!/bin/bash
#SBATCH --job-name=fw_split_reviews
#SBATCH --account=project_465002727
#SBATCH --partition=small
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=00:15:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_split_reviews_%j.log
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
srun bash experiments/blender_fun_control/run_env.sh experiments/blender_fun_control/review_split.py
