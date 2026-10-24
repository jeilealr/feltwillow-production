#!/bin/bash
# Authorized two-at-a-time dev-g queue for the remaining v7 S01-S03 clips.
set -euo pipefail
LAUNCH=/flash/project_465002727/jelealro/feltwillow-production/launch/20261023
QUEUE=$LAUNCH/dev_g_queue
ARRAY=23111104
TASKS=(2 3 4 5 6 7 8 9 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25)
exec 9>"$QUEUE/controller.lock"
flock -n 9 || { echo 'Another controller already holds the lock'; exit 1; }
log() { echo "$(date -Iseconds) $*"; }
status() { printf '%s\n' "$(date -Iseconds) $*" > "$QUEUE/status.txt"; }
finished=0
trap 'rc=$?; if [ "$finished" -ne 1 ]; then status "STOPPED exit=$rc; inspect controller.log"; fi' EXIT
cd /scratch/project_465002727/jelealro/feltwillow-production
log 'Starting dev-g controller; limit two submitted/running clips, advance after both finish'
# Hold remaining small-g jobs so this controller exclusively decides their start.
for index in "${TASKS[@]}"; do
    job=${ARRAY}_${index}
    live=$(squeue -h -j "$job" -o '%P|%T' 2>/dev/null || true)
    if [[ "$live" == 'small-g|PENDING' ]]; then
        scontrol hold "$job"
        log "Held $job on small-g pending its dev-g turn"
    fi
done
completed=0
for ((offset=0; offset<${#TASKS[@]}; offset+=2)); do
    batch=("${TASKS[@]:offset:2}")
    [ ! -f "$QUEUE/STOP" ] || { log 'STOP requested'; exit 0; }
    status "Preparing batch=${batch[*]} completed=$completed/23"
    for index in "${batch[@]}"; do
        job=${ARRAY}_${index}
        live=$(squeue -h -j "$job" -o '%P|%T' 2>/dev/null || true)
        if [[ "$live" == 'small-g|PENDING' ]]; then
            scontrol update JobId="$job" Partition=dev-g TimeLimit=01:30:00
            scontrol release "$job"
            log "Moved/released $job on dev-g"
        elif [[ "$live" == 'dev-g|PENDING' || "$live" == 'dev-g|RUNNING' || "$live" == 'dev-g|CONFIGURING' || -z "$live" ]]; then
            log "Using current state of $job: ${live:-not in live queue}"
        else
            log "Unexpected state $job: $live; stopping to avoid duplicates"
            exit 1
        fi
    done
    while :; do
        [ ! -f "$QUEUE/STOP" ] || { log 'STOP requested'; exit 0; }
        all_done=1
        summary=''
        for index in "${batch[@]}"; do
            job=${ARRAY}_${index}
            record=$(sacct -X -n -P -j "$job" -o State,ExitCode | head -1)
            state=${record%%|*}
            state=${state//[[:space:]]/}
            summary+=" $job=${state:-WAITING_ACCOUNTING}"
            case "$state" in
                COMPLETED) ;;
                FAILED*|CANCELLED*|TIMEOUT*|OUT_OF_MEMORY*|NODE_FAIL*|BOOT_FAIL*|PREEMPTED*|DEADLINE*)
                    log "Render did not complete: $job $record"
                    exit 1 ;;
                *) all_done=0 ;;
            esac
        done
        status "Batch=${batch[*]} completed=$completed/23;$summary"
        [ "$all_done" -eq 1 ] && break
        sleep 30
    done
    log "Both tasks completed; verifying batch ${batch[*]}"
    bash "$LAUNCH/run.sh" python "$QUEUE/verify_batch.py" "${batch[@]}"
    completed=$((completed+${#batch[@]}))
    log "Verified $completed/23 remaining clips"
done
finished=1
status 'COMPLETE: all 23 queued clips finished and passed receipt/frame checks; three prior clips already saved'
log 'All requested renders complete'
