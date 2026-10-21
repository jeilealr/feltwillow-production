"""Record one approved built-in output; never submits generation requests."""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image
D=Path(__file__).resolve().parent
R=D.parents[4]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def record(index,source):
 op=json.loads((D/'OPERATION.json').read_text());auth=json.loads((D/'AUTHORIZATION.json').read_text());assert digest(D/'OPERATION.json')==auth['operation_sha256']
 q=op['requests'][index];source=Path(source);out=R/q['output'];side=R/q['sidecar'];assert not out.exists() and not side.exists()
 for f in q['inputs']:assert digest(R/f['path'])==f['sha256']
 out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,out)
 with Image.open(out) as im:im.verify()
 with Image.open(out) as im:dimensions=list(im.size);mode=im.mode
 receipt={'schema':'feltwillow.scene-performance-candidate.v1','image_id':q['image_id'],'line_id':q['line_id'],'beat_id':q['beat_id'],'path':q['output'],'sha256':digest(out),'dimensions':dimensions,'mode':mode,'status':'candidate_pending_owner_review','audio':q['audio'],'performance':q.get('performance'),'expression_requirement':q.get('expression_requirement'),'world_state':q.get('world_state'),'inputs':q['inputs'],'creation':{'endpoint':op['endpoint'],'arguments':q['arguments'],'operation':str((D/'OPERATION.json').relative_to(R)),'operation_sha256':auth['operation_sha256'],'authorization':str((D/'AUTHORIZATION.json').relative_to(R)),'tool_output_path':str(source),'model':None,'seed':None,'request_id':None,'actual_cost':None,'attempt':1},'technical_review':'pending_visual_review','owner_decision':None,'production_readiness':False,'readiness_limitations':q.get('production_readiness_blockers',['Exact background/anatomy/acorn size/damage/contact review pending'])}
 write(side,receipt);(D/'receipts').mkdir(exist_ok=True);write(D/'receipts'/f'{index+1:03d}.json',receipt)
 p=D/'EXECUTION.json';log=json.loads(p.read_text()) if p.exists() else {'operation_sha256':auth['operation_sha256'],'endpoint':op['endpoint'],'requested':1,'automatic_retries':0,'actual_cost':None,'outputs':[]}
 log['outputs'].append({'sequence':index+1,'image_id':q['image_id'],'path':q['output'],'sha256':digest(out),'sidecar':{'path':q['sidecar'],'sha256':digest(side)},'dimensions':dimensions,'status':'candidate_pending_owner_review'});log['completed']=len(log['outputs']);write(p,log);print(json.dumps({'saved':q['output'],'completed':log['completed']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('index',type=int);p.add_argument('source');a=p.parse_args();record(a.index,a.source)
