#!/usr/bin/env python3
"""Freeze P1 source only. Guide generation requires an allocated CPU/GPU node."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control/feasibility_20261016'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--guides',action='store_true')
    ap.add_argument('--frames',type=int,default=81)
    ap.add_argument('--width',type=int,default=832)
    ap.add_argument('--height',type=int,default=480)
    args=ap.parse_args()
    source=ROOT/'character/characters/lion_and_mouse_v6/interactions/keyframes/s01x_p03_r01_candidate.png'
    out=RUN/'story_inputs'
    if not args.guides:
        out.mkdir(exist_ok=False)
        shutil.copyfile(source,out/'start.png')
        shutil.copyfile(ROOT/'character/characters/lion_and_mouse_v6/interactions/keyframes/s01_p04_r02_candidate.png',out/'end_evaluation.png')
        (out/'source.json').write_text(json.dumps(dict(production_eligible=False,start_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            end_image_role='evaluation_only',hypothesis='Controlled acorn/head motion with fixed feet and camera; no identity loss.'),indent=2))
        return
    if not os.environ.get('SLURM_JOB_ID'):
        raise SystemExit('Guide rendering requires an allocation')
    if not any(p.exists() and json.loads(p.read_text())['status']=='complete' for p in (RUN/'reference/receipt.json',RUN/'diagnostic/receipt.json')):
        raise SystemExit('Reference backend render must complete before custom guides')
    if (out/'moving_edges.mp4').exists() or (out/'stationary_edges.mp4').exists():
        raise SystemExit('Guide files already exist; use a new run root rather than overwrite')
    import cv2
    import imageio.v2 as imageio
    import numpy as np
    from PIL import Image
    from feltwillow.wan import fit
    width,height,frames=args.width,args.height,args.frames
    if frames < 5 or (frames-1)%4 or width%16 or height%16:
        raise SystemExit('Unsupported frame/dimension shape')
    im=np.array(fit(Image.open(out/'start.png'),width,height))
    Image.fromarray(im).save(out/'start_fitted.png')
    # Image-space proxy: fixed feet/background, gentle movement in head/acorn area.
    # This is an experimental deformed guide source, never a canonical image edit.
    y,x=np.mgrid[:height,:width].astype('float32')
    head=np.exp(-(((x-width*.50)/(width*.17))**4+((y-height*.38)/(height*.22))**4))
    acorn=np.exp(-(((x-width*.55)/(width*.085))**4+((y-height*.64)/(height*.13))**4))
    head*=np.clip((height*.77-y)/(height*.14),0,1)
    acorn*=np.clip((height*.79-y)/(height*.09),0,1)
    edge0=cv2.Canny(im,100,200)
    from feltwillow.media import locate_ffmpeg
    os.environ['IMAGEIO_FFMPEG_EXE']=str(locate_ffmpeg())
    with imageio.get_writer(out/'moving_edges.mp4',fps=16,codec='libx264',pixelformat='yuv420p',quality=9,macro_block_size=1) as moving, \
         imageio.get_writer(out/'stationary_edges.mp4',fps=16,codec='libx264',pixelformat='yuv420p',quality=9,macro_block_size=1) as stationary:
        for i in range(frames):
            # Cycle starts/ends at source; two small nibbling motions, planted feet unchanged.
            a=math.sin(2*math.pi*i/(frames-1))**2
            dy=4*a*head+6*a*acorn
            warped=cv2.remap(im,x,y+dy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
            edges=cv2.Canny(warped,100,200)
            moving.append_data(np.repeat(edges[:,:,None],3,axis=2))
            stationary.append_data(np.repeat(edge0[:,:,None],3,axis=2))
            if i in (0,20,40,60,80):
                Image.fromarray(edges).save(out/f'guide_{i:03d}.png')
    (out/'motion_spec.json').write_text(json.dumps(dict(schema='feltwillow.proxy-motion.v0-proposal',production_eligible=False,
        representation='Canny RGB 8bit white edges on black',canny_thresholds=[100,200],fps=16,frames=frames,width=width,height=height,
        description='Image-space smooth local head/acorn deformation; original feet and background fixed; not a 3D rig or anatomy guarantee',
        max_head_displacement_px=4,max_acorn_displacement_px=6,phase=f'sin(2*pi*i/{frames-1})^2',
        image_transform='feltwillow.wan.fit, shared with baseline',allocation=os.environ['SLURM_JOB_ID']),indent=2))

if __name__=='__main__': main()
