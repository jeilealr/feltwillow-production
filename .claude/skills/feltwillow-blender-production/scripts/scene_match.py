#!/usr/bin/env python3
"""Compare existing equal-size display images; never grant visual approval.

Requires Pillow. Optional landmarks are human/agent supplied and hash-bound.
No rendering, model calls, image generation, auto-alignment or source edits.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import shutil
import tempfile

SCHEMA = 'feltwillow.scene-match-landmarks.v1'
COORDS = 'normalized_top_left_pixel_centers'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pairs(items):
    obj = {}
    for key, value in items:
        if key in obj:
            raise ValueError('Duplicate JSON key: ' + key)
        obj[key] = value
    return obj


def _bad_number(value):
    raise ValueError('Non-finite JSON value: ' + value)


def _point(value):
    if value is None:
        return None
    if not isinstance(value, list) or len(value) != 2 or any(
        isinstance(v, bool) or not isinstance(v, (int, float)) or
        not math.isfinite(v) or not 0 <= v <= 1 for v in value
    ):
        raise ValueError('Coordinates must be two finite normalized numbers in [0, 1]')
    return value


def landmark_metrics(data: dict, reference_hash: str, render_hash: str, size: tuple) -> dict:
    if not isinstance(data, dict) or data.get('schema') != SCHEMA:
        raise ValueError('Unsupported landmark schema')
    if data.get('coordinate_system') != COORDS:
        raise ValueError('Unsupported coordinate system')
    if data.get('reference_sha256') != reference_hash or data.get('render_sha256') != render_hash:
        raise ValueError('Landmark hashes are missing or stale for these images')
    points = data.get('points')
    if not isinstance(points, list):
        raise ValueError('Landmarks need a points list')
    width, height = size
    if width < 2 or height < 2:
        raise ValueError('Images must be at least 2 pixels in each dimension')
    diagonal = math.hypot(width - 1, height - 1)
    rows, seen, errors = [], set(), []
    for item in points:
        if not isinstance(item, dict):
            raise ValueError('Each landmark must be an object')
        ident = item.get('id')
        if not isinstance(ident, str) or not ident.strip() or ident in seen:
            raise ValueError('Missing or duplicate landmark ID')
        seen.add(ident)
        ref, cur = _point(item.get('reference_xy')), _point(item.get('render_xy'))
        row = {'id': ident, 'reference_xy': ref, 'render_xy': cur,
               'uncertainty': item.get('uncertainty', 'not supplied')}
        if ref is None or cur is None:
            row.update(status='not_measured', distance_pixels=None)
        else:
            dx, dy = (cur[0] - ref[0]) * (width - 1), (cur[1] - ref[1]) * (height - 1)
            distance = math.hypot(dx, dy)
            row.update(status='measured_not_approved', dx_pixels=dx, dy_pixels=dy,
                       distance_pixels=distance, frame_diagonal_fraction=distance / diagonal)
            errors.append(distance)
        rows.append(row)
    return {'points': rows, 'measured_count': len(errors), 'unmeasured_count': len(rows)-len(errors),
            'mean_distance_pixels': sum(errors)/len(errors) if errors else None,
            'max_distance_pixels': max(errors) if errors else None,
            'warning': 'Supplied correspondences only; not automatic detection, camera calibration or visual acceptance.'}


def _load_display(path: Path, assume_srgb: bool):
    from PIL import Image, ImageOps
    with Image.open(path) as opened:
        if opened.format not in ('PNG', 'JPEG') or opened.mode not in ('RGB', 'RGBA'):
            raise ValueError('Use opaque 8-bit RGB/RGBA PNG or RGB JPEG display exports, not raw EXR/data images')
        if opened.format == 'PNG':
            with path.open('rb') as raw:
                header = raw.read(25)
            if len(header) < 25 or header[24] != 8:
                raise ValueError('Only 8-bit PNG display exports are supported')
        if getattr(opened, 'n_frames', 1) != 1:
            raise ValueError('Animated images are not supported')
        if opened.mode == 'RGBA' and opened.getchannel('A').getextrema() != (255, 255):
            raise ValueError('Composite transparent images explicitly before comparison')
        exif_orientation = opened.getexif().get(274, 1)
        im = ImageOps.exif_transpose(opened).convert('RGB')
        profile = opened.info.get('icc_profile')
        if profile:
            from PIL import ImageCms
            try:
                im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(profile)),
                                              ImageCms.createProfile('sRGB'), outputMode='RGB')
            except Exception as exc:
                raise ValueError('Cannot convert embedded profile to sRGB: ' + path.name) from exc
            handling = 'embedded ICC converted to sRGB'
        elif 'srgb' in opened.info:
            handling = 'PNG sRGB declaration'
        elif assume_srgb:
            handling = 'untagged image explicitly assumed sRGB; verify export settings'
        else:
            raise ValueError('Untagged color: use verified sRGB exports or explicitly pass --assume-srgb')
        return im.copy(), {'color_handling': handling, 'exif_orientation': exif_orientation}


def compare(reference: Path, render: Path, out_dir: Path,
            landmarks: Path | None = None, assume_srgb: bool = False) -> dict:
    from PIL import Image, ImageChops, ImageDraw, ImageStat
    reference, render, out_dir = Path(reference), Path(render), Path(out_dir)
    if out_dir.exists() or out_dir.is_symlink():
        raise ValueError('Output path already exists; choose a new review directory')
    ref, ref_color = _load_display(reference, assume_srgb)
    cur, cur_color = _load_display(render, assume_srgb)
    if ref.size != cur.size or min(ref.size) < 2:
        raise ValueError('Images must have equal dimensions, at least 2x2; no automatic resizing or warping')
    rh, ch = sha256(reference), sha256(render)
    landmark_report = None
    if landmarks:
        data = json.loads(Path(landmarks).read_text(), object_pairs_hook=_pairs, parse_constant=_bad_number)
        landmark_report = landmark_metrics(data, rh, ch, ref.size)
    width, height = ref.size
    diff = ImageChops.difference(ref, cur)
    side = Image.new('RGB', (width*2, height+28), 'white')
    side.paste(ref, (0, 28)); side.paste(cur, (width, 28))
    draw = ImageDraw.Draw(side)
    draw.text((8, 8), 'REFERENCE - display image', fill='black')
    draw.text((width+8, 8), 'RENDER - not an approval', fill='black')
    split = ref.copy(); split.paste(cur.crop((width//2, 0, width, height)), (width//2, 0))
    outputs = {'side_by_side.png': side, 'overlay_50.png': Image.blend(ref, cur, 0.5),
               'split.png': split, 'difference.png': diff}
    if landmark_report:
        marked = side.copy(); pen = ImageDraw.Draw(marked)
        for i, row in enumerate(landmark_report['points'], 1):
            for field, offset in [('reference_xy', 0), ('render_xy', width)]:
                point = row[field]
                if point is not None:
                    x, y = round(point[0]*(width-1)) + offset, round(point[1]*(height-1))+28
                    pen.ellipse((x-4, y-4, x+4, y+4), outline='white', width=2)
                    pen.text((min(x+6,offset+width-18), max(28,y-12)), str(i), fill='white', stroke_width=1, stroke_fill='black')
        outputs['landmarks.png'] = marked
    report = {'schema': 'feltwillow.scene-match-diagnostics.v1',
              'visual_approval': 'not_assessed',
              'reference': {'label': reference.name, 'sha256': rh, **ref_color},
              'render': {'label': render.name, 'sha256': ch, **cur_color},
              'size_px': list(ref.size), 'resized_or_warped': False,
              'mean_absolute_display_channel_error_0_255': ImageStat.Stat(diff).mean,
              'landmarks': landmark_report,
              'warning': 'Encoded display-pixel differences are diagnostic, not perceptual quality, linear-light error, proof of geometry, or owner approval.'}
    out_dir.parent.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix='.scene-match-', dir=out_dir.parent))
    try:
        # Attach an sRGB profile to all diagnostic output when ImageCms is available.
        from PIL import ImageCms
        srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
        for name, image in outputs.items():
            image.save(temp/name, format='PNG', icc_profile=srgb)
        report['outputs'] = {name: sha256(temp/name) for name in outputs}
        (temp/'report.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
        if out_dir.exists() or out_dir.is_symlink():
            raise ValueError('Output appeared during comparison; refusing overwrite')
        temp.rename(out_dir)
    finally:
        if temp.exists():
            shutil.rmtree(temp)
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--reference', type=Path, required=True)
    p.add_argument('--render', type=Path, required=True)
    p.add_argument('--out-dir', type=Path, required=True)
    p.add_argument('--landmarks', type=Path)
    p.add_argument('--assume-srgb', action='store_true', help='Explicitly treat untagged display images as sRGB')
    a = p.parse_args()
    try:
        report = compare(a.reference, a.render, a.out_dir, a.landmarks, a.assume_srgb)
    except (ValueError, OSError, ImportError) as e:
        p.error(str(e))
    print('Diagnostic comparisons saved to', a.out_dir)
    print('Visual approval:', report['visual_approval'])


if __name__ == '__main__':
    main()
