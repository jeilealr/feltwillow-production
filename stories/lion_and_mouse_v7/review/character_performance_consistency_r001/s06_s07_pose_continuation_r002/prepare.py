"""Record owner foundation selections and prepare bounded derived performances."""
import copy
import hashlib
import json
from pathlib import Path
import shutil

D=Path(__file__).resolve().parent
R=D.parents[4]
S=R/'stories/lion_and_mouse_v7'
F=S/'review/character_performance_consistency_r001/s06_s07_pose_planning_r001'

def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(path,role,authority):return {'path':path,'sha256':digest(R/path),'role':role,'authority':authority}

def main():
    assert not (D/'OPERATION.json').exists(),'Do not overwrite prepared operation'
    lib=read(S/'character_performance_library.json');plan=read(S/'audio_visual_plan.json')
    A=D/'owner_acceptance'
    for name in ['character_performance_library.json','audio_visual_plan.json']:
        shutil.copy2(S/name,A/('before_'+name))
    execution=read(F/'EXECUTION.json');decisions={};pair_decisions={}
    statement='ok then yes, those 3 images look fine. continue'
    for row in execution['outputs']:
        assert digest(R/row['path'])==row['sha256']
        qid=row['requirement_id'];name=row['variant']
        if len(row['actors'])==1:
            asset=lib['assets'][qid]
            decisions[qid+':'+name]={'asset_id':qid,'revision':asset['revision'],'variant':name,'sha256':row['sha256'],
                'canonical_sha256':asset['canonical']['sha256'],'reviewer':'project_owner','scope':'performance_use_only',
                'statement':statement,'image_revision':'r001','acting_scope':'face acting as depicted in this selected portrait base; not a separately generated expression file'}
        else:
            pair=lib['joint_performance_requirements'][qid]
            pair_decisions[qid+':'+name]={'requirement_id':qid,'revision':pair['revision'],'variant':name,'sha256':row['sha256'],
                'canonical_sha256':{a:r['sha256'] for a,r in pair['canonical'].items()},'reviewer':'project_owner',
                'scope':'joint_performance_use_only','statement':statement,'image_revision':'r001'}
    ledger=A/'OWNER_SELECTION.json'
    write(ledger,{'decisions':decisions,'joint_decisions':pair_decisions,'scope':'Three depicted performance foundations only; anatomy measurements, scene contact/plate and video approval remain separate.'})
    changes=[]
    for row in execution['outputs']:
        qid=row['requirement_id'];name=row['variant'];joint=len(row['actors'])==2
        v=(lib['joint_performance_requirements'][qid] if joint else lib['assets'][qid])['variants'][name]
        decision=(pair_decisions if joint else decisions)[qid+':'+name]
        decision=dict(decision,record={'path':str(ledger.relative_to(R)),'sha256':digest(ledger)})
        side=R/v['file']['sidecar']['path'];shutil.copy2(side,A/side.name)
        old_hash=digest(side);data=read(side)
        v.update(status='owner_selected_for_performance',owner_decision=decision)
        data.update(status=v['status'],owner_decision=decision);write(side,data)
        v['file']['sidecar']['sha256']=digest(side)
        row['sidecar']['sha256']=digest(side)
        changes.append({'path':str(side.relative_to(R)),'before_sha256':old_hash,'after_sha256':digest(side),
                        'reason':'owner review status overlay; original sidecar archived, generation receipt and PNG unchanged'})
    execution['review_status']='three foundations selected by owner';execution['review_changes']=changes;write(F/'EXECUTION.json',execution)
    write(A/'REVIEW_CHANGES.json',changes)
    # Remove an unintended redundant planned-only view alias; no generated pixels affected.
    duplicate='milo.freeze.front_paw.3q_left_left';preferred='milo.freeze.front_paw.3q_left'
    for l in plan['lines']:
        for b in l['beats']:
            for im in b['image_sequence']['images']:
                for binding in im.get('performance',{}).values():
                    if binding.get('pose_id')==duplicate:binding['pose_id']=preferred
    pair=lib['joint_performance_requirements']['milo_leo.s06.great_tree']
    for v in pair['variants'].values():
        for binding in v['actor_bindings'].values():
            if binding['pose_id']==duplicate:binding['pose_id']=preferred
    if duplicate in lib['assets']:
        assert all(v['file'] is None and v['status']=='planned' for v in lib['assets'][duplicate]['variants'].values())
        del lib['assets'][duplicate]
    # The stronger second Leo question is a distinct expression variant, same portrait base.
    expression=lib['assets']['leo.expression.mildly_annoyed.s07.3q']
    expression['variants']['questioning']=dict(copy.deepcopy(expression['variants']['default']),label='questioning; why were you racing without watching')
    for l in plan['lines']:
        if l['line_id']=='S07-L002':l['beats'][0]['image_sequence']['images'][0]['performance']['Leo']['expression_variant']='questioning'
    for l in plan['lines']:
        if l['audio_scene']=='S07':
            for b in l['beats']:
                for im in b['image_sequence']['images']:
                    for binding in im['performance'].values():
                        pose=lib['assets'][binding['pose_id']]['variants'][binding['pose_variant']]
                        binding['pose_sha256']=pose['file']['sha256'] if pose['file'] else None
    write(S/'character_performance_library.json',lib);write(S/'audio_visual_plan.json',plan)
    pair_file=pair['variants']['path_arrival']['file']
    mc=ref('character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png','canonical_identity_milo','identity/anatomy/material/intrinsic palette for Milo only')
    lc=ref('character/characters/lion_and_mouse_v7/Leo/canonical/full-body_leo_neutral_pose_r01.png','canonical_identity_leo','identity/anatomy/material/intrinsic palette for Leo only')
    mg=ref('stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/milo_combined_annotated.jpg','canonical_measurement_milo','Milo visible head/body/width/paw/cream patch baselines; no guide marks in output')
    lg=ref('stories/lion_and_mouse_v7/review/character_performance_consistency_r001/canonical_measurements_r001/leo_combined_annotated.jpg','canonical_measurement_leo','Leo own visible head/mane/body/paw baselines; no guide marks in output')
    requests=[]
    for phase,action in [
        ('rest_nose','Earlier S06-L001-B01-I01: Leo lies awake with head still low/resting as immediately before the narrated head lift. Preserve the same resting trunk, hips, hind legs, tail and body axis as reference 1. Milo is on viewer RIGHT close beside Leo nose, in the low startled nose-contact/landing position before scrambling away to the path. He is ground-supported beside the muzzle, not perched on top of Leo, not pinned or grabbed. No full stand, jump or new location. Keep nose-side contact and plausible support readable. This state precedes the head lift; do not use the later front-paw block.'),
        ('paw_planted','S06-L002-B01-I03: Leo remains lying with head/chest raised as reference 1. His NEAR FRONT paw is extended and planted on the ground immediately beside/in front of Milo to block the path. It is a front limb, never the rear paw used for the S05 trip. Show a continuous anatomically attached foreleg from shoulder through rounded wrist to large clawless paw. Milo stays screen-RIGHT at the path-arrival body scale/position and looks startled toward Leo. The paw blocks his route with clear space beside his body; never touch, cover, step on, trap or grab Milo. Preserve rear legs/tail/trunk and Milo silhouette. This planted front-paw layout becomes the base for later frozen/worried/humbled face-only variants.')]:
        refs=[ref(pair_file['path'],'selected_joint_edit_base','retain both identities, relative proportions, whole-body geometry, screen axis and shared support; only specified action changes'),mc,lc,mg,lg]
        prompt='Edit reference 1, the owner-selected paired Leo+Milo transparent performance. '+action+' Canonical references 2/4 own Milo identity and his own visible surface ratios; 3/5 own Leo identity and his DIFFERENT species-specific ratios. Do not independently resize heads, torsos, ears, paws or characters; preserve same-depth relative design from selected pair. Milo stays lean grey felt with grey felt paws, cream muzzle/belly, moss-green eyes, orange tail, readable neck and continuous hips/legs. Canonical upright head fraction 0.39 +/-0.01 applies only at compatible upright pitch, not to bent/lying poses. Keep Leo canonical mane/skull/ears/trunk and rounded paws. Both mouths closed, toothless; narrator never creates speech shapes. Full pair with margins, genuine transparent alpha. No background, ground plane, cast shadow, props, annotation marks, words or watermark. One output only.'
        v=pair['variants'][phase];out='character/characters/lion_and_mouse_v7/interactions/performance_pairs/leo_milo_s06_'+phase+'_3q_r001_candidate.png'
        requests.append({'sequence':len(requests)+1,'requirement_id':pair['id'],'variant':phase,'revision':'r001','actors':['Leo','Milo'],
                         'output':out,'sidecar':out.replace('.png','.json'),'audio_image_uses':v['image_ids'],'audio':v['audio'],'state_ref':v['state_ref'],
                         'inputs':refs,'tool_arguments':{'prompt':prompt,'referenced_image_paths':[str(R/f['path']) for f in refs],'transparent_background':True}})
    for actor,aid,variant,poseid,uses,action in [
        ('Leo','leo.expression.mildly_annoyed.s07.3q','questioning','leo.s07.dialogue.portrait.3q',['S07-L002-B01-I01'],
         "A sharper but controlled questioning reaction to 'Why were you racing through here without watching where you were going?': one brow raised with a small skeptical crease, amber eyes down toward nearby offscreen Milo on screen-right, slightly tense closed mouth. Mild annoyance, not rage, snarling or frightening aggression."),
        ('Milo','milo.expression.anxious_sincere.3q_left','default','milo.portrait.base.3q_left',['S07-L004-B01-I01'],
         "Anxiously explaining the shortcut and wanting to get home before dark: inner brows gently lifted, worried concentration, earnest eyes looking up-left toward offscreen Leo, tense but closed mouth, no happy smile."),
        ('Milo','milo.expression.sincere.3q_left','default','milo.portrait.base.3q_left',['S07-L005-B01-I01'],
         "A small sincere promise: eyes still looking up-left toward Leo, gentler pleading brows and calm earnest facial tension, closed toothless mouth. Sincerity must be distinct from anxious explanation, without a big happy grin or changed skull/eye anatomy.")]:
        parent=lib['assets'][poseid]['variants']['default']['file']
        refs=[ref(parent['path'],'selected_portrait_edit_base','exact approved head/ears-or-mane/neck/chest geometry, view, body extent and canvas; facial acting only'),mc if actor=='Milo' else lc,mg if actor=='Milo' else lg]
        prompt='Edit ONLY the eyes/eyelids/brows and local facial tension of reference 1, the owner-selected '+actor+' S07 portrait base. '+action+' Keep EXACT head pose/angle, skull/muzzle, eye size and spacing, ears/'+('mane curls' if actor=='Leo' else 'whiskers and cream muzzle')+', neck/shoulders/upper-chest silhouette, visible body extent, crop and image canvas. No zoom, head lift, body rebuild, mirroring or new anatomy. Reference 2 owns canonical identity/material/palette; reference 3 supplies that character\'s own projected surface guides, not new targets. Preserve intrinsic felt colors and texture. Closed mouth at still boundary despite dialogue; no teeth or speech mouth. Genuine transparent alpha, no environment, props, captions, symbols, shadows or watermark. One output only. A reference constrains generation but does not prove exact pixel identity; preserve surrounding body as closely as possible.'
        name=('leo_s07_questioning_expression_3q' if actor=='Leo' else 'milo_s07_'+('anxious_sincere' if 'anxious' in aid else 'sincere')+'_expression_3q_left')
        out='character/characters/lion_and_mouse_v7/'+actor+'/expressions/'+name+'_r001_candidate.png'
        line=next(l for l in plan['lines'] if l['line_id']==uses[0][:8])
        requests.append({'sequence':len(requests)+1,'requirement_id':aid,'variant':variant,'revision':'r001','actors':[actor],
                         'output':out,'sidecar':out.replace('.png','.json'),'audio_image_uses':uses,'audio':line['audio'],
                         'inputs':refs,'tool_arguments':{'prompt':prompt,'referenced_image_paths':[str(R/f['path']) for f in refs],'transparent_background':True}})
    for q in requests:
        assert not (R/q['output']).exists()
        for f in q['inputs']:assert digest(R/f['path'])==f['sha256']
    operation={'schema':'feltwillow.performance-generation-proposal.v1','status':'prepared_pending_concrete_owner_approval','endpoint':'image_gen.imagegen',
               'request_count':5,'outputs_per_request':1,'automatic_retries':0,'estimated_total_cost':None,'pricing':'Built-in current price/model/seed not exposed; cost unknown',
               'scope':'Next two joint action anchors and three S07 face variants, derived from the three newly selected foundations. Other seven joint phases wait for the reviewed low-head/planted-paw references. No scene/background/audio/video generation.',
               'requests':requests}
    write(D/'OPERATION.json',operation)
    before=read(A/'before_audio_visual_plan.json')
    assert plan['world_states']==before['world_states'] and plan['world_events']==before['world_events']
    assert [(l['line_id'],l['text'],l['audio']) for l in plan['lines']]==[(l['line_id'],l['text'],l['audio']) for l in before['lines']]
    write(D/'REUSE_AND_DEPENDENCIES.json',{'approved_foundations':3,'new_requests_prepared':5,'new_candidates_generated':0,
         'reuse_without_new_image':{'S07-L001-B01-I01':'selected Leo portrait base including its accepted facial acting','S07-L003-B01-I01':'selected Milo portrait base including its accepted facial acting'},
         'not_duplicate_expression_pngs':'Base-embedded approved faces are retained; standalone duplicate PNGs are not created for L001/L003.',
         'remaining_joint_phases_after_this_stage':['head_raised_nose','scramble_descent','paw_ready','paw_descending','frozen','worried','humbled'],
         'dependency_policy':'Review new rest and planted-paw anchors before subsequent action or face-only variants. Do not generate independent replacement bodies for frozen/worried/humbled.',
         'planned_alias_deduplication':duplicate+' -> '+preferred,'audio_and_world_state_unchanged':True})
    h=digest(D/'OPERATION.json')
    (D/'REVIEW.md').write_text('# S06/S07 derived pose and expression pass\n\nOwner selected all three first foundations at exact hashes in [owner_acceptance/OWNER_SELECTION.json](owner_acceptance/OWNER_SELECTION.json). Approval is for depicted performances only; technical ratios/contact and scenes remain separate. PNGs and immutable generation receipts unchanged; status sidecars have before snapshots and review hashes.\n\n**Prepared only: five requests to image_gen.imagegen, one transparent output each, no retries. Cost unknown.** [Exact inputs/hashes/prompts/settings](OPERATION.json). Operation SHA-256 `'+h+'`. Not submitted.\n\n1. Paired **rest_nose**: earlier awake, low-head Leo and startled Milo at the nose-side position on viewer right. No later blocking action.\n2. Paired **paw_planted**: same lying/raised Leo, continuous FRONT foreleg and paw planted beside Milo without touching/pinning him. Preserve paired anatomy and Milo placement.\n3. Leo **questioning** face for S07-L002, on the selected portrait body.\n4. Milo **anxious_sincere** face for S07-L004, same left-view body.\n5. Milo **sincere promise** face for S07-L005, same left-view body.\n\nS07-L001 and L003 reuse the selected base depictions/embedded acting; no duplicate files. Seven further paired S06 states remain after these two action anchors: head_raised_nose, scramble_descent, paw_ready, paw_descending, frozen, worried, humbled. Those depend on reviewed low-head/planted-paw hashes, especially the shared planted-body geometry for the last three reactions.\n\nThe original 10-state S06 plan is unchanged in meaning. A redundant planned-only _left_left alias was deduplicated; no generated asset was changed. No new full-standing event, side switch, dialogue mouth, acorn/net state or audio change. No scene/clean-plate reconstruction in this operation. Current per-actor and joint selection scopes remain distinct.\n')
    print('Recorded 3 selections; prepared 5 exact derived requests, no generation.')

if __name__=='__main__':main()
