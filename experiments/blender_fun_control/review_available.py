#!/usr/bin/env python3
"""Aggregate only verified available experiments; never rerun inference."""
import json
import os
from pathlib import Path
import time
from run_case import digest
ROOT=Path(__file__).resolve().parents[2]
PARENT=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control'
def main():
    if not os.environ.get('SLURM_JOB_ID'):raise SystemExit('Allocated CPU required')
    import imageio.v2 as imageio
    import numpy as np
    from PIL import Image,ImageDraw
    from feltwillow.media import locate_ffmpeg
    os.environ['IMAGEIO_FFMPEG_EXE']=str(locate_ffmpeg())
    out=PARENT/'reviews_available_20261018';out.mkdir(exist_ok=False)
    (out/'executed_collector.py').write_bytes(Path(__file__).read_bytes())
    receipt=dict(status='running',production_eligible=False,job_id=os.environ['SLURM_JOB_ID'],script_sha256=digest(__file__),groups={},omitted=[],start_epoch=time.time())
    try:
        panels=[('seed43',PARENT/'i2v_followup_20261016/long_81')]
        for seed in (44,45,46):
            folder=PARENT/f'matrix_seeds_seed_{seed}_split_20261017'/f'seed_{seed}'
            proof=folder/'receipt.json'
            if not proof.is_file():
                receipt['omitted'].append(dict(seed=seed,reason='No completed clip receipt'));continue
            if json.loads(proof.read_text()).get('status')!='complete':
                receipt['omitted'].append(dict(seed=seed,reason='Clip receipt incomplete'));continue
            panels.append((f'seed{seed}',folder))
        if len(panels)<2:raise RuntimeError('At least two seed clips required')
        groups={'articulated_6way':[(action+': '+mode,PARENT/('articulated_'+mode+'_split_20261017')/(action+'_'+mode)) for action in ('reach','walk','camera') for mode in ('normal','control')],'seeds_available':panels}
        for name,items in groups.items():
            clips=[];proofs=[]
            for label,folder in items:
                proof=json.loads((folder/'receipt.json').read_text())
                if proof['status']!='complete' or proof['output_sha256']!=digest(folder/'output.mp4'):raise RuntimeError('Incomplete or changed clip '+label)
                with imageio.get_reader(folder/'output.mp4') as reader:
                    frames=[frame for frame in reader]
                    if reader.get_meta_data()['fps']!=16:raise RuntimeError('Bad FPS')
                clips.append(frames);proofs.append(dict(label=label,folder=str(folder),sha256=proof['output_sha256']))
            count=len(clips[0]);h,w=clips[0][0].shape[:2]
            if any(len(c)!=count or any(f.shape!=(h,w,3) for f in c) for c in clips):raise RuntimeError('Mismatched geometry')
            with imageio.get_writer(out/(name+'.mp4'),fps=16,codec='libx264',quality=9,macro_block_size=1) as writer:
                for index in range(count):
                    canvas=Image.new('RGB',(w*2,(h+24)*((len(clips)+1)//2)),'#202020');draw=ImageDraw.Draw(canvas)
                    for k,((label,_),clip) in enumerate(zip(items,clips)):
                        x,y=k%2*w,k//2*(h+24)
                        canvas.paste(Image.fromarray(clip[index]),(x,y+24));draw.text((x+4,y+4),label,fill='white')
                    writer.append_data(np.array(canvas))
                    if index==count//2:canvas.save(out/(name+'_poster.png'))
            receipt['groups'][name]=dict(status='complete',output_sha256=digest(out/(name+'.mp4')),sources=proofs)
        receipt['status']='complete'
    except BaseException:
        import traceback
        receipt.update(status='failed',error=traceback.format_exc());raise
    finally:
        receipt['elapsed_seconds']=time.time()-receipt['start_epoch']
        (out/'receipt.json').write_text(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
