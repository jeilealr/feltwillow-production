#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../.."
source lumi/site.sh
export XDG_CACHE_HOME="$FELTWILLOW_PROJECT/video_control_blender_env/cache"
export XDG_CONFIG_HOME="$FELTWILLOW_PROJECT/video_control_blender_env/config"
export BLENDER_USER_CONFIG="$XDG_CONFIG_HOME/blender"
export TMPDIR="$FELTWILLOW_PROJECT/tmp/video-control/blender_${SLURM_JOB_ID:-setup}_${SLURM_PROCID:-0}"
export TMP="$TMPDIR" TEMP="$TMPDIR"
export CUDA_VISIBLE_DEVICES='' HIP_VISIBLE_DEVICES='' ROCR_VISIBLE_DEVICES=''
mkdir -p "$XDG_CACHE_HOME" "$BLENDER_USER_CONFIG" "$TMPDIR"
exec "$FELTWILLOW_PROJECT/video_control_blender_env/bin/python" "$@"
