"""Profile one unchanged production render; outputs and receipts stay standard."""
import hashlib
import json
import os
from pathlib import Path
import resource
import runpy
import sys
import threading
import time
import traceback

started=time.perf_counter()
repo=Path('/scratch/project_465002727/jelealro/feltwillow-production')
sys.path.insert(0,str(repo))
base=Path('/flash/project_465002727/jelealro/feltwillow-production')
out=base/'profiles'/(os.environ.get('SLURM_JOB_ID','manual')+'_'+os.environ.get('SLURM_PROCID','0'))
out.mkdir(parents=True,exist_ok=True)
report=dict(status='starting',job_id=os.environ.get('SLURM_JOB_ID'),arguments=sys.argv[1:],
    requested_host_memory=os.environ.get('SLURM_MEM_PER_NODE'),task_rank=os.environ.get('SLURM_PROCID'),allocation_scope='two tasks share 256 GiB host RAM; one GCD each',stages=[],samples='memory_samples.jsonl',
    code_sha256={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [repo/'production/shot.py',repo/'feltwillow/wan.py']})
stop=threading.Event()
phase='python_imports'

def persist():
    stage=out/'profile.json.tmp'
    stage.write_text(json.dumps(report,indent=2))
    stage.replace(out/'profile.json')

persist()
import torch
from feltwillow import wan
if not torch.cuda.is_available() or not torch.version.hip:
    raise RuntimeError('Profiling requires a ROCm GPU allocation')
torch.cuda.init()
torch.cuda.reset_peak_memory_stats()
report.update(status='running',torch_version=torch.__version__,gpu_name=torch.cuda.get_device_name(0),
    gpu_total_bytes=torch.cuda.get_device_properties(0).total_memory,
    visible_devices=os.environ.get('ROCR_VISIBLE_DEVICES'),cpu_threads=torch.get_num_threads())
persist()

def sample():
    with (out/'memory_samples.jsonl').open('w',buffering=1) as stream:
        while not stop.is_set():
            row=dict(unix_time=time.time(),elapsed_seconds=round(time.perf_counter()-started,3),phase=phase)
            for line in Path('/proc/self/status').read_text().splitlines():
                if line.startswith(('VmRSS:','VmHWM:')):
                    row[line.split(':')[0]+'_bytes']=int(line.split()[1])*1024
            try:
                free,total=torch.cuda.mem_get_info()
                row.update(gpu_device_used_bytes=total-free,gpu_torch_allocated_bytes=torch.cuda.memory_allocated(),
                           gpu_torch_reserved_bytes=torch.cuda.memory_reserved())
            except Exception as exc:
                row['gpu_sampling_error']=str(exc)
            stream.write(json.dumps(row)+'\n')
            stop.wait(2)

thread=threading.Thread(target=sample,daemon=True)
thread.start()

def measured(name,original):
    def wrapper(*args,**kwargs):
        global phase
        phase=name
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()
        begin=time.perf_counter()
        record=dict(stage=name,status='running')
        report['stages'].append(record)
        persist()
        try:
            result=original(*args,**kwargs)
            torch.cuda.synchronize()
            record['status']='complete'
            return result
        except BaseException:
            record['status']='failed'
            raise
        finally:
            record.update(elapsed_seconds=round(time.perf_counter()-begin,3),
                host_process_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                gpu_peak_allocated_bytes=torch.cuda.max_memory_allocated(),
                gpu_peak_reserved_bytes=torch.cuda.max_memory_reserved())
            persist()
    return wrapper

wan.load=measured('model_load',wan.load)
wan.generate=measured('generation',wan.generate)
wan.save=measured('video_encoding',wan.save)
try:
    script=repo/'production/shot.py'
    sys.argv=[str(script),*sys.argv[1:]]
    runpy.run_path(str(script),run_name='__main__')
    report['status']='complete'
except BaseException:
    report.update(status='failed',error=traceback.format_exc())
    raise
finally:
    stop.set()
    thread.join(timeout=5)
    usage=resource.getrusage(resource.RUSAGE_SELF)
    report.update(total_wall_seconds=round(time.perf_counter()-started,3),host_peak_rss_bytes=usage.ru_maxrss*1024,
        cpu_user_seconds=usage.ru_utime,cpu_system_seconds=usage.ru_stime,
        gpu_peak_allocated_bytes=max((r.get('gpu_peak_allocated_bytes',0) for r in report['stages']),default=0),
        gpu_peak_reserved_bytes=max((r.get('gpu_peak_reserved_bytes',0) for r in report['stages']),default=0))
    persist()
    print(json.dumps(report,indent=2),flush=True)
