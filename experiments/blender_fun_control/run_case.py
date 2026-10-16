#!/usr/bin/env python3
"""Allocated-only feasibility runner. Writes isolated, non-production receipts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT.parent
BACKEND = PROJECT / 'ext/VideoX-Fun-video-control'
REVISION = '6183d41df8fbeb44f24b6c617efb8ef0ab690052'
MODEL_REVISION = '297be6d520f54908e124be0298e2317ee50ffdf4'
MODEL = PROJECT / ('hf_cache/hub/models--alibaba-pai--Wan2.2-Fun-A14B-Control/snapshots/' + MODEL_REVISION)
RUN = ROOT / 'work/stories/lion_and_mouse_v6/experiments/blender_fun_control/feasibility_20261016'


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def load_control():
    import torch
    from omegaconf import OmegaConf
    from diffusers import FlowMatchEulerDiscreteScheduler
    from transformers import AutoTokenizer
    from videox_fun.models import AutoencoderKLWan, Wan2_2Transformer3DModel, WanT5EncoderModel
    from videox_fun.pipeline import Wan2_2FunControlPipeline
    from videox_fun.utils import filter_kwargs
    cfg = OmegaConf.load(BACKEND / 'config/wan2.2/wan_civitai_i2v.yaml')
    kw = OmegaConf.to_container(cfg.transformer_additional_kwargs)
    low = Wan2_2Transformer3DModel.from_pretrained(str(MODEL/'low_noise_model'), transformer_additional_kwargs=kw,
                                                 low_cpu_mem_usage=True, torch_dtype=torch.bfloat16)
    high = Wan2_2Transformer3DModel.from_pretrained(str(MODEL/'high_noise_model'), transformer_additional_kwargs=kw,
                                                  low_cpu_mem_usage=True, torch_dtype=torch.bfloat16)
    vae = AutoencoderKLWan.from_pretrained(str(MODEL/'Wan2.1_VAE.pth'),
                                           additional_kwargs=OmegaConf.to_container(cfg.vae_kwargs)).to(torch.bfloat16)
    encoder = WanT5EncoderModel.from_pretrained(str(MODEL/'models_t5_umt5-xxl-enc-bf16.pth'),
        additional_kwargs=OmegaConf.to_container(cfg.text_encoder_kwargs), low_cpu_mem_usage=True,
        torch_dtype=torch.bfloat16).eval()
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL/'google/umt5-xxl'), local_files_only=True)
    scheduler = FlowMatchEulerDiscreteScheduler(**filter_kwargs(FlowMatchEulerDiscreteScheduler,
                                                               OmegaConf.to_container(cfg.scheduler_kwargs)))
    pipe = Wan2_2FunControlPipeline(transformer=low, transformer_2=high, vae=vae,
                                   tokenizer=tokenizer, text_encoder=encoder, scheduler=scheduler)
    pipe.enable_model_cpu_offload(device='cuda')
    return pipe


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--case', choices=['diagnostic', 'reference', 'baseline', 'controlled', 'stationary', 'blender'], required=True)
    ap.add_argument('--steps', type=int)
    ap.add_argument('--frames', type=int)
    ap.add_argument('--width', type=int)
    ap.add_argument('--height', type=int)
    ap.add_argument('--also-stationary', action='store_true', help='same backend/seed control ablation without reloading')
    ap.add_argument('--run-name', help='unique attempt name; never overwrites an existing run')
    args = ap.parse_args()
    if not os.environ.get('SLURM_JOB_ID'):
        raise SystemExit('Inference requires a SLURM allocation.')
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=BACKEND,text=True).strip() != REVISION:
        raise SystemExit('Backend revision mismatch')
    os.environ['VIDEOX_ATTENTION_TYPE'] = 'SDPA'
    name = args.run_name or args.case
    if not name.replace('_','').replace('-','').isalnum():
        raise SystemExit('Invalid run name')
    out = RUN / name
    out.mkdir(exist_ok=False)
    started = time.time()
    receipt = dict(schema='feltwillow.video-control-result.v0-proposal', status='running',
        approval='isolated_experiment_not_for_production', production_eligible=False, case=args.case,
        backend_commit=REVISION, model_revision=MODEL_REVISION, script_sha256=digest(__file__),
        repo_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        repo_dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()),
        allocation={k:os.environ.get(k) for k in ('SLURM_JOB_ID','SLURM_JOB_PARTITION','SLURM_CPUS_PER_TASK','SLURM_MEM_PER_NODE')},
        seed=43, fps=16, loras=[], start_epoch=started, attention='torch SDPA', dtype='bf16', end_image_role='absent')
    try:
        import numpy as np
        import torch
        from PIL import Image
        from diffusers.utils import export_to_video
        if not torch.cuda.is_available() or not torch.version.hip:
            raise RuntimeError('Expected allocated ROCm GPU')
        receipt['environment'] = dict(torch=torch.__version__, rocm=torch.version.hip,
                                      gpu=torch.cuda.get_device_name(0), hbm_bytes=torch.cuda.get_device_properties(0).total_memory)
        torch.cuda.reset_peak_memory_stats()
        torch.set_num_threads(int(os.environ.get('SLURM_CPUS_PER_TASK','7')))
        # Explicit GPU kernel proof before model loading.
        q = torch.randn(1,4,128,64,device='cuda',dtype=torch.bfloat16)
        assert torch.isfinite(torch.nn.functional.scaled_dot_product_attention(q,q,q)).all()
        torch.cuda.synchronize()
        receipt['sdpa_kernel_passed'] = True
        print('SDPA_KERNEL_OK', receipt['environment'], flush=True)
        reference = args.case in ('diagnostic','reference')
        height,width,frames = (256,256,9) if args.case=='diagnostic' else ((512,512,81) if reference else (480,832,81))
        height,width,frames = args.height or height, args.width or width, args.frames or frames
        if frames < 5 or (frames-1)%4 or min(width,height)<128 or width%16 or height%16:
            raise ValueError('Expected >=5 frames in 4k+1 form and dimensions divisible by 16')
        steps = args.steps or (2 if args.case=='diagnostic' else 40)
        if steps < 1:
            raise ValueError('Expected positive inference steps')
        receipt.update(width=width,height=height,frames=frames,steps=steps)
        if reference:
            image_path = BACKEND/'asset/8.png'
            guide_path = BACKEND/'asset/pose.mp4'
            prompt = 'A young woman with purple hair stands at the seashore and moves her arms naturally, ocean waves in the background.'
        else:
            image_path = RUN/'story_inputs/start_fitted.png'
            guide_path = RUN/'story_inputs'/({'controlled':'moving_edges.mp4','stationary':'stationary_edges.mp4','blender':'blender_edges.mp4'}.get(args.case,'moving_edges.mp4'))
            prompt = ('A single small grey needle-felt mouse Milo sits on the grass beside the stream, holding one acorn in both paws. '
                      'He gently brings the acorn toward his mouth, nibbles, and lowers it, with a small natural head nod. '
                      'His feet stay planted. Fixed camera, unchanged framing and mouse size, softly flowing stream, warm afternoon light, felt storybook animation.')
        negative = 'extra animals, extra limbs, deformed paws, face distortion, changing identity, camera movement, zoom, cuts, flicker, text, subtitles'
        receipt.update(prompt=prompt,negative_prompt=negative,source_image=str(image_path),source_image_sha256=digest(image_path))
        t = time.time()
        if args.case == 'baseline':
            from feltwillow import wan
            receipt['model'] = wan.model_id('i2v')
            pipe = wan.load('i2v',frames=frames)
            receipt['load_seconds']=time.time()-t
            result=wan.generate(pipe,prompt,negative=negative,width=width,height=height,frames=frames,steps=steps,
                                guidance=3.5,guidance_2=3.5,seed=43,image=Image.open(image_path))
            receipt['guidance']=[3.5,3.5]
        else:
            from videox_fun.utils import get_image_to_video_latent, get_video_to_video_latent, get_image_latent
            receipt['model']='alibaba-pai/Wan2.2-Fun-A14B-Control@'+MODEL_REVISION
            receipt['guide_path']=str(guide_path)
            receipt['guide_sha256']=digest(guide_path)
            pipe=load_control()
            receipt['load_seconds']=time.time()-t
            sample_size=[height,width]
            video,mask,_=get_image_to_video_latent(None if reference else str(image_path),None,video_length=frames,sample_size=sample_size)
            control,_,_,_=get_video_to_video_latent(str(guide_path),video_length=frames,sample_size=sample_size,fps=16,ref_image=None)
            ref=get_image_latent(str(image_path),sample_size=sample_size)
            print('CONTROL_ENCODE_INPUT', list(control.shape), flush=True)
            receipt['control_input_shape']=list(control.shape)
            with torch.no_grad():
                sample=pipe(prompt,num_frames=frames,negative_prompt=negative,height=height,width=width,
                    generator=torch.Generator(device='cuda').manual_seed(43),guidance_scale=6.0,num_inference_steps=steps,
                    video=video,mask_video=mask,control_video=control,ref_image=ref,boundary=0.9,shift=5.0).videos
            result=[Image.fromarray(np.clip(sample[0,:,i].permute(1,2,0).cpu().float().numpy()*255,0,255).astype('uint8')) for i in range(frames)]
            receipt['guidance']=6.0
            receipt['image_roles']='appearance_reference' if reference else 'start_and_appearance_reference'
        if args.also_stationary:
            if args.case != 'controlled':
                raise ValueError('Stationary ablation requires controlled case')
            ablation_start=time.time()
            stationary_path=RUN/'story_inputs/stationary_edges.mp4'
            static,_,_,_=get_video_to_video_latent(str(stationary_path),video_length=frames,sample_size=sample_size,fps=16,ref_image=None)
            with torch.no_grad():
                ablation=pipe(prompt,num_frames=frames,negative_prompt=negative,height=height,width=width,
                    generator=torch.Generator(device='cuda').manual_seed(43),guidance_scale=6.0,num_inference_steps=steps,
                    video=video,mask_video=mask,control_video=static,ref_image=ref,boundary=0.9,shift=5.0).videos
            static_frames=[Image.fromarray(np.clip(ablation[0,:,i].permute(1,2,0).cpu().float().numpy()*255,0,255).astype('uint8')) for i in range(frames)]
            export_to_video(static_frames,str(out/'stationary.mp4'),fps=16)
            for i in (0,frames//4,frames//2,3*frames//4,frames-1):
                static_frames[i].save(out/f'stationary_{i:03d}.png')
            receipt['ablation']=dict(change='stationary control; all other settings including seed unchanged',
                guide_sha256=digest(stationary_path),output_sha256=digest(out/'stationary.mp4'),seconds=time.time()-ablation_start)
        torch.cuda.synchronize()
        receipt['inference_seconds']=time.time()-t-receipt['load_seconds']
        export_to_video(result,str(out/'output.mp4'),fps=16)
        for i in (0,frames//4,frames//2,3*frames//4,frames-1):
            result[i].save(out/f'frame_{i:03d}.png')
        receipt.update(status='complete',output_sha256=digest(out/'output.mp4'),decoded_frames=len(result),
                       peak_hbm_allocated_bytes=torch.cuda.max_memory_allocated(),peak_hbm_reserved_bytes=torch.cuda.max_memory_reserved())
    except BaseException:
        receipt.update(status='failed',error=traceback.format_exc())
        raise
    finally:
        receipt.update(total_seconds=time.time()-started,peak_host_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        (out/'receipt.tmp').write_text(json.dumps(receipt,indent=2))
        (out/'receipt.tmp').replace(out/'receipt.json')
        print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':
    main()
