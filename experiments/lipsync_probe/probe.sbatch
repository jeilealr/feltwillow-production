#!/bin/bash
#SBATCH --job-name=fw_lipsync_video_diag
#SBATCH --account=project_465002727
#SBATCH --partition=dev-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-node=mi250:1
#SBATCH --cpus-per-task=7
#SBATCH --mem=96G
#SBATCH --time=00:30:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_lipsync_video_%j.log
# One first-run diagnostic: static/moving mouth-ROI behavior on two character close-ups.
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
srun --ntasks=1 --gpus-per-task=mi250:1 bash experiments/blender_fun_control/run_env.sh experiments/lipsync_probe/run_probe.py
