"""Render current candidates and acorn comparison; never generates media."""
import json,html,os,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[4];S=R/'stories/lion_and_mouse_v7'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 latest=D.parent/'acorn_setup_r005'
 if (latest/'EXECUTION.json').exists() and read(latest/'EXECUTION.json').get('completed')==2:
  import runpy
  runpy.run_path(str(latest/'build_review.py'),run_name='__main__');return
 op=read(D/'OPERATION.json');exe=read(D/'EXECUTION.json');assert exe['completed']==5
 prior=read(D.parent/'s01_s03_corrections_r003/AUDIO_IMAGE_INDEX.json')['images'];updates={q['image_id']:(q,o) for q,o in zip(op['requests'],exe['outputs'])};retained={r['path']:r for r in read(D/'OWNER_DIRECTION.json')['retained_candidates']};lines={l['line_id']:l for l in read(S/'audio_visual_plan.json')['lines']}
 notes={'S01-L004-B03-I03':['Small eaten area visible below the cap; compare acorn/head size with S02 reference. No measured scale pass.'], 'S02-L001-B01-I02':['Eaten area added while retaining reference size intent. Notch topology needs comparison across shots.'], 'S02-L004-B01-I02':['Standing hold with enlarged tasted acorn. This exact candidate is the proposed shared start for placement; no cut.'], 'S02-L004-B02-I02':['Crouched contact key: hands still touch/support acorn on rock. Body/head proportions and root contacts remain unmeasured.'], 'S02-L004-B02-I03':['Hands visibly withdrawn from acorn. CONTINUITY FLAG: eaten area is larger/rounder than contact frame; acorn also appears smaller. This does not pass unchanged-prop-state continuity.']}
 rows=[]
 def current(q,o):return {**o,'line_id':q['line_id'],'beat_id':q['beat_id'],'audio':q['audio'],'status':'candidate_pending_owner_review','review_notes':notes[q['image_id']],'owner_approval':None}
 for old in prior:
  iid=old.get('image_id')
  if iid=='S02-L004-B02-I03':q,o=updates['S02-L004-B02-I02'];rows.append(current(q,o))
  if iid in updates:q,o=updates[iid];rows.append(current(q,o))
  else:
   r=dict(old);assert r['path'] in retained;r['status']='owner_retained_candidate';r['retention_decision']=retained[r['path']];rows.append(r)
 overlay_path=D.parent/'acorn_setup_r005/OWNER_DIRECTION.json'
 if overlay_path.exists():
  overlay=read(overlay_path)
  held={r['path']:r for r in overlay['retained_candidates']}
  for row in rows:
   if row['path'] in held:
    row['status']='owner_retained_candidate';row['retention_decision']=held[row['path']]
   elif row.get('image_id') in ['S01-L004-B03-I03','S02-L001-B01-I02']:
    row['status']='revision_proposed_not_generated'
    row['review_notes']=['Pending r005: whole acorn before eating.' if row['image_id'].startswith('S01') else 'Pending r005: use current S02-L004 standing background/root/scale and smaller bitten acorn.']+row.get('review_notes',[])
 assert len(rows)==26
 def url(path):return html.escape(os.path.relpath(R/path,D),quote=True)
 def pic(row,caption):return '<figure><figcaption>'+html.escape(caption)+'</figcaption><a href="'+url(row['path'])+'"><img loading="lazy" src="'+url(row['path'])+'"></a></figure>'
 cards=[]
 for row in rows:
  assert sha(R/row['path'])==row['sha256'];iid=row.get('image_id') or 'S01-L001 · forest establishing';lid=row['line_id'];q=updates.get(iid);extra=''
  if q:
   base=q[0]['inputs'][1];extra='<details><summary>Original edit base · unchanged</summary>'+pic(base,'Source reference, preserved')+'</details>'
  cards.append('<article id="'+iid+'"><h2>'+iid+'</h2><p class="status">'+row['status']+'</p><p>'+html.escape(lines[lid]['text'])+'</p><audio controls preload="none" src="'+url(lines[lid]['audio']['wav'])+'"></audio>'+pic(row,'Current candidate · click for native PNG')+'<ul>'+''.join('<li>'+html.escape(n)+'</li>' for n in row.get('review_notes',[]))+'</ul>'+extra+'</article>')
 compare='<section><h2>Standing → rock contact → hands released</h2><p>One no-cut action in the authored plan; standing endpoint reused as the placement start. These three generated candidates still require exact background/root/anatomy/prop checks before a video proposal.</p><div class="triple">'+''.join(pic(next(r for r in rows if r.get('image_id')==iid),label) for iid,label in [('S02-L004-B01-I02','Shared standing hold'),('S02-L004-B02-I02','Crouch/contact'),('S02-L004-B02-I03','Hands released · notch/size mismatch flagged')])+'</div></section>'
 style='body{font:17px system-ui;background:#252821;color:#eee;max-width:1450px;margin:25px auto;padding:0 20px}a{color:#c7edab}article,section{background:#343a31;padding:18px;margin:24px 0;border-radius:10px}img{display:block;width:100%;height:auto}figure{margin:10px 0}figcaption,.status{color:#ffdb91;margin:8px 0}audio{width:100%;max-width:700px}.triple{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}li{margin:8px 0}body.native article>figure{overflow:auto}body.native article>figure img{width:auto;max-width:none}@media(max-width:750px){.triple{grid-template-columns:1fr}}'
 page='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>S01–S03 · acorn corrections r004</title><style>'+style+'</style></head><body><h1>S01–S03 · acorn continuity r004</h1><p><strong>Current display: 24 owner-retained candidates; 2 r005 corrections proposed, not generated. Existing r004 media remains visible below. No retries. Cost not exposed.</strong></p><p>Current size/setup reference is S02-L004 standing r004. S01 I03 must be whole before eating; S02 carries the tasted state. Historical r004 notes below remain visible. Generated release still has a notch/size mismatch. Exact background and anatomy remain unverified; no scene or video approval inferred.</p><label><input type="checkbox" id="native"> Native-pixel display (scroll)</label>'+compare+''.join(cards)+'<script>document.querySelector("#native").addEventListener("change",e=>document.body.classList.toggle("native",e.target.checked));document.querySelectorAll("audio").forEach(p=>p.addEventListener("play",()=>document.querySelectorAll("audio").forEach(q=>{if(q!==p)q.pause()})));</script></body></html>'
 (D/'review.html').write_text(page+'\n');write(D/'AUDIO_IMAGE_INDEX.json',{'schema':'feltwillow.current-scene-candidates.v1','new_candidates':5,'retained_candidates':sum(r['status']=='owner_retained_candidate' for r in rows),'pending_revisions':2,'images':rows,'sequence_start_reuse':{'S02-L004-B02-I01':'S02-L004-B01-I02'},'owner_scene_approvals':0})
 for name in ['s01_s03_performance_r002','s01_s03_corrections_r003']:
  target=D.parent/name/'review.html';backup=target.with_name('review_before_acorn_r004.html')
  if not backup.exists():backup.write_bytes(target.read_bytes())
  target.write_text(page+'\n')
 write(D/'VISUAL_OBSERVATIONS.json',{'scope':'Native displayed-image visual screening; no ratio measurements or hidden anatomy inferred','notes':notes,'prop_continuity':'not_passed; release notch and apparent scale differ','smooth_video_readiness':False})
 print(json.dumps({'new_candidates':5,'retained':21,'total_gallery_images':26}))
if __name__=='__main__':build()
