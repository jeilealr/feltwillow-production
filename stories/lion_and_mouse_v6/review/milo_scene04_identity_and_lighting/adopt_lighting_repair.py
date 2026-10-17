#!/usr/bin/env python3
"""Adopt the owner-directed facial-lighting repair only; no identity promotion."""
import copy,hashlib,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HOME=Path(__file__).resolve().parent;STORY=ROOT/'stories/lion_and_mouse_v6'
sys.path.insert(0,str(ROOT))
from production.keyframe_visual_gate import CHECKS,build_frame_dispositions
from production import video_boundary_plan

def load(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return str(p.relative_to(ROOT))
def main():
 receipt=load(HOME/'lighting_receipt.json');assert receipt['status']=='prepared_pending_owner_review_not_adopted','Already adopted.'
 plan=load(STORY/'keyframe_plan.json');row=next(x for x in plan['images'] if x['id']=='s04_p02');old_path=row['candidate_path'];old=ROOT/old_path;assert sha(old)==row['sha256']==receipt['source_sha256'];candidate=ROOT/receipt['output_path'];assert sha(candidate)==receipt['output_sha256']
 owner=load(STORY/'owner_visual_acceptance.json');reviews=load(STORY/'keyframe_visual_reviews.json');previous=copy.deepcopy(row);old_selection=copy.deepcopy(next(x for x in owner['images'] if x['id']==row['id']))
 dump(HOME/'before_lighting_adoption.json',{'keyframe':previous,'selection':old_selection,'technical_review':reviews['images'].get(row['id'])})
 archive=ROOT/'character/characters/lion_and_mouse_v6/interactions/sources/lighting_repairs'/old.name;archive.parent.mkdir(exist_ok=True);assert not archive.exists();shutil.move(old,archive)
 active=old.parent/'s04_p02_r14_candidate.png';assert not active.exists();shutil.copyfile(candidate,active)
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();locator={'commit':head,'path':old_path,'blob':subprocess.check_output(['git','rev-parse',head+':'+old_path],cwd=ROOT,text=True).strip(),'sha256':previous['sha256']}
 row.setdefault('generation_history',[]).append({'candidate_path':old_path,'archive_path':rel(archive),'sha256':previous['sha256'],'git_locator':locator,'prompt':previous['historical_candidate_prompt'],'references':previous['historical_candidate_references'],'generation_inputs':previous.get('historical_candidate_inputs',[]),'status':'historical_superseded_owner_selection','reason':'Owner identified bright facial disc from earlier face-protection mask; continuous illumination repair preserves original geometry and texture.'})
 inputs=load(HOME/'inputs.json');inputs[1]['original_generation_path']=old_path;inputs[1]['path']=rel(archive);dump(HOME/'inputs.json',inputs)
 ref=inputs[2]
 historical=[{'role':'owner_correction_target','path':rel(archive),'sha256':previous['sha256'],'required':False,'regeneration_allowed':False,'owner_directed_correction':True,'authority_scope':'correction target only; not identity, scale, camera, plate, or lighting authority'},{'role':'owner_correction_reference','path':ref['path'],'sha256':ref['sha256'],'required':False,'regeneration_allowed':False,'owner_directed_correction':True,'authority_scope':'correction guidance only; not identity, scale, pose, camera, plate, or lighting authority'}]
 row.update(candidate_path=rel(active),sha256=receipt['output_sha256'],historical_candidate_prompt=(HOME/'lighting_prompt.txt').read_text().strip(),historical_candidate_references=[r['path'] for r in historical],historical_candidate_inputs=historical,historical_candidate_tool='Built-in ImageGen lighting guidance; smooth bounded illumination transfer to original pixels.',revision_note='Owner-directed removal of bright face-mask disc; geometry, expression detail, scale, placement and background retained.')
 row.pop('git_locator',None);row['selected_lighting_repair']={'receipt':rel(HOME/'lighting_receipt.json'),'original_path':rel(archive),'original_sha256':previous['sha256'],'output_sha256':receipt['output_sha256'],'geometry_changed':False,'identity_authority_changed':False}
 selection={'id':row['id'],'path':row['candidate_path'],'sha256':row['sha256'],'selection_basis':'owner_directed_face_lighting_artifact_repair','reviewer':'agent_under_owner_authorization','reconciled_at':'2026-10-17','evidence':'When zooming s04_p02_r13 the owner reported a circular bright area on Milo\'s face and preferred the natural integration of s04x_p02_r03.','previous_selection':old_selection,'finish_receipt':rel(HOME/'lighting_receipt.json')}
 row['owner_visual_selection']=selection
 for i,r in enumerate(owner['images']):
  if r['id']==row['id']:owner['images'][i]=selection
 owner['evidence']['face_lighting_correction']='Owner identified an artificial circular bright facial patch in s04_p02_r13; light-only repair selected by agent under that correction request.';owner['counts']['subsequent_lighting_repairs']=1
 previous_review=reviews['images'].get(row['id'])
 if previous_review:reviews.setdefault('historical_visual_reviews',[]).append({'frame_id':row['id'],**previous_review,'superseded_reason':'New facial-lighting correction changes image hash; prior technical evidence not transferred.'})
 reviews['images'][row['id']]={'sha256':row['sha256'],'reviewer':'agent_under_owner_authorization','reviewed_at':'2026-10-17','owner_approval_status':'owner_directed_repair_pending_technical_validation','checks':{k:None for k in CHECKS},'owner_visual_selection':selection,'integration_inspection':{'receipt':rel(HOME/'lighting_receipt.json'),'scope':'Native matching before/after actor crops and whole-frame inspection; continuous face/body illumination, original details and geometry retained.'}}
 reviews['frame_dispositions']=build_frame_dispositions(plan,reviews);dump(STORY/'keyframe_plan.json',plan);dump(STORY/'owner_visual_acceptance.json',owner);dump(STORY/'keyframe_visual_reviews.json',reviews)
 receipt.update(status='adopted_owner_directed_lighting_repair',source_path=rel(archive),original_generation_path=old_path,active_path=rel(active),active_sha256=row['sha256'],active_selection_changed=True,previous_selection=old_selection);dump(HOME/'lighting_receipt.json',receipt)
 audit_path=STORY/'review/integration_finish/audit.json';audit=load(audit_path)
 a=next(x for x in audit['frames'] if x['id']==row['id']);a.update(initial_adopted_path=a['active_path'],initial_adopted_sha256=a['active_sha256'],active_path=row['candidate_path'],active_sha256=row['sha256'],post_adoption_lighting_repair=rel(HOME/'lighting_receipt.json'),status='adopted_with_subsequent_owner_directed_lighting_repair');dump(audit_path,audit)
 advisory=load(STORY/'perceptual_world_plan.json')
 a=next(x for x in advisory['frames'] if x['id']==row['id']);a.update(candidate_path=row['candidate_path'],sha256=row['sha256']);advisory['source_sha256']['keyframe_plan.json']=sha(STORY/'keyframe_plan.json');dump(STORY/'perceptual_world_plan.json',advisory)
 boundary=video_boundary_plan.build(plan,load(STORY/'video_boundary_config.json'),staging=load(STORY/'staging_plan.json'));dump(STORY/'video_boundary_plan.json',boundary);(STORY/'VIDEO_BOUNDARIES.md').write_text(video_boundary_plan.markdown(boundary))
 p=STORY/'KEYFRAME_REVIEW.md';p.write_text(p.read_text().replace(Path(old_path).name,active.name))
 print('Adopted',rel(active),'; new canonical remains a candidate.')
if __name__=='__main__':main()
