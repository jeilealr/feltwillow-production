#!/bin/bash
# Isolated control environment; production venv is read-only dependency input.
set -euo pipefail
cd "$(dirname "$0")/../.."
source lumi/site.sh
export HF_HUB_DISABLE_IMPLICIT_TOKEN=1
export PYTHONUNBUFFERED=1
export TOKENIZERS_PARALLELISM=false
export PYTHONPATH="$PWD/lumi/stubs:$FELTWILLOW_PROJECT/video_control_env/venv/lib/python3.12/site-packages:$FELTWILLOW_VENV_GEN/lib/python3.12/site-packages:$FELTWILLOW_PROJECT/ext/VideoX-Fun-video-control:$PWD${PYTHONPATH:+:$PYTHONPATH}"
export MIOPEN_USER_DB_PATH="$FELTWILLOW_PROJECT/video_control_env/miopen/${SLURM_JOB_ID:-setup}"
export MIOPEN_CUSTOM_CACHE_DIR="$MIOPEN_USER_DB_PATH"
mkdir -p "$MIOPEN_USER_DB_PATH"
exec singularity exec -B "$FELTWILLOW_BINDS" "$FELTWILLOW_SIF" \
  "$FELTWILLOW_PROJECT/video_control_env/venv/bin/python" "$@"
