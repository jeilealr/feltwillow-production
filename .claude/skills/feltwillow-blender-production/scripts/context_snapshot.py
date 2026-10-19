#!/usr/bin/env python3
"""Read selected repository metadata and hashes; never dump credentials or files."""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from pathlib import Path
from fw_contracts import load_json, safe_path, sha256_file

def git(root:Path,*args:str):
    try:
        r=subprocess.run(['git','-C',str(root),*args],capture_output=True,text=True,timeout=15,check=False)
        return r.stdout.strip() if r.returncode==0 else None
    except (OSError,subprocess.TimeoutExpired):
        return None

def collect(root:Path,story:str) -> dict:
    root=Path(root).resolve()
    if not root.is_dir() or not re.fullmatch(r'[a-z0-9][a-z0-9_-]*',story):
        raise ValueError('Existing root and simple story slug required')
    names=['AGENTS.md','CLAUDE.md','README.md','blender/README.md',
           '.claude/skills/consistent-image-prompts/SKILL.md',
           '.claude/skills/audio-chained-coverage/SKILL.md']
    names += [f'stories/{story}/{n}' for n in (
        'README.md','visual_bible.json','staging_plan.json','keyframe_plan.json',
        'owner_visual_acceptance.json','keyframe_visual_reviews.json','audio_manifest.json',
        'video_boundary_plan.json','pose_reference_plan.json')]
    records=[]; documents={}
    for name in names:
        try:
            path=safe_path(root,name)
            rec={'path':name,'exists':path.is_file()}
            if path.is_file():
                rec['sha256']=sha256_file(path)
                if path.suffix=='.json':
                    try:
                        documents[path.name]=load_json(path)
                    except (ValueError,OSError) as exc:
                        rec['parse_error']=str(exc)
            records.append(rec)
        except (ValueError,OSError) as exc:
            records.append({'path':name,'error':str(exc)})
    bible=documents.get('visual_bible.json',{})
    plan=documents.get('keyframe_plan.json',{})
    bible=bible if isinstance(bible,dict) else {}
    plan=plan if isinstance(plan,dict) else {}
    chars=[]
    for actor,item in bible.get('characters',{}).items() if isinstance(bible.get('characters'),dict) else []:
        if not isinstance(item,dict):continue
        entry={'actor':actor,'canonical':item.get('canonical'),'declared_status':item.get('status')}
        try:
            path=safe_path(root,item.get('canonical'))
            entry['canonical_exists']=path.is_file()
            if path.is_file():entry['actual_sha256']=sha256_file(path)
        except (ValueError,OSError) as exc:entry['error']=str(exc)
        chars.append(entry)
    rows=plan.get('images',[])
    return {'schema':'feltwillow.blender.context-snapshot.v1','story':story,
            'git':{'branch':git(root,'branch','--show-current'),'head':git(root,'rev-parse','HEAD'),
                   'status_porcelain':git(root,'status','--porcelain')},
            'local_blender_directory_exists':(root/'blender').is_dir(),
            'files':records,'characters':chars,'pipeline':bible.get('pipeline'),
            'keyframe_count':len(rows) if isinstance(rows,list) else None,
            'owner_acceptance_ledger_present':'owner_visual_acceptance.json' in documents,
            'warning':'Presence, status text and counts do not establish approval. Read current owner scopes and technical evidence. No Blender assets or appearance inspected.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True);p.add_argument('--story',required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    try:
        result=collect(a.root,a.story)
        a.out.parent.mkdir(parents=True,exist_ok=True)
        with a.out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
        print(a.out)
    except (ValueError,OSError) as e:p.error(str(e))
if __name__=='__main__':main()
