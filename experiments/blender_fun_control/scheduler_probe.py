#!/usr/bin/env python3
"""Read-only queue investigation. sbatch is always called with --test-only."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]


def capture(command):
    result=subprocess.run(command,cwd=ROOT,text=True,capture_output=True,check=False)
    return dict(command=command,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',nargs='+',type=int,default=[22914092,22915166,22916690,22916691,22916692])
    args=parser.parse_args()
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control'/('scheduler_probe_'+stamp)
    out.mkdir(exist_ok=False)
    jobs=','.join(map(str,args.jobs))
    result=dict(timestamp_utc=stamp,read_only=True,actual_jobs_submitted=0,
        caveat='Hypothetical new-job estimates are volatile and do not predict existing jobs with accumulated priority. Smaller requests do not guarantee an earlier start.',
        queue=capture(['squeue','-j',jobs,'-o','%.18i %.12P %.30j %.8T %.10M %.10l %.30R']),
        start_estimates=capture(['squeue','--start','-j',jobs]),
        priorities=capture(['sprio','--jobs='+jobs]),
        job_details=[capture(['scontrol','show','job',str(job)]) for job in args.jobs],probes=[])
    for wall,memory in [('00:15:00','96G'),('00:30:00','96G'),('01:00:00','96G'),('02:00:00','96G'),('00:30:00','128G')]:
        result['probes'].append(capture(['sbatch','--test-only','--partition=small-g',
            '--gpus-per-node=mi250:1','--cpus-per-task=7','--mem='+memory,'--time='+wall,
            'experiments/blender_fun_control/video_matrix.sbatch','endpoint']))
    (out/'receipt.json').write_text(json.dumps(result,indent=2))
    print(out/'receipt.json')
    for probe in result['probes']:print(probe['stderr'].strip() or probe['stdout'].strip())


if __name__=='__main__':main()
