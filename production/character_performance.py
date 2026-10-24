#!/usr/bin/env python3
"""V7 performance planning, evidence and dry-run proposals. No provider calls."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import html
import json
import math
from pathlib import Path
import re
import sys

try:
    from . import audio_visual_plan as av
except ImportError:
    import audio_visual_plan as av

ROOT = av.ROOT
SCHEMA = 'feltwillow.character-performance.v1'
LIBRARY = 'character_performance_library.json'
AUDIT = 'review/character_performance_consistency_r001'
APPROVED = {'owner_selected_for_performance', 'approved_for_scene_use'}
STATUSES = {'planned', 'candidate_pending_owner_review'} | APPROVED
KINDS = {'pose', 'locomotion_key', 'portrait_base', 'expression', 'interaction'}
VIEWS = {'front', 'rear', 'profile', 'three_quarter'}
FACINGS = {'screen_left', 'screen_right', 'toward_camera', 'away_from_camera'}
SUPPORTS = {'ground', 'airborne', 'ground_rolling', 'unbalanced_paw_contact'}
AUTHORITIES = {'identity_anatomy_material_palette', 'pose_only', 'expression_only',
               'portrait_geometry_only', 'historical_inspiration_only'}


def load(root, story):
    folder, plan, chars, locs = av.load(root, story)
    if story != 'lion_and_mouse_v7':
        raise ValueError('Performance workflow is version-local to lion_and_mouse_v7')
    return folder, plan, chars, locs, av.read(folder/LIBRARY)


def uses(plan):
    """Derived assignments only; no second authored used-by list."""
    for line in plan['lines']:
        for beat in line['beats']:
            for image in beat['image_sequence']['images']:
                for actor, binding in image.get('performance', {}).items():
                    yield line, beat, image, actor, binding


def checked_file(root, record):
    """Structural path/hash validation also works when no checkout is supplied."""
    if not isinstance(record.get('path'),str) or not record['path'] or '\\' in record['path']:
        raise ValueError('invalid repository reference path')
    path = av.source_file(root, record['path']) if root is not None else av.local(ROOT, record['path'])
    if not re.fullmatch('[0-9a-f]{64}', record['sha256']):
        raise ValueError('invalid SHA-256')
    if root is not None and (not path.is_file() or av.digest(path) != record['sha256']):
        raise ValueError(f'missing or changed bytes: {record["path"]}')
    return path


def canonical_record(chars, actor):
    entry = chars['characters'][actor]
    return {'id':entry['asset_id'], **{k:entry['canonical'][k] for k in ('path','sha256')}}


def horizontal_review_blockers(library, actor, variant):
    profile=library.get('anatomy_policies',{}).get(actor,{}).get('ratio_profile',{})
    if not profile.get('horizontal_review_policy',{}).get('required'):return []
    asset=next((a for a in library['assets'].values() if a['actor']==actor and any(v is variant for v in a['variants'].values())),None)
    scope='portrait' if asset and asset['asset_type'] in {'portrait_base','expression'} else 'body'
    categories=('head_width','ear_width','eye_spacing') if scope=='portrait' else ('body_bulk','cream_patch','limb_bulk')
    review=variant.get('anatomy_review',{}).get('horizontal_review',{})
    if (review.get('scope')!=scope or not review.get('evidence') or
            any(review.get('checks',{}).get(k)!='matched_in_compatible_view' for k in categories)):
        return [f'{actor}: horizontal {scope} evidence pending; height alone cannot certify widths/cream patch']
    return []


def anatomy_blockers(library, actor, variant):
    """Art approval never proves comparable anatomy or prop contact."""
    policy=library.get('anatomy_policies',{}).get(actor)
    blockers=list(variant.get('technical_use_blockers',[]))
    if not policy:return blockers
    if policy.get('calibration_status')=='blocked_canonical_hash_reconciliation':
        return blockers+[f'{actor}: own canonical hash must be reconciled before ratio calibration']
    review=variant.get('anatomy_review',{})
    file=variant.get('file') or {}
    if (review.get('status')!='matched_reviewed_reference' or
            review.get('image_sha256')!=file.get('sha256') or
            review.get('reference_sha256')!=policy['proportion_reference']['sha256'] or
            ('ratio_profile' in policy and review.get('profile_sha256')!=ratio_profile_digest(policy['ratio_profile'])) or
            not review.get('evidence') or not review.get('comparison_method')):
        blockers.append(f'{actor}: anatomy match pending; pose/acting approval does not certify proportions')
    return blockers+horizontal_review_blockers(library,actor,variant)


def ratio_profile_digest(profile):
    return hashlib.sha256(json.dumps(profile,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def immutable_errors(root, folder):
    """Append audit evidence; never rewrite historical generation receipts."""
    before = folder/AUDIT/'BEFORE.json'
    if not before.exists():
        return ['Missing pre-change audit evidence']
    errors = []
    for record in av.read(before)['files']:
        path = record['path']
        # These authored files are intentionally migrated, and have exact before snapshots.
        if Path(path).name in {'audio_visual_plan.json','character_library.json'}:
            continue
        if Path(path).name == 'location_library.json':
            # Authored location policy changed at the owner's direction. Verify
            # the exact historical snapshot rather than freezing live planning.
            snapshot = folder / 'review/character_performance_consistency_r001/before_location_library.json'
            if snapshot.is_file() and av.digest(snapshot) == record['sha256']:
                continue
        try:
            checked_file(root, record)
        except (ValueError, OSError, KeyError) as exc:
            errors.append(f'Immutable source: {exc}')
    return errors


def _decision(root, asset, name, variant):
    decision = variant.get('owner_decision')
    if not isinstance(decision, dict):
        raise ValueError('owner decision required, scoped to exact performance bytes')
    expected = dict(asset_id=asset['id'], revision=asset['revision'], variant=name,
                    sha256=variant['file']['sha256'], canonical_sha256=asset['canonical']['sha256'],
                    reviewer='project_owner', scope='performance_use_only')
    if any(decision.get(k) != value for k, value in expected.items()) or not decision.get('statement'):
        raise ValueError('fake/incomplete owner approval or wrong scope/hash')
    ledger = decision['record']
    path = checked_file(root, ledger)
    if root is not None:
        stored = av.read(path)['decisions'][asset['id'] + ':' + name]
        if stored != {k:v for k,v in decision.items() if k != 'record'}:
            raise ValueError('decision differs from independent owner ledger')


def validate(library, plan, chars, root=None, gate='planning', folder=None):
    """Planning accepts missing planned PNGs; image readiness never does."""
    errors = []
    assets = library.get('assets', {})
    for actor,policy in library.get('anatomy_policies',{}).items():
        try:
            if policy['canonical']!=canonical_record(chars,actor):
                raise ValueError('anatomy policy changed canonical identity')
            if policy.get('proportion_reference'):
                checked_file(root,policy['proportion_reference'])
            elif policy.get('calibration_status')!='blocked_canonical_hash_reconciliation':
                raise ValueError('anatomy policy needs a proportion reference or explicit canonical blocker')
            if 'ratio_profile' in policy:
                try:from .character_proportions import validate_profile
                except ImportError:from character_proportions import validate_profile
                profile=policy['ratio_profile']
                if profile.get('actor')!=actor or profile.get('canonical')!=policy['canonical']:
                    raise ValueError('ratios belong to this character and exact canonical only')
                problems=validate_profile(profile)
                if problems:raise ValueError('; '.join(problems))
                if profile.get('observation_source'):
                    checked_file(root,profile['observation_source'])
                if profile.get('measurement_evidence'):
                    checked_file(root,profile['measurement_evidence'])
                for metric in profile['ratios'].values():
                    observation=metric.get('reference_measurement')
                    if observation and observation.get('source')!=profile.get('observation_source'):
                        raise ValueError('measured ratio must bind its actual observation bytes')
            if policy['staging_scale_policy']!='uniform_whole_actor_only':
                raise ValueError('head/body cannot be independently resized to repair anatomy')
        except (KeyError,ValueError,TypeError,OSError) as exc:
            errors.append(f'{actor}: {exc}')
    if library.get('schema') != SCHEMA or library.get('story') != plan['story']:
        errors.append('Wrong performance schema/story')
    expected_library = f"stories/{plan['story']}/{LIBRARY}"
    if plan.get('performance_library') != expected_library or chars.get('performance_library') != expected_library:
        errors.append('Plan and identity library must point to one performance authority')
    for actor in chars['characters']:
        if library.get('asset_roots',{}).get(actor)!=f"character/characters/{plan['story']}/{actor}":
            errors.append(f'{actor}: invalid version-local asset root')
    for cid,contract in plan.get('performance_staging_contracts',{}).items():
        try:
            if contract['measurement_status']=='pending_owner_anchor_measurement':
                if any(contract.get(k) is not None for k in ('approved_anchor','root_contact_pixels','anatomical_scale')):
                    raise ValueError('pending anchor cannot invent measurements/approval')
            elif contract['measurement_status']=='owner_reviewed_anchor':
                anchor=contract['approved_anchor']
                if not anchor or contract['root_contact_pixels'] is None or contract['anatomical_scale'] is None:
                    raise ValueError('reviewed anchor needs exact bytes and root/scale evidence')
                checked_file(root,anchor)
                decision=anchor['owner_decision']
                if decision.get('reviewer')!='project_owner' or decision.get('scope')!='shot_staging_anchor_only' or decision.get('image_sha256')!=anchor['sha256'] or not decision.get('statement'):
                    raise ValueError('staging anchor owner approval is missing/mis-scoped')
                path=checked_file(root,decision['record'])
                if root is not None and av.read(path)['staging_contracts'][cid]!={k:v for k,v in decision.items() if k!='record'}:
                    raise ValueError('staging anchor ledger differs')
            else:
                raise ValueError('unknown staging measurement status')
        except (KeyError,ValueError,TypeError,OSError) as exc:
            errors.append(f'{cid}: {exc}')
    files = set()
    for aid, asset in assets.items():
        try:
            actor = asset['actor']
            if actor not in chars['characters'] or asset['id'] != aid or not aid.startswith(actor.lower()+'.'):
                raise ValueError('unknown actor or unstable performance ID')
            if asset['canonical'] != canonical_record(chars, actor):
                raise ValueError('mis-bound canonical identity/hash')
            checked_file(None, asset['canonical'])
            if asset['asset_type'] not in KINDS or asset['reuse_status'] not in {'reusable','one_off','needs_view_variant'}:
                raise ValueError('unsupported performance/reuse type')
            if not re.fullmatch(r'r\d{3}',asset['revision']) or not asset['variants']:
                raise ValueError('revision and at least one variant required')
            if asset['view'] not in VIEWS or asset['head_view'] not in VIEWS or asset['body_facing'] not in FACINGS:
                raise ValueError('unknown view/facing/head orientation')
            if asset['head_orientation'] not in {'forward_right','up','left','right'}:
                raise ValueError('unknown head orientation')
            if asset['constraints'].get('mouth') != 'closed' or asset['constraints'].get('visible_teeth') is not False:
                raise ValueError('still mouth/teeth constraints violated')
            if any(k in asset for k in ('pixel_height','screen_scale','camera_distance_m')):
                raise ValueError('shot pixel scale must not live in a reusable performance')
            for parent in asset['parents']:
                other = assets[parent['id']]
                if parent['revision'] != other['revision'] or parent['authority'] not in AUTHORITIES:
                    raise ValueError('parent revision/reference authority invalid')
                pv = other['variants'][parent['variant']]
                expected_hash = pv['file']['sha256'] if pv.get('file') else None
                if parent.get('sha256') != expected_hash:
                    raise ValueError('parent hash does not identify current variant bytes')
                if other['actor'] != actor:
                    raise ValueError('parent belongs to different actor')
            if asset['asset_type'] == 'expression':
                base = assets[asset['portrait_base']['id']]
                if base['asset_type'] != 'portrait_base' or asset['portrait_base']['revision'] != base['revision']:
                    raise ValueError('expression portrait-base revision invalid')
                if (base['actor'],base['view'],base['head_view'],base['body_facing'],base['head_orientation']) != (actor,asset['view'],asset['head_view'],asset['body_facing'],asset['head_orientation']):
                    raise ValueError('expression incompatible with portrait geometry/angle')
                if not any(x['id']==base['id'] and x['authority']=='portrait_geometry_only' for x in asset['parents']):
                    raise ValueError('expression must bind exact portrait-base parent')
            if 'gait_order' in asset:
                order=asset['gait_order']
                if len(order)<3 or len(set(order))!=len(order) or any(v not in asset['variants'] for v in order):
                    raise ValueError('walk/action key order must name distinct registered states')
                generated=[asset['variants'][v]['file']['sha256'] for v in order if asset['variants'][v].get('file')]
                if len(generated)!=len(set(generated)):
                    raise ValueError('identical stamp is not a gait/action sequence')
            for name, variant in asset['variants'].items():
                component = variant.get('component_review')
                if component:
                    if component['image_sha256'] != (variant.get('file') or {}).get('sha256'):
                        raise ValueError('component review is bound to different image bytes')
                    if root is not None:
                        evidence = av.read(av.local(root, component['evidence']))
                        if not any(r['asset_id']==aid and r['variant']==name and
                                   r['image']['sha256']==component['image_sha256'] and
                                   r['body']==component['body'] and r['face']==component['face']
                                   for r in evidence['entries']):
                            raise ValueError('component review differs from owner feedback evidence')
                anatomy=variant.get('anatomy_review')
                if anatomy:
                    if anatomy.get('status') not in {'needs_matched_view_review','matched_reviewed_reference'}:
                        raise ValueError('unknown anatomy review status')
                    if anatomy.get('image_sha256')!=(variant.get('file') or {}).get('sha256'):
                        raise ValueError('anatomy review is bound to different image bytes')
                    policy=library.get('anatomy_policies',{}).get(actor,{})
                    if anatomy.get('reference_sha256')!=policy.get('proportion_reference',{}).get('sha256'):
                        raise ValueError('anatomy review uses a different proportion reference')
                    if anatomy['status']=='matched_reviewed_reference':
                        if not anatomy.get('comparison_method'):
                            raise ValueError('anatomy pass requires comparable-view method')
                        checked_file(root,anatomy.get('evidence') or {})
                        if policy.get('ratio_profile') and anatomy.get('profile_sha256')!=ratio_profile_digest(policy['ratio_profile']):
                            raise ValueError('anatomy review must identify current ratio-profile version')
                        horizontal=horizontal_review_blockers(library,actor,variant)
                        if horizontal:raise ValueError('; '.join(horizontal))
                        if policy.get('ratio_profile',{}).get('horizontal_review_policy',{}).get('required'):
                            checked_file(root,anatomy['horizontal_review']['evidence'])
                if variant['status'] not in STATUSES or variant['support'] not in SUPPORTS:
                    raise ValueError('unknown lifecycle or unsupported support/contact state')
                if variant['support']=='airborne' and variant['support_contacts']:
                    raise ValueError('airborne variant cannot plant support contacts')
                file = variant.get('file')
                if variant['status']=='planned':
                    if file or variant.get('owner_decision') or variant.get('creation'):
                        raise ValueError('planned variant cannot claim bytes/generation/approval')
                    continue
                if not file:
                    raise ValueError('candidate/approved variant missing file evidence')
                path = checked_file(root,file)
                asset_root = library['asset_roots'][actor]
                category = 'expressions' if asset['asset_type'] in {'expression','portrait_base'} else 'poses'
                if not str(Path(file['path'])).startswith(asset_root+'/'+category+'/') or path.name in files:
                    raise ValueError('performance candidate location/filename duplicated or out of actor scope')
                files.add(path.name)
                image_revision=file.get('image_revision',asset['revision'])
                if not re.fullmatch(r'r\d{3}',image_revision) or not re.fullmatch(actor.lower()+r'_[a-z0-9_]+_'+image_revision+r'_candidate\.png',path.name):
                    raise ValueError('semantic performance candidate filename invalid')
                side=file['sidecar']
                if Path(side['path']) != Path(file['path']).with_suffix('.json'):
                    raise ValueError('candidate sidecar must have same basename')
                checked_file(root,side)
                creation=variant['creation']
                if not creation.get('method') or not creation.get('prompt') or not isinstance(creation.get('settings'),dict) or not creation.get('inputs'):
                    raise ValueError('candidate needs exact creation method/inputs/prompt/settings')
                checked_file(root,creation['receipt'])
                roles=[]
                for ref in creation['inputs']:
                    checked_file(root,ref)
                    role_authority={'canonical_identity':'identity_anatomy_material_palette',
                                    'pose':'pose_only','expression':'expression_only',
                                    'portrait_base':'portrait_geometry_only',
                                    'existing_scene_pose_inspiration':'pose_only',
                                    'historical_inspiration':'historical_inspiration_only',
                                    'canonical_width_annotation':'visible_surface_measurements_only; no identity approval change',
                                    'canonical_measurement_annotation':'visible_surface_measurements_only; never render markings',
                                    'reviewed_walking_anatomy_reference':'pose-family anatomy balance and felt construction; not requested action or shot pixel size',
                                    'previous_pose_candidate':'acting_reference_only; no anatomy authority or approval transfer'}
                    if ref.get('role') not in role_authority or ref['authority']!=role_authority[ref['role']]:
                        raise ValueError('reference role contradicts its authority')
                    roles.append(ref['authority'])
                direct_identity=any(ref['path']==asset['canonical']['path'] and ref['sha256']==asset['canonical']['sha256'] and ref['authority']=='identity_anatomy_material_palette' for ref in creation['inputs'])
                if not direct_identity:
                    # Owner-requested isolation uses the scene itself as the only actual
                    # input. Verify canonical lineage without inventing an attachment.
                    if creation['method']!='built-in image_gen.imagegen scene_isolation':
                        raise ValueError('canonical identity reference missing from actual inputs')
                    lineage=creation['identity_lineage']
                    checked_file(root,lineage['scene_sidecar'])
                    if lineage['canonical']!=asset['canonical'] or len(creation['inputs'])!=1:
                        raise ValueError('scene isolation canonical lineage mismatch')
                    if root is not None:
                        original=av.read(av.local(root,lineage['scene_sidecar']['path']))
                        source=creation['inputs'][0]
                        if original['image']['path']!=source['path'] or original['image']['sha256']!=source['sha256'] or not any(ref['path']==asset['canonical']['path'] and ref['sha256']==asset['canonical']['sha256'] for ref in original['generation']['inputs']):
                            raise ValueError('scene isolation source does not descend from canonical')
                if variant['status'] in APPROVED:
                    _decision(root,asset,name,variant)
                    if root is not None:
                        checked_file(root,asset['canonical'])
                elif variant.get('owner_decision'):
                    raise ValueError('candidate cannot claim owner approval')
                if root is not None:
                    from PIL import Image
                    with Image.open(path) as image:
                        image.load()
                        if list(image.size)!=file['dimensions']:
                            raise ValueError('candidate dimensions differ')
                        alpha=image.getchannel('A').getextrema() if 'A' in image.getbands() else None
                        if file['alpha'] != {'has_alpha':alpha is not None,'extrema':list(alpha) if alpha else None}:
                            raise ValueError('candidate alpha evidence differs')
                    data=av.read(av.local(root,side['path']))
                    receipt=av.read(av.local(root,creation['receipt']['path']))
                    if any(receipt.get(k)!=creation[k] for k in ('method','prompt','settings','inputs')):
                        raise ValueError('creation facts differ from immutable receipt')
                    if data.get('asset_id')!=aid or data.get('revision')!=asset['revision'] or data.get('variant')!=name or data.get('image_sha256')!=file['sha256'] or data.get('canonical')!=asset['canonical'] or data.get('creation')!=creation or data.get('status')!=variant['status'] or data.get('owner_decision')!=variant.get('owner_decision'):
                        raise ValueError('candidate sidecar binding differs')
        except (ValueError,KeyError,TypeError,OSError) as exc:
            errors.append(f'{aid}: {exc}')
    # Parentage cycle check, without recursion into invalid unknown records.
    visited, active = set(), set()
    def visit(aid):
        if aid in active:
            errors.append(f'{aid}: variant parentage cycle'); return
        if aid in visited or aid not in assets:return
        active.add(aid)
        for parent in assets[aid].get('parents',[]):visit(parent.get('id'))
        active.remove(aid);visited.add(aid)
    for aid in assets:visit(aid)
    for line in plan['lines']:
        for beat in line['beats']:
            for image in beat['image_sequence']['images']:
                mapping=image.get('performance',{})
                if set(mapping)!=set(beat['cast']):errors.append(f"{image['id']}: performance must bind each visible actor exactly once")
                if not beat['cast'] and not image.get('performance_reason','').startswith('no_library_pose_needed:'):
                    errors.append(f"{image['id']}: environment-only image needs explicit reason")
    for line,beat,image,actor,binding in uses(plan):
        try:
            if actor not in chars['characters']:raise ValueError('unknown actor')
            if binding['binding_status'] not in {'planned','requires_view_variant','bound_reviewed_performance'}:
                raise ValueError('unknown binding status')
            if gate!='planning' and binding['required_for_image'] and binding['binding_status']!='bound_reviewed_performance':
                errors.append(f"{image['id']}/{actor}: planned binding is not pinned to reviewed performance bytes")
            state=plan['world_states'][image['state']]
            if binding['world_state_ref']!=image['state'] or binding['support']!=state['actors'][actor]['support']:
                raise ValueError('binding overrides world state/support')
            if binding['mouth']!='closed' or binding['visible_teeth'] is not False:
                raise ValueError('narrator/dialogue still mouths stay closed and toothless')
            if binding['render_method'] not in {'reference_guidance','deterministic_layers'}:
                raise ValueError('unknown realization strategy')
            acting = binding.get('acting')
            if acting:
                expression = assets[binding['expression_id']]
                if expression.get('acting_intent') != acting['intent']:
                    raise ValueError('expression does not match authored action intent')
                if acting['application_status'] != 'not_applied':
                    raise ValueError('face application needs a separate exact-hash scene review; no inferred integration')
                if gate != 'planning' and binding['required_for_image']:
                    errors.append(f"{image['id']}/{actor}: action expression not applied or reviewed at local head view/pitch/roll")
            for role,variant_key in [('pose','pose_variant'),('expression','expression_variant')]:
                aid=binding[role+'_id'];asset=assets[aid];variant=asset['variants'][binding[variant_key]]
                if variant.get('active_review_disposition') == 'superseded_by_turn_exit_reuse':
                    raise ValueError('superseded turn-entry body cannot be actively bound; reuse turn_exit')
                if binding[role+'_revision']!=asset['revision']:
                    raise ValueError('bound performance revision differs; explicit rebind required')
                expected_hash=variant['file']['sha256'] if variant.get('file') else None
                if binding.get(role+'_sha256') is not None and binding[role+'_sha256']!=expected_hash:
                    raise ValueError('bound performance hash differs')
                if asset['actor']!=actor or (role=='expression')!=(asset['asset_type']=='expression'):
                    raise ValueError('actor/pose/expression role mismatch')
                if (binding['view'],binding['head_view'],binding['body_facing'])!=(asset['view'],asset['head_view'],asset['body_facing']):
                    raise ValueError('incompatible view/facing/head orientation; author a view variant')
                if binding['head_orientation'] != variant['head_orientation']:
                    raise ValueError('incompatible head orientation; no angle-mismatched face overlay')
                if role=='pose' and variant['support']!=binding['support']:
                    raise ValueError('unsupported physical contact/support for pose')
                for key,allowed in asset['state_requirements'].items():
                    if av.field(state,key) not in allowed:raise ValueError('performance contradicts persistent state')
                if role == 'pose':
                    for key,allowed in variant['state_requirements'].items():
                        if av.field(state,key) not in allowed:
                            raise ValueError('performance contact/prop phase contradicts persistent state')
                if binding['binding_status']=='bound_reviewed_performance' and variant['status'] not in APPROVED:
                    raise ValueError('pending asset cannot be used as approved')
                if binding['binding_status']=='bound_reviewed_performance' and binding.get(role+'_sha256')!=expected_hash:
                    raise ValueError('reviewed binding must pin exact performance bytes')
                if gate!='planning' and binding['required_for_image']:
                    errors.extend(anatomy_blockers(library,actor,variant))
                    if variant['status'] not in APPROVED:
                        errors.append(f"{image['id']}/{actor}: {aid}:{binding[variant_key]} is {variant['status']}, performance use blocked")
                    elif role=='expression':
                        base=assets[asset['portrait_base']['id']]
                        if not any(v['status'] in APPROVED for v in base['variants'].values()):
                            errors.append(f"{aid}: portrait base not approved")
                    elif binding['render_method']=='deterministic_layers':
                        file=variant.get('file')
                        if not file or not file['alpha']['has_alpha'] or file['alpha']['extrema'][0]!=0 or variant['root_contact'] is None:
                            errors.append(f"{aid}: reviewed transparent pose and source root/contact required for layers")
            stage=binding['staging']
            if stage['camera_status'] not in {'camera_unknown','measured'}:raise ValueError('invalid camera status')
            if stage['camera_status']=='camera_unknown' and any(stage.get(k) is not None for k in ('camera_distance_m','lens_or_zoom','crop','depth','root_contact_pixels','screen_scale')):
                raise ValueError('unmeasured camera must not invent distance/scale')
            if gate!='planning' and stage['camera_status']=='camera_unknown':
                errors.append(f"{image['id']}/{actor}: shot staging camera/depth/contact still unreviewed")
            if beat['continuity_group']=='fork_decision':
                contract=plan['performance_staging_contracts']['fork_decision.Milo']
                if actor!='Milo' or stage['contract_id']!='fork_decision.Milo' or contract['actor']!=actor or contract['camera_policy']!='locked_camera_crop' or contract['standing_depth_policy']!='same_standing_depth' or contract['root_contract']!='one_shared_root_and_foot_contact' or contract['scale_contract']!='one_shared_anatomical_projection; gaze/pose_does_not_resize_head_or_body':
                    raise ValueError('locked camera/depth requires common root and anatomical scale contract')
                if any(stage.get(k) is not None for k in ('root_contact_pixels','screen_scale')):
                    raise ValueError('locked root/scale must be authored once in the common contract')
                if gate!='planning' and contract['measurement_status']!='owner_reviewed_anchor':
                    errors.append(f"{image['id']}: fixed-fork root/scale anchor still unmeasured")
            if line['line_id']=='S03-L004' and (binding.get('story_constraint')!='stationary_route_consideration; no_shortcut_commitment' or 'stationary' not in binding['pose_id'] or binding['travel_direction']!='stationary_or_action_local'):
                raise ValueError('route emphasis must not commit to shortcut before decision')
            if line['line_id']=='S05-L009' and actor=='Milo':
                phase=['rear_paw_support_lost','flank_tumble','flank_roll','nose_contact'][int(image['id'][-2:])-1]
                if binding.get('trajectory_phase')!=phase or binding['pose_variant']!=['support_lost','tumble','roll','nose_landing'][int(image['id'][-2:])-1]:
                    raise ValueError('rear paw -> flank -> face trajectory/contact keys collapsed')
        except (KeyError,ValueError,TypeError,IndexError) as exc:
            errors.append(f"{image['id']}/{actor}: {exc}")
    if root is not None:
        if folder is not None:errors.extend(immutable_errors(root,folder))
        if gate!='planning':
            for actor in chars['characters']:
                try:
                    if chars['characters'][actor]['canonical']['status']!='owner_approved':
                        raise ValueError('identity is not owner-approved')
                    checked_file(root,canonical_record(chars,actor))
                except (ValueError,OSError) as exc:errors.append(f'{actor}: canonical owner reconciliation required: {exc}')
    return errors


def usage_report(library,plan):
    impact=defaultdict(list);rows=[]
    for line,beat,image,actor,b in uses(plan):
        row={'line_id':line['line_id'],'audio_wav':line['audio']['wav'],'beat_id':beat['id'],'image_id':image['id'],'actor':actor,**copy.deepcopy(b)}
        rows.append(row)
        for role in ('pose','expression'):
            aid=b[role+'_id'];variant=b[role+'_variant'];impact[aid].append({'image_id':image['id'],'actor':actor,'variant':variant,'role':role})
    counts=Counter(v['status'] for a in library['assets'].values() for v in a['variants'].values())
    return {'schema':'feltwillow.performance-usage.v1','derived_from':['audio_visual_plan.json',LIBRARY],
            'counts':{'unique_pose_records':sum(a['asset_type']!='expression' for a in library['assets'].values()),
                      'expression_records':sum(a['asset_type']=='expression' for a in library['assets'].values()),
                      'asset_types':dict(Counter(a['asset_type'] for a in library['assets'].values())),
                      'planned_pose_variants':sum(v['status']=='planned' for a in library['assets'].values() if a['asset_type']!='expression' for v in a['variants'].values()),
                      'planned_expression_variants':sum(v['status']=='planned' for a in library['assets'].values() if a['asset_type']=='expression' for v in a['variants'].values()),
                      'variant_statuses':dict(counts),'actual_generated_performance_candidates':sum(n for s,n in counts.items() if s!='planned'),
                      'approved_performance_variants':sum(n for s,n in counts.items() if s in APPROVED),
                      'generated_variants_pending_anatomy_review':sum(bool(v.get('file')) and bool(anatomy_blockers(library,a['actor'],v)) for a in library['assets'].values() for v in a['variants'].values()),
                      'planned_actor_image_assignments':len(rows),'unique_scene_image_ids':len({r['image_id'] for r in rows}),
                      'actual_scene_images_approved_by_this_library':0},'uses':rows,'impact':dict(impact)}


def derive(folder,library,plan,chars):
    report=usage_report(library,plan)
    recorded=sum(l['audio']['status']=='available_in_r001' for l in plan['lines'])
    av.write(folder/'derived/performance_usage.json',report)
    out=['# Character performance requirements (derived)','',
         f'Authored registry: character_performance_library.json. Shot uses come only from audio_visual_plan.json. Lifecycle counts distinguish planned, generated candidates and reviewed assets; generation grants no approval. Current r001 audio: {recorded}/{len(plan["lines"])} lines recorded. Visual authoring and phrase alignment are separate.','',
         'Counts: `'+json.dumps(report['counts'])+'`.','',
         'Highest-impact assets are listed first; this is a requirements inventory, not an instruction to generate a catalogue. Unresolved view proposals need scoped staging review. Canonical identity follows the current exact-hash owner record; changed bytes require reconciliation.','',
         '| Actor / asset | Type / view / reuse | Variants / lifecycle | Exact image uses | Owner review |','|---|---|---|---|---|']
    for aid,a in sorted(library['assets'].items(),key=lambda kv:(-len(report['impact'].get(kv[0],[])),kv[0])):
        names=', '.join(f"{n} ({v['status']})" for n,v in a['variants'].items())
        image_uses=', '.join(f"{u['image_id']}:{u['variant']}" for u in report['impact'].get(aid,[])) or 'unassigned proposal / parent requirement'
        out.append(f"| {a['actor']} / `{aid}` — {a['label']} | {a['asset_type']} / {a['view']}, {a['body_facing']} / {a['reuse_status']} | {names} | {image_uses} | Confirm view, contacts and minimum required keys; no automatic approval |")
    out+=['','## Reuse and rollout','',
          'Walking family includes contact, passing/lift and opposite-contact keys; only assigned keys need later production. A still reference is not a walk cycle. Sleeping Leo establish/mane/eyes/rear-paw shots share one persistent pose, with separate framing. Multi-phase trip, scramble, trigger/net and run keys retain state/contact distinctions.','',
          'Portrait-base and expression requirements are angle-specific. Current S02-L003 is inspiration only, with tight ear clearance; existing scene PNGs and v6 atlases are not performance approval. No screen pixel height belongs in reusable pose anatomy.','',
          'Reuse existing exact scoped pose/expression decisions. Review only unresolved shot-specific contact, crop, projection and integration; do not ask again for accepted gait or portrait artwork. The full S03-L001–L008 fork setup stays stationary with one declared root/foot/scale anchor.','',
          'See character-performance-library.md in docs for validation, dry proposals and composition limitations.']
    (folder/'derived/PERFORMANCE_REQUIREMENTS.md').write_text('\n'.join(out)+'\n')
    index=['# Audio → image → performance (derived)','','Planned assignments do not retroactively change existing scene receipts or approvals.','','| Audio | Beat / image | Actor | Pose / key | Expression | View / staging | Lifecycle |','|---|---|---|---|---|---|---|']
    for row in report['uses']:
        a=library['assets'][row['pose_id']];v=a['variants'][row['pose_variant']]
        index.append(f"| {row['line_id']} | {row['beat_id']} / {row['image_id']} | {row['actor']} | {row['pose_id']}:{row['pose_variant']} | {row['expression_id']} | {row['view']} / {row['staging']['contract_id'] or 'camera_unknown'} | {v['status']} |")
    (folder/'derived/AUDIO_PERFORMANCE_INDEX.md').write_text('\n'.join(index)+'\n')
    return report


def proposal(root,folder,library,plan,chars,locs,image_id,reference_limit=8):
    if type(reference_limit) is not int or reference_limit < 1:
        raise ValueError('Reference limit must be a positive integer')
    matches=[(l,b,im) for l in plan['lines'] for b in l['beats'] for im in b['image_sequence']['images'] if im['id']==image_id]
    if len(matches)!=1:raise ValueError('Unknown or duplicate image ID')
    line,beat,image=matches[0]
    errors=validate(library,plan,chars,root,folder=folder)
    refs=[];required=[];blockers=list(errors)
    for actor,binding in image.get('performance',{}).items():
        canonical=canonical_record(chars,actor)
        try:checked_file(root,canonical)
        except (ValueError,OSError) as exc:blockers.append(str(exc))
        refs.append({'role':'canonical_identity','actor':actor,'authority':'identity_anatomy_material_palette',**canonical})
        for role in ('pose','expression'):
            aid=binding[role+'_id'];variant_name=binding[role+'_variant'];asset=library['assets'][aid];v=asset['variants'][variant_name]
            ref={'role':role,'actor':actor,'asset_id':aid,'revision':asset['revision'],'variant':variant_name,'authority':role+'_only','path':v['file']['path'] if v.get('file') else None,'sha256':v['file']['sha256'] if v.get('file') else None,'status':v['status']}
            required.append(ref)
            if v['status'] not in APPROVED:blockers.append(f'{aid}:{variant_name}: reviewed performance bytes missing')
            else:refs.append(ref)
        if binding['staging']['camera_status']=='camera_unknown':blockers.append(f'{actor}: shot camera/depth/contact measurements pending')
    view=locs['views'][image['location_view']]
    if beat['background_continuity']=='locked_background':
        if not view.get('source'):blockers.append('locked background view not owner-selected; master reference is not a selected scene plate')
        else:refs.append({'role':'locked_background','authority':'exact_background_camera',**view['source']})
    # Include prop authority requirements explicitly, never substitute an unapproved design.
    state=plan['world_states'][image['state']]
    for actor,binding in image.get('performance',{}).items():
        for role in ('pose','expression'):
            asset=library['assets'][binding[role+'_id']]
            blockers.extend(anatomy_blockers(library,actor,asset['variants'][binding[role+'_variant']]))
    if state['props']['acorn']['owner']=='Milo' and 'Milo' in image.get('performance',{}):
        required.append({'role':'prop_design','prop':'acorn','status':'approval_and_byte_binding_required'})
        blockers.append('single acorn prop design/contact requires approved shot-specific reference')
    required_count=len(refs)+sum(r.get('status') not in APPROVED for r in required)
    required_count+=int(beat['background_continuity']=='locked_background' and not view.get('source'))
    if required_count>reference_limit:
        blockers.append('reference limit exceeded; no critical reference may be silently dropped')
    ordered_roles={'canonical_identity':0,'pose':1,'expression':2,'locked_background':3,'prop_design':4,'edit_base':5}
    refs.sort(key=lambda r:ordered_roles[r['role']])
    profiles={actor:copy.deepcopy(library['anatomy_policies'][actor]['ratio_profile']) for actor in image.get('performance',{}) if 'ratio_profile' in library.get('anatomy_policies',{}).get(actor,{})}
    prompt=f"Compose {image_id}: {beat['action']} Phase: {image['phase_intent']}. Preserve canonical anatomy, felt identity and intrinsic palette. Use the named actor's own proportion profile only where its view/articulation comparability holds; null targets are uncalibrated. Never transfer mouse ratios to the lion or impose full-body head fraction on portraits/crouches. Performance controls pose/expression only; camera, depth, support, shadow, occlusion and props follow the separate shot staging. Keep still mouths closed and Milo toothless. Respect exact world state {image['state']}; no automatic continuity across cuts."
    return {'schema':'feltwillow.performance-shot-proposal.v1','dry_run':True,'submission_allowed':False,
            'endpoint':None,'request_count':1,'automatic_retries':0,'estimated_total_cost':None,'pricing':'unknown; endpoint/model/settings and current quote must be selected and owner-approved later',
            'story':plan['story'],'image_id':image_id,'audio':line['audio'],'beat_id':beat['id'],'world_state_ref':image['state'],
            'proportion_profiles':profiles,'proportion_profile_sha256':{actor:ratio_profile_digest(profile) for actor,profile in profiles.items()},
            'plan_sha256':av.digest(folder/'audio_visual_plan.json'),'performance_library_sha256':av.digest(folder/LIBRARY),
            'ordered_references':refs,'required_performance_and_prop_references':required,'reference_limit':reference_limit,
            'prompt':prompt,'settings':{'model':None,'seed':None,'output_size':None},'performance_bindings':image.get('performance',{}),
            'staging':{'location_view':image['location_view'],'background_continuity':beat['background_continuity'],'camera_intent':beat['camera_intent'],'world_state':state,'actor_staging':{a:b['staging'] for a,b in image.get('performance',{}).items()}},
            'composition_recipe':{'schema':'feltwillow.character-layer-recipe.v1','status':'proposal_only','background':view.get('source'),'actor_layers':[{ 'actor':a,'pose_id':b['pose_id'],'pose_variant':b['pose_variant'],'pose_revision':library['assets'][b['pose_id']]['revision'],'pose_sha256':None,'transform':{'uniform_scale':None,'translate_pixels':None},'source_root_pixels':None,'target_root_pixels':None,'occlusion_mask':None,'contact_shadow':None} for a,b in image.get('performance',{}).items()],
                                  'protected_background':'unchanged outside exact actor/contact/occlusion support mask','finishing':'separate narrowly scoped proposal; no repaint approval'},
            'sidecar_requirements':{'performance_assets':required,'ordered_reference_authorities':refs,'staging_record':'must include actual camera/contact/transform and masks independently','owner_scene_approval':None},
            'blockers':list(dict.fromkeys(blockers)),
            'limitations':['Reference guidance can redraw anatomy; visual comparison still required.','No production compositor run: approved alpha layers, perspective match, contact shadow and occlusion are missing.','Expression overlays require same registered head angle/base geometry; no arbitrary face replacement.']}


def compose_synthetic_pilot(background, actor, recipe):
    """Tiny CPU proof of layer placement/protected pixels; never writes production media.

    Only uniform positive scale + translation. No expression warp, relight, shadow
    synthesis, perspective projection or generator. Production CLI emits recipes only.
    """
    from PIL import Image
    if recipe.get('purpose')!='synthetic_contract_test':raise ValueError('Production composition remains proposal-only')
    if actor.mode!='RGBA' or actor.getchannel('A').getextrema()[0]!=0 or actor.getchannel('A').getextrema()[1]==0:raise ValueError('Reviewed transparent RGBA layer required')
    scale=recipe['uniform_scale'];translation=recipe['translate_pixels']
    if not isinstance(scale,(int,float)) or not math.isfinite(scale) or scale<=0:raise ValueError('positive uniform scale required')
    if len(translation)!=2 or any(type(x) is not int for x in translation):raise ValueError('integer translation required')
    root=recipe['source_root_pixels'];target=recipe['target_root_pixels']
    if any(abs(root[i]*scale+translation[i]-target[i])>1e-6 for i in (0,1)):
        raise ValueError('root/foot contact transform is inconsistent')
    layer=actor.resize((max(1,round(actor.width*scale)),max(1,round(actor.height*scale))),Image.Resampling.NEAREST)
    placed=Image.new('RGBA',background.size);placed.paste(layer,translation)
    mask=placed.getchannel('A')
    result=Image.alpha_composite(background.convert('RGBA'),placed)
    return result,mask


def pilot_proposal(folder, library, chars):
    """Bounded review draft. Unknown dependent hashes prevent submission."""
    canonical=canonical_record(chars,'Milo')
    specification=[
        ('milo.walk.screen_right.lightstep.3q','contact',None),
        ('milo.walk.screen_right.lightstep.3q','passing_step','P01'),
        ('milo.portrait.base.3q','default',None),
        ('milo.expression.startled_realization.3q','default','P03'),
        ('milo.expression.determined.3q','default','P03'),
        ('milo.decision.stationary.3q','sky',None),
        ('milo.decision.stationary.3q','long_path','P06'),
        ('milo.decision.stationary.3q','shortcut','P06')]
    requests=[]
    for n,(aid,name,parent) in enumerate(specification,1):
        asset=library['assets'][aid]
        category='expressions' if asset['asset_type'] in {'expression','portrait_base'} else 'poses'
        slug=aid.replace('.','_')+'_'+name
        prompt=(f"Create one transparent Milo performance layer: {asset['label']}; variant {name}. "
                "Use the exact approved Milo identity for compact head/body/limb/ear/tail design and felt palette. "
                "No visible teeth; mouth closed. No environment, story props or camera-specific pixel-height target. "
                "Full body and tail for poses, full ears and upper chest for portrait/expression. "
                "Preserve the registered three-quarter body view; "
                f"head orientation {asset['variants'][name]['head_orientation']}. "
                + ("Preserve the owner-reviewed parent body's dimensions/geometry; change only the declared gait or head/gaze/expression within compatible projection." if parent else "Establish a reviewable silhouette and support/root landmarks; this result needs owner review before dependent variants."))
        requests.append({'id':f'P{n:02d}','asset_id':aid,'variant':name,'revision':asset['revision'],
                         'endpoint':'built-in image_gen.imagegen (proposed, not called)',
                         'known_ordered_inputs':[{'role':'canonical_identity','authority':'identity_anatomy_material_palette',**canonical}],
                         'conditional_parent':{'request_id':parent,'path':None,'sha256':None,'approval_required_before_use':True} if parent else None,
                         'prompt':prompt,'settings':{'transparent_background':True,'model':None,'seed':None},
                         'proposed_output':f"{library['asset_roots']['Milo']}/{category}/{slug}_r001_candidate.png",
                         'status':'draft_not_authorization_ready','estimated_cost':None})
    result={'schema':'feltwillow.performance-pilot-proposal.v1','dry_run':True,'submission_allowed':False,
            'potential_request_count':8,'scene_image_requests':0,'automatic_retries':0,'estimated_total_cost':None,
            'pricing':'unknown; obtain endpoint/settings/price or disclose unknown before a later concrete approval request',
            'source_library_sha256':av.digest(folder/LIBRARY),'requests':requests,
            'deferred':['opposite-contact walking key until a chosen scene endpoint needs it','all Leo generation until canonical-byte reconciliation','scene composition and any finishing pass'],
            'owner_review_first':['confirm contact/passing silhouette and head/body design','choose full-ear portrait base and compatible expression geometry','confirm fixed-fork root/depth/head angles against one selected background'],
            'blockers':['dependent source PNG paths/hashes do not exist','first-stage candidates must be individually reviewed before later references','scene camera/root/scale measurements still pending','no generation authorization requested or inferred']}
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--story',required=True)
    sub=parser.add_subparsers(dest='command',required=True)
    val=sub.add_parser('validate');val.add_argument('--gate',choices=['planning','image'],default='planning')
    sub.add_parser('derive')
    sub.add_parser('pilot')
    audit=sub.add_parser('audit');audit.add_argument('--review',default='s01_s03_r001')
    prop=sub.add_parser('proposal');prop.add_argument('--image-id',required=True);prop.add_argument('--reference-limit',type=int,default=8)
    args=parser.parse_args()
    try:
        folder,plan,chars,locs,library=load(ROOT,args.story)
        errors=validate(library,plan,chars,ROOT,gate=getattr(args,'gate','planning'),folder=folder)
        if errors:raise ValueError('\n'.join(errors))
        if args.command=='derive':result=derive(folder,library,plan,chars)['counts']
        elif args.command=='proposal':result=proposal(ROOT,folder,library,plan,chars,locs,args.image_id,args.reference_limit)
        elif args.command=='pilot':result=pilot_proposal(folder,library,chars)
        elif args.command=='audit':
            if args.review!='s01_s03_r001':raise ValueError('Only existing s01_s03_r001 review is supported')
            try:from . import character_performance_audit as audit_tools
            except ImportError:import character_performance_audit as audit_tools
            result=audit_tools.build(ROOT,folder,plan,library)
        else:result={'planning':'PASS','scope':'performance planning; no generation or scene approval'}
        print(json.dumps(result,indent=2,ensure_ascii=False));return 0
    except (ValueError,KeyError,TypeError,OSError) as exc:
        print('PERFORMANCE_BLOCKED:',exc,file=sys.stderr);return 1


if __name__=='__main__':raise SystemExit(main())
