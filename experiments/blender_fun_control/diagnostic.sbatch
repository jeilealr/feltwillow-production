#!/bin/bash
#SBATCH --job-name=fw_control_diag
#SBATCH --account=project_465002727
#SBATCH --partition=dev-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=7
#SBATCH --mem=128G
#SBATCH --time=00:30:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_control_diag_%j.log
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
srun --ntasks=1 --gpus-per-task=1 bash experiments/blender_fun_control/run_env.sh experiments/blender_fun_control/run_case.py --case diagnostic
