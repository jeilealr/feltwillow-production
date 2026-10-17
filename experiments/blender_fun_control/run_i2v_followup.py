#!/usr/bin/env python3
"""Isolated long-shot and two-shot Lightning comparison; allocated compute only."""
import argparse
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import time
import traceback
from run_case import digest

ROOT = Path(__file__).resolve().parents[2]
PRIOR = ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control/feasibility_20261016'
RUN = PRIOR.parent/'i2v_followup_20261016'
PROMPT = ('A single small grey needle-felt mouse Milo sits on the grass beside the stream, holding one acorn in both paws. '
          'He gently brings the acorn toward his mouth, nibbles, and lowers it, with a small natural head nod. '
          'His feet stay planted. Fixed camera, unchanged framing and mouse size, softly flowing stream, warm afternoon light, felt storybook animation.')
NEGATIVE = 'extra animals, extra limbs, deformed paws, face distortion, changing identity, camera movement, zoom, cuts, flicker, text, subtitles'


def pixels(frame):
    import numpy as np
    from PIL import Image
    if isinstance(frame, Image.Image):
        return frame.convert('RGB')
    array = np.asarray(frame)
    if not np.isfinite(array).all():
        raise ValueError('Non-finite generated pixels')
    if np.issubdtype(array.dtype, np.floating) and array.min() >= 0 and array.max() <= 1:
        array = array * 255
    return Image.fromarray(np.clip(array, 0, 255).astype('uint8')).convert('RGB')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage',choices=['all','first','continuations'],default='all')
    args=ap.parse_args()
    if not os.environ.get('SLURM_JOB_ID'):
        raise SystemExit('Inference and review rendering require a SLURM allocation')
    if args.stage=='continuations':
        first=json.loads((RUN/'receipt_first.json').read_text())
        if first['status']!='complete' or first['cases'][0]['last_exact_sha256']!=digest(RUN/'long_81/last_exact.png'):
            raise RuntimeError('First stage incomplete or changed')
    else:
        RUN.mkdir(exist_ok=False)
    receipt_path=RUN/('receipt.json' if args.stage=='all' else 'receipt_'+args.stage+'.json')
    if receipt_path.exists():raise RuntimeError('Stage already attempted')
    shutil.copyfile(__file__, RUN/('executed_runner_'+args.stage+'.py'))
    receipt = dict(status='running', production_eligible=False,
        approval='isolated_experiment_not_for_production', stage=args.stage,
        job_id=os.environ['SLURM_JOB_ID'], partition=os.environ.get('SLURM_JOB_PARTITION'),
        repo_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        script_sha256=digest(__file__), width=832, height=480, frames=81, fps=16,
        steps=4, guidance=[1.0,1.0], prompt=PROMPT, negative_prompt=NEGATIVE,
        end_conditioning='none', cases=[], started_epoch=time.time(),
        comparison_limit='Next keyframe changes subject size and pose: deliberate new-shot cut, not seamless continuation. Duration and resolution both differ from prior pilot.')
    try:
        import torch
        import numpy as np
        import imageio.v2 as imageio
        from PIL import Image, ImageDraw
        from feltwillow import wan
        from feltwillow.media import locate_ffmpeg
        os.environ['IMAGEIO_FFMPEG_EXE'] = str(locate_ffmpeg())
        if not torch.cuda.is_available() or not torch.version.hip:
            raise RuntimeError('Expected allocated ROCm GPU')
        torch.set_num_threads(int(os.environ.get('SLURM_CPUS_PER_TASK','7')))
        receipt['environment'] = dict(torch=torch.__version__,hip=torch.version.hip,gpu=torch.cuda.get_device_name(0))
        receipt['model'] = wan.model_id('i2v')
        receipt['lightning'] = wan.LIGHTNING
        cache = ROOT.parent/'models/video_control_baseline_bf16'/wan.REVISIONS['i2v']
        proof = cache/'conversion_receipt.json'
        verified = json.loads(proof.read_text())
        if verified.get('status') != 'complete' or verified.get('revision') != wan.REVISIONS['i2v']:
            raise RuntimeError('Unverified baseline storage cache')
        receipt['cache_proof_sha256'] = digest(proof)
        wan.MODELS['i2v'] = str(cache)  # process only; existing bf16 precision
        inputs = RUN/'inputs'
        inputs.mkdir(exist_ok=args.stage=='continuations')
        for source,name in [('start.png','start'),('end_evaluation.png','next_keyframe')]:
            if args.stage!='continuations':
                shutil.copyfile(PRIOR/'story_inputs'/source,inputs/(name+'_original.png'))
                wan.fit(Image.open(inputs/(name+'_original.png')),832,480).save(inputs/(name+'.png'))
            elif digest(inputs/(name+'_original.png'))!=first['sources'][name+'_original.png'] or digest(inputs/(name+'.png'))!=first['sources'][name+'.png']:
                raise RuntimeError('Frozen input changed between stages')
        receipt['sources'] = {p.name:digest(p) for p in inputs.glob('*.png')}
        started = time.time()
        pipe = wan.load('i2v',frames=81,fast=True)
        receipt['load_seconds'] = time.time()-started
        lightning = wan.lightning_lora()
        receipt['lora_hashes'] = {key:digest(lightning[key]) for key in ('high','low')}
        cases = [('long_81',inputs/'start.png',43),
                 ('continue_generated',RUN/'long_81'/'last_exact.png',44),
                 ('restart_keyframe',inputs/'next_keyframe.png',44)]
        if args.stage=='first':cases=cases[:1]
        elif args.stage=='continuations':cases=cases[1:]
        decoded = {}
        if args.stage=='continuations':
            proof=json.loads((RUN/'long_81/receipt.json').read_text())
            if proof['status']!='complete' or proof['output_sha256']!=digest(RUN/'long_81/output.mp4'):raise RuntimeError('First clip integrity failure')
            with imageio.get_reader(RUN/'long_81/output.mp4') as reader:decoded['long_81']=[f for f in reader]
        for name,image_path,seed in cases:
            folder = RUN/name
            folder.mkdir()
            item = dict(name=name,status='running',seed=seed,source=str(image_path),source_sha256=digest(image_path))
            receipt['cases'].append(item)
            receipt_path.write_text(json.dumps(receipt,indent=2))
            torch.cuda.reset_peak_memory_stats()
            started = time.time()
            print('START_CASE',name,flush=True)
            result = wan.generate(pipe,PROMPT,negative=NEGATIVE,width=832,height=480,frames=81,
                steps=4,guidance=1.0,guidance_2=1.0,seed=seed,image=Image.open(image_path))
            result = [pixels(frame) for frame in result]
            if len(result)!=81 or any(frame.size!=(832,480) for frame in result):
                raise RuntimeError('Unexpected output geometry')
            torch.cuda.synchronize()
            item['inference_seconds'] = time.time()-started
            wan.save(result,folder/'output.mp4',fps=16)
            result[-1].save(folder/'last_exact.png')
            result[0].save(folder/'first_exact.png')
            sheet = Image.new('RGB',(9*208,9*140),'#202020')
            draw = ImageDraw.Draw(sheet)
            for index,frame in enumerate(result):
                x,y = index%9*208,index//9*140
                sheet.paste(frame.resize((208,120)),(x,y+20))
                draw.text((x+3,y+3),str(index),fill='white')
            sheet.save(folder/'all_frames.jpg')
            for index in (0,20,40,60,80):
                result[index].save(folder/f'frame_{index:03d}.png')
            with imageio.get_reader(folder/'output.mp4') as reader:
                decoded[name] = [frame for frame in reader]
                item['encoded_fps'] = reader.get_meta_data()['fps']
            if len(decoded[name])!=81 or decoded[name][0].shape!=(480,832,3) or item['encoded_fps']!=16:
                raise RuntimeError('Export format mismatch')
            item.update(status='complete',frames=81,output_sha256=digest(folder/'output.mp4'),
                peak_hbm_bytes=torch.cuda.max_memory_allocated(),last_exact_sha256=digest(folder/'last_exact.png'))
            (folder/'receipt.json').write_text(json.dumps(dict(production_eligible=False,**item),indent=2))
            receipt_path.write_text(json.dumps(receipt,indent=2))
            del result
            print('COMPLETE_CASE',name,item,flush=True)
        if args.stage!='first':
            with imageio.get_writer(RUN/'continuity_comparison.mp4',fps=16,codec='libx264',quality=9,macro_block_size=1) as writer:
                for index in range(162):
                    canvas = Image.new('RGB',(1664,512),'#202020')
                    draw = ImageDraw.Draw(canvas)
                    for column,name,label in [(0,'continue_generated','A: extend from exact generated last frame'),
                        (1,'restart_keyframe','B: new shot from existing next keyframe (cut)')]:
                        frame = decoded['long_81'][index] if index<81 else decoded[name][index-81]
                        canvas.paste(Image.fromarray(frame),(column*832,32))
                        draw.text((column*832+8,8),label,fill='white')
                    writer.append_data(np.array(canvas))
            receipt['review_sha256'] = digest(RUN/'continuity_comparison.mp4')
        receipt['status'] = 'complete'
    except BaseException:
        receipt.update(status='failed',error=traceback.format_exc())
        raise
    finally:
        receipt['elapsed_seconds'] = time.time()-receipt['started_epoch']
        receipt['peak_host_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        receipt_path.write_text(json.dumps(receipt,indent=2))
        print(json.dumps(receipt,indent=2),flush=True)


if __name__ == '__main__':
    main()
