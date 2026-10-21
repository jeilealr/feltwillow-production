"""CPU-only scene revision proposal. Never authorizes or submits a request."""
import copy
import html
import json
import os
from pathlib import Path
import re
import sys

R=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(R))
from production import character_performance as cp

D=Path(__file__).parent
S=D.parents[2]


def build():
    if (D/"AUTHORIZATION.json").exists():
        raise RuntimeError("Operation already authorized; preserve exact approved operation bytes. Use build_review.py for gallery updates.")
    folder,plan,chars,locs,lib=cp.load(R,'lion_and_mouse_v7')
    errors=cp.validate(lib,plan,chars,R,folder=folder)
    if errors:raise ValueError('\n'.join(errors))
    old=D.parent/'s01_s03_r001'
    index=cp.av.read(old/'AUDIO_IMAGE_INDEX.json')
    specs={q['planned_image_id']:q for q in cp.av.read(old/'OPERATION.json')['requests']}
    lookup={im['id']:(line,beat,im) for line in plan['lines'] for beat in line['beats'] for im in beat['image_sequence']['images']}
    requests=[];held=[];retained=[];rows=[]
    canonical=cp.canonical_record(chars,'Milo')
    for source in index['images']:
        cp.checked_file(R,source);cp.checked_file(R,source['sidecar'])
        iid=source['image_id'];line,beat,image=lookup[iid]
        cp.checked_file(R,{'path':line['audio']['wav'],'sha256':line['audio']['sha256']})
        binding=image.get('performance',{}).get('Milo')
        base={'image_id':iid,'line_id':line['line_id'],'beat_id':beat['id'],'text':line['text'],'speaker':line['speaker'],'audio':line['audio'],'edit_base':{'path':source['path'],'sha256':source['sha256']},'background_continuity':beat['background_continuity'],'state_ref':image['state'],'world_state':plan['world_states'][image['state']]}
        if not binding:
            row={**base,'status':'retained_environment_only','reason':'No visible actor in the authored shot; preserve the shadow/environment cutaway unchanged.'}
            retained.append(row);rows.append(row);continue
        asset=lib['assets'][binding['pose_id']];variant=asset['variants'][binding['pose_variant']]
        if variant['status'] not in cp.APPROVED:raise ValueError('Owner performance acceptance required: '+iid)
        cp._decision(R,asset,binding['pose_variant'],variant)
        pose={'role':'reviewed_performance','authority':'pose_and_local_character_construction; not camera, prop design or scene approval','asset_id':asset['id'],'design_revision':asset['revision'],'variant':binding['pose_variant'],'image_revision':variant['file']['image_revision'],'path':variant['file']['path'],'sha256':variant['file']['sha256'],'owner_decision':variant['owner_decision']}
        expression_asset=lib['assets'][binding['expression_id']]
        expression=expression_asset['variants'][binding['expression_variant']]
        expression_requirement={'id':expression_asset['id'],'variant':binding['expression_variant'],'status':expression['status'],'file':expression.get('file'),'handling':'Planned expression remains missing; emotional direction is proposed only within the new scene candidate, not claimed as a reviewed reusable expression.'}
        blockers=cp.anatomy_blockers(lib,'Milo',variant)
        if expression['status'] not in cp.APPROVED:blockers.append('Required standalone expression asset remains planned; not a production-ready binding.')
        if beat['background_continuity']=='locked_background':
            row={**base,'status':'held_fixed_fork_group','performance':pose,'expression_requirement':expression_requirement,'reason':'Keep S03-L006–L008 as one group. Shared camera/depth/root/scale anchor is unmeasured and long_path still turns the whole body. Guidance cannot promise exact background pixels.','production_readiness_blockers':blockers,'staging_contract':plan['performance_staging_contracts']['fork_decision.Milo']}
            held.append(row);rows.append(row);continue
        output=re.sub(r'_r\d+_candidate\.png$','_r002_candidate.png',source['path'])
        if output==source['path'] or (R/output).exists():raise ValueError('Output revision already exists or invalid')
        refs=[{**canonical,'role':'canonical_identity','authority':'identity_anatomy_material_palette'},pose,{**base['edit_base'],'role':'scene_edit_base','authority':'existing composition, camera/framing, location light, ground and story props; old Milo anatomy is not authority'}]
        props=base['world_state']['props'];owner=props['acorn']['owner']
        portrait=asset['asset_type']=='portrait_base'
        if owner=='Milo':
            prop_rule='Milo retains the same story acorn from the scene reference. Do not adopt a different acorn from the pose reference or resize hands to fit it. '
            prop_rule+=('Acorn possession persists offscreen in this portrait; do not include hands/acorn/lower torso in the crop.' if portrait else 'Preserve plausible finger contact and occlusion; actual acorn fit remains for owner review.')
        elif owner=='stone':
            prop_rule=('The acorn is released on the stream stone, Milo hands empty; retain the acorn beside the stone and contact/readable separation.' if line['line_id']=='S02-L004' else 'The acorn remains behind on the stream stone, offscreen. Milo hands are empty; do not insert an acorn in this route/portrait shot.')
        else:prop_rule='Do not add an acorn: it has not yet entered this shot. Do not import incidental props from the pose reference.'
        extra=''
        if 'berry' in iid.lower() or 'berries' in asset['id'] or 'berry_thicket' in asset['id']:
            extra+=' Preserve berries/vegetation belonging to the scene base; do not import the isolated pose branch or replace scene berries with unrelated blueberries. Match grip to the existing story plant.'
        if 'lightstep' in asset['id']:
            extra+=' Show one readable rightward walking moment, with a grounded supporting foot. This scene still does not prove a complete gait cycle.'
        if line['line_id'] in {'S03-L003','S03-L004','S03-L005'}:
            extra+=' Milo is stationary and considering the route. Do not show him committing to or walking into the shortcut before S03-L009.'
        framing=('Full head and both ears, short natural neck, shoulders and upper chest only; shallow-focus background from this scene. All whiskers inside frame with margin; no torso, hands, tail or feet in this portrait.' if portrait else 'Retain the scene camera/framing and support-depth relationship. Place feet on the same local support plane with contact shadow and correct occlusion. New canonical anatomy controls head/body proportions; do not preserve the old Milo silhouette as a shape target.')
        emotion=beat.get('emotion') or ('startled realization that it is late' if line['line_id']=='S02-L003' else 'the listening audience should read the exact action and emotion of this line')
        prompt=f'''Edit one existing 16:9 Feltwillow scene into a new candidate image for {iid}. Reference 1 is approved Milo identity/anatomy/material. Reference 2 is the owner-selected Milo performance ({asset['id']}:{binding['pose_variant']}); use its pose, body construction and angle-compatible face, not its studio background, crop, lighting or incidental props. Reference 3 is the existing scene to edit: preserve its place, broad composition, camera, lighting and narrative context, replacing the old Milo depiction. Return one complete scene with one Milo, not a pose sheet or extra duplicate mouse. A reference-guided edit can redraw pixels; this is a review draft, not a claim of deterministic identity or exact background protection.

Audience hears: {line['text']}
Visual beat: {beat['action']}
Key-image phase: {image['phase_intent']}
Performance/emotion: {emotion}.
{framing}

Preserve the canonical grey felt mouse, cream muzzle and restrained elongated chest/belly inset, green eyes, charcoal nose, rounded ears, orange tail where visible. Keep his short readable neck and lean build; no inflated belly, shortened torso, independently enlarged head or hands. Applicable upright projected-head target remains 0.39 +/-0.01 only with matching head pitch/support. Canonical-compatible visible torso-panel/head-width guides are approximately 0.44 upper / 0.53 middle / 0.49 lower; mid cream patch / visible belly panel approximately 0.61. These are visible surface observations with uncertainty, not universal skeleton targets. Bent, occluded, turned and portrait views need local compatible anatomy, not forced upright fractions. Preserve angle-compatible ear/head and eye/head construction. Foreground perspective and a closer camera may change pixel size, not anatomy. Use uniform whole-character staging; no stretching separate parts to hit a screen box. No invented camera distance in metres.

{prop_rule}{extra}
Persistent world state: {image['state']}; change view only, not prop custody or causal state. Narrator does not drive mouth motion. Spoken dialogue also keeps closed still-mouth boundaries for later lip-sync; no visible teeth. Preserve handmade forest materials and intrinsic Milo palette while matching scene light and depth of field. No text, logos, pale corner symbol, watermark, measurement marks or reference-sheet labels. No Leo or other animal added. This is one revised representative composition, not completion/approval of every motion endpoint or Wan clip.'''
        row={**base,'sequence':len(requests)+1,'status':'prepared_candidate_edit_pending_operation_approval','performance':pose,'expression_requirement':expression_requirement,'performance_binding':copy.deepcopy(binding),'prop_rule':prop_rule,'camera_status':'source_framing_reference_only; camera/depth not measured','production_readiness':False,'production_readiness_blockers':blockers,'inputs':refs,'arguments':{'prompt':prompt,'referenced_image_paths':[str(R/ref['path']) for ref in refs],'transparent_background':False},'output':output,'sidecar':str(Path(output).with_suffix('.json')),'review_scope':'Representative scene-composition candidate only; no automatic anatomy, prop, scene, sequence or video approval.'}
        requests.append(row);rows.append(row)
    assert (len(requests),len(held),len(retained))==(20,3,1)
    op={'schema':'feltwillow.scene-performance-revision-operation.v1','story':'lion_and_mouse_v7','status':'prepared_pending_exact_operation_approval','endpoint':'image_gen.imagegen','request_count':20,'outputs_per_request':1,'automatic_retries':0,'model':None,'seed':None,'estimated_total_cost':None,'pricing':'Built-in current model/pricing not exposed; total unknown, not assumed free.','scope':'20 representative S01-S03 scene edits using owner-selected Milo performances; three fixed-fork shots held, one environment cutaway retained. No new performance assets, canonical, narration or video generation.','source_plan_sha256':cp.av.digest(folder/'audio_visual_plan.json'),'source_library_sha256':cp.av.digest(folder/cp.LIBRARY),'production_ready':False,'generation_authorized':False,'requests':requests,'held':held,'retained':retained}
    cp.av.write(D/'OPERATION.json',op)
    md=['# S01–S03 Milo scene replacements · proposed operation','','**Prepared only. No image requests submitted.** Endpoint: `image_gen.imagegen`. 20 requests, one candidate per request, zero automatic retries. Full-scene 16:9 image guidance, opaque output. Model and seed are managed by the tool, not exposed. Total cost is unknown.','', 'Twenty owner-review scene edits; three fixed-fork shots held; one environment-only cutaway unchanged. Milo performances are owner-selected, while anatomy/prop/standalone expression/staging evidence is incomplete. This proposal does not declare production readiness or bypass those gates. Existing scene originals stay intact and new outputs use r002.','', 'Operation SHA-256: `'+cp.av.digest(D/'OPERATION.json')+'`','', '## Held fixed-fork group','']
    md += ['- '+h['image_id']+': '+h['reason'] for h in held]
    md += ['','Environment retained: '+retained[0]['image_id']+'.','']
    for q in requests:
        md+=['## '+str(q['sequence'])+'. '+q['image_id'],'','Output: `'+q['output']+'`','','| Reference role | Exact input | SHA-256 |','|---|---|---|']
        md+=['| '+f['role']+' | '+f['path']+' | '+f['sha256']+' |' for f in q['inputs']]
        md+=['','Expression requirement: '+q['expression_requirement']['id']+' ('+q['expression_requirement']['status']+'). No standalone expression file invented.','','Readiness limitations: '+'; '.join(q['production_readiness_blockers']),'','Exact prompt:','','```text',q['arguments']['prompt'],'```','']
    (D/'OPERATION.md').write_text('\n'.join(md)+'\n')
    def url(path):return html.escape(os.path.relpath(cp.av.local(R,path),D),quote=True)
    cards=[]
    for q in rows:
        pose=q.get('performance');pics='<figure><figcaption>Existing scene · unchanged</figcaption><img loading="lazy" src="'+url(q['edit_base']['path'])+'"></figure>'
        if pose:pics+='<figure><figcaption>Owner-selected Milo performance</figcaption><img class="pose" loading="lazy" src="'+url(pose['path'])+'"></figure>'
        label=q.get('reason') or 'New scene r002 is planned, not generated. '+q['prop_rule']
        cards.append('<article><h2>'+html.escape(q['image_id'])+'</h2><p class="status">'+html.escape(q['status'])+'</p><p>'+html.escape(q['text'])+'</p><audio controls preload="none" src="'+url(q['audio']['wav'])+'"></audio><div class="pair">'+pics+'</div><p>'+html.escape(label)+'</p>'+('<details><summary>Remaining technical review</summary><p>'+html.escape('; '.join(q.get('production_readiness_blockers',[])))+'</p></details>' if pose else '')+'</article>')
    (D/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>S01–S03 Milo scene revision preflight</title><style>body{font:17px system-ui;background:#252821;color:#eee;margin:26px}a{color:#c7edab}article{background:#343a31;padding:18px;margin:24px 0;border-radius:8px}.pair{display:grid;grid-template-columns:2fr 1fr;gap:16px}figure{margin:0;min-width:0}img{width:100%;height:auto}.pose{max-height:440px;object-fit:contain;background:repeating-conic-gradient(#ddd 0% 25%,#fff 0% 50%) 50%/24px 24px}audio{width:100%;max-width:700px}.status{color:#ffdb91}h2{overflow-wrap:anywhere}</style><h1>S01–S03 · scene replacement preflight</h1><p><strong>0 new scene images generated; 20 candidate edits prepared, 3 fixed-fork shots held, 1 environment-only shot unchanged.</strong></p><p>Each row pairs the existing scene with the owner-selected Milo performance. These pairs are references, not finished composites. New compositions need their own owner review; anatomy, prop fit, expression and staging checks remain separate.</p><p><a href="../../character_performance_consistency_r001/pose_library/review.html">Milo performance library and canonical measurements</a></p>'+''.join(cards)+'<script>document.querySelectorAll("audio").forEach(p=>p.addEventListener("play",()=>document.querySelectorAll("audio").forEach(q=>{if(q!==p)q.pause()})));</script>')
    cp.av.write(D/'SOURCE_REVIEW_INDEX.json',{'scope':'scene edit bases and reviewed performances; not newly generated images','rows':rows})
    return {'requests':20,'held':3,'retained':1,'submitted':0,'gallery':str((D/'review.html').relative_to(R))}


if __name__=='__main__':print(json.dumps(build(),indent=2))
