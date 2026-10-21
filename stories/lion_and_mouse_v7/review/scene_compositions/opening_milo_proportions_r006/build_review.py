"""Render the single approved correction without changing original media."""
import hashlib,html,json,os,re
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[4]
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 op=read(D/'OPERATION.json');exe=read(D/'EXECUTION.json');auth=read(D/'AUTHORIZATION.json');assert exe['completed']==1 and sha(D/'OPERATION.json')==auth['operation_sha256'];q=op['requests'][0];o=exe['outputs'][0];assert sha(R/o['path'])==o['sha256']
 prior=D.parent/'acorn_setup_r005';index=read(prior/'AUDIO_IMAGE_INDEX.json');rows=[];unchanged=0
 notes=['More upright torso and readable short neck; light walking action retained. Visual observation, not certified anatomy compliance.','Projected head fraction, horizontal widths, cream-patch and paw ratios still need comparable-view landmark measurements.','Original PNG and sidecar preserved. New r006 candidate awaits owner review; no approval transfers from previous bytes.']
 for row in index['images']:
  assert sha(R/row['path'])==row['sha256']
  if row.get('image_id')==q['image_id']:row={**o,'line_id':q['line_id'],'beat_id':q['beat_id'],'audio':q['audio'],'status':'candidate_pending_owner_review','review_notes':notes,'owner_approval':None}
  else:unchanged+=1
  rows.append(row)
 assert unchanged==25 and len(rows)==26
 ledger_path=R/'stories/lion_and_mouse_v7/scene_image_selection.json'
 if ledger_path.exists():
  selected={r['path']:r for r in read(ledger_path)['images']}
  for row in rows:
   if row['path'] in selected and row['sha256']==selected[row['path']]['sha256']:
    row['status']='owner_selected_scene_image'
    row['owner_approval']={'ledger':str(ledger_path.relative_to(R)),'sha256':row['sha256'],'scope':'scene_image_use; technical observations retained'}
 page=(prior/'review.html').read_text();old=next(r for r in index['images'] if r.get('image_id')==q['image_id'])
 def url(p):return html.escape(os.path.relpath(R/p,D),quote=True)
 def pic(p,label):return '<figure><figcaption>'+html.escape(label)+'</figcaption><a href="'+url(p)+'"><img loading="lazy" src="'+url(p)+'"></a></figure>'
 block=re.search(r'<article id="'+q['image_id']+r'">.*?</article>',page,re.S);assert block
 body=block.group().replace(url(old['path']),url(q['output'])).replace('owner_retained_candidate','candidate_pending_owner_review')
 body=re.sub(r'<ul>.*?</ul>','<ul>'+''.join('<li>'+html.escape(n)+'</li>' for n in notes)+'</ul>',body,flags=re.S)
 body+='' # source comparison is in the dedicated section below
 page=page[:block.start()]+body+page[block.end():]
 compare='<section><h2>Opening Milo · before / new r006 / walking reference</h2><p>Compare torso length, neck transition, head/body balance and belly profile; independent cameras do not require equal pixel heights. No numerical measurement pass inferred.</p><div class="compare">'+pic(old['path'],'Previous r002 · preserved')+pic(q['output'],'NEW r006 · awaiting owner review')+pic(q['inputs'][3]['path'],'S01-L003 · owner-preferred walking comparison')+pic(q['inputs'][1]['path'],'Canonical identity · unchanged')+'</div></section>'
 page=page.replace('<title>S01–S03 · acorn setup r005</title>','<title>S01–S03 · opening Milo r006</title>').replace('<h1>S01–S03 · acorn setup r005</h1>','<h1>S01–S03 · opening Milo r006</h1>')
 page=page.replace('2 new r005 candidates saved; 24 other candidates retained. Two approved requests, no retries. Cost unknown.','1 new opening Milo r006 candidate; 25 other current images unchanged, including both r005 acorn corrections. One approved request, no retries. Cost unknown.')
 page=page.replace('<label><input type="checkbox" id="native">',compare+'<label><input type="checkbox" id="native">',1)
 if ledger_path.exists():
  page=page.replace('candidate_pending_owner_review','owner_selected_scene_image').replace('owner_retained_candidate','owner_selected_scene_image')
  page=page.replace('New candidates await owner review. No scene/video approval inferred.','All 26 current images are owner-selected for scene use. Existing technical observations remain; generated video is not approved.')
  page=page.replace('NEW r006 · awaiting owner review','r006 · owner selected').replace('New r006 candidate awaits owner review; no approval transfers from previous bytes.','Owner selected these exact r006 bytes for scene use; numerical anatomy measurement remains pending.')
 (D/'review.html').write_text(page);write(D/'AUDIO_IMAGE_INDEX.json',{'schema':index['schema'],'new_candidates':1,'other_candidates_unchanged':25,'images':rows,'sequence_start_reuse':index['sequence_start_reuse'],'owner_scene_approvals':sum(r['status']=='owner_selected_scene_image' for r in rows)})
 for name in ['s01_s03_performance_r002','s01_s03_corrections_r003']:
  p=D.parent/name/'review.html';p.write_text(page)
 write(D/'VISUAL_OBSERVATIONS.json',{'source':q['inputs'][0],'candidate':o,'assessment':'visually improved torso/neck readability; quantitative compliance not established','notes':notes,'camera':'camera_unknown; no physical distance inferred','numerical_anatomy_pass':False,'owner_decision':None})
 print(json.dumps({'new':1,'other_images_unchanged':25,'gallery':26}))
if __name__=='__main__':build()
