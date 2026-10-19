#!/usr/bin/env python3
"""Static versus subtly animated close-up mouth diagnostic for two speakers."""
import gc
import json
import os
from pathlib import Path
import time
import traceback
from composite_probe import RUN,ROOT,sha,compose


def main():
    if not os.environ.get('SLURM_JOB_ID'):raise SystemExit('Allocated compute only')
    alignment=json.loads((RUN/'alignment/receipt.json').read_text())
    if alignment['status']!='complete':raise RuntimeError('Alignment/mask diagnostic incomplete')
    output=RUN/'video_probe';output.mkdir(exist_ok=False)
    (output/'executed_runner.py').write_bytes(Path(__file__).read_bytes())
    receipt=dict(status='running',production_eligible=False,job_id=os.environ['SLURM_JOB_ID'],script_sha256=sha(__file__),
        alignment_sha256=sha(RUN/'alignment/receipt.json'),start_epoch=time.time(),cases=[])
    try:
        import torch
        import numpy as np
        from PIL import Image
        from feltwillow import wan
        from feltwillow.media import locate_ffmpeg
        import imageio.v2 as imageio
        os.environ['IMAGEIO_FFMPEG_EXE']=str(locate_ffmpeg())
        if not torch.cuda.is_available() or not torch.version.hip:raise RuntimeError('Expected ROCm GPU')
        torch.set_num_threads(int(os.environ.get('SLURM_CPUS_PER_TASK','7')))
        manifest=json.loads((RUN/'inputs/manifest.json').read_text())
        for case in manifest['cases']:
            for role,path in case['paths'].items():
                if sha(path)!=case['hashes'][role]:raise RuntimeError('Source input changed')
            line=alignment['lines'][case['character']]
            for role,path in line['fitted'].items():
                if sha(path)!=line['fitted_hashes'][role]:raise RuntimeError('Calibration changed')
            source=output/(case['character']+'_static.mp4')
            frame=np.array(Image.open(line['fitted']['closed']).convert('RGB'))
            wan.save([frame]*65,source,fps=16)
            receipt['cases'].append(compose(case,line,source,'static'))
        receipt['model']=wan.model_id('i2v');receipt['lightning']=wan.LIGHTNING
        cache=ROOT.parent/'models/video_control_baseline_bf16'/wan.REVISIONS['i2v']
        proof=json.loads((cache/'conversion_receipt.json').read_text())
        if proof['status']!='complete' or proof['revision']!=wan.REVISIONS['i2v']:raise RuntimeError('Bad cache proof')
        receipt['cache_proof_sha256']=sha(cache/'conversion_receipt.json');wan.MODELS['i2v']=str(cache)
        lo=wan.lightning_lora();receipt['lora_hashes']={k:sha(lo[k]) for k in ('high','low')}
        before=time.time();pipe=wan.load('i2v',frames=65,fast=True);receipt['load_seconds']=time.time()-before
        for case in manifest['cases']:
            line=alignment['lines'][case['character']]
            prompt=(f'A close-up of {"Milo the small grey felt mouse" if case["character"]=="milo" else "Leo the tawny felt lion"}. '
                    'Keep the head nearly still and the mouth gently closed. A small natural blink and subtle relieved eyebrow and eye expression. '
                    'Fixed camera, unchanged blurred background, same felt fibers, same identity and framing, restrained storybook acting.')
            before=time.time();torch.cuda.reset_peak_memory_stats()
            frames=wan.generate(pipe,prompt,negative='speech, open mouth, teeth, face distortion, changing identity, camera movement, zoom, cuts, flicker, text',
                width=768,height=432,frames=65,steps=4,guidance=1.,guidance_2=1.,seed=43,image=Image.open(line['fitted']['closed']))
            source=output/(case['character']+'_wan.mp4');wan.save(frames,source,fps=16)
            item=compose(case,line,source,'wan')
            item.update(generation_prompt=prompt,generation_seconds=time.time()-before,peak_hbm_bytes=torch.cuda.max_memory_allocated())
            receipt['cases'].append(item);(output/'receipt.json').write_text(json.dumps(receipt,indent=2))
            del frames;gc.collect()
        receipt['status']='complete'
    except BaseException:
        receipt.update(status='failed',error=traceback.format_exc());raise
    finally:
        receipt['elapsed_seconds']=time.time()-receipt['start_epoch']
        (output/'receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':main()
