"""V7 adapter for full-resolution pairs, protected-pixel diffs and sequence review.

Writes evidence only, never approvals. Counts and IDs come from shot_plan.
"""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path
import sys

try:
    from .paired_images import (load_story, read, verify, digest, atomic_json,
                                 protected_difference, spec_hash)
except ImportError:
    from paired_images import (load_story, read, verify, digest, atomic_json,
                               protected_difference, spec_hash)

ROOT = Path(__file__).resolve().parents[1]


def geometry_errors(start, end, allowed_changes):
    """Compare measured pose/view-independent geometry, not silhouette boxes."""
    errors = []
    for key in ['setup_id', 'crop_rect_norm', 'output_size', 'lighting', 'identity_hashes']:
        if start.get(key) != end.get(key) or key not in start:
            errors.append(f'incompatible/missing {key}')
    if not start.get('actors') or start.get('actors', {}).keys() != end.get('actors', {}).keys():
        errors.append('visible actor geometry missing/mismatched')
    for actor, a in start.get('actors', {}).items():
        b = end.get('actors', {}).get(actor, {})
        for value in [a, b]:
            if not value.get('pose_calibration_id') or not value.get('support_valid') or not value.get('anatomy_measurements'):
                errors.append(f'{actor}: pose calibration, anatomy measurements or support evidence missing')
        if a.get('neutral_equivalent_plate_px') != b.get('neutral_equivalent_plate_px'):
            errors.append(f'{actor}: unexplained anatomical scaling')
        if a.get('depth_projection_scale') != b.get('depth_projection_scale') and f'actors.{actor}.depth' not in allowed_changes:
            errors.append(f'{actor}: unexplained depth scaling')
        if b.get('support') == 'airborne' and b.get('planted_contact_shadow'):
            errors.append(f'{actor}: airborne subject has planted contact shadow')
    return errors


def review_pair(root, story, piece_id, output, mask_ref, geometry):
    from PIL import Image
    import numpy as np
    folder, plan, chars, locs = load_story(root, story)
    piece = next(p for p in plan['pieces'] if p['id'] == piece_id)
    selection = read(folder / 'selection.json')
    refs = [selection['endpoints'].get(piece[k]) for k in ['start_image', 'end_image']]
    if not all(refs):
        raise ValueError('select both actual endpoint candidates before pair review')
    images = [Image.open(verify(root, r)).convert('RGB') for r in refs]
    mask = Image.open(verify(root, mask_ref)).convert('L')
    pixels = protected_difference(*images, mask)
    errors = geometry_errors(geometry['start'], geometry['end'], piece['allowed_changes'])
    setup = locs['setups'][piece['setup_id']]
    for role in ['start', 'end']:
        measured = geometry[role]
        for key in ['crop_rect_norm', 'output_size', 'lighting']:
            if measured.get(key) != setup[key]:
                errors.append(f'{role}: measured {key} differs from setup')
        if measured.get('setup_id') != piece['setup_id']:
            errors.append(f'{role}: measured setup differs from plan')
        for actor in piece['visible_cast']:
            if measured.get('identity_hashes', {}).get(actor) != chars['characters'][actor]['canonical']['sha256']:
                errors.append(f'{role}/{actor}: wrong canonical identity')
    if not pixels['pass']:
        errors.append('static protected background changed outside allowed support')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    a, b = [np.asarray(im).astype(int) for im in images]
    delta = np.max(np.abs(a-b), axis=2).astype('uint8')
    diff = np.zeros((*delta.shape,3), dtype='uint8')
    diff[:,:,0] = delta
    Image.fromarray(diff).save(output / 'difference.png')
    for role, image in zip(['start','end'], images):
        image.save(output / f'{role}.png')
        for i, box in enumerate(geometry[role].get('detail_boxes_px', [])):
            image.crop(tuple(box)).save(output / f'{role}_detail_{i+1}.png')
    report = {'schema': 'paired_pixel_review_v1', 'piece_id': piece_id,
        'endpoint_ids': [piece['start_image'],piece['end_image']],
        'image_hashes': [r['sha256'] for r in refs], 'mask': mask_ref,
        'authority_sha256': spec_hash([piece,chars,setup]), 'geometry': geometry,
        'pixel_check': pixels, 'technical_errors': errors, 'visual_review': 'pending',
        'owner_approval': 'pending', 'technical_pass': not errors}
    atomic_json(output / 'report.json', report)
    (output / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Pair review</title>'
        '<style>body{font:16px sans-serif;background:#eee}img{max-width:49%}pre{white-space:pre-wrap}</style>'
        f'<h1>{html.escape(piece_id)}</h1><p>Technical evidence; visual and owner approval pending.</p>'
        '<a href="start.png"><img src="start.png"></a><a href="end.png"><img src="end.png"></a>'
        '<h2>Decoded pixel difference</h2><a href="difference.png"><img src="difference.png"></a>'
        '<pre>'+html.escape(json.dumps(report,indent=2))+'</pre>')
    return report


def sequence_page(root, story, output):
    folder, plan, chars, locs = load_story(root, story)
    selection = read(folder/'selection.json')
    output = Path(output)
    output.mkdir(parents=True,exist_ok=True)
    rows = []
    receipt = []
    for piece in plan['pieces']:
        images = []
        for role in ['start','end']:
            endpoint = piece[f'{role}_image']
            chosen = selection['endpoints'].get(endpoint)
            if chosen:
                path = verify(root,chosen)
                # Embed exact bytes: portable review, no fragile cache links.
                import base64
                encoded = base64.b64encode(path.read_bytes()).decode()
                images.append(f'<img alt="{html.escape(endpoint)}" src="data:image/png;base64,{encoded}">')
                receipt.append({'piece':piece['id'],'role':role,'endpoint':endpoint,**chosen})
            else:
                images.append(f'<p>{html.escape(endpoint)}: missing planned image</p>')
        rows.append('<tr><td>'+html.escape(piece['id'])+'<br>'+html.escape(piece['action'])+'<br>'+html.escape(piece['handoff']['type'])+'</td><td>'+images[0]+'</td><td>'+images[1]+'</td></tr>')
    (output/'sequence.html').write_text('<!doctype html><meta charset="utf-8"><title>V7 sequence review</title><style>body{font:14px sans-serif}table{width:100%}td{width:33%;border-bottom:1px solid #aaa}img{width:100%}</style><h1>V7 planned sequence</h1><p>Missing images are listed explicitly. No thumbnail substitutes or inferred approvals.</p><table>'+''.join(rows)+'</table>')
    atomic_json(output/'sequence_manifest.json',{'plan_sha256':digest(folder/'shot_plan.json'),'images':receipt})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--story',required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--piece')
    parser.add_argument('--mask-ref',type=Path)
    parser.add_argument('--geometry',type=Path)
    args=parser.parse_args()
    try:
        if args.piece:
            if not args.mask_ref or not args.geometry:
                parser.error('--piece requires --mask-ref JSON and --geometry JSON')
            report=review_pair(ROOT,args.story,args.piece,args.out,read(args.mask_ref),read(args.geometry))
            return bool(report['technical_errors'])
        sequence_page(ROOT,args.story,args.out)
    except (ValueError,KeyError,OSError,StopIteration) as exc:
        parser.exit(1,f'PAIR_REVIEW_BLOCKED: {exc}\n')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
