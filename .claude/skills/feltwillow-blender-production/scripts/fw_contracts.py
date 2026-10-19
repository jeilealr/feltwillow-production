"""Portable advisory checks for NEW Blender manifests, not existing story schemas.

No network calls, scene changes, approvals, payment or security enforcement.
Python 3.10+. See references/contracts.md for limits.
"""
from __future__ import annotations
import hashlib
import json
import math
import re
from datetime import datetime, timezone, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath
from typing import Any

SHA = re.compile(r'^[0-9a-f]{64}$')
ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.:@,-]*$')
ENDPOINTS = frozenset({
    'tripo3d/h3.1/image-to-3d', 'tripo3d/h3.1/multiview-to-3d',
    'fal-ai/patina', 'fal-ai/patina/material', 'fal-ai/patina/material/extract',
})
CHECKS = {
    'character': ('identity', 'anatomy', 'deformation', 'materials', 'motion', 'portability'),
    'environment': ('landmarks', 'camera_envelope', 'support', 'materials', 'ambient', 'portability'),
    'prop': ('identity', 'scale', 'interactions', 'state_transitions', 'portability'),
    'material': ('color', 'mapping', 'temporal_stability', 'portability'),
}

def reject_constant(value: str):
    raise ValueError('Non-finite JSON number: ' + value)

def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result

def load_json(path: Path) -> Any:
    with Path(path).open(encoding='utf-8') as stream:
        return json.load(stream, parse_constant=reject_constant, object_pairs_hook=unique_pairs)

def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                      allow_nan=False).encode('utf-8')

def digest(value: Any, exclude: tuple[str, ...] = ()) -> str:
    if exclude:
        if not isinstance(value, dict):
            raise ValueError('Exclusion requires an object')
        value = {k: v for k, v in value.items() if k not in exclude}
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def safe_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or '\\' in relative or '\x00' in relative:
        raise ValueError('Expected a nonempty repository-relative POSIX path')
    parts = relative.split('/')
    if PurePosixPath(relative).is_absolute() or any(p in ('', '.', '..') for p in parts):
        raise ValueError('Unsafe relative path: ' + relative)
    root = Path(root).resolve()
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root):
        raise ValueError('Path escapes root, including through a symlink')
    return candidate

def number(value: Any) -> bool:
    try:
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
    except OverflowError:
        return False

def integer(value: Any) -> bool:
    return type(value) is int

def money(value: Any) -> Decimal:
    if isinstance(value, bool) or value is None:
        raise ValueError('Cost must be a finite nonnegative decimal')
    try:
        n = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError('Invalid decimal cost') from exc
    if not n.is_finite() or n < 0:
        raise ValueError('Cost must be finite and nonnegative')
    return n

def timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError('Timestamp must be ISO 8601 text with timezone')
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('Timestamp needs timezone')
    return dt.astimezone(timezone.utc)

def binding_errors(binding: Any, root: Path, label: str) -> list[str]:
    if not isinstance(binding, dict):
        return [label + ': expected path/hash object']
    errors = []
    d = binding.get('sha256')
    if not isinstance(d, str) or not SHA.fullmatch(d):
        errors.append(label + ': valid SHA-256 required')
    try:
        p = safe_path(root, binding.get('path'))
        if not p.is_file():
            errors.append(label + ': file missing')
        elif isinstance(d, str) and SHA.fullmatch(d) and sha256_file(p) != d:
            errors.append(label + ': file hash mismatch')
    except (ValueError, OSError) as exc:
        errors.append(label + ': ' + str(exc))
    return errors

def list_bindings(value: Any, root: Path, label: str, nonempty: bool = True) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        return [label + ': nonempty bindings list required']
    errors, paths = [], set()
    for i, item in enumerate(value):
        errors.extend(binding_errors(item, root, f'{label}[{i}]'))
        path = item.get('path') if isinstance(item, dict) else None
        if isinstance(path, str):
            if path in paths:
                errors.append(label + ': duplicate path ' + path)
            paths.add(path)
    return errors

