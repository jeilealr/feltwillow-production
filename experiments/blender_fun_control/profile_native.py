#!/usr/bin/env python3
"""One native-length 480p capacity/timing diagnostic, not a quality render."""
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import time
import traceback
from run_case import digest

ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control/profile_native_20261017'


def main():
    if not os.environ.get('SLURM_JOB_ID'):raise SystemExit('Allocated compute only')
    RUN.mkdir(exist_ok=False)
    shutil.copyfile(__file__,RUN/'executed_runner.py')
    receipt=dict(status='running',production_eligible=False,approval='resource_diagnostic_not_quality_render',
        job_id=os.environ['SLURM_JOB_ID'],partition=os.environ.get('SLURM_JOB_PARTITION'),
        width=832,height=480,frames=81,steps=2,seed=43,requested_host_memory='96G',
        script_sha256=digest(__file__),repo_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        start_epoch=time.time(),phase='imports',steps_completed=[],
        limitations=['Two steps differs from trained four-step Lightning recipe: no visual quality inference.',
        '480p native frame count, not a 720p test.',
        'Per-step durations include transfers and are not a linear four-step runtime estimate.',
        'Slurm MaxRSS includes a different process scope from Python ru_maxrss.'])
    def checkpoint():
        receipt['elapsed_seconds']=time.time()-receipt['start_epoch']
        receipt['peak_host_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        (RUN/'receipt.tmp').write_text(json.dumps(receipt,indent=2));(RUN/'receipt.tmp').replace(RUN/'receipt.json')
    checkpoint()
    try:
        import torch
        import numpy as np
        from PIL import Image
        from feltwillow import wan
        if not torch.cuda.is_available() or not torch.version.hip:raise RuntimeError('Expected ROCm GPU')
        torch.set_num_threads(int(os.environ.get('SLURM_CPUS_PER_TASK','7')))
        receipt['environment']=dict(torch=torch.__version__,hip=torch.version.hip,gpu=torch.cuda.get_device_name(0))
        source=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control/feasibility_20261016/story_inputs/start.png'
        receipt['source_sha256']=digest(source)
        receipt['model']=wan.model_id('i2v');receipt['lightning']=wan.LIGHTNING
        cache=ROOT.parent/'models/video_control_baseline_bf16'/wan.REVISIONS['i2v']
        proof=cache/'conversion_receipt.json';verified=json.loads(proof.read_text())
        if verified['status']!='complete' or verified['revision']!=wan.REVISIONS['i2v']:raise RuntimeError('Unverified bf16 cache')
        receipt['cache_receipt_sha256']=digest(proof);wan.MODELS['i2v']=str(cache)
        lo=wan.lightning_lora();receipt['lora_hashes']={k:digest(lo[k]) for k in ('high','low')}
        receipt['phase']='load';checkpoint();before=time.time()
        pipe=wan.load('i2v',frames=81,fast=True)
        receipt['load_seconds']=time.time()-before
        receipt['phase']='inference';checkpoint();before=time.time();last=[before]
        torch.cuda.reset_peak_memory_stats()
        def callback(pipeline,step,timestep,kwargs):
            torch.cuda.synchronize();now=time.time()
            receipt['steps_completed'].append(dict(index=step,seconds_since_previous=now-last[0],
                elapsed_inference_seconds=now-before,peak_hbm_bytes=torch.cuda.max_memory_allocated()))
            last[0]=now;checkpoint();print('STEP_PROFILE',receipt['steps_completed'][-1],flush=True)
            return kwargs
        # Same parameters as wan.generate, adding only a timing callback.
        frames=pipe(prompt='A small grey needle-felt mouse holds one acorn and gently nibbles it. Fixed camera, planted feet, felt storybook animation.',
            negative_prompt='extra limbs, deformed paws, changing identity, camera movement, text',
            image=wan.fit(Image.open(source),832,480),height=480,width=832,num_frames=81,
            num_inference_steps=2,guidance_scale=1.,guidance_scale_2=1.,
            generator=torch.Generator(device='cpu').manual_seed(43),callback_on_step_end=callback,
            callback_on_step_end_tensor_inputs=[]).frames[0]
        torch.cuda.synchronize()
        receipt['inference_and_decode_seconds']=time.time()-before
        if len(frames)!=81:raise RuntimeError('Unexpected decoded frame count')
        for index in (0,80):
            a=np.asarray(frames[index]);
            if a.shape!=(480,832,3) or not np.isfinite(a).all():raise RuntimeError('Bad decoded output')
        receipt.update(status='complete',phase='complete',decoded_frames=len(frames),
            peak_hbm_allocated_bytes=torch.cuda.max_memory_allocated(),peak_hbm_reserved_bytes=torch.cuda.max_memory_reserved(),
            decode_after_last_step_seconds=time.time()-last[0])
        # No review movie: under-stepped output is not a candidate video.
    except BaseException:
        receipt.update(status='failed',error=traceback.format_exc());raise
    finally:
        checkpoint();print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':main()
