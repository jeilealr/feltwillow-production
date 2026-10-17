#!/usr/bin/env python3
"""Adopt the authorized, inspected v6 surface finishes; never approve video use.

One-shot operation. Verify all inputs before mutation; originals and old ledgers
are preserved. Requires the image inspection environment used by finish_frame.py.
"""
import hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[4]; HOME=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from production.keyframe_visual_gate import CHECKS,build_frame_dispositions
from production import video_boundary_plan
STORY=ROOT/'stories/lion_and_mouse_v6'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def rel(p):return str(p.relative_to(ROOT))
def main():
 audit=load(HOME/'audit.json');assert audit['status']=='in_progress','Already adopted; use verify_finish.py.'
 plan=load(STORY/'keyframe_plan.json');ledger=load(STORY/'owner_visual_acceptance.json');reviews=load(STORY/'keyframe_visual_reviews.json')
 before_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 # Scene 5 already integrates naturally. The attempted smooth-lighting changes
 # offer no visible improvement and are not selected merely to increase coverage.
 for row in audit['frames']:
  if row['id'] in ['s05_p02','s05_p03','s05_p04','s05x_p05']:
   row.update(decision='retain',status='retained_after_native_trial_comparison',reason='Native before/after and scene comparison show the original already has natural sunset material and contact; the restricted lighting trial adds no clear improvement.',actors_to_edit=[])
 changes=[r for r in audit['frames'] if r['decision']=='finish'];by_id={r['id']:r for r in plan['images']}
 assert len(changes)==47
 # Preflight every byte and edit support before moving any selected file.
 for row in audit['frames']:
  assert sha(ROOT/row['source_path'])==row['source_sha256']
 checked=set()
 for row in changes:
  source=ROOT/row['source_path'];candidate=ROOT/row['candidate_path'];assert sha(candidate)==row['candidate_sha256']
  assert Image.open(source).size==Image.open(candidate).size==(1920,1080)
  if row['source_sha256'] in checked:continue
  checked.add(row['source_sha256']);receipt_path=ROOT/row['candidate_receipt'];receipt=load(receipt_path)
  if row['id']=='s04_p03':
   mask=receipt_path.parent/'integration_edit_mask.png'
   assert sha(ROOT/receipt['generative_recipe']['raw_path'])==receipt['generative_recipe']['raw_sha256']
  else:
   mask=ROOT/receipt['edit_mask_path'];assert sha(ROOT/receipt['raw_generated_path'])==receipt['raw_sha256']
   for layer in receipt['source_layers']:assert sha(ROOT/layer['path'])==layer['sha256']
  a=np.array(Image.open(source).convert('RGB'));b=np.array(Image.open(candidate).convert('RGB'));m=np.array(Image.open(mask).convert('L'));diff=np.any(a!=b,axis=2)
  assert not np.any(diff & (m==0)),row['id']
  protected=receipt_path.parent/'protected_features.png'
  if protected.exists():assert not np.any(diff & (np.array(Image.open(protected))>0)),row['id']
 # Preserve full old authority/selection records, including untouched historical evidence.
 archive=ROOT/'character/characters/lion_and_mouse_v6/interactions/sources/integration_originals';archive.mkdir(exist_ok=True)
 snapshots=HOME/'before_adoption';snapshots.mkdir(exist_ok=True)
 for name in ['keyframe_plan.json','owner_visual_acceptance.json','keyframe_visual_reviews.json']:shutil.copyfile(STORY/name,snapshots/name)
 pathmap={};old_selections={r['id']:json.loads(json.dumps(r)) for r in ledger['images']};ledger_rows={r['id']:r for r in ledger['images']}
 for row in changes:
  fid=row['id'];active=by_id[fid];old_path=row['source_path'];old_hash=row['source_sha256'];old=ROOT/old_path
  archived=archive/old.name;assert not archived.exists();shutil.move(old,archived)
  new_name=re.sub(r'_r(\d+)_candidate',lambda m:'_r'+str(int(m[1])+1).zfill(2)+'_candidate',old.name)
  new=old.parent/new_name;assert not new.exists();shutil.copyfile(ROOT/row['candidate_path'],new);new_path=rel(new)
  pathmap[old_path]={'original':rel(archived),'selected':new_path}
  active.setdefault('generation_history',[]).append({'candidate_path':old_path,'archive_path':rel(archived),'sha256':old_hash,'prompt':active.get('historical_candidate_prompt'),'references':active.get('historical_candidate_references',[]),'generation_inputs':active.get('historical_candidate_inputs',[]),'git_locator':{'commit':before_commit,'path':old_path,'sha256':old_hash},'status':'historical_superseded_owner_selection','reason':'Owner-authorized C-style integration finish; original geometry and selected expression preserved.'})
  receipt_path=ROOT/row['candidate_receipt'];receipt=load(receipt_path)
  prompt_path=(receipt_path.parent/'integration_prompt.txt' if fid=='s04_p03' else receipt_path.parent/'prompt.txt')
  prompt=prompt_path.read_text()
  active.update(candidate_path=new_path,sha256=row['candidate_sha256'],historical_candidate_prompt=prompt,historical_candidate_references=[rel(archived)],historical_candidate_inputs=[{'role':'owner_correction_target','path':rel(archived),'sha256':old_hash,'required':False}],historical_candidate_tool='Built-in ImageGen suggestion with bounded integration postprocess; see selected_integration_finish.',revision_note='Selected geometry, identity features and expression retained; scoped character/background integration finish only.')
  active.pop('git_locator',None)
  active['selected_integration_finish']={'receipt':row['candidate_receipt'],'audit':rel(HOME/'audit.json'),'original_path':rel(archived),'original_sha256':old_hash,'finished_sha256':row['candidate_sha256'],'geometry_changed':False,'technical_approval_inferred':False,'previous_composition_record':active.get('selected_composition_record')}
  selected={'id':fid,'path':new_path,'sha256':row['candidate_sha256'],'selection_basis':'owner_selected_C_trial' if fid=='s04_p03' else 'owner_delegated_integration_finish_after_C_preference','reviewer':'project_owner' if fid=='s04_p03' else 'agent_under_owner_authorization','evidence':'I also prefer C, can we apply this change to all keyfeature images that need it. set that as the next goal','reconciled_at':'2026-10-17','previous_selection':old_selections[fid],'finish_receipt':row['candidate_receipt']}
  ledger_rows[fid].clear();ledger_rows[fid].update(selected);active['owner_visual_selection']=selected
  previous=reviews['images'].get(fid)
  if previous:reviews.setdefault('historical_visual_reviews',[]).append({'frame_id':fid,**previous,'superseded_reason':'Integration finish changes image hash; previous technical checks not transferred.'})
  reviews['images'][fid]={'sha256':row['candidate_sha256'],'reviewer':'agent_under_owner_authorization','reviewed_at':'2026-10-17','owner_approval_status':'owner_selected_C_trial_pending_technical_validation' if fid=='s04_p03' else 'owner_delegated_finish_selection_pending_technical_validation','checks':{name:None for name in CHECKS},'owner_visual_selection':selected,'integration_inspection':{'receipt':row['candidate_receipt'],'scope':'Native actor original/finish comparison and full-frame adjacent-scene inspection; integration-only acceptance, no new anatomy/setup/production approval.'}}
  row.update(source_path=rel(archived),original_active_path=old_path,active_path=new_path,active_sha256=row['candidate_sha256'],status='adopted_after_native_and_scene_inspection',inspection={'reviewer':'agent_under_owner_authorization','date':'2026-10-17','native_actor_comparison':True,'whole_frame_sequence_comparison':True,'result':'Directional lighting and material integrate with the selected location; expressions, scale, placement and prop contact remain consistent.'})
 # Relocate receipt inputs without rewriting immutable Git provenance or exact prompts.
 for rp in (HOME/'frames').glob('*/receipt.json'):
  r=load(rp)
  for key in ['source_path']:
   if r[key] in pathmap:r['original_active_path']=r[key];r[key]=pathmap[r[key]]['original']
  for layer in r['source_layers']:
   if layer['path'] in pathmap:layer['original_active_path']=layer['path'];layer['path']=pathmap[layer['path']]['original']
  r['status']='adopted_after_integration_inspection' if any(x['candidate_receipt']==rel(rp) for x in changes) else 'trial_not_selected_original_retained'
  r['prompt_path']=rel(rp.parent/'prompt.txt');r['prompt_sha256']=sha(rp.parent/'prompt.txt')
  for field,name in [('edit_mask','edit_mask.png'),('protected_features','protected_features.png')]:r[field+'_sha256']=sha(rp.parent/name)
  dump(rp,r)
 trial=HOME.parent/'integration_trial_s04_p03/verification.json';tr=load(trial);tr['source']['original_active_path']=tr['source']['path'];tr['source']['path']=pathmap[tr['source']['path']]['original'];tr['status']='C_selected_by_owner_and_adopted';tr['adoption_audit']=rel(HOME/'audit.json');dump(trial,tr)
 ledger.update(reconciled_at='2026-10-17',reviewer='project_owner_and_authorized_agent',scope='96 selected images: 47 C-style integration finishes (one individually owner-preferred trial, 46 agent-selected under explicit owner authorization), 49 original images retained. Earlier perceptual-world selections remain in previous_selection history. Technical approval is separate.')
 ledger['evidence']['integration_direction']='I also prefer C, can we apply this change to all keyfeature images that need it. set that as the next goal'
 ledger['counts']={'selected':96,'integration_finishes':47,'individually_owner_selected_C':1,'delegated_finish_selection':46,'retained_without_integration_change':49}
 summary={'ledger':'stories/lion_and_mouse_v6/owner_visual_acceptance.json','reconciled_at':'2026-10-17','count':96,'integration_finishes':47,'note':'One owner-selected trial and 46 agent-selected finishes under explicit owner authorization. Technical validation and staging/authority registration remain incomplete.'}
 plan['owner_visual_selection']=summary;reviews['owner_visual_selection']=summary;reviews['frame_dispositions']=build_frame_dispositions(plan,reviews)
 dump(STORY/'keyframe_plan.json',plan);dump(STORY/'owner_visual_acceptance.json',ledger);dump(STORY/'keyframe_visual_reviews.json',reviews)
 perceptual=load(STORY/'perceptual_world_plan.json')
 for r in perceptual['frames']:
  r['candidate_path']=by_id[r['id']]['candidate_path'];r['sha256']=by_id[r['id']]['sha256']
 perceptual['source_sha256']['keyframe_plan.json']=sha(STORY/'keyframe_plan.json');perceptual['integration_audit']=rel(HOME/'audit.json');dump(STORY/'perceptual_world_plan.json',perceptual)
 boundaries=video_boundary_plan.build(plan,load(STORY/'video_boundary_config.json'),staging=load(STORY/'staging_plan.json'))
 dump(STORY/'video_boundary_plan.json',boundaries);(STORY/'VIDEO_BOUNDARIES.md').write_text(video_boundary_plan.markdown(boundaries))
 # Only current presentation links are rebound. Old receipts/prompts keep generation-time paths.
 current=STORY/'KEYFRAME_REVIEW.md';text=current.read_text()
 for old,mapping in pathmap.items():text=text.replace(Path(old).name,Path(mapping['selected']).name)
 current.write_text(text)
 audit.update(status='complete',completed_at='2026-10-17',pre_finish_commit=before_commit,selection_scope='Owner preferred the C trial and delegated rollout; agent inspected and selected the other finishes. No per-image owner review or production approval is inferred.')
 audit['counts']={'screened':96,'trialled_slots':51,'trialled_distinct_sources':39,'adopted':47,'adopted_distinct_sources':35,'retained':49,'trialled_but_retained':4};dump(HOME/'audit.json',audit)
 dump(HOME/'adoption_paths.json',pathmap);print(json.dumps(audit['counts']))
if __name__=='__main__':main()
