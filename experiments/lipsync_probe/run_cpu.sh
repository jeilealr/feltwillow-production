#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../.."
source lumi/site.sh
export TMPDIR="$FELTWILLOW_PROJECT/tmp/lipsync-probe/${SLURM_JOB_ID:-setup}"
export TMP="$TMPDIR" TEMP="$TMPDIR" APPTAINER_TMPDIR="$TMPDIR" SINGULARITY_TMPDIR="$TMPDIR"
export TORCH_HOME="$FELTWILLOW_PROJECT/models/lipsync_probe_alignment"
export XDG_CACHE_HOME="$FELTWILLOW_PROJECT/lipsync_probe_env/cache"
export NLTK_DATA="$FELTWILLOW_PROJECT/lipsync_probe_env/nltk_data"
export HF_HOME="$FELTWILLOW_PROJECT/hf_cache"
export PYTHONPATH="$FELTWILLOW_PROJECT/feltwillow-production/.venv-lipsync/lib/python3.12/site-packages:$PWD:$PWD/production"
export PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false
mkdir -p "$TMPDIR" "$TORCH_HOME" "$XDG_CACHE_HOME" "$NLTK_DATA"
exec singularity exec -B "$FELTWILLOW_BINDS" "$FELTWILLOW_SIF" /opt/miniconda3/envs/pytorch/bin/python "$@"
