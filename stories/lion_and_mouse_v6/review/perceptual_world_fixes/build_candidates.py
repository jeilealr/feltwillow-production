#!/usr/bin/env python3
"""Reproduce review-only composites using the existing locked-plate compositor.

Requires Pillow, numpy and opencv-python-headless. Does not edit active plans,
keyframes, approval records or video implementation.
"""
import hashlib
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from production.keyframe import compose
from production.materialize_plate_crop import materialize

HOME = Path(__file__).resolve().parent
MANIFEST = HOME / 'candidate_manifest.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads(MANIFEST.read_text())
    frames = {f['id']: f for f in manifest['frames']}
    layers = {f['id']: f for f in manifest['layers']}
    # Preliminary pose QA is recorded before composition; not owner approval.
    for layer in layers.values():
        source = ROOT / layer['output_path']
        if not source.is_file() or sha(source) != layer['sha256']:
            raise ValueError('missing/stale pose source: ' + layer['id'])
        if layer.get('preliminary_review', {}).get('usable_for_review_composition') is not True:
            raise ValueError('pose needs preliminary review: ' + layer['id'])
    # Portrait full-body support lies below frame. Choose the camera to retain
    # full ears and upper chest rather than clipping the ears at h=2.05.
    portrait = frames['s07_p03']
    portrait['proposed_camera'].update(crop_rect_on_plate=[0.62, 0.72, 0.08, 0.08],
                                      magnification=12.5,
                                      standing_equivalent_height_fraction_after_crop={'milo': 1.5})
    portrait['camera_revision_note'] = 'First portrait trial copied its framing reference background; final uses only registered plate soil/root crop, with full-body h=1.5 and support below crop.'
    frames['s04_p01']['proposed_contacts_on_plate']['milo'] = [0.28, 0.7725]
    frames['s04_p01']['proposed_contact_depth_t'] = {'milo': 0.5114}
    frames['s04_p01']['proposed_camera']['standing_equivalent_height_fraction_after_crop'] = {'milo': 0.4096}
    frames['s04_p01']['contact_revision_note'] = 'Planted foot moved from foreground vegetation to clear dirt; revised depth 0.5114 and target follow the registered shortcut near/far model.'
    specs = {
        's04_p01': [('milo_run', .5852, .65, .40, False)],
        's06_p01': [('leo_rest', .45, .8325, .69, False),
                    ('milo_scramble', .7425, .9225, .25, False)],
        's07_p03': [('milo_explain_upper', .5, 1.07, 1.0, True)],
        's16_p05': [('leo_rest', .4305, .8085, .63, False),
                    ('milo_friend', .7665, .8925, .2415, True)],
    }
    reports = []
    for fid, entries in specs.items():
        f = frames[fid]
        source = ROOT / f['materialized_crop']['source_plate']
        crop_path = HOME / (fid + '_proposed_plate_crop.png')
        receipt = materialize(source, f['proposed_camera']['crop_rect_on_plate'], crop_path)
        f['materialized_crop'] = {'path': str(crop_path.relative_to(ROOT)), **receipt}
        normalized = HOME / (fid + '_delivery_background.png')
        with Image.open(crop_path) as raw:
            raw.convert('RGB').resize((1920, 1080), Image.Resampling.LANCZOS).save(normalized)
        blur = 10.0 if fid == 's07_p03' else 0.0
        chars = []
        for layer_id, x, y, height, flip in entries:
            actor = layers[layer_id]['actor']
            if layer_id == 'milo_run':
                contacts = [{'u': .68, 'v': .98, 'rx': .16, 'ry': .025, 'blur': .018}]
            elif layer_id == 'milo_scramble':
                contacts = [{'u': .39, 'v': .98, 'rx': .14, 'ry': .025, 'blur': .018}]
            elif layer_id == 'milo_friend':
                contacts = [{'u': .40, 'v': .985}, {'u': .79, 'v': .975}]
            elif layer_id == 'leo_rest':
                contacts = [{'u': .53, 'v': .94, 'rx': .40, 'ry': .035, 'blur': .02},
                            {'u': .33, 'v': .92, 'rx': .17, 'ry': .025, 'blur': .018},
                            {'u': .72, 'v': .985, 'rx': .12, 'ry': .018, 'blur': .012},
                            {'u': .93, 'v': .965, 'rx': .09, 'ry': .016, 'blur': .012}]
            else:
                contacts = []
            chars.append({'actor': actor, 'pose_layer_id': layer_id,
                          'still': str(ROOT / layers[layer_id]['output_path']),
                          'x': x, 'y': y, 'h': height, 'flip': flip,
                          'light': 0.12, 'shadow': 0.62,
                          'contact_shadows': contacts})
        output = ROOT / f['output_path']
        authority = {'status': 'proposed_bootstrap_anchor_not_owner_approved',
                     'source_plate': str(source.relative_to(ROOT)),
                     'source_plate_sha256': sha(source), 'materialized_crop': receipt,
                     'normalization': 'LANCZOS from exact integer registered crop to 1920x1080; source aspect rounding only',
                     'perceptual_world': f['perceptual_world'],
                     'standing_equivalent_height_targets': f['proposed_camera']['standing_equivalent_height_fraction_after_crop'],
                     'pose_height_note': 'h is visible pose-box height. Relation to standing-equivalent anatomy remains a preliminary calibration proposal needing measured owner review.'}
        record = compose(normalized, chars, output, blur=blur, authority=authority,
                         write_edit_mask=True)
        actual = np.array(Image.open(output).convert('RGB'))
        expected = np.array(Image.open(normalized).convert('RGB')).astype(np.float32)
        if blur:
            expected = cv2.GaussianBlur(expected, (0, 0), sigmaX=blur)
        expected = np.clip(expected, 0, 255).astype(np.uint8)
        mask = np.array(Image.open(output.with_name(output.stem + '_edit_mask.png')))
        mismatches = int(np.count_nonzero(np.any(actual[mask == 0] != expected[mask == 0], axis=1)))
        if mismatches:
            raise RuntimeError(f'{fid}: changed protected background pixels')
        f.update(status='generated_bootstrap_anchor_pending_owner_review',
                 sha256=sha(output), canvas_px=[1920, 1080],
                 generation_tool='built-in ImageGen RGBA pose studies + existing production.keyframe.compose',
                 final_composition_record=str(output.with_suffix('.json').relative_to(ROOT)),
                 normalized_background={'path': str(normalized.relative_to(ROOT)), 'sha256': sha(normalized), 'blur_sigma_px': blur})
        reports.append({'id': fid, 'output_path': f['output_path'], 'sha256': f['sha256'],
                        'canvas_px': [1920, 1080], 'protected_background_mismatched_pixels': mismatches,
                        'actor_boxes_xywh': {x['actor']: x['box'] for x in record['characters']},
                        'visible_pose_height_targets': {x['actor']: x['h'] for x in chars},
                        'owner_approval': None})
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n')
    (HOME / 'composition_verification.json').write_text(json.dumps(reports, indent=2) + '\n')
    print('Composed four review candidates; zero protected-background mismatches.')


if __name__ == '__main__':
    main()
