#!/bin/bash
#SBATCH --job-name=fw_v7_pair_controller
#SBATCH --account=project_465002727
#SBATCH --partition=small
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=2-00:00:00
#SBATCH --output=/flash/project_465002727/jelealro/feltwillow-production/logs/controller_%j.log
set -euo pipefail
QUEUE=/flash/project_465002727/jelealro/feltwillow-production/launch/20261023/dev_g_queue
echo "Pair controller job $SLURM_JOB_ID on $(hostname); progress in $QUEUE/status.txt"
exec bash "$QUEUE/controller.sh" >> "$QUEUE/controller.log" 2>&1
