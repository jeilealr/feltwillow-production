#!/usr/bin/env python3
"""Final six owner-requested reference-pose and shared-world corrections."""
import hashlib
import json
import re
import sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from production.keyframe import compose
from production.materialize_plate_crop import materialize
HOME=Path(__file__).resolve().parent
ASSETS=ROOT/'character/characters/lion_and_mouse_v6/interactions/keyframes/.review/perceptual_world_fixes'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return str(p.relative_to(ROOT))
def head_per_h(path,window=None):
    a=np.array(Image.open(path).convert('RGBA'))[:,:,3]>127;y,x=np.nonzero(a);height=y.max()-y.min()+1
    if window:
        x0,y0,x1,y1=window;roi=a[y0:y1,x0:x1]
    else:
        roi=a[y.min():y.min()+int(height*.35),x.min():x.max()+1]
    y,x=np.nonzero(roi);return 1080*(x.max()-x.min()+1)/height

def main():
    snapshot=HOME/'final_reference_input_plan.json'
    if not snapshot.exists():snapshot.write_text((HOME/'complete_replacement_plan.json').read_text())
    plan=load(snapshot);frames={f['id']:f for f in plan['frames']}
    for f in frames.values():
        if f.get('continuity_revision'):f['earlier_continuity_revision']=True;f['continuity_revision']=False
    active={f['id']:f for f in load(HOME.parent.parent/'keyframe_plan.json')['images']}
    staged={f['id']:f for f in load(HOME.parent.parent/'staging_plan.json')['frames']}
    layers={f['id']:ROOT/f['output_path'] for f in load(HOME/'final_pose_layers.json')['layers']}
    for f in load(HOME/'final_pose_layers.json')['layers']:
        assert sha(ROOT/f['output_path'])==f['sha256'];assert Image.open(ROOT/f['output_path']).getchannel('A').getextrema()[0]==0
    base=ASSETS/'layers';layers['leo_rising']=base/'leo_rising_r01.png';layers['milo_friend']=base/'milo_friend_r01.png'
    target_shared=.25*head_per_h(base/'milo_scramble_r01.png')
    target_action=.4*head_per_h(base/'milo_run_r01.png')
    crouch_window=[600,120,1536,470]
    crouch_h=target_action/head_per_h(layers['milo_atlas_crouch'],crouch_window)
    walk_h=target_shared/head_per_h(layers['milo_atlas_walk'])
    friend_h=target_shared/head_per_h(layers['milo_friend'])
    ids=['s04_p02','s08_p06','s13_p01','s13_p03','s14_p03','s14_p06'];updates=[]
    for fid in ids:
        previous=frames.get(fid);selected=active[fid]
        stem=Path(previous['output_path'] if previous else selected['candidate_path']).stem
        rev=int(re.search(r'_r(\d+)_',stem).group(1))+1;out=ASSETS/(fid+'_r%02d_candidate.png'%rev)
        row={'id':fid,'category':previous['category'] if previous else 'closer_review_fix','source_candidate':{'path':selected['candidate_path'],'sha256':selected['sha256']},'output_path':rel(out),'canvas_px':[1920,1080],'owner_visual_selection':None,'status':'replacement_candidate_pending_owner_review','technical_approval':None,'final_reference_revision':True,'continuity_revision':True,'camera_join':'cut'}
        if previous:row['supersedes_candidate']={'path':previous['output_path'],'sha256':previous['sha256']}
        if fid in ['s13_p01','s13_p03','s14_p03']:
            source=active['s13_p03'] if fid.startswith('s13_') else selected
            source_path=ROOT/source['candidate_path'];crop=[.12,.20,.78,.78]
            raw=HOME/(fid+'_final_selected_crop.png');receipt=materialize(source_path,crop,raw)
            Image.open(raw).convert('RGB').resize((1920,1080),Image.Resampling.LANCZOS).save(out)
            camera_receipt={'method':'uniform_camera_crop_of_selected_composite','source_path':source['candidate_path'],'source_sha256':sha(source_path),'materialized_crop':receipt,'delivery_resampling':'LANCZOS 1920x1080','scope':'Shared medium view: both faces, ground support and active closure loop remain; rear net/tail may extend beyond the right frame edge. No independent actor resizing or generated rope pixels.'}
            out.with_suffix('.json').write_text(json.dumps(camera_receipt,indent=2)+'\n')
            row.update({'camera_source':{'path':source['candidate_path'],'sha256':sha(source_path)},'camera_crop_receipt':rel(out.with_suffix('.json')),'crop_rect_on_selected_image':crop,'crop_rect_on_plate':None,'generation':'Uniform crop of selected composite; no generative edits','continuity_note':'Closer shared net-action view, magnifying actors and location together. Preserve existing mesh, mouth-to-knot contact and Milo LEFT / Leo RIGHT.'})
            if fid=='s13_p01':row['hold_note']='Use the selected p03 approach view as the compact arrival hold; p02 supplies dedicated dialogue coverage.'
        else:
            if fid=='s04_p02':
                crop=[.295,.595,.25,.25];entries=[('milo_atlas_crouch',.5,.70,crouch_h,False)]
                reason='Use atlas row3/column3 Crouch, at natural aspect ratio and matched ear span; no generated running crouch or anisotropic squash.'
            elif fid=='s08_p06':
                crop=[.27,.43,1/2.25,1/2.25];entries=[('leo_rising',.45,.8325,.79,False),('milo_atlas_walk',.84,.9225,walk_h,False)]
                reason='Keep s07_p01 standing Leo and shared camera; atlas Walk Right lets Milo depart with matched head size.'
            else:
                crop=[.25,.43,.5,.5];entries=[('leo_release_selected',.56,.86,.74,False),('milo_friend',.11,.91,friend_h,False)]
                reason='Compact exit view with Milo LEFT / Leo RIGHT, selected cautious release pose and trailing net; matched Milo head size, no new anatomy.'
            raw=HOME/(fid+'_final_plate_crop.png');receipt=materialize(ROOT/staged[fid]['plate'],crop,raw)
            background=HOME/(fid+'_final_background.png');Image.open(raw).convert('RGB').resize((1920,1080),Image.Resampling.LANCZOS).save(background)
            chars=[]
            for ident,x,y,h,flip in entries:
                actor='leo' if ident.startswith('leo') else 'milo'
                if ident=='milo_atlas_crouch':contacts=[{'u':u,'v':v,'rx':.07,'ry':.013,'blur':.008} for u,v in [(.14,.95),(.44,.93),(.59,.985),(.84,.96)]]
                elif ident=='leo_rising':contacts=[{'u':u,'v':v,'rx':.07,'ry':.009,'blur':.006} for u,v in [(.23,.946),(.46,.925),(.70,.991),(.92,.965)]]
                elif actor=='leo':contacts=[{'u':.35,'v':.98,'rx':.27,'ry':.018,'blur':.012}]
                elif ident=='milo_atlas_walk':contacts=[{'u':.43,'v':.995,'rx':.10,'ry':.015,'blur':.008}]
                else:contacts=[{'u':.40,'v':.985},{'u':.79,'v':.975}]
                c={'actor':actor,'pose_layer_id':ident,'still':str(layers[ident]),'x':x,'y':y,'h':h,'flip':flip,'light':.12,'shadow':.62,'contact_shadows':contacts}
                if ident=='milo_atlas_crouch':c['head_measurement_window_px']=crouch_window
                chars.append(c)
            record=compose(background,chars,out,authority={'status':'owner_requested_final_reference_revision_pending_selection','source_plate':staged[fid]['plate'],'source_plate_sha256':sha(ROOT/staged[fid]['plate']),'materialized_crop':receipt,'camera_join':'cut','continuity_reason':reason,'anatomical_calibration':None},write_edit_mask=True)
            row.update({'composition_receipt':rel(out.with_suffix('.json')),'crop_rect_on_plate':crop,'continuity_note':reason,'plate':staged[fid]['plate'],'cast_in_new_view':[c['actor'] for c in chars],'pose_box_heights':{c['actor']:c['h'] for c in chars},'visible_actor_boxes_xywh':{c['actor']:c['box'] for c in record['characters']},'generation':'Built-in ImageGen reference extraction + existing native compositor','isotropic_actor_scaling':True})
        row['sha256']=sha(out);frames[fid]=row;updates.append(row)
    closer=load(HOME/'closer_review_22.json')
    for f in closer['frames']:
        if f['id'] in ids:
            if f['decision']=='retain':f['previous_decision']='retain'
            f['decision']='fix';f['reason']=frames[f['id']]['continuity_note'];f['owner_direction']='Final owner request: use s07_p01 shared readability as reference while preserving causal action and net state.'
    (HOME/'closer_review_22.json').write_text(json.dumps(closer,indent=2)+'\n')
    plan.update({'frames':sorted(frames.values(),key=lambda f:f['id']),'status':'final_six_reference_and_shared_world_corrections_pending_review','replacement_count':len(frames),'closer_review_fix_count':20,'closer_review_retained_count':2,'new_candidates_pending_owner_review':len(frames)-4,'continuity_revision_ids':ids,'final_reference_revision_ids':ids})
    (HOME/'complete_replacement_plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    reference=frames['s07_p01']
    report={'comparison_reference':{'id':'s07_p01','path':reference['output_path'],'sha256':reference['sha256'],'owner_feedback':'I think milo and leo have the correct nice size','scope':'Shared-view readability preference; not neutral-anatomy calibration'},'schema':'feltwillow.final-reference-corrections.v1','ids':ids,'assessment':'Agree with closer framing for all named frames. A true crouch lowers the body without distorting anatomy; net-action views use uniform camera cuts rather than independently resizing Milo.','pose_reference':'m_complete_reference_r03_candidate.png row3/column3 Crouch and row2/column3 Walk Right','head_measurement':'Upper35% alpha head/ear span; crouch uses an explicit head window to exclude its raised tail. Previous upper44% proxy included the running tail. These are screen-readability comparisons, not anatomical approval.','target_action_ear_span_px':target_action,'target_shared_ear_span_px':target_shared,'crouch_head_window_px':crouch_window,'frames':updates,'active_production_plans_modified':False}
    (HOME/'final_reference_corrections.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Final six corrections ready;',len(frames),'replacement slots; two retained originals.')
if __name__=='__main__':main()
