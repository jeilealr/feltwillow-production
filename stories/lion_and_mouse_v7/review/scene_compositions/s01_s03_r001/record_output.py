"""Local receipts and immutable saves only; never submits image requests."""
from pathlib import Path
import sys,shutil,datetime,os,json
R=Path(__file__).resolve().parents[5];sys.path.insert(0,str(R))
from production import audio_visual_plan as a
from PIL import Image
F=Path(__file__).parent;S=R/'stories/lion_and_mouse_v7';op=a.read(F/'OPERATION.json');q=a.read(F/'QUEUE.json');n=int(sys.argv[2]);req=op['requests'][n-1];row=q['requests'][n-1]
assert a.digest(F/'OPERATION.json')==a.read(F/'AUTHORIZATION.json')['operation_sha256']
def queue_save():
 q['submitted_count']=sum(r['status']!='not_submitted' for r in q['requests']);q['generated_count']=sum(r['status']=='saved_candidate_pending_review' for r in q['requests']);q['status']='completed_pending_owner_review' if q['generated_count']==24 else 'authorized_in_progress';a.write(F/'QUEUE.json',q)
if sys.argv[1]=='begin':
 assert row['status']=='not_submitted'
 for ref in req['inputs']:assert a.digest(R/ref['path'])==ref['sha256']
 assert not (R/req['proposed_saved_output']).exists()
 row.update(status='submitted_awaiting_result',submitted_at=datetime.datetime.now(datetime.timezone.utc).isoformat());queue_save();print(json.dumps(req['arguments']))
elif sys.argv[1]=='save':
 assert row['status']=='submitted_awaiting_result'
 source=Path(sys.argv[3]);out=R/req['proposed_saved_output'];out.parent.mkdir(parents=True,exist_ok=True);assert not out.exists();shutil.copyfile(source,out)
 with Image.open(out) as im:dimensions=list(im.size);im.verify()
 row.update(status='saved_candidate_pending_review',path=req['proposed_saved_output'],sha256=a.digest(out),dimensions=dimensions,tool_default_saved_path=str(source),actual_cost=None)
 side={'schema':'feltwillow.audio-linked-scene-composition.v1','status':'candidate_pending_owner_review','story':op['story'],'line_id':req['audio_line'],'beat_id':req['beat_id'],'image_id':req['planned_image_id'],'location_view':req['location_view'],'background_continuity':req['background_continuity'],'audio':req['audio'],'image':dict(path=row['path'],sha256=row['sha256'],dimensions=dimensions),'generation':{'tool':'image_gen.imagegen','actual_arguments':req['arguments'],'inputs':req['inputs'],'operation_sha256':a.digest(F/'OPERATION.json'),'sequence':n,'default_saved_path':str(source),'model':None,'seed':None,'request_id':None,'estimated_cost':None,'actual_cost':None},'authorization':a.read(F/'AUTHORIZATION.json'),'owner_approval':None,'technical_review':{'status':'pending_visual_review','scope':'composition preview only, remaining action keys not fulfilled'}}
 a.write(R/req['proposed_sidecar'],side);row['sidecar']={'path':req['proposed_sidecar'],'sha256':a.digest(R/req['proposed_sidecar'])};queue_save();a.write(F/f'receipts/{n:03d}.json',{'request':req,'result':row})
 html=['<!doctype html><meta charset="utf-8"><title>S01–S03 scene review</title><style>body{font:18px system-ui;background:#20241d;color:#eee;max-width:1300px;margin:30px auto}img{width:100%;height:auto}figure{margin:40px 0}</style>',f"<h1>S01–S03: {q['generated_count']} / 24 scene compositions</h1><p>Full compositions, pending owner review. These previews do not complete every motion endpoint.</p>"]
 index=[]
 for rr in q['requests']:
  if rr['status']=='saved_candidate_pending_review':
   spec=op['requests'][rr['sequence']-1];html.append(f"<figure><h2>{spec['beat_id']} · {spec['speaker']}</h2><p>{spec['text']}</p><p>{Path(rr['path']).name}</p><img loading='lazy' src='{os.path.relpath(R/rr['path'],F)}' alt='{spec['beat_id']}'></figure>");index.append({'line_id':spec['audio_line'],'beat_id':spec['beat_id'],'image_id':spec['planned_image_id'],'audio_wav':spec['audio']['wav'],**rr})
 (F/'review.html').write_text('\n'.join(html));a.write(F/'AUDIO_IMAGE_INDEX.json',{'scope':'generated scene-composition previews, not selected key images','images':index});print(json.dumps({'saved':n,'completed':q['generated_count'],'path':row['path']}))