def validate_asset(doc: Any, root: Path, require_approved: bool = False) -> list[str]:
    if not isinstance(doc, dict):
        return ['asset: expected JSON object']
    errors = []
    if doc.get('schema') != 'feltwillow.blender.asset.v1':
        errors.append('asset: unsupported schema')
    if not isinstance(doc.get('asset_id'), str) or not ID.fullmatch(doc['asset_id']):
        errors.append('asset: invalid asset_id')
    kind = doc.get('kind')
    if not isinstance(kind, str):
        kind = None
    if kind not in CHECKS:
        errors.append('asset: unsupported kind')
    errors += binding_errors(doc.get('candidate'), root, 'candidate')
    errors += list_bindings(doc.get('source_bindings'), root, 'source_bindings')
    if not isinstance(doc.get('design'), dict) or not doc['design']:
        errors.append('asset: design contract required')
    if kind == 'character':
        anatomy = doc.get('anatomy')
        if not isinstance(anatomy, dict):
            errors.append('character: anatomy profile required')
        else:
            app = anatomy.get('appendages')
            ids = []
            if not isinstance(app, list):
                errors.append('character: appendages list required (may be empty for a limbless design)')
            else:
                for entry in app:
                    if not isinstance(entry, dict) or not isinstance(entry.get('id'), str) or not ID.fullmatch(entry['id']) or not entry.get('kind'):
                        errors.append('character: each appendage needs semantic id and kind')
                    else:
                        ids.append(entry['id'])
                if len(ids) != len(set(ids)):
                    errors.append('character: duplicate appendage id')
            modes = anatomy.get('locomotion')
            if not isinstance(modes, list) or not modes or not all(isinstance(x, str) and x for x in modes):
                errors.append('character: locomotion capabilities required')
            measurement = anatomy.get('neutral_measurement', {})
            if not isinstance(measurement, dict) or not measurement.get('definition') or not measurement.get('unit') or not number(measurement.get('value')) or measurement.get('value', 0) <= 0:
                errors.append('character: positive neutral anatomical measurement, unit and definition required')
    if kind == 'environment':
        env = doc.get('environment', {})
        if not isinstance(env, dict) or not env.get('camera_envelope') or not isinstance(env.get('support_surfaces'), list):
            errors.append('environment: camera envelope and support surface list required')
    try:
        spec = digest(doc, ('review',))
    except (ValueError, TypeError):
        errors.append('asset: specification contains non-finite/non-JSON data')
        spec = None
    if require_approved:
        review = doc.get('review')
        if not isinstance(review, dict):
            return errors + ['review: explicit owner/technical evidence missing']
        if review.get('decision') != 'approved' or not review.get('reviewer'):
            errors.append('review: approved decision and actual reviewer required')
        try:
            timestamp(review.get('reviewed_at'))
        except ValueError:
            errors.append('review: valid timezone-aware reviewed_at required')
        if review.get('spec_sha256') != spec:
            errors.append('review: stale specification fingerprint')
        errors += list_bindings(review.get('evidence'), root, 'review.evidence')
        checks = review.get('checks', {})
        if not isinstance(checks, dict):
            checks = {}
        for check in CHECKS.get(kind, ()):
            if checks.get(check) is not True:
                errors.append('review: missing passed check ' + check)
    return errors

def ledger_used(ledger: Any) -> Decimal:
    if not isinstance(ledger, dict) or ledger.get('currency') != 'USD' or not isinstance(ledger.get('entries'), list):
        raise ValueError('ledger: USD currency and entries list required')
    total = Decimal('0')
    ids = set()
    for entry in ledger['entries']:
        if not isinstance(entry, dict) or not isinstance(entry.get('job_id'), str):
            raise ValueError('ledger: job_id required')
        if entry['job_id'] in ids:
            raise ValueError('ledger: duplicate job_id')
        ids.add(entry['job_id'])
        if entry.get('status') == 'settled':
            total += money(entry.get('actual_usd'))
        elif entry.get('status') in ('reserved', 'submitted', 'unknown'):
            total += money(entry.get('maximum_usd'))
        else:
            raise ValueError('ledger: unknown status; unresolved charges must remain reserved')
    return total

