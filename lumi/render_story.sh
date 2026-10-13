#!/bin/bash
# Receipt-aware fast render of every shot in a legacy story.yaml runtime.
#   bash lumi/render_story.sh lion_and_mouse_v5 --inventory-only
# Existing stale media stops submission; review and move it aside explicitly.
set -euo pipefail
STORY=${1:?story slug}
[[ "$STORY" =~ ^[a-z0-9_]+$ ]] || { echo "invalid story slug: $STORY" >&2; exit 2; }
MODE=${2:-}
if [ -n "$MODE" ] && [ "$MODE" != "--inventory-only" ]; then
  echo "usage: $0 <story slug> [--inventory-only]" >&2
  exit 2
fi
PER_TASK=${PER_TASK:-3}
[[ "$PER_TASK" =~ ^[1-9][0-9]*$ ]] || { echo "PER_TASK must be positive" >&2; exit 2; }
cd "$(dirname "$0")/.."
source lumi/site.sh
WORK_ROOT=$(python3 -c 'from feltwillow.paths import WORK; print(WORK)')
echo "FELTWILLOW_WORK=$WORK_ROOT"
TASK_DIR="$WORK_ROOT/tasks"
mkdir -p "$TASK_DIR"
INVENTORY="$TASK_DIR/${STORY}_render_inventory.json"
COMMANDS="$TASK_DIR/${STORY}_commands.txt"
LINES="$TASK_DIR/${STORY}_lines.txt"
NAME="feltwillow_${STORY##*_}"

inventory() {
  python3 production/render_story_inventory.py --story "$STORY" \
    --output "$INVENTORY" --commands "$COMMANDS"
}

submit_all() {
  local per=$1 f k
  [ -s "$COMMANDS" ] || return 0
  rm -f "$TASK_DIR/${STORY}_part_"*
  paste -d';' $(printf -- '- %.0s' $(seq "$per")) < "$COMMANDS" \
    | sed 's/;;*$//; s/;/ ; /g' > "$LINES"
  split -l 4 -d "$LINES" "$TASK_DIR/${STORY}_part_"
  for f in "$TASK_DIR/${STORY}_part_"*; do
    [ -f "$f" ] || continue
    while [ "$(squeue -u "$USER" -h -p dev-g | wc -l)" -ge 2 ]; do sleep 60; done
    k=$(grep -c . "$f")
    sbatch --ntasks="$k" --gpus-per-node="$k" --mem=$((k * 110))G -J "$NAME" lumi/run_tasks.sbatch "$f"
    sleep 30
  done
  while squeue -u "$USER" -h -o %j | grep -qx "$NAME"; do sleep 60; done
}

inventory
[ "$MODE" = "--inventory-only" ] && exit 0
for round in 1 2 3; do
  n=$(wc -l < "$COMMANDS")
  [ "$n" -eq 0 ] && { echo "all renders verified complete"; exit 0; }
  echo "$(date '+%F %T') round $round: $n shots need rendering"
  if [ "$round" -eq 1 ]; then submit_all "$PER_TASK"; else submit_all 1; fi
  inventory
done
n=$(wc -l < "$COMMANDS")
echo "$(date '+%F %T') done: $n shots still missing a seed"
[ "$n" -eq 0 ]
