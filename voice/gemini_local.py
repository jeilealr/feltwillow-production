#!/usr/bin/env python3
"""Set up a local Gemini key outside the repository, or run a voice script.

No authentication/generation requests are made by setup/check. Keys are never
printed or supplied as command arguments. Use the same AI Studio project as
the saved custom voices on LUMI.
"""
import argparse
import getpass
import importlib.util
import os
from pathlib import Path
import shlex
import stat
import subprocess
import sys
import tempfile

KEY_FILE = Path.home() / '.config/gemini/env'
ROOT = Path(__file__).resolve().parents[1]


def read_saved_key(path=KEY_FILE):
    if not Path(path).is_file():
        return None
    for line in Path(path).read_text().splitlines():
        text = line.strip().removeprefix('export ')
        key, sep, value = text.partition('=')
        if sep and key.strip() == 'GEMINI_API_KEY':
            try:
                values = shlex.split(value, comments=True)
            except ValueError:
                raise ValueError('Saved key file has invalid quoting; run setup --replace.') from None
            if len(values) == 1 and values[0].strip():
                return values[0]
    return None


def save_key(key, path=KEY_FILE):
    if not key.strip() or any(c in key for c in '\n\r\x00'):
        raise ValueError('Key must be nonempty and contain no line breaks.')
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.parent.chmod(0o700)
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix='.gemini-key-')
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, 'w') as out:
            out.write('GEMINI_API_KEY=' + shlex.quote(key.strip()) + '\n')
        os.replace(temp, path)
    finally:
        if Path(temp).exists():
            Path(temp).unlink()


def sdk_available():
    try:
        return importlib.util.find_spec('google.genai') is not None
    except ModuleNotFoundError:
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest='command', required=True)
    modes.add_parser('check')
    setup = modes.add_parser('setup')
    setup.add_argument('--replace', action='store_true')
    run = modes.add_parser('run')
    run.add_argument('script', help='repository Python script, e.g. voice/list_voices.py')
    run.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        saved = read_saved_key()
        if args.command == 'setup':
            if saved and not args.replace:
                KEY_FILE.chmod(0o600)
                KEY_FILE.parent.chmod(0o700)
                print('Reusing the saved key; file permissions set to 600. No API request made.')
            else:
                save_key(getpass.getpass('Gemini API key (hidden; same project as LUMI voices): '))
                print('Key saved outside the repository with permissions 600. No API request made.')
        elif args.command == 'check':
            print('Python:', sys.executable)
            print('Saved key:', 'present (not authenticated)' if saved else 'missing')
            if saved:
                print('Key-file permissions:', oct(stat.S_IMODE(KEY_FILE.stat().st_mode)))
            print('google-genai:', 'available' if sdk_available() else 'missing; run python -m pip install google-genai')
            return 0 if saved and sdk_available() and stat.S_IMODE(KEY_FILE.stat().st_mode) == 0o600 else 1
        else:
            key = os.environ.get('GEMINI_API_KEY') or saved
            if not key:
                raise ValueError('No key configured; run python voice/gemini_local.py setup.')
            if saved and stat.S_IMODE(KEY_FILE.stat().st_mode) & 0o077:
                raise ValueError('Saved key permissions are too broad; run setup to secure the existing file.')
            script = (ROOT / args.script).resolve()
            if not script.is_relative_to(ROOT) or not script.is_file() or script.suffix != '.py':
                raise ValueError('Script must be an existing repository Python file.')
            env = dict(os.environ, GEMINI_API_KEY=key)
            env.pop('GOOGLE_API_KEY', None)
            return subprocess.run([sys.executable, str(script), *args.arguments], cwd=ROOT, env=env).returncode
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
