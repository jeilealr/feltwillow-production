#!/bin/bash
#SBATCH --job-name=fw_video_matrix
#SBATCH --account=project_465002727
#SBATCH --partition=small-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=7
#SBATCH --mem=128G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_video_matrix_%j.log
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
recipe="${1:?Pass endpoint, seeds, representation, or depth_diagnostic}"
srun --ntasks=1 --gpus-per-task=1 bash experiments/blender_fun_control/run_env.sh experiments/blender_fun_control/run_video_matrix.py "$recipe"
