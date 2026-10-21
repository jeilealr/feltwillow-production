"""Build the completed candidate gallery from immutable operation and receipts."""
import hashlib,html,json,os
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[4]
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 latest=D.parent/'s01_s03_corrections_r003/build_review.py'
 if latest.is_file():
  import runpy
  return runpy.run_path(str(latest))['build']()
 op=read(D/'OPERATION.json');log=read(D/'EXECUTION.json');assert log['completed']==20
 before=D/'preflight.html'
 if not before.exists():before.write_bytes((D/'review.html').read_bytes())
 issues={
 'S01-L001-B01-I02':['confirmed_defect: pale corner symbol remains at bottom right despite exclusion prompt.'],
 'S01-L004-B03-I03':['needs_review: acorn appears larger relative to Milo than in the later S02-L004 hold. Camera and contact differ; no measured prop-scale pass.'],
 'S02-L001-B01-I02':['needs_review: compare acorn/head/hand proportions against the other acorn shots; no numerical prop-scale pass.'],
 'S02-L004-B01-I02':['suspected_defect: acorn is visibly smaller relative to the nearby head than in preceding acorn compositions; prop consistency is not passed.'],
 'S02-L004-B02-I03':['confirmed_defect: hand still touches the acorn cap, so the intended fully released/empty-hands state is not clearly depicted.'],
 'S03-L001-B01-I02':['needs_review: hand-to-chin performance follows scene base rather than exact arms-down pose reference.'],
 'S03-L002-B01-I02':['needs_review: hand-to-chin performance follows scene base rather than exact arms-down pose reference.']}
 corrections=read(D/"OWNER_CORRECTIONS.json") if (D/"OWNER_CORRECTIONS.json").exists() else {}
 rows=[];cards=[]
 def url(path):return html.escape(os.path.relpath(R/path,D),quote=True)
 def fig(path,title):return '<figure><figcaption>'+html.escape(title)+'</figcaption><a href="'+url(path)+'"><img loading="lazy" src="'+url(path)+'"></a></figure>'
 mapping={q['image_id']:q for q in op['requests']+op['held']+op['retained']}
 ordered=read(D/'SOURCE_REVIEW_INDEX.json')['rows']
 for source in ordered:
  q=mapping[source['image_id']];out=next((r for r in log['outputs'] if r['image_id']==q['image_id']),None)
  correction=corrections.get('notes',{}).get(q['image_id'])
  notes=([correction] if correction else [])+issues.get(q['image_id'],[])+(['needs_review: anatomy/width ratios, pose fidelity and contacts have not received matched-view measurement or owner scene approval.'] if out else [])
  if out:
   assert sha(R/out['path'])==out['sha256'];assert sha(R/out['sidecar']['path'])==out['sidecar']['sha256']
   row={**out,'line_id':q['line_id'],'beat_id':q['beat_id'],'audio':q['audio'],'performance':q['performance'],'observations':notes,'owner_approval':None}
   primary=fig(out['path'],'NEW r002 · candidate pending your review')
   compare='<details><summary>Original scene and selected pose reference</summary><div class="compare">'+fig(q['edit_base']['path'],'Original r001 · retained unchanged')+fig(q['performance']['path'],'Owner-selected performance reference')+'</div></details>'
   status='Owner requested correction · current pixels unchanged' if correction else 'New candidate · pending owner review'
  else:
   row={'image_id':q['image_id'],'line_id':q['line_id'],'status':q['status'],'path':q['edit_base']['path'],'sha256':q['edit_base']['sha256'],'reason':q['reason']};primary=fig(row['path'],'Existing r001 · unchanged');compare='';status=q['status'];notes=[q['reason']]
  rows.append(row)
  cards.append('<article id="'+q['image_id']+'"><h2>'+q['image_id']+'</h2><p class="status">'+html.escape(status)+'</p><p>'+html.escape(q['text'])+'</p><audio controls preload="none" src="'+url(q['audio']['wav'])+'"></audio>'+primary+'<ul>'+''.join('<li>'+html.escape(n)+'</li>' for n in notes)+'</ul>'+compare+'</article>')
 write(D/'AUDIO_IMAGE_INDEX.json',{'schema':'feltwillow.audio-scene-review-index.v1','operation_sha256':sha(D/'OPERATION.json'),'generated_candidates':20,'held':3,'retained':1,'images':rows})
 style='body{font:17px system-ui;background:#252821;color:#eee;margin:25px auto;padding:0 20px;max-width:1450px}a{color:#c7edab}article{background:#343a31;padding:18px;margin:25px 0;border-radius:10px}figure{margin:12px 0}figcaption{margin:8px 0;color:#ffdb91}img{display:block;width:100%;height:auto}audio{width:100%;max-width:700px}.compare{display:grid;grid-template-columns:2fr 1fr;gap:20px}.compare img{max-height:650px;object-fit:contain}.status{color:#ffdb91}summary{cursor:pointer}li{margin:8px 0}body.native figure{overflow:auto}body.native article>figure img{width:auto;max-width:none}@media(max-width:700px){.compare{grid-template-columns:1fr}}'
 page='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>S01–S03 Milo scene candidates r002</title><style>'+style+'</style></head><body><h1>S01–S03 · Milo scene candidates r002</h1><p><strong>20 new candidates generated and saved · 3 fixed-fork shots held · 1 environment-only shot retained.</strong> Exactly 20 approved requests, no retries. Actual cost not exposed.</p><p><strong>Latest owner corrections are recorded on the affected cards; no correction images have been generated yet. S03-L001–L008 now form one stationary fork setup; S02-L004 is one background setup; L009 uses L010 portrait-body framing.</strong></p><p>New candidates appear first in each card. Open the comparison panel for the original and selected Milo pose. Click an image for its native PNG. These are representative compositions, not complete endpoint sequences or approved production images.</p><p>Review flags include acorn-size variation, hand still touching the released acorn, and a retained corner symbol on the first image. Anatomy ratios remain unmeasured in these composed views. No automatic repair or approval.</p><p><a href="../../character_performance_consistency_r001/pose_library/review.html">Milo poses and canonical measurements</a> · <a href="#S02-L004-B02-I03">Acorn release review</a></p><label><input type="checkbox" id="native"> Native-pixel display (scroll)</label>'+''.join(cards)+'<script>document.querySelector("#native").addEventListener("change",e=>document.body.classList.toggle("native",e.target.checked));document.querySelectorAll("audio").forEach(p=>p.addEventListener("play",()=>document.querySelectorAll("audio").forEach(q=>{if(q!==p)q.pause()})));</script></body></html>'
 (D/'review.html').write_text(page+'\n')
 write(D/'VISUAL_OBSERVATIONS.json',{'scope':'Advisory visual observations from displayed full compositions; no measured anatomy pass','issues':issues,'owner_scene_decisions':0})
 print(json.dumps({'generated_candidates':20,'held':3,'retained':1,'index_rows':len(rows)}))
if __name__=='__main__':build()
