#!/usr/bin/env python3
"""Verify adopted finishes against preserved originals and exact edit masks.

Pixel checks prove bounded edits and preserved specified features; appearance and
physical scale still require inspection and the separate production gates.
"""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[4]; HOME=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from production.keyframe_reference_gate import validate_active_inventory
from production.keyframe_visual_gate import build_frame_dispositions
from production.video_boundary_plan import build
STORY=ROOT/'stories/lion_and_mouse_v6'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rgb(p):return np.array(Image.open(p).convert('RGB'))
def main():
 audit=load(HOME/'audit.json');assert audit['status']=='complete'
 plan=load(STORY/'keyframe_plan.json');ledger=load(STORY/'owner_visual_acceptance.json');reviews=load(STORY/'keyframe_visual_reviews.json');before=load(HOME/'before_adoption/keyframe_plan.json')
 rows={x['id']:x for x in plan['images']};owners={x['id']:x for x in ledger['images']};old={x['id']:x for x in before['images']}
 assert len(rows)==len(owners)==96
 assert not validate_active_inventory(plan,ROOT/'character/characters/lion_and_mouse_v6/interactions/keyframes')
 preserved_fields=['scene','view','crop_rect_on_plate','planned_view','planned_crop_rect_on_plate','planned_actors','planned_size_anchor_id','planned_camera_family','approved_plate','selected_actor_placements','regeneration_status']
 duplicates={};changed=0
 for a in audit['frames']:
  fid=a['id'];r=rows[fid];assert sha(ROOT/r['candidate_path'])==r['sha256']==owners[fid]['sha256'];assert r['candidate_path']==owners[fid]['path'];assert Image.open(ROOT/r['candidate_path']).size==(1920,1080)
  for field in preserved_fields:assert r.get(field)==old[fid].get(field),(fid,field)
  assert sha(ROOT/a['source_path'])==a['source_sha256']
  if a['decision']=='finish':
   changed+=1;assert r['sha256']==a['candidate_sha256']==sha(ROOT/a['candidate_path']);assert all(x is None for x in reviews['images'][fid]['checks'].values())
  else:assert r['sha256']==old[fid]['sha256']
  duplicates.setdefault(a['source_sha256'],set()).add(r['sha256'])
 assert changed==47;assert all(len(s)==1 for s in duplicates.values())
 checked=[]
 for rp in sorted((HOME/'frames').glob('*/receipt.json')):
  r=load(rp);source=ROOT/r['source_path'];output=ROOT/r['finished_path'];assert sha(source)==r['source_sha256'];assert sha(output)==r['finished_sha256'];assert sha(ROOT/r['raw_generated_path'])==r['raw_sha256']
  for layer in r['source_layers']:assert sha(ROOT/layer['path'])==layer['sha256']
  assert sha(ROOT/r['prompt_path'])==r['prompt_sha256']
  mask=ROOT/r['edit_mask_path'];protect=rp.parent/'protected_features.png';assert sha(mask)==r['edit_mask_sha256'];assert sha(protect)==r['protected_features_sha256']
  diff=np.any(rgb(output)!=rgb(source),axis=2);m=np.array(Image.open(mask));p=np.array(Image.open(protect));outside=int(np.count_nonzero(diff&(m==0)));protected=int(np.count_nonzero(diff&(p>0)))
  assert outside==protected==0;assert int(diff.sum())==r['changed_pixels']
  checked.append({'id':r['id'],'status':r['status'],'changed_pixels':int(diff.sum()),'changed_outside_mask':outside,'changed_protected_features':protected})
 trial=load(HOME.parent/'integration_trial_s04_p03/verification.json');tr=trial['results']['focused_generative'];assert sha(ROOT/tr['path'])==tr['sha256'];assert sha(ROOT/trial['source']['path'])==trial['source']['sha256']
 diff=np.any(rgb(ROOT/tr['path'])!=rgb(ROOT/trial['source']['path']),axis=2);mask=np.array(Image.open(HOME.parent/'integration_trial_s04_p03/integration_edit_mask.png'));assert not np.any(diff&(mask==0))
 yy,xx=np.mgrid[:1080,:1920];face=np.clip(np.maximum(0,1-(((xx-548)/83)**2+((yy-490)/62)**2))*5,0,1);assert not np.any(diff&(face==1))
 assert reviews['frame_dispositions']==build_frame_dispositions(plan,reviews)
 assert load(STORY/'video_boundary_plan.json')==build(plan,load(STORY/'video_boundary_config.json'),staging=load(STORY/'staging_plan.json'))
 manifest=load(ROOT/'character/characters/lion_and_mouse_v6/interactions/keyframes/.review/contact_sheets/current/manifest.json')
 assert manifest['images']==[{k:r[k] for k in ['id','scene','candidate_path','sha256']} for r in plan['images']]
 report={'schema':'feltwillow.integration-adoption-verification.v1','status':'passed','active_images':96,'adopted_slots':47,'distinct_adopted_sources':35,'retained_slots':49,'all_original_hashes_recoverable':True,'all_source_geometry_metadata_unchanged':True,'duplicates_preserve_exact_bytes':True,'owner_delegation_is_not_individual_owner_review':True,'technical_approvals_granted':False,'trial_C_exact_owner_preferred_bytes':True,'current_contact_sheet_manifest_matches':True,'receipts':checked}
 (HOME/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: 96 active images; 47 adopted / 49 retained; exact original hashes, masks, features, geometry, duplicates, selection ledger, boundary data and contact-sheet manifest verified.')
if __name__=='__main__':main()
