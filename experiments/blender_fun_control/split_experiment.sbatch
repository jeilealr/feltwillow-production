#!/bin/bash
#SBATCH --job-name=fw_split_experiment
#SBATCH --account=project_465002727
#SBATCH --partition=small-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-node=mi250:1
#SBATCH --cpus-per-task=7
#SBATCH --mem=96G
#SBATCH --time=00:40:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/fw_split_%j.log
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
driver="${1:?Pass a supported experiment runner}"
case "$driver" in
  run_i2v_followup.py|run_video_matrix.py|run_articulated_comparison.py) ;;
  *) echo 'Unsupported experiment runner' >&2; exit 2 ;;
esac
shift
srun --ntasks=1 --gpus-per-task=mi250:1 bash experiments/blender_fun_control/run_env.sh "experiments/blender_fun_control/$driver" "$@"
