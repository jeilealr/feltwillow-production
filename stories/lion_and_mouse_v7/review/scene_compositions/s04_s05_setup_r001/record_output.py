"""Journal approved scene requests and preserve raw output; never submits calls."""
import argparse,datetime,hashlib,json,shutil
from pathlib import Path
from PIL import Image
D=Path(__file__).resolve().parent
R=D.parents[4]
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inputs(i):
 op=read(D/'OPERATION.json');auth=read(D/'AUTHORIZATION.json');assert digest(D/'OPERATION.json')==auth['operation_sha256'];q=op['requests'][i]
 for f in q['inputs']:assert digest(R/f['path'])==f['sha256']
 for k,h in [('wav','sha256'),('metadata','metadata_sha256')]:assert digest(R/q['audio'][k])==q['audio'][h]
 return op,q,auth
def start(i):
 op,q,auth=inputs(i);p=D/'EXECUTION.json';log=read(p) if p.exists() else {'operation_sha256':auth['operation_sha256'],'endpoint':op['endpoint'],'requested':7,'automatic_retries':0,'actual_cost':None,'attempts':{},'outputs':[],'completed':0}
 assert str(i) not in log['attempts'],'Already attempted; reconcile instead of retrying';assert not (R/q['output']).exists();assert not (R/q['sidecar']).exists()
 log['attempts'][str(i)]={'image_id':q['image_id'],'status':'submitting_outcome_not_yet_recorded','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};write(p,log);print('Starting',i+1,q['image_id'])
def record(i,source):
 op,q,auth=inputs(i);log=read(D/'EXECUTION.json');assert log['attempts'][str(i)]['status']=='submitting_outcome_not_yet_recorded';out=R/q['output'];side=R/q['sidecar'];assert not out.exists() and not side.exists();out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,out)
 with Image.open(out) as im:im.verify()
 with Image.open(out) as im:dimensions=list(im.size);mode=im.mode
 receipt={'schema':'feltwillow.scene-performance-candidate.v1','image_id':q['image_id'],'line_id':q['line_id'],'beat_id':q['beat_id'],'path':q['output'],'sha256':digest(out),'dimensions':dimensions,'mode':mode,'status':'candidate_pending_owner_review','audio':q['audio'],'performance':q['performance_bindings'],'world_state':q['world_state'],'state_id':q['state_id'],'events_before':q['events_before'],'background_continuity':q['background_continuity'],'continuity_group':q['continuity_group'],'inputs':q['inputs'],'creation':{'endpoint':op['endpoint'],'arguments':q['tool_arguments'],'operation':str((D/'OPERATION.json').relative_to(R)),'operation_sha256':auth['operation_sha256'],'authorization':str((D/'AUTHORIZATION.json').relative_to(R)),'tool_output_path':str(source),'model':None,'seed':None,'request_id':None,'actual_cost':None,'attempt':1},'technical_review':'pending_visual_review','owner_decision':None,'production_readiness':False,'readiness_limitations':['Scene candidate only; anatomy/acting/support/contact/scale must be reviewed. No measured camera or exact-background continuity pass. Missing downstream performance variants remain held.']}
 write(side,receipt);(D/'receipts').mkdir(exist_ok=True);receipt_path=D/'receipts'/f'{i+1:03d}.json';write(receipt_path,receipt)
 log['outputs'].append({'sequence':i+1,'image_id':q['image_id'],'path':q['output'],'sha256':digest(out),'sidecar':{'path':q['sidecar'],'sha256':digest(side)},'receipt':{'path':str(receipt_path.relative_to(R)),'sha256':digest(receipt_path)},'dimensions':dimensions,'status':'candidate_pending_owner_review'});log['completed']=len(log['outputs']);log['attempts'][str(i)]['status']='completed_candidate_saved';write(D/'EXECUTION.json',log);print('Saved',q['image_id'],log['completed'],'of 7')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['start','record']);p.add_argument('index',type=int);p.add_argument('source',nargs='?');a=p.parse_args();start(a.index) if a.command=='start' else record(a.index,a.source)
