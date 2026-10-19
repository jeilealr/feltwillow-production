#!/usr/bin/env python3
"""Safely update one Feltwillow skill source and retain its Codex symlink.

Default is dry-run. No network, client configuration, Blender operations or Git
writes. Three-way comparison preserves local changes to files unchanged by this
release; overlapping edits cause a stop before any writes. Stop active agents
before --apply. Python 3.9+ standard library only.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
import uuid
import zipfile

NAME = 'feltwillow-blender-production'
RELATIVE_TARGET = '../../.claude/skills/' + NAME
SCHEMA = 'feltwillow.skill-release-update.v1'
LIMIT = 25 * 1024 * 1024


def digest(data):
    return hashlib.sha256(data).hexdigest()


def _pairs(items):
    out = {}
    for key, value in items:
        if key in out:
            raise ValueError('Duplicate manifest key: ' + key)
        out[key] = value
    return out


def _relative(value):
    if not isinstance(value, str) or not value or '\\' in value or '\0' in value:
        raise ValueError('Unsafe path')
    parts = value.split('/')
    if PurePosixPath(value).is_absolute() or any(p in ('', '.', '..') for p in parts):
        raise ValueError('Unsafe path: ' + value)
    return Path(*parts)


def read_release(archive):
    archive = Path(archive)
    if not archive.is_file():
        raise ValueError('Archive not found: ' + str(archive) + '. Download the new skill.zip and use its exact filename.')
    if archive.stat().st_size > LIMIT:
        raise ValueError('Archive exceeds 25 MiB')
    files, total, names, folded = {}, 0, set(), set()
    with zipfile.ZipFile(archive) as z:
        for item in z.infolist():
            name = item.filename.rstrip('/') if item.is_dir() else item.filename
            rel = _relative(name)
            if rel.parts[0] != NAME or len(rel.parts) < 2:
                if item.is_dir() and rel.parts == (NAME,):
                    continue
                raise ValueError('Archive must contain only the expected skill directory')
            mode = item.external_attr >> 16
            kind = stat.S_IFMT(mode)
            if kind not in (0, stat.S_IFREG, stat.S_IFDIR) or item.flag_bits & 1:
                raise ValueError('Link, special or encrypted archive member refused')
            if item.is_dir():
                continue
            short = Path(*rel.parts[1:]).as_posix()
            if short in names or short.casefold() in folded:
                raise ValueError('Duplicate or case-colliding archive path')
            names.add(short); folded.add(short.casefold())
            total += item.file_size
            if total > LIMIT or item.file_size > LIMIT:
                raise ValueError('Expanded archive exceeds 25 MiB')
            data = z.read(item)
            files[short] = data
    entries = [p for p in files if Path(p).name.upper() == 'SKILL.MD']
    if entries != ['SKILL.md']:
        raise ValueError('Archive must have exactly one root SKILL.md')
    if 'release-update.json' not in files:
        raise ValueError('This is an older/non-upgrade archive. Download the matching current skill.zip with its release manifest, not a pre-update ZIP.')
    m = json.loads(files['release-update.json'], object_pairs_hook=_pairs)
    if m.get('schema') != SCHEMA or m.get('skill_name') != NAME:
        raise ValueError('Unsupported release update manifest')
    baseline = m.get('baseline_sha256')
    if not isinstance(baseline, dict) or not baseline or 'SKILL.md' not in baseline:
        raise ValueError('Missing baseline hashes')
    for name, h in baseline.items():
        _relative(name)
        if not isinstance(h, str) or len(h) != 64 or any(c not in '0123456789abcdef' for c in h):
            raise ValueError('Invalid baseline SHA-256')
        if name not in files:
            raise ValueError('This updater does not perform upstream deletions')
    version_lines = files.get('VERSION', b'').decode().splitlines()
    if not version_lines or version_lines[0] != m.get('version'):
        raise ValueError('VERSION and update manifest disagree')
    # Refuse an archive that has a file where a later member needs a directory.
    for name in files:
        if any(p.as_posix() in files for p in Path(name).parents if str(p) != '.'):
            raise ValueError('Archive file/directory path collision')
    return files, m


def scan(root):
    result = {}
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            p = Path(directory)/name
            mode = p.lstat().st_mode
            if stat.S_ISLNK(mode) or not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
                raise ValueError('Linked or special file inside source refused: ' + str(p))
            if stat.S_ISREG(mode):
                result[p.relative_to(root).as_posix()] = digest(p.read_bytes())
    return result


def layout(repo):
    repo = Path(repo).expanduser().resolve()
    if not repo.is_dir() or not (repo/'.git').exists():
        raise ValueError('Not a Git checkout: ' + str(repo))
    source = repo/'.claude/skills'/NAME
    alias = repo/'.agents/skills'/NAME
    for p in [repo/'.claude', repo/'.claude/skills', repo/'.agents', repo/'.agents/skills', source]:
        if p.is_symlink():
            raise ValueError('Source/parent is a symlink: ' + str(p))
        if p.exists() and not p.is_dir():
            raise ValueError('Expected directory: ' + str(p))
    if not (source/'SKILL.md').is_file():
        raise ValueError('Existing source skill not found; use the installation helper for a fresh install')
    if alias.is_symlink():
        if os.readlink(alias) != RELATIVE_TARGET or alias.resolve() != source:
            raise ValueError('Codex link points somewhere else; refusing to alter it')
    elif alias.exists():
        raise ValueError('Codex path is a separate copy. Reconcile copies before updating; no overwrite performed')
    return repo, source, alias


def make_plan(local, files, baseline):
    changes, conflicts, preserved = [], [], []
    folded = {p.casefold(): p for p in local}
    for name, data in sorted(files.items()):
        new = digest(data)
        old, current = baseline.get(name), local.get(name)
        if name.casefold() in folded and folded[name.casefold()] != name:
            conflicts.append(name + ' (case-colliding local path)')
        elif current == new:
            pass
        elif current is None:
            if old is not None:
                conflicts.append(name + ' (previous file deleted locally)')
            else:
                changes.append(('ADD', name))
        elif old is not None and current == old:
            changes.append(('UPDATE', name))
        elif old is not None and new == old:
            preserved.append(name)
        else:
            conflicts.append(name + ' (local and release edits overlap)')
    return changes, conflicts, preserved


def update(repo, archive, apply=False, backup_dir=None):
    repo, source, alias = layout(repo)
    files, manifest = read_release(archive)
    before = scan(source)
    changes, conflicts, preserved = make_plan(before, files, manifest['baseline_sha256'])
    # Detect local directory/file obstructions before making any filesystem changes.
    for operation, name in changes:
        p = source/_relative(name)
        if p.exists() and not p.is_file():
            conflicts.append(name + ' (local directory occupies file path)')
        for parent in p.parents:
            if parent == source:
                break
            if parent.exists() and not parent.is_dir():
                conflicts.append(name + ' (local file occupies parent directory)')
                break
    print('Source of truth:', source)
    print('Codex link:     ', alias, '->', RELATIVE_TARGET)
    print('Release:', manifest['version'], '| Archive SHA-256:', digest(Path(archive).read_bytes()))
    for op, name in changes:
        print(op + ': ' + name)
    for name in preserved:
        print('PRESERVE LOCAL EDIT (unchanged upstream): ' + name)
    extras = sorted(set(before)-set(files))
    if extras:
        print('PRESERVE LOCAL-ONLY FILES:', len(extras))
    if conflicts:
        raise ValueError('Conflicts; no files changed:\n  ' + '\n  '.join(conflicts) +
                         '\nAsk your local agent to merge these files; do not force overwrite.')
    backups = Path(backup_dir or Path.home()/'.local/state/feltwillow/skill-backups').expanduser().resolve()
    if backups == repo or repo in backups.parents:
        raise ValueError('Backup directory must be outside the repository')
    link_needed = not alias.is_symlink()
    plan = {'changes': changes, 'preserved_local_edits': preserved,
            'preserved_extra_files': extras, 'link_needed': link_needed, 'version': manifest['version']}
    if not apply:
        print('DRY RUN: no files changed. Add --apply after reviewing; stop active agents first.')
        return plan
    if not changes and not link_needed:
        print('ALREADY CURRENT: no writes needed. Both clients share the same files.')
        return plan
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    backup = backups/('update-'+stamp)
    backup.mkdir(parents=True, exist_ok=False)
    shutil.copytree(source, backup/'source-before')
    if scan(backup/'source-before') != before or scan(source) != before:
        raise ValueError('Source changed while backing up. No skill update applied; stop active agents and retry.')
    receipt = {**plan, 'repo': str(repo), 'backup': str(backup), 'source': str(source),
               'archive_sha256': digest(Path(archive).read_bytes()), 'before': before,
               'state': 'backup_created_not_applied'}
    (backup/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    work = Path(tempfile.mkdtemp(prefix='.feltwillow-skill-update-', dir=repo/'.claude'))
    stage, previous = work/'new-source', work/'previous-source'
    moved_old, moved_new, created_link = False, False, False
    try:
        shutil.copytree(source, stage)
        for operation, name in changes:
            p = stage/_relative(name)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(files[name])
            # Plain Python invocation works without executable permission.
            if operation == 'ADD':
                p.chmod(0o644)
        expected = dict(before)
        expected.update({name: digest(files[name]) for _, name in changes})
        if scan(stage) != expected or scan(source) != before:
            raise ValueError('Source/staging changed during preparation; refusing update')
        layout(repo)  # Recheck link and containment immediately before the swap.
        source.rename(previous); moved_old = True
        stage.rename(source); moved_new = True
        if link_needed:
            alias.parent.mkdir(parents=True, exist_ok=True)
            alias.symlink_to(RELATIVE_TARGET); created_link = True
        if scan(source) != expected or not os.path.samefile(source/'SKILL.md', alias/'SKILL.md'):
            raise ValueError('Post-update verification failed')
        receipt.update(state='applied_and_verified', after=expected)
        (backup/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    except BaseException:
        # A normal error/interrupt restores the old directory. Power loss cannot
        # be made transactional across directory operations; the external backup remains.
        if created_link and alias.is_symlink():
            alias.unlink()
        if moved_new and source.exists():
            source.rename(work/'failed-new-source')
        if moved_old and previous.exists():
            previous.rename(source)
        raise
    finally:
        # Never delete a still-unrestored original after a rollback error.
        if not previous.exists() or (source.exists() and scan(source) == expected):
            shutil.rmtree(work)
    print('UPDATED AND VERIFIED:', manifest['version'])
    print('Backup and receipt:', backup)
    print('Both paths resolve to the exact same SKILL.md. Restart Claude Code/Codex in this checkout.')
    print('No Blender, fal, MCP, account, other skill, Git commit or push was changed.')
    return {**plan, 'backup': str(backup)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--backup-dir', type=Path)
    a = p.parse_args()
    try:
        update(a.repo, a.archive, a.apply, a.backup_dir)
    except (ValueError, OSError, zipfile.BadZipFile) as e:
        p.exit(2, 'STOP: ' + str(e) + '\n')


if __name__ == '__main__':
    main()
