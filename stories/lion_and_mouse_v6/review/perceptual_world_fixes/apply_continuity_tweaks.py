#!/usr/bin/env python3
"""Build the owner's requested scene-continuity revisions using native layers."""
import hashlib
import json
import re
import sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from production.keyframe import compose
from production.materialize_plate_crop import materialize
HOME=Path(__file__).resolve().parent
ASSETS=ROOT/'character/characters/lion_and_mouse_v6/interactions/keyframes/.review/perceptual_world_fixes'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return str(p.relative_to(ROOT))
def load(p):return json.loads(p.read_text())
def head_band_per_h(path):
    a=np.asarray(Image.open(path).convert('RGBA'))[:,:,3]>127
    yy,xx=np.nonzero(a);a=a[yy.min():yy.max()+1,xx.min():xx.max()+1]
    yy,xx=np.nonzero(a[:int(a.shape[0]*.44)])
    return 1080*(int(xx.max()-xx.min()+1))/a.shape[0]
def main():
    snapshot=HOME/'continuity_input_plan.json'
    if not snapshot.exists():snapshot.write_text((HOME/'complete_replacement_plan.json').read_text())
    plan=load(snapshot); old={f['id']:f for f in plan['frames']}
    active={f['id']:f for f in load(HOME.parent.parent/'keyframe_plan.json')['images']}
    staged={f['id']:f for f in load(HOME.parent.parent/'staging_plan.json')['frames']}
    layers={f['id']:ROOT/f['output_path'] for f in load(HOME/'candidate_manifest.json')['layers']}
    layers.update({f['id']:ROOT/f['output_path'] for f in load(HOME/'followup_layers.json')['layers']})
    new=load(HOME/'continuity_layers.json')
    for f in new['layers']:
        p=ROOT/f['output_path'];assert sha(p)==f['sha256'];assert Image.open(p).mode=='RGBA'
        assert Image.open(p).getchannel('A').getextrema()[0]==0
        layers[f['id']]=p
    for name in ['milo_kind_upper','milo_playful_upper']:
        layers[name]=ASSETS/'layers'/(name+'_face_locked.png')
    # Match the approved scramble's upper-head band across standing/run poses.
    early_head=.25*head_band_per_h(layers['milo_scramble'])
    friend_h=early_head/head_band_per_h(layers['milo_friend'])
    run_h=early_head/head_band_per_h(layers['milo_run'])
    duck_h=.4*head_band_per_h(layers['milo_run'])/head_band_per_h(layers['milo_duck'])
    closing_head=.2415*head_band_per_h(layers['milo_friend'])
    restored_h=closing_head/head_band_per_h(layers['milo_original_closing'])
    early_crop=[.27,.43,1/2.25,1/2.25]
    specs=[('s04_p03',[.68,.595,.25,.25],[('milo_run',.24,.70,.4,False)],'Match approved p01 running head size across the same foreground lane.'),
           ('s04_p04',[.65,.565,.25,.25],[('milo_run',.50,.70,.4,False)],'Match approved p01/p03 running head size while continuing right past the stump.'),
           ('s04_p02',[.295,.595,.25,.25],[('milo_duck',.5,.70,duck_h,False)],'Match p03 head scale and local-ground magnification; tighter crop requested by owner.')]
    for fid in ['s06_p02','s07_p01','s08_p04']:
        specs.append((fid,early_crop,[('leo_rising',.45,.8325,.79,False),('milo_friend',.79,.9225,friend_h,True)],'Same shared camera/depth and head scale as s06_p01/x01; Leo remains on four paws, with nearest paw beside Milo and no contact.'))
    specs.append(('s08_p06',early_crop,[('leo_rest',.45,.8325,.69,False),('milo_run',.84,.9225,run_h,False)],'Open-path departure at unchanged head scale; do not revert to the tiny old wide.'))
    # The released Leo/net group is reflected as a layer, never the forest plate.
    shared15=[('leo_released_net',.54,.87,.75,True),('milo_friend',.22,.91,.245,False)]
    for fid in ['s15_p01','s15_p02','s15_p06']:
        specs.append((fid,[.25,.43,.5,.5],shared15,'Scene13–15 axis: Milo LEFT / Leo RIGHT; shared reaction hold, collapsed net remains on the ground.'))
    for fid in ['s15_p03','s15_p04','s15x_p02','s15x_p04','s15x_p06']:
        pose='milo_playful_upper' if fid=='s15x_p02' else 'milo_kind_upper'
        specs.append((fid,[.28,.72,.08,.08],[(pose,.38,1.07,1.,False)],'Milo portrait on LEFT looking RIGHT to offscreen Leo; common upper-body scale and camera.'))
    for fid in ['s15_p05','s15x_p01','s15x_p03','s15x_p05']:
        specs.append((fid,[.62,.34,.22,.22],[('leo_left_portrait',.62,1.07,1.,False)],'Leo portrait on RIGHT looking LEFT toward offscreen Milo; same selected upper-body authority.'))
    specs.append(('s16_p04',[.245,.405,1/2.1,1/2.1],[('leo_original_closing',.4305,.8085,.63,False),('milo_original_closing',.7665,.8925,restored_h,False)],'Restore original open-eyed expressions, keeping the corrected shared crop and matched Milo head scale.'))
    specs.append(('s16x_p02',[.245,.405,1/2.1,1/2.1],[('leo_rest',.4305,.8085,.63,False),('milo_friend',.7665,.8925,.2415,True)],'Exact shared closing composition and actor sizes from x01/x03; narration hold.'))
    updates=[]
    for fid,crop,entries,reason in specs:
        previous=old.get(fid);source=active[fid]
        stem=Path(previous['output_path'] if previous else source['candidate_path']).stem
        rev=int(re.search(r'_r(\d+)_',stem).group(1))+1
        output=ASSETS/(fid+'_r%02d_candidate.png'%rev)
        raw=HOME/(fid+'_continuity_plate_crop.png'); material=materialize(ROOT/staged[fid]['plate'],crop,raw)
        background=HOME/(fid+'_continuity_background.png')
        Image.open(raw).convert('RGB').resize((1920,1080),Image.Resampling.LANCZOS).save(background)
        portrait=len(entries)==1 and ('upper' in entries[0][0] or 'portrait' in entries[0][0]);blur=10. if portrait else 0.
        chars=[];heads={}
        for ident,x,y,h,flip in entries:
            actor='leo' if ident.startswith('leo') else 'milo'
            if portrait:contacts=[]
            elif ident=='leo_rising':contacts=[{'u':u,'v':v,'rx':.07,'ry':.009,'blur':.006} for u,v in [(.23,.946),(.46,.925),(.70,.991),(.92,.965)]]
            elif actor=='leo':contacts=[{'u':.55,'v':.97,'rx':.4,'ry':.025,'blur':.015}]
            elif ident in ['milo_run','milo_duck']:contacts=[{'u':.67,'v':.998,'rx':.14,'ry':.018,'blur':.01}]
            else:contacts=[{'u':.40,'v':.99,'rx':.09,'ry':.012,'blur':.008},{'u':.79,'v':.985,'rx':.09,'ry':.012,'blur':.008}]
            chars.append({'actor':actor,'pose_layer_id':ident,'still':str(layers[ident]),'x':x,'y':y,'h':h,'flip':flip,'light':.12,'shadow':.62,'contact_shadows':contacts})
            if actor=='milo' and not portrait:heads[actor]=round(h*head_band_per_h(layers[ident]),3)
        if fid=='s16x_p02':
            # Use the exact selected family recipe, including contact-shadow settings.
            anchor=load(ROOT/old['s16x_p01']['composition_receipt'])
            chars=[dict({k:v for k,v in c.items() if k not in ['still_source','box','edit_region','scale']},still=str(ROOT/c['still_source']['label'])) for c in anchor['characters']]
        receipt_path=output.with_suffix('.json')
        cached=load(receipt_path) if output.exists() and receipt_path.exists() else None
        keys=['actor','pose_layer_id','x','y','h','flip','light','shadow','contact_shadows']
        reusable=cached and cached['blur']==blur and cached['authority']['materialized_crop']['crop_rect_on_plate']==crop and len(cached['characters'])==len(chars)
        if reusable:
            reusable=all(all(a.get(k)==b.get(k) for k in keys) and a['still_source']['sha256']==sha(Path(b['still'])) for a,b in zip(cached['characters'],chars))
        if reusable:record=cached
        else:record=compose(background,chars,output,blur=blur,authority={'status':'owner_requested_continuity_revision_pending_visual_selection','source_plate':staged[fid]['plate'],'source_plate_sha256':sha(ROOT/staged[fid]['plate']),'materialized_crop':material,'camera_join':'cut','continuity_reason':reason,'physical_anatomy_approval':None},write_edit_mask=True)
        row={'id':fid,'category':previous['category'] if previous else ('closer_review_fix' if fid in {f['id'] for f in load(HOME/'closer_review_22.json')['frames']} else 'continuity_fix'),
          'source_candidate':{'path':source['candidate_path'],'sha256':source['sha256']},'output_path':rel(output),'sha256':sha(output),'canvas_px':[1920,1080],
          'status':'replacement_candidate_pending_owner_review','owner_visual_selection':None,'composition_receipt':rel(output.with_suffix('.json')),'crop_rect_on_plate':crop,
          'plate':staged[fid]['plate'],'blur_sigma_px':blur,'camera_join':'cut','cast_in_new_view':[c['actor'] for c in chars],
          'visible_actor_boxes_xywh':{c['actor']:c['box'] for c in record['characters']},'pose_box_heights':{c['actor']:c['h'] for c in chars},
          'continuity_note':reason,'continuity_revision':True,'head_band_width_px':heads,'technical_approval':None,
          'generation':'Existing native compositor and ImageGen RGBA layers; registered plate is never mirrored.'}
        if previous:row['supersedes_candidate']={'path':previous['output_path'],'sha256':previous['sha256']}
        old[fid]=row;updates.append(row)
    closer=load(HOME/'closer_review_22.json')
    for f in closer['frames']:
        if f['id'] in {r['id'] for r in updates}:
            if f['decision']=='retain':f['previous_decision']='retain'
            f['decision']='fix';f['reason']='Owner continuity correction: '+old[f['id']]['continuity_note']
            f['owner_direction']='Keep Milo size consistent across adjacent shared views; Scene15 Milo left / Leo right.'
    (HOME/'closer_review_22.json').write_text(json.dumps(closer,indent=2)+'\n')
    plan['frames']=sorted(old.values(),key=lambda x:x['id']);plan['status']='owner_continuity_tweaks_applied_pending_review'
    plan['replacement_count']=len(old);plan['closer_review_fix_count']=sum(f['decision']=='fix' for f in closer['frames']);plan['closer_review_retained_count']=sum(f['decision']=='retain' for f in closer['frames'])
    plan['new_candidates_pending_owner_review']=len(old)-4
    plan['continuity_request']='Owner requested larger s04_p02, consistent Milo size across Scenes6–8 and16, Scene15 Milo left / Leo right, original s16_p04 expressions; s12_p04 remains exception.'
    plan['continuity_revision_ids']=[r['id'] for r in updates]
    (HOME/'complete_replacement_plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    report={'schema':'feltwillow.perceptual-world-continuity-revision.v1','updated_slots':len(updates),'frames':updates,
      'scale_method':'Upper-head silhouette band (upper 44% of trimmed alpha box) is a repeatable screen-size proxy checked visually; not neutral-anatomy calibration.',
      'early_shared_target_head_band_width_px':round(early_head,3),'closing_shared_target_head_band_width_px':round(closing_head,3),
      'scene15_axis':{'milo':'left, looking right','leo':'right, looking left'},'unchanged_owner_exception':'s12_p04',
      'original_four_selection_hashes_unchanged':True,'active_production_plans_modified':False}
    (HOME/'continuity_tweaks.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Built',len(updates),'continuity tweaks;',len(old),'total candidate slots;',plan['closer_review_retained_count'],'retained closer-review originals.')
if __name__=='__main__':main()
