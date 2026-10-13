#!/usr/bin/env python3
"""Audit image assets and gate scene generation/approval for a story.

    python production/image_handoff.py --story <manifest-backed-story> audit
    python production/image_handoff.py --story <manifest-backed-story> audit --strict
    python production/image_handoff.py --story <manifest-backed-story> check <record-id>
    python production/image_handoff.py --story <manifest-backed-story> check <record-id> --for-approval

A prompt lint checks instructions; this checks that the actual image files and size anchors
are approved and that a measured scene review was recorded. It cannot judge visual anatomy
or whether the named contact surface really appears under a character.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from .image_approval import spec_sha256
except ImportError:  # direct `python production/image_handoff.py` invocation
    from image_approval import spec_sha256

REPO = Path(__file__).resolve().parents[1]
SHARP = {"scene_wide", "close_two_shot"}


def scene_reference_cycles(images: dict) -> list[list[str]]:
    """Find scene-image reference loops that make generation order impossible."""
    scene = {rid: r for rid, r in images.items() if r.get("prompt_kind") == "scene"}
    edges = {rid: [ref["id"] for ref in r.get("ordered_references", []) if ref.get("id") in scene]
             for rid, r in scene.items()}
    active, done, path, cycles = set(), set(), [], []

    def visit(rid):
        active.add(rid)
        path.append(rid)
        for parent in edges[rid]:
            if parent in active:
                cycle = path[path.index(parent):] + [parent]
                if cycle not in cycles:
                    cycles.append(cycle)
            elif parent not in done:
                visit(parent)
        path.pop()
        active.remove(rid)
        done.add(rid)

    for rid in scene:
        if rid not in done:
            visit(rid)
    return cycles


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load(story: str):
    story_dir = REPO / "stories" / story
    manifest = json.loads((story_dir / "prompt_manifest.json").read_text())
    bible = json.loads((story_dir / "visual_bible.json").read_text())
    approval_path = story_dir / "image_approvals.json"
    approvals = json.loads(approval_path.read_text()).get("images", {}) if approval_path.exists() else {}
    return manifest, bible, approvals


def approval_errors(record: dict, approvals: dict) -> list[str]:
    rid = record["id"]
    entry = approvals.get(rid)
    if not entry:
        return [f"{rid}: no hash-bound approval"]
    errors = []
    path = REPO / record["target"]
    if not path.is_file():
        errors.append(f"{rid}: approved target missing: {record['target']}")
    elif entry.get("file") != record["target"] or entry.get("sha256") != digest(path):
        errors.append(f"{rid}: approved file path or SHA-256 differs from current target")
    if entry.get("spec_sha256") != spec_sha256(record):
        errors.append(f"{rid}: approved prompt/specification SHA-256 is stale")
    current_refs = record.get("ordered_references", [])
    approved_refs = entry.get("references", [])
    if [(r.get("id"), r.get("path")) for r in current_refs] != [
        (r.get("id"), r.get("path")) for r in approved_refs
    ]:
        errors.append(f"{rid}: approved reference list differs from current record")
    else:
        for ref, stamped in zip(current_refs, approved_refs):
            path = REPO / ref["path"]
            if not path.is_file() or stamped.get("sha256") != digest(path):
                errors.append(f"{rid}: reference {ref['id']} is missing or changed")
    return errors


def scene_errors(record: dict, images: dict, bible: dict, approvals: dict,
                 for_approval: bool = False) -> list[str]:
    rid = record["id"]
    if record.get("prompt_kind") != "scene":
        return [f"{rid}: this check is for scene image records"]
    setup = bible.get("setups", {}).get(record.get("setup"))
    if not setup:
        return [f"{rid}: unknown setup {record.get('setup')}"]
    errors = []
    refs = record.get("ordered_references", [])
    for ref in refs:
        parent = images.get(ref.get("id"))
        if parent:
            if parent.get("status") != "accepted":
                errors.append(f"{rid}: reference {parent['id']} is {parent.get('status')}; approve it first")
            else:
                errors.extend(approval_errors(parent, approvals))
        elif not (REPO / ref.get("path", "")).is_file():
            errors.append(f"{rid}: reference missing: {ref.get('path')}")
    if not any(r.get("role") == "locked_plate" for r in refs):
        errors.append(f"{rid}: no locked plate is attached")
    visible = [char for char in bible.get("characters", {}) if record.get("counts", {}).get(char)]
    if setup.get("framing") in SHARP and visible:
        if not setup.get("numeric_size_targets") or not setup.get("walkable_surface"):
            errors.append(f"{rid}: setup needs numeric size targets and a walkable surface")
        anchor_id = setup.get("anchor_record")
        if not anchor_id or anchor_id not in images:
            errors.append(f"{rid}: setup has no valid size anchor record")
        elif anchor_id != rid and rid not in setup.get("bootstrap_records", []):
            anchor = images[anchor_id]
            if anchor.get("status") != "accepted":
                errors.append(f"{rid}: size anchor {anchor_id} is {anchor.get('status')}; approve it first")
            else:
                errors.extend(approval_errors(anchor, approvals))
            if not any(r.get("id") == anchor_id and r.get("role") == "size_anchor" for r in refs):
                errors.append(f"{rid}: approved anchor {anchor_id} must be attached as size_anchor")
    if for_approval:
        target = REPO / record["target"]
        if not target.is_file():
            errors.append(f"{rid}: target image is missing")
        result = record.get("result") or {}
        candidate = result.get("candidate_path")
        if not candidate or not (REPO / candidate).is_file():
            errors.append(f"{rid}: reviewed candidate PNG is missing")
        elif target.is_file() and digest(REPO / candidate) != digest(target):
            errors.append(f"{rid}: target differs from reviewed candidate")
        checks = result.get("review_checks") or {}
        if checks.get("identity_match") is not True or checks.get("plate_match") is not True:
            errors.append(f"{rid}: record identity_match and plate_match=true after visual review")
        if setup.get("framing") in SHARP and visible:
            if checks.get("pair_match") is not True:
                errors.append(f"{rid}: record pair_match=true after start/end comparison")
            measured = checks.get("measured_size") or {}
            contact = checks.get("ground_contact") or {}
            for char, targets in setup.get("numeric_size_targets", {}).items():
                if not record.get("counts", {}).get(char):
                    continue
                for dimension, goal in targets.items():
                    actual = (measured.get(char) or {}).get(dimension)
                    tolerance = .02 if dimension in ("height", "mane", "face") else .015
                    if not isinstance(actual, (int, float)) or abs(actual - goal) > tolerance:
                        errors.append(f"{rid}: measured {char} {dimension} must be within {tolerance:.3f} of {goal:.3f}")
                point = contact.get(char) or {}
                if not point.get("surface") or not all(isinstance(point.get(k), (int, float)) and 0 <= point[k] <= 1 for k in ("x", "y")):
                    errors.append(f"{rid}: record {char} support surface and normalized contact x/y")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", required=True)
    sub = ap.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit", help="report image readiness; --strict exits nonzero on blockers")
    audit.add_argument("--strict", action="store_true",
                       help="return status 1 when approvals, anchors, or dependencies are blocked")
    check = sub.add_parser("check")
    check.add_argument("record")
    check.add_argument("--for-approval", action="store_true")
    args = ap.parse_args()
    manifest, bible, approvals = load(args.story)
    images = {r["id"]: r for r in manifest["images"]}
    if args.command == "audit":
        states = Counter((r.get("prompt_kind"), r.get("status")) for r in manifest["images"])
        for (kind, status), count in sorted(states.items()):
            print(f"{kind or 'unknown'} {status}: {count}")
        accepted = [r for r in manifest["images"] if r.get("status") == "accepted"]
        problems = [p for r in accepted for p in approval_errors(r, approvals)]
        print(f"accepted asset approval issues: {len(problems)}")
        for problem in problems[:30]: print("  ", problem)
        if len(problems) > 30: print(f"  ... {len(problems)-30} more")
        pending_scenes = [r for r in manifest["images"]
                          if r.get("prompt_kind") == "scene" and r.get("status") != "accepted"]
        print(f"scene images awaiting approval: {len(pending_scenes)}")
        sharp = [r for r in manifest["images"] if r.get("prompt_kind") == "scene" and
                 bible.get("setups", {}).get(r.get("setup"), {}).get("framing") in SHARP]
        missing = sorted({bible["setups"][r["setup"]]["anchor_record"] for r in sharp
                          if bible["setups"][r["setup"]].get("anchor_record") in images and
                          (images[bible["setups"][r["setup"]]["anchor_record"]].get("status") != "accepted" or
                           approval_errors(images[bible["setups"][r["setup"]]["anchor_record"]], approvals))})
        print(f"sharp scene records: {len(sharp)}; setup anchors awaiting approval: {len(missing)}")
        for rid in missing: print("  ", rid)
        cycles = scene_reference_cycles(images)
        print(f"scene reference cycles: {len(cycles)}")
        for cycle in cycles[:10]: print("  ", " -> ".join(cycle))
        if args.strict and (problems or pending_scenes or missing or cycles):
            raise SystemExit(1)
        return
    rec = images.get(args.record)
    if not rec:
        raise SystemExit(f"unknown record: {args.record}")
    problems = scene_errors(rec, images, bible, approvals, args.for_approval)
    if problems:
        for problem in problems: print("BLOCKED:", problem)
        raise SystemExit(1)
    print(f"READY: {args.record} ({'approval' if args.for_approval else 'generation'})")


if __name__ == "__main__":
    main()
