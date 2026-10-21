"""Read-only media verification and current gallery rendering; no generation."""
import hashlib,html,json,os
from pathlib import Path
import numpy as np
from PIL import Image
D=Path(__file__).resolve().parent;R=D.parents[4];S=R/'stories/lion_and_mouse_v7'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 latest=D.parent/'opening_milo_proportions_r006'
 if (latest/'EXECUTION.json').exists() and read(latest/'EXECUTION.json').get('completed')==1:
  import runpy
  runpy.run_path(str(latest/'build_review.py'),run_name='__main__');return
 op=read(D/'OPERATION.json');exe=read(D/'EXECUTION.json');auth=read(D/'AUTHORIZATION.json');assert exe['completed']==2 and sha(D/'OPERATION.json')==auth['operation_sha256']
 plan=read(S/'audio_visual_plan.json');lines={l['line_id']:l for l in plan['lines']};images={i['id']:i for l in plan['lines'] for b in l['beats'] for i in b['image_sequence']['images']}
 old=read(D.parent/'acorn_continuity_r004/AUDIO_IMAGE_INDEX.json')['images'];updates={q['image_id']:(q,o) for q,o in zip(op['requests'],exe['outputs'])};held={r['path']:r for r in read(D/'OWNER_DIRECTION.json')['retained_candidates']}
 notes={'S01-L004-B03-I03':['Whole orange-brown shell restored; no pale bitten patch visible. Visual observation only; comparative prop/anatomy measurements pending.','Intermediate pre-eating key; future I04 tasted endpoint remains planned without media.'], 'S02-L001-B01-I02':['Uses the stone/stream standing setup with upward head/gaze and the smaller reference acorn with a tasted patch.','Feet/root and torso look close to the standing reference; no measured anatomy/prop-scale pass. Exact background pixels differ (see test below).']}
 rows=[]
 for row in old:
  iid=row.get('image_id')
  if iid in updates:
   q,o=updates[iid];row={**o,'line_id':q['line_id'],'beat_id':q['beat_id'],'audio':q['audio'],'status':'candidate_pending_owner_review','review_notes':notes[iid],'owner_approval':None}
  else:
   row=dict(row);assert row['path'] in held;assert sha(R/row['path'])==held[row['path']]['sha256'];row['status']='owner_retained_candidate';row['retention_decision']=held[row['path']]
  assert sha(R/row['path'])==row['sha256'];rows.append(row)
 assert len(rows)==26
 # Native-resolution background gate uses a deliberately broad actor/head/tail
 # exclusion. Different pixels in the remaining scene disprove exact equality;
 # the rectangle is not a measured actor segmentation or root/anatomy score.
 base=R/op['requests'][1]['inputs'][0]['path'];out=R/op['requests'][1]['output']
 a=np.asarray(Image.open(base).convert('RGB'));b=np.asarray(Image.open(out).convert('RGB'));assert a.shape==b.shape
 mask=np.ones(a.shape[:2],bool);mask[:850,220:1010]=False
 delta=np.abs(a.astype(np.int16)-b.astype(np.int16));pixels=np.any(delta!=0,axis=2)
 bg={'reference':str(base.relative_to(R)),'candidate':str(out.relative_to(R)),'dimensions':[a.shape[1],a.shape[0]],'method':'native RGB equality outside broad actor exclusion x=[220,1010), y=[0,850); no alignment or resampling','compared_pixels':int(mask.sum()),'different_pixels':int((pixels&mask).sum()),'mean_absolute_channel_difference':float(delta[mask].mean()),'exact_background_pass':not bool(pixels[mask].any()),'root_and_anatomy_measurement':'pending'}
 write(D/'BACKGROUND_CHECK.json',bg)
 def url(p):return html.escape(os.path.relpath(R/p,D),quote=True)
 def pic(r,label):return '<figure><figcaption>'+html.escape(label)+'</figcaption><a href="'+url(r['path'])+'"><img loading="lazy" src="'+url(r['path'])+'"></a></figure>'
 cards=[]
 for row in rows:
  iid=row.get('image_id') or 'S01-L001 forest establishment';lid=row['line_id'];prior=''
  if iid in updates:
   q,o=updates[iid];source=q['inputs'][0] if iid.startswith('S01') else q['inputs'][1]
   prior='<details><summary>Previous candidate (preserved)</summary>'+pic(source,'Previous candidate, unchanged')+'</details>'
  cards.append('<article id="'+iid+'"><h2>'+iid+'</h2><p class="status">'+row['status']+'</p><p>'+html.escape(lines[lid]['text'])+'</p><audio controls preload="none" src="'+url(lines[lid]['audio']['wav'])+'"></audio>'+pic(row,'Current candidate · click for native PNG')+'<ul>'+''.join('<li>'+html.escape(n)+'</li>' for n in row.get('review_notes',[]))+'</ul>'+prior+'</article>')
 def row(iid):return next(r for r in rows if r.get('image_id')==iid)
 compare='<section><h2>Same S02 place: look up → standing → contact → release</h2><p>L001 and L004 share a physical setup. L002/L003 remain cutaways; only L004 is the no-cut placement action. Exact background check: '+('PASS' if bg['exact_background_pass'] else 'FAIL')+'; native mean channel difference '+format(bg['mean_absolute_channel_difference'],'.3f')+'. No actor-root/anatomy pass inferred. The retained release frame still has a flagged notch/scale difference.</p><div class="compare">'+''.join(pic(row(i),label) for i,label in [('S02-L001-B01-I02','NEW r005: looking up'),('S02-L004-B01-I02','Retained r004: standing setup reference'),('S02-L004-B02-I02','Retained r004: crouch/contact'),('S02-L004-B02-I03','Retained r004: release; prior prop flag remains')])+'</div></section>'
 style='body{font:17px system-ui;background:#252821;color:#eee;max-width:1450px;margin:25px auto;padding:0 20px}a{color:#c7edab}article,section{background:#343a31;padding:18px;margin:24px 0;border-radius:10px}img{display:block;width:100%;height:auto}figure{margin:10px 0}figcaption,.status{color:#ffdb91;margin:8px 0}audio{width:100%;max-width:700px}.compare{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}li{margin:8px 0}body.native article>figure{overflow:auto}body.native article>figure img{width:auto;max-width:none}@media(max-width:750px){.compare{grid-template-columns:1fr}}'
 page='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>S01–S03 · acorn setup r005</title><style>'+style+'</style></head><body><h1>S01–S03 · acorn setup r005</h1><p><strong>2 new r005 candidates saved; 24 other candidates retained. Two approved requests, no retries. Cost unknown.</strong></p><p>Whole acorn before eating in S01. Shared stone/stream setup and reference acorn in S02. New candidates await owner review. No scene/video approval inferred.</p><label><input type="checkbox" id="native"> Native-pixel display (scroll)</label>'+compare+''.join(cards)+'<script>document.querySelector("#native").addEventListener("change",e=>document.body.classList.toggle("native",e.target.checked));document.querySelectorAll("audio").forEach(p=>p.addEventListener("play",()=>document.querySelectorAll("audio").forEach(q=>{if(q!==p)q.pause()})));</script></body></html>'
 (D/'review.html').write_text(page+'\n');write(D/'AUDIO_IMAGE_INDEX.json',{'schema':'feltwillow.current-scene-candidates.v1','new_candidates':2,'retained_candidates':24,'images':rows,'sequence_start_reuse':{'S02-L004-B02-I01':'S02-L004-B01-I02'},'owner_scene_approvals':0})
 for name in ['s01_s03_performance_r002','s01_s03_corrections_r003']:
  p=D.parent/name/'review.html';backup=p.with_name('review_before_acorn_r005.html')
  if not backup.exists():backup.write_bytes(p.read_bytes())
  p.write_text(page+'\n')
 write(D/'VISUAL_OBSERVATIONS.json',{'scope':'Displayed full-size visual screening, not a measured anatomy pass','notes':notes,'exact_background':bg,'owner_review':'pending','video_ready':False})
 print(json.dumps({'new':2,'retained':24,'gallery':26,'exact_background_pass':bg['exact_background_pass'],'background_mae':bg['mean_absolute_channel_difference']}))
if __name__=='__main__':build()
