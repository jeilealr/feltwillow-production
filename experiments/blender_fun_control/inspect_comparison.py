#!/usr/bin/env python3
"""CPU-only clip inspection, contact sheets and normalized motion diagnostics."""
import argparse
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control/feasibility_20261016'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--baseline',default='baseline_smoke_33')
    ap.add_argument('--controlled',default='controlled_smoke_33')
    args=ap.parse_args()
    import cv2
    import numpy as np
    from PIL import Image,ImageDraw
    import imageio.v2 as imageio
    from feltwillow.media import locate_ffmpeg
    os.environ['IMAGEIO_FFMPEG_EXE']=str(locate_ffmpeg())
    source=np.array(Image.open(RUN/'story_inputs/start_fitted.png').convert('RGB'))
    clips={'baseline':RUN/args.baseline/'output.mp4','controlled':RUN/args.controlled/'output.mp4',
           'stationary':RUN/args.controlled/'stationary.mp4'}
    rois={'head':(.34,.12,.69,.52),'acorn':(.46,.51,.66,.73),'feet':(.34,.72,.59,.80),'background':(.02,.25,.25,.75)}
    result={}
    all_frames={}
    for name,path in clips.items():
        if not path.exists(): continue
        frames=list(imageio.get_reader(path))
        all_frames[name]=frames
        h,w=frames[0].shape[:2]
        source_resized=cv2.resize(source,(w,h))
        metrics={'frames':len(frames),'width':w,'height':h,
                 'first_frame_mae_0_255':float(np.abs(frames[0].astype(float)-source_resized).mean()),
                 'mean_consecutive_rgb_difference':float(np.mean([np.abs(b.astype(float)-a).mean() for a,b in zip(frames,frames[1:])]))}
        previous=cv2.cvtColor(frames[0],cv2.COLOR_RGB2GRAY)
        flows={k:[] for k in rois}
        for frame in frames[1:]:
            gray=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
            flow=cv2.calcOpticalFlowFarneback(previous,gray,None,.5,3,15,3,5,1.2,0)
            for region,(x0,y0,x1,y1) in rois.items():
                f=flow[int(y0*h):int(y1*h),int(x0*w):int(x1*w)]
                flows[region].append({'median_dx_px':float(np.median(f[:,:,0])),
                                      'median_dy_px':float(np.median(f[:,:,1])),
                                      'mean_magnitude_px':float(np.linalg.norm(f,axis=2).mean())})
            previous=gray
        metrics['flow_by_roi']=flows
        result[name]=metrics
        sheet=Image.new('RGB',(w*7,(h+22)*5),'#202020')
        d=ImageDraw.Draw(sheet)
        for i,f in enumerate(frames):
            x,y=(i%7)*w,(i//7)*(h+22)
            sheet.paste(Image.fromarray(f),(x,y+22)); d.text((x+3,y+3),f'{name}: frame {i}',fill='white')
        sheet.save(RUN/f'{name}_all_frames.jpg',quality=94)
    result['limitations']=['Optical flow measures pixel motion, not anatomical correctness or semantic control adherence.',
                          'Fixed normalized regions are approximate and must be checked against actual output.',
                          'Low-resolution short diagnostic does not establish production quality.']
    (RUN/'motion_metrics.json').write_text(json.dumps(result,indent=2))
    names=list(all_frames)
    if names and len({len(v) for v in all_frames.values()})==1:
        with imageio.get_writer(RUN/'comparison.mp4',fps=16,codec='libx264',quality=9,macro_block_size=1) as writer:
            for i in range(len(all_frames[names[0]])):
                panes=[]
                for name in names:
                    im=Image.fromarray(all_frames[name][i]); bar=Image.new('RGB',(im.width,24),'#202020')
                    ImageDraw.Draw(bar).text((5,5),name,fill='white')
                    pane=Image.new('RGB',(im.width,im.height+24));pane.paste(bar,(0,0));pane.paste(im,(0,24))
                    panes.append(np.array(pane))
                writer.append_data(np.concatenate(panes,axis=1))
    print(json.dumps({name:{k:v for k,v in row.items() if k!='flow_by_roi'} for name,row in result.items() if isinstance(row,dict)},indent=2))

if __name__=='__main__': main()
