"""Exercise the existing compositor using explicit unapproved test fixtures."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import wave

ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'work/stories/lion_and_mouse_v6/experiments/lipsync_probe/20261017'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compose(case,alignment,source,mode):
    import numpy as np
    import imageio.v2 as imageio
    from PIL import Image,ImageDraw
    from production.lip_sync import render_piece,_alpha_at
    from feltwillow.media import read_frames,locate_ffmpeg
    ffmpeg=locate_ffmpeg();os.environ['IMAGEIO_FFMPEG_EXE']=str(ffmpeg)
    name=case['character'];out=RUN/(mode+'_'+name);out.mkdir(exist_ok=False)
    frames=65;fps=16;duration=frames/fps;padding=.5
    cues=[dict(text=w['text'],start=w['start']+padding,end=w['end']+padding,line_id=case['line_id']) for w in alignment['words']]
    manifest={'production_eligible':False,'status':'unapproved_experimental_fixture',
        'shots':[dict(id='probe',start_image='closed',end_image='closed',variants=[dict(id='mouth',mode='mouth',speaker=case['speaker'],mouth_open_image='open')])],
        '_image_index':{'closed':dict(id='closed',target=alignment['fitted']['closed']),
          'open':dict(id='open',target=alignment['fitted']['open_candidate'],mouth_character=name,ordered_references=[dict(id='closed',role='edit_base')])}}
    bible={'characters':{name:dict(voice_speaker=case['speaker'],mouth_animation=dict(roi=case['roi']))}}
    row=dict(piece='probe',variant='mouth',frames=frames,seconds=duration,speed=1.)
    details=render_piece('isolated_lipsync_probe',row,source,out/'synced_silent.mp4',cues,manifest,bible,fps)
    render_piece('isolated_lipsync_probe',row,source,out/'no_cues_control.mp4',[],manifest,bible,fps)
    with wave.open(case['paths']['audio'],'rb') as original:
        rate=original.getframerate();data=original.readframes(original.getnframes())
        if original.getnchannels()!=1 or original.getsampwidth()!=2:raise RuntimeError('Expected mono PCM16')
    total=round(duration*rate);before=round(padding*rate);after=total-before-len(data)//2
    if after<0:raise RuntimeError('Recording does not fit clip')
    with wave.open(str(out/'padded_audio.wav'),'wb') as wav:
        wav.setparams((1,2,rate,0,'NONE','not compressed'));wav.writeframes(b'\0'*(before*2)+data+b'\0'*(after*2))
    subprocess.run([ffmpeg,'-nostdin','-v','error','-i',str(out/'synced_silent.mp4'),'-i',str(out/'padded_audio.wav'),
        '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out/'synced_with_audio.mp4')],check=True)
    source_frames=read_frames(source);synced=read_frames(out/'synced_silent.mp4');control=read_frames(out/'no_cues_control.mp4')
    if any(len(x)!=frames or x.shape[1:3]!=(432,768) for x in (source_frames,synced,control)):raise RuntimeError('Video geometry mismatch')
    amounts=[0. if i in (0,frames-1) else _alpha_at(i/fps,cues) for i in range(frames)]
    if any(a!=0 for i,a in enumerate(amounts) if i/fps<padding or i/fps>padding+alignment['audio_seconds']):raise RuntimeError('Mouth driven outside audio window')
    with imageio.get_writer(out/'review_silent.mp4',fps=fps,codec='libx264',quality=9,macro_block_size=1) as writer:
        for i,(a,b) in enumerate(zip(source_frames,synced)):
            canvas=Image.new('RGB',(1536,464),'#202020');draw=ImageDraw.Draw(canvas)
            canvas.paste(Image.fromarray(a),(0,32));canvas.paste(Image.fromarray(b),(768,32))
            active=' / '.join(c['text'] for c in cues if c['start']<=i/fps<=c['end'])
            draw.text((4,8),f'{name} {mode}: original | t={i/fps:.3f}s',fill='white')
            draw.text((772,8),f'word-timed composite: {active} / open={amounts[i]:.2f}',fill='white')
            writer.append_data(np.array(canvas))
    subprocess.run([ffmpeg,'-nostdin','-v','error','-i',str(out/'review_silent.mp4'),'-i',str(out/'padded_audio.wav'),
        '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k',str(out/'review_with_audio.mp4')],check=True)
    # Silence should match a no-cue composite within codec error, not byte-for-byte MP4 identity.
    delta=np.abs(synced.astype(float)-control.astype(float)).mean(axis=(1,2,3))
    silence=[i for i,a in enumerate(amounts) if a==0]
    flow=[];import cv2
    roi=case['roi'];x0,y0,x1,y1=round(roi[0]*768),round(roi[1]*432),round(roi[2]*768),round(roi[3]*432)
    previous=cv2.cvtColor(source_frames[0],cv2.COLOR_RGB2GRAY)
    for frame in source_frames[1:]:
        current=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
        field=cv2.calcOpticalFlowFarneback(previous,current,None,.5,3,15,3,5,1.2,0)
        flow.append(np.median(field[max(0,y0-20):min(432,y1+20),max(0,x0-20):min(768,x1+20)],axis=(0,1)))
        previous=current
    drift=float(np.linalg.norm(np.sum(flow,axis=0)))
    receipt=dict(status='complete',production_eligible=False,approval='unapproved_mouth_candidates_not_production',
        character=name,speaker=case['speaker'],mode=mode,source_sha256=sha(source),audio_sha256=case['hashes']['audio'],
        compositor_sha256=sha(ROOT/'production/lip_sync.py'),cues=cues,amounts=amounts,
        width=768,height=432,frames=65,fps=16,audio_padding_seconds=padding,
        silent_control_mean_difference=float(delta[silence].mean()),approx_source_mouth_region_accumulated_flow_px=drift,
        output_hashes={f.name:sha(f) for f in out.glob('*.mp4')},details=details,
        limitations=['Single open shape, broad word/vowel pulses: not phoneme-level sync.',
          'Fixed ROI does not track head/expression movement. Optical flow is approximate, not anatomy verification.',
          'First/last raw compositor frames preserved; lossy encoding is not pixel-exact.',
          'Only owner listening/playback can confirm perceptual timing; alignment is not ground truth.'])
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2))
    return receipt
