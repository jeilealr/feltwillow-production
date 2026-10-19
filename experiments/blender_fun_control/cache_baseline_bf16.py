#!/usr/bin/env python3
"""Create an isolated, verified storage cache of the baseline's normal bf16 cast.

No original cache entry is modified. CPU allocation only; never runs on login.
"""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import time

PROJECT=Path(__file__).resolve().parents[3]
REV='596658fd9ca6b7b71d5057529bbf319ecbc61d74'
SOURCE=PROJECT/'hf_cache/hub/models--Wan-AI--Wan2.2-I2V-A14B-Diffusers/snapshots'/REV
DEST=PROJECT/'models/video_control_baseline_bf16'/REV


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda:f.read(4*1024*1024),b''): h.update(data)
    return h.hexdigest()


def convert(relative):
    import torch
    from safetensors import safe_open
    from safetensors.torch import save_file
    src=SOURCE/relative; dst=DEST/relative
    started=time.time()
    proof=dst.with_name(dst.name+'.verified.json')
    if dst.exists() and proof.exists():
        previous=json.loads(proof.read_text())
        if previous['source_sha256']!=digest(src) or previous['cache_sha256']!=digest(dst):
            raise RuntimeError('Previously verified cache changed: '+str(relative))
        return previous
    with safe_open(src,framework='pt',device='cpu') as f:
        metadata=f.metadata()
        tensors={key:f.get_tensor(key).to(torch.bfloat16).contiguous() for key in f.keys()}
    temporary=dst.with_suffix('.partial')
    save_file(tensors,str(temporary),metadata=metadata)
    with safe_open(temporary,framework='pt',device='cpu') as check:
        if set(check.keys()) != set(tensors): raise RuntimeError('Key mismatch: '+str(relative))
        for key,value in tensors.items():
            if not torch.equal(check.get_tensor(key).reshape(-1).view(torch.uint8),value.reshape(-1).view(torch.uint8)): raise RuntimeError('Roundtrip mismatch: '+str(relative)+':'+key)
    temporary.replace(dst)
    row=dict(path=str(relative),source_sha256=digest(src),cache_sha256=digest(dst),
             verified_tensors=len(tensors),tensor_bytes=sum(t.numel()*t.element_size() for t in tensors.values()),
             source_bytes=src.stat().st_size,cache_bytes=dst.stat().st_size,seconds=time.time()-started,
             verification='Every saved tensor equals the in-memory normal torch.bfloat16 cast, bit for bit')
    proof.write_text(json.dumps(row,indent=2))
    print(json.dumps(row),flush=True)
    return row


def main():
    if not os.environ.get('SLURM_JOB_ID'): raise SystemExit('CPU conversion requires a SLURM allocation')
    import torch
    torch.set_num_threads(1)
    started=time.time()
    DEST.mkdir(parents=True,exist_ok=True)
    if (DEST/'conversion_receipt.json').exists():
        raise SystemExit('Cache already complete; no conversion needed')
    converted=[]; passthrough=[]
    for src in SOURCE.rglob('*'):
        relative=src.relative_to(SOURCE); dst=DEST/relative
        if src.is_dir(): dst.mkdir(exist_ok=True)
        elif src.suffix=='.safetensors' and relative.parts[0] in ('transformer','transformer_2'):
            dst.parent.mkdir(parents=True,exist_ok=True);converted.append(relative)
        elif src.suffix=='.safetensors':
            dst.parent.mkdir(parents=True,exist_ok=True);
            if not dst.exists(): dst.symlink_to(src.resolve())
            passthrough.append(str(relative))
        else:
            dst.parent.mkdir(parents=True,exist_ok=True);
            if not dst.exists(): shutil.copyfile(src,dst)
    rows=[]
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            ordered=sorted(converted)
            first_start=time.time()
            rows=list(pool.map(convert,ordered[:4]))
            first_seconds=time.time()-first_start
            estimate=(len(ordered)/4)*first_seconds
            print('CACHE_THROUGHPUT_ESTIMATE_SECONDS',estimate,flush=True)
            if os.environ.get('SLURM_JOB_PARTITION')=='debug' and estimate>600:
                raise RuntimeError('Projected conversion exceeds quick-test budget; preserve verified shards and resume on small')
            rows+=list(pool.map(convert,ordered[4:]))
        for component in ('transformer','transformer_2'):
            index=DEST/component/'diffusion_pytorch_model.safetensors.index.json'
            d=json.loads(index.read_text())
            d['metadata']['total_size']=sum(r['tensor_bytes'] for r in rows if r['path'].startswith(component+'/'))
            index.write_text(json.dumps(d,indent=2))
        receipt=dict(status='complete',origin='Wan-AI/Wan2.2-I2V-A14B-Diffusers',revision=REV,
            conversion='Exactly the existing baseline load dtype torch.bfloat16; VAE/text encoder unchanged',
            original_cache_modified=False,script_sha256=digest(Path(__file__)),files=rows,unchanged_symlinked_weights=passthrough,
            total_seconds=time.time()-started,job_id=os.environ['SLURM_JOB_ID'])
        (DEST/'conversion_receipt.json').write_text(json.dumps(receipt,indent=2))
    except BaseException:
        import traceback
        (DEST/'conversion_failure.json').write_text(json.dumps(dict(status='failed',error=traceback.format_exc()),indent=2))
        raise

if __name__=='__main__': main()
