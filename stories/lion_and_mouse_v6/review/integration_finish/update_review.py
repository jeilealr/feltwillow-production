#!/usr/bin/env python3
"""Render the comparison page without changing audit decisions or selection."""
import html,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HOME=Path(__file__).resolve().parent
def main():
 audit=json.loads((HOME/'audit.json').read_text());done=audit['status']=='complete'
 parts=['<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V6 focused integration</title><style>body{background:#191b1e;color:#eee;font:17px/1.5 system-ui;margin:25px}a{color:#9bd2ff}img{width:49%;height:auto}section{padding:15px;border-bottom:1px solid #666}h1{font-size:28px}</style><h1>V6 focused integration — '+('adopted' if done else 'in progress')+'</h1><p>All 96 frames screened. Original left / finish right. The owner preferred C and authorized the rollout; other finishes were inspected and selected by the agent under that authorization. This is separate from individual owner review and production approval.</p><pre>'+html.escape(json.dumps(audit['counts'],indent=2))+'</pre>']
 for row in sorted(audit['frames'],key=lambda x:(x['scene'],x['id'])):
  parts.append('<section><strong>'+row['id']+'</strong> — '+row['decision']+' — '+row['status']+'<p>'+html.escape(row['reason'])+'</p>')
  if 'candidate_path' in row:
   orig=os.path.relpath(ROOT/row['source_path'],HOME);new=os.path.relpath(ROOT/row.get('active_path',row['candidate_path']),HOME)
   parts.append('<a href="'+orig+'"><img loading="lazy" src="'+orig+'" alt="'+row['id']+' original"></a><a href="'+new+'"><img loading="lazy" src="'+new+'" alt="'+row['id']+' finish'+(' trial not selected' if row['decision']=='retain' else '')+'"></a>')
  parts.append('</section>')
 (HOME/'owner_review.html').write_text('\n'.join(parts))
 print(json.dumps(audit['counts']))
if __name__=='__main__':main()
