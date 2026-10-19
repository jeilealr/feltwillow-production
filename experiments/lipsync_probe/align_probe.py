#!/usr/bin/env python3
"""Two-line forced-alignment diagnostic, writing only isolated experiment data."""
import hashlib
import json
import os
from pathlib import Path
import time
import traceback
import wave

ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'work/stories/lion_and_mouse_v6/experiments/lipsync_probe/20261017'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    if not os.environ.get('SLURM_JOB_ID'):raise SystemExit('Allocated compute only')
    out=RUN/'alignment';out.mkdir(exist_ok=False)
    receipt=dict(status='running',production_eligible=False,job_id=os.environ['SLURM_JOB_ID'],
                 script_sha256=sha(__file__),start_epoch=time.time(),lines={})
    try:
        import numpy as np
        import torch
        import torchaudio
        import whisperx
        from production.lip_sync import token,_anchors_and_mask
        from feltwillow.wan import fit
        from PIL import Image
        torch.set_num_threads(int(os.environ.get('SLURM_CPUS_PER_TASK','7')))
        receipt['environment']=dict(torch=torch.__version__,torchaudio=torchaudio.__version__,device='cpu')
        manifest=json.loads((RUN/'inputs/manifest.json').read_text())
        print('ALIGNMENT_IMPORTS_OK',receipt['environment'],flush=True)
        model,metadata=whisperx.load_align_model(language_code='en',device='cpu',model_dir=os.environ['TORCH_HOME'])
        for case in manifest['cases']:
            for role,path in case['paths'].items():
                if sha(path)!=case['hashes'][role]:raise RuntimeError('Changed source '+role)
            with wave.open(case['paths']['audio'],'rb') as wav:
                if wav.getnchannels()!=1 or wav.getsampwidth()!=2:raise RuntimeError('Expected mono PCM16')
                rate=wav.getframerate();audio=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').astype('float32')/32768
            audio=torchaudio.functional.resample(torch.from_numpy(audio),rate,16000).numpy()
            duration=len(audio)/16000
            result=whisperx.align([dict(start=0.,end=duration,text=case['text'])],model,metadata,audio,'cpu',return_char_alignments=False)
            words=[dict(text=w['word'],start=float(w['start']),end=float(w['end']),score=w.get('score')) for segment in result['segments'] for w in segment['words'] if w.get('start') is not None and w.get('end') is not None]
            import re
            expected=[token(x) for x in re.findall(r"[\w']+",case['text'])]
            if [token(w['text']) for w in words]!=expected:raise RuntimeError('Aligned transcript mismatch '+case['line_id'])
            if not all(0<=w['start']<w['end']<=duration+.05 for w in words):raise RuntimeError('Invalid word intervals')
            fitted={}
            for role in ('closed','open_candidate'):
                path=out/(case['character']+'_'+role+'_768x432.png')
                fit(Image.open(case['paths'][role]),768,432).save(path);fitted[role]=str(path)
            closed,opened,mask=_anchors_and_mask(Path(fitted['closed']),Path(fitted['open_candidate']),(768,432),tuple(case['roi']))
            Image.fromarray(np.clip(mask[:,:,0]*255,0,255).astype('uint8')).save(out/(case['character']+'_mask.png'))
            # Report generated reference drift; never assume a prompt made all other pixels exact.
            outside=np.ones((432,768),bool)
            x0,y0,x1,y1=case['roi'];outside[round(y0*432):round(y1*432),round(x0*768):round(x1*768)]=False
            drift=float(np.abs(opened-closed)[outside].mean())
            receipt['lines'][case['character']]=dict(line_id=case['line_id'],speaker=case['speaker'],text=case['text'],
                audio_sha256=case['hashes']['audio'],audio_seconds=duration,words=words,status='aligned_needs_listening_review',
                fitted=fitted,fitted_hashes={k:sha(p) for k,p in fitted.items()},roi=case['roi'],mask_area=float(np.mean(mask>.2)),
                open_candidate_nonmouth_mae_0_255=drift,
                caveat='Generated calibration is unapproved and has nonmouth drift; compositor restricts application to ROI. No production readiness inferred.')
            print(case['character'],receipt['lines'][case['character']],flush=True)
        receipt['alignment_model_files']={str(p):sha(p) for p in Path(os.environ['TORCH_HOME']).glob('*.pth')}
        receipt['status']='complete'
    except BaseException:
        receipt.update(status='failed',error=traceback.format_exc());raise
    finally:
        receipt['elapsed_seconds']=time.time()-receipt['start_epoch']
        (out/'receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':main()
