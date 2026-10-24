"""Validate and present the owner's current, exact-hash S01-S05 selection."""
from collections import Counter
import html
import json
import os
from pathlib import Path

try:
    from . import audio_visual_plan as av
except ImportError:
    import audio_visual_plan as av

LEDGER='scene_image_selection_s01_s05.json'

def verify(root, story):
    from PIL import Image
    folder=Path(root)/'stories'/story
    ledger=av.read(folder/LEDGER)
    if ledger.get('decision')!='owner_selected_scene_images' or ledger.get('reviewer')!='project_owner':
        raise ValueError('Owner-selected scene ledger required')
    paths=set()
    for row in ledger['images']:
        if row['path'] in paths:
            raise ValueError('Duplicate selected image bytes/use')
        paths.add(row['path'])
        for ref in [row,row['sidecar']]:
            path=av.local(root,ref['path'])
            if not path.is_file() or av.digest(path)!=ref['sha256']:
                raise ValueError('Selected bytes changed: '+ref['path'])
        side=av.read(av.local(root,row['sidecar']['path']))
        image_hash=side.get('sha256') or side.get('image',{}).get('sha256')
        if image_hash!=row['sha256'] or side['image_id']!=row['image_id']:
            raise ValueError('Selected sidecar mismatch')
        with Image.open(av.local(root,row['path'])) as image:
            image.load()
            if list(image.size)!=row['dimensions']:
                raise ValueError('Selected dimensions mismatch')
        for key,hash_key in [('wav','sha256'),('metadata','metadata_sha256')]:
            if av.digest(av.local(root,row['audio'][key]))!=row['audio'][hash_key]:
                raise ValueError('Selected audio bytes changed')
    if len(paths)!=ledger['count']:
        raise ValueError('Selection count mismatch')
    counts=dict(Counter(r['line_id'][:3] for r in ledger['images']))
    if counts!=ledger['counts_by_scene']:
        raise ValueError('Scene counts mismatch')
    reuse=av.read(folder/'selected_images/IMAGE_REUSE.json')
    source=next(r for r in ledger['images'] if r['image_id']==reuse['reuse_of'])
    if (reuse['path'],reuse['sha256'])!=(source['path'],source['sha256']):
        raise ValueError('Reused image mismatch')
    for key,hash_key in [('wav','sha256'),('metadata','metadata_sha256')]:
        if av.digest(av.local(root,reuse['audio'][key]))!=reuse['audio'][hash_key]:
            raise ValueError('Reuse audio changed')
    return folder,ledger,reuse


