# Sourced inside the container (run_in_container.sh): the generation venv.
# Exports are defaults (${VAR:-...}), so a caller's value wins, except the two
# forced below. Fails (return 1) when the venv is missing, rather than letting
# the command run on the container's own, different library versions.
source "/pfs/lustrep4/scratch/project_465002727/jelealro/feltwillow-production/lumi/site.sh"
export HF_HUB_DISABLE_IMPLICIT_TOKEN=${HF_HUB_DISABLE_IMPLICIT_TOKEN:-1}
export PYTHONUNBUFFERED=${PYTHONUNBUFFERED:-1}
export TOKENIZERS_PARALLELISM=${TOKENIZERS_PARALLELISM:-false}
export LC_ALL=C.UTF-8 LANG=C.UTF-8      # forced: the caller's locale may not exist in the container
${WITH_CONDA:-}                         # the container's conda environment (its PyTorch)
source "$FELTWILLOW_VENV_GEN/bin/activate" || { echo "no venv at $FELTWILLOW_VENV_GEN: run lumi/setup_env.sh" >&2; return 1; }
# MIOpen kernel cache: /tmp on some GPU nodes is full/unwritable (job 22225720 died with
# "Cannot open database file:/tmp/gfx90a6e.ukdb"), so keep it on scratch, per job and task.
# Forced, not a default: a /tmp value set by the container or the caller would bring that back.
export MIOPEN_USER_DB_PATH=/flash/project_465002727/jelealro/feltwillow-production/cache/miopen/${SLURM_JOB_ID:-login}_${SLURM_PROCID:-0}
export MIOPEN_CUSTOM_CACHE_DIR=$MIOPEN_USER_DB_PATH
mkdir -p "$MIOPEN_USER_DB_PATH"