def validate_job(doc: Any, ledger: Any, root: Path, now: datetime | None = None) -> list[str]:
    if not isinstance(doc, dict):
        return ['job: expected JSON object']
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('now requires timezone')
    errors = []
    if doc.get('schema') != 'feltwillow.blender.job.v1' or doc.get('provider') != 'fal':
        errors.append('job: unsupported schema/provider')
    if not isinstance(doc.get('endpoint'), str) or doc.get('endpoint') not in ENDPOINTS:
        errors.append('job: endpoint is not in this package allowlist')
    if not isinstance(doc.get('job_id'), str) or not ID.fullmatch(doc['job_id']):
        errors.append('job: invalid job_id')
    if not isinstance(doc.get('settings'), dict):
        errors.append('job: settings object required')
    errors += list_bindings(doc.get('inputs'), root, 'inputs', nonempty=False)
    if doc.get('endpoint') != 'fal-ai/patina/material' and not doc.get('inputs'):
        errors.append('job: image-based endpoint requires bound input files')
    count = doc.get('requests')
    if not integer(count) or count < 1:
        errors.append('job: positive integer requests required')
    try:
        spec = digest(doc, ('approval',))
    except (ValueError, TypeError):
        spec = None
        errors.append('job: non-JSON/non-finite specification')
    price = doc.get('quote', {})
    maximum = None
    try:
        if not isinstance(price, dict) or price.get('currency') != 'USD':
            raise ValueError('quote must use USD')
        maximum = money(price.get('maximum_usd'))
        quoted = timestamp(price.get('quoted_at'))
        ttl = price.get('max_age_hours', 24)
        if not number(ttl) or not 0 < ttl <= 168:
            raise ValueError('quote max_age_hours must be 0-168')
        if quoted > now + timedelta(minutes=5) or now - quoted > timedelta(hours=ttl):
            raise ValueError('quote is stale or in the future')
        if not isinstance(price.get('source_url'), str) or not price['source_url'].startswith('https://fal.ai/'):
            raise ValueError('quote needs a fal pricing/source URL')
    except (ValueError, TypeError) as exc:
        errors.append('quote: ' + str(exc))
    approval = doc.get('approval', {})
    try:
        if not isinstance(approval, dict) or approval.get('decision') != 'approved' or not approval.get('by'):
            raise ValueError('explicit approved decision and owner identity required')
        if approval.get('request_sha256') != spec or spec is None:
            raise ValueError('approval is stale for exact request')
        approved = timestamp(approval.get('at'))
        if approved > now + timedelta(minutes=5):
            raise ValueError('approval time is in the future')
        permitted = approval.get('max_requests')
        if not integer(permitted) or not integer(count) or permitted < count:
            raise ValueError('request count exceeds approval')
        if maximum is not None and maximum > money(approval.get('max_total_usd')):
            raise ValueError('quoted maximum exceeds approved amount')
    except (ValueError, TypeError) as exc:
        errors.append('approval: ' + str(exc))
    try:
        used = ledger_used(ledger)
        cap = money(ledger.get('cap_usd'))
        if maximum is not None and used + maximum > cap:
            errors.append('budget: insufficient unreserved balance under local cap')
        for entry in ledger['entries']:
            if entry.get('job_id') == doc.get('job_id') or (spec and entry.get('request_sha256') == spec):
                errors.append('job: already recorded; inspect existing request rather than resubmit')
    except (ValueError, TypeError) as exc:
        errors.append(str(exc))
    return errors

def vector(value: Any, size: int) -> bool:
    return isinstance(value, list) and len(value) == size and all(number(x) for x in value)

