"""Persist an already-returned authorized output; never submits generation."""
import argparse,datetime,hashlib,json,shutil
from pathlib import Path
from PIL import Image
D=Path(__file__).resolve().parent;R=D.parents[4]
def read(p):return json.loads(p.read_text())
def write(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def inputs(i):
 op=read(D/'OPERATION.json');a=read(D/'AUTHORIZATION.json');assert sha(D/'OPERATION.json')==a['operation_sha256'];q=op['requests'][i]
 for f in q['inputs']:assert sha(R/f['path'])==f['sha256']
 return op,a,q

def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=['start','record']);p.add_argument('index',type=int);p.add_argument('source',nargs='?');args=p.parse_args();op,a,q=inputs(args.index);e=read(D/'EXECUTION.json');k=str(args.index)
 if args.command=='start':
  assert k not in e['attempts'];e['attempts'][k]={'status':'submitting_outcome_not_yet_recorded','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};write(D/'EXECUTION.json',e);return
 assert e['attempts'][k]['status']=='submitting_outcome_not_yet_recorded';raw=R/q['output'];assert not raw.exists();shutil.copy2(args.source,raw)
 with Image.open(raw) as im:im.load();dims=list(im.size);mode=im.mode
 receipt=D/'receipts'/f'{args.index+1:03d}_generation.json';receipt.parent.mkdir(exist_ok=True)
 write(receipt,{'endpoint':op['endpoint'],'tool_arguments':q['tool_arguments'],'inputs':q['inputs'],'operation_sha256':a['operation_sha256'],'authorization':ref(D/'AUTHORIZATION.json'),'tool_output_path':args.source,'actual_cost':None,'request_id':None,'seed':None,'attempt':1})
 row=dict(ref(raw),image_id=q['image_id'],dimensions=dims,mode=mode,receipt=ref(receipt),status='raw_output_saved_pending_visual_and_protected_composition')
 write(raw.with_suffix('.json'),row);row['sidecar']=ref(raw.with_suffix('.json'));e['outputs'].append(row);e['completed']=len(e['outputs']);e['attempts'][k]['status']='completed_raw_candidate_saved';write(D/'EXECUTION.json',e);print('Saved',args.index+1,'of',len(op['requests']),dims)
if __name__=='__main__':main()
