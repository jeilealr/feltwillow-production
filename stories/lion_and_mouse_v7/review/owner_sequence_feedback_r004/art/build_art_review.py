"""CPU-only read-only source review; writes annotations/proposals in this folder only."""
from pathlib import Path
import json,hashlib,subprocess,sys,html
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from feltwillow.wan import fit,fitted_record
OUT=Path(__file__).resolve().parent
STORY='stories/lion_and_mouse_v7/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
def record(p):
 p=Path(p);p=p if p.is_absolute() else ROOT/p
 return {'path':str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),'available':p.is_file(),'sha256':sha(p) if p.is_file() else None}
def write(n,x):(OUT/n).write_text(json.dumps(x,indent=2)+'\n')
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
# Baseline immutable source avoids other writers' in-progress authoritative migration.
plan=json.loads(subprocess.check_output(['git','show',f'{commit}:{STORY}audio_visual_plan.json'],cwd=ROOT))
rows=[]
for ledger in ('scene_image_selection_s01_s05.json','scene_composition_candidates_s06_s07.json','scene_composition_candidates_s08.json'):
 for r in read(STORY+ledger)['images']:
  rows.append(dict(r,ledger=STORY+ledger))
byid={r['image_id']:r for r in rows if r.get('image_id')}
def picked(i):
 r=byid[i];return dict(image_id=i,ledger=r['ledger'],recorded_sha256=r.get('sha256'),**record(r['path']))
inv={}
for scene in ('S05','S06'):
 slots=[]
 for line in plan['lines']:
  if not line['line_id'].startswith(scene):continue
  for b in line['beats']:
   for i in b['image_sequence']['images']:
    if scene=='S05' and not line['line_id'].startswith(('S05-L008','S05-L009')):continue
    slots.append({'image_id':i['id'],'role':i.get('role'),'selected':picked(i['id']) if i['id'] in byid else None,'planned_state':i,'status':'selected_exact' if i['id'] in byid else 'unfilled_logical_use'})
 inv[scene]=slots
write('SOURCE_ART_INVENTORY.json',{'source_commit':commit,'baseline_plan_sha256':hashlib.sha256(subprocess.check_output(['git','show',f'{commit}:{STORY}audio_visual_plan.json'],cwd=ROOT)).hexdigest(),'scenes':inv,'s08_affected_uses':[picked(f'S08-L{i:03}-B01-I01') for i in (16,17,18)]})
# Existing view-specific closed references, not automatically approved open calibration.
families=[]
for key,a in read(STORY+'character_performance_library.json')['assets'].items():
 if 'portrait' not in a.get('asset_type','') and 'portrait' not in key:continue
 for vname,v in a['variants'].items():
  if not (v.get('file') or {}).get('path'):continue
  families.append({'id':key+'.'+vname,'actor':a['actor'],'view':a.get('head_view',a.get('view')),'canonical':record(a['canonical']['path']),'closed_base':record(v['file']['path']),'closed_selection_scope':v.get('status'),'purpose':'speech_calibration','open_candidate':None,'mouth_roi_normalized':None,'production_eligible':False,'blocked_by':['matching_view_toothless_open_calibration_not_selected','mouth_ROI_and_fit_review_pending'],'constraints':{'no_teeth':True,'no_tongue_or_gums':True,'closed_boundaries':True,'matching_camera_scale_lighting':True,'outside_mouth_pixels_protected':True},'minimum_request':'one calibration per compatible view family, not one per dialogue line'})
write('MOUTH_FAMILY_PROPOSALS.json',{'source_commit':commit,'families':families,'historical_probe':read('experiments/lipsync_probe/evidence/input_manifest.json'),'historical_probe_reuse':'v6 diagnostic only; unavailable remote paths and old identity do not establish v7 calibration selection','bite_policy':'Separate shot-specific tiny open/contact and closed/tasted key; never narrator word-driven speech.'})
mp=[]
work=ROOT.parent/'work/stories/lion_and_mouse_v7/shots'
for name,scope in [('s02_l001_b01_i02_s1_fast','owner-liked visual feedback; not formal complete take selection'),('s02_l003_b01_i01_s1_fast','owner-reported unplanned hand; not fixed'),('s01_l004_b03_i03_s1_fast','owner-reported teeth; rejected baseline')]:
 mp.append(dict(record(work/(name+'.mp4')),receipt=record(work/(name+'.json')),scope=scope,whole_motion_review='not_performed_by_art_review'))
