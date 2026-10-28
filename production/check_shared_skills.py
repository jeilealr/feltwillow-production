"""Check shared skill discovery paths before using repository skills (offline)."""
from pathlib import Path
import argparse
import json


def check(root):
    canonical = root / '.claude/skills'
    alias = root / '.agents/skills'
    errors = []
    if not canonical.is_dir() or not alias.is_dir() or alias.resolve() != canonical.resolve():
        return ['Agent and Claude skill directories must resolve to the same collection']
    expected = json.loads((root / '.claude/shared-skills.json').read_text())
    names = sorted(p.name for p in canonical.iterdir() if p.is_dir())
    if names != sorted(expected):
        errors.append('Skill inventory changed: review additions/removals and update .claude/shared-skills.json')
    for name in names:
        skill = canonical / name
        if not (skill / 'SKILL.md').is_file():
            errors.append(f'{name}: missing SKILL.md')
        for p in skill.rglob('*'):
            if p.is_symlink() and not p.exists():
                errors.append(f'Broken resource link: {p}')
        # Opening through both discovery paths must read the identical file.
        if (skill / 'SKILL.md').is_file() and (alias / name / 'SKILL.md').read_bytes() != (skill / 'SKILL.md').read_bytes():
            errors.append(f'{name}: divergent instructions')
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check(args.root)
    print(json.dumps({'shared_skills': 'FAIL' if errors else 'PASS', 'errors': errors}))
    raise SystemExit(bool(errors))
