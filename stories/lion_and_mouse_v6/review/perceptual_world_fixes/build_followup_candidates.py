#!/usr/bin/env python3
"""Build the full Agent A replacement proposal without altering active approvals.

Uses ImageGen layers with the existing compositor. All camera cuts, local
support targets, source hashes, masks and review slots are explicit.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from production.keyframe import compose
from production.materialize_plate_crop import materialize

HOME = Path(__file__).resolve().parent
ASSETS = ROOT / 'character/characters/lion_and_mouse_v6/interactions/keyframes/.review/perceptual_world_fixes'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def relative(p):
    return str(p.relative_to(ROOT))


def freeze_expression(base_path, donor_path, output, shift, ellipse):
    """Constrain an ImageGen expression to the clear face; alpha/body stay exact."""
    base = np.asarray(Image.open(base_path).convert('RGBA')).copy()
    donor = np.asarray(Image.open(donor_path).convert('RGBA'))
    if donor.shape != base.shape:
        raise ValueError('expression donor canvas must match approved base')
    matrix = np.array([[1., 0., shift[0]], [0., 1., shift[1]]], dtype=np.float32)
    aligned = cv2.warpAffine(donor, matrix, (base.shape[1], base.shape[0]))
    yy, xx = np.ogrid[:base.shape[0], :base.shape[1]]
    cx, cy, rx, ry = ellipse
    distance = np.sqrt(((xx-cx)/rx)**2 + ((yy-cy)/ry)**2)
    mask = np.clip((1.0-distance)/.12, 0, 1)
    mask *= ((base[:,:,3] > 220) & (aligned[:,:,3] > 220))
    out = base.copy()
    out[:,:,:3] = np.rint(base[:,:,:3]*(1-mask[:,:,None]) + aligned[:,:,:3]*mask[:,:,None]).astype('uint8')
    Image.fromarray(out).save(output)
    assert np.array_equal(base[:,:,3],out[:,:,3])
    assert np.array_equal(base[mask==0],out[mask==0])
    mask_path=output.with_name(output.stem+'_face_mask.png')
    Image.fromarray(np.rint(mask*255).astype('uint8')).save(mask_path)
    receipt = {'edit_base': relative(base_path), 'edit_base_sha256': digest(base_path),
               'ImageGen_expression_donor': relative(donor_path), 'donor_sha256': digest(donor_path),
               'alignment_translation_xy': shift, 'face_ellipse_xyrr': ellipse,
               'mask_path': relative(mask_path), 'mask_sha256': digest(mask_path),
               'output_path': relative(output), 'sha256': digest(output),
               'outside_face_mismatched_pixels': 0, 'alpha_silhouette_unchanged': True}
    output.with_suffix('.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt


def build():
    first = json.loads((HOME/'candidate_manifest.json').read_text())
    follow = json.loads((HOME/'followup_layers.json').read_text())
    baseline = {l['id']: ROOT/l['output_path'] for l in first['layers']}
    layerpaths = dict(baseline)
    for l in follow['layers']:
        p=ROOT/l['output_path']
        if digest(p)!=l['sha256']: raise ValueError('stale layer '+l['id'])
        layerpaths[l['id']]=p
    face_receipts=[]
    # Keep ears/head outer contour, shoulders/chest and alpha EXACT through expressions.
    for ident,shift in [('milo_apology_upper',[-10,100]),('milo_fear_upper',[-5,28]),
                        ('milo_kind_upper',[0,0]),('milo_playful_upper',[-4,106])]:
        out=ASSETS/'layers'/(ident+'_face_locked.png')
        face_receipts.append(freeze_expression(baseline['milo_explain_upper'],layerpaths[ident],out,shift,[625,830,235,222]))
        layerpaths[ident]=out
    for ident,base,ellipse in [('milo_smile','milo_friend',[625,520,245,205]),
                                ('leo_smile_rest','leo_rest',[1100,450,235,200])]:
        out=ASSETS/'layers'/(ident+'_face_locked.png')
        face_receipts.append(freeze_expression(baseline[base],layerpaths[ident],out,[0,0],ellipse))
        layerpaths[ident]=out
    (HOME/'expression_continuity.json').write_text(json.dumps(face_receipts,indent=2)+'\n')
    # Each tuple: ID, normalized crop, isolated layer placement x/y/pose-height/flip.
    # These are proposed cuts, not a continuous camera move or actor growth.
    specifications=[
      ('s04_p02',[.30,.30,.49,.49],[('milo_duck',.28,.95,.18,False)]),
      ('s04_p03',[.68,.595,.25,.25],[('milo_run',.24,.70,.38,False)]),
      ('s04_p04',[.65,.565,.25,.25],[('milo_run',.50,.70,.36,False)]),
      ('s06x_p01',[.27,.43,1/2.25,1/2.25],[('leo_rising',.45,.8325,.79,False),('milo_scramble',.79,.9225,.25,False)]),
      ('s07_p02',[.62,.72,.08,.08],[('milo_apology_upper',.5,1.07,1.,True)]),
      ('s09_p01',[.555,.565,.25,.25],[('milo_careful',.50,.70,.36,False)]),
      ('s15_p06',[.25,.43,.5,.5],[('leo_released_net',.50,.87,.75,False),('milo_friend',.76,.91,.245,True)]),
      ('s16_p01',[.245,.405,1/2.1,1/2.1],[('leo_rest',.4305,.8085,.63,False),('milo_friend',.7665,.8925,.2415,True)]),
      ('s16x_p01',[.245,.405,1/2.1,1/2.1],[('leo_rest',.4305,.8085,.63,False),('milo_friend',.7665,.8925,.2415,True)]),
      ('s16x_p03',[.245,.405,1/2.1,1/2.1],[('leo_rest',.4305,.8085,.63,False),('milo_friend',.7665,.8925,.2415,True)]),
      ('s06_p03',[.62,.72,.08,.08],[('milo_fear_upper',.5,1.07,1.,True)]),
      ('s07_p04',[.62,.72,.08,.08],[('milo_kind_upper',.5,1.07,1.,True)]),
      ('s08_p01',[.62,.72,.08,.08],[('milo_fear_upper',.5,1.07,1.,True)]),
      ('s12_p03',[.405,.62,.25,.25],[('milo_run',.50,.68,.40,False)]),
      ('s13_p06',[.28,.72,.08,.08],[('milo_playful_upper',.5,1.07,1.,False)]),
      ('s15_p03',[.64,.72,.08,.08],[('milo_kind_upper',.5,1.07,1.,True)]),
      ('s15_p04',[.64,.72,.08,.08],[('milo_kind_upper',.5,1.07,1.,True)]),
      ('s16_p04',[.245,.405,1/2.1,1/2.1],[('leo_smile_rest',.4305,.8085,.63,False),('milo_smile',.7665,.8925,.2415,True)]),
    ]
    audit=json.loads((HOME.parent.parent/'perceptual_world_plan.json').read_text())
    initial=json.loads((HOME.parent.parent/'keyframe_plan.json').read_text())
    staging=json.loads((HOME.parent.parent/'staging_plan.json').read_text())
    active={f['id']:f for f in initial['images']};staged={f['id']:f for f in staging['frames']}
    priority={f['id'] for f in audit['frames'] if f['priority']=='must_fix'}
    results=[]
    for old in first['frames']:
        results.append({'id':old['id'],'category':'priority','source_candidate':old['source_candidate'],
          'output_path':old['output_path'],'sha256':old['sha256'],'canvas_px':[1920,1080],
          'status':'owner_selected_visual_composition_pending_technical_validation',
          'owner_visual_selection':old['owner_visual_selection'],
          'crop_rect_on_plate':old['proposed_camera']['crop_rect_on_plate'],
          'composition_receipt':old['final_composition_record'],
          'existing_approval_scope_preserved':True})
    layers_by_id={l['id']:l for l in follow['layers']}
    for fid,crop,entries in specifications:
        source=active[fid];frame=staged[fid]
        rev=int(Path(source['candidate_path']).stem.split('_r')[-1].split('_')[0])+1
        output=ASSETS/(f'{fid}_r{rev:02d}_candidate.png')
        crop_path=HOME/(fid+'_followup_plate_crop.png')
        crop_receipt=materialize(ROOT/frame['plate'],crop,crop_path)
        delivery=HOME/(fid+'_followup_background.png')
        Image.open(crop_path).convert('RGB').resize((1920,1080),Image.Resampling.LANCZOS).save(delivery)
        portrait=len(entries)==1 and entries[0][0].endswith('_upper')
        blur=10. if portrait else 0.
        chars=[]
        for ident,x,y,height,flip in entries:
            actor='leo' if ident.startswith('leo') else 'milo'
            if 'upper' in ident:contacts=[]
            elif ident=='leo_rising':
                contacts=[{'u':u,'v':v,'rx':.07,'ry':.009,'blur':.006} for u,v in [(.23,.946),(.46,.925),(.70,.991),(.92,.965)]]
            elif ident.startswith('leo'):
                contacts=[{'u':.55,'v':.96,'rx':.40,'ry':.03,'blur':.02}]
            elif ident=='milo_run':contacts=[{'u':.68,'v':.998,'rx':.16,'ry':.025,'blur':.018}]
            elif ident=='milo_duck':contacts=[{'u':.65,'v':.998,'rx':.14,'ry':.025,'blur':.018}]
            elif ident=='milo_scramble':contacts=[{'u':.39,'v':.98,'rx':.14,'ry':.025,'blur':.018}]
            elif ident=='milo_careful':contacts=[{'u':.40,'v':.985,'rx':.12,'ry':.025,'blur':.018}]
            else:contacts=[{'u':.40,'v':.985},{'u':.79,'v':.975}]
            chars.append({'actor':actor,'pose_layer_id':ident,'still':str(layerpaths[ident]),'x':x,'y':y,'h':height,
              'flip':flip,'light':.12,'shadow':.62,'contact_shadows':contacts})
        authority={'status':'new_candidate_not_owner_approved','source_plate':frame['plate'],
           'source_plate_sha256':digest(ROOT/frame['plate']),'materialized_crop':crop_receipt,
           'camera_join':'cut','framing':'upper_body_speaker_or_reaction' if portrait else 'local_action_or_shared',
           'scope':'Framing replacement proposal; no standing-equivalent scale approval inferred from visible pose boxes.'}
        record=compose(delivery,chars,output,blur=blur,authority=authority,write_edit_mask=True)
        actual=np.array(Image.open(output).convert('RGB'));background=np.array(Image.open(delivery).convert('RGB')).astype(np.float32)
        if blur:background=cv2.GaussianBlur(background,(0,0),sigmaX=blur)
        mask=np.array(Image.open(output.with_name(output.stem+'_edit_mask.png')))
        expected=np.clip(background,0,255).astype('uint8')
        mismatch=int(np.count_nonzero(np.any(actual[mask==0]!=expected[mask==0],axis=1)))
        if mismatch:raise RuntimeError(fid+' changed protected plate pixels')
        contacts={c['actor']:[round(crop[0]+c['x']*crop[2],5),round(crop[1]+c['y']*crop[3],5)] for c in chars}
        row={'id':fid,'category':'priority' if fid in priority else 'closer_review_fix',
          'source_candidate':{'path':source['candidate_path'],'sha256':source['sha256']},
          'output_path':relative(output),'sha256':digest(output),'canvas_px':[1920,1080],
          'status':'replacement_candidate_pending_owner_review','owner_visual_selection':None,
          'crop_rect_on_plate':crop,'plate':frame['plate'],'materialized_crop_receipt':crop_receipt,
          'composition_receipt':relative(output.with_suffix('.json')),'blur_sigma_px':blur,
          'protected_background_mismatched_pixels':mismatch,
          'visible_actor_boxes_xywh':{c['actor']:c['box'] for c in record['characters']},
          'proposed_support_on_plate':contacts,
          'pose_box_heights':{c['actor']:c['h'] for c in chars},
          'camera_join':'cut','cast_in_new_view':[c['actor'] for c in chars],
          'action':frame['action'],'normalization':'Exact crop then LANCZOS to 1920x1080; no global grading',
          'generation':'built-in ImageGen layers + existing production.keyframe.compose',
          'technical_approval':None}
        if fid=='s04_p02':
            row['context_note']='Contextual branch passage: retain the registered overhead branch with a 2.04x crop and proportionately magnified crouch. Adjacent p01/p03 supply tighter action views; no subtle facial beat is assigned here.'
        if fid in ('s16_p01','s16x_p01','s16x_p03'):
            row['hold_note']='Intentional shared closing hold in the owner-selected composition; these narration slots do not require invented pose changes.'
        results.append(row)
    # Reuse the already owner-selected causal detail image; never redesign the net.
    fid='s14_p01';source=active[fid];insert=active['s14_p02'];out=ASSETS/'s14_p01_r07_candidate.png'
    shutil.copy2(ROOT/insert['candidate_path'],out)
    results.append({'id':fid,'category':'closer_review_fix','source_candidate':{'path':source['candidate_path'],'sha256':source['sha256']},
      'output_path':relative(out),'sha256':digest(out),'canvas_px':[1920,1080],
      'status':'replacement_candidate_pending_owner_review','owner_visual_selection':None,
      'reuse_source':{'id':'s14_p02','path':insert['candidate_path'],'sha256':insert['sha256']},
      'generation':'Exact reuse of existing owner-selected knot-action insert; no new image generation or pixel edits',
      'view':'causal_knot_insert','camera_join':'cut',
      'reason':'Begin gnawing on the same selected knot image held into p02, preserving mouth/paw contact and exact net topology. The wider p03 returns to geography.',
      'technical_approval':None})
    assert len(results)==23 and len({r['id'] for r in results})==23
    assert priority <= {r['id'] for r in results}
    final={'schema':'feltwillow.perceptual-world-complete-replacements.v1','story':'lion_and_mouse_v6',
       'status':'all_14_priority_and_9_closer_fixes_generated',
       'owner_continuation_authorization':first['owner_continuation_authorization'],
       'source_plans':{n:digest(HOME.parent.parent/n) for n in ['keyframe_plan.json','staging_plan.json']},
       'priority_count':14,'closer_review_count':22,'closer_review_fix_count':9,'closer_review_retained_count':13,
       'owner_approved_compositions':4,'new_candidates_pending_owner_review':19,
       'active_production_plans_modified':False,'frames':sorted(results,key=lambda x:x['id'])}
    (HOME/'complete_replacement_plan.json').write_text(json.dumps(final,indent=2)+'\n')
    print('23 corrected slots ready: 14 priority, 9 additional. 13 reviewed originals retained.')


if __name__=='__main__':build()
