#!/usr/bin/env python3
"""CPU-only audio-line visual planning. Never generates media or submits work.

One authored plan; WAV/JSON recordings own audio facts. Image/video readiness
are separate from planning validity. Legacy paired plans are not consumed.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import wave

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
SCHEMA = 'feltwillow.audio-line-visual.v1'
TRANSITIONS = {'cut','same_location_cut','same_state_camera_cut','continuous_motion',
               'shared_boundary','time_change','location_change','portrait_cut','detail_cut'}
MODES = {'single','pair','multi_key','cut_sequence'}


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def image_filename(beat_id, subject, revision=1, *, image_id=None, role='location'):
    """Audio-linked names for new assets; canonical/master names stay unchanged."""
    if not re.fullmatch(r'S\d{2}-L\d{3}-B\d{2}', beat_id):
        raise ValueError('filename needs an audio-line beat ID')
    if not re.fullmatch(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)*', subject):
        raise ValueError('subject must be a lowercase underscore slug')
    if type(revision) is not int or not 1 <= revision <= 999:
        raise ValueError('image revision must be 1..999')
    if image_id is None:
        if role != 'location':
            raise ValueError('key images require their explicit image ID')
        prefix = beat_id
    else:
        if not re.fullmatch(re.escape(beat_id) + r'-I\d{2}', image_id) or role not in {'single','start','key','end'}:
            raise ValueError('key image ID/role does not match its beat')
        prefix = image_id
    return f'{prefix}_{role}_{subject}_r{revision:03d}_candidate.png'


def candidate_errors(plan, locations, root=None):
    """Verify candidate naming and exact audio links without granting approval."""
    lines = {line['line_id']: line for line in plan['lines']}
    beats = {b['id']: b for line in plan['lines'] for b in line['beats']}
    errors, paths = [], set()
    for vid, view in locations['views'].items():
        for candidate in view.get('candidates', []):
            try:
                bid = candidate['primary_beat_id']
                if bid not in beats or bid not in view['used_by_beats']:
                    raise ValueError('candidate primary beat is not a use of this view')
                expected = image_filename(bid, candidate['subject'], candidate['image_revision'])
                if Path(candidate['path']).name != expected or candidate['path'] in paths:
                    raise ValueError('candidate filename/uniqueness violates audio-linked naming')
                paths.add(candidate['path'])
                approval = candidate.get('owner_approval')
                if candidate['status'] == 'owner_approved':
                    if not approval or approval.get('image_sha256') != candidate['sha256'] or approval.get('reviewer') != 'project_owner':
                        raise ValueError('owner approval is missing or bound to different bytes')
                    if view['status'] != 'owner_approved_view' or view.get('source') != {'path':candidate['path'],'sha256':candidate['sha256']} or view.get('approval') != approval:
                        raise ValueError('approved candidate differs from selected view')
                    if root is not None:
                        decision = read(local(root,approval['record']))['views'][vid]
                        if decision['path'] != candidate['path'] or decision['sha256'] != candidate['sha256'] or decision['owner_statement'] != approval['statement'] or decision['reviewer'] != 'project_owner' or decision['scope'] != 'location_view_only':
                            raise ValueError('approval ledger does not authorize these view bytes')
                elif candidate['status'] != 'candidate_pending_owner_review' or approval:
                    raise ValueError('candidate record cannot invent owner approval')
                if candidate['sidecar']['path'] != str(Path(candidate['path']).with_suffix('.json')):
                    raise ValueError('sidecar must have the image basename')
                links = []
                for lid in dict.fromkeys(b[:8] for b in view['used_by_beats']):
                    audio = lines[lid]['audio']
                    links.append({'line_id':lid, 'audio_revision':plan['audio_revision'],
                        **{k:audio[k] for k in ['wav','metadata','sha256','metadata_sha256']}})
                if candidate['audio_links'] != links:
                    raise ValueError('candidate audio associations are stale or incomplete')
                if root is not None:
                    image = local(root,candidate['path'])
                    sidecar = local(root,candidate['sidecar']['path'])
                    if not image.is_file() or digest(image) != candidate['sha256']:
                        raise ValueError('candidate image bytes missing/changed')
                    if not sidecar.is_file() or digest(sidecar) != candidate['sidecar']['sha256']:
                        raise ValueError('candidate sidecar missing/changed')
                    data = read(sidecar)
                    if data['audio_links'] != links or data['primary_beat_id'] != bid or data['image']['path'] != candidate['path'] or data['image']['sha256'] != candidate['sha256']:
                        raise ValueError('sidecar disagrees with candidate/audio bindings')
                    if data.get('owner_approval') != approval or data.get('status') != candidate['status']:
                        raise ValueError('sidecar approval/status differs from selected candidate')
            except (KeyError,ValueError,TypeError,OSError) as exc:
                errors.append(f'{vid}: {exc}')
    return errors


def local(root, path):
    root = Path(root).resolve()
    if not isinstance(path, str) or Path(path).is_absolute() or '..' in Path(path).parts:
        raise ValueError(f'unsafe repository path: {path!r}')
    target = (root / path).resolve()
    if not target.is_relative_to(root):
        raise ValueError('path escapes repository')
    return target


def source_file(root, path):
    """Resolve read-only provenance relocated by an owner-authorized cleanup.

    Keep ``local`` unchanged for writes and active asset paths. Archived source
    lookup is explicit, repository-contained and bound to the original hash.
    """
    target = local(root, path)
    if target.is_file():
        return target
    archive = 'stories/lion_and_mouse_v7/history/retained_sources'
    index = local(root, archive + '/INDEX.json')
    if not index.is_file():
        return target
    record = read(index).get('files', {}).get(path)
    if record is None:
        return target
    archived = record['archived_path']
    if not isinstance(archived, str) or not archived.startswith(archive + '/files/'):
        raise ValueError('retained source escapes its archive')
    source = local(root, archived)
    if not source.is_file() or digest(source) != record['sha256']:
        raise ValueError(f'archived source missing or changed: {path}')
    return source


def wav_facts(path):
    with wave.open(str(path), 'rb') as audio:
        if audio.getnframes() <= 0:
            raise ValueError('empty WAV')
        return {'duration_seconds': audio.getnframes() / audio.getframerate(),
                'sample_rate_hz': audio.getframerate(), 'channels': audio.getnchannels(),
                'sample_width_bits': audio.getsampwidth() * 8,
                'sample_count': audio.getnframes(), 'sha256': digest(path)}


def inventory_audio(root, audio_root, expected_ids):
    """Read actual bytes; never infer current availability from tracked history."""
    root = Path(root).resolve()
    directory = local(root, audio_root)
    line_dir = directory / 'lines'
    wavs = {p.stem: p for p in line_dir.glob('*.wav')}
    metas = {p.stem: p for p in line_dir.glob('*.json')}
    errors, available = [], {}
    for unknown in sorted((wavs.keys() | metas.keys()) - set(expected_ids)):
        errors.append(f'unknown r001 line asset: {unknown}')
    for lid in sorted(wavs.keys() | metas.keys()):
        if lid not in expected_ids:
            continue
        if lid not in wavs or lid not in metas:
            errors.append(f'{lid}: incomplete WAV/JSON pair')
            continue
        try:
            meta = read(metas[lid])
            facts = wav_facts(wavs[lid])
            if meta['id'] != lid:
                raise ValueError('metadata ID differs from filename')
            if meta['sha256'] != facts['sha256']:
                raise ValueError('metadata WAV hash differs from actual bytes')
            if abs(float(meta['seconds']) - facts['duration_seconds']) > .02:
                raise ValueError('metadata duration differs from actual WAV')
            if facts['channels'] != 1 or facts['sample_width_bits'] != 16:
                raise ValueError('expected recorded PCM16 mono')
            if not meta.get('text') or not meta.get('speaker'):
                raise ValueError('metadata text/speaker missing')
            available[lid] = {'status': 'available_in_r001', 'revision': 'r001',
                'wav': str(wavs[lid].relative_to(root)),
                'metadata': str(metas[lid].relative_to(root)),
                'metadata_sha256': digest(metas[lid]), **facts,
                'metadata_recorded_duration_seconds': meta['seconds'],
                'voice_id': meta.get('voice'), 'provider': meta.get('model'),
                'metadata_text': meta['text'], 'metadata_speaker': meta['speaker'],
                'metadata_style': meta.get('style', '')}
        except (ValueError, KeyError, OSError, wave.Error, EOFError) as exc:
            errors.append(f'{lid}: {exc}')
    return available, errors


def field(state, path):
    value = state
    for key in path.split('.'):
        value = value[key]
    return value


def apply_event(state, event, rules):
    """Replay the declared delta; unaffected/offscreen state stays exact."""
    result = copy.deepcopy(state)
    for condition in event.get('preconditions', []):
        if field(result, condition['path']) != condition['value']:
            raise ValueError(f"event prerequisite: {condition['path']}")
    seen = set()
    for change in event['changes']:
        path = change['path']
        if path in seen:
            raise ValueError('event changes one property twice')
        seen.add(path)
        if field(result, path) != change['before']:
            raise ValueError(f'event stale before-state: {path}')
        rule = next((r for r in rules if r['path'] == path), None)
        if rule:
            transition = next((t for t in rule['transitions'] if
                t['before'] == change['before'] and t['after'] == change['after'] and t['event'] == event['kind']), None)
            if transition is None:
                raise ValueError(f'illegal causal transition: {path}')
            for requirement in transition.get('requires', []):
                if field(result, requirement['path']) != requirement['value']:
                    raise ValueError(f"causal prerequisite: {requirement['path']}")
        target = result
        keys = path.split('.')
        for key in keys[:-1]:
            target = target[key]
        if keys[-1] not in target:
            raise ValueError(f'unknown persistent property: {path}')
        target[keys[-1]] = change['after']
    return result


def shot_continuity_errors(plan, root=None):
    """Protect explicitly connected staging without inventing measured anchors."""
    errors = []
    images = {im['id']: im for line in plan['lines'] for beat in line['beats'] for im in beat['image_sequence']['images']}
    contracts = plan.get('shot_continuity_contracts', {})
    for name, contract in contracts.items():
        try:
            ref = contract['reference']
            if name == 'fork_stationary' and not all(contract.get(k) is True for k in ('lock_background','lock_root','lock_anatomical_scale')):
                raise ValueError('stationary fork must preserve background, root and scale')
            if name == 'acorn_background' and contract.get('lock_background') is not True:
                raise ValueError('connected placement must preserve background')
            if not re.fullmatch(r'[0-9a-f]{64}', ref['sha256']):
                raise ValueError('reference needs exact hash')
            if root is not None and digest(source_file(root, ref['path'])) != ref['sha256']:
                raise ValueError('reference bytes changed')
            for iid in contract['image_ids']:
                im = images[iid]
                if im.get('shot_continuity_contract') != name:
                    raise ValueError('image lost shared shot contract')
                if contract.get('lock_root'):
                    binding = im['performance'][contract['actor']]
                    if binding['travel_direction'] != 'stationary_or_action_local' or binding['staging']['contract_id'] != 'fork_decision.Milo':
                        raise ValueError('stationary group moved root or lost shared scale')
            if name == 'decision_portrait_body' and not all(contract.get(k) is True for k in ('lock_upper_body_geometry','lock_visible_body_extent','lock_crop')):
                raise ValueError('connected portraits must preserve body geometry and crop')
        except (KeyError, TypeError, ValueError, OSError) as exc:
            errors.append(f'{name}: {exc}')
    for iid, im in images.items():
        name = im.get('shot_continuity_contract')
        if name and (name not in contracts or iid not in contracts[name]['image_ids']):
            errors.append(f'{iid}: unknown/unregistered shot contract')
    whole = plan.get('prop_visual_contracts', {}).get('story_acorn_whole_before_eating')
    if whole:
        try:
            if not whole['no_visible_character_teeth']:
                raise ValueError('pre-eating still must preserve the no-teeth rule')
            for iid in whole['image_ids']:
                im = images[iid]
                if plan['world_states'][im['state']]['props']['acorn']['condition'] != 'whole':
                    raise ValueError('pre-eating image must show a whole acorn')
                if whole['next_event'] in im['events_before']:
                    raise ValueError('taste event cannot precede the pre-eating still')
        except (KeyError, ValueError, TypeError) as exc:
            errors.append(f'story_acorn_whole_before_eating: {exc}')
    acorn = plan.get('prop_visual_contracts', {}).get('story_acorn_tasted')
    if acorn:
        try:
            ref = acorn['size_reference']
            if root is not None and digest(source_file(root, ref['path'])) != ref['sha256']:
                raise ValueError('acorn size-reference bytes changed')
            if acorn['condition_state'] != 'tasted' or not acorn['no_visible_character_teeth']:
                raise ValueError('tasted acorn must not expose character teeth')
            for iid in acorn['image_ids']:
                if plan['world_states'][images[iid]['state']]['props']['acorn']['condition'] != 'tasted':
                    raise ValueError('eaten appearance precedes the taste event')
            group = plan['continuity_groups']['acorn_placement']
            if group.get('motion_policy') != 'continuous_no_cut':
                raise ValueError('acorn placement must remain continuous')
            beats = {b['id']: b for line in plan['lines'] for b in line['beats']}
            a, b = (beats[bid] for bid in group['beat_ids'])
            if a['transition_out'] != 'shared_boundary' or b['transition_in'] != 'shared_boundary' or b['image_sequence']['images'][0].get('reuse_of') != a['image_sequence']['images'][-1]['id']:
                raise ValueError('standing-to-crouch boundary lost its shared frame')
        except (KeyError, ValueError, TypeError, OSError) as exc:
            errors.append(f'story_acorn_tasted: {exc}')
    return errors


def validate(plan, characters, locations, root=None):
    from production.sequence_plan import validate_sequences
    errors = validate_sequences(plan)
    if plan.get('schema') != SCHEMA:
        return ['unsupported audio-line visual schema']
    if plan.get('audio_revision') != 'r001':
        errors.append('active audio revision must be explicit r001')
    errors.extend(candidate_errors(plan, locations, root))
    errors.extend(shot_continuity_errors(plan, root))
    lines = plan.get('lines', [])
    ids = [line['line_id'] for line in lines]
    expected = plan['script_line_order']
    if ids != expected or len(ids) != len(set(ids)):
        errors.append('line inventory/order differs from script; duplicate, unknown or omitted line')
    if plan['audio_scene_order'] != [s['id'] for s in plan['audio_scenes']]:
        errors.append('audio scene order differs from scene records')
    for scene in plan['audio_scenes']:
        if scene['line_ids'] != [l['line_id'] for l in lines if l['audio_scene'] == scene['id']]:
            errors.append(f"{scene['id']}: line-to-audio-scene mapping differs")
    for vid, view in locations['views'].items():
        if view.get('id') != vid or view.get('family_id') not in locations['families']:
            errors.append(f'{vid}: invalid location view/family identity')
        if view.get('status') == 'planned':
            if view.get('source') or view.get('generation_provenance') or view.get('owner_approval') or view.get('approval'):
                errors.append(f'{vid}: planned view cannot claim generated or approved bytes')
            for ref in view.get('reference_masters', []):
                if ref not in locations['views'] or locations['views'][ref]['status'] != 'existing_owner_approved_master':
                    errors.append(f'{vid}: unknown/unapproved reference master')
    cast = set(characters['characters'])
    states = plan['world_states']
    current = plan['initial_world_state']
    previous = None
    seen_images, seen_beats, used_events = {}, [], set()
    groups = {key: [] for key in plan['continuity_groups']}
    available_ids = []
    for line in lines:
        lid = line['line_id']
        try:
            if not re.fullmatch(r'S\d{2}-L\d{3}', lid) or line['audio_scene'] != lid[:3]:
                raise ValueError('invalid line/audio-scene ID')
            if line['speaker'] not in {'NARRATOR'} | {c['voice_speaker'] for c in characters['characters'].values()}:
                raise ValueError('unknown recorded speaker')
            audio = line['audio']
            available = audio['status'] == 'available_in_r001'
            if available:
                available_ids.append(lid)
                if not math.isfinite(audio['duration_seconds']) or audio['duration_seconds'] <= 0 or not audio['sha256'] or not audio['metadata_sha256']:
                    raise ValueError('available audio lacks actual duration/hash provenance')
                if not line['beats']:
                    if line['planning_status'] != 'pending_visual_authoring':
                        raise ValueError('available line has no visual beats or explicit authoring backlog')
                    if line['coverage']['target_duration_seconds'] != audio['duration_seconds']:
                        raise ValueError('recorded backlog must bind actual WAV duration')
                    if line['coverage']['phrase_timing_status'] != 'pending_alignment':
                        raise ValueError('recorded backlog cannot claim aligned visual timing')
                    continue
            else:
                if audio['status'] != 'not_available_in_r001':
                    raise ValueError('unknown audio availability')
                if any(audio.get(k) is not None for k in ['duration_seconds','sha256','wav','metadata','metadata_sha256']):
                    raise ValueError('pending audio masquerades as timed/available')
                if line['planning_status'] != 'pending_audio_visual_authoring' or line['beats']:
                    raise ValueError('pending audio cannot be ready or carry timed beats')
                continue
            if line['coverage']['target_duration_seconds'] != audio['duration_seconds']:
                raise ValueError('coverage uses historical rather than current WAV duration')
            if line['coverage']['scope'] != 'complete_line_wav':
                raise ValueError('line must promise complete WAV coverage')
            reviewed_windows = []
            for index, beat in enumerate(line['beats'], 1):
                bid = f'{lid}-B{index:02d}'
                if beat['id'] != bid:
                    raise ValueError('beat IDs/order must follow their audio line')
                seen_beats.append(bid)
                if beat['semantic_span'] not in line['text']:
                    raise ValueError('semantic span is not an exact clause of the spoken line')
                view = locations['views'][beat['location_view']]
                if beat['location_family'] not in locations['families'] or view['family_id'] != beat['location_family']:
                    raise ValueError('unknown/mismatched location family/view')
                if set(beat['cast']) - cast or len(set(beat['cast'])) != len(beat['cast']):
                    raise ValueError('unknown/duplicate visible cast')
                if set(beat['offscreen_cast']) != cast - set(beat['cast']):
                    raise ValueError('offscreen cast omitted from persistent world')
                if beat['transition_in'] not in TRANSITIONS or beat['transition_out'] not in TRANSITIONS:
                    raise ValueError('vague or unsupported transition')
                group = beat['continuity_group']
                if group is not None:
                    groups[group].append(bid)
                background = beat.get('background_continuity')
                if background not in {'independent_scene','same_place_new_view','locked_background'}:
                    raise ValueError('background continuity must be explicitly classified')
                if background == 'independent_scene' and beat['transition_in'] == 'shared_boundary':
                    raise ValueError('independent scene cannot inherit a shared image boundary')
                if background == 'locked_background':
                    contract = plan['continuity_groups'].get(group, {})
                    if contract.get('background_policy') != 'exact_same_background' or contract.get('locked_location_view') != beat['location_view'] or contract.get('camera_policy') != 'locked_camera_crop':
                        raise ValueError('locked background needs one explicit fixed-view/camera contract')
                    if any(im['location_view'] != beat['location_view'] for im in beat['image_sequence']['images']):
                        raise ValueError('locked background changes within its image sequence')
                if beat['state_in'] != current:
                    raise ValueError('cut reset the persistent world state')
                state = copy.deepcopy(states[current])
                def replay(event_id):
                    nonlocal state, current
                    if event_id in used_events:
                        raise ValueError('world event replayed twice')
                    event = plan['world_events'][event_id]
                    if event['source_line'] != lid or event['before_state'] != current:
                        raise ValueError('event source/order mismatch')
                    state = apply_event(state, event, plan['state_rules'])
                    current = event['after_state']
                    if state != states[current]:
                        raise ValueError('state changed outside declared events')
                    used_events.add(event_id)
                for event_id in beat['entry_events']:
                    replay(event_id)
                if current != beat['state_start']:
                    raise ValueError('shot start state differs from entry events')
                mode = beat['image_sequence']['mode']
                images = beat['image_sequence']['images']
                minimum = beat['image_sequence'].get('minimum_images', 1)
                if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 1 or len(images) < minimum:
                    raise ValueError('sequence below authored minimum image count')
                roles = [im['role'] for im in images]
                if mode not in MODES:
                    raise ValueError('unknown image sequence mode')
                if mode == 'single' and roles != ['single']:
                    raise ValueError('single requires exactly one single image')
                if mode == 'pair' and roles != ['start','end']:
                    raise ValueError('pair requires exactly start/end')
                if mode == 'multi_key' and (len(roles) < 3 or roles != ['start'] + ['key']*(len(roles)-2) + ['end']):
                    raise ValueError('multi_key requires start, intermediate key(s), end')
                if mode == 'cut_sequence' and (len(roles) < 2 or any(r != 'single' for r in roles)):
                    raise ValueError('cut_sequence requires multiple independent single shots')
                for n, image in enumerate(images, 1):
                    if image['id'] != f'{bid}-I{n:02d}' or image['id'] in seen_images:
                        raise ValueError('image IDs/order invalid')
                    image_view = locations['views'][image['location_view']]
                    if image_view['family_id'] != beat['location_family']:
                        raise ValueError('image view changes physical family inside one beat')
                    for event_id in image['events_before']:
                        replay(event_id)
                    if image['state'] != current:
                        raise ValueError('image state is not the event-derived state')
                    reused = image.get('reuse_of')
                    if reused:
                        prior = seen_images.get(reused)
                        if not prior or prior['state'] != image['state'] or prior['location_view'] != image['location_view']:
                            raise ValueError('shared image reuse has incompatible state/view')
                    if mode in {'pair','multi_key'} and image['location_view'] != beat['location_view']:
                        raise ValueError('connected image sequence changes camera view; use separate beats/cuts')
                    if any(state['actors'][actor]['location_family'] != beat['location_family'] for actor in beat['cast']):
                        raise ValueError('visible actor is in a different physical family')
                    if state['props']['net']['phase'] in {'falling','settled'} and state['actors']['Leo']['support'] != 'ground':
                        raise ValueError('falling/settled net must keep Leo grounded')
                    if image.get('path') or image.get('sha256') or image.get('generation_provenance') or image.get('owner_approval'):
                        raise ValueError('planned placeholder cannot claim generated or approved bytes')
                    if image['status'] != 'planned':
                        raise ValueError('this planning revision cannot invent image selection/approval')
                    seen_images[image['id']] = image
                if current != beat['state_out']:
                    raise ValueError('beat end state differs from final image')
                if previous:
                    if previous['transition_out'] != beat['transition_in']:
                        raise ValueError('incoming/outgoing transition disagreement')
                    if beat['transition_in'] in {'shared_boundary','continuous_motion'}:
                        if group is None or group != previous['continuity_group']:
                            raise ValueError('motion continuity needs an explicit common group')
                        before = previous['image_sequence']['images'][-1]
                        after = images[0]
                        if before['location_view'] != after['location_view'] or before['state'] != after['state'] or previous['cast'] != beat['cast']:
                            raise ValueError('continuous/shared input geometry/state/cast differs')
                        if beat['entry_events']:
                            raise ValueError('continuous transition cannot hide a story event')
                        if beat['transition_in'] == 'shared_boundary' and after.get('reuse_of') != before['id']:
                            raise ValueError('shared boundary must explicitly reuse the previous image')
                    elif any(im.get('reuse_of') for im in images):
                        raise ValueError('image reuse requires an explicit shared boundary')
                dialogue = beat['dialogue']
                speaker_actor = next((c for c in cast if characters['characters'][c]['voice_speaker'] == line['speaker']), None)
                if line['speaker'] == 'NARRATOR':
                    if dialogue['mode'] != 'narrator_voiceover' or dialogue['mouth_driver'] is not None:
                        raise ValueError('narration must never drive character mouths')
                elif dialogue['mode'] != 'character_dialogue' or dialogue['speaker_character'] != speaker_actor or dialogue['mouth_driver'] != 'future_reviewed_dialogue_pipeline':
                    raise ValueError('character speech needs explicit later dialogue handling')
                if dialogue['boundary_mouth'] != 'closed':
                    raise ValueError('still boundaries must not invent baked speech mouths')
                timing = beat['timing']
                if timing['status'] == 'pending_alignment':
                    if timing['start_seconds'] is not None or timing['end_seconds'] is not None:
                        raise ValueError('pending phrase timing contains invented windows')
                elif timing['status'] == 'whole_line' and len(line['beats']) == 1:
                    if timing['start_seconds'] != 0 or timing['end_seconds'] != audio['duration_seconds']:
                        raise ValueError('whole-line duration mismatch')
                elif timing['status'] == 'reviewed_alignment':
                    if not timing.get('evidence') or not (0 <= timing['start_seconds'] < timing['end_seconds'] <= audio['duration_seconds']):
                        raise ValueError('phrase timing lacks valid alignment evidence')
                    reviewed_windows.append((timing['start_seconds'], timing['end_seconds']))
                else:
                    raise ValueError('unsupported timing authority')
                previous = beat
            if reviewed_windows:
                if len(reviewed_windows) != len(line['beats']):
                    raise ValueError('line has partial reviewed coverage')
                cursor = 0
                for a, b in reviewed_windows:
                    if abs(a-cursor) > 1e-6:
                        raise ValueError('aligned phrase coverage has a gap/overlap')
                    cursor = b
                if abs(cursor-audio['duration_seconds']) > 1e-6:
                    raise ValueError('aligned beats do not cover complete line WAV')
        except (ValueError, KeyError, TypeError, IndexError) as exc:
            errors.append(f'{lid}: {exc}')
    for gid, members in groups.items():
        if members != plan['continuity_groups'][gid]['beat_ids'] or not members:
            errors.append(f'{gid}: group membership/order differs')
    locked = [(line['line_id'], b) for line in lines for b in line['beats'] if b.get('background_continuity') == 'locked_background']
    policy = plan.get('location_continuity_policy', {})
    if policy.get('first_exact_background_line') and (not locked or locked[0][0] != policy['first_exact_background_line'] or locked[0][1]['continuity_group'] != policy['first_exact_background_group']):
        errors.append('first exact-background sequence differs from owner direction')
    if set(plan['world_events']) != used_events:
        errors.append('orphaned or unvalidated world events')
    if root is not None:
        actual, problems = inventory_audio(root, plan['audio_source']['root'], set(expected))
        errors.extend(problems)
        if set(actual) != set(available_ids):
            errors.append('local r001 audio coverage differs from the plan; refresh bindings and author new beats')
        for line in lines:
            lid = line['line_id']
            if lid in actual:
                a = actual[lid]
                if any(line['audio'].get(k) != a.get(k) for k in a):
                    errors.append(f'{lid}: stale WAV/JSON timing or hash binding')
                if (line['text'],line['speaker'],line['performance_style']) != (a['metadata_text'],a['metadata_speaker'],a['metadata_style']):
                    errors.append(f'{lid}: line text/speaker/style differs from recording metadata')
        for scene in plan['audio_scenes']:
            ids = scene['line_ids']
            if scene['status'] == 'available_in_r001' and not all(lid in actual for lid in ids):
                errors.append(f"{scene['id']}: scene readiness claims missing line audio")
            assembly = scene.get('assembly')
            if assembly:
                try:
                    if not all(lid in actual for lid in ids):
                        raise ValueError('assembly cannot certify missing line audio')
                    facts = wav_facts(local(root,assembly['path']))
                    if any(assembly.get(k) != v for k,v in facts.items()):
                        raise ValueError('scene WAV duration/hash binding changed')
                except (ValueError,OSError,wave.Error,EOFError) as exc:
                    errors.append(f"{scene['id']}: {exc}")
        summary = local(root, plan['audio_source']['timing_summary'])
        if not summary.is_file() or digest(summary) != plan['audio_source']['timing_summary_sha256']:
            errors.append('r001 scene/line timing summary changed; refresh bindings')
        else:
            timing = read(summary)
            for scene in plan['audio_scenes']:
                if scene.get('assembly'):
                    row=timing.get(str(int(scene['id'][1:])), {})
                    if abs(row.get('seconds', -1)-scene['assembly']['duration_seconds']) > .02:
                        errors.append(f"{scene['id']}: timing summary differs from actual scene WAV")
            for line in lines:
                if line['line_id'] not in actual:
                    continue
                row = next((r for r in timing.get(str(int(line['audio_scene'][1:])), {}).get('lines', []) if r['id'] == line['line_id']), None)
                if row is None or row['speaker'] != line['speaker'] or abs(row['seconds']-line['audio']['duration_seconds']) > .02:
                    errors.append(f"{line['line_id']}: r001 timing summary inconsistent with actual line WAV")
    if plan.get('performance_library'):
        try:
            try:
                from . import character_performance as performance
            except ImportError:
                import character_performance as performance
            library_path = local(root or ROOT, plan['performance_library'])
            library = read(library_path)
            errors.extend(performance.validate(library, plan, characters, root,
                folder=library_path.parent if root is not None else None))
        except (ValueError, KeyError, OSError) as exc:
            errors.append(f'Performance library: {exc}')
    return errors


def load(root, story):
    folder = local(root, f'stories/{story}')
    return folder, read(folder/'audio_visual_plan.json'), read(folder/'character_library.json'), read(folder/'location_library.json')


def summary(plan, locations):
    beats = [b for l in plan['lines'] for b in l['beats']]
    images = [im for b in beats for im in b['image_sequence']['images']]
    from collections import Counter
    return {'available_audio_scenes':[s['id'] for s in plan['audio_scenes'] if s['status']=='available_in_r001'],
        'available_lines':sum(l['audio']['status']=='available_in_r001' for l in plan['lines']),
        'script_lines':len(plan['lines']),'lines_planned':sum(bool(l['beats']) for l in plan['lines']),
        'recorded_lines_pending_visual_authoring':sum(l['planning_status']=='pending_visual_authoring' for l in plan['lines']),
        'pending_audio_lines':sum(l['audio']['status']=='not_available_in_r001' for l in plan['lines']),
        'visual_beats':len(beats),'image_placeholders':len(images),
        'unique_planned_images':sum(not im.get('reuse_of') for im in images),
        'image_roles':dict(Counter(im['role'] for im in images)),
        'sequence_modes':dict(Counter(b['image_sequence']['mode'] for b in beats)),
        'continuity_groups':len(plan['continuity_groups']),
        'planned_new_views':[key for key,v in locations['views'].items() if v['status']=='planned'],
        'location_families':list(locations['families']), 'new_physical_location_families':[],
        'generated_images':0,'approved_scene_images':0,
        'generated_location_view_candidates':sum(len(v.get('candidates',[])) for v in locations['views'].values()),
        'owner_approved_location_views':sum(v['status']=='owner_approved_view' for v in locations['views'].values()),
        'active_owner_approved_location_views':sum(v['status']=='owner_approved_view' and not v.get('active_plan_status','').startswith('superseded') for v in locations['views'].values()),
        'world_region_families':[k for k,v in locations['families'].items() if v.get('kind')=='world_region']}


def readiness(plan, chars, locs, root, gate):
    errors = validate(plan, chars, locs, root)
    if errors or gate == 'planning':
        return errors
    if plan.get('performance_library'):
        try:
            from . import character_performance as performance
        except ImportError:
            import character_performance as performance
        errors.extend(performance.validate(read(local(root, plan['performance_library'])),
            plan, chars, root, gate='image'))
    for name, actor in chars['characters'].items():
        ref = actor['canonical']
        path = local(root, ref['path'])
        if not path.is_file() or digest(path) != ref['sha256']:
            errors.append(f'{name}: canonical bytes differ from approval ledger; owner reconciliation required')
    for key, view in locs['views'].items():
        if view['status'] == 'planned':
            stage = 'generated location candidate awaits owner selection/review' if view.get('candidates') else 'planned location view needs generation/provenance/review'
            errors.append(f'{key}: {stage}')
        if view.get('source'):
            path = source_file(root,view['source']['path'])
            if not path.is_file() or digest(path) != view['source']['sha256']:
                errors.append(f'{key}: location master bytes changed')
    for line in plan['lines']:
        for beat in line['beats']:
            errors.append(f"{beat['id']}: planned key images, anatomy/scale/contact and owner review pending")
    if gate == 'video':
        errors.append('No video export: approved stills, aligned phrase/key timing and reviewed dialogue/takes are required')
        if any(l['audio']['status'] != 'available_in_r001' for l in plan['lines']):
            errors.append('Full-story video coverage blocked by pending r001 audio')
    return errors


def future_intervals(plan):
    """Derive possible adjacent image edges only, without inventing clip times."""
    result = []
    for line in plan['lines']:
        for beat in line['beats']:
            mode = beat['image_sequence']['mode']
            images = beat['image_sequence']['images']
            pairs = list(zip(images, images[1:])) if mode in {'pair','multi_key'} else [(im,im) for im in images]
            for index,(a,b) in enumerate(pairs,1):
                result.append({'id':f"{beat['id']}-D{index:02d}",'beat_id':beat['id'],
                    'planned_first_image':a['id'],'planned_last_image':b['id'],
                    'join':'editorial_cut' if mode=='cut_sequence' else 'single_image_hold' if a is b else 'within_beat_action',
                    'start_seconds':None,'end_seconds':None,
                    'status':'candidate_structure_only; approved_images_and_reviewed_timing_required',
                    'actual_generated_first':None,'actual_generated_last':None})
    return result


def derive(folder, plan, chars, locs):
    stats = summary(plan,locs)
    from production.sequence_plan import selection_catalog, resolve_sequence
    selected=selection_catalog(folder)
    stats['selected_scene_uses']=len({i.get('image_id') or i['path'] for i in selected})
    stats['selected_scene_rasters']=len({i['sha256'] for i in selected})
    write(folder/'derived/sequence_realization_index.json',{'schema':'feltwillow.sequence-index.v1','derived_from':'audio_visual_plan.json + scoped selection records','sequences':{sid:resolve_sequence(plan,sid,ROOT,selections=selected) for sid in plan.get('production_sequences',{})}})
    if plan.get('performance_library'):
        try:
            from . import character_performance as performance
        except ImportError:
            import character_performance as performance
        library_path = folder/'character_performance_library.json'
        if not library_path.exists():
            library_path = local(ROOT, plan['performance_library'])
        report = performance.derive(folder, read(library_path), plan, chars)
        stats['performance'] = report['counts']
    composition_file = folder/'scene_composition_candidates.json'
    compositions = json.loads(composition_file.read_text())['images'] if composition_file.exists() else []
    # The opening registry is retained as exact-hash historical provenance.
    # New production stages append associations through their own registry.
    continuation_file = folder/'scene_composition_candidates_s06_s07.json'
    if continuation_file.exists():
        compositions += read(continuation_file)['images']
    s08_file = folder/'scene_composition_candidates_s08.json'
    if s08_file.exists():
        compositions += read(s08_file)['images']
    stats['generated_scene_composition_candidates'] = len(compositions)
    write(folder/'derived/audio_visual_summary.json',stats)
    write(folder/'derived/future_clip_candidates.json',{'derived_from':'audio_visual_plan.json',
        'not_a_runtime_export':True,'intervals':future_intervals(plan)})
    lines = ['# Audio-line visual inventory (derived)', '',
        'Authored source: `audio_visual_plan.json`. Actual r001 WAVs own duration; phrase/key timing is pending alignment. Planned counts are not generated media.', '',
        f"Available: {stats['available_lines']} lines in {len(stats['available_audio_scenes'])} audio scenes. Planned: {stats['visual_beats']} beats, {stats['image_placeholders']} image slots ({stats['unique_planned_images']} unique planned images). Pending audio: {stats['pending_audio_lines']} lines.", '',
        'Sequence modes: '+json.dumps(stats['sequence_modes'])+'. Roles: '+json.dumps(stats['image_roles'])+'.', '',
        f"Location families: {', '.join(stats['location_families'])}. New physical families: none. Planned views: {len(stats['planned_new_views'])}. Explicit continuity groups: {stats['continuity_groups']}.", '',
        f"Generated location-view images: {stats['generated_location_view_candidates']}; owner-approved location views: {stats['owner_approved_location_views']}. Scene-composition candidates: {len(compositions)}; these records include historical previews and current selected depictions. Scoped selection resolves separately; none establishes complete sequence readiness. See AUDIO_IMAGE_INDEX.md for exact audio-to-file associations.", '']
    image_index = []
    for line in plan['lines']:
        audio = line['audio']
        duration = f"{audio['duration_seconds']:.3f}s" if audio['status']=='available_in_r001' else 'pending r001 audio; no duration'
        lines += [f"## {line['line_id']} · {line['speaker']} · {duration}", '', line['text'], '']
        if not line['beats']:
            lines += [('Recorded audio available; visual authoring and phrase alignment pending.' if audio['status']=='available_in_r001' else 'Script retained; visual authoring/timing pending actual r001 audio.'), '']
            continue
        lines += ['| Beat | Semantic span / visual intent | Family / view | Framing | Transition in → out / group | Image mode / count | Timing / status |', '|---|---|---|---|---|---|---|']
        for beat in line['beats']:
            lines.append(f"| {beat['id']} | {beat['semantic_span']} — {beat['action']} | {beat['location_family']} / {beat['location_view']} | {beat['shot_type']} / {beat.get('background_continuity','unspecified')} | {beat['transition_in']} → {beat['transition_out']} / {beat['continuity_group'] or 'none'} | {beat['image_sequence']['mode']} / {len(beat['image_sequence']['images'])} | {beat['timing']['status']} / planned |")
            view_ids = dict.fromkeys([beat['location_view']] +
                [im['location_view'] for im in beat['image_sequence']['images']])
            for view_id in view_ids:
                for candidate in locs['views'][view_id].get('candidates', []):
                    image_index.append({'line_id':line['line_id'], 'beat_id':beat['id'],
                        'audio_wav':audio['wav'], 'audio_sha256':audio['sha256'],
                        'location_view':view_id, **candidate})
        lines += ['']
        for row in [r for r in image_index if r['line_id']==line['line_id']]:
            lines += [f"Location image for {row['beat_id']}: `{row['path']}`; matching metadata `{row['sidecar']['path']}`. Status: {row['status']}.", '']
    lines += ['## Planned new location views', '']
    for key in stats['planned_new_views']:
        v=locs['views'][key]
        lines.append(f"- `{key}` ({v['family_id']}, {v['lighting']}): {v['purpose']}")
    (folder/'derived/AUDIO_VISUAL_INVENTORY.md').write_text('\n'.join(lines)+'\n')
    image_index.extend(compositions)
    write(folder/'derived/audio_image_index.json', {'schema':'feltwillow.audio-image-index.v1',
        'derived_from':'audio_visual_plan.json + location_library.json + scene_composition_candidates*.json',
        'audio_revision':plan['audio_revision'], 'associations':image_index})
    index = ['# Audio → image index (derived)', '',
        'Filenames begin with the exact audio-line and beat IDs. Location-view approval and scene-key-image approval are separate scopes; the status column records each candidate decision. Scene compositions remain previews until reviewed and selected. Shared views list each use without duplicating image bytes.', '',
        '| Audio line | Beat | Audio WAV | Image file | Status |', '|---|---|---|---|---|']
    for row in image_index:
        index.append(f"| {row['line_id']} | {row['beat_id']} | `{row['audio_wav']}` | `{row['path']}` | {row['status']} |")
    (folder/'derived/AUDIO_IMAGE_INDEX.md').write_text('\n'.join(index)+'\n')
    active_paths = {row['path'] for row in image_index}
    previous = [{'location_view':vid, 'assignment':'not_assigned_in_current_plan', **candidate}
        for vid,view in locs['views'].items() for candidate in view.get('candidates', [])
        if candidate['path'] not in active_paths]
    write(folder/'derived/previous_image_assets.json', {'scope':'preserved outputs/approvals from earlier direction; not current scene selections', 'images':previous})
    historical = ['# Preserved image assets from earlier direction', '',
        'These files and their original approvals/provenance remain intact. They are not assigned to the revised opening; no old approval transfers to a new image.', '',
        '| Prior audio beat | View | File | Asset status |', '|---|---|---|---|']
    for row in previous:
        historical.append(f"| {row['primary_beat_id']} | {row['location_view']} | `{row['path']}` | {row['status']} |")
    (folder/'derived/PREVIOUS_IMAGE_ASSETS.md').write_text('\n'.join(historical)+'\n')
    script = ['# Lion and Mouse v7 — script (derived)', '',
        'Text follows current r001 JSON for available audio. Actual WAV samples own timing. Recorded future lines retain actual audio bindings while their visual beats and phrase alignment remain explicitly pending. Edit audio_visual_plan.json and rederive; historical timing is archived.', '']
    for line in plan['lines']:
        a = line['audio']
        timing = f"{a['duration_seconds']:.3f}s — {a['wav']}" if a['status'] == 'available_in_r001' else 'pending r001 audio; no duration'
        script += [f"## {line['line_id']} · {line['speaker']}", '', line['text'], '', timing, '']
    (folder/'SCRIPT.md').write_text('\n'.join(script).rstrip()+'\n')
    # Compatibility indexes are derived references, not second audio authorities.
    write(folder/'audio_manifest.json',{'schema':'feltwillow.audio-revision-index.v1', 'story':plan['story'],
        'source_story':plan['story'],'active_audio_revision':plan['audio_revision'],
        'authored_plan':'audio_visual_plan.json','audio_source':plan['audio_source'],
        'line_count':len(plan['lines']),'scene_count':len(plan['audio_scenes']),
        'available_line_count':stats['available_lines'],'pending_line_count':stats['pending_audio_lines'],
        'lines':[{'id':l['line_id'],'scene':l['audio_scene'],'speaker':l['speaker'],**l['audio']} for l in plan['lines']],
        'scenes':plan['audio_scenes'],'scope':'current r001 derived index; not byte-identical historical recovery'})
    write(folder/'dialogue_coverage.json',{'story':plan['story'],'schema':'feltwillow.dialogue-line-index.v1',
        'derived_from':'audio_visual_plan.json','duration_authority':plan['audio_source']['root'],
        'lines':[{'id':l['line_id'],'scene':int(l['audio_scene'][1:]),'speaker':l['speaker'],
            'text':l['text'],'performance_direction':l['performance_style'],
            'audio_path':l['audio']['wav'],'audio_sha256':l['audio']['sha256'],
            'duration_seconds':l['audio']['duration_seconds'],'audio_status':l['audio']['status'],
            'visual_beats':[b['id'] for b in l['beats']]} for l in plan['lines']]})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--story',required=True)
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('validate');sub.add_parser('derive')
    ready=sub.add_parser('readiness');ready.add_argument('--sequence');ready.add_argument('--packet',type=Path);ready.add_argument('--stage',choices=['realization','still','timing','execution'],default='execution');ready.add_argument('--mode',choices=['diagnostic','production'],default='diagnostic');ready.add_argument('--gate',choices=['planning','image','video'],default='planning')
    refresh=sub.add_parser('refresh-audio');refresh.add_argument('--write',action='store_true')
    args=parser.parse_args()
    try:
        folder,plan,chars,locs=load(ROOT,args.story)
        if args.command=='refresh-audio':
            actual,errors=inventory_audio(ROOT,plan['audio_source']['root'],set(plan['script_line_order']))
            if errors:raise ValueError('\n'.join(errors))
            added=[]
            for line in plan['lines']:
                if line['line_id'] in actual:
                    facts=actual[line['line_id']]
                    if facts['metadata_text']!=line['text'] or facts['metadata_speaker']!=line['speaker']:
                        raise ValueError(f"{line['line_id']}: new recording text/speaker changed; review semantic plan first")
                    if line['audio']['status']!='available_in_r001':added.append(line['line_id'])
                    if not line['beats']:
                        line['planning_status']='pending_visual_authoring'
                        line['coverage']['phrase_timing_status']='pending_alignment'
                    line['audio']=facts
                    line['performance_style']=facts['metadata_style']
                    line['coverage']['target_duration_seconds']=facts['duration_seconds']
                    for beat in line['beats']:
                        beat['timing']={'status':'pending_alignment','start_seconds':None,'end_seconds':None}
                elif line['audio']['status']=='available_in_r001':
                    raise ValueError(f"{line['line_id']}: previously available bytes missing; restore them rather than downgrading authority")
            plan['audio_source']['timing_summary_sha256']=digest(local(ROOT,plan['audio_source']['timing_summary']))
            for scene in plan['audio_scenes']:
                ready_lines=[l for l in plan['lines'] if l['audio_scene']==scene['id'] and l['audio']['status']=='available_in_r001']
                scene['status']='available_in_r001' if len(ready_lines)==len(scene['line_ids']) else 'not_available_in_r001'
                audio_file=local(ROOT,plan['audio_source']['root'])/f"scene{int(scene['id'][1:]):02d}.wav"
                scene['assembly']=({'path':str(audio_file.relative_to(ROOT)),**wav_facts(audio_file)} if audio_file.is_file() else None)
            if args.write:
                write(folder/'audio_visual_plan.json',plan)
            print(json.dumps({'new_audio_lines':added,'write':args.write,'next':'Author beats for newly recorded lines in audio_visual_plan.json, then validate and derive. No migration or generation is needed.'}))
            return 0
        if args.command=='readiness' and args.sequence:
            from production.sequence_plan import resolve_sequence,fingerprint
            from production.sequence_readiness import evaluate
            packet=json.loads(args.packet.read_text()) if args.packet else resolve_sequence(plan,args.sequence,ROOT)
            if packet['sequence_id']!=args.sequence or packet['source_plan_sha256']!=fingerprint(plan):raise ValueError('packet sequence/plan mismatch; refresh realization')
            result=evaluate(packet,args.stage,args.mode)
            print(json.dumps(result,indent=2))
            return 0 if result['stage_passed'] else 1
        errors=readiness(plan,chars,locs,ROOT,args.gate) if args.command=='readiness' else validate(plan,chars,locs,ROOT)
        if errors:
            for error in errors:print('BLOCKED:',error)
            return 1
        if args.command=='derive':derive(folder,plan,chars,locs)
        print(json.dumps({'planning':'PASS',**summary(plan,locs)},indent=2))
    except (ValueError,KeyError,OSError,wave.Error) as exc:
        parser.exit(1,f'AUDIO_VISUAL_BLOCKED: {exc}\n')
    return 0


if __name__=='__main__':raise SystemExit(main())
