#!/bin/bash
set -euo pipefail
source /scratch/project_465002727/jelealro/feltwillow-production/lumi/site.sh
export TMPDIR=/flash/project_465002727/jelealro/feltwillow-production/tmp
export TMP="$TMPDIR" TEMP="$TMPDIR" APPTAINER_TMPDIR="$TMPDIR" SINGULARITY_TMPDIR="$TMPDIR"
export FELTWILLOW_WORK=/flash/project_465002727/jelealro/feltwillow-production/work
export XDG_CACHE_HOME=/flash/project_465002727/jelealro/feltwillow-production/cache
export PYTHONPYCACHEPREFIX="$XDG_CACHE_HOME/pycache"
export TORCHINDUCTOR_CACHE_DIR="$XDG_CACHE_HOME/torchinductor"
export TRITON_CACHE_DIR="$XDG_CACHE_HOME/triton"
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
cd "$FELTWILLOW_REPO"
exec singularity exec -B "$FELTWILLOW_BINDS" "$FELTWILLOW_SIF" bash -c 'source "$0" || exit 1; exec "$@"' /flash/project_465002727/jelealro/feltwillow-production/launch/20261023/env_render.sh "$@"
