#!/bin/bash
# List generated assets and print two rsync commands to run on your computer.
#   bash lumi/backup_assets.sh [--dry-run]
#   KEEP_STEPS="500 750" FELTWILLOW_WORK=/scratch/... bash lumi/backup_assets.sh
# One source root is generated work; the other is tracked/owner-made character
# art in the repository. Separate relative file lists keep both rsync roots exact.
set -euo pipefail
MODE=${1:-}
if [ -n "$MODE" ] && [ "$MODE" != "--dry-run" ]; then
  echo "usage: $0 [--dry-run]" >&2
  exit 2
fi
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/site.sh"
cd "$FELTWILLOW_REPO"
WORK_ROOT=$(python3 -c 'from feltwillow.paths import WORK; print(WORK)')
echo "FELTWILLOW_WORK=$WORK_ROOT"
[ -d "$WORK_ROOT" ] || { echo "work root does not exist: $WORK_ROOT" >&2; exit 1; }
KEEP_STEPS=${KEEP_STEPS:-500}
for s in $KEEP_STEPS; do
  [[ "$s" =~ ^[0-9]+$ ]] || { echo "KEEP_STEPS must contain integers" >&2; exit 2; }
done
if [ "$MODE" = "--dry-run" ]; then
  LIST_DIR=$(mktemp -d)
  trap 'rm -rf "$LIST_DIR"' EXIT
else
  LIST_DIR="$WORK_ROOT"
fi
WORK_LIST="$LIST_DIR/backup_work_files.txt"
CHARACTER_LIST="$LIST_DIR/backup_character_files.txt"
(
  cd "$WORK_ROOT"
  {
    find . \( -path './lora/*/out_*' -o -path './lora/*/cache' \) -prune -o -type f -print
    for d in ./lora/*/out_*; do
      [ -d "$d" ] || continue
      for f in "$d"/*.safetensors; do
        [ -f "$f" ] || continue
        case ${f##*/} in *-step[0-9]*.safetensors) ;; *) echo "$f" ;; esac
      done
      for s in $KEEP_STEPS; do
        for f in "$d"/*-step"$(printf %08d "$s")".safetensors; do
          if [ -f "$f" ]; then echo "$f"; fi
        done
      done
    done
  } | sed 's|^./||' | awk '$0 != "backup_work_files.txt" && $0 != "backup_character_files.txt"' \
    | sort -u > "$WORK_LIST"
)
find character -type f \( -name '*.png' -o -name '*.jpg' -o -path '*/gemini/*' \) \
  | sort -u > "$CHARACTER_LIST"
WORK_COUNT=$(wc -l < "$WORK_LIST" | tr -d ' ')
CHARACTER_COUNT=$(wc -l < "$CHARACTER_LIST" | tr -d ' ')
echo "work root: $WORK_ROOT ($WORK_COUNT files)"
echo "character root: $FELTWILLOW_REPO ($CHARACTER_COUNT files)"
echo "work file list: $WORK_LIST"
echo "character file list: $CHARACTER_LIST"
if [ "$MODE" = "--dry-run" ]; then
  echo "dry run: no persistent lists written and no rsync invoked"
  exit 0
fi
DEST="./$(basename "$FELTWILLOW_REPO")_backup"
echo
echo "Run on your computer:"
echo "  rsync -av --files-from=:$WORK_LIST ${USER:-$(id -un)}@$FELTWILLOW_SSH_HOST:$WORK_ROOT/ $DEST/work/"
echo "  rsync -av --files-from=:$CHARACTER_LIST ${USER:-$(id -un)}@$FELTWILLOW_SSH_HOST:$FELTWILLOW_REPO/ $DEST/repository/"
