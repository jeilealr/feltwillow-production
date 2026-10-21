#!/usr/bin/env python3
"""Verify approved S01-S03 inputs or stage single-image Wan pilots, CPU only.

These pilots test animation. They do not replace the authored visual plan,
complete missing endpoints, align narration or submit GPU jobs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
STORY = 'lion_and_mouse_v7'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Input escapes repository: {name}')
    return path


def verify(root=ROOT, require_audio=False):
    story = root / 'stories' / STORY
    ledger_path = story / 'scene_image_selection.json'
    ledger = json.loads(ledger_path.read_text())
    folder = story / 'handoff/s01_s03'
    proposals = json.loads((folder / 'CLIP_PROPOSALS.json').read_text())
    if ledger['decision'] != 'owner_selected_scene_images' or ledger['reviewer'] != 'project_owner':
        raise ValueError('Owner scene selection is required')
    if proposals['selection_sha256'] != digest(ledger_path):
        raise ValueError('Pilot proposals do not match owner-selected image ledger')
    selected = {}
    for row in ledger['images']:
        if row['path'] in selected:
            raise ValueError('Duplicate selected image')
        for ref in [row, row['sidecar']]:
            if digest(local(root, ref['path'])) != ref['sha256']:
                raise ValueError(f"Selected bytes changed: {ref['path']}")
        selected[row['path']] = row
    if len(proposals['clips']) != len(selected):
        raise ValueError('Pilot/selection coverage differs')
    for clip in proposals['clips']:
        if clip['keyframe'] not in selected or clip['keyframe_sha256'] != selected[clip['keyframe']]['sha256']:
            raise ValueError('Unselected pilot image')
        if clip['mode'] != 'single_image_i2v_pilot' or clip['editorial_duration_seconds'] is not None:
            raise ValueError('Pilots cannot claim final editorial timing')
    audio = json.loads((folder / 'AUDIO_TRANSFER_MANIFEST.json').read_text())
    missing_audio = []
    for ref in audio['files']:
        path = local(root, ref['path'])
        if not path.is_file():
            missing_audio.append(ref['path'])
        elif digest(path) != ref['sha256']:
            raise ValueError(f"Narration bytes changed: {ref['path']}")
    if require_audio and missing_audio:
        raise ValueError(f'{len(missing_audio)} narration WAV files need transfer')
    return proposals, missing_audio


def prepare(root=ROOT, work=None):
    import yaml
    proposals, missing_audio = verify(root)
    if work is None:
        sys.path.insert(0, str(root))
        from feltwillow.paths import WORK
        work = WORK
    story_work = work / 'stories' / STORY
    runtime = {'name': 'S01-S03 approved-image animation pilots', 'characters': {},
               'negative': 'anatomy drift, visible teeth, text, watermark',
               'status': 'pilot_only_not_final_audio_edit', 'scenes': {}}
    copies = []
    for clip in proposals['clips']:
        relative = f"keyframes/opening_pilot/{clip['id']}.png"
        target = story_work / relative
        if target.exists() and digest(target) != clip['keyframe_sha256']:
            raise ValueError(f'Existing frozen keyframe changed: {target}')
        copies.append((local(root, clip['keyframe']), target))
        shot = {k: clip[k] for k in ['prompt', 'negative', 'frames', 'seeds', 'size']}
        shot.update(name=clip['id'], keyframe=relative)
        runtime['scenes'].setdefault(clip['scene'], {'shots': []})['shots'].append(shot)
    output = root / 'stories' / STORY / 'story.yaml'
    contents = yaml.safe_dump(runtime, sort_keys=False, allow_unicode=True)
    if output.exists() and output.read_text() != contents:
        raise ValueError('Existing story.yaml differs; refusing to overwrite a runtime')
    for source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copy2(source, target)
    output.write_text(contents)
    return {'staged_pilots': len(copies), 'runtime': str(output),
            'missing_audio_files': len(missing_audio), 'gpu_jobs_submitted': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'prepare-pilots'])
    parser.add_argument('--require-audio', action='store_true')
    args = parser.parse_args()
    try:
        proposals, missing = verify(require_audio=args.require_audio)
        result = prepare() if args.command == 'prepare-pilots' else {
            'selected_images': len(proposals['clips']), 'missing_audio_files': len(missing),
            'selection': 'verified', 'final_audio_coverage': 'not_ready'}
        print(json.dumps(result, indent=2))
    except (OSError, KeyError, ValueError) as exc:
        parser.exit(1, f'HANDOFF_BLOCKED: {exc}\n')


if __name__ == '__main__':
    main()
