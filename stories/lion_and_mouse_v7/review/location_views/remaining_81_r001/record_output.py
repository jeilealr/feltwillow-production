"""CPU-only receipt/save helper for the explicitly approved operation; no API calls."""
from pathlib import Path
import sys,json,shutil,datetime,os
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from production import audio_visual_plan as a
from PIL import Image
F=Path(__file__).parent;S=ROOT/'stories/lion_and_mouse_v7'
# This file sits one level deeper than story/history migration helpers.
if not (ROOT/'production').is_dir():
 ROOT=Path(__file__).resolve().parents[6];sys.path.insert(0,str(ROOT));S=ROOT/'stories/lion_and_mouse_v7'
op=a.read(F/'OPERATION.json');queue=a.read(F/'QUEUE.json');n=int(sys.argv[2]);req=op['requests'][n-1];row=queue['requests'][n-1]
assert a.digest(F/'OPERATION.json')==a.read(F/'AUTHORIZATION.json')['operation_sha256']
def save_queue():
 queue['submitted_count']=sum(r['status']!='not_submitted' for r in queue['requests'])
 queue['generated_count']=sum(r['status']=='saved_candidate_pending_review' for r in queue['requests'])
 queue['status']='all_81_saved_pending_review' if queue['generated_count']==81 else 'authorized_in_progress'
 a.write(F/'QUEUE.json',queue)
if sys.argv[1]=='begin':
 if queue.get('generation_hold'):raise SystemExit('Generation held for camera-framing review; no further submissions authorized by this helper until reconciled.')
 assert row['status']=='not_submitted',row
 for ref in req['inputs']:assert a.digest(ROOT/ref['path'])==ref['sha256']
 for ref in op['approved_views_to_preserve']:assert a.digest(ROOT/ref['path'])==ref['sha256']
 assert not (ROOT/req['proposed_saved_output']).exists()
 row.update(status='submitted_awaiting_tool',submitted_at=datetime.datetime.now(datetime.timezone.utc).isoformat());save_queue()
 print(json.dumps(req['arguments']))
elif sys.argv[1]=='save':
 assert row['status']=='submitted_awaiting_tool'
 source=Path(sys.argv[3]);target=ROOT/req['proposed_saved_output'];target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();shutil.copyfile(source,target)
 with Image.open(target) as im:size=list(im.size);im.verify()
 sha=a.digest(target)
 side={'schema':'feltwillow.audio-linked-image.v1','story':op['story'],'status':'candidate_pending_owner_review','location_view_id':req['id'],'primary_beat_id':req['primary_beat_id'],'used_by_beats':req['purpose_beats'],'audio_links':req['audio_links'],'image':{'path':req['proposed_saved_output'],'sha256':sha,'dimensions':size,'image_revision':1,'role':'location','subject':req['subject']},'generation':{'tool':'image_gen.imagegen','model':'tool-selected; not exposed','actual_arguments':req['arguments'],'inputs':req['inputs'],'tool_default_saved_path':str(source),'request_id':None,'seed':None,'estimated_cost':None,'actual_cost':None,'operation':'stories/lion_and_mouse_v7/review/location_views/remaining_81_r001/OPERATION.json','operation_sha256':a.digest(F/'OPERATION.json'),'sequence':n},'authorization':a.read(F/'AUTHORIZATION.json'),'owner_approval':None,'technical_review':{'status':'pending_assistant_visual_inspection','limitations':['Not a measured geography/scale proof. Final character support, occlusion, identity and action staging await scene-key-image review.']}}
 sidepath=ROOT/req['proposed_sidecar'];a.write(sidepath,side)
 candidate={'path':req['proposed_saved_output'],'sha256':sha,'primary_beat_id':req['primary_beat_id'],'subject':req['subject'],'image_revision':1,'status':'candidate_pending_owner_review','sidecar':{'path':req['proposed_sidecar'],'sha256':a.digest(sidepath)},'audio_links':req['audio_links'],'owner_approval':None}
 locs=a.read(S/'location_library.json');view=locs['views'][req['id']];assert view['status']=='planned';assert not view.get('candidates');view['candidates']=[candidate];view['generation_status']='candidate_available_pending_owner_review';a.write(S/'location_library.json',locs)
 row.update(status='saved_candidate_pending_review',saved_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),path=req['proposed_saved_output'],sha256=sha,dimensions=size,sidecar=candidate['sidecar'],tool_default_saved_path=str(source));save_queue()
 a.write(F/f'receipts/{n:03d}.json',{'request':req,'result':row,'actual_cost':None,'owner_approval':None})
 plan=a.read(S/'audio_visual_plan.json');a.derive(S,plan,a.read(S/'character_library.json'),locs)
 html=['<!doctype html><meta charset="utf-8"><title>81 location views</title><style>body{font:18px system-ui;background:#20241d;color:#eee;max-width:1200px;margin:30px auto}img{width:100%;height:auto}figure{margin:30px 0}</style>',f"<h1>{queue['generated_count']} / 81 location views saved</h1><p>All new images are candidates pending owner review. Audio/beat IDs appear in every filename.</p>"]
 for r in queue['requests']:
  if r['status']=='saved_candidate_pending_review':html.append(f"<figure><h2>{r['sequence']:02d} · {Path(r['path']).name}</h2><img loading='lazy' src='{os.path.relpath(ROOT/r['path'],F)}' alt='{r['id']}'></figure>")
 (F/'review.html').write_text('\n'.join(html))
 print(json.dumps({'saved':n,'completed':queue['generated_count'],'path':req['proposed_saved_output'],'sha256':sha,'dimensions':size}))
else:raise SystemExit('begin/save only; never generates or retries')
