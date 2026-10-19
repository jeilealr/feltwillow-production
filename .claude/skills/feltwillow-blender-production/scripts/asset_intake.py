#!/usr/bin/env python3
"""Offline external-asset record checks; NOT legal clearance or a downloader.

Read a JSON record, check declared decisions and optional file SHA-256s.
Never import Blender, execute downloaded content, access the network, write files,
modify permissions, approve artwork, or authorize publication.
"""
from __future__ import annotations
import argparse
from datetime import date, datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlsplit

SCHEMA = 'feltwillow.external-asset.v1'
INTENTS = ('research', 'local_test', 'public_bundle')
SHA256 = re.compile(r'^[0-9a-f]{64}$')


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def unique_pairs(items):
    out = {}
    for k, v in items:
        if k in out:
            raise ValueError('Duplicate JSON key: ' + k)
        out[k] = v
    return out


def load_record(path: Path):
    if path.stat().st_size > 2 * 1024 * 1024:
        raise ValueError('Record exceeds 2 MiB')
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Non-finite JSON: ' + x)))


def text(value) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not value.strip().upper().startswith('REPLACE')


def https_url(value) -> bool:
    if not text(value):
        return False
    try:
        u = urlsplit(value)
        return (u.scheme == 'https' and bool(u.hostname) and not u.hostname.endswith('.invalid')
                and not u.username and not u.password and not u.query)
    except ValueError:
        return False


