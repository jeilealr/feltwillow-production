#!/usr/bin/env python3
"""Allocated-only sparse Canny diagnostic using saved actual Blender renders."""
import json
import os
from pathlib import Path
import shutil
import sys

import run_case

PRIOR = run_case.RUN
RUN = PRIOR.parent/'blender_sparse_probe_20261016'


def main():
    if not os.environ.get('SLURM_JOB_ID'):
        raise SystemExit('Requires a SLURM allocation')
    import cv2
    import imageio.v2 as imageio
    import numpy as np
    from PIL import Image, ImageDraw
    from feltwillow.media import locate_ffmpeg
    os.environ['IMAGEIO_FFMPEG_EXE'] = str(locate_ffmpeg())
    reference = json.loads((PRIOR/'blender_smoke_33/receipt.json').read_text())
    if reference['status']!='complete' or reference['output_sha256']!=run_case.digest(PRIOR/'blender_smoke_33/output.mp4'):
        raise RuntimeError('Original Blender-conditioned reference integrity check failed')
    RUN.mkdir(exist_ok=False)
    shutil.copyfile(__file__,RUN/'executed_probe.py')
    inputs = RUN/'story_inputs'
    inputs.mkdir()
    source = PRIOR/'story_inputs/start_fitted.png'
    if run_case.digest(source)!=reference['source_image_sha256']:
        raise RuntimeError('Original start image changed')
    shutil.copyfile(source,inputs/'start_fitted.png')
    y,x = np.mgrid[:240,:416]
    # Coarse experimental image-space mask, not canonical segmentation/staging.
    head = ((x/416-.50)/.235)**2+((y/240-.37)/.30)**2 < 1
    body = ((x/416-.45)/.18)**2+((y/240-.66)/.23)**2 < 1
    acorn = ((x/416-.55)/.115)**2+((y/240-.65)/.18)**2 < 1
    tail = ((x/416-.32)/.10)**2+((y/240-.65)/.20)**2 < 1
    face_inside = ((x/416-.515)/.105)**2+((y/240-.435)/.13)**2 < 1
    mask = (head|body|acorn|tail)&~face_inside
    Image.fromarray((mask*255).astype('uint8')).save(RUN/'guide_mask.png')
    files = sorted((PRIOR/'blender_cpu').glob('[0-9]*.png'))
    if len(files)!=33:
        raise RuntimeError('Expected 33 actual Blender frames')
    hashes = {}
    with imageio.get_writer(inputs/'blender_edges.mp4',fps=16,codec='libx264',pixelformat='yuv420p',quality=9,macro_block_size=1) as writer:
        for index,path in enumerate(files):
            edges = cv2.Canny(np.array(Image.open(path).convert('RGB')),100,200)
            edges[~mask] = 0  # After Canny: do not invent a mask-border contour.
            rgb = np.repeat(edges[:,:,None],3,axis=2)
            writer.append_data(rgb)
            if index in (0,8,16,24,32):
                Image.fromarray(rgb).save(RUN/f'guide_{index:03d}.png')
            hashes[path.name] = run_case.digest(path)
    proof = dict(status='complete',production_eligible=False,job_id=os.environ['SLURM_JOB_ID'],
        script_sha256=run_case.digest(__file__),blender_source_hashes=hashes,
        reference_receipt_sha256=run_case.digest(PRIOR/'blender_smoke_33/receipt.json'),
        guide_sha256=run_case.digest(inputs/'blender_edges.mp4'),mask_sha256=run_case.digest(RUN/'guide_mask.png'),
        hypothesis='Removing most background and inner-face Canny constraints permits richer acting while retaining Blender-authored motion.',
        caveat='Coarse fixed ROI, not segmentation. Background edges inside it remain. Sparse Canny is experimental; this does not test articulated 3D or depth.')
    (RUN/'prepare_receipt.json').write_text(json.dumps(proof,indent=2))
    # Reuse the already tested inference/receipt path, only isolated run root differs.
    run_case.RUN = RUN
    sys.argv = [str(Path(run_case.__file__)), '--case','blender','--run-name','sparse_smoke_33',
                '--frames','33','--width','416','--height','240','--steps','28']
    run_case.main()
    result = json.loads((RUN/'sparse_smoke_33/receipt.json').read_text())
    for key in ('prompt','negative_prompt','source_image_sha256','seed','fps','frames','width','height','steps','guidance','model','backend_commit'):
        if result[key]!=reference[key]:
            raise RuntimeError('Reference setting mismatch: '+key)
    paths = [PRIOR/'baseline_fast_smoke_33/output.mp4',PRIOR/'blender_smoke_33/output.mp4',RUN/'sparse_smoke_33/output.mp4']
    clips = []
    for path in paths:
        with imageio.get_reader(path) as reader:
            clip = [frame for frame in reader]
            if len(clip)!=33 or clip[0].shape!=(240,416,3) or reader.get_meta_data()['fps']!=16:
                raise RuntimeError('Encoded video format mismatch')
            clips.append(clip)
    sheet = Image.new('RGB',(7*416,5*264),'#202020')
    draw = ImageDraw.Draw(sheet)
    for index,frame in enumerate(clips[2]):
        x,y = index%7*416,index//7*264
        sheet.paste(Image.fromarray(frame),(x,y+24));draw.text((x+4,y+4),str(index),fill='white')
    sheet.save(RUN/'all_frames.jpg')
    with imageio.get_writer(RUN/'comparison_3way.mp4',fps=16,codec='libx264',quality=9,macro_block_size=1) as writer:
        for index in range(33):
            canvas = Image.new('RGB',(1248,264),'#202020');draw = ImageDraw.Draw(canvas)
            for column,label in enumerate(['Normal Wan Lightning 4 steps','Blender full Canny 28 steps','Blender sparse Canny 28 steps']):
                canvas.paste(Image.fromarray(clips[column][index]),(416*column,24))
                draw.text((416*column+4,4),label,fill='white')
            writer.append_data(np.array(canvas))
    (RUN/'comparison_receipt.json').write_text(json.dumps(dict(status='complete',production_eligible=False,
        comparison_sha256=run_case.digest(RUN/'comparison_3way.mp4'),settings_match=True,
        caveat='Full-versus-sparse Control holds model/settings fixed. Normal Wan is a different model/step configuration.'),indent=2))


if __name__=='__main__':
    main()
