#!/bin/bash
# Isolated control environment; production venv is read-only dependency input.
set -euo pipefail
cd "$(dirname "$0")/../.."
source lumi/site.sh
# All temporary/cache data stay on scratch; never use login-node /tmp.
export TMPDIR="$FELTWILLOW_PROJECT/tmp/video-control/${SLURM_JOB_ID:-setup}_${SLURM_PROCID:-0}"
export TMP="$TMPDIR" TEMP="$TMPDIR"
export APPTAINER_TMPDIR="$TMPDIR" SINGULARITY_TMPDIR="$TMPDIR"
export XDG_CACHE_HOME="$FELTWILLOW_PROJECT/video_control_env/cache"
export PIP_CACHE_DIR="$FELTWILLOW_PROJECT/video_control_env/pip_cache"
mkdir -p "$TMPDIR" "$XDG_CACHE_HOME" "$PIP_CACHE_DIR"
# Inference only: all required weights must already be staged explicitly.
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export HF_HUB_DISABLE_TELEMETRY=1
export HF_HUB_DISABLE_IMPLICIT_TOKEN=1
export PYTHONUNBUFFERED=1
export TOKENIZERS_PARALLELISM=false
export PYTHONPATH="$PWD/lumi/stubs:$FELTWILLOW_PROJECT/video_control_env/venv/lib/python3.12/site-packages:$FELTWILLOW_VENV_GEN/lib/python3.12/site-packages:$FELTWILLOW_PROJECT/ext/VideoX-Fun-video-control:$PWD${PYTHONPATH:+:$PYTHONPATH}"
export MIOPEN_USER_DB_PATH="$FELTWILLOW_PROJECT/video_control_env/miopen/${SLURM_JOB_ID:-setup}"
export MIOPEN_CUSTOM_CACHE_DIR="$MIOPEN_USER_DB_PATH"
mkdir -p "$MIOPEN_USER_DB_PATH"
exec singularity exec -B "$FELTWILLOW_BINDS" "$FELTWILLOW_SIF" \
  "$FELTWILLOW_PROJECT/video_control_env/venv/bin/python" "$@"