write('BASELINE_VIDEO_HASHES.json',{'videos':mp,'not_a_video_quality_pass':True})
# Explicitly marked analytical overlays; never production repair pixels.
reviewids=['S08-L001-B01-I01','S08-L016-B01-I01','S02-L004-B02-I02','S02-L004-B02-I03','S01-L004-B03-I03']
previews=[]
for i in reviewids:
 r=byid[i];im=Image.open(ROOT/r['path']);fitim=fit(im,1280,720);name=i+'_fit.png';fitim.save(OUT/name)
 previews.append({'id':i,**record(r['path']),'dimensions':list(im.size),'mode':im.mode,'fit':fitted_record(im,1280,720),'preview':name})
 if i.startswith('S08'):
  ov=im.convert('RGB');d=ImageDraw.Draw(ov)
  boxes=([(370,660,535,755),(625,680,745,760),(900,680,1070,800),(1090,680,1260,790)] if 'L001' in i else [(370,660,535,755),(625,680,745,760),(945,650,1115,755)])
  for n,b in enumerate(boxes):d.rectangle(b,outline='cyan',width=4);d.text((b[0],b[1]-15),f'Visible distal cluster {n+1}',fill='cyan',stroke_width=1,stroke_fill='black')
  if 'L016' in i:
   roi=(1040,605,1230,765);d.rectangle(roi,outline='red',width=5);d.text((1040,585),'Review far-forepaw attachment; NOT a transplant mask',fill='red',stroke_width=1,stroke_fill='white')
   mask=Image.new('L',im.size);ImageDraw.Draw(mask).rectangle(roi,fill=255);mask.save(OUT/'s08_paw_proposed_edit_envelope.png')
  ov.save(OUT/(i+'_anatomy_overlay.png'))
write('NATIVE_FIT_EVIDENCE.json',previews)
base=picked('S08-L016-B01-I01');reference=picked('S08-L001-B01-I01')
ops=[{'operation_id':'s08_missing_visible_paw_r002','type':'provider_edit_proposal_NOT_AUTHORIZED','max_calls':1,'retry_limit':0,'cost':'unknown; provider must be confirmed before authorization','provider':'image editor not yet selected; no unattended API assumed','ordered_references':[dict(role='edit base; preserve every pixel outside accepted edit region',**base),dict(role='lying limb topology reference only; NOT same-pose transplant',**reference),dict(role='Leo species identity/material',**record('character/characters/lion_and_mouse_v7/Leo/canonical/full-body_leo_neutral_pose_r01.png'))],'mask':record(OUT/'s08_paw_proposed_edit_envelope.png'),'mask_status':'proposed envelope, manual attachment review required before provider use','target_path':'character/characters/lion_and_mouse_v7/interactions/scene_compositions/S08-L016-B01-I01_single_gentle_clear_r002_candidate.png','positive_prompt':'Edit this same 1672x941 scene only in the reviewed far-forelimb envelope. Keep Leo lying gently with his head and chest raised, Milo and his clear route unchanged. Make the currently indistinct image-top-right far forepaw visibly attached to the correct existing foreleg, resting on the same ground with a rounded golden-cream felt paw, correct occlusion and small contact shadow. Preserve exactly four structurally accounted limbs, no claws or nails, identity, mane, ears, other paws, face, lighting, root, camera and backdrop. Do not copy the extended blocking pose from the reference. Do not place a new blocking paw in Milo’s route. Keep all protected pixels unchanged.','affected_uses':['S08-L016-B01-I01','S08-L017-B01-I01','S08-L018-B01-I01'],'deterministic_repair':'not geometrically justified: reference has extended blocking front limbs; base has different folded/released arrangement','required_reviews':['native limb tracing and manual four-limb audit','outside-mask exact pixel comparison','same-size fitted review','owner exact-hash scene selection'],'selection':None}, {'operation_id':'s01_tiny_bite_contact','type':'source_art_proposal_NOT_AUTHORIZED','source':picked('S01-L004-B03-I03'),'target':'new unique revisioned tiny_open_no_teeth_contact and closed_postbite states; names frozen after exact art route chosen','purpose':'physical tiny bite, not speech calibration','prompt':'Preserve exact local head projection, muzzle, ears, body, hands, backdrop and one whole supported acorn. Add only a tiny soft dark felt lip opening at acorn contact, no teeth, gums or tongue; close to a resting mouth after the tasted event. Acorn remains same scale/design; a small tasted notch exists only after the bite. No extra paw, duplicate acorn or crumbs.','status':'needs same-view contact ROI and selected closed/tasted art; no request submitted','retry_limit':0}, {'operation_id':'s02_beside_stone_contact_release','type':'source_art_proposal_NOT_AUTHORIZED','sources':[picked('S02-L004-B02-I02'),picked('S02-L004-B02-I03')],'purpose':'preserve spoken beside-stone meaning; correct prop support/contact while preserving standing->contact->released order','default_rise_coverage':'narrated_offscreen_before_first_visible_standing_key','prompt':'Keep the camera, stream, stone, vegetation and Milo body/root consistent. Show one tasted acorn on the ground beside the stone, with hands supporting during contact then separated during released settle. Preserve shell cap/stem/notch and local size; stable ground contact shadow, no floating, duplication or mouth lift. Only physically necessary hand/forearm/acorn support changes inside reviewed masks.','status':'native contact inspection and reviewed ground/hand masks required; no fabricated physical pass','retry_limit':0}]
write('OPERATION_PROPOSALS.json',{'source_commit':commit,'authorization':'none','operations':ops,'paid_calls_performed':0,'gpu_jobs_performed':0,'automatic_retries':0})
write('TECHNICAL_BLOCKS.json',{'S08-L016-B01-I01':{'status':'owner_selected_but_technically_blocked','reason':'owner-reported missing visible image-top-right paw; native review confirms fourth distal cluster not separately readable','propagates_to':['S08-L017-B01-I01','S08-L018-B01-I01'],'manual_anatomy_review_required':True,'anatomical_side':'not inferred from screen side','likely_limb':'far forelimb, attachment/occlusion must be reviewed','automatic_paw_count_certification':False},'mouth_calibration':'no V7-selected toothless open references established by old V6 probe','video_pass':False})
links=lambda p: html.escape(str(Path(p)))
cards=[]
for p in previews:
 cards.append(f'<article><h2>{p["id"]}</h2><p>{p["sha256"]}</p><a href="../../../../../{links(p["path"])}">Native source</a><img src="{p["preview"]}" alt="{p["id"]} fitted source"><p>1280×720 fitted preview; technical and art review remain separate.</p></article>')
