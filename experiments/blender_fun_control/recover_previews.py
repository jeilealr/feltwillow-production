#!/usr/bin/env python3
"""Recover CPU previews from an already saved baseline clip; retain raw failure."""
import hashlib
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'work/stories/lion_and_mouse_v6/experiments/blender_fun_control/feasibility_20261016/baseline_smoke_33_cached'


def main():
    import imageio.v2 as imageio
    from PIL import Image
    from feltwillow.media import locate_ffmpeg
    os.environ['IMAGEIO_FFMPEG_EXE']=str(locate_ffmpeg())
    original=RUN/'receipt.json'
    failure=json.loads(original.read_text())
    if failure['status']!='failed' or 'has no attribute' not in failure.get('error',''):
        raise RuntimeError('Expected preview-only failure')
    with imageio.get_reader(RUN/'output.mp4') as reader:
        metadata=reader.get_meta_data()
        frames=[frame for frame in reader]
    if len(frames)!=33 or frames[0].shape!=(240,416,3) or abs(metadata['fps']-16)>1e-6:
        raise RuntimeError('Unexpected saved clip format')
    for i in (0,8,16,24,32): Image.fromarray(frames[i]).save(RUN/f'frame_{i:03d}.png')
    result=dict(status='complete',production_eligible=False,recovery='CPU previews and decoder validation only; no inference rerun',
        original_job_id='22908225',original_job_status='failed_in_preview_export',
        original_receipt_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
        output_sha256=hashlib.sha256((RUN/'output.mp4').read_bytes()).hexdigest(),frames=len(frames),fps=metadata['fps'],width=416,height=240)
    (RUN/'recovery_receipt.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
