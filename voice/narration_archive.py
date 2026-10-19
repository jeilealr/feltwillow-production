#!/usr/bin/env python3
"""Create/verify a portable SHA-256 manifest for an audio revision, even partial.

No deletion, upload or API calls. Copy the revision to LUMI and a separate
backup, then verify its existing manifest on each destination.
"""
import argparse
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def snapshot(root):
    root = Path(root).resolve()
    paths = sorted(p for p in root.rglob('*') if p.is_file() and p.name not in ['archive_manifest.json', 'SHA256SUMS'])
    if not any(p.suffix == '.wav' for p in paths):
        raise ValueError('No WAV recordings exist yet; nothing to archive.')
    entries = []
    for path in paths:
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError('Archive source cannot contain links outside its revision.')
        relative = path.relative_to(root).as_posix()
        if any(c in relative for c in '\n\r\\'):
            raise ValueError('Archive filenames must not contain line breaks/backslashes.')
        entries.append({'path': relative, 'bytes': path.stat().st_size, 'sha256': sha(path)})
    manifest = {'schema': 'narration_archive_v1', 'scope': 'current saved files, possibly partial; not speech or timing approval', 'files': entries}
    (root / 'archive_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (root / 'SHA256SUMS').write_text(''.join(f"{e['sha256']}  {e['path']}\n" for e in entries))
    return manifest


def verify(root):
    root = Path(root).resolve()
    manifest = json.loads((root / 'archive_manifest.json').read_text())
    errors = []
    for entry in manifest['files']:
        path = (root / entry['path']).resolve()
        if not path.is_relative_to(root):
            errors.append('Unsafe archive path')
        elif not path.is_file() or sha(path) != entry['sha256']:
            errors.append(f"Missing/changed file: {entry['path']}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['snapshot', 'verify'])
    parser.add_argument('--audio-root', required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'snapshot':
            result = snapshot(args.audio_root)
            print(f"Manifest created for {len(result['files'])} saved files; no upload performed.")
        else:
            errors = verify(args.audio_root)
            for error in errors:
                print(error)
            print(f'{len(errors)} checksum errors')
            return bool(errors)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, str(exc) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
