#!/usr/bin/env python3
"""Read-only advisory lint for perceptual-world planning, never visual approval.

No production renderer imports this module. Source hashes bind the observations
and planning warnings to a specific keyframe/staging snapshot.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRATEGIES = {
    'balanced_two_shot', 'speaker_closeup', 'environmental_medium',
    'action_insert', 'environment_establishing', 'establishing_exception',
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(home: Path, root: Path) -> tuple[list[str], list[str]]:
    """Validate metadata/bindings; warn on design targets, without measuring pixels."""
    advisory = json.loads((home / 'perceptual_world_plan.json').read_text())
    plan = json.loads((home / 'keyframe_plan.json').read_text())
    staging = json.loads((home / 'staging_plan.json').read_text())
    errors, warnings = [], []
    if advisory.get('schema') != 'feltwillow.perceptual-world-plan.v1':
        errors.append('unsupported perceptual-world schema')
    if advisory.get('status') != 'advisory_not_visual_approval':
        errors.append('sidecar must remain advisory_not_visual_approval')
    if not advisory.get('story') == plan.get('story') == staging.get('story'):
        errors.append('story identity mismatch')
    for filename in ('keyframe_plan.json', 'staging_plan.json'):
        if advisory.get('source_sha256', {}).get(filename) != digest(home / filename):
            errors.append(f'{filename}: audit snapshot stale; inspect changes before rebinding')
    active = {r['id']: r for r in plan['images']}
    staged = {r['id']: r for r in staging['frames']}
    rows = advisory['frames']
    ids = [r['id'] for r in rows]
    if len(ids) != len(set(ids)):
        errors.append('duplicate advisory frame IDs')
    if set(ids) != set(active) or set(ids) != set(staged):
        errors.append('advisory, active and staged frame inventories differ')
    resolved_root = root.resolve()
    for row in rows:
        fid = row['id']
        if fid not in active or fid not in staged:
            continue
        current, frame = active[fid], staged[fid]
        path = (root / current['candidate_path']).resolve()
        if not path.is_relative_to(resolved_root):
            errors.append(f'{fid}: candidate escapes repository')
        elif not path.is_file() or digest(path) != current['sha256']:
            errors.append(f'{fid}: active PNG missing or bytes differ from plan')
        if any(row.get(k) != current[k] for k in ('candidate_path', 'sha256', 'scene')):
            errors.append(f'{fid}: audit candidate binding is stale')
        actors = set(frame['actors'])
        if set(row.get('characters_present', [])) != actors or row.get('current_view') != frame['view']:
            errors.append(f'{fid}: cast/view snapshot differs from staging')
        world = row.get('perceptual_world')
        if (world == 'shared' and len(actors) < 2 or
                world == 'environment' and actors or
                world not in actors | {'shared', 'environment'}):
            errors.append(f'{fid}: world does not match the staged cast')
        priority = row.get('subject_priority', [])
        if not isinstance(priority, list) or not set(priority) <= actors or (actors and not priority):
            errors.append(f'{fid}: subject priority must name visible actors')
        strategy = row.get('composition_strategy')
        if strategy not in STRATEGIES:
            errors.append(f'{fid}: invalid composition strategy')
        exception = row.get('establishing_exception')
        if strategy == 'establishing_exception':
            if not isinstance(exception, dict) or not exception.get('reason') or not exception.get('companion_frame_ids'):
                errors.append(f'{fid}: establishing exception needs reason and detailed companions')
            else:
                for companion in exception['companion_frame_ids']:
                    if companion == fid or companion not in active:
                        errors.append(f'{fid}: invalid exception companion {companion}')
                warnings.append(f'{fid}: establishing rationale requires human review; no approval inferred')
        actor = row.get('detail_floor_actor')
        floor = row.get('detail_floor_min_frame_height_fraction')
        if actor is not None:
            if actor not in actors or not isinstance(floor, (int, float)) or isinstance(floor, bool) or not math.isfinite(floor) or not 0 < floor <= 1:
                errors.append(f'{fid}: detail floor needs a visible actor and finite fraction in (0,1]')
            else:
                height = frame['actors'][actor].get('standing_equivalent_height_fraction_after_crop')
                if height is not None and height < floor:
                    warnings.append(f'{fid}: planned {actor} standing-equivalent height {height:.3f} < advisory {floor:.3f}; inspect visible face/action, do not resize anatomy')
        elif floor is not None:
            errors.append(f'{fid}: detail fraction has no actor')
        if len(actors) > 1 and current.get('dialogue_speakers'):
            warnings.append(f'{fid}: shared dialogue needs speaker-face preview or registered close coverage')
        if row.get('readability_result') not in {'pass', 'fail', 'needs_review'}:
            errors.append(f'{fid}: invalid readability result')
        elif row['readability_result'] == 'fail':
            warnings.append(f'{fid}: advisory framing failure; existing owner selection remains separate')
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--story', required=True)
    args = parser.parse_args()
    home = (ROOT / 'stories' / args.story).resolve()
    if home.parent != (ROOT / 'stories').resolve():
        parser.error('--story must be a story slug')
    try:
        errors, warnings = validate(home, ROOT)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'ERROR: cannot validate advisory metadata: {exc}')
        return 1
    for entry in errors:
        print(f'ERROR: {entry}')
    for entry in warnings:
        print(f'WARN: {entry}')
    print(f'{len(errors)} errors, {len(warnings)} advisory warnings. No visual approval or generation authorization is granted.')
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
