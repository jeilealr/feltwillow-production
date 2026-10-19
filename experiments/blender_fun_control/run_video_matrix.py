#!/usr/bin/env python3
"""Named, bounded video experiments. No production assets/defaults are modified."""
import argparse
import gc
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import traceback
from run_case import digest, load_control, BACKEND, REVISION
from run_i2v_followup import pixels, PROMPT, NEGATIVE

ROOT=Path(__file__).resolve().parents[2]
PARENT=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control'
PROXY=PARENT/'articulated_20261016_v2'
RECIPES={
 'depth_diagnostic':dict(backend='control',frames=33,width=416,height=240,
    cases=[dict(name='moving_depth',action='camera',representation='depth'),
           dict(name='stationary_depth',action='camera',representation='depth',stationary=True)]),
 'endpoint':dict(backend='normal',frames=81,width=416,height=240,
    cases=[dict(name='start_only'),dict(name='start_and_end',end=True)]),
 'seeds':dict(backend='normal',frames=81,width=832,height=480,
    cases=[dict(name='seed_44',seed=44),dict(name='seed_45',seed=45),dict(name='seed_46',seed=46)]),
 'representation':dict(backend='control',frames=49,width=416,height=240,
    cases=[dict(name='reach_edges',action='reach',representation='edges'),
           dict(name='reach_depth',action='reach',representation='depth'),
           dict(name='reach_stationary_depth',action='reach',representation='depth',stationary=True)])}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('recipe',choices=RECIPES)
    ap.add_argument('--case',help='Run only this named recipe case in a separate output root')
    args=ap.parse_args()
    if not os.environ.get('SLURM_JOB_ID'):raise SystemExit('Allocated compute only')
    os.environ['VIDEOX_ATTENTION_TYPE']='SDPA'
    import torch
    import numpy as np
    import cv2
    import imageio.v2 as imageio
    from PIL import Image,ImageDraw
    from feltwillow import wan
    from feltwillow.media import locate_ffmpeg
    if not torch.cuda.is_available() or not torch.version.hip:raise RuntimeError('Expected ROCm GPU')
    torch.set_num_threads(int(os.environ.get('SLURM_CPUS_PER_TASK','7')))
    os.environ['IMAGEIO_FFMPEG_EXE']=str(locate_ffmpeg())
    recipe=dict(RECIPES[args.recipe])
    if args.case:
        selected=[case for case in recipe['cases'] if case['name']==args.case]
        if len(selected)!=1:ap.error('Unknown case for selected recipe')
        recipe['cases']=selected
    n,w,h=recipe['frames'],recipe['width'],recipe['height']
    run=PARENT/('matrix_'+args.recipe+('_'+args.case+'_split_20261017' if args.case else '_20261016'))
    run.mkdir(exist_ok=False)
    shutil.copyfile(__file__,run/'executed_runner.py')
    receipt=dict(status='running',production_eligible=False,approval='isolated_experiment_not_for_production',
        recipe=args.recipe,configuration=recipe,job_id=os.environ['SLURM_JOB_ID'],
        partition=os.environ.get('SLURM_JOB_PARTITION'),script_sha256=digest(__file__),
        environment=dict(torch=torch.__version__,hip=torch.version.hip,gpu=torch.cuda.get_device_name(0)),
        repo_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        frames=n,width=w,height=h,fps=16,cases=[],start_epoch=time.time(),
        limitations=['Single pilot scene, not general quality evidence.',
          'Candidate image inputs are isolated experiments, not production-approved assets.',
          'Proxy proportions/view and synthetic stage differ from original illustration.',
          'Synthetic depth is fixed near-bright camera-Z; model training-domain equivalence is unverified.',
          'Numerical motion and endpoint pixel error are not identity/anatomy approval.'])
    try:
        inputs=run/'inputs';inputs.mkdir()
        for source,name in [('start.png','start'),('end_evaluation.png','end')]:
            original=PARENT/'feasibility_20261016/story_inputs'/source
            shutil.copyfile(original,inputs/(name+'_original.png'))
            wan.fit(Image.open(original),w,h).save(inputs/(name+'.png'))
        receipt['input_hashes']={p.name:digest(p) for p in inputs.glob('*.png')}
        if recipe['backend']=='normal':
            receipt['model']=wan.model_id('i2v');receipt['lightning']=wan.LIGHTNING
            cache=ROOT.parent/'models/video_control_baseline_bf16'/wan.REVISIONS['i2v']
            proof=cache/'conversion_receipt.json';verified=json.loads(proof.read_text())
            if verified['status']!='complete' or verified['revision']!=wan.REVISIONS['i2v']:raise RuntimeError('Unverified cache')
            receipt['cache_receipt_sha256']=digest(proof)
            wan.MODELS['i2v']=str(cache)
            lo=wan.lightning_lora();receipt['lora_hashes']={k:digest(lo[k]) for k in ('high','low')}
            started=time.time();pipe=wan.load('i2v',frames=n,fast=True)
        else:
            if subprocess.check_output(['git','rev-parse','HEAD'],cwd=BACKEND,text=True).strip()!=REVISION:
                raise RuntimeError('Backend revision mismatch')
            proxy=json.loads((PROXY/'proxy_receipt.json').read_text());gate=json.loads((PROXY/'guide_gate.json').read_text())
            if proxy['status']!='complete' or gate['decision']!='admit_isolated_feasibility_only' or gate['proxy_receipt_sha256']!=digest(PROXY/'proxy_receipt.json'):
                raise RuntimeError('Proxy inspection gate mismatch')
            receipt['proxy_receipt_sha256']=digest(PROXY/'proxy_receipt.json')
            receipt['model']='alibaba-pai/Wan2.2-Fun-A14B-Control@297be6d520f54908e124be0298e2317ee50ffdf4'
            receipt['backend_revision']=REVISION
            for case in recipe['cases']:
                files=sorted((PROXY/case['action']).glob('[0-9]*.png'))
                if len(files)!=49:raise RuntimeError('Expected 49 source guide frames')
                indices=[0]*n if case.get('stationary') else np.rint(np.linspace(0,48,n)).astype(int).tolist()
                case_path=inputs/(case['name']+'.mp4')
                source_hashes={}
                with imageio.get_writer(case_path,fps=16,codec='libx264',quality=9,macro_block_size=1) as writer:
                    for i,index in enumerate(indices):
                        path=files[index];a=np.array(Image.open(path).convert('RGB'))
                        source_hashes[path.name]=digest(path)
                        if case['representation']=='depth':
                            value=a.astype('float32')/255
                            linear=np.where(value<=.04045,value/12.92,((value+.055)/1.055)**2.4)
                            a=np.clip(linear*255,0,255).astype('uint8')
                        else:
                            edge=cv2.Canny(a,10,25)
                            yy,xx=np.mgrid[:240,:416]
                            edge[~((xx>125)&(xx<310)&(yy>15)&(yy<220))]=0
                            a=np.repeat(edge[:,:,None],3,axis=2)
                        writer.append_data(a)
                        if i in (0,n//2,n-1):Image.fromarray(a).save(inputs/f'{case["name"]}_{i:03d}.png')
                (inputs/(case['name']+'_guide.json')).write_text(json.dumps(dict(
                    guide_sha256=digest(case_path),source_hashes=source_hashes,indices=indices,
                    representation=case['representation'],depth_near_far=[5,12],depth_nearer='white',
                    note='Fixed-range inverse camera-Z, inverse sRGB applied; not per-frame normalized'),indent=2))
            started=time.time();pipe=load_control()
        receipt['load_seconds']=time.time()-started
        decoded={}
        for case in recipe['cases']:
            name=case['name'];folder=run/name;folder.mkdir()
            prompt=proxy['cases'][case['action']]['prompt'] if recipe['backend']=='control' else PROMPT
            negative=NEGATIVE.replace('camera movement, zoom, ','') if case.get('action')=='camera' else NEGATIVE
            item=dict(name=name,status='running',seed=case.get('seed',43),prompt=prompt,negative_prompt=negative,
                end_image_role='conditioning' if case.get('end') else 'evaluation_only',
                source_sha256=digest(inputs/'start.png'),end_sha256=digest(inputs/'end.png'))
            receipt['cases'].append(item);(run/'receipt.json').write_text(json.dumps(receipt,indent=2))
            torch.cuda.reset_peak_memory_stats();started=time.time();print('START_CASE',name,flush=True)
            if recipe['backend']=='normal':
                result=wan.generate(pipe,prompt,negative=negative,width=w,height=h,frames=n,steps=4,
                    guidance=1,guidance_2=1,seed=item['seed'],image=Image.open(inputs/'start.png'),
                    last_image=Image.open(inputs/'end.png') if case.get('end') else None)
                item.update(steps=4,guidance=[1,1])
            else:
                from videox_fun.utils import get_image_to_video_latent,get_video_to_video_latent,get_image_latent
                video,mask,_=get_image_to_video_latent(str(inputs/'start.png'),None,video_length=n,sample_size=[h,w])
                control,_,_,_=get_video_to_video_latent(str(inputs/(name+'.mp4')),video_length=n,sample_size=[h,w],fps=16,ref_image=None)
                ref=get_image_latent(str(inputs/'start.png'),sample_size=[h,w])
                with torch.no_grad():
                    sample=pipe(prompt,num_frames=n,negative_prompt=negative,height=h,width=w,
                        generator=torch.Generator(device='cuda').manual_seed(item['seed']),guidance_scale=6.,num_inference_steps=28,
                        video=video,mask_video=mask,control_video=control,ref_image=ref,boundary=.9,shift=5.).videos
                result=[Image.fromarray(np.clip(sample[0,:,i].permute(1,2,0).cpu().float().numpy()*255,0,255).astype('uint8')) for i in range(n)]
                item.update(steps=28,guidance=6.,guide_sha256=digest(inputs/(name+'.mp4')))
                del sample,video,mask,control,ref
            result=[pixels(frame) for frame in result];torch.cuda.synchronize()
            item['inference_seconds']=time.time()-started
            if len(result)!=n or any(f.size!=(w,h) for f in result):raise RuntimeError('Bad output geometry')
            wan.save(result,folder/'output.mp4',fps=16)
            sheet=Image.new('RGB',(7*208,((n+6)//7)*140),'#202020');draw=ImageDraw.Draw(sheet)
            for i,frame in enumerate(result):
                x,y=i%7*208,i//7*140;sheet.paste(frame.resize((208,120)),(x,y+20));draw.text((x+3,y+3),str(i),fill='white')
                if i in (0,n//4,n//2,3*n//4,n-1):frame.save(folder/f'frame_{i:03d}.png')
            sheet.save(folder/'all_frames.jpg')
            target=np.array(Image.open(inputs/'end.png')).astype(float)
            item['last_frame_target_mae_0_255']=float(np.abs(np.array(result[-1]).astype(float)-target).mean())
            with imageio.get_reader(folder/'output.mp4') as reader:
                decoded[name]=[frame for frame in reader]
                if len(decoded[name])!=n or decoded[name][0].shape!=(h,w,3) or reader.get_meta_data()['fps']!=16:
                    raise RuntimeError('Encoded format mismatch')
            item.update(status='complete',output_sha256=digest(folder/'output.mp4'),peak_hbm_bytes=torch.cuda.max_memory_allocated())
            (folder/'receipt.json').write_text(json.dumps(dict(production_eligible=False,**item),indent=2))
            (run/'receipt.json').write_text(json.dumps(receipt,indent=2));del result
            print('COMPLETE_CASE',name,flush=True)
        with imageio.get_writer(run/'comparison.mp4',fps=16,codec='libx264',quality=9,macro_block_size=1) as writer:
            for i in range(n):
                canvas=Image.new('RGB',(w*len(decoded),h+32),'#202020');draw=ImageDraw.Draw(canvas)
                for column,(name,frames) in enumerate(decoded.items()):
                    canvas.paste(Image.fromarray(frames[i]),(column*w,32));draw.text((column*w+5,5),name,fill='white')
                writer.append_data(np.array(canvas))
        receipt.update(status='complete',comparison_sha256=digest(run/'comparison.mp4'))
    except BaseException:
        receipt.update(status='failed',error=traceback.format_exc());raise
    finally:
        receipt['elapsed_seconds']=time.time()-receipt['start_epoch']
        (run/'receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':main()
