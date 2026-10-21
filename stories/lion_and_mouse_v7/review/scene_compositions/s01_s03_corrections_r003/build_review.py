"""Current S01–S03 review: latest correction bytes, retained references and audio."""
import json,hashlib,html,os
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[4];B=D.parent/'s01_s03_performance_r002'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 latest=D.parent/"acorn_continuity_r004/build_review.py"
 if (latest.parent/"EXECUTION.json").is_file():
  import runpy
  return runpy.run_path(str(latest))["build"]()
 op=read(D/'OPERATION.json');log=read(D/'EXECUTION.json');assert log['completed']==11
 old=read(B/'AUDIO_IMAGE_INDEX.json')['images'];byid={q['image_id']:(q,r) for q,r in zip(op['requests'],log['outputs']) if q['image_id']}
 plan=read(R/'stories/lion_and_mouse_v7/audio_visual_plan.json');lines={l['line_id']:l for l in plan['lines']}
 notes={'S01-L004-B01-I01':['Earlier phase: upright noticing seeds, hands clear of ground; compare with retained reaching I02.'], 'S03-L001-B01-I02':['Acting flag: requested forward look still reads upward, similar to the sky anchor.'], 'S03-L002-B01-I02':['Acting flag: requested thoughtful forward gaze remains upward.'], 'S03-L008-B01-I02':['Acting review: right gaze remains pitched upward.'], 'S02-L004-B01-I02':['Prop flag: held acorn appears smaller than the placement reference; no prop-scale pass.'], 'S03-L009-B01-I01':['Body/crop follows L010 reference; stronger brow expression needs owner review.']}
 ledger_path=D.parent/'acorn_continuity_r004/OWNER_DIRECTION.json'
 ledger=read(ledger_path) if ledger_path.is_file() else {}
 retained_paths={r['path']:r for r in ledger.get('retained_candidates',[])}
 pending_acorns={'S01-L004-B03-I03','S02-L001-B01-I02','S02-L004-B01-I02','S02-L004-B02-I03'} if ledger else set()
 rows=[];cards=[]
 def url(path):return html.escape(os.path.relpath(R/path,D),quote=True)
 def fig(path,title):return '<figure><figcaption>'+html.escape(title)+'</figcaption><a href="'+url(path)+'"><img loading="lazy" src="'+url(path)+'"></a></figure>'
 def card(row,prior=None):
  lid=row['line_id'];iid=row.get('image_id') or 'S01-L001 · forest establishment';obs=list(row.get('review_notes',[]))
  if row['path'] in retained_paths:
   row['status']='owner_retained_candidate';row['retention_decision']=retained_paths[row['path']]
  if iid in pending_acorns:
   row['status']='owner_requested_acorn_correction_pending';obs.insert(0,'Pending: match S02-L001 acorn size with same small eaten area; S02-L004 shares standing frame then continuous crouch/contact/release. Existing pixels unchanged.')
  if iid.startswith('S03-L') and int(lid[-3:])<=8:
   obs+=['Stationary fork group: visually close root/body placement, native root/scale measurements pending.','Exact background gate: FAIL for each generated fork edit (pixel drift outside actor rectangle); remains a review candidate, not approved continuity.'] if iid in byid else ['Retained L006 setup reference; no new request.']
  extra=('<details><summary>Previous candidate and setup anchor</summary><div class="compare">'+fig(prior['path'],'Previous candidate · preserved')+fig(byid[iid][0]['inputs'][1]['path'],'Setup reference')+'</div></details>') if prior else ''
  cards.append('<article id="'+iid+'"><h2>'+iid+'</h2><p class="status">'+html.escape(row['status'])+'</p><p>'+html.escape(lines[lid]['text'])+'</p><audio controls preload="none" src="'+url(lines[lid]['audio']['wav'])+'"></audio>'+fig(row['path'],'Current candidate · click for native PNG')+'<ul>'+''.join('<li>'+html.escape(n)+'</li>' for n in obs)+'</ul>'+extra+'</article>')
 # New editorial establishing image precedes the retained opening walk image.
 q=op['requests'][-1];out=log['outputs'][-1];est={**out,'line_id':'S01-L001','beat_id':'S01-L001-B01','audio':q['audio'],'status':'candidate_pending_owner_review','review_notes':['Environment-only establishment for the 9.96-second opening; editorial cut pending audio alignment.','Defect: small pale corner symbol remains bottom right. No automatic cleanup submitted.']};rows.append(est);card(est)
 for before in old:
  iid=before['image_id']
  if iid in byid:
   q,out=byid[iid];row={**out,'line_id':q['line_id'],'beat_id':q['beat_id'],'audio':q['audio'],'performance':q['performance'],'status':'candidate_pending_owner_review','review_notes':notes.get(iid,[]),'owner_approval':None};card(row,before)
  else:
   row={**before,'status':'retained_previous_candidate_pending_review'}
   if iid=='S03-L010-B01-I01':row['review_notes']=['Retained preferred upper-body/crop reference; no new request.']
   elif iid=='S02-L004-B02-I03':row['review_notes']=['Retained background reference; hand still touches acorn, release action not passed.']
   card(row)
  rows.append(row)
 for row in rows:
  assert digest(R/row['path'])==row['sha256']
 write(D/'AUDIO_IMAGE_INDEX.json',{'schema':'feltwillow.current-scene-candidates.v1','new_candidates':11,'retained_previous_candidates':14,'images':rows,'owner_scene_approvals':0})
 style='body{font:17px system-ui;background:#252821;color:#eee;margin:25px auto;padding:0 20px;max-width:1450px}a{color:#c7edab}article{background:#343a31;padding:18px;margin:25px 0;border-radius:10px}figure{margin:12px 0}img{width:100%;height:auto;display:block}figcaption,.status{color:#ffdb91;margin:8px 0}audio{width:100%;max-width:700px}.compare{display:grid;grid-template-columns:1fr 1fr;gap:15px}li{margin:9px 0}body.native figure{overflow:auto}body.native article>figure img{width:auto;max-width:none}'
 page='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>S01–S03 corrections r003</title><style>'+style+'</style></head><body><h1>S01–S03 · latest corrections r003</h1><p><strong>11 new candidates saved; 14 previous images retained. One request each, no retries. Current retention/correction status appears on each card.</strong></p><p>Includes distinct upright seed-noticing I01, seven stationary fork edits anchored to retained L006, L009 portrait using L010 body/crop, acorn-holding background correction and forest establishment. Original PNGs and receipts are intact.</p><p><strong>Continuity limitation:</strong> native pixel comparison finds background drift on all seven generated fork edits. Root/scale are visually closer but not measured. These do not pass the exact-background contract. Forward-gaze, acorn-size and corner-symbol flags appear below; no extra repair calls were made.</p><p><a href="../../character_performance_consistency_r001/pose_library/review.html">Milo poses and canonical measurements</a></p><label><input id="native" type="checkbox"> Native-pixel view (scroll)</label>'+''.join(cards)+'<script>document.querySelector("#native").addEventListener("change",e=>document.body.classList.toggle("native",e.target.checked));document.querySelectorAll("audio").forEach(p=>p.addEventListener("play",()=>document.querySelectorAll("audio").forEach(q=>{if(q!==p)q.pause()})));</script></body></html>'
 (D/'review.html').write_text(page+'\n')
 backup=B/'review_before_r003.html'
 if not backup.exists():backup.write_bytes((B/'review.html').read_bytes())
 (B/'review.html').write_text(page+'\n')
 print(json.dumps({'new':11,'retained':14,'cards':len(rows),'exact_fork_background_pass':False}))
if __name__=='__main__':build()
