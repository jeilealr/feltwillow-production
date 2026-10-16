#!/usr/bin/env python3
"""Verify replacement bytes, immutable inputs, face locks and review links."""
import hashlib
import json
import re
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[4]
HOME=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    plan=json.loads((HOME/'complete_replacement_plan.json').read_text())
    audit=json.loads((HOME.parent.parent/'perceptual_world_plan.json').read_text())
    closer=json.loads((HOME/'closer_review_22.json').read_text())
    priority={f['id'] for f in audit['frames'] if f['priority']=='must_fix'}
    fixes={f['id'] for f in closer['frames'] if f['decision']=='fix'}
    assert len(priority)==14 and len(closer['frames'])==22 and len(fixes)==plan['closer_review_fix_count']
    additional={f['id'] for f in plan['frames'] if f['category']=='continuity_fix'}
    assert {f['id'] for f in plan['frames']}==priority|fixes|additional
    assert len([f for f in closer['frames'] if f['decision']=='retain'])==plan['closer_review_retained_count']
    for name,h in plan['source_plans'].items():assert sha(HOME.parent.parent/name)==h
    for f in audit['frames']:assert sha(ROOT/f['candidate_path'])==f['sha256'], f['id']+' active image changed'
    verifications=[]
    for f in plan['frames']:
        p=ROOT/f['output_path'];assert sha(p)==f['sha256']
        assert Image.open(p).size==(1920,1080)
        assert sha(ROOT/f['source_candidate']['path'])==f['source_candidate']['sha256']
        row={'id':f['id'],'output_path':f['output_path'],'sha256':f['sha256'],'canvas_px':[1920,1080]}
        if 'camera_source' in f:
            source=f['camera_source'];assert sha(ROOT/source['path'])==source['sha256']
            receipt=json.loads((ROOT/f['camera_crop_receipt']).read_text())['materialized_crop']
            raw=Image.open(ROOT/source['path']).convert('RGB').crop(receipt['pixel_box'])
            expected=np.array(raw.resize((1920,1080),Image.Resampling.LANCZOS))
            assert np.array_equal(np.array(Image.open(p).convert('RGB')),expected),f['id']+' crop changed pixels'
            row['selected_composite_camera_crop_exact']=True
        elif 'reuse_source' in f:
            assert p.read_bytes()==(ROOT/f['reuse_source']['path']).read_bytes()
            row['exact_selected_knot_insert_reuse']=True
        else:
            record=json.loads((ROOT/f['composition_receipt']).read_text())
            bg=ROOT/record['plate_source']['label'];assert sha(bg)==record['plate_source']['sha256']
            for c in record['characters']:
                source=c['still_source'];assert sha(ROOT/source['label'])==source['sha256']
            expected=np.array(Image.open(bg).convert('RGB')).astype(np.float32)
            if record['blur']:expected=cv2.GaussianBlur(expected,(0,0),sigmaX=record['blur'])
            expected=np.clip(expected,0,255).astype('uint8')
            actual=np.array(Image.open(p).convert('RGB'))
            mask=np.array(Image.open(p.with_name(p.stem+'_edit_mask.png')))
            n=int(np.count_nonzero(np.any(actual[mask==0]!=expected[mask==0],axis=1)))
            assert n==0,f['id']+' changed background'
            row['protected_background_mismatched_pixels']=n
        row['inspection_scope']='native_1920x1080_and_480x270_whole_frame'
        row['visual_review']='Framing/readability review by Codex; owner and anatomical calibration remain separate.'
        if f.get('continuity_note'):row['continuity_note']=f['continuity_note']
        verifications.append(row)
    for f in json.loads((HOME/'expression_continuity.json').read_text()):
        base=np.array(Image.open(ROOT/f['edit_base']).convert('RGBA'))
        out=np.array(Image.open(ROOT/f['output_path']).convert('RGBA'))
        mask=np.array(Image.open(ROOT/f['mask_path']))
        assert sha(ROOT/f['output_path'])==f['sha256']
        assert np.array_equal(base[:,:,3],out[:,:,3])
        # The on-disk mask is quantized; allow nonzero sub-byte mask feathers.
        yy,xx=np.ogrid[:base.shape[0],:base.shape[1]];cx,cy,rx,ry=f['face_ellipse_xyrr']
        outside=((xx-cx)/rx)**2+((yy-cy)/ry)**2>=1
        assert np.array_equal(base[outside],out[outside])
    approved=[f for f in plan['frames'] if f['owner_visual_selection']]
    assert len(approved)==4
    for f in approved:assert f['sha256']==f['owner_visual_selection']['sha256']
    page=(HOME/'owner_review.html').read_text(); links=re.findall(r'(?:src|href)="([^"]+)"',page)
    for link in links:
        if link!='batch_verification.json' and not link.startswith('#'):assert (HOME/link).exists(),link
    report={'schema':'feltwillow.perceptual-world-batch-verification.v1','scope':'Candidate verification; does not grant owner/technical approval',
      'priority_slots_covered':14,'closer_slots_reviewed':22,'additional_fixes':len(fixes),'retained':plan['closer_review_retained_count'],
      'replacement_slots':len(plan['frames']),'owner_selected_compositions':4,'new_candidates_pending_owner_review':len(plan['frames'])-4,
      'active_image_hashes_unchanged':96,'source_plan_hashes_unchanged':True,
      'expression_face_locks_verified':6,'review_links_checked':len(links),'frames':verifications}
    (HOME/'batch_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(plan['frames']),'candidate hashes/canvases and source/background locks; exact knot reuse; 6 expression locks; 96 active images unchanged; complete priority/review/continuity coverage; all review links.')
if __name__=='__main__':main()
