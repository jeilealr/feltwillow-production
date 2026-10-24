"""Save only the owner-authorized raw image outputs; never submits calls."""
import argparse
import copy
import datetime
import hashlib
import json
from pathlib import Path
import shutil

from PIL import Image

D=Path(__file__).resolve().parent
R=D.parents[4]
S=R/'stories/lion_and_mouse_v7'

def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':str(p.relative_to(R)),'sha256':digest(p)}

def inputs(index):
    operation=read(D/'OPERATION.json');authorization=read(D/'AUTHORIZATION.json')
    assert digest(D/'OPERATION.json')==authorization['operation_sha256']
    q=operation['requests'][index]
    for f in q['inputs']:assert digest(R/f['path'])==f['sha256']
    return operation,authorization,q

def start(index):
    _,_,q=inputs(index);log=read(D/'EXECUTION.json')
    assert str(index) not in log['attempts'];assert not (R/q['output']).exists()
    log['attempts'][str(index)]={'status':'submitting_outcome_not_yet_recorded','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    write(D/'EXECUTION.json',log);print('Starting',index+1,q['requirement_id'])

def record(index,source):
    op,auth,q=inputs(index);log=read(D/'EXECUTION.json')
    assert log['attempts'][str(index)]['status']=='submitting_outcome_not_yet_recorded'
    out=R/q['output'];side=R/q['sidecar'];assert not out.exists() and not side.exists()
    out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,out)
    with Image.open(out) as im:
        im.load();dims=list(im.size);alpha={'has_alpha':'A' in im.getbands(),'extrema':list(im.getchannel('A').getextrema()) if 'A' in im.getbands() else None}
    lib=read(S/'character_performance_library.json')
    normalized=[]
    for f in q['inputs']:
        role=f['role']
        if role in {'existing_portrait_geometry_reference','selected_portrait_edit_base'}:mapped,authority='portrait_base','portrait_geometry_only'
        elif role.startswith('canonical_identity'):mapped,authority='canonical_identity','identity_anatomy_material_palette'
        elif role.startswith('canonical_measurement'):mapped,authority='canonical_measurement_annotation','visible_surface_measurements_only; never render markings'
        else:mapped,authority=role,f['authority']
        normalized.append(dict(f,role=mapped,authority=authority,operation_role=role,operation_authority=f['authority']))
    creation={'method':'built-in image_gen.imagegen','prompt':q['tool_arguments']['prompt'],
              'settings':{'transparent_background':True,'model':None,'seed':None},'inputs':normalized,
              'actual_tool_arguments':q['tool_arguments'],'endpoint':op['endpoint'],
              'operation_sha256':auth['operation_sha256'],'authorization':str((D/'AUTHORIZATION.json').relative_to(R)),
              'tool_output_path':str(source),'actual_cost':None,'request_id':None,'attempt':1}
    (D/'receipts').mkdir(exist_ok=True);receipt=D/'receipts'/f'{index+1:03d}.json'
    write(receipt,creation);creation['receipt']=ref(receipt)
    file={'path':q['output'],'sha256':digest(out),'image_revision':'r001','dimensions':dims,'alpha':alpha}
    if len(q['actors'])==2:
        joint=lib['joint_performance_requirements'][q['requirement_id']];v=joint['variants'][q['variant']]
        data={'schema':'feltwillow.joint-performance-candidate.v1','requirement_id':q['requirement_id'],'revision':'r001',
              'variant':q['variant'],'actors':q['actors'],'canonical':joint['canonical'],'image_path':q['output'],
              'image_sha256':digest(out),'dimensions':dims,'alpha':alpha,'creation':creation,
              'status':'candidate_pending_owner_review','owner_decision':None,'audio_image_uses':q['audio_image_uses'],
              'actor_bindings':v['actor_bindings'],'state_ref':v['state_ref'],
              'readiness_limitations':['Joint depicted anatomy, relative scale, screen axis, support and alpha need owner review.',
                                      'One paired PNG is not two approved per-actor performance assets; individual required assets remain planned.',
                                      'Not a scene or empty background plate; S05 old-Leo removal/clean-plate gate remains.']}
        write(side,data);file['sidecar']=ref(side)
        v.update(status='candidate_pending_owner_review',file=file,creation=creation,owner_decision=None)
    else:
        actor=q['actors'][0];asset=lib['assets'][q['requirement_id']];v=asset['variants'][q['variant']]
        assert v['status']=='planned' and v['file'] is None
        data={'asset_id':asset['id'],'revision':asset['revision'],'image_revision':'r001','variant':q['variant'],'actor':actor,
              'canonical':asset['canonical'],'image_path':q['output'],'image_sha256':digest(out),'dimensions':dims,'alpha':alpha,
              'creation':creation,'status':'candidate_pending_owner_review','owner_decision':None,
              'planned_audio_image_uses':q['audio_image_uses'],'readiness_limitations':['New view/acting/body/crop/alpha needs owner review; no measured anatomy or scene approval inferred.']}
        write(side,data);file['sidecar']=ref(side)
        v.update(status='candidate_pending_owner_review',file=file,creation=creation,owner_decision=None)
        # Candidate hashes identify parent bytes only; never transfer approval.
        for a in lib['assets'].values():
            for parent in a['parents']:
                if parent['id']==asset['id'] and parent['variant']==q['variant']:parent['sha256']=file['sha256']
    write(S/'character_performance_library.json',lib)
    row=dict(file,requirement_id=q['requirement_id'],variant=q['variant'],actors=q['actors'],
             audio_image_uses=q['audio_image_uses'],receipt=ref(receipt),status='candidate_pending_owner_review')
    log['outputs'].append(row);log['completed']=len(log['outputs']);log['attempts'][str(index)]['status']='completed_candidate_saved'
    write(D/'EXECUTION.json',log);print('Saved',index+1,'of',len(op['requests']),q['requirement_id'],dims,alpha)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['start','record']);p.add_argument('index',type=int);p.add_argument('source',nargs='?');a=p.parse_args()
    start(a.index) if a.command=='start' else record(a.index,a.source)
