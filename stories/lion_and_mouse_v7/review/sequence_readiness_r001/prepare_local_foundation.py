"""One authorized deterministic candidate; never changes selected files/ledgers."""
import json
import sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from production.sequence_plan import digest
from production.sequence_review import protected_pixels


def main():
    out=Path(__file__).resolve().parent/'local_fork_foundation_r001'
    if out.exists():raise SystemExit('Existing candidate operation: inspect it; never overwrite or repeat automatically')
    folder=ROOT/'stories/lion_and_mouse_v7'
    ledger=json.loads((folder/'scene_image_selection_s01_s05.json').read_text())
    selected={r['image_id']:r for r in ledger['images'] if r['image_id']}
    base,target=selected['S03-L006-B01-I02'],selected['S03-L001-B01-I02']
    for row in (base,target):
        if digest(ROOT/row['path'])!=row['sha256']:raise ValueError('selected source changed')
    a=Image.open(ROOT/base['path']).convert('RGB');b=Image.open(ROOT/target['path']).convert('RGB')
    if a.size!=b.size:raise ValueError('same native projection/canvas required')
    # Face only: ears, skull silhouette, body, root, feet and all geography
    # remain the exact base. No translation, independent scaling or redraw.
    box=[636,330,860,518];x0,y0,x1,y1=box
    yy,xx=np.mgrid[:a.height,:a.width]
    radius=np.sqrt(((xx-(x0+x1)/2)/((x1-x0)/2))**2+((yy-(y0+y1)/2)/((y1-y0)/2))**2)
    alpha=np.round(np.clip((1-radius)/0.12,0,1)*255).astype(np.uint8)
    out.mkdir()
    mask=out/'face_alpha.png';Image.fromarray(alpha).save(mask)
    candidate=ROOT/'character/characters/lion_and_mouse_v7/interactions/scene_compositions/S03-L001-B01-I02_end_homeward_distance_r004_candidate.png'
    if candidate.exists():raise SystemExit('Candidate revision already exists; choose a new revision')
    Image.composite(b,a,Image.fromarray(alpha)).save(candidate)
    check=protected_pixels(ROOT/base['path'],candidate,mask)
    if check['changed_protected_pixels']!=0:raise AssertionError('protected base pixels changed')
    plan=json.loads((folder/'audio_visual_plan.json').read_text());line=next(l for l in plan['lines'] if l['line_id']=='S03-L001')
    receipt=dict(operation_id='fork-l001-local-face-foundation-r004',method='deterministic Pillow composite; no model/provider call',image_id=target['image_id'],path=str(candidate.relative_to(ROOT)),sha256=digest(candidate),canvas=list(a.size),inputs=[dict(role='unchanged scene/camera/body/root',path=base['path'],sha256=base['sha256']),dict(role='selected local facial attention only',path=target['path'],sha256=target['sha256'])],mask=dict(path=str(mask.relative_to(ROOT)),sha256=digest(mask),ellipse_xyxy=box,soft_interior_fraction=0.12,policy='zero outside ellipse; feathering only inside'),transforms='none; identical native pixel coordinates',audio=line['audio'],protected_pixels=check,provider_calls=0,gpu_jobs=0,retries=0,owner_selection='pending',technical_review='pending native/fitted face/lighting/integration review; exact preservation alone is insufficient',source_selections_unchanged=True)
    candidate.with_suffix('.json').write_text(json.dumps(receipt,indent=2)+'\n')
    (out/'OPERATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(path=str(candidate),sha256=receipt['sha256'],changed_protected_pixels=check['changed_protected_pixels']),indent=2))


if __name__=='__main__':main()
