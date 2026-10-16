#!/bin/bash
#SBATCH --job-name=fw_i2v_continuity
#SBATCH --account=project_465002727
#SBATCH --partition=small-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=7
#SBATCH --mem=128G
#SBATCH --time=01:30:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_i2v_continuity_%j.log
# Three four-step 81-frame 832x480 clips; one load and one GCD, sequential.
# Longer comparison belongs on the regular partition, not dev-g.
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
srun --ntasks=1 --gpus-per-task=1 bash experiments/blender_fun_control/run_env.sh experiments/blender_fun_control/run_i2v_followup.py
