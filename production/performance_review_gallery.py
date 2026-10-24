"""Read-only, reusable performance-library cards and local audio review."""
import argparse
import html
import json
import os
from pathlib import Path

try:
    from . import character_performance as cp
except ImportError:
    import character_performance as cp


def comparison_is_current(library, report):
    """Old comparison pixels must not appear to describe replacement assets."""
    for row in report.get('rows',[]):
        variant=library['assets'].get(row['asset_id'],{}).get('variants',{}).get(row['variant'],{})
        current=variant.get('file') or {}
        if current.get('path')!=row['source']['path'] or current.get('sha256')!=row['source']['sha256']:
            return False
    return bool(report.get('rows'))


def build(root,story):
    folder,plan,chars,locs,library=cp.load(root,story)
    errors=cp.validate(library,plan,chars,root,folder=folder)
    if errors:raise ValueError('\n'.join(errors))
    if (folder/'scene_image_selection_s01_s05.json').is_file():
        try:
            from .selected_scene_review import build as build_selected
        except ImportError:
            from selected_scene_review import build as build_selected
        return build_selected(root,story)
    target=folder/cp.AUDIT/'pose_library'
    target.mkdir(parents=True,exist_ok=True)
    def url(path):
        # Resolve trusted registry paths through the existing repository boundary.
        return html.escape(os.path.relpath(cp.av.local(root,path),target),quote=True)
    h=html.escape
    rows=cp.usage_report(library,plan)['uses']
    profiles=[]
    canonical_panels=[]
    for actor,policy in library.get('anatomy_policies',{}).items():
        profile=policy.get('ratio_profile',{})
        table=[]
        for name,metric in profile.get('ratios',{}).items():
            label='No adopted target yet' if metric['target'] is None else f"{metric['target']} ± {metric['tolerance']} (absolute ratio units)"
            observation=metric.get('reference_measurement')
            measured=(f"{observation['value']:.2f} (interval {observation['interval'][0]:.2f}–{observation['interval'][1]:.2f})" if observation else 'Not measurable / pending')
            table.append('<tr><td>'+h(name)+'</td><td>'+h(label)+'</td><td>'+h(measured)+'</td><td>'+h(metric['definition'])+'</td><td>'+h(metric['comparability'])+'</td></tr>')
        profiles.append('<details><summary>'+h(actor+' · '+profile.get('calibration_status','pending'))+'</summary><p>Own canonical SHA-256: <code>'+h(policy['canonical']['sha256'])+'</code></p><p>Observation identity: '+h(profile.get('observation_identity_status','pending'))+'. Baselines are projected surface measurements; they do not automatically become design targets.</p><table><thead><tr><th>Ratio</th><th>Target</th><th>Measured baseline</th><th>Definition</th><th>Comparable when</th></tr></thead><tbody>'+''.join(table)+'</tbody></table></details>')
        annotation=folder/cp.AUDIT/'canonical_measurements_r001'/(actor.lower()+'_combined_annotated.jpg')
        if annotation.is_file():
            canonical_panels.append('<section><h2>'+h(actor)+' · all canonical measurements</h2><p>'+h(profile.get('observation_identity_status','pending'))+'</p><a href="'+url(str(annotation.relative_to(root)))+'"><img class="comparison" loading="lazy" src="'+url(str(annotation.relative_to(root)))+'" alt="'+h(actor)+' combined canonical height width face and paw measurements"></a><p>All previous landmarks and new widths, cream patch, hands and paws in one image. Numbered dots are coordinates; W labels are horizontal spans. No hidden joints inferred. <a href="../canonical_measurements_r001/review.html">Full coordinate/width legends, native pixels, ratio tables and uncertainty</a></p></section>')
    cards=[]
    history=[]
    for aid,asset in library['assets'].items():
        ordered=asset.get('review_variant_order',list(asset['variants']))
        for variant_name in ordered:
            variant=asset['variants'][variant_name]
            file=variant.get('file')
            if not file:continue
            if variant.get('active_review_disposition') == 'superseded_by_turn_exit_reuse':
                history.append({'asset_id':aid,'variant':variant_name,'file':file,
                                'reason':'Owner requested reuse of turn_exit; original bytes preserved'})
                continue
            for previous in variant.get('superseded_candidates',[]):
                history.append({'asset_id':aid,'variant':variant_name,**previous})
            cp.checked_file(root,file)
            matched=[r for r in rows if (r.get('pose_id')==aid and r.get('pose_variant')==variant_name) or (r.get('expression_id')==aid and r.get('expression_variant')==variant_name)]
            image_ids=sorted({r['image_id'] for r in matched})
            scenes=sorted({r['line_id'].split('-')[0] for r in matched})
            # Include current S01-S05 review audio; later uses remain IDs.
            audio={r['line_id']:r['audio_wav'] for r in matched if r['line_id'].startswith(('S01-','S02-','S03-','S04-','S05-'))}
            players=[]
            for lid,wav in sorted(audio.items()):
                if cp.av.local(root,wav).is_file():
                    players.append('<label>'+h(lid)+'<audio controls preload="none" src="'+url(wav)+'"></audio></label>')
            side=cp.av.read(cp.av.local(root,file['sidecar']['path']))
            note=side.get('technical_review','No visual verdict recorded')
            if not isinstance(note,str):note=json.dumps(note,ensure_ascii=False)
            review=variant.get('candidate_review',{})
            if review.get('image_sha256')==file['sha256']:
                note=review['observation']+' '+note
            component=variant.get('component_review')
            if component:
                note = ('Body: '+component['body']+'; face: '+component['face']+
                        '. Original face pixels have not been changed. '+note)
            blockers=cp.anatomy_blockers(library,asset['actor'],variant)
            anatomy=variant.get('anatomy_review',{}).get('status','pending')
            category='portrait' if asset['asset_type']=='portrait_base' else 'expression' if asset['asset_type']=='expression' else 'body'
            cards.append('<article data-kind="'+category+'" data-scenes="'+' '.join(scenes)+'" data-search="'+h((aid+' '+variant_name+' '+' '.join(image_ids)).lower(),quote=True)+'"><h2>'+h(aid+':'+variant_name)+'</h2><p class="badge">Pose/acting: '+h(variant['status'])+'</p><p>Anatomy: '+h(anatomy)+'</p><a href="'+url(file['path'])+'" target="_blank"><img loading="lazy" src="'+url(file['path'])+'" alt="'+h(aid+':'+variant_name,quote=True)+'"></a><p class="filename">'+h(Path(file['path']).name)+'</p><p>'+h(note)+'</p><p class="warning">'+h('; '.join(blockers) or 'No anatomy evidence blockers; scene/prop review remains separate')+'</p><details><summary>Audio-linked image uses ('+str(len(image_ids))+')</summary><p>'+h(', '.join(image_ids) or 'Reusable angle-base dependency; no direct scene assignment')+'</p>'+''.join(players)+'</details><details><summary>Source evidence</summary><p>Image SHA-256: <code>'+h(file['sha256'])+'</code></p><p>Canonical SHA-256: <code>'+h(asset['canonical']['sha256'])+'</code></p><p>View / head: '+h(asset['view']+' / '+variant['head_orientation'])+'</p><p>Card fit is a display choice, not a common anatomical pixel scale.</p></details></article>')
    comparison=folder/cp.AUDIT/'milo_anatomy_r001/normalized_comparison.jpg'
    comparison_report=folder/cp.AUDIT/'milo_anatomy_r001/PROJECTED_LANDMARKS.json'
    current_comparison=comparison_report.is_file() and comparison_is_current(library,cp.av.read(comparison_report))
    pending=[]
    for aid,asset in library['assets'].items():
        if asset['asset_type']!='expression':continue
        if any(r['line_id'].startswith(('S01-','S02-','S03-','S04-','S05-')) and r.get('expression_id')==aid for r in rows):
            for name,v in asset['variants'].items():
                if not v.get('file'):pending.append('<li>'+h(aid+':'+name)+' — planned; no image generated</li>')
    summary='<section><h2>Current review status</h2><p><strong>'+str(len(cards))+' current generated performance assets</strong>. The registry supplies one current file per pose/variant. '+str(len(history))+' superseded versions are excluded from these cards and preserved as history; current candidates remain marked by their own approval/readiness state.</p><p><strong>Milo upright projected head fraction: 0.39 ±0.01 (0.38–0.40).</strong> Canonical measured baseline is approximately 0.39 with annotation uncertainty. Target tolerance is not measurement precision.</p><p>Pose/acting approval does not establish anatomy congruence or acorn fit. Known body-facing/contact concerns remain on the relevant cards. Leo current identity bytes are owner-reconciled; his numerical design targets and pose/scene approvals remain separate.</p><details><summary>Missing S01–S05 expressions ('+str(len(pending))+')</summary><ul>'+''.join(pending)+'</ul></details></section>'
    batch=folder/cp.AUDIT/'s04_s05_pose_planning_r001/EXECUTION.json'
    acting_review=folder/cp.AUDIT/'s04_s05_acting_repairs_r002/ACTING_REQUIREMENTS.json'
    if acting_review.is_file():
        requirements=cp.av.read(acting_review)['uses']
        table=''.join('<tr><td>'+h(r['image_id'])+'</td><td>'+h(r['intent'])+'</td><td>'+h(r['expression_id'])+'</td><td>'+h(r['application_status'])+'</td></tr>' for r in requirements)
        journal=acting_review.parent/'EXECUTION.json'
        completed=cp.av.read(journal)['completed'] if journal.is_file() else 0
        status=(str(completed)+' of 7 approved requests saved as candidates; no retries. Two body repairs and five expression references await owner review.' if completed else 'Seven requests prepared, not submitted: two body repairs and five expressions.')
        summary+='<section><h2>S04–S05 facial acting corrections</h2><p>Twelve body depictions retained by the owner; facial acting remains pending. Turn entry reuses turn_exit; rejected entry is archived. '+h(status)+' Cost unknown. Expressions are saved under Milo/expressions and still require local head-angle application review. Focus faces retain a slight smile; startled/panic/landing strength and geometric consistency need review.</p><details open><summary>Per-image expression and scene integration status</summary><table><tr><th>Image</th><th>Acting intent</th><th>Expression reference</th><th>Applied to scene?</th></tr>'+table+'</table></details></section>'
    face_batch=folder/cp.AUDIT/'s05_trip_fall_face_application_r003/EXECUTION.json'
    if face_batch.is_file():
        completed=cp.av.read(face_batch)['completed']
        face_keys=[('milo.trip.rear_paw.3q','trip')]+[('milo.tumble.flank_to_face.3q',v) for v in ('support_lost','tumble','roll')]
        selected=sum(library['assets'][aid]['variants'][name]['status'] in cp.APPROVED for aid,name in face_keys)
        summary+='<section><h2>S05 trip/fall · pose-local face edits</h2><p>'+str(completed)+' of 4 approved requests saved: trip, support_lost, tumble and roll. '+str(selected)+' selected by the owner for performance use at exact hashes. Their current cards show worried/panicked faces; old smiling versions are archived. Numerical anatomy, body preservation evidence and scene/contact readiness remain separate. These pose edits are not applied scene images. No retries. No full unit-test suite run for this image update.</p><p><a href="?q=milo.trip.rear_paw.3q">Trip poses</a> · <a href="?q=milo.tumble.flank_to_face.3q">Tumble/roll poses</a></p></section>'
    leo_proposal=folder/cp.AUDIT/'leo_s05_foundations_r002/OPERATION.json'
    if leo_proposal.is_file():
        journal=leo_proposal.parent/'EXECUTION.json'
        completed=cp.av.read(journal)['completed'] if journal.is_file() else 0
        selected=sum(library['assets'][aid]['variants']['default']['status'] in cp.APPROVED for aid in ('leo.sleep.rear_paw_path.3q','leo.portrait.base.3q'))
        status=(str(completed)+' of 2 approved requests saved. '+str(selected)+' selected by the owner for performance depiction. Sleeping cutout has a broad translucent halo; portrait mane clearance is tight at the side edges. Technical clean-layer/geometry and scene/contact review remain separate.' if completed else 'Two requests prepared, not submitted.')
        summary+='<section><h2>Leo S05 · foundations</h2><p>'+h(status)+' One sleeping full body serves L001–L009; the resting-head portrait base establishes L010–L011 geometry. After base review, closed/open-eye variants will reuse its mane/ear/neck/chest extent. Leo uses his own canonical ratios. Cost unknown; no retries. No new approval inferred.</p><p><a href="?q=leo.">Show Leo candidates</a></p></section>'
    scene_proposal=folder/'review/scene_compositions/s04_s05_setup_r001/OPERATION.json'
    if scene_proposal.is_file():
        execution_path=scene_proposal.parent/'EXECUTION.json'
        scene_execution=cp.av.read(execution_path) if execution_path.is_file() else {'outputs':[]}
        scene_rows=list(scene_execution['outputs'])
        revised_setup=scene_proposal.parent/'setup_reference_pack_r002/EXECUTION.json'
        if revised_setup.is_file():scene_rows.extend(cp.av.read(revised_setup)['outputs'])
        owner_sequence=folder/'review/scene_compositions/s05_owner_sequence_through_trip_r003'
        if (owner_sequence/'OWNER_DIRECTION.json').is_file():
            # The old joint L005 scene reveals Leo too early under owner direction.
            # Preserve its file/receipt in history; exclude it from current cards.
            scene_rows=[r for r in scene_rows if r['image_id']!='S05-L005-B01-I01']
        sequence_execution=owner_sequence/'EXECUTION.json'
        if sequence_execution.is_file():
            scene_rows.extend(cp.av.read(sequence_execution)['outputs'])
        contact_repair=folder/'review/scene_compositions/s05_contact_scene_repair_r006'
        if (contact_repair/'EXECUTION.json').is_file():
            scene_rows.extend(cp.av.read(contact_repair/'EXECUTION.json').get('outputs',[]))
        local_contact=folder/'review/scene_compositions/s05_contact_local_composition_r007'
        if (local_contact/'EXECUTION.json').is_file():
            scene_rows.extend(cp.av.read(local_contact/'EXECUTION.json').get('outputs',[]))
        continuation=folder/'review/scene_compositions/s05_local_continuation_r008'
        if (continuation/'EXECUTION.json').is_file():
            scene_rows.extend(cp.av.read(continuation/'EXECUTION.json').get('outputs',[]))
        leo_portraits=folder/'review/scene_compositions/s05_leo_portrait_completion_r009'
        if (leo_portraits/'EXECUTION.json').is_file():
            scene_rows.extend(cp.av.read(leo_portraits/'EXECUTION.json').get('outputs',[]))
        grounding=folder/'review/scene_compositions/s05_contact_grounding_r010'
        if (grounding/'EXECUTION.json').is_file():
            scene_rows.extend(cp.av.read(grounding/'EXECUTION.json').get('outputs',[]))
        expression_review=folder/'review/scene_compositions/s05_leo_expression_portraits_r011'
        if (expression_review/'EXECUTION.json').is_file():
            scene_rows.extend(cp.av.read(expression_review/'EXECUTION.json').get('outputs',[]))
        # Current cards use the latest receipt per image ID; historical bytes stay intact.
        scene_rows=list({r['image_id']:r for r in scene_rows}.values())
        observations_path=scene_proposal.parent/'VISUAL_OBSERVATIONS.json'
        observations={r['image_id']:r['observation'] for r in cp.av.read(observations_path)['images']} if observations_path.is_file() else {}
        setup_observations=revised_setup.parent/'VISUAL_OBSERVATIONS.json'
        if setup_observations.is_file():observations.update({r['image_id']:r['observation'] for r in cp.av.read(setup_observations)['images']})
        sequence_observations=owner_sequence/'VISUAL_OBSERVATIONS.json'
        if sequence_observations.is_file():observations.update({r['image_id']:r['observation'] for r in cp.av.read(sequence_observations)['images']})
        if (contact_repair/'VISUAL_OBSERVATIONS.json').is_file():
            observations.update({r['image_id']:r['observation'] for r in cp.av.read(contact_repair/'VISUAL_OBSERVATIONS.json')['images']})
        if (local_contact/'VISUAL_OBSERVATIONS.json').is_file():
            observations.update({r['image_id']:r['observation'] for r in cp.av.read(local_contact/'VISUAL_OBSERVATIONS.json')['images']})
        if (continuation/'VISUAL_OBSERVATIONS.json').is_file():
            observations.update({r['image_id']:r['observation'] for r in cp.av.read(continuation/'VISUAL_OBSERVATIONS.json')['images']})
        if (leo_portraits/'VISUAL_OBSERVATIONS.json').is_file():
            observations.update({r['image_id']:r['observation'] for r in cp.av.read(leo_portraits/'VISUAL_OBSERVATIONS.json')['images']})
        if (grounding/'VISUAL_OBSERVATIONS.json').is_file():
            observations.update({r['image_id']:r['observation'] for r in cp.av.read(grounding/'VISUAL_OBSERVATIONS.json')['images']})
        if (expression_review/'VISUAL_OBSERVATIONS.json').is_file():
            observations.update({r['image_id']:r['observation'] for r in cp.av.read(expression_review/'VISUAL_OBSERVATIONS.json')['images']})
        selection_path=scene_proposal.parent/'S04_OWNER_SELECTION.json'
        selected_scenes={r['image_id']:r['sha256'] for r in cp.av.read(selection_path)['images']} if selection_path.is_file() else {}
        if (owner_sequence/'OWNER_SELECTION.json').is_file():
            selected_scenes.update({r['image_id']:r['sha256'] for r in cp.av.read(owner_sequence/'OWNER_SELECTION.json')['images']})
        if (continuation/'OWNER_SELECTION.json').is_file():
            selected_scenes.update({r['image_id']:r['sha256'] for r in cp.av.read(continuation/'OWNER_SELECTION.json')['images']})
        expression_review=folder/'review/scene_compositions/s05_leo_expression_portraits_r011'
        if (expression_review/'OWNER_SELECTION.json').is_file():
            selected_scenes.update({r['image_id']:r['sha256'] for r in cp.av.read(expression_review/'OWNER_SELECTION.json')['images']})
        owner_review=scene_proposal.parent/'CURRENT_OWNER_REVIEW.json'
        revision=cp.av.read(owner_review).get('revision_requested',{}) if owner_review.is_file() else {}
        scene_cards=[]
        for row in scene_rows:
            cp.checked_file(root,row)
            cp.checked_file(root,row['sidecar'])
            side=cp.av.read(cp.av.local(root,row['sidecar']['path']))
            if side['sha256']!=row['sha256'] or side['image_id']!=row['image_id']:
                raise ValueError('Scene review sidecar does not identify candidate bytes')
            audio=side['audio']
            cp.checked_file(root,{'path':audio['wav'],'sha256':audio['sha256']})
            note=observations.get(row['image_id'],'Visual review pending')
            if row['image_id']=='S05-L005-B01-I01' and sequence_execution.is_file():
                reuse=cp.av.read(owner_sequence/'IMAGE_REUSE.json')
                if reuse['sha256']!=row['sha256'] or reuse['path']!=row['path']:
                    raise ValueError('Shared L005/L006 image bytes differ')
                cp.checked_file(root,{'path':reuse['audio']['wav'],'sha256':reuse['audio']['sha256']})
                note+=' S05-L006 reuses these exact pixels with no cut or additional generated image.'
                reuse_audio='<p>S05-L006 · '+h(reuse['audio']['metadata_text'])+' · same image</p><audio controls preload="none" src="'+url(reuse['audio']['wav'])+'"></audio>'
            else:
                reuse_audio=''
            status='Pending owner review · anatomy/contact unmeasured'
            if selected_scenes.get(row['image_id'])==row['sha256']:
                status='Owner-selected scene depiction · technical observations retained'
            if revision.get('image_id')==row['image_id'] and revision.get('sha256')==row['sha256']:
                status='Revision requested · remove ground dust and move Milo modestly left'
                note=revision['direction']+' Earlier observation: '+note
            scene_cards.append('<article data-kind="scene" data-scenes="'+h(side['line_id'].split('-')[0])+'" data-search="'+h(('scene '+row['image_id']+' '+side['line_id']+(' S05-L006' if reuse_audio else '')).lower(),quote=True)+'"><h2>'+h(row['image_id'])+' · scene candidate</h2><p class="badge">'+h(status)+'</p><a href="'+url(row['path'])+'" target="_blank"><img loading="lazy" src="'+url(row['path'])+'" alt="'+h(row['image_id'])+' scene candidate"></a><p>'+h(audio['metadata_text'])+'</p><audio controls preload="none" src="'+url(audio['wav'])+'"></audio><p>'+h(note)+'</p><details><summary>Source evidence</summary><p>SHA-256 <code>'+h(row['sha256'])+'</code></p><p>'+h(row['path'])+'</p><p>Original PNG and receipt preserved. This scene is a candidate, not a reusable performance asset or approved clip.</p></details></article>')
            if reuse_audio:scene_cards[-1]=scene_cards[-1].replace('</article>',reuse_audio+'</article>')
        sequence_note=('S05-L001 is owner-selected. Seven approved requests saved: S04 dust correction plus six S05 candidates. L002–L004 show mane/grass, eyes and rear paw; L002 framing needs review. L005–L006 share identical Milo-only pixels and separate audio; L007 is Milo portrait. L008 is the first joint contact candidate: open mouth and suspected Milo identity/anatomy drift are flagged, scale/contact remain unmeasured. Stopped here; no later motion generated. Old joint L005 is archived, not current.' if (owner_sequence/'OWNER_DIRECTION.json').is_file() else 'No S05 selection inferred; shared setup requires review before connected frames.')
        if (local_contact/'EXECUTION.json').is_file():
            sequence_note='L008 now shows local composite r003: exact selected r004 Milo layer uniformly resized over original L001 Leo/background. Zero background pixels changed outside actor alpha; no body redraw, recoloring or face swap. Grounding/contact, actor scale, light and cutout integration await owner review; no new shadow. Earlier generative L008 versions rejected and archived. L006 reuses L005 pixels with separate audio. L002 mane/grass framing still needs review. Stopped at L008 contact.'
        if (continuation/'EXECUTION.json').is_file():
            sequence_note='L008-I02 r003 is owner-selected. Four new local candidates continue with the selected trip/support_lost/tumble/roll layers at anchor scale 0.32; no anatomy redraw or recolor. Exact original background is retained outside each actor alpha. Path, contact, occlusion, light and proportions across distinct source poses require review; same source scale alone does not certify matching anatomy. Missing approach/forward-pitch/landing and Leo eye/portrait states remain held. No new shadows or paid calls.'
            summary+='<section><h2>S05 selected contact anchor · scene measurements</h2><p>Canvas 1672 × 941; Milo alpha &gt;8 bounds are 405 × 346 px including ears and tail: 24.22% of frame width, 36.77% of frame height. Whole-layer scale 0.32. These are pose/setup extents, not anatomical height or canonical design targets. Bent Milo and sleeping Leo do not establish a standing-height ratio; camera/depth remain unknown.</p><p><a href="'+url(str((continuation/'ANCHOR_MEASUREMENTS.md').relative_to(root)))+'">Measurement method and limitations</a></p><img class="comparison" src="'+url(str((continuation/'comparison.jpg').relative_to(root)))+'" alt="Four new S05 local composition candidates"></section>'
        if (leo_portraits/'VISUAL_OBSERVATIONS.json').is_file():
            sequence_note+=' L010 eyes-open and L011 questioning portraits now saved, pending owner review: same resting scene source, closed mouths; L011 reaction is subtle. Geometry, gaze and crop/body match unmeasured. Source closed-eyes crop remains reference-only. Missing approach/forward-pitch/landing and L010 start remain held.'
            summary+='<details open><summary>Leo resting portraits · source and candidates</summary><p>Source crop is scene geometry only, not an approved portrait master. Two approved requests saved, no retries; cost unknown. Review amber eyes/gaze, reaction and matching mane/head/chest extent. No pixel-lock pass inferred.</p><img class="comparison" src="'+url(str((leo_portraits/'comparison.jpg').relative_to(root)))+'" alt="Closed-eyes reference and two Leo portrait candidates"></details>'
        if (grounding/'EXECUTION.json').is_file():
            sequence_note='Current contact/grounding revisions: L008-I02 moves Milo 32 px left; L008-I04 aligns foot to rear-paw rim with contact shadow and foreground fur overlap; L009-I03 lowers the roll toward ground with shadow. Whole-actor scale stays 0.32 with source RGB/anatomy unchanged. These three new hashes await owner review; prior I02 selection belongs to its older bytes. L009-I01/I02 pose depictions retained at unchanged hashes, not new full-scene/video approvals. Background pixels are exact outside explicitly recorded actor/shadow effect masks; shadows intentionally change local lighting. Leo portraits remain pending; missing approach/forward-pitch/landing and L010 start remain held.'
            summary+='<details open><summary>S05 contact and grounding · before / revised</summary><p>Local repairs only: no AI redraw, recoloring or paid calls. Contact, occlusion, footing and smooth trajectory still require owner review. Earlier selected-frame measurements describe the archived source placement; the same layer scale is retained.</p><img class="comparison" src="'+url(str((grounding/'comparison.jpg').relative_to(root)))+'" alt="Before and revised Milo placement, rear-paw contact and ground roll"></details>'
        if (expression_review/'OWNER_SELECTION.json').is_file():
            sequence_note+=' Latest owner decision: these three grounding revisions pass provisionally at their current hashes; technical motion/physical certification remains separate. Leo expressions require revision: newly-awakened L010 vs clearly startled-questioning L011, matching tight portrait framing with blurred background. Milo remains beside the nose offscreen, never removed from world state. Two concrete portrait-edit requests prepared, not submitted.'
        if (expression_review/'VISUAL_OBSERVATIONS.json').is_file():
            sequence_note='Three contact/grounding revisions provisionally owner-selected. Latest L010/L011 r002 portraits show newly-awake/confused vs stronger startled-questioning acting, blurred backgrounds, Milo offscreen but still at nose in world state. Two requests completed without retries; cost unknown. Upper mane clips at frame edge, and L011 head placement/chest/forearm extent differ from L010; no matched-geometry pass. Both await owner review. Earlier portrait versions archived; remaining approach/forward-pitch/landing and L010 start held.'
            summary+='<details open><summary>Latest tight Leo expression portraits · r002</summary><p>Newly awakened / startled question. Review upper mane clearance and head/upper-body framing mismatch; no automatic anatomy, geometry or performance-master approval.</p><img class="comparison" src="'+url(str((expression_review/'comparison.jpg').relative_to(root)))+'" alt="Latest two Leo expression portrait candidates"></details>'
        summary+='<section><h2>S04–S05 current scenes · '+str(len(scene_cards))+' unique images</h2><p>Four S04 starts are owner-selected; revised S04-L005 awaits review. '+h(sequence_note)+'</p><p><a href="?q=scene&amp;kind=scene">Show only scenes</a> · <a href="?q=S05&amp;kind=scene">Show S05 scenes</a></p><div class="grid">'+''.join(scene_cards)+'</div></section>'
    if batch.is_file():
        execution=cp.av.read(batch)
        unresolved=[a['image_asset'] for a in execution.get('attempts',{}).values() if a['status']!='completed_candidate_saved']
        summary+='<section id="s04-s05-current"><h2>S04–S05 new Milo candidates</h2><p>'+str(execution['completed'])+' of '+str(execution['requested'])+' approved requests have saved candidates. No retries. Cost unknown. Missing/unresolved: '+h(', '.join(unresolved) or 'none')+'.</p><p><a href="?q=S04">Show S04 poses</a> · <a href="?q=S05">Show S05 poses</a> · <a href="?">Show all</a></p><p>Cutout anatomy, gait phase, backward/forward balance, paw contact and flank-to-nose trajectory still need review. Leo sleeping setup must establish contact clearance. No new pose is owner-approved by generation.</p></section>'
    next_stage=folder/'review/scene_compositions/s01_s03_performance_r002/review.html'
    if next_stage.is_file():
        summary+='<p><a href="../../scene_compositions/s01_s03_performance_r002/review.html">S01–S03 composed scene candidates · audio and comparisons</a></p>'
    if canonical_panels:
        summary+='<details open><summary>Combined annotated canonical images: Milo and Leo · all measurements</summary><p>Height, face, widths, cream patch and paws are shown together. Width and height must both agree in compatible views. Current candidates require matched-view measurements; generation guidance does not establish a proportion pass. Portraits use applicable head/ear/eye ratios; a cropped belly is not measurable.</p><div class="grid">'+''.join(canonical_panels)+'</div></details>'
    compare='<details open><summary>Current annotated comparison</summary><p>Uniform crown-to-sole normalization; manual ±20 px; head pitch differs. Screening only. Source images unchanged.</p><img class="comparison" src="'+url(str(comparison.relative_to(root)))+'"></details>' if comparison.is_file() and current_comparison else '<p>Earlier anatomy comparison is archived; it does not describe all current replacement bytes.</p>'
    style='body{font:17px system-ui;background:#252821;color:#eee;margin:26px}a{color:#c7edab}header{max-width:1100px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:22px}article{background:#343a31;padding:16px;min-width:0;border-radius:8px}h2{font-size:18px;overflow-wrap:anywhere}article img{display:block;width:100%;height:auto;background:repeating-conic-gradient(#ddd 0% 25%,#fff 0% 50%) 50% / 24px 24px}body.native article{overflow:auto}body.native article img{width:auto;max-width:none}code,.filename{font-size:12px;overflow-wrap:anywhere}.badge,.warning{color:#ffdb91}audio{width:100%;margin:6px 0 14px}details{margin:14px 0}summary{cursor:pointer}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border:1px solid #697160;padding:8px;text-align:left}nav{display:flex;gap:15px;flex-wrap:wrap;align-items:center;margin:20px 0}input,select{font:inherit}.comparison{max-width:100%;height:auto}article[hidden]{display:none}'
    script="""const search=document.querySelector('#search'),kind=document.querySelector('#kind');function filter(){document.querySelectorAll('article').forEach(c=>c.hidden=!(c.dataset.search.includes(search.value.toLowerCase())&&(kind.value==='all'||c.dataset.kind===kind.value)))}search.addEventListener('input',filter);kind.addEventListener('change',filter);document.querySelector('#native').addEventListener('change',e=>document.body.classList.toggle('native',e.target.checked));document.querySelectorAll('audio').forEach(p=>p.addEventListener('play',()=>document.querySelectorAll('audio').forEach(q=>{if(q!==p)q.pause()})));"""
    page='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Character pose library review</title><style>'+style+'</style></head><body><header><h1>Character pose library · '+h(story)+'</h1><p>Reusable read-only review. Pose/acting selection, anatomy evidence and scene/prop readiness are separate. Original PNGs and receipts remain unchanged.</p><p>Each character owns its canonical-bound ratios; current targets and measured baselines appear separately below. Portraits and bent/foreshortened poses use applicable local ratios, not whole-body fraction.</p><p><a href="../canonical_measurements_r001/review.html">Canonical annotations and measured ratios for Milo and Leo</a></p></header>'+summary+''.join(profiles)+compare+'<nav><label>Find pose or image ID <input id="search" type="search"></label><label>Type <select id="kind"><option value="all">All</option><option value="body">Body poses</option><option value="portrait">Portrait bases</option><option value="scene">Scene candidates</option><option value="expression">Expressions</option></select></label><label><input id="native" type="checkbox"> Native size (scroll)</label></nav><main class="grid">'+''.join(cards)+'</main><script>'+script+'</script></body></html>'
    page=page.replace('</script>',"const initialKind=new URLSearchParams(location.search).get('kind');if(initialKind){document.querySelector('#kind').value=initialKind;}const initialQuery=new URLSearchParams(location.search).get('q');if(initialQuery){document.querySelector('#search').value=initialQuery;document.querySelector('#search').dispatchEvent(new Event('input'));}</script>")
    (target/'review.html').write_text(page+'\n')
    cp.av.write(target/'HISTORY_INDEX.json',{'scope':'superseded files; excluded from active pose cards','files':history})
    return {'gallery':str((target/'review.html').relative_to(root)),'generated_assets_shown':len(cards),'source_image_changes':0,'provider_calls':0}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--story',required=True);args=p.parse_args()
    import json
    print(json.dumps(build(cp.ROOT,args.story),indent=2))


if __name__=='__main__':main()
