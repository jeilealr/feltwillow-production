#!/bin/bash
#SBATCH --job-name=fw_v7_s01_s03_flash
#SBATCH --account=project_465002727
#SBATCH --partition=small-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=7
#SBATCH --gpus-per-node=mi250:1
#SBATCH --mem=128G
#SBATCH --time=03:00:00
#SBATCH --array=0-25%26
#SBATCH --output=/flash/project_465002727/jelealro/feltwillow-production/logs/render_%A_%a.log
set -euo pipefail
cd /scratch/project_465002727/jelealro/feltwillow-production
LAUNCH=/flash/project_465002727/jelealro/feltwillow-production/launch/20261023
LINE=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" "$LAUNCH/tasks.txt")
[ -n "$LINE" ] || { echo "Missing task $SLURM_ARRAY_TASK_ID"; exit 1; }
echo "Job $SLURM_JOB_ID array $SLURM_ARRAY_JOB_ID task $SLURM_ARRAY_TASK_ID: $LINE"
srun --ntasks=1 --gpus-per-task=mi250:1 bash "$LAUNCH/run.sh" bash -c "$LINE"
