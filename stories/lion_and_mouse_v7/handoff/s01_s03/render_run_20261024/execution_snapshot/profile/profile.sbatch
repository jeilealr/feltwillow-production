#!/bin/bash
#SBATCH --job-name=fw_v7_time_memory
#SBATCH --account=project_465002727
#SBATCH --partition=dev-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=7
#SBATCH --gpus-per-node=mi250:1
#SBATCH --mem=192G
#SBATCH --time=01:00:00
#SBATCH --output=/flash/project_465002727/jelealro/feltwillow-production/logs/profile_%j.log
set -euo pipefail
LAUNCH=/flash/project_465002727/jelealro/feltwillow-production/launch/20261023
srun --ntasks=1 --gpus-per-task=mi250:1 bash "$LAUNCH/run.sh" python "$LAUNCH/profile/profile_shot.py" --story lion_and_mouse_v7 --scene 1 --shot s01_l001_b01_i02 --fast
