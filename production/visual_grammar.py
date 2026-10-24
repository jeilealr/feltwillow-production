"""Validate the optional authored visual grammar, independently of media approval.

Legacy planned image slots remain historical planning requirements. Active production
coverage comes from visual_units and their referenced production_sequences instead.
"""
from __future__ import annotations

import copy

ENUMS = {
    'editorial_relationship': {'individual', 'connected'},
    'composition': {'portrait', 'body_or_interaction', 'environment_only', 'detail'},
    'mouth_policy': {'no_mouth_driver', 'dialogue_lipsync', 'diegetic_bite', 'ambience_only'},
    'visual_motion': {'single_i2v', 'ambient_hold', 'paired_motion', 'multi_key_chain', 'controlled_static'},
    'continuity_strength': {'none', 'story_world', 'camera_locked'},
    'connected_scope': {'not_applicable', 'narrative_with_cuts', 'continuous_setup'},
    'status': {'authored', 'blocked', 'reviewed'},
    'boundary_to_next': {'cut', 'motion', 'hold', 'none'},
}
ACTORS = {'MOUSE': 'Milo', 'LION': 'Leo'}


def canonical_sequence_id(plan, sequence_id):
    """Resolve review aliases without creating another editorial use."""
    sequences = plan.get('production_sequences', {})
    seen = set()
    while sequence_id in sequences:
        if sequence_id in seen:
            raise ValueError('sequence alias cycle')
        seen.add(sequence_id)
        target = sequences[sequence_id].get('alias_of_sequence')
        if not target:
            return sequence_id
        sequence_id = target
    raise ValueError(f'unknown sequence {sequence_id}')


def unit_for_sequence(plan, sequence_id):
    sid = canonical_sequence_id(plan, sequence_id)
    found = [u for u in plan.get('visual_units', {}).values() if u.get('sequence_id') == sid]
    if len(found) > 1:
        raise ValueError(f'duplicate visual units for {sid}')
    return found[0] if found else None


def classification_matrix(plan):
    """Return a display-only copy; never write this back as another authority."""
    return {'schema': 'feltwillow.visual-classification.v1',
            'source': 'audio_visual_plan.json#/visual_units',
            'units': copy.deepcopy(plan.get('visual_units', {}))}


def validate_grammar(plan):
    """Return actionable errors; optional on historical plans, strict when present."""
    if 'visual_units' not in plan:
        return []
    units = plan['visual_units']
    if not isinstance(units, dict):
        return ['visual_units must be an object keyed by unit ID']
    lines = {l['line_id']: l for l in plan.get('lines', [])}
    positions = {lid: n for n, lid in enumerate(lines)}
    beats = {b['id']: l['line_id'] for l in lines.values() for b in l.get('beats', [])}
    errors, seen_sequences, scopes = [], set(), {}
    for uid, unit in units.items():
        prefix = f'visual_units.{uid}: '
        try:
            if unit.get('id') != uid:
                raise ValueError('unit identity mismatch')
            for field, allowed in ENUMS.items():
                if unit.get(field) not in allowed:
                    raise ValueError(f'invalid {field}')
            sid = canonical_sequence_id(plan, unit['sequence_id'])
            if sid != unit['sequence_id'] or sid in seen_sequences:
                raise ValueError('one canonical sequence per visual unit required')
            seen_sequences.add(sid)
            seq = plan['production_sequences'][sid]
            lids = unit['audio_line_ids']
            if not lids or len(lids) != len(set(lids)) or any(l not in lines for l in lids):
                raise ValueError('unknown/duplicate audio line')
            if [positions[l] for l in lids] != sorted(positions[l] for l in lids):
                raise ValueError('audio lines must follow story order')
            if not isinstance(unit.get('visible_cast'), list):
                raise ValueError('visible_cast required')
            cast = unit['visible_cast']
            if unit['composition'] == 'environment_only' and cast:
                raise ValueError('environment_only requires zero visible cast')
            speakers = {lines[l]['speaker'] for l in lids}
            if unit.get('speaker') != (next(iter(speakers)) if len(speakers) == 1 else None):
                raise ValueError('speaker conflicts with authoritative audio lines')
            audible = {ACTORS[s] for s in speakers if s in ACTORS}
            policy = unit['mouth_policy']
            if policy == 'dialogue_lipsync' and (not audible or not audible.issubset(set(cast))):
                raise ValueError('dialogue requires the actual visible named speaker; narrator cannot drive lips')
            if unit['composition'] == 'portrait' and audible and policy != 'dialogue_lipsync':
                if not unit.get('dialogue_unsupported_reason') or unit['status'] != 'blocked':
                    raise ValueError('speaking portrait requires dialogue or explicit technical blocker')
            if unit['editorial_relationship'] == 'individual':
                if unit.get('continuity_group_id') is not None or unit['connected_scope'] != 'not_applicable':
                    raise ValueError('individual is not a connected group')
                if unit['visual_motion'] == 'single_i2v' and (len(seq['uses']) != 1 or seq['edges']):
                    raise ValueError('single_i2v requires one actual input and no phantom end')
            else:
                if not unit.get('continuity_group_id') or unit['connected_scope'] == 'not_applicable':
                    raise ValueError('connected group identity and scope required')
            if unit['continuity_strength'] == 'camera_locked':
                if not unit.get('camera_and_crop_lock'):
                    raise ValueError('camera lock identifier required')
                for use in seq['uses']:
                    if set(use.get('visible_cast', cast)) != set(cast):
                        raise ValueError('camera-locked group cast reset requires a cut')
                locks = {u['camera_and_crop_lock'] for u in seq['uses'] if u.get('camera_and_crop_lock')}
                if locks and locks != {unit['camera_and_crop_lock']}:
                    raise ValueError('incompatible camera/crop inside locked group')
            if unit['boundary_to_next'] == 'cut' and not unit.get('cut_reason'):
                raise ValueError('cut requires a reason')
            scope = unit.get('audio_scope', 'line')
            bids = unit.get('beat_ids', [])
            if scope == 'beat_phrase' and (not bids or any(beats.get(b) not in lids for b in bids)):
                raise ValueError('phrase scope requires exact matching beat IDs')
            for lid in lids:
                for old_scope, old_beats, old_partition in scopes.setdefault(lid, []):
                    if scope == 'line' or old_scope == 'line' or (set(bids) & old_beats and (not unit.get('phrase_partition_id') or not old_partition or unit['phrase_partition_id'] == old_partition)):
                        raise ValueError('duplicate editorial audio coverage')
                scopes[lid].append((scope, set(bids), unit.get('phrase_partition_id')))
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(prefix + str(exc))
    return errors
