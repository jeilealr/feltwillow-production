#!/usr/bin/env python3
"""Rebuild cross-job review panels after completed split renders; CPU allocation."""
import argparse
import json
import os
from pathlib import Path
import time
from run_case import digest

ROOT=Path(__file__).resolve().parents[2]
PARENT=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control'


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--allow-incomplete-seeds',action='store_true')
    ap.add_argument('--run-name',default='split_reviews_20261017')
    args=ap.parse_args()
    if not args.run_name.replace('_','').isalnum():ap.error('Invalid run name')
    if not os.environ.get('SLURM_JOB_ID'):raise SystemExit('Allocated compute only')
    import imageio.v2 as imageio
    import numpy as np
    from PIL import Image,ImageDraw
    from feltwillow.media import locate_ffmpeg
    os.environ['IMAGEIO_FFMPEG_EXE']=str(locate_ffmpeg())
    out=PARENT/args.run_name;out.mkdir(exist_ok=False)
    receipt=dict(status='running',production_eligible=False,job_id=os.environ['SLURM_JOB_ID'],script_sha256=digest(__file__),groups={},started_epoch=time.time())
    groups={
      'articulated_6way':[(action+': '+mode,PARENT/('articulated_'+mode+'_split_20261017')/(action+'_'+mode)) for action in ('reach','walk','camera') for mode in ('normal','control')],
      'seeds_4way':[('seed43',PARENT/'i2v_followup_20261016/long_81')]+[(f'seed{seed}',PARENT/f'matrix_seeds_seed_{seed}_split_20261017'/f'seed_{seed}') for seed in (44,45,46)]}
    if args.allow_incomplete_seeds:
        available=[];omitted=[]
        for label,folder in groups.pop('seeds_4way'):
            proof=folder/'receipt.json'
            if proof.is_file() and json.loads(proof.read_text()).get('status')=='complete':available.append((label,folder))
            else:omitted.append(dict(label=label,path=str(folder),reason='No completed clip receipt; no inference rerun'))
        if len(available)<2:raise RuntimeError('Need at least two completed seed clips')
        groups['seeds_available']=available
        receipt['omitted_seed_panels']=omitted
    try:
        for name,panels in groups.items():
            clips=[];proofs=[]
            for label,folder in panels:
                proof=json.loads((folder/'receipt.json').read_text())
                if proof['status']!='complete' or proof['output_sha256']!=digest(folder/'output.mp4'):
                    raise RuntimeError('Incomplete/changed clip: '+str(folder))
                with imageio.get_reader(folder/'output.mp4') as reader:
                    clip=[frame for frame in reader]
                    if reader.get_meta_data()['fps']!=16:raise RuntimeError('Unexpected FPS')
                clips.append(clip);proofs.append(dict(label=label,path=str(folder),receipt_sha256=digest(folder/'receipt.json'),output_sha256=proof['output_sha256']))
            n=len(clips[0]);h,w=clips[0][0].shape[:2]
            if any(len(c)!=n or any(f.shape!=(h,w,3) for f in c) for c in clips):raise RuntimeError('Panel geometry mismatch')
            with imageio.get_writer(out/(name+'.mp4'),fps=16,codec='libx264',quality=9,macro_block_size=1) as writer:
                for index in range(n):
                    canvas=Image.new('RGB',(w*2,(h+24)*((len(clips)+1)//2)),'#202020');draw=ImageDraw.Draw(canvas)
                    for k,((label,_),frames) in enumerate(zip(panels,clips)):
                        x,y=(k%2)*w,(k//2)*(h+24)
                        canvas.paste(Image.fromarray(frames[index]),(x,y+24));draw.text((x+4,y+4),label,fill='white')
                    writer.append_data(np.array(canvas))
                    if index==n//2:canvas.save(out/(name+'_poster.png'))
            receipt['groups'][name]=dict(status='complete',output_sha256=digest(out/(name+'.mp4')),sources=proofs)
        receipt['status']='complete'
    except BaseException:
        import traceback
        receipt.update(status='failed',error=traceback.format_exc());raise
    finally:
        receipt['elapsed_seconds']=time.time()-receipt['started_epoch']
        (out/'receipt.json').write_text(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
