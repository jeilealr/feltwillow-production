#!/usr/bin/env python3
"""Rebuild current keyframe sheets on Linux or macOS (requires Pillow).

Reads selected paths/hashes without changing plans, decisions or approvals.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]


def build(story: str, root: Path = ROOT) -> None:
    home = (root / 'stories' / story).resolve()
    if home.parent != (root / 'stories').resolve():
        raise ValueError('story must be a story slug')
    plan = json.loads((home / 'keyframe_plan.json').read_text())
    rows = plan['images']
    if not rows or len({row['id'] for row in rows}) != len(rows):
        raise ValueError('empty or duplicate frame inventory')
    boundary_path = home / 'video_boundary_plan.json'
    scenes = json.loads(boundary_path.read_text())['scenes'] if boundary_path.exists() else []
    order = {row['scene']: {fid: i for i, fid in enumerate(row['ordered_keyframes'])}
             for row in scenes}
    # Verify every source before replacing any presentation.
    parents = set()
    for row in rows:
        source = (root / row['candidate_path']).resolve()
        if not source.is_relative_to(root.resolve()):
            raise ValueError(f"source escapes repository: {row['id']}")
        if hashlib.sha256(source.read_bytes()).hexdigest() != row['sha256']:
            raise ValueError(f"selected source hash differs: {row['id']}")
        parents.add(source.parent)
    if len(parents) != 1:
        raise ValueError('selected frames must share one keyframe directory')
    output = parents.pop() / '.review/contact_sheets/current'
    output.mkdir(parents=True, exist_ok=True)
    for scene in sorted({row['scene'] for row in rows}):
        frames = sorted((row for row in rows if row['scene'] == scene),
                        key=lambda row: (order.get(scene, {}).get(row['id'], 10000), row['id']))
        lines = (len(frames) + 2) // 3
        sheet = Image.new('RGB', (1516, 106 + lines * 318), '#202020')
        draw = ImageDraw.Draw(sheet)
        draw.text((24, 22), f'Scene {scene:02d} - current selected keyframes', fill='white')
        for index, row in enumerate(frames):
            x, y = 24 + (index % 3) * 494, 72 + (index // 3) * 318
            with Image.open(root / row['candidate_path']) as source:
                thumbnail = source.convert('RGB').resize((480, 270), Image.Resampling.LANCZOS)
            sheet.paste(thumbnail, (x, y))
            draw.text((x + 2, y + 276), Path(row['candidate_path']).stem, fill='white')
        sheet.save(output / f'scene{scene:02d}_keyframes.png')
    manifest = {'story': story, 'builder': 'production/build_keyframe_contact_sheets.py',
                'images': [{key: row[key] for key in ('id', 'scene', 'candidate_path', 'sha256')}
                           for row in rows]}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Rebuilt {len({row["scene"] for row in rows})} sheets from {len(rows)} selected images.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--story', required=True)
    args = parser.parse_args()
    build(args.story)
