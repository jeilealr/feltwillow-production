#!/bin/bash
#SBATCH --job-name=fw_v7_dual_profile
#SBATCH --account=project_465002727
#SBATCH --partition=dev-g
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=7
#SBATCH --gpus-per-node=mi250:2
#SBATCH --mem=256G
#SBATCH --time=01:30:00
#SBATCH --output=/flash/project_465002727/jelealro/feltwillow-production/logs/dual_profile_%j.log
set -euo pipefail
LAUNCH=/flash/project_465002727/jelealro/feltwillow-production/launch/20261023
srun --ntasks=2 --cpus-per-task=7 --gpus-per-task=mi250:1 --kill-on-bad-exit=0 --output=/flash/project_465002727/jelealro/feltwillow-production/logs/dual_profile_%j_%t.log bash "$LAUNCH/profile_pair/task.sh"
