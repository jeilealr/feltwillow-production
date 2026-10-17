#!/bin/bash
#SBATCH --job-name=fw_native_resource_diag
#SBATCH --account=project_465002727
#SBATCH --partition=dev-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-node=mi250:1
#SBATCH --cpus-per-task=7
#SBATCH --mem=96G
#SBATCH --time=00:25:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_native_resource_diag_%j.log
# Capacity/phase-timing test: 81 frames at 480p, only two denoising steps.
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
srun --ntasks=1 --gpus-per-task=mi250:1 bash experiments/blender_fun_control/run_env.sh experiments/blender_fun_control/profile_native.py
