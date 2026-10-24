#!/usr/bin/env python3
"""Replay preserved probes: original vs historical fixed patch vs tracked mouth.

No generation or asset adoption. Writes one compact audio comparison per actor.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from feltwillow.mouth_tracking import composite_frames
from feltwillow.media import read_frames, locate_ffmpeg
from production.lip_sync import _anchors_and_mask, _alpha_at


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    os.environ['TMPDIR'] = str(ROOT.parent/'tmp')
    cv2.setNumThreads(int(os.environ.get('SLURM_CPUS_PER_TASK', '2')))
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-root', type=Path, default=ROOT.parent/'feltwillow-video-control/work/stories/lion_and_mouse_v6/experiments/lipsync_probe/20261017')
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    ffmpeg = locate_ffmpeg()
    manifest = json.loads((args.source_root/'inputs/manifest.json').read_text())
    alignment = json.loads((args.source_root/'alignment/receipt.json').read_text())
    receipts = []
    for case in manifest['cases']:
        name = case['character']
        line = alignment['lines'][name]
        for role, path in line['fitted'].items():
            assert sha(path) == line['fitted_hashes'][role], path
        source = args.source_root/'video_probe'/(name+'_wan.mp4')
        prior = json.loads((args.source_root/('wan_'+name)/'receipt.json').read_text())
        assert sha(source) == prior['source_sha256']
        frames = read_frames(source)
        h, w = frames.shape[1:3]
        closed, opened, mask = _anchors_and_mask(Path(line['fitted']['closed']), Path(line['fitted']['open_candidate']), (w,h), tuple(case['roi']))
        amounts = [0. if i in (0,len(frames)-1) else _alpha_at(i/16,prior['cues']) for i in range(len(frames))]
        tracked, report = composite_frames(frames,closed,opened,mask,case['roi'],amounts,diagnostic=True)
        # Historical baseline includes its original broad mask and silent patch.
        diff = np.abs(opened-closed).max(axis=2)
        x0,y0,x1,y1 = np.rint(np.array(case['roi'])*[w,h,w,h]).astype(int)
        legacy = np.zeros((h,w),np.uint8)
        legacy[y0:y1,x0:x1] = (diff[y0:y1,x0:x1]>=18).astype(np.uint8)*255
        legacy = np.asarray(Image.fromarray(legacy).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2)),dtype=np.float32)[:,:,None]/255
        fixed = np.array([frame if i in (0,len(frames)-1) else np.clip(frame.astype(np.float32)*(1-legacy)+(closed*(1-amounts[i])+opened*amounts[i])*legacy,0,255).astype(np.uint8) for i,frame in enumerate(frames)])
        silent = np.array(amounts)==0
        assert np.array_equal(tracked[silent],frames[silent])
        out = args.out/name
        out.mkdir()
        active = [r for r in report['frames'] if r['status']=='tracked']
        item = dict(character=name,source_sha256=sha(source),input_receipt_sha256=sha(args.source_root/('wan_'+name)/'receipt.json'),
            tracking=report,active_frames=sum(a>0 for a in amounts),tracked_active_frames=len(active),
            no_cue_frames=int(silent.sum()),no_cue_raw_max_difference=int(np.abs(tracked[silent].astype(int)-frames[silent].astype(int)).max()),
            previous_no_cue_raw_mean_difference=float(np.abs(fixed[silent].astype(float)-frames[silent].astype(float)).mean()),
            limitations=['Unapproved diagnostic calibration assets.', 'Small in-plane motion only; turns/occlusions reject active frames.',
                        'One open shape with word/vowel pulses, not phoneme visemes.',
                        'Playback review required; feature fit is not independent mouth accuracy.'])
        (out/'receipt.json').write_text(json.dumps(item,indent=2))
        indices=sorted(set([next(i for i,a in enumerate(amounts) if a>0),int(np.argmax(amounts)),max(i for i,a in enumerate(amounts) if a>0)]))
        sheet=Image.new('RGB',(720,210*len(indices)),'#202020')
        draw=ImageDraw.Draw(sheet)
        cx,cy=round((case['roi'][0]+case['roi'][2])*w/2),round((case['roi'][1]+case['roi'][3])*h/2)
        for row,i in enumerate(indices):
            for col,(label,arr) in enumerate(zip(['Source','Fixed','Tracked'],[frames,fixed,tracked])):
                crop=Image.fromarray(arr[i]).crop((cx-90,cy-65,cx+90,cy+65)).resize((240,174))
                sheet.paste(crop,(col*240,row*210+30))
                draw.text((col*240+3,row*210+5),f'{label} frame {i}',fill='white')
        sheet.save(out/'mouth_comparison.jpg')
        audio=args.source_root/('wan_'+name)/'padded_audio.wav'
        width,height=w*3//2,h//2+30
        video=out/'comparison_with_audio.mp4'
        proc=subprocess.Popen([ffmpeg,'-nostdin','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{height}','-r','16','-i','-',
            '-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','24','-threads','2',
            '-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
        try:
            for i,frame in enumerate(frames):
                canvas=Image.new('RGB',(width,height),'#202020')
                draw=ImageDraw.Draw(canvas)
                for j,(label,img) in enumerate(zip(['Source','Previous fixed patch','Tracked mouth delta'],[frame,fixed[i],tracked[i]])):
                    canvas.paste(Image.fromarray(img).resize((w//2,h//2)),(j*w//2,30))
                    draw.text((j*w//2+5,8),f'{label} / {i} / {report["frames"][i]["status"]}',fill='white')
                proc.stdin.write(np.asarray(canvas).tobytes())
        finally:
            proc.stdin.close()
            rc=proc.wait()
        if rc:
            raise RuntimeError(f'Comparison export failed, ffmpeg exit {rc}')
        decoded=read_frames(video)
        assert len(decoded)==len(frames) and decoded.shape[1:3]==(height,width)
        item['output_sha256']={video.name:sha(video),'mouth_comparison.jpg':sha(out/'mouth_comparison.jpg')}
        (out/'receipt.json').write_text(json.dumps(item,indent=2))
        receipts.append(item)
        print(json.dumps({k:v for k,v in item.items() if k not in ('tracking','output_sha256','limitations')}),flush=True)
    (args.out/'receipt.json').write_text(json.dumps(dict(status='diagnostic_complete',production_eligible=False,
        code_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'feltwillow/mouth_tracking.py',ROOT/'production/lip_sync.py']},cases=receipts),indent=2))


if __name__=='__main__':
    main()
