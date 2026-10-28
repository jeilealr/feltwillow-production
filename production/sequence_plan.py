"""Normalize optional v7 production sequences without realizing planned slots.

Selection, technical evidence and causal state are independent authorities.
This module never submits work or changes selected files.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import argparse
import copy
import hashlib
import json
from pathlib import Path
from fractions import Fraction
from PIL import Image
from feltwillow import wan
from production.scene_image_bindings import apply_current_bindings

STATUSES = {
    "selected_exact",
    "selected_alias",
    "selected_hold",
    "candidate_pending_selection",
    "missing_distinct_state",
    "incompatible_for_edge",
    "unavailable_bytes",
    "ambiguous_authority",
}
KINDS = {"motion", "hold", "cut", "shared_boundary"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fingerprint(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


DEPENDENCY_FIELDS = (
    "schema",
    "story",
    "sequence_id",
    "scope_plan_sha256",
    "sequence",
    "resolved_images",
    "edges",
    "size",
    "global_schema_errors",
    "audio_lines",
)


def dependency_fingerprint(packet):
    """Only reviewed scope inputs; later unused selections are not dependencies."""
    payload={k: packet[k] for k in DEPENDENCY_FIELDS}
    if 'visual_unit' in packet:payload['visual_unit']=packet['visual_unit']
    return fingerprint(payload)


def local(root, path):
    result = (Path(root) / path).resolve()
    if not result.is_relative_to(Path(root).resolve()):
        raise ValueError(f"path escapes repository: {path}")
    return result


def sequences(plan):
    section = plan.get("production_sequences", {})
    if not isinstance(section, dict):
        raise ValueError("production_sequences must be an object keyed by sequence ID")
    return section


def validate_sequences(plan):
    errors = []
    images = {
        im["id"]: im
        for l in plan["lines"]
        for b in l["beats"]
        for im in b["image_sequence"]["images"]
    }
    beats = {b["id"]: b for l in plan["lines"] for b in l["beats"]}
    try:
        section = sequences(plan)
    except ValueError as exc:
        return [str(exc)]
    shared_uses = {}
    for sid, seq in section.items():
        try:
            import re

            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", sid):
                raise ValueError("invalid sequence ID")
            if seq.get("id") != sid:
                raise ValueError("sequence identity mismatch")
            if seq.get('alias_of_sequence'):
                target=seq['alias_of_sequence'];seen={sid}
                while True:
                    if target in seen or target not in section:raise ValueError('cyclic/missing sequence alias')
                    seen.add(target);other=section[target]
                    if not other.get('alias_of_sequence'):break
                    target=other['alias_of_sequence']
                if not seq.get('execution_alias') or seq.get('uses') or seq.get('edges'):raise ValueError('review alias must not add execution uses/edges')
                continue
            uses = seq["uses"]
            ids = [u["id"] for u in uses]
            if (
                any(not isinstance(i, str) or not i for i in ids)
                or len(ids) != len(set(ids))
                or not ids
            ):
                raise ValueError("unique nonempty use IDs required")
            aliases = {
                im["id"]: im["reuse_of"] for im in images.values() if im.get("reuse_of")
            }
            for u in uses:
                if u["id"] in shared_uses and shared_uses[u["id"]] != fingerprint(u):
                    raise ValueError("conflicting shared logical use definitions")
                shared_uses[u["id"]] = fingerprint(u)
                if u.get("image_id") and u["image_id"] not in images:
                    raise ValueError("unknown planned image ID")
                if (
                    not u.get("image_id")
                    and not u.get("source")
                    and not u.get("alias_of")
                ):
                    raise ValueError("editorial use requires explicit semantic source")
                if u.get("alias_of"):
                    existing = aliases.get(u["id"]) or aliases.get(u.get("image_id"))
                    if existing and existing != u["alias_of"]:
                        raise ValueError("contradictory alias graphs")
                    aliases[u["id"]] = u["alias_of"]
                if u.get("hold") and not u.get("hold_reason"):
                    raise ValueError("hold requires a reason")
                if u.get("visible_cast") == [] and u.get("image_id"):
                    owner = next(
                        b
                        for b in beats.values()
                        if any(
                            i["id"] == u["image_id"]
                            for i in b["image_sequence"]["images"]
                        )
                    )
                    if owner["cast"]:
                        raise ValueError(
                            "cast-empty editorial role cannot replace character-bearing slot"
                        )
            for n, u in enumerate(uses):
                target = u.get("alias_of")
                if target and target not in ids and target not in images:
                    raise ValueError("missing alias target")
                if target in ids and ids.index(target) >= n:
                    raise ValueError("forward/self aliases unsupported")
                chain = set()
                key = u["id"]
                while key in aliases:
                    if key in chain:
                        raise ValueError("alias cycle")
                    chain.add(key)
                    key = aliases[key]
            for edge in seq["edges"]:
                if (
                    edge["from"] not in ids
                    or edge["to"] not in ids
                    or edge["kind"] not in KINDS
                ):
                    raise ValueError("invalid edge endpoint/kind")
                a, b = ids.index(edge["from"]), ids.index(edge["to"])
                if b != a + 1:
                    raise ValueError("edges must cover adjacent ordered uses")
                if edge["kind"] != "cut":
                    ua, ub = uses[a], uses[b]
                    if ua.get('composition') and ub.get('composition') and ua['composition']!=ub['composition']:
                        raise ValueError('composition/view change requires an explicit cut')
                    if (
                        ua.get("visible_cast") is not None
                        and ub.get("visible_cast") is not None
                        and ua["visible_cast"] != ub["visible_cast"]
                    ):
                        raise ValueError(
                            "cast change requires an explicit cut in the supported sequence mode"
                        )
                if edge["kind"] == "hold" and edge.get("visible_action"):
                    raise ValueError("hold cannot claim new visible action")
            if len(seq["edges"]) != len(uses) - 1:
                raise ValueError("every ordered adjacency needs exactly one edge")
            if len({(e["from"], e["to"]) for e in seq["edges"]}) != len(seq["edges"]):
                raise ValueError("duplicate edge")
        except (KeyError, ValueError, TypeError) as exc:
            errors.append(f"{sid}: {exc}")
    return errors


def selection_catalog(folder):
    """Read declared owner selections; candidate registries cannot grant selection."""
    folder = Path(folder)
    files = []
    for name in ["scene_image_selection_s01_s05.json", "scene_image_selection.json"]:
        if (folder / name).exists():
            files.append(folder / name)
    # Later ledgers have explicit scene-depiction scopes. Performance-only
    # decisions are intentionally excluded even when they use the same PNG.
    files += sorted(
        (folder / "review").glob("**/owner_acceptance/OWNER_SELECTION.json")
    )
    records = []
    for p in files:
        obj = json.loads(p.read_text())
        if p.name.startswith("scene_image_selection"):
            if (
                obj.get("reviewer") != "project_owner"
                or obj.get("decision") != "owner_selected_scene_images"
            ):
                continue
        for row in obj.get("images", []):
            if row.get("scope") not in (None, "scene_depiction_only"):
                continue
            if not row.get("path") or not row.get("sha256"):
                continue
            if (
                p.name == "OWNER_SELECTION.json"
                and row.get("reviewer") != "project_owner"
            ):
                continue
            record = dict(row, selection_record={"path": str(p), "sha256": digest(p)})
            records.append(record)
            for iid in row.get("all_image_ids", []):
                if iid != row.get("image_id"):
                    records.append(dict(record, image_id=iid))
    # S08 stores exact scene approval inside its association rows, not an
    # acceptance directory. Validate the approval against each association.
    s08 = folder / "scene_composition_candidates_s08.json"
    if s08.is_file():
        for row in json.loads(s08.read_text()).get("images", []):
            approval = row.get("owner_approval") or {}
            if (
                row.get("status") == "owner_selected_scene_image"
                and approval.get("reviewer") == "project_owner"
                and approval.get("scope") == "scene_depiction_only"
                and row.get("path") == approval.get("path")
                and row.get("sha256") == approval.get("sha256")
                and row.get("image_id")
                in [approval.get("image_id")] + approval.get("all_image_ids", [])
            ):
                records.append(
                    dict(
                        row, selection_record={"path": str(s08), "sha256": digest(s08)}
                    )
                )
    reuse = folder / "selected_images/IMAGE_REUSE.json"
    if reuse.is_file():
        row = json.loads(reuse.read_text())
        if row.get("selection") == "owner_selected_shared_scene_use" and any(
            r.get("image_id") == row.get("reuse_of")
            and (r["path"], r["sha256"]) == (row["path"], row["sha256"])
            for r in records
        ):
            records.append(
                dict(
                    row, selection_record={"path": str(reuse), "sha256": digest(reuse)}
                )
            )
    current = {
        r.get("image_id")
        for r in records
        if Path(r["selection_record"]["path"]).name
        == "scene_image_selection_s01_s05.json"
    }
    records = [
        r
        for r in records
        if not (
            Path(r["selection_record"]["path"]).name == "scene_image_selection.json"
            and r.get("image_id") in current
        )
    ]
    return apply_current_bindings(folder, records)


def resolve_sequence(plan, sid, root, selections=None, size=(1280, 720)):
    errors = validate_sequences(plan)
    if errors:
        raise ValueError("; ".join(errors))
    requested_sid=sid
    while sequences(plan)[sid].get('alias_of_sequence'):
        sid=sequences(plan)[sid]['alias_of_sequence']
    seq = copy.deepcopy(sequences(plan)[sid])
    root = Path(root).resolve()
    if plan.get("schema") == "feltwillow.audio-line-visual.v1":
        from production.audio_visual_plan import load, validate

        _, _, characters, locations = load(root, plan["story"])
        errors = validate(plan, characters, locations, root)
    catalog = (
        selections
        if selections is not None
        else selection_catalog(root / "stories" / plan["story"])
    )
    images = {
        im["id"]: im
        for l in plan["lines"]
        for b in l["beats"]
        for im in b["image_sequence"]["images"]
    }
    legacy = {k: v["reuse_of"] for k, v in images.items() if v.get("reuse_of")}
    uses = {u["id"]: u for u in seq["uses"]}
    reuse_path = root / "stories" / plan["story"] / "selected_images/IMAGE_REUSE.json"
    if reuse_path.is_file():
        reuse = json.loads(reuse_path.read_text())
        for u in seq["uses"]:
            if u.get("image_id") == reuse.get("image_id") and u.get("alias_of"):
                target = uses.get(u["alias_of"], {}).get("image_id", u["alias_of"])
                if target != reuse.get("reuse_of"):
                    raise ValueError(
                        "authored alias contradicts selected reuse association"
                    )
    done = {}

    def one(uid, trail=()):
        if uid in done:
            return done[uid]
        if uid in trail:
            raise ValueError("alias cycle")
        u = uses.get(uid, {"id": uid, "image_id": uid})
        iid = u.get("image_id", uid)
        target = u.get("alias_of") or legacy.get(iid)
        row = dict(u, status="missing_distinct_state", blockers=[])
        if target:
            if target not in uses and target not in images:
                row.update(
                    status="ambiguous_authority", blockers=["missing alias target"]
                )
            else:
                parent = one(target, trail + (uid,))
                row.update(
                    source=parent.get("source"),
                    fit=parent.get("fit"),
                    native=parent.get("native"),
                    alias_target=target,
                    status="selected_alias"
                    if parent["status"].startswith("selected_")
                    else parent["status"],
                    blockers=parent["blockers"][:],
                )
                parent_iid = parent.get("image_id", parent["id"])
                if (
                    iid in images
                    and parent_iid in images
                    and (images[iid]["state"], images[iid]["location_view"])
                    != (
                        images[parent_iid]["state"],
                        images[parent_iid]["location_view"],
                    )
                ):
                    row.update(
                        status="incompatible_for_edge",
                        blockers=["alias changes state or camera"],
                    )
        else:
            source = u.get("source")
            candidates = [
                c
                for c in catalog
                if (
                    c.get("image_id") == iid
                    if source is None
                    else (c["path"], c["sha256"]) == (source["path"], source["sha256"])
                )
            ]
            distinct = {(c["path"], c["sha256"]) for c in candidates}
            if len(distinct) > 1:
                row.update(
                    status="ambiguous_authority",
                    blockers=["conflicting active selected bytes"],
                )
            elif not candidates:
                row["status"] = (
                    "candidate_pending_selection"
                    if u.get("candidate")
                    else "missing_distinct_state"
                )
                row["blockers"] = ["no applicable selected scene bytes"]
            else:
                c = candidates[0]
                record = {
                    "path": c["path"],
                    "sha256": c["sha256"],
                    "selection_record": c.get("selection_record"),
                }
                row["source"] = record
                try:
                    p = local(root, c["path"])
                    if not p.is_file():
                        row.update(
                            status="unavailable_bytes",
                            blockers=["selected file unavailable"],
                        )
                    elif digest(p) != c["sha256"]:
                        row.update(
                            status="ambiguous_authority",
                            blockers=["selected file hash changed"],
                        )
                    else:
                        with Image.open(p) as im:
                            im.load()
                            row["native"] = {"size": list(im.size), "mode": im.mode}
                            row["fit"] = wan.fitted_record(im, *size)
                        row["status"] = (
                            "selected_hold" if u.get("hold") else "selected_exact"
                        )
                except (OSError, ValueError) as exc:
                    row.update(status="incompatible_for_edge", blockers=[str(exc)])
        done[uid] = row
        return row

    resolved = [one(u["id"]) for u in seq["uses"]]
    for use in resolved:
        block=plan.get('production_blocks',{}).get((use.get('source') or {}).get('sha256'))
        if block and block.get('status') in {'needs_repair','blocked'}:
            use['selection_status']=use['status']
            use['status']='owner_selected_but_technically_blocked'
            use['blockers'].append(block['reason'])
    # Transitive input identity includes both graph and current source bytes.
    packet = {
        "schema": "feltwillow.sequence-realization.v1",
        "story": plan["story"],
        "sequence_id": sid,
        "source_plan_sha256": fingerprint(plan),
        "sequence": seq,
        "resolved_images": resolved,
        "edges": seq["edges"],
        "size": list(size),
        "selection_fingerprints": sorted(
            {fingerprint(c.get("selection_record", {})) for c in catalog}
        ),
        "global_schema_errors": errors,
    }
    scope_ids = {u.get("image_id") for u in seq["uses"]}
    scope_images = {k: v for k, v in images.items() if k in scope_ids}
    line_ids = {
        u.get("audio_line_id") or u.get("image_id", "").split("-B")[0]
        for u in seq["uses"]
    }
    packet["audio_lines"] = [
        dict(line_id=l["line_id"], speaker=l["speaker"], text=l["text"], **l["audio"])
        for l in plan["lines"]
        if l.get("line_id") in line_ids
    ]
    packet["scope_plan_sha256"] = fingerprint(
        {
            "sequence": seq,
            "images": scope_images,
            "states": {
                i["state"]: plan.get("world_states", {}).get(i["state"])
                for i in scope_images.values()
            },
        }
    )
    if plan.get('visual_units'):
        from production.visual_grammar import unit_for_sequence
        packet['visual_unit']=unit_for_sequence(plan,sid)
        if packet['visual_unit']:
            line_ids=set(packet['visual_unit']['audio_line_ids'])
            packet['audio_lines']=[dict(line_id=l['line_id'],speaker=l['speaker'],text=l['text'],**l['audio']) for l in plan['lines'] if l.get('line_id') in line_ids]
    if requested_sid!=sid:packet['requested_sequence_id']=requested_sid
    packet["dependency_sha256"] = dependency_fingerprint(packet)
    return packet


def resolved_visual_state(plan, image_id):
    for l in plan["lines"]:
        for b in l["beats"]:
            for im in b["image_sequence"]["images"]:
                if im["id"] == image_id:
                    state = copy.deepcopy(plan["world_states"][im["state"]])
                    binding = im.get("performance", {})
                    return {
                        "causal_state": state,
                        "depiction": binding,
                        "staging": b.get("staging_continuity", {}),
                        "policy": "world events own custody/support; performance owns depiction; stale pose strings are not prompts",
                        "source_state": im["state"],
                    }
    raise ValueError("unknown image")


def audio_intervals(plan, root, scenes=None):
    import wave

    result = {}
    for scene in plan["audio_scenes"]:
        if scenes and scene["id"] not in scenes:
            continue
        lines = [l for l in plan["lines"] if l["audio_scene"] == scene["id"]]
        cursor = 0
        previous = None
        intervals = []
        assembly = scene.get("assembly")
        master = None
        rate = 24000
        issues = []
        if assembly:
            p = local(root, assembly["path"])
            if p.exists():
                with wave.open(str(p)) as w:
                    rate = w.getframerate()
                    master = w.readframes(w.getnframes())
                    master_count = w.getnframes()
                    width = w.getsampwidth() * w.getnchannels()
            else:
                issues.append("master unavailable")
        for l in lines:
            if previous:
                gap = round(rate * (0.45 if previous == l["speaker"] else 0.70))
                if master is not None and any(
                    master[cursor * width : (cursor + gap) * width]
                ):
                    issues.append(l["line_id"] + " gap contains nonzero PCM")
                cursor += gap
            a = l["audio"]
            count = a.get("sample_count")
            status = "unavailable"
            p = local(root, a["wav"]) if a.get("wav") else None
            if p and p.exists():
                with wave.open(str(p)) as w:
                    raw = w.readframes(w.getnframes())
                    actual = w.getnframes()
                    line_rate = w.getframerate()
                if digest(p) != a["sha256"] or actual != count or line_rate != rate:
                    status = "failed"
                    issues.append(l["line_id"] + " line facts mismatch")
                elif master is not None:
                    status = (
                        "passed"
                        if master[cursor * width : (cursor + count) * width] == raw
                        else "failed"
                    )
                else:
                    status = "line_verified_master_unavailable"
            intervals.append(
                {
                    "line_id": l["line_id"],
                    "start_sample": cursor,
                    "end_sample": cursor + count,
                    "pcm_comparison": status,
                    "pause_owner": "outgoing settled shot",
                    "semantic_alignment": "pending",
                }
            )
            cursor += count
            previous = l["speaker"]
        expected = cursor + rate
        if master is not None:
            if digest(local(root, assembly["path"])) != assembly["sha256"]:
                issues.append("master hash mismatch")
            if any(master[cursor * width : expected * width]):
                issues.append("tail contains nonzero PCM")
        if master is not None and master_count != expected:
            issues.append("master duration mismatch")
        result[scene["id"]] = {
            "sample_rate": rate,
            "intervals": intervals,
            "master_samples_expected": expected,
            "master_duration": expected / rate,
            "tail_samples": rate,
            "issues": issues,
            "phrase_alignment": "pending; offsets do not locate spoken phrases",
        }
    return result


def frame_accounting(intervals, sample_rate, fps=16):
    """Quantize a single cumulative sample timeline using exact rationals.

    This plans frame cells, not model endpoint fidelity or permission to trim.
    Each shared boundary is quantized once, avoiding summed local rounding.
    """
    if any(
        isinstance(v, bool) or not isinstance(v, int) or v <= 0
        for v in (sample_rate, fps)
    ):
        raise ValueError("positive integer sample rate/fps required")
    cursor = 0
    rows = []
    for number, interval in enumerate(intervals):
        start, end = interval["start_sample"], interval["end_sample"]
        if (
            any(isinstance(v, bool) or not isinstance(v, int) for v in (start, end))
            or start != cursor
            or end <= start
        ):
            raise ValueError("noncontiguous or noninteger sample timeline")
        first, last = (
            round(Fraction(start * fps, sample_rate)),
            round(Fraction(end * fps, sample_rate)),
        )
        if last <= first:
            raise ValueError("editorial interval is shorter than a frame cell")
        error = Fraction(last, fps) - Fraction(end, sample_rate)
        rows.append(
            dict(
                id=interval.get("id", str(number)),
                start_frame=first,
                end_frame_exclusive=last,
                frame_cells=last - first,
                end_quantization_error_seconds=str(error),
            )
        )
        cursor = end
    if not rows:
        raise ValueError("empty editorial timeline")
    return dict(
        fps=fps,
        sample_rate=sample_rate,
        total_samples=cursor,
        total_frame_cells=rows[-1]["end_frame_exclusive"],
        encoded_duration_seconds=str(Fraction(rows[-1]["end_frame_exclusive"], fps)),
        intervals=rows,
        boundary_policy="keep all generated frames until actual native/motion review; no inferred shared-frame deletion",
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--story", required=True)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--sequence")
    p.add_argument("--audio", action="store_true")
    a = p.parse_args()
    plan = json.loads(
        (a.root / "stories" / a.story / "audio_visual_plan.json").read_text()
    )
    output = (
        audio_intervals(plan, a.root)
        if a.audio
        else resolve_sequence(plan, a.sequence, a.root)
        if a.sequence
        else {"errors": validate_sequences(plan), "sequences": list(sequences(plan))}
    )
    print(json.dumps(output, indent=2))


def applied_performance_evidence(use, record, root):
    """Validate realized acting/projection evidence without changing planned enums.

    A reviewer supplies this record for exact scene bytes; a pose approval alone
    cannot satisfy it. Unknown physical lens/distance stays unknown.
    """
    if record.get("scene_sha256") != use.get("source", {}).get("sha256"):
        raise ValueError("acting evidence identifies different scene bytes")
    if record.get("fit_sha256") != use.get("fit", {}).get("pixel_sha256"):
        raise ValueError("acting evidence identifies a different crop/fit")
    if (
        not record.get("reviewer")
        or record.get("scope") != "realized_scene_acting_projection"
    ):
        raise ValueError("scoped acting/projection reviewer required")
    projection = record.get("projection", {})
    if projection.get("kind") != "reviewed_2d" or not projection.get("landmarks"):
        raise ValueError(
            "reviewed native 2D landmarks required; do not invent camera calibration"
        )
    for actor, expression in record.get("applied_expressions", {}).items():
        if actor not in use.get("visible_cast", []):
            raise ValueError("expression evidence names an offscreen actor")
        source = expression["source"]
        if digest(local(root, source["path"])) != source["sha256"]:
            raise ValueError("expression reference bytes changed")
        if not expression.get("expression_id"):
            raise ValueError("expression identity required")
    return dict(
        record, validation="exact_sources_verified", planned_lifecycle_unchanged=True
    )


if __name__ == "__main__":
    main()