def dated(value) -> bool:
    if not isinstance(value, str):
        return False
    try:
        if len(value) == 10:
            date.fromisoformat(value)
        else:
            datetime.fromisoformat(value.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def binding_check(items, label: str, root: Path, errors: list[str], required=False):
    if not isinstance(items, list):
        errors.append(label + ': expected a file-binding list')
        return
    if required and not items:
        errors.append(label + ': at least one evidence/file binding required')
    seen = set()
    for i, item in enumerate(items):
        tag = f'{label}[{i}]'
        if not isinstance(item, dict):
            errors.append(tag + ': expected object')
            continue
        raw = item.get('path')
        if (not isinstance(raw, str) or not raw or '\\' in raw or '\x00' in raw
                or ':' in raw or raw.startswith('/') or '..' in PurePosixPath(raw).parts):
            errors.append(tag + ': unsafe or missing relative path')
            continue
        if raw in seen:
            errors.append(tag + ': duplicate binding')
        seen.add(raw)
        try:
            p = (root / raw).resolve(strict=True)
            if not p.is_relative_to(root) or not p.is_file():
                raise ValueError('file must be inside root')
        except (OSError, ValueError, RuntimeError):
            errors.append(tag + ': missing or external file')
            continue
        expected = item.get('sha256')
        if not isinstance(expected, str) or not SHA256.fullmatch(expected):
            errors.append(tag + ': missing/invalid SHA-256')
            continue
        try:
            if sha256_file(p) != expected:
                errors.append(tag + ': SHA-256 mismatch')
        except OSError:
            errors.append(tag + ': unreadable file')


def validate(record, root: Path, intent='research') -> dict:
    errors: list[str] = []
    notes = ['Checks supplied metadata and local hashes only. Not legal, security, visual or owner approval.']
    result = {'schema': 'feltwillow.external-asset-check.v1', 'intent': intent,
              'metadata_ok': False, 'production_approved': False,
              'errors': errors, 'notes': notes}
    if intent not in INTENTS:
        errors.append('Unsupported intent')
        return result
    if not isinstance(record, dict):
        errors.append('Expected a JSON object')
        return result
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        errors.append('Root must exist and be a directory')
        return result
    if record.get('schema') != SCHEMA:
        errors.append('Unsupported schema')
    if not text(record.get('asset_id')) or record.get('asset_id', '').startswith('replace_'):
        errors.append('asset_id: set a real unique ID')
    groups = {}
    for key in ('origin', 'rights', 'files', 'storage', 'use', 'inspection'):
        value = record.get(key)
        if not isinstance(value, dict):
            errors.append(key + ': expected object')
            value = {}
        groups[key] = value
    origin, rights, files = groups['origin'], groups['rights'], groups['files']
    storage, use, inspection = groups['storage'], groups['use'], groups['inspection']
    for key in ('provider', 'creator', 'version_or_tier', 'license_id'):
        if not text(origin.get(key)):
            errors.append('origin.' + key + ': required')
    for key in ('asset_url', 'license_url'):
        if not https_url(origin.get(key)):
            errors.append('origin.' + key + ': use a stable HTTPS page URL without credentials/query')
    if not dated(origin.get('checked_at')):
        errors.append('origin.checked_at: use an actual ISO date/time')
    for key in ('commercial_render', 'modification', 'raw_redistribution', 'external_processing_upload'):
        if rights.get(key) not in ('allowed', 'denied', 'unknown'):
            errors.append('rights.' + key + ': expected allowed/denied/unknown')
    attribution = rights.get('attribution_required')
    if attribution is not None and type(attribution) is not bool:
        errors.append('rights.attribution_required: expected boolean or null')
    for key in ('conditions_met',):
        if type(rights.get(key)) is not bool:
            errors.append('rights.' + key + ': expected boolean')
    if not isinstance(rights.get('unresolved_questions'), list):
        errors.append('rights.unresolved_questions: expected list')
    for key in ('publish_originals', 'publish_derivatives', 'source_dependency_audit_complete'):
        if type(storage.get(key)) is not bool:
            errors.append('storage.' + key + ': expected boolean')
    if not text(use.get('purpose')):
        errors.append('use.purpose: state the observed gap')
    acquired = intent != 'research'
    binding_check(origin.get('evidence'), 'origin.evidence', root, errors, acquired)
    binding_check(files.get('originals'), 'files.originals', root, errors, acquired)
    binding_check(files.get('derivatives'), 'files.derivatives', root, errors)
    if acquired:
        for key in ('commercial_render', 'modification'):
            if rights.get(key) != 'allowed':
                errors.append('rights.' + key + ': not documented as allowed for this commercial pilot')
        if not text(origin.get('license_id')) or origin['license_id'].lower() in ('unknown', 'none'):
            errors.append('origin.license_id: license still unknown')
        if rights.get('conditions_met') is not True or rights.get('unresolved_questions'):
            errors.append('rights: conditions/questions remain unresolved')
        if not text(rights.get('reviewer')) or not dated(rights.get('reviewed_at')):
            errors.append('rights: record who checked the actual terms and when')
        if attribution is None:
            errors.append('rights: attribution requirement unknown')
        if attribution is True and (not text(rights.get('attribution_text')) or not text(use.get('credit_destination'))):
            errors.append('rights: required credit text and destination missing')
        if inspection.get('auto_execution_disabled') is not True:
            errors.append('inspection: disable automatic script execution for external intake')
    else:
        notes.append('Research may record unresolved rights; it does not authorize downloading or import.')
    if intent == 'public_bundle':
        if not (storage.get('publish_originals') is True or storage.get('publish_derivatives') is True):
            errors.append('storage: name which asset files the source bundle would publish')
        if rights.get('raw_redistribution') != 'allowed':
            errors.append('rights: render rights do not establish raw/embedded source redistribution')
        if storage.get('source_dependency_audit_complete') is not True:
            errors.append('storage: packed/linked source dependency review incomplete')
        if storage.get('publish_derivatives') is True and not files.get('derivatives'):
            errors.append('files.derivatives: selected publication has no bound derivative files')
    if rights.get('external_processing_upload') != 'allowed':
        notes.append('No recorded permission for external generation processing; do not upload these files.')
    result['metadata_ok'] = not errors
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--root', type=Path, required=True, help='Local containment root for relative file bindings')
    parser.add_argument('--intent', choices=INTENTS, default='research')
    args = parser.parse_args()
    try:
        result = validate(load_record(args.record), args.root, args.intent)
    except (OSError, ValueError, RecursionError) as exc:
        print(json.dumps({'metadata_ok': False, 'production_approved': False, 'errors': [str(exc)]}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result['metadata_ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