(OUT/'REVIEW.html').write_text('<!doctype html><meta charset="utf-8"><title>r004 art dependencies</title><style>body{font:16px system-ui;max-width:1250px;margin:30px auto;background:#171717;color:#eee}img{width:100%}article{border-top:1px solid #888;margin-top:30px}a{color:#9cd}code{overflow-wrap:anywhere}</style><h1>r004 source-art review — no new selected art or video pass</h1><p>Native source bytes preserved. Red envelope is proposed review area, not a valid paw transplant. No paid call/GPU/retry performed.</p><p><a href="S08-L016-B01-I01_anatomy_overlay.png">L016 native paw overlay</a> · <a href="S08-L001-B01-I01_anatomy_overlay.png">L001 reference overlay</a> · <a href="OPERATION_PROPOSALS.json">Concrete proposals</a> · <a href="SOURCE_ART_INVENTORY.json">Exact inventories</a></p>'+''.join(cards))
print(json.dumps({'source_commit':commit,'families':len(families),'source_previews':len(previews),'output_directory':str(OUT),'S06_slots':len(inv['S06']),'S06_selected':sum(x['selected'] is not None for x in inv['S06'])}))
# Normalize legacy same-state aliases without treating them as new raster requests.
for x in inv['S06']:
 target=x['planned_state'].get('reuse_of')
 if target:x.update(status='explicit_alias_pending_target_review',alias_of=target)
missing=[{'image_id':x['image_id'],'variant':x['planned_state'].get('joint_performance_requirement',{}).get('variant')} for x in inv['S06'] if x['selected'] is None and not x.get('alias_of')]
write('SOURCE_ART_INVENTORY.json',{'source_commit':commit,'scenes':inv,'S06_summary':{'logical_slots':13,'selected_distinct_anchors':3,'authored_aliases':3,'missing_meaningful_phases':missing},'s08_affected_uses':[picked(f'S08-L{i:03}-B01-I01') for i in (16,17,18)]})
fork=read(STORY+'review/sequence_readiness_r001/fork_turn_preparation_r001/OPERATION.json')
write('FORK_FOUNDATION_DEPENDENCY.json',{'existing_preparation':record(STORY+'review/sequence_readiness_r001/fork_turn_preparation_r001/OPERATION.json'),'references_verified':[{**r,'actual':record(r['path'])} for r in fork['input_refs']],'existing_operation':fork,'current_status':'owner accepted strategy only; no completed clean plate or paid authorization inferred','dependent_turns':'correct original head-angle-specific pose/expression required; r004 small face ellipse cannot serve left/right yaw states','L006_anchor':picked('S03-L006-B01-I02'),'next_step':'one bounded clean-region reconstruction, exact protected restoration and reviewed result before angle-specific turn composites'})
# Candidate/calibration file availability is verified, never turned into approval.
write('CHECKS.json',{'command':'/Users/lealroja/miniconda3/envs/feltwillow/bin/python '+str(Path(__file__).relative_to(ROOT)),'source_commit':commit,'reviewer':'art_review','CPU_only':True,'source_checks':[{'id':x['image_id'],'hash_matches':x['sha256']==x['recorded_sha256']} for s in inv.values() for r in s if (x:=r['selected'])], 'fit_preview_count':len(previews),'json_outputs_valid':True,'paid_calls':0,'GPU_jobs':0,'video_whole_motion_review':'not_performed','deterministic_production_repairs':0})
