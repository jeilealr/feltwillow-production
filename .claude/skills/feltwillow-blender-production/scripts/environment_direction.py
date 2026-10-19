#!/usr/bin/env python3
"""Validate an environment design brief; no aesthetic/owner-approval inference."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

MODES = {'plate_match', 'reference_inspired', 'original_design'}
INVARIANTS = {'character_identity', 'character_physical_scale', 'story_interactions', 'handmade_felt_style'}

def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result

def nonempty(value):
    return isinstance(value, str) and bool(value.strip()) and 'REPLACE' not in value

def string_list(value):
    return isinstance(value, list) and all(nonempty(x) for x in value) and len(value) == len(set(value))

def validate(doc):
    errors = []
    if not isinstance(doc, dict):
        return ['Brief must be a JSON object']
    if doc.get('schema') != 'feltwillow.environment-direction.v1':
        errors.append('Unsupported schema')
    mode = doc.get('mode')
    if not isinstance(mode, str) or mode not in MODES:
        errors.append('Select plate_match, reference_inspired, or original_design')
        mode = None
    direction = doc.get('owner_direction')
    if not isinstance(direction, dict) or not all(nonempty(direction.get(k)) for k in ['text', 'scope']):
        errors.append('Record specific owner direction and scope; placeholders are not ready')
    target = doc.get('target_environment')
    if not isinstance(target, dict) or not all(nonempty(target.get(k)) for k in ['id', 'revision']):
        errors.append('Name the candidate environment ID and revision')
    elif target.get('status') != 'candidate_only':
        errors.append('This brief creates candidates, not automatic publication')
    inv = doc.get('invariants')
    if not string_list(inv) or not INVARIANTS.issubset(set(inv)):
        errors.append('Preserve character identity/physical scale, story interactions and handmade style')
    roles = doc.get('source_roles')
    if not string_list(roles):
        errors.append('source_roles must be unique nonempty strings')
        roles = []
    if mode == 'plate_match' and 'matching_target' not in roles:
        errors.append('plate_match needs a declared matching_target source role')
    if mode == 'reference_inspired' and 'inspiration' not in roles:
        errors.append('reference_inspired needs an inspiration role')
    if mode in {'reference_inspired', 'original_design'} and 'matching_target' in roles:
        errors.append('Do not impose a whole-image matching target in a design mode; name retained invariants separately')
    for field in ['story_requirements', 'required_views']:
        value = doc.get(field)
        if not string_list(value) or not value:
            errors.append(field + ' must contain actual task-specific entries')
    if not string_list(doc.get('creative_freedoms')):
        errors.append('creative_freedoms must be a list; empty is allowed for strict matching')
    if doc.get('legacy_outputs_policy') != 'preserve_unchanged':
        errors.append('Preserve existing approved outputs')
    if doc.get('continuity_policy') not in ['separate_candidate_no_mix', 'reviewed_new_plates', 'explicit_reviewed_transition']:
        errors.append('Declare how a new environment remains separate or is reviewed against older shots')
    review = doc.get('review')
    if not isinstance(review, dict):
        errors.append('Missing review policy')
    else:
        expected = 'plate_correspondence_and_style' if mode == 'plate_match' else 'design_brief_and_style'
        if review.get('target') != expected:
            errors.append('Review target does not match selected mode')
        if review.get('requires_owner_acceptance') is not True or review.get('automatic_visual_approval') is not False:
            errors.append('Require owner acceptance and prohibit automatic visual approval')
    if doc.get('spend_approved') is not False:
        errors.append('Keep design-brief spend_approved false; paid requests require separate scoped approval')
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('brief', type=Path)
    args = parser.parse_args()
    try:
        doc = json.loads(args.brief.read_text(encoding='utf-8'), object_pairs_hook=pairs,
                         parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Non-finite JSON: ' + value)))
        errors = validate(doc)
    except (OSError, ValueError, TypeError) as exc:
        errors = [str(exc)]
    print(json.dumps({'metadata_valid': not errors, 'errors': errors,
                      'visual_approved': False, 'owner_authority_authenticated': False,
                      'note': 'Metadata checks only; no Blender inspection, spending or publication.'}, indent=2))
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