def build(root, story):
    folder,ledger,reuse=verify(root,story)
    target=folder/'review/character_performance_consistency_r001/pose_library'
    target.mkdir(parents=True,exist_ok=True)
    h=html.escape
    def url(name):
        return h(os.path.relpath(av.local(root,name),target),quote=True)
    cards=[]
    for row in ledger['images']:
        label=row['image_id'] or row['beat_id']+' · forest establishment'
        audio=row['audio']
        note=row.get('technical_review') or 'Owner selected depiction; technical review remains separate.'
        if not isinstance(note,str):note=json.dumps(note)
        extra=''
        if row['image_id']==reuse['reuse_of']:
            extra='<p>S05-L006 · same selected image, no cut</p><audio controls preload="none" src="'+url(reuse['audio']['wav'])+'"></audio>'
        cards.append('<article data-kind="scene" data-search="'+h((label+' '+row['line_id']+(' S05-L006' if extra else '')).lower(),quote=True)+'"><h2>'+h(label)+'</h2><p class="badge">Owner-selected scene image</p><a href="'+url(row['path'])+'" target="_blank"><img loading="lazy" src="'+url(row['path'])+'" alt="'+h(label)+'"></a><p>'+h(audio['metadata_text'])+'</p><audio controls preload="none" src="'+url(audio['wav'])+'"></audio>'+extra+'<details><summary>Source and technical notes</summary><p>'+h(note)+'</p><p class="file">'+h(row['path'])+'</p><code>'+h(row['sha256'])+'</code><p>Selection is bound to these image bytes. Video, contact and numerical anatomy certification remain separate.</p></details></article>')
    library=av.read(folder/'character_performance_library.json')
    performance=[];pending=0
    for aid,asset in library['assets'].items():
        for name,v in asset['variants'].items():
            f=v.get('file')
            if not f:continue
            if v['status'] not in {'owner_selected_for_performance','approved_for_scene_use'}:
                pending+=1;continue
            if av.digest(av.local(root,f['path']))!=f['sha256']:
                raise ValueError('Selected performance changed')
            performance.append('<article data-kind="performance" data-search="'+h((aid+':'+name).lower(),quote=True)+'"><h2>'+h(aid+':'+name)+'</h2><p class="badge">Owner-selected performance · separate from scene approval</p><a href="'+url(f['path'])+'"><img loading="lazy" src="'+url(f['path'])+'" alt="'+h(aid+':'+name)+'"></a><p class="file">'+h(f['path'])+'</p></article>')
    gaps=av.read(folder/'selected_images/COVERAGE_GAPS.json')
    gap_rows=''.join('<li>'+h(g['image_id'])+' · '+h(g['phase'] or '')+'</li>' for g in gaps['missing_planned_keys'])
    upcoming=''
    next_folder=folder/'review/character_performance_consistency_r001/s06_s07_pose_planning_r001'
    if (next_folder/'OPERATION.json').is_file():
        operation=av.read(next_folder/'OPERATION.json')
        narration=av.read(folder/'audio_visual_plan.json')
        players=[]
        for line in narration['lines']:
            if line['audio_scene'] in {'S06','S07'}:
                players.append('<p><strong>'+h(line['line_id'])+'</strong> · '+h(line['text'])+'</p><audio controls preload="none" src="'+url(line['audio']['wav'])+'"></audio>')
        upcoming='<details open><summary>Next character-performance work · S06 and S07</summary><p>S06: one connected two-character setup on S05 background/camera. Leo stays lying with head/chest raised; Milo screen-right, facing and looking up-left. A FRONT paw blocks beside him; S05 trip involved the REAR paw. S07: Leo portraits L001/L002, Milo portraits L003–L005 with reciprocal eyelines and locked upper-body geometry within each family.</p><p>Three foundation requests prepared: one paired path-arrival pose plus two portrait bases. Ten paired S06 phases and five S07 portrait uses are planned; 0 new candidates or approvals inferred. Cost unknown, no retries; no submission authorized by this gallery. Source S05 contains Leo, so later scene composition needs reviewed old-Leo removal/clean-plate handling.</p><details><summary>Actual S06/S07 narration</summary>'+''.join(players)+'</details></details>'
        if (next_folder/'EXECUTION.json').is_file():
            execution=av.read(next_folder/'EXECUTION.json')
            review=av.read(next_folder/'VISUAL_OBSERVATIONS.json') if (next_folder/'VISUAL_OBSERVATIONS.json').is_file() else {'candidates':[]}
            continuation=next_folder.parent/'s06_s07_pose_continuation_r002'
            if (continuation/'EXECUTION.json').is_file():
                execution['outputs']+=av.read(continuation/'EXECUTION.json')['outputs']
                if (continuation/'VISUAL_OBSERVATIONS.json').is_file():
                    review['candidates']+=av.read(continuation/'VISUAL_OBSERVATIONS.json')['candidates']
            notes={r['sha256']:r['observation'] for r in review['candidates']}
            line_lookup={line['line_id']:line for line in narration['lines']}
            incoming=[]
            approved_foundations=0
            for row in execution['outputs']:
                for record in [row,row['sidecar'],row['receipt']]:
                    if av.digest(av.local(root,record['path']))!=record['sha256']:
                        raise ValueError('New performance candidate bytes changed')
                labels=row['audio_image_uses']
                audio=[]
                for lid in sorted({iid[:8] for iid in labels}):
                    line=line_lookup[lid]
                    if av.digest(av.local(root,line['audio']['wav']))!=line['audio']['sha256']:
                        raise ValueError('New performance candidate audio changed')
                    audio.append('<p>'+h(lid)+' · '+h(line['text'])+'</p><audio controls preload="none" src="'+url(line['audio']['wav'])+'"></audio>')
                label=row['requirement_id']+':'+row['variant']
                joint=len(row['actors'])==2
                registry=library['joint_performance_requirements'] if joint else library['assets']
                variant=registry[row['requirement_id']]['variants'][row['variant']]
                decision=variant.get('owner_decision')
                badge='New performance candidate · pending owner review'
                if decision:
                    record=decision['record']
                    if av.digest(av.local(root,record['path']))!=record['sha256']:
                        raise ValueError('Performance selection ledger changed')
                    decisions=av.read(av.local(root,record['path']))['joint_decisions' if joint else 'decisions']
                    if decision['sha256']!=row['sha256'] or decisions[label]!={k:v for k,v in decision.items() if k!='record'}:
                        raise ValueError('Performance selection does not identify these exact bytes')
                    approved_foundations+=1
                    badge='Owner-selected joint performance reference' if joint else 'Owner-selected performance reference'
                incoming.append('<article data-kind="candidate" data-search="'+h((label+' '+' '.join(labels)).lower(),quote=True)+'"><h2>'+h(label)+'</h2><p class="badge">'+h(badge)+'</p><a href="'+url(row['path'])+'" target="_blank"><img loading="lazy" src="'+url(row['path'])+'" alt="'+h(label)+'"></a><p>'+h(notes.get(row['sha256'],'Native review pending'))+'</p><p>'+h(', '.join(labels))+'</p>'+''.join(audio)+'<details><summary>Source evidence</summary><p class="file">'+h(row['path'])+'</p><code>'+h(row['sha256'])+'</code><p>Performance scope only; no measured anatomy or scene approval.</p></details></article>')
            upcoming='<section><h2>S06/S07 · '+str(execution['completed'])+' new foundation candidates</h2><p>One paired Leo+Milo PNG and two individual portrait bases saved, not four generated assets. Leo remains lying/head raised, Milo screen-right; portrait eyelines are reciprocal. All pending owner review. Leo mane clearance is tight; anatomy, relative scale, support and acting need review. Remaining phase/expression keys held. No S06/S07 scene images or clean-background edits yet. No retries; actual cost unknown.</p><p><a href="?kind=candidate">Show new candidates</a> · <a href="?kind=scene">Selected S01–S05 scenes</a></p><div class="grid">'+''.join(incoming)+'</div><details><summary>All S06/S07 narration</summary>'+''.join(players)+'</details></section>'
            if approved_foundations:
                upcoming=upcoming.replace('new foundation candidates','performance foundations').replace('All pending owner review.',str(approved_foundations)+' foundations owner-selected at exact hashes; technical notes retained.')
            if (continuation/'EXECUTION.json').is_file():
                total=len(execution['outputs'])
                summary=(f'{total} performance references · {approved_foundations} selected foundations · '
                         f'{total-approved_foundations} new candidates pending review')
                start=upcoming.index('<h2>')
                end=upcoming.index('<p><a href="?kind=candidate">')
                upcoming=upcoming[:start]+'<h2>S06/S07 · '+summary+'</h2><p>Three paired Leo+Milo PNGs plus five individual portraits/expressions. Leo stays lying; Milo remains screen-right. The planted-paw candidate has a suspected overlap with Milo’s foot and must be reviewed before dependent poses. Expression crop/body preservation and anatomy remain unverified. Seven further joint phases are held for reviewed anchors. No S06/S07 scene compositions yet; no retries, actual cost unknown.</p>'+upcoming[end:]
            continuation=next_folder.parent/'s06_s07_pose_continuation_r002'
            if (continuation/'OPERATION.json').is_file() and not (continuation/'EXECUTION.json').is_file():
                upcoming=upcoming.replace('<details><summary>All S06/S07 narration</summary>','<p>Next concrete stage: five requests prepared, not submitted—low-head/nose joint pose, planted FRONT-paw block, Leo questioning face, Milo anxious explanation and sincere promise. S07-L001/L003 reuse approved base depictions. Seven other joint phases await reviewed anchor hashes. No new scenes or background repairs.</p><details><summary>All S06/S07 narration</summary>')
    scene_work=folder/'review/scene_compositions/s06_s07_background_scenes_r001'
    if (scene_work/'LOCAL_SCENES.json').is_file():
        scene_cards=[]
        scene_rows=av.read(scene_work/'LOCAL_SCENES.json')['outputs']
        if (scene_work/'S06_SCENES.json').is_file():
            scene_rows=av.read(scene_work/'S06_SCENES.json')['outputs']+scene_rows
        for row in scene_rows:
            for record in [row,row['sidecar'],row['receipt']]:
                if av.digest(av.local(root,record['path']))!=record['sha256']:
                    raise ValueError('New scene candidate bytes changed')
            for key,hash_key in [('wav','sha256'),('metadata','metadata_sha256')]:
                if av.digest(av.local(root,row['audio'][key]))!=row['audio'][hash_key]:
                    raise ValueError('New scene candidate audio changed')
            label=row['image_id']+' · scene candidate'
            scene_badge='Pending owner scene review'
            decision=row.get('owner_approval')
            if decision:
                record=decision['record']
                if av.digest(av.local(root,record['path']))!=record['sha256']:
                    raise ValueError('Scene selection ledger changed')
                matches=[v for v in av.read(av.local(root,record['path']))['images'] if v['image_id']==row['image_id'] and v['sha256']==row['sha256']]
                if len(matches)!=1 or matches[0]!={k:v for k,v in decision.items() if k!='record'}:
                    raise ValueError('Scene selection does not identify exact candidate bytes')
                scene_badge='Owner-selected scene depiction · technical notes retained'
            elif (scene_work.parent/'s07_milo_nervous_faces_r002/OWNER_FEEDBACK.json').is_file() and row['line_id'] in {'S07-L003','S07-L004','S07-L005'}:
                scene_badge='Nervous-face revision · pending owner scene review' if row['image_revision']=='r002' else 'Needs more nervous facial acting · revision prepared'
            scene_cards.append('<article data-kind="scene_candidate" data-search="'+h(label.lower(),quote=True)+'"><h2>'+h(label)+'</h2><p class="badge">'+h(scene_badge)+'</p><a href="'+url(row['path'])+'" target="_blank"><img loading="lazy" src="'+url(row['path'])+'" alt="'+h(label)+'"></a><p>'+h(row['audio']['metadata_text'])+'</p><audio controls preload="none" src="'+url(row['audio']['wav'])+'"></audio><p>'+h(row['technical_review'])+'</p><details><summary>Source evidence</summary><p class="file">'+h(row['path'])+'</p><code>'+h(row['sha256'])+'</code></details></article>')
        scene_summary='Five S07 portraits use exact selected character layers over blurred actor-free S05 foliage, with a fixed transform per portrait family.'
        if (scene_work/'S06_SCENES.json').is_file():
            scene_summary+=' Three S06 anchors use selected joint pose layers on one protected reconstructed background; one approved background-generation request, no retries. Seven motion/reaction phases remain missing. Grounding, paw clearance and scale continuity need scene review.'
        else:
            scene_summary+=' S06 awaits clean-background reconstruction; seven motion/reaction phases remain missing.'
        upcoming='<section><h2>S06/S07 · '+str(len(scene_rows))+' scene candidates</h2><p>'+scene_summary+'</p><p><a href="?kind=scene_candidate">Show new scenes</a></p><div class="grid">'+''.join(scene_cards)+'</div></section>'+upcoming
        upcoming=upcoming.replace('No S06/S07 scene compositions yet;', 'Five S07 local portrait scenes saved; S06 clean-background repair pending;')
        upcoming=upcoming.replace('Seven further joint phases are held for reviewed anchors.', 'Seven further joint phases still need generation using the selected anchors.')
        if (scene_work/'S06_SCENES.json').is_file():
            upcoming=upcoming.replace('Five S07 local portrait scenes saved; S06 clean-background repair pending;', 'Three S06 anchors and five S07 portraits saved;')
    s08=folder/'review/character_performance_consistency_r001/s08_planning_r001'
    if (s08/'OPERATION.json').is_file():
        operation=av.read(s08/'OPERATION.json')
        shot_map=av.read(s08/'S08_SHOT_MAP.json')
        preview=[]
        generated={}
        if (s08/'EXECUTION.json').is_file():
            generated={row['requirement_id']+':'+row['variant']:row for row in av.read(s08/'EXECUTION.json')['outputs']}
        for request in operation['requests']:
            for record in request['inputs']:
                if av.digest(av.local(root,record['path']))!=record['sha256']:
                    raise ValueError('S08 proposed input changed')
            label=request['requirement_id']+':'+request['variant']
            output=generated.get(label)
            if output:
                for record in [output,output['sidecar'],output['receipt']]:
                    if av.digest(av.local(root,record['path']))!=record['sha256']:
                        raise ValueError('S08 generated performance changed')
            shown=output['path'] if output else request['inputs'][0]['path']
            badge='S08 generated performance candidate · pending owner review' if output else 'Planned S08 performance · existing reference shown below'
            preview.append('<article data-kind="planning" data-search="'+h((label+' '+' '.join(request['audio_image_uses'])).lower(),quote=True)+'"><h2>'+h(label)+'</h2><p class="badge">'+badge+'</p><img loading="lazy" src="'+url(shown)+'" alt="'+h(badge)+'"><p>'+h(', '.join(request['audio_image_uses']))+'</p><details><summary>Exact prompt</summary><p>'+h(request['tool_arguments']['prompt'])+'</p></details></article>')
        narration=[]
        for line in av.read(folder/'audio_visual_plan.json')['lines']:
            if line['audio_scene']!='S08':continue
            shots=[v for v in shot_map['images'] if v['line_id']==line['line_id']]
            narration.append('<p><strong>'+h(line['line_id'])+' · '+h(shots[0]['framing'])+'</strong> · '+h(line['text'])+'</p><audio controls preload="none" src="'+url(line['audio']['wav'])+'"></audio>')
        upcoming='<section><h2>S08 · planned performances and narration</h2><p>Close-ups L007–L015 and L019–L024; nine other lines use the fixed S06 great-tree setup. Leo lying left, Milo screen-right. Paw release at L010 and sky gesture at L024 happen below portrait crop; world events persist. Seven foundation requests prepared, not submitted; cost unknown, no retries. Existing reference images shown, no S08 output yet.</p><p><a href="?kind=planning">Show S08 plan</a></p><div class="grid">'+''.join(preview)+'</div><details><summary>24 S08 lines · framing and audio</summary>'+''.join(narration)+'</details></section>'+upcoming
        if generated:
            upcoming=upcoming.replace('S08 · planned performances and narration','S08 · performances and narration').replace('Seven foundation requests prepared, not submitted; cost unknown, no retries. Existing reference images shown, no S08 output yet.',str(len(generated))+' of seven authorized outputs saved; all pending owner review. Leo considerate/soft/reassuring; Milo nervous, cautiously relieved, then grateful. Cost unknown, no retries.')
    s08_scenes=folder/'review/scene_compositions/s08_scenes_r001/SCENES.json'
    if s08_scenes.is_file():
        scenes=av.read(s08_scenes)
        actual=[]
        for row in scenes['associations']:
            for record in [row,row['sidecar'],row['receipt']]:
                if av.digest(av.local(root,record['path']))!=record['sha256']:
                    raise ValueError('S08 scene association bytes changed')
            if av.digest(av.local(root,row['audio']['wav']))!=row['audio']['sha256']:
                raise ValueError('S08 scene audio changed')
            reuse='Same scene pixels as '+row['primary_image_id']+'; deliberate hold/offscreen action.' if row['reuses_exact_scene_pixels'] else 'Primary scene raster; related lines may reuse this depiction.'
            badge='Pending owner performance/scene review'
            decision=row.get('owner_approval')
            if decision:
                record=decision['record']
                if av.digest(av.local(root,record['path']))!=record['sha256']:
                    raise ValueError('S08 scene selection ledger changed')
                matches=[v for v in av.read(av.local(root,record['path']))['images'] if v['image_id']==row['primary_image_id'] and v['sha256']==row['sha256']]
                if len(matches)!=1 or row['image_id'] not in matches[0]['all_image_ids'] or matches[0]!={k:v for k,v in decision.items() if k!='record'}:
                    raise ValueError('S08 selection does not identify scene bytes and use')
                badge='Owner-selected scene depiction · technical notes retained'
            actual.append('<article data-kind="s08_scene" data-search="'+h((row['image_id']+' '+row['source_variant']).lower(),quote=True)+'"><h2>'+h(row['image_id'])+' · scene candidate</h2><p class="badge">'+badge+'</p><a href="'+url(row['path'])+'" target="_blank"><img loading="lazy" src="'+url(row['path'])+'" alt="'+h(row['image_id'])+'"></a><p>'+h(row['audio']['metadata_text'])+'</p><audio controls preload="none" src="'+url(row['audio']['wav'])+'"></audio><p>'+h(row['source_variant']+' · '+reuse)+'</p><details><summary>Source and limits</summary><p>'+h(' '.join(row['review_notes']))+'</p><p class="file">'+h(row['path'])+'</p><code>'+h(row['sha256'])+'</code></details></article>')
        upcoming='<section><h2>S08 · 24 narration lines / '+str(scenes['unique_scene_files'])+' unique scene depictions</h2><p>Line-specific acting choices reuse suitable expressions rather than generic surprise. Close-up families retain head/neck/chest geometry. Shared shots use one S06 protected background/camera. Identical L001/L010/L024 boundaries are holds or offscreen changes, not distinct visible action endpoints. All are candidate previews using unapproved new performances; no numerical anatomy or video readiness inferred.</p><p><a href="?kind=s08_scene">Show S08 scenes</a></p><div class="grid">'+''.join(actual)+'</div></section>'+upcoming
        if all(row.get('owner_approval') for row in scenes['associations']):
            upcoming=upcoming.replace('All are candidate previews using unapproved new performances; no numerical anatomy or video readiness inferred.', 'All seven scene depictions and their recorded uses are owner-selected at exact hashes. Raw performance approval, numerical anatomy and video readiness remain separate.')
    later=folder/'review/character_performance_consistency_r001/s09_s11_pose_planning_r001'
    if (later/'OPERATION.json').is_file():
        cards_later=[]
        operation=av.read(later/'OPERATION.json')
        for request in operation['requests']:
            for record in request['inputs']:
                if av.digest(av.local(root,record['path']))!=record['sha256']:
                    raise ValueError('S09–S11 proposed source changed')
            label=request['requirement_id']+':'+request['variant']
            cards_later.append('<article data-kind="later_plan" data-search="'+h((label+' '+' '.join(request['audio_image_uses'])).lower(),quote=True)+'"><h2>'+h(label)+'</h2><p class="badge">Planned pose · source reference shown, not new output</p><img loading="lazy" src="'+url(request['inputs'][0]['path'])+'" alt="Existing reference for planned pose"><p>'+h(', '.join(request['audio_image_uses']))+'</p><details><summary>Exact proposed prompt</summary><p>'+h(request['tool_arguments']['prompt'])+'</p></details></article>')
        local=av.read(later/'LOCAL_OUTPUTS.json')['outputs'][0]
        for record in [local,local['sidecar'],local['receipt']]:
            if av.digest(av.local(root,record['path']))!=record['sha256']:
                raise ValueError('Local awake-Leo extraction changed')
        cards_later.insert(0,'<article data-kind="later_plan" data-search="leo rest awake s09-l006 s09-l007"><h2>leo.rest.awake.clear.3q:default</h2><p class="badge">New local extraction candidate · pending owner review</p><img loading="lazy" src="'+url(local['path'])+'" alt="Awake lying Leo, transparent extraction"><p>S09-L006 / S09-L007. Native Leo pixels retained; separate Milo removed across near-transparent gap. No paid call or body redraw; no approval transfer from source scene.</p></article>')
        lines=[]
        for line in av.read(folder/'audio_visual_plan.json')['lines']:
            if line['audio_scene'] in {'S09','S10','S11'}:
                lines.append('<p><strong>'+h(line['line_id'])+'</strong> · '+h(line['text'])+'</p><audio controls preload="none" src="'+url(line['audio']['wav'])+'"></audio>')
        upcoming='<section><h2>S09–S11 · poses and narration</h2><p>Reuse homeward Milo walking and standing references. Five new requests prepared: two careful Milo steps, two curious Leo steps, one grounded connected-net anchor. Cost unknown, no retries; no paid submissions yet. Review net topology before falling/tug/trapped-portrait/call variants. Leo remains grounded; curiosity, concern and frustration replace the old encouraging-face placeholders.</p><p><a href="?kind=later_plan">Show S09–S11 poses</a></p><div class="grid">'+''.join(cards_later)+'</div><details><summary>S09–S11 actual narration</summary>'+''.join(lines)+'</details></section>'+upcoming
    style='body{font:17px system-ui;background:#252821;color:#eee;margin:26px}a{color:#c7edab}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:22px}article{background:#343a31;padding:16px;min-width:0;border-radius:8px}h2{font-size:18px;overflow-wrap:anywhere}article img{width:100%;height:auto;background:repeating-conic-gradient(#ddd 0% 25%,#fff 0% 50%) 50%/24px 24px}audio{width:100%;margin:8px 0}.badge{color:#ffdb91}.file,code{font-size:12px;overflow-wrap:anywhere}details{margin:15px 0}nav{display:flex;gap:15px;flex-wrap:wrap;margin:20px 0}input,select{font:inherit}article[hidden]{display:none}body.native article{overflow:auto}body.native article img{width:auto;max-width:none}'
    page='<!doctype html><html><head><meta charset="utf-8"><title>V7 selected S01–S05 images</title><style>'+style+'</style></head><body><header><h1>Lion and Mouse v7 · selected S01–S05 images</h1><p><strong>'+str(ledger['count'])+' selected scene images · 45 scene uses including L006 reuse.</strong> '+h(' · '.join(k+': '+str(v) for k,v in ledger['counts_by_scene'].items()))+'.</p><p>Clean current selection: superseded candidates are excluded. Existing technical notes remain. These are the images selected so far, not complete audio-aligned video coverage.</p><p><a href="../../canonical_measurements_r001/review.html">Canonical measurements · Milo and Leo</a></p><details><summary>Remaining planned keys ('+str(gaps['count'])+')</summary><p>These are missing authored scene endpoints, not failed selections. No missing media or motion approval is inferred.</p><ul>'+gap_rows+'</ul></details><p>'+str(len(performance))+' selected reusable performance assets; '+str(pending)+' current unapproved performance candidates retained separately for unfinished work. Historical sources needed for receipts are stored in the provenance archive.</p></header><nav><label>Search <input id="search" placeholder="S05, image ID or pose"></label><select id="kind"><option value="scene">Selected scenes</option><option value="performance">Selected performances</option><option value="all">All selected</option></select><label><input type="checkbox" id="native"> Native pixels</label></nav><main class="grid">'+''.join(cards+performance)+'</main>'
    page=page.replace('</header>',upcoming+'</header>')
    page=page.replace('<option value="all">All selected</option>','<option value="later_plan">S09–S11 poses</option><option value="s08_scene">S08 scenes</option><option value="scene_candidate">S06/S07 scenes</option><option value="planning">S08 performances</option><option value="candidate">Performance references</option><option value="all">All review items</option>')
    sequence_boards=sorted((folder/'review').glob('sequence_readiness_r[0-9][0-9][0-9]/*/review.html'))
    if sequence_boards:
        links=' '.join('<a href="'+h(os.path.relpath(p,target),quote=True)+'">'+h(p.parent.name)+'</a>' for p in sequence_boards)
        page+='<section><h2>Ordered sequence boards</h2><p>Source/fitted anchors, audio and blocked gates; selection is separate from technical readiness.</p>'+links+'</section>'
    page+='''<script>const params=new URLSearchParams(location.search), search=document.querySelector('#search'), kind=document.querySelector('#kind');search.value=params.get('q')||'';kind.value=['scene','performance','scene_candidate','s08_scene','later_plan','planning','candidate','all'].includes(params.get('kind'))?params.get('kind'):'scene';function filter(){const q=search.value.toLowerCase();document.querySelectorAll('article').forEach(a=>a.hidden=!(a.dataset.search.includes(q)&&(kind.value==='all'||a.dataset.kind===kind.value)));}search.addEventListener('input',filter);kind.addEventListener('change',filter);document.querySelector('#native').addEventListener('change',e=>document.body.classList.toggle('native',e.target.checked));filter();</script></body></html>'''
    (target/'review.html').write_text(page)
    return {'gallery':str((target/'review.html').relative_to(root)),'selected_scene_images':ledger['count'],'selected_performance_assets_shown':len(performance),'pending_performance_candidates_retained':pending,'unfilled_planned_keys':gaps['count'],'provider_calls':0,'source_image_changes':0}
