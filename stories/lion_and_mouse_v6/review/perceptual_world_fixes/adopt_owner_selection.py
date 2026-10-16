#!/usr/bin/env python3
"""Activate the owner's reviewed stills, without approving technical/render gates."""
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from production import keyframe_reference_gate,video_boundary_plan
from production.revise_keyframe_candidate import write_plan
HOME=Path(__file__).resolve().parent;STORY=HOME.parent.parent
KEYFRAMES=ROOT/'character/characters/lion_and_mouse_v6/interactions/keyframes'
EVIDENCE='they all passed! are they set now as ketframes at /Users/lealroja/Documents/feltwillow/feltwillow-production/character/characters/lion_and_mouse_v6/interactions/keyframes with no other previous version? if no, please do so'
def read(p):return json.loads(p.read_text())
def write(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return str(p.relative_to(ROOT))
def contact_sheets(plan,boundaries):
    directory=KEYFRAMES/'.review/contact_sheets/current';directory.mkdir(parents=True,exist_ok=True)
    font=ImageFont.load_default(size=15);titlefont=ImageFont.load_default(size=24)
    by_id={f['id']:f for f in plan['images']}
    for scene in boundaries['scenes']:
        ids=scene['ordered_keyframes'];rows=(len(ids)+2)//3;w=1496;h=48+58+rows*304+max(0,rows-1)*14
        out=Image.new('RGB',(w,h),'#1f1f1f');draw=ImageDraw.Draw(out);draw.text((24,24),f"Scene {scene['scene']:02d} - CURRENT owner-selected keyframes",font=titlefont,fill='white')
        for i,fid in enumerate(ids):
            f=by_id[fid];im=Image.open(ROOT/f['candidate_path']).convert('RGB').resize((480,270),Image.Resampling.LANCZOS);x=24+i%3*494;y=82+i//3*318
            out.paste(im,(x,y));draw.text((x+2,y+278),fid+'  '+Path(f['candidate_path']).stem,font=font,fill='white')
        out.save(directory/('scene%02d_keyframes.png'%scene['scene']))
    write(directory/'manifest.json',{'story':'lion_and_mouse_v6','images':[{k:f[k] for k in ['id','scene','candidate_path','sha256']} for f in plan['images']],'builder':'Portable Pillow layout matching native three-column scene-sheet presentation'})
def main():
    target=HOME/'owner_adoption.json'
    if target.exists() and read(target).get('status')=='adopted':
        print('Already adopted; verify owner_adoption.json and current inventory.');return
    proposal=read(HOME/'complete_replacement_plan.json')
    if proposal.get('status')=='owner_selected_set_adopted':
        plan=read(STORY/'keyframe_plan.json');boundaries=read(STORY/'video_boundary_plan.json')
        contact_sheets(plan,boundaries)
        previous_path=HOME/'previous_selection/keyframe_plan_before_adoption.json'
        prior={f['id']:f for f in read(previous_path)['images']};rows=[]
        for f in proposal['frames']:
            old=prior[f['id']];archive=HOME/'previous_selection'/Path(old['candidate_path']).name
            assert sha(archive)==old['sha256'] and sha(ROOT/f['output_path'])==f['sha256']
            rows.append({'id':f['id'],'previous_path':old['candidate_path'],'archive_path':rel(archive),'previous_sha256':old['sha256'],'review_artifact_path':f['review_artifact_path'],'active_path':f['output_path'],'sha256':f['sha256']})
        assert len(list(KEYFRAMES.glob('*.png')))==96
        write(target,{'schema':'feltwillow.owner-keyframe-adoption.v1','status':'adopted','owner_evidence':EVIDENCE,'mac_checkout_accessible':False,'previous_plan_path':rel(previous_path),'archived_source_paths':{f['previous_path']:f['archive_path'] for f in rows},'count':41,'unchanged_count':55,'current_keyframe_count':96,'obsolete_direct_keyframes':0,'all_16_contact_sheets_rebuilt':True,'technical_gate_status':'pending; staging/authority approvals were not promoted','frames':rows})
        print('Adoption completed: 41 replacements, 96 active PNGs, 16 rebuilt sheets.');return
    old_plan=read(STORY/'keyframe_plan.json');old_reviews=read(STORY/'keyframe_visual_reviews.json');acceptance=read(STORY/'owner_visual_acceptance.json')
    old_by_id={f['id']:f for f in old_plan['images']};stage=read(STORY/'staging_plan.json');staged={f['id']:f for f in stage['frames']}
    assert len(old_by_id)==96 and len(proposal['frames'])==41
    for f in old_plan['images']:assert sha(ROOT/f['candidate_path'])==f['sha256']
    for f in proposal['frames']:
        p=ROOT/f['output_path'];assert sha(p)==f['sha256'] and Image.open(p).size==(1920,1080)
    archive=HOME/'previous_selection';archive.mkdir(exist_ok=True)
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    tree=subprocess.check_output(['git','ls-tree','-r',commit],cwd=ROOT).decode().splitlines();blobs={line.split('\t',1)[1]:line.split()[2] for line in tree if '\t' in line}
    def locator(path,digest):return {'commit':commit,'path':path,'blob':blobs[path],'sha256':digest}
    previous_plan=archive/'keyframe_plan_before_adoption.json';write(previous_plan,old_plan);write(archive/'keyframe_visual_reviews_before_adoption.json',old_reviews);write(archive/'owner_visual_acceptance_before_adoption.json',acceptance)
    archived={old_by_id[f['id']]['candidate_path']:rel(archive/Path(old_by_id[f['id']]['candidate_path']).name) for f in proposal['frames']}
    report={'schema':'feltwillow.owner-keyframe-adoption.v1','status':'prepared','owner_evidence':EVIDENCE,'source_commit':commit,'mac_checkout_accessible':False,'previous_plan_path':rel(previous_plan),'archived_source_paths':archived,'count':41,'unchanged_count':55,'scope':'Owner visual selection and active files only. Staging/anatomical/authority/render gates are not approved by this operation.','frames':[]}
    updated=copy.deepcopy(old_plan);updates={f['id']:f for f in updated['images']};reviews=copy.deepcopy(old_reviews);accepted={f['id']:f for f in acceptance['images']}
    for f in proposal['frames']:
        fid=f['id'];old=old_by_id[fid];row=updates[fid];source=f['output_path'];destination=rel(KEYFRAMES/Path(source).name);archive_path=archived[old['candidate_path']]
        old_file=ROOT/old['candidate_path'];archived_file=ROOT/archive_path
        assert not archived_file.exists() or sha(archived_file)==old['sha256']
        shutil.copy2(old_file,archived_file);shutil.copy2(ROOT/source,ROOT/destination)
        selection={'id':fid,'path':destination,'sha256':f['sha256'],'selection_basis':'explicit_perceptual_world_final_set_acceptance','reviewer':'project_owner','evidence':EVIDENCE,'reconciled_at':'2026-10-16'}
        row.setdefault('generation_history',[]).append({'candidate_path':old['candidate_path'],'sha256':old['sha256'],'git_locator':locator(old['candidate_path'],old['sha256']),'archive_path':archive_path,'status':'historical_superseded_owner_selection','reason':'Owner accepted the reviewed perceptual-world replacement set.'})
        row['historical_previous_selection']={'archive_path':archive_path,'sha256':old['sha256'],'snapshot':rel(previous_plan)}
        row.update(candidate_path=destination,sha256=f['sha256'],canvas_px=[1920,1080],status='candidate_generated_pending_owner_review',owner_visual_selection=selection,git_locator=locator(source,f['sha256']),regeneration_status='stale_pending_new_revision',technical_reconciliation_note='Owner selected these existing bytes. Stale denotes pending staging/authority registration, not visual rejection or permission to regenerate.',revision_note='Owner-selected perceptual-world composition; exact approved PNG activated.',selected_composition_record={'path':rel(HOME/'complete_replacement_plan.json'),'id':fid},historical_candidate_tool=f.get('generation','Built-in ImageGen layers and native compositor'))
        row['planned_view']=old.get('view');row['planned_crop_rect_on_plate']=old.get('crop_rect_on_plate');row['planned_actors']=old.get('actors');row['historical_previous_staging_signature']=old.get('staging_signature');row.pop('staging_signature',None)
        inputs=[]
        if 'composition_receipt' in f:
            record=read(ROOT/f['composition_receipt']);crop=f['crop_rect_on_plate'];actors=[c['actor'] for c in record['characters']]
            row['view']='upper_body_close' if record.get('blur') else ('medium_two' if len(actors)>1 else 'medium_solo')
            row['crop_rect_on_plate']=crop;row['selected_actor_placements']=record['characters'];row['actors']={actor:{} for actor in actors}
            row['historical_candidate_prompt']=json.dumps({'native_composition_receipt':f['composition_receipt'],'record':record},ensure_ascii=False)
            for item in [record['plate_source']]+[c['still_source'] for c in record['characters']]:inputs.append({'role':'historical_compositor_input','path':item['label'],'sha256':item['sha256'],'required':False})
        elif 'camera_source' in f:
            source_record=old_by_id['s13_p03'] if fid.startswith('s13_') else old
            base=source_record['crop_rect_on_plate'];cut=f['crop_rect_on_selected_image'];row['crop_rect_on_plate']=[base[0]+cut[0]*base[2],base[1]+cut[1]*base[3],base[2]*cut[2],base[3]*cut[3]]
            row['view']='medium_two';row['actors']={a:{} for a in staged[fid]['actors']};row['selected_camera_crop']=f['camera_source']|{'crop_rect_on_selected_image':cut,'plate_registration_status':'derived_from_selected_composite_pending_technical_registration'}
            item=f['camera_source'];inputs.append({'role':'historical_selected_composite','path':archived.get(item['path'],item['path']),'original_path':item['path'],'sha256':item['sha256'],'required':False});row['historical_candidate_prompt']=json.dumps(read(ROOT/f['camera_crop_receipt']),ensure_ascii=False)
        else:
            item=f['reuse_source'];base=old_by_id[item['id']];row['crop_rect_on_plate']=base['crop_rect_on_plate'];row['view']=base['view'];row['actors']={a:{} for a in staged[fid]['actors']};inputs.append({'role':'historical_selected_insert','path':archived.get(item['path'],item['path']),'sha256':item['sha256'],'required':False});row['historical_candidate_prompt']=f['generation']
        row['historical_candidate_inputs']=inputs;row['historical_candidate_references']=[i['path'] for i in inputs]
        for field in ['prompt','references','reference_roles','generation_inputs','generation_tool']:row.pop(field,None)
        old_review=reviews['images'].get(fid,{})
        reviews.setdefault('historical_visual_reviews',[]).append({'id':fid,'reason':'Superseded by owner-approved perceptual-world image','record':copy.deepcopy(old_review)})
        reviews['images'][fid]={'sha256':f['sha256'],'reviewer':'project_owner','reviewed_at':'2026-10-16','owner_approval_status':'owner_selected_pending_technical_validation','checks':{k:None for k in old_review.get('checks',{})},'owner_visual_selection':selection,'review_note':'Owner accepted the reviewed perceptual-world set. No anatomical, staging or render authority approval is inferred.'}
        accepted[fid]=selection;f.update(output_path=destination,review_artifact_path=source,status='owner_selected_active_pending_technical_validation',owner_visual_selection=selection)
        report['frames'].append({'id':fid,'previous_path':old['candidate_path'],'archive_path':archive_path,'previous_sha256':old['sha256'],'review_artifact_path':source,'active_path':destination,'sha256':f['sha256']})
    # Move the superseded direct images outside the active keyframe directory.
    for previous,archived_path in archived.items():
        assert sha(ROOT/previous)==sha(ROOT/archived_path);(ROOT/previous).unlink()
    acceptance['images']=[accepted[f['id']] for f in updated['images']];acceptance['scope']='Current 96-image owner selection, including 41 explicitly accepted perceptual-world replacements and 55 retained selections. Technical validation remains separate.';acceptance['evidence']['perceptual_world_final_acceptance']=EVIDENCE
    summary={'ledger':rel(STORY/'owner_visual_acceptance.json'),'reconciled_at':'2026-10-16','count':96,'perceptual_world_replacements':41,'note':'Owner visual selection only; technical validation and staging/authority registration remain incomplete.'}
    updated['owner_visual_selection']=summary;reviews['owner_visual_selection']=summary
    write(STORY/'owner_visual_acceptance.json',acceptance);write(STORY/'keyframe_visual_reviews.json',reviews)
    config=read(STORY/'video_boundary_config.json');config['shared_entries'].pop('14',None);config['cut_reasons']['14']='Cut from Milo reaction portrait to the owner-selected knot-action insert; preserve the connected net state.'
    write(STORY/'video_boundary_config.json',config);boundaries=video_boundary_plan.build(updated,config,staging=stage);write_plan('lion_and_mouse_v6',updated,boundaries,root=ROOT)
    text=(STORY/'KEYFRAME_REVIEW.md').read_text()
    for f in report['frames']:text=text.replace(Path(f['previous_path']).name,Path(f['active_path']).name)
    text=text.replace('Reconciled 2026-10-16:', 'Perceptual-world owner selection adopted 2026-10-16:')
    (STORY/'KEYFRAME_REVIEW.md').write_text(text)
    proposal.update(status='owner_selected_set_adopted',owner_approved_compositions=41,new_candidates_pending_owner_review=0,active_production_plans_modified=True,owner_final_acceptance=EVIDENCE,adoption_manifest=rel(target));write(HOME/'complete_replacement_plan.json',proposal)
    contact_sheets(updated,boundaries)
    files=list(KEYFRAMES.glob('*.png'));assert len(files)==96 and {p.name for p in files}=={Path(f['candidate_path']).name for f in updated['images']}
    for f in updated['images']:assert sha(ROOT/f['candidate_path'])==f['sha256']
    report.update(status='adopted',current_keyframe_count=96,obsolete_direct_keyframes=0,all_16_contact_sheets_rebuilt=True,technical_gate_status='pending; previous staging/authority approvals were not promoted')
    write(target,report);print('Adopted 41 owner-selected replacements; 55 retained; exactly 96 active PNGs; no superseded direct images. All 16 scene sheets rebuilt.')
if __name__=='__main__':main()