def state_errors(state: Any, frame: int, label: str) -> list[str]:
    if not isinstance(state, dict):
        return [label + ': state object required']
    errors = []
    if state.get('global_frame') != frame:
        errors.append(label + ': boundary global_frame mismatch')
    for field in ('environment_sha256', 'camera_sha256', 'lighting_sha256', 'render_settings_sha256'):
        if not isinstance(state.get(field), str) or not SHA.fullmatch(state[field]):
            errors.append(label + ': missing valid ' + field)
    for field in ('assets', 'props', 'actors', 'ambient', 'velocities'):
        if not isinstance(state.get(field), dict):
            errors.append(label + ': ' + field + ' object required')
    assets = state.get('assets', {})
    if isinstance(assets, dict):
        for k,v in assets.items():
            if not isinstance(v,str) or not SHA.fullmatch(v):
                errors.append(label + ': invalid asset hash ' + k)
    actors = state.get('actors', {})
    velocities = state.get('velocities', {})
    if isinstance(actors,dict):
        for name, actor in actors.items():
            if not isinstance(actor,dict) or not vector(actor.get('root_matrix'),16) or not isinstance(actor.get('pose_sha256'),str) or not SHA.fullmatch(actor['pose_sha256']):
                errors.append(label + ': incomplete actor state ' + name)
            vel = velocities.get(name) if isinstance(velocities,dict) else None
            if not isinstance(vel,dict) or not vector(vel.get('linear'),3) or not vector(vel.get('angular'),3) or not isinstance(vel.get('pose_velocity_sha256'),str) or not SHA.fullmatch(vel['pose_velocity_sha256']):
                errors.append(label + ': incomplete velocity state ' + name)
    try:
        canonical_bytes(state)
    except (ValueError,TypeError):
        errors.append(label + ': non-finite/non-JSON state')
    return errors

def validate_chain(doc: Any) -> list[str]:
    if not isinstance(doc,dict):
        return ['chain: expected object']
    errors = []
    if doc.get('schema') != 'feltwillow.blender.chain.v1':
        errors.append('chain: unsupported schema')
    if any(not integer(doc.get(k)) or doc[k] <= 0 for k in ('fps_num','fps_den')):
        errors.append('chain: positive integer rational FPS required')
    shots=doc.get('shots')
    if not isinstance(shots,list) or not shots:
        return errors + ['chain: nonempty shots list required']
    previous = None
    ids = set()
    for i,shot in enumerate(shots):
        label=f'shots[{i}]'
        if not isinstance(shot,dict):
            errors.append(label+': expected object'); previous=None; continue
        sid=shot.get('id')
        if not isinstance(sid,str) or sid in ids or not ID.fullmatch(sid):
            errors.append(label+': missing/duplicate/invalid id')
        else:
            ids.add(sid)
        start,end=shot.get('start'),shot.get('end')
        if not integer(start) or not integer(end) or start < 0 or end <= start:
            errors.append(label+': expected nonnegative half-open frame interval'); previous=None; continue
        errors += state_errors(shot.get('start_state'),start,label+'.start_state')
        errors += state_errors(shot.get('end_state'),end,label+'.end_state')
        join=shot.get('join')
        if i==0 and join != 'start':
            errors.append(label+': first shot join must be start')
        if i>0 and join not in ('continuous','cut'):
            errors.append(label+': join must be continuous or cut')
        if join=='cut' and not shot.get('cut_reason'):
            errors.append(label+': cut needs a reason')
        if previous:
            if previous['end'] != start:
                errors.append(label+': gap or overlap in editorial intervals')
            a,b=previous.get('end_state'),shot.get('start_state')
            if join=='continuous':
                try:
                    if canonical_bytes(a) != canonical_bytes(b):
                        errors.append(label+': continuous boundary states differ')
                except (ValueError,TypeError):
                    errors.append(label+': invalid boundary state')
            elif join=='cut' and isinstance(a,dict) and isinstance(b,dict):
                if a.get('props') != b.get('props') and not shot.get('events'):
                    errors.append(label+': prop change across cut requires an explicit event')
        previous=shot
    return errors
