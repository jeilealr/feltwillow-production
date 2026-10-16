#!/usr/bin/env python3
"""Build a four-way review video from completed saved experimental clips."""
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control/feasibility_20261016'


def main():
    import imageio.v2 as imageio
    import numpy as np
    from PIL import Image,ImageDraw
    from feltwillow.media import locate_ffmpeg
    os.environ['IMAGEIO_FFMPEG_EXE']=str(locate_ffmpeg())
    cases=[('Normal I2V: Lightning, 4 steps','baseline_fast_smoke_33'),
           ('Plain I2V: 28 steps','baseline_smoke_33_cached'),
           ('Python Canny guide: 28 steps','controlled_smoke_33'),
           ('Blender Canny guide: 28 steps','blender_smoke_33')]
    clips=[]
    for label,name in cases:
        folder=RUN/name
        receipt=json.loads((folder/('recovery_receipt.json' if name=='baseline_smoke_33_cached' else 'receipt.json')).read_text())
        if receipt['status']!='complete': raise RuntimeError('Incomplete case: '+name)
        with imageio.get_reader(folder/'output.mp4') as reader:
            frames=[frame for frame in reader]
        if len(frames)!=33 or frames[0].shape!=(240,416,3): raise RuntimeError('Clip format mismatch')
        clips.append((label,frames))
    poster=None
    with imageio.get_writer(RUN/'comparison_4way.mp4',fps=16,codec='libx264',quality=9,macro_block_size=1) as writer:
        for i in range(33):
            canvas=Image.new('RGB',(832,528),'#202020')
            draw=ImageDraw.Draw(canvas)
            for index,(label,frames) in enumerate(clips):
                x,y=(index%2)*416,(index//2)*264
                draw.text((x+6,y+6),label,fill='white')
                canvas.paste(Image.fromarray(frames[i]),(x,y+24))
            writer.append_data(np.array(canvas))
            if i==8: poster=canvas.copy()
    poster.save(RUN/'comparison_frame_008.png')
    print(RUN/'comparison_4way.mp4')

if __name__=='__main__': main()
