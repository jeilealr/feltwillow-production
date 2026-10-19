"""One-time, fail-closed migration from the preserved 52-unit v7 draft.

The action table is story-specific authored planning. Subsequent production
edits shot_plan.json, not this migration. No generation or approval occurs.
"""
from pathlib import Path
import copy
import hashlib
import json
import math
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from production.paired_images import atomic_json, digest, import_canonical, changed_paths
S = Path(__file__).parent

# One reachable action per entry. Explicit event names govern lasting changes.
ACTIONS = {
'S01-U01': [('Milo explores the introductory forest path', 'walk')],
'S01-U02': [('Milo walks beside the berry bushes', 'walk'), ('Milo pauses beside the stream', 'pause')],
'S01-U03': [('Milo lifts the acorn', 'acorn_pick'), ('Milo enjoys the acorn quietly', 'hold')],
'S02-U01': [('Hold the same stream geography under sunset light', 'hold')],
'S02-U02': [('Milo lifts his ears at the fading light', 'ears')],
'S02-U03': [('Milo stands while holding the acorn', 'stand'), ('Milo sets the acorn beside the flat stone', 'acorn_place')],
'S03-U01': [('Milo pauses where both fork routes are visible', 'pause')],
'S03-U02': [('Milo looks toward the safe left route', 'look_left'), ('Milo looks toward the right shortcut', 'look_right')],
'S03-U03': [('Milo commits to the right shortcut', 'walk')],
'S04-U01': [('Milo runs past the mossy stone', 'run')],
'S04-U02': [('Milo ducks beneath the fallen branch', 'duck'), ('Milo rounds the stump', 'run')],
'S04-U03': [('Milo runs along the shortcut lane', 'run')],
'S05-U01': [('Leo rests beneath the tree with his paw across the path', 'hold')],
'S05-U02': [('Milo approaches the obstructing paw around the root', 'approach_paw'), ('Milo contacts the paw and loses balance', 'trip')],
'S05-U03': [('Milo tumbles with support lost', 'tumble'), ('Milo lands beside the nose', 'land')],
'S05-U04': [('Leo opens his eyes', 'wake'), ('Milo looks up at Leo', 'look_up')],
'S06-U01': [('Leo raises his head', 'head_lift'), ('Milo scrambles onto the path', 'scramble')],
'S06-U02': [('Leo plants one paw beside Milo', 'block')],
'S06-U03': [('Milo freezes beside the blocking paw', 'freeze')],
'S07-U01': [('Leo lowers his gaze toward Milo', 'look_down')],
'S07-U02': [('Milo draws his paws close in apology', 'apology')],
'S08-U01': [('Leo softens his expression', 'soften')],
'S08-U02': [('Leo lifts the blocking paw clear', 'unblock')],
'S08-U03': [('Milo lifts his ears in surprised relief', 'relief')],
'S08-U04': [('Milo gives a small grateful nod', 'nod'), ('Leo gestures toward the darkening sky', 'sky')],
'S09-U01': [('Milo walks carefully toward home', 'walk')],
'S09-U02': [('Hold Leo resting beneath his favorite tree after the time cut', 'hold')],
'S10-U01': [('Leo notices the leaf-covered trigger', 'notice')],
'S10-U02': [('Leo steps closer to the trigger', 'approach_trigger'), ('Leo presses the trigger', 'press')],
'S10-U03': [('The suspended net begins falling', 'drop'), ('The falling net settles over grounded Leo', 'settle')],
'S11-U01': [('Leo gives one careful tug against intact rope', 'tug')],
'S11-U02': [('Leo relaxes after the rope resists', 'pause')],
'S11-U03': [('Leo raises his head for the call', 'head_lift')],
'S12-U01': [('Milo lifts his ears toward the distant call', 'ears')],
'S12-U02': [('Milo runs along the root-lined route', 'run')],
'S12-U03': [('Milo runs beneath the branches toward the trap', 'run')],
'S13-U01': [('Milo arrives at the trapped lion', 'arrive')],
'S13-U02': [('Milo inspects the main knot', 'inspect'), ('Milo steps to the main knot', 'approach_knot')],
'S13-U03': [('Milo gives a small confident nod', 'nod')],
'S13-U04': [('Milo smiles with a closed felt mouth crease', 'smile')],
'S14-U01': [('Milo braces the rope fold with both paws', 'brace'), ('Milo begins felt-lip contact against the rope', 'gnaw')],
'S14-U02': [('Milo works at the same main strand', 'gnaw')],
'S14-U03': [('The main strand fibers become visibly frayed', 'fray'), ('The frayed main strand parts', 'part')],
'S14-U04': [('Milo steps aside from the opening', 'aside'), ('The parted net opening widens', 'open'), ('Leo steps through the opening on four paws', 'escape'), ('The open net falls behind the freed lion', 'discard')],
'S15-U01': [('Leo turns his gaze to Milo', 'look_down')],
'S15-U02': [('Leo gives a gentle grateful nod', 'nod')],
'S15-U03': [('Milo gives a modest paw gesture', 'gesture')],
'S15-U04': [('Leo lowers his head in reflection', 'reflect')],
'S15-U05': [('Leo forms a gentle closed-mouth smile', 'smile')],
'S16-U01': [('Hold the friends resting at the same Great Tree', 'hold')],
'S16-U02': [('The friends exchange a small amused glance', 'glance')],
'S16-U03': [('Hold the warm closing tableau with quiet breathing', 'hold')],
}


