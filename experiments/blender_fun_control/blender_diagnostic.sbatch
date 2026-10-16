#!/bin/bash
#SBATCH --job-name=fw_blender_cpu_diag
#SBATCH --account=project_465002727
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=7
#SBATCH --mem=16G
#SBATCH --time=00:15:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_blender_cpu_diag_%j.log
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
export XDG_CACHE_HOME=/scratch/project_465002727/jelealro/video_control_blender_env/cache
export XDG_CONFIG_HOME=/scratch/project_465002727/jelealro/video_control_blender_env/config
export BLENDER_USER_CONFIG="$XDG_CONFIG_HOME/blender"
export TMPDIR=/scratch/project_465002727/jelealro/video_control_blender_env/tmp
mkdir -p "$XDG_CACHE_HOME" "$BLENDER_USER_CONFIG" "$TMPDIR"
srun /scratch/project_465002727/jelealro/video_control_blender_env/bin/python experiments/blender_fun_control/blender_guide.py
