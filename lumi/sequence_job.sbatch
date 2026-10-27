#!/bin/bash
# Noninteractive execution only. Resource/account/partition directives must be
# supplied by an exact, approved host-specific Slurm request; none are inferred.
#SBATCH --job-name=feltwillow-sequence
#SBATCH --no-requeue
set -euo pipefail
: "${FELTWILLOW_REPO:?Set the trusted versioned checkout outside the untrusted package}"
: "${FELTWILLOW_PYTHON:?Set the verified existing host/container Python executable}"
if [ "$#" -ne 4 ]; then
  echo "usage: sequence_job.sbatch PACKAGE OPERATION DURABLE_JOURNAL AUTHORIZATION_JSON" >&2
  exit 2
fi
exec "$FELTWILLOW_PYTHON" "$FELTWILLOW_REPO/production/sequence_package.py" worker "$1" \
  --operation "$2" --journal "$3" --authorization "$4" --execute