def main():
    if (S / 'shot_plan.json').exists():
        raise SystemExit('Migration already applied; edit authored authorities and run derive instead.')
    history = S / 'history' / 'pre_paired_2026-10-19'
    history.mkdir(parents=True, exist_ok=False)
    original = sorted(p for p in S.rglob('*') if p.is_file() and 'history' not in p.parts and p.name != 'migrate_paired.py')
    inventory = []
    for p in original:
        inventory.append({'path': str(p.relative_to(ROOT)), 'sha256': digest(p), 'bytes': p.stat().st_size})
        target = history / p.relative_to(S)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
    unit_plan = json.loads((S / 'visual_unit_plan.json').read_text())
    units = unit_plan['units']
    missing = []
    for u in units:
        for key in ['image_path', 'character_layer']:
            if u.get(key):
                p = ROOT / u[key]
                missing.append({'unit': u['id'], 'role': key, 'path': u[key], 'present': p.is_file(),
                                'expected_sha256': u.get('sha256') if key == 'image_path' else None,
                                'actual_sha256': digest(p) if p.is_file() else None})
    bible = json.loads((ROOT / 'stories/lion_and_mouse_v6/visual_bible.json').read_text())
    chars = {'schema': 'character_library_v1', 'story': 'lion_and_mouse_v7', 'characters': {},
             'scale_contract': {'milo_to_leo': .25, 'review_range': [.22, .28],
                'measurements': {'Milo': 'neutral ear-tip to supporting foot', 'Leo': 'neutral quadrupedal mane-top to supporting paw'},
                'scope': 'same depth, standing equivalent; never raw pose boxes'},
             'performance_references': [], 'pose_calibrations': {}}
    expected = {'Leo': '6b587c8ee2739767bb7af056ee3176ec3d2e698a5bed0e013263814ee8059545',
                'Milo': 'c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f'}
    for name in ['Leo', 'Milo']:
        source = bible['characters'][name.lower()]
        canonical = import_canonical(ROOT, {'path': source['canonical'], 'sha256': expected[name],
            'status': 'owner_approved', 'approval_authority': 'stories/lion_and_mouse_v6/visual_bible.json#' + ('character_foundation_approval.milo_canonical_owner_approval' if name == 'Milo' else 'characters.leo.status'),
            'hash_evidence': 'stories/lion_and_mouse_v6/keyframe_visual_reviews.json'},
            source['canonical'].replace('lion_and_mouse_v6', 'lion_and_mouse_v7'))
        chars['characters'][name] = {'asset_id': name.lower() + '_v6_approved_identity', 'canonical': canonical,
            'voice_speaker': source['voice_speaker'], 'identity': source['identity'],
            'portrait_identity': ("Milo's canonical rounded felt forehead, cheeks, moss-green eyes, two large rounded ears and soft closed mouth crease; no visible teeth."
                if name == 'Milo' else "Leo's canonical amber eyes, nose, pale honey-cream muzzle, tawny mane outline and rounded ears; preserve the full mane."),
            'anatomy_rules': {'visible_teeth': False} if name == 'Milo' else {'paws': 'rounded golden-cream felt toes; no invented nails'},
            'performance_status': 'minimum pilot views need derivation/review; no atlas imported as authority'}
    atomic_json(S / 'character_library.json', chars)
    locs = json.loads((S / 'location_library.json').read_text())
    locs['schema'] = 'location_library_v2'
    locs['environment_scale'] = 'Milo is physically small; readable local-world views magnify actor and forest together. Establishing wides may keep him tiny.'
    locs['setups'] = {}
    physical = {'stream_afternoon': 'stream_bank', 'stream_sunset': 'stream_bank', 'great_tree_dusk': 'great_tree', 'great_tree_day': 'great_tree', 'trap_morning': 'trap_path', 'forest_run_morning': 'forest_run', 'fork_sunset': 'fork', 'shortcut_dusk': 'shortcut'}
    sources = {l['id']: l for l in locs['locations']}
    setup_keys = {}
    for u in units:
        l = sources[u['location_id']]
        if digest(ROOT / l['path']) != l['sha256'] or digest(ROOT / l['source_path']) != l['source_sha256']:
            raise ValueError('location bytes differ: ' + l['id'])
        l['physical_location_id'] = physical.get(l['id'].replace('v7_loc_', ''), l['id'].replace('v7_loc_', ''))
        key = (l['id'], tuple(u['camera_view']['crop_rect_norm']), 'portrait' if u['framing'] == 'close' else u['framing'])
        if key not in setup_keys:
            setup_id = f"{l['physical_location_id']}_{len(setup_keys)+1:02d}"
            setup_keys[key] = setup_id
            locs['setups'][setup_id] = {'id': setup_id, 'physical_location_id': l['physical_location_id'],
                'plate': {'path': l['path'], 'sha256': l['sha256']}, 'lighting': l['time'],
                'crop_rect_norm': u['camera_view']['crop_rect_norm'], 'output_size': [1536, 864],
                'framing': key[2], 'allow_offscreen_support': key[2] == 'portrait',
                'visible_prop_ids': ['acorn'] if l['physical_location_id']=='stream_bank' else ['trigger','net','rope','main_strand_id','net_anchors'] if l['physical_location_id']=='trap_path' else [],
                'support_zones': {}, 'landmarks': l['landmarks'],
                'status': 'candidate_needs_foundation_review', 'support_and_axis_status': 'named anchors below require measured coordinates and visual review',
                'anchor_ids': ['ground_route', 'flat_stone'] if l['physical_location_id'] == 'stream_bank' else
                    ['root_turn', 'leo_paw', 'nose_landing', 'ground_route'] if l['physical_location_id'] == 'great_tree' else
                    ['trigger', 'main_knot', 'ground_attachments', 'ground_route'] if l['physical_location_id'] == 'trap_path' else ['ground_route'],
                'axis_policy': 'preserve registered geography; S15 proposes Milo left, Leo right; confirm in foundation',
                'source_resolution_status': 'close crops need native-detail review before adoption'}
        u['_paired_setup'] = setup_keys[key]
    atomic_json(S / 'location_library.json', locs)
    audio = json.loads((S / 'audio_manifest.json').read_text())
    for entry in audio['lines'] + audio['scenes']:
        entry['runtime_path'] = entry['v7_path']
        entry.pop('v6_path', None)
        entry['availability'] = 'verified' if (ROOT / entry['runtime_path']).is_file() and digest(ROOT / entry['runtime_path']) == entry['sha256'] else 'missing_restore_exact_bytes'
        missing.append({'role': 'audio', 'path': entry['runtime_path'], 'present': entry['availability'] == 'verified',
                        'expected_sha256': entry['sha256'], 'source_path': entry['source_v6_path']})
    audio['schema'] = 'versioned_audio_manifest_v1'
    audio['runtime_story'] = 'lion_and_mouse_v7'
    audio['verification_status'] = 'missing_local_recordings; timing_metadata_only'
    atomic_json(S / 'audio_manifest.json', audio)
    coverage = json.loads((S / 'dialogue_coverage.json').read_text())
    coverage['story'] = 'lion_and_mouse_v7'
    coverage['status'] = 'paired_planning_provisional_missing_local_audio'
    byline = {l['id']: l for l in audio['lines']}
    for line in coverage['lines']:
        line['audio_path'] = byline[line['id']]['runtime_path']
    atomic_json(S / 'dialogue_coverage.json', coverage)
    spans = {}
    for scene in audio['scenes']:
        lines = [l for l in audio['lines'] if l['scene'] == scene['scene']]
        cursor = 0.
        for n, line in enumerate(lines):
            duration = line['duration_seconds']
            pause = (1. if n == len(lines)-1 else .45 if line['speaker'] == lines[n+1]['speaker'] else .7)
            spans[line['id']] = {'scene': scene['scene'], 'start': round(cursor, 5), 'end': round(cursor+duration+pause,5),
                'speech_end': round(cursor+duration,5), 'speaker': line['speaker'], 'status': 'copied_metadata_unverified'}
            cursor += duration + pause
        if abs(cursor - scene['duration_seconds']) > .02:
            raise ValueError('audio metadata assembly differs')
    world = {'actors': {
        'Milo': {'location': 'forest_run', 'anchor': 'ground_route', 'support': 'ground', 'pose': 'upright', 'gaze': 'route', 'mouth': 'closed'},
        'Leo': {'location': 'great_tree', 'anchor': 'rest_under_tree', 'support': 'ground', 'pose': 'sleeping', 'gaze': 'eyes_closed', 'mouth': 'closed'}},
        'props': {'acorn': 'at_stream', 'trigger': 'unpressed', 'net': 'suspended', 'rope': 'intact',
                  'main_strand_id': 'main_knot_strand_01', 'net_anchors': 'trap_ground_attachments_01'}}
    plan = {'schema': 'paired_keyframes_v1', 'story': 'lion_and_mouse_v7',
        'timing_status': 'provisional_uniform_action_windows_not_word_alignment',
        'timing_note': 'Full playback spans partitioned provisionally, including pauses/tails. Restore WAVs, align words and review action timing before freezing render pieces.',
        'state_event_rules': [{'path': 'props.trigger', 'transitions': [{'before': 'unpressed', 'after': 'pressed', 'event': 'press'}]}, {'path': 'props.rope', 'transitions': [{'before': 'intact', 'after': 'frayed', 'event': 'fray'}, {'before': 'frayed', 'after': 'parted', 'event': 'part'}]}, {'path': 'props.net', 'transitions': [{'before': 'suspended', 'after': 'falling', 'event': 'drop'}, {'before': 'falling', 'after': 'settled', 'event': 'settle'}, {'before': 'settled', 'after': 'opened', 'event': 'open'}, {'before': 'opened', 'after': 'discarded', 'event': 'discard'}], 'requires': {'open': [{'path': 'props.rope', 'value': 'parted'}], 'discard': [{'path': 'props.rope', 'value': 'parted'}]}}],
        'audio_spans': spans, 'states': {}, 'endpoints': {}, 'pieces': [], 'migration_map': {},
        'decisions': {'S01-U01': 'Retain morning forest as an introductory time/location view; explicit cut to afternoon stream, not a continuous afternoon run.',
                      'S09': 'Montage time cut; no interpolation across days.',
                      'same_state_handoffs': 'Use shared endpoint only in identical setup; close views use camera cuts of the same state.'}}
    state_counter = 0
    def state(value):
        nonlocal state_counter
        state_counter += 1
        sid = f'world_{state_counter:04d}'
        plan['states'][sid] = copy.deepcopy(value)
        return sid
    current = state(world)
    previous = None
    for u in units:
        actions = ACTIONS[u['id']]
        start_time = spans[u['line_ids'][0]]['start']
        end_time = spans[u['line_ids'][-1]]['end']
        # Each action window is provisional. Long windows are incremental phases
        # of that single action, never fabricated exact word/sentence boundaries.
        windows = []
        for i, (action, event) in enumerate(actions):
            a = start_time + (end_time-start_time)*i/len(actions)
            b = start_time + (end_time-start_time)*(i+1)/len(actions)
            parts = max(1, math.ceil((b-a)/6.0))
            for j in range(parts):
                windows.append((action, event, j, parts, a+(b-a)*j/parts, a+(b-a)*(j+1)/parts))
        plan['migration_map'][u['id']] = []
        setup_id = u['_paired_setup']
        setup = locs['setups'][setup_id]
        for n, (action, event, phase, phases, begin, end) in enumerate(windows):
            setup_id = u['_paired_setup']
            setup = locs['setups'][setup_id]
            if setup['framing'] == 'portrait':
                subject = 'Leo' if action.startswith('Leo ') else 'Milo'
                base_id = setup_id
                setup_id += '_' + subject.lower()
                if setup_id not in locs['setups']:
                    locs['setups'][setup_id] = {**copy.deepcopy(locs['setups'][base_id]),
                        'id': setup_id, 'view_subject': subject,
                        'framing_review': 'candidate crop inherited from old unit; confirm upper-body envelope and readable subject before approval'}
                setup = locs['setups'][setup_id]
            pid = u['id'].lower().replace('-', '_') + f'_p{n+1:02d}'
            location_change = previous is not None and locs['setups'][previous['setup_id']]['physical_location_id'] != setup['physical_location_id']
            light_change = previous is not None and locs['setups'][previous['setup_id']]['lighting'] != setup['lighting']
            explicit_time = u['id'] in ['S09-U02', 'S16-U01'] and n == 0
            if location_change or light_change or explicit_time:
                # Offscreen actors and every prop persist; only an explicitly
                # travelling visible actor relocates under the documented cut.
                for c in u['cast']:
                    world['actors'][c]['location'] = setup['physical_location_id']
                if u['id'] == 'S05-U01':
                    world['actors']['Milo'].update(location='great_tree', anchor='root_turn')
                current = state(world)
            start_state = current
            start_world = copy.deepcopy(world)
            focal = (('Leo' if action.startswith('Leo ') else 'Milo')
                     if action.startswith(('Leo ', 'Milo ')) else None)
            actor = world['actors'].get(focal)
            # Setups change visibility only. Do not assign the same action pose
            # to both actors (the previous draft did so in the tumble sequence).
            if actor and event != 'hold':
                actor['action_progress'] = {'action': action, 'phase': phase+1, 'phases': phases}
            final = phase == phases-1
            if final:
                if event in ['walk','run']: actor.update(pose=event, support='ground', anchor='ground_route')
                elif event == 'acorn_pick': world['props']['acorn'] = 'held_by_Milo'
                elif event == 'acorn_place': world['props']['acorn'] = 'beside_flat_stone'
                elif event == 'approach_paw': actor.update(anchor='leo_paw_approach', support='ground')
                elif event == 'trip': actor.update(anchor='leo_paw', support='paw_contact_unbalanced', pose='destabilized')
                elif event == 'tumble': actor.update(anchor='between_paw_and_nose', support='airborne', pose='tumbling')
                elif event == 'land': actor.update(anchor='nose_landing', support='ground', pose='seated')
                elif event == 'wake': world['actors']['Leo'].update(gaze='Milo', pose='lying_awake')
                elif event == 'head_lift': world['actors']['Leo']['pose'] = 'head_raised'
                elif event == 'scramble': actor.update(anchor='ground_route', support='ground', pose='upright')
                elif event == 'block': world['actors']['Leo']['anchor'] = 'blocking_paw_beside_Milo'
                elif event == 'unblock': world['actors']['Leo']['anchor'] = 'paw_clear_of_route'
                elif event == 'approach_trigger': world['actors']['Leo']['anchor'] = 'trigger_approach'
                elif event == 'press': world['props']['trigger'] = 'pressed'
                elif event == 'drop': world['props']['net'] = 'falling'
                elif event == 'settle': world['props']['net'] = 'settled'
                elif event == 'arrive': world['actors']['Milo'].update(location='trap_path', anchor='trap_approach', support='ground')
                elif event in ['approach_knot','brace','gnaw']: world['actors']['Milo'].update(anchor='main_knot', pose=event, support='ground_and_rope' if event in ['brace','gnaw'] else 'ground')
                elif event == 'fray': world['props']['rope'] = 'frayed'
                elif event == 'part': world['props']['rope'] = 'parted'
                elif event == 'aside': world['actors']['Milo'].update(anchor='clear_of_opening', support='ground')
                elif event == 'open': world['props']['net'] = 'opened'
                elif event == 'escape': world['actors']['Leo'].update(anchor='outside_net', support='ground', pose='quadrupedal_free')
                elif event == 'discard': world['props']['net'] = 'discarded'
                elif event == 'glance':
                    world['actors']['Leo']['gaze'] = 'Milo'
                    world['actors']['Milo']['gaze'] = 'Leo'
                elif actor and event != 'hold': actor['gaze_or_expression'] = event
            current = state(world) if world != start_world else current
            end_state = current
            if previous and not (location_change or light_change or explicit_time) and previous['setup_id'] == setup_id:
                start_image = previous['end_image']
                handoff = {'type': 'shared_boundary', 'reason': 'same instant and fixed setup; reuse exact previous endpoint'}
            else:
                start_image = pid + '_start'
                handoff = {'type': 'film_start' if previous is None else 'time_cut' if light_change or explicit_time else 'location_cut' if location_change else 'camera_cut',
                    'reason': 'introductory view' if previous is None else 'explicit time/light transition' if light_change or explicit_time else 'travel to registered location' if location_change else 'registered view of the same persistent state'}
                plan['endpoints'][start_image] = {'state_id': start_state, 'setup_id': setup_id, 'status': 'planned'}
            end_image = start_image if start_state == end_state else pid + '_end'
            plan['endpoints'][end_image] = {'state_id': end_state, 'setup_id': setup_id, 'status': 'planned'}
            intervals = []
            for lid in u['line_ids']:
                a, b = max(begin, spans[lid]['start']), min(end, spans[lid]['end'])
                if b-a > 1e-7: intervals.append({'line_id': lid, 'start': round(a,5), 'end': round(b,5)})
            visible = sorted(u['cast'])
            # Dialogue close views carry only the focal actor. Other characters
            # remain in world state, with no canonical attached to summon them.
            if setup['framing'] == 'portrait' and len(visible)>1: visible = [focal]
            speaking = {spans[x['line_id']]['speaker'] for x in intervals} - {'NARRATOR'}
            visible_speakers = {chars['characters'][c]['voice_speaker'] for c in visible}
            speaker = next(iter(speaking)) if len(speaking)==1 and speaking <= visible_speakers and setup['framing']=='portrait' else None
            p = {'id': pid, 'narrative_units': [u['id']], 'audio_scene': u['audio_scene'],
                'shot_id': f"scene{u['audio_scene']:02d}_{setup_id}", 'setup_id': setup_id,
                'physical_location_id': setup['physical_location_id'], 'lighting': setup['lighting'],
                'visible_cast': visible, 'offscreen_cast': sorted(set(world['actors'])-set(visible)),
                'start_state': start_state, 'end_state': end_state, 'start_image': start_image, 'end_image': end_image,
                'action': action + (f' (incremental phase {phase+1}/{phases})' if phases>1 else ''),
                'event': event if final else 'action_phase', 'allowed_changes': sorted(changed_paths(start_world,world)),
                'handoff': handoff, 'previous_piece': previous['id'] if previous else None,
                'audio_intervals': intervals, 'speaker': speaker, 'boundary_mouth': 'closed',
                'dialogue_status': 'separate reviewed mouth calibration and audio alignment required' if speaking else 'narrator_or_silence_no_lip_motion',
                'support_requirements': 'measured master-space anchor, per-paw contacts and intended occlusion; no planted contact shadow during airborne tumble',
                'reference_bundle': [chars['characters'][c]['asset_id'] for c in visible],
                'required_masks': ['union_start_end_actor_shadow_occlusion_support'],
                'review_dependencies': ['canonical_hashes','setup_foundation','pose_calibration','pair_pixels','sequence_state','owner_selection'],
                'status': 'planned_pending_foundation', 'intermediate_endpoint_required': len(actions)>1,
                'pilot': u['id'] in ['S01-U03','S05-U02','S05-U03','S05-U04','S06-U01','S10-U02','S10-U03','S13-U04','S14-U01','S14-U03']}
            plan['pieces'].append(p); plan['migration_map'][u['id']].append(pid); previous=p
    atomic_json(S / 'location_library.json', locs)
    atomic_json(S / 'shot_plan.json', plan)
    atomic_json(S / 'selection.json', {'schema': 'paired_selection_v1', 'endpoints': {}, 'reviews': {}})
    atomic_json(S / 'migration_report.json', {'starting_head': '8bc175a7444999d6147cd90ae96f82159c7c76dc',
        'starting_branch': 'main', 'starting_worktree': 'clean', 'original_files': inventory, 'asset_recovery': missing,
        'narrative_units': len(units), 'pieces': len(plan['pieces']), 'unique_endpoints': len(plan['endpoints']),
        'shared_boundaries': sum(p['handoff']['type']=='shared_boundary' for p in plan['pieces']),
        'images_generated_this_migration': 0, 'generation_spend': 0,
        'original_records': str(history.relative_to(ROOT)), 'source_policy': 'Do not recover thumbnails as originals; missing candidates require exact bytes or new immutable candidates.'})
    print('Migrated',len(plan['pieces']),'pieces;',len(plan['endpoints']),'unique endpoints')

if __name__ == '__main__': main()
