#!/usr/bin/env python3
"""Encode actual Blender frames using the same Canny representation as the proxy."""
import hashlib
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control/feasibility_20261016'


def main():
    if not os.environ.get('SLURM_JOB_ID'): raise SystemExit('Guide encoding requires an allocation')
    import cv2
    import imageio.v2 as imageio
    import numpy as np
    from PIL import Image
    from feltwillow.media import locate_ffmpeg
    os.environ['IMAGEIO_FFMPEG_EXE']=str(locate_ffmpeg())
    path=RUN/'story_inputs/blender_edges.mp4'
    if path.exists(): raise SystemExit('Refusing guide overwrite')
    files=sorted((RUN/'blender_cpu').glob('[0-9]*.png'))
    if len(files)!=33: raise RuntimeError('Expected 33 Blender frames')
    source=np.array(Image.open(RUN/'story_inputs/start_fitted.png').convert('RGB'))
    rgb0=np.array(Image.open(files[0]).convert('RGB'))
    mae=float(np.abs(rgb0.astype(float)-source).mean())
    if mae>10: raise RuntimeError(f'Blender initial-frame alignment/color mismatch: MAE {mae}')
    with imageio.get_writer(path,fps=16,codec='libx264',pixelformat='yuv420p',quality=9,macro_block_size=1) as writer:
        for file in files:
            im=np.array(Image.open(file).convert('RGB'))
            edge=cv2.Canny(im,100,200)
            writer.append_data(np.repeat(edge[:,:,None],3,axis=2))
    (RUN/'blender_cpu/control_receipt.json').write_text(json.dumps(dict(status='complete',production_eligible=False,
        frames=33,width=416,height=240,fps=16,representation='Canny 100/200 RGB uint8 white on black',
        initial_frame_mae_0_255=mae,guide_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        job_id=os.environ['SLURM_JOB_ID']),indent=2))
    print('BLENDER_GUIDE_READY',mae,flush=True)

if __name__=='__main__': main()
