#!/usr/bin/env python3
"""Six sequential bounded A/B renders; rough 3D proxy is not production staging."""
import argparse
import gc
import json
import os
from pathlib import Path
import shutil
import time
import traceback
from run_case import digest, load_control, BACKEND, REVISION
from run_i2v_followup import pixels

ROOT=Path(__file__).resolve().parents[2]
PARENT=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control'
PROXY=PARENT/'articulated_20261016_v2'
RUN=PARENT/'articulated_comparison_20261016'
NEGATIVE='extra animals, extra limbs, deformed paws, face distortion, changing identity, flicker, text, subtitles, sliding feet'


def main():
    global RUN
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--backend',choices=['all','normal','control'],default='all')
    args=ap.parse_args()
    if args.backend!='all':RUN=PARENT/('articulated_'+args.backend+'_split_20261017')
    if not os.environ.get('SLURM_JOB_ID'):raise SystemExit('Allocated compute only')
    os.environ['VIDEOX_ATTENTION_TYPE']='SDPA'
    import subprocess
    import cv2
    import torch
    import numpy as np
    import imageio.v2 as imageio
    from PIL import Image,ImageDraw
    from feltwillow import wan
    from feltwillow.media import locate_ffmpeg
    from videox_fun.utils import get_image_to_video_latent,get_video_to_video_latent,get_image_latent
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=BACKEND,text=True).strip()!=REVISION:
        raise RuntimeError('Backend revision mismatch')
    proxy=json.loads((PROXY/'proxy_receipt.json').read_text())
    gate=json.loads((PROXY/'guide_gate.json').read_text())
    if proxy['status']!='complete' or gate['decision']!='admit_isolated_feasibility_only':
        raise RuntimeError('Proxy has not passed inspection gate')
    if gate['proxy_receipt_sha256']!=digest(PROXY/'proxy_receipt.json'):
        raise RuntimeError('Proxy gate hash mismatch')
    if not torch.cuda.is_available() or not torch.version.hip:raise RuntimeError('Expected ROCm GPU')
    torch.set_num_threads(int(os.environ.get('SLURM_CPUS_PER_TASK','7')))
    os.environ['VIDEOX_ATTENTION_TYPE']='SDPA'
    os.environ['IMAGEIO_FFMPEG_EXE']=str(locate_ffmpeg())
    RUN.mkdir(exist_ok=False)
    shutil.copyfile(__file__,RUN/'executed_runner.py')
    receipt=dict(status='running',execution_backend=args.backend,production_eligible=False,approval='isolated_experiment_not_for_production',
        job_id=os.environ['SLURM_JOB_ID'],partition=os.environ.get('SLURM_JOB_PARTITION'),
        script_sha256=digest(__file__),repo_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        proxy_receipt_sha256=digest(PROXY/'proxy_receipt.json'),gate_sha256=digest(PROXY/'guide_gate.json'),
        seed=43,frames=49,fps=16,width=416,height=240,cases=[],started_epoch=time.time(),
        limits=['Approximate 3D proxy does not exactly align with original image or approved plate.',
        'Generic depth-driven camera motion; explicit Camera checkpoint not tested.',
        'Near-bright fixed inverse-Z is a synthetic depth encoding, not calibrated monocular training data.',
        'Only one seed and short low-resolution clip per action; model/steps/guidance differ between A/B.'])
    try:
        inputs=RUN/'inputs';inputs.mkdir()
        source=PARENT/'feasibility_20261016/story_inputs/start.png'
        shutil.copyfile(source,inputs/'start_original.png')
        wan.fit(Image.open(source),416,240).save(inputs/'start.png')
        receipt['source_sha256']=digest(source);receipt['fitted_source_sha256']=digest(inputs/'start.png')
        receipt['guides']={}
        for name,spec in proxy['cases'].items():
            files=sorted((PROXY/name).glob('[0-9]*.png'))
            if len(files)!=49:raise RuntimeError('Expected 49 guide frames')
            hashes={}
            with imageio.get_writer(inputs/(name+'.mp4'),fps=16,codec='libx264',quality=9,macro_block_size=1) as writer:
                for index,path in enumerate(files):
                    a=np.array(Image.open(path).convert('RGB'))
                    if spec['representation']=='depth':
                        value=a.astype('float32')/255
                        linear=np.where(value<=.04045,value/12.92,((value+.055)/1.055)**2.4)
                        a=np.clip(linear*255,0,255).astype('uint8')
                    else:
                        edge=cv2.Canny(a,10,25)
                        # Retain a fixed generous actor region, exclude distant rocks/horizon.
                        yy,xx=np.mgrid[:240,:416]
                        keep=(xx>125)&(xx<310)&(yy>15)&(yy<220)
                        edge[~keep]=0
                        a=np.repeat(edge[:,:,None],3,axis=2)
                    writer.append_data(a)
                    if index in (0,12,24,36,48):Image.fromarray(a).save(inputs/f'{name}_{index:03d}.png')
                    hashes[path.name]=digest(path)
            receipt['guides'][name]=dict(representation=spec['representation'],source_hashes=hashes,
                guide_sha256=digest(inputs/(name+'.mp4')))
        def save(name,frames,metadata):
            frames=[pixels(frame) for frame in frames]
            if len(frames)!=49 or any(f.size!=(416,240) for f in frames):raise RuntimeError('Bad inference geometry')
            out=RUN/name;out.mkdir()
            wan.save(frames,out/'output.mp4',fps=16)
            sheet=Image.new('RGB',(7*416,7*264),'#202020');draw=ImageDraw.Draw(sheet)
            for i,frame in enumerate(frames):
                x,y=i%7*416,i//7*264;sheet.paste(frame,(x,y+24));draw.text((x+3,y+3),str(i),fill='white')
                if i in (0,12,24,36,48):frame.save(out/f'frame_{i:03d}.png')
            sheet.save(out/'all_frames.jpg')
            with imageio.get_reader(out/'output.mp4') as reader:
                decoded=[frame for frame in reader]
                if len(decoded)!=49 or decoded[0].shape!=(240,416,3) or reader.get_meta_data()['fps']!=16:
                    raise RuntimeError('Bad exported clip')
            metadata.update(status='complete',output_sha256=digest(out/'output.mp4'),peak_hbm_bytes=torch.cuda.max_memory_allocated())
            receipt['cases'].append(dict(name=name,**metadata))
            (out/'receipt.json').write_text(json.dumps(dict(production_eligible=False,**metadata),indent=2))
            (RUN/'receipt.json').write_text(json.dumps(receipt,indent=2))
        if args.backend in ('all','normal'):
            cache=ROOT.parent/'models/video_control_baseline_bf16'/wan.REVISIONS['i2v']
            proof=json.loads((cache/'conversion_receipt.json').read_text())
            if proof['status']!='complete' or proof['revision']!=wan.REVISIONS['i2v']:raise RuntimeError('Bad cache proof')
            receipt['baseline_model']=wan.model_id('i2v');receipt['lightning']=wan.LIGHTNING
            receipt['cache_receipt_sha256']=digest(cache/'conversion_receipt.json')
            wan.MODELS['i2v']=str(cache)
            pipe=wan.load('i2v',frames=49,fast=True)
            for name,spec in proxy['cases'].items():
                print('START_BASELINE',name,flush=True);torch.cuda.reset_peak_memory_stats();start=time.time()
                frames=wan.generate(pipe,spec['prompt'],negative=NEGATIVE,width=416,height=240,frames=49,
                    steps=4,guidance=1,guidance_2=1,seed=43,image=Image.open(inputs/'start.png'))
                save(name+'_normal',frames,dict(prompt=spec['prompt'],negative_prompt=NEGATIVE,steps=4,guidance=[1,1],seconds=time.time()-start))
                del frames
            del pipe;gc.collect();torch.cuda.empty_cache()
        if args.backend in ('all','control'):
            pipe=load_control()
            receipt['control_model']='alibaba-pai/Wan2.2-Fun-A14B-Control@297be6d520f54908e124be0298e2317ee50ffdf4'
            for name,spec in proxy['cases'].items():
                print('START_CONTROL',name,flush=True);torch.cuda.reset_peak_memory_stats();start=time.time()
                video,mask,_=get_image_to_video_latent(str(inputs/'start.png'),None,video_length=49,sample_size=[240,416])
                control,_,_,_=get_video_to_video_latent(str(inputs/(name+'.mp4')),video_length=49,sample_size=[240,416],fps=16,ref_image=None)
                ref=get_image_latent(str(inputs/'start.png'),sample_size=[240,416])
                with torch.no_grad():
                    sample=pipe(spec['prompt'],num_frames=49,negative_prompt=NEGATIVE,height=240,width=416,
                        generator=torch.Generator(device='cuda').manual_seed(43),guidance_scale=6.,num_inference_steps=28,
                        video=video,mask_video=mask,control_video=control,ref_image=ref,boundary=.9,shift=5.).videos
                frames=[Image.fromarray(np.clip(sample[0,:,i].permute(1,2,0).cpu().float().numpy()*255,0,255).astype('uint8')) for i in range(49)]
                save(name+'_control',frames,dict(prompt=spec['prompt'],negative_prompt=NEGATIVE,steps=28,guidance=6.,seconds=time.time()-start))
                del sample,frames,video,mask,control,ref
        if args.backend=='all':
            clips={}
            for name in proxy['cases']:
                for mode in ('normal','control'):
                    key=name+'_'+mode
                    with imageio.get_reader(RUN/key/'output.mp4') as reader:clips[key]=[frame for frame in reader]
            with imageio.get_writer(RUN/'comparison_6way.mp4',fps=16,codec='libx264',quality=9,macro_block_size=1) as writer:
                for i in range(49):
                    canvas=Image.new('RGB',(832,792),'#202020');draw=ImageDraw.Draw(canvas)
                    for row,name in enumerate(proxy['cases']):
                        for col,mode in enumerate(('normal','control')):
                            x,y=col*416,row*264
                            canvas.paste(Image.fromarray(clips[name+'_'+mode][i]),(x,y+24))
                            draw.text((x+4,y+4),name+': '+('Wan Lightning 4' if mode=='normal' else '3D guide Control 28'),fill='white')
                    writer.append_data(np.array(canvas))
            receipt['comparison_sha256']=digest(RUN/'comparison_6way.mp4')
        receipt['status']='complete'
    except BaseException:
        receipt.update(status='failed',error=traceback.format_exc());raise
    finally:
        receipt['elapsed_seconds']=time.time()-receipt['started_epoch']
        (RUN/'receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':main()
