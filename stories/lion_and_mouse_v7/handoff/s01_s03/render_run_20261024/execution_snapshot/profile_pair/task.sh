#!/bin/bash
set -euo pipefail
LAUNCH=/flash/project_465002727/jelealro/feltwillow-production/launch/20261023
case "$SLURM_PROCID" in
  0) SCENE=1; SHOT=s01_l001_b01_establish ;;
  1) SCENE=2; SHOT=s02_l004_b02_i02 ;;
  *) exit 2 ;;
esac
exec bash "$LAUNCH/run.sh" python "$LAUNCH/profile_pair/profile_shot.py" --story lion_and_mouse_v7 --scene "$SCENE" --shot "$SHOT" --fast
