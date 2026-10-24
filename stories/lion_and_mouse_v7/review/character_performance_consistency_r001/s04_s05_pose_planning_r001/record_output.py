"""Journal one approved request/output; never submits image generation."""
import argparse
import datetime
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image

D=Path(__file__).resolve().parent
R=D.parents[4]
S=R/'stories/lion_and_mouse_v7'

def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inputs(index):
 op=read(D/'OPERATION.json');auth=read(D/'AUTHORIZATION.json')
 assert digest(D/'OPERATION.json')==auth['operation_sha256']
 q=op['requests'][index]
 for f in q['inputs']:assert digest(R/f['path'])==f['sha256']
 return op,q,auth

def start(index):
 op,q,auth=inputs(index);p=D/'EXECUTION.json'
 log=read(p) if p.exists() else {'operation_sha256':auth['operation_sha256'],'endpoint':op['endpoint'],'requested':16,'automatic_retries':0,'actual_cost':None,'attempts':{},'outputs':[],'completed':0}
 assert str(index) not in log['attempts'],'Already attempted; reconcile outcome instead of retrying'
 assert not (R/q['output']).exists()
 log['attempts'][str(index)]={'image_asset':q['asset_id']+':'+q['variant'],'status':'submitting_outcome_not_yet_recorded','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};write(p,log)
 print(json.dumps({'starting':index+1,'asset':q['asset_id'],'variant':q['variant']}))

def record(index,source):
 op,q,auth=inputs(index);source=Path(source);out=R/q['output'];side=R/q['sidecar'];log=read(D/'EXECUTION.json')
 assert log['attempts'][str(index)]['status']=='submitting_outcome_not_yet_recorded'
 assert not out.exists() and not side.exists()
 out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,out)
 with Image.open(out) as im:im.verify()
 with Image.open(out) as im:
  dims=list(im.size);alpha={'has_alpha':'A' in im.getbands(),'extrema':list(im.getchannel('A').getextrema()) if 'A' in im.getbands() else None}
 lib=read(S/'character_performance_library.json');asset=lib['assets'][q['asset_id']];v=asset['variants'][q['variant']];assert v['status']=='planned' and not v['file']
 (D/'receipts').mkdir(exist_ok=True);receipt_path=D/'receipts'/f'{index+1:03d}.json'
 creation={'method':'built-in image_gen.imagegen','prompt':q['arguments']['prompt'],'settings':{'transparent_background':True,'model':None,'seed':None},'inputs':q['inputs'],'actual_tool_arguments':q['arguments'],'endpoint':op['endpoint'],'operation_sha256':auth['operation_sha256'],'authorization':str((D/'AUTHORIZATION.json').relative_to(R)),'tool_output_path':str(source),'actual_cost':None,'request_id':None,'attempt':1}
 write(receipt_path,creation);creation['receipt']={'path':str(receipt_path.relative_to(R)),'sha256':digest(receipt_path)}
 status='candidate_pending_owner_review'
 data={'asset_id':asset['id'],'revision':asset['revision'],'image_revision':'r001','variant':q['variant'],'actor':'Milo','image_path':q['output'],'image_sha256':digest(out),'canonical':asset['canonical'],'dimensions':dims,'alpha':alpha,'creation':creation,'status':status,'owner_decision':None,'readiness_limitations':q['readiness_limitations'],'planned_audio_image_uses':q['uses']}
 write(side,data);v.update(status=status,file={'path':q['output'],'sha256':digest(out),'image_revision':'r001','dimensions':dims,'alpha':alpha,'sidecar':{'path':q['sidecar'],'sha256':digest(side)}},creation=creation,owner_decision=None)
 write(S/'character_performance_library.json',lib)
 row={'sequence':index+1,'asset_id':asset['id'],'variant':q['variant'],'path':q['output'],'sha256':digest(out),'sidecar':{'path':q['sidecar'],'sha256':digest(side)},'dimensions':dims,'alpha':alpha,'status':status};log['outputs'].append(row);log['completed']=len(log['outputs']);log['attempts'][str(index)]['status']='completed_candidate_saved';write(D/'EXECUTION.json',log);print(json.dumps({'completed':log['completed'],'of':16,'asset':asset['id']+':'+q['variant'],'has_alpha':alpha['has_alpha']}))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['start','record']);p.add_argument('index',type=int);p.add_argument('source',nargs='?');a=p.parse_args();start(a.index) if a.command=='start' else record(a.index,a.source)
