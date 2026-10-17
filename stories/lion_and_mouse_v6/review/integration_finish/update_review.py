#!/usr/bin/env python3
"""Refresh the current integration audit and local comparison navigation."""
import json,hashlib,html,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HOME=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 audit=json.loads((HOME/'audit.json').read_text());receipts={}
 for path in sorted((HOME/'frames').glob('*/receipt.json')):
  r=json.loads(path.read_text());assert sha(ROOT/r['source_path'])==r['source_sha256'];assert sha(ROOT/r['finished_path'])==r['finished_sha256'];receipts[r['source_sha256']]=r
 trial=HOME.parent/'integration_trial_s04_p03';r=json.loads((trial/'verification.json').read_text());trial_source=r['source']['sha256'];trial_output=r['results']['focused_generative']['path']
 for row in audit['frames']:
  match=receipts.get(row['source_sha256'])
  if match:
   row['candidate_path']=match['finished_path'];row['candidate_sha256']=match['finished_sha256'];row['candidate_receipt']=str((HOME/'frames'/match['id']/'receipt.json').relative_to(ROOT));row['status']='finished_candidate_pending_final_quality_and_sequence_acceptance';row['native_generation_inspected']=True
   if row['id']!=match['id']:row['identical_source_reuse']=match['id']
  if row['source_sha256']==trial_source:
   row['candidate_path']=trial_output;row['candidate_sha256']=sha(ROOT/trial_output);row['candidate_receipt']=str((trial/'verification.json').relative_to(ROOT));row['status']='owner_selected_C_trial_ready_to_adopt'
 audit['counts']={'screened':len(audit['frames']),'finish_candidates':sum(x['decision']=='finish' for x in audit['frames']),'retain':sum(x['decision']=='retain' for x in audit['frames']),'distinct_finish_sources':len({x['source_sha256'] for x in audit['frames'] if x['decision']=='finish'}),'prepared_slots':sum('candidate_path' in x for x in audit['frames']),'prepared_distinct_sources':len(receipts)+1,'adopted':0};(HOME/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
 parts=['<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V6 integration finishing progress</title><style>body{background:#191b1e;color:#eee;font:17px/1.5 system-ui;margin:25px}a{color:#9bd2ff}img{width:49%;height:auto}section{padding:15px;border-bottom:1px solid #666}summary{cursor:pointer}h1{font-size:28px}</style><h1>V6 integration finishing — in progress</h1><p>All 96 frames screened. Only frames with an integration defect are selected for finishing. Candidates below are not yet adopted; original keyframes remain active. Each pair shows original (left) / finish (right). New technical approvals are not inferred.</p><pre>'+html.escape(json.dumps(audit['counts'],indent=2))+'</pre>']
 for row in sorted(audit['frames'],key=lambda x:(x['scene'],x['id'])):
  parts.append('<section><strong>'+row['id']+'</strong> — '+row['decision']+' — '+row['status']+'<p>'+html.escape(row['reason'])+'</p>')
  if 'candidate_path' in row:
   orig=os.path.relpath(ROOT/row['source_path'],HOME);new=os.path.relpath(ROOT/row['candidate_path'],HOME)
   parts.append('<a href="'+orig+'"><img loading="lazy" src="'+orig+'" alt="'+row['id']+' original"></a><a href="'+new+'"><img loading="lazy" src="'+new+'" alt="'+row['id']+' integration finish"></a>')
  parts.append('</section>')
 (HOME/'owner_review.html').write_text('\n'.join(parts));print(json.dumps(audit['counts']))
if __name__=='__main__':main()
