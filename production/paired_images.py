"""Versioned paired-image contracts; CPU only, no provider or model imports.

Historical paired-schema utilities. Migrated v7 must use audio_visual_plan.py.

Legacy authored authorities: character_library, location_library, shot_plan. Candidates
are immutable directories; selection is one atomic pointer transaction. A
structural pass never grants visual or owner approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import tempfile

REPO = Path(__file__).resolve().parents[1]
SCHEMA = "paired_keyframes_v1"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def spec_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".transaction-")
    try:
        with os.fdopen(fd, "w") as out:
            json.dump(value, out, indent=2, ensure_ascii=False)
            out.write("\n")
            out.flush()
            os.fsync(out.fileno())
        os.replace(tmp, path)
    finally:
        if Path(tmp).exists():
            Path(tmp).unlink()


def local(root, path):
    result = (Path(root) / path).resolve()
    if not result.is_relative_to(Path(root).resolve()):
        raise ValueError(f"path escapes repository: {path}")
    return result


def verify(root, ref, *, approved=False):
    if approved and ref.get("status") != "owner_approved":
        raise ValueError(f"unapproved reference: {ref.get('path', ref.get('id'))}")
    path = local(root, ref["path"])
    if not path.is_file():
        raise ValueError(f"restore exact source {ref['path']} (SHA-256 {ref['sha256']})")
    if digest(path) != ref["sha256"]:
        raise ValueError(f"source hash changed: {ref['path']}")
    return path


def import_canonical(root, source, destination):
    """Validate before writing; never replace an existing identity import."""
    src = verify(root, source, approved=True)
    dst = local(root, destination)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if digest(dst) != source["sha256"]:
            raise ValueError(f"immutable canonical destination differs: {destination}")
    else:
        with dst.open("xb") as out:
            out.write(src.read_bytes())
    return {**source, "source_path": source["path"], "path": destination,
            "scope": "identity only; excludes new poses, scale anchors, scenes and video"}


def crop_for_setup(setup):
    crop = setup["crop_rect_norm"]
    if len(crop) != 4 or not all(math.isfinite(x) for x in crop):
        raise ValueError("invalid fixed setup crop")
    x, y, w, h = crop
    if min(x, y) < 0 or min(w, h) <= 0 or x + w > 1.00001 or y + h > 1.00001:
        raise ValueError("fixed setup crop leaves master plate")
    return list(crop)


def project(point, setup):
    x, y, w, h = crop_for_setup(setup)
    return [(point[0] - x) / w, (point[1] - y) / h]


def calibrated_transform(calibration, placement, setup, plate_size):
    """Scale entire source canvas from anatomy, never from its alpha box."""
    if calibration.get("status") != "owner_approved":
        raise ValueError("pose/view calibration needs review and owner approval")
    if calibration.get("kind") == "group":
        members = calibration.get("members", {})
        if len(members) < 2 or any(not m.get("internal_scale_reviewed") or
                not m.get('anatomical_measurements') for m in members.values()):
            raise ValueError("group box cannot certify internal actor scale")
    neutral = calibration["neutral_equivalent_source_px"]
    target = placement["neutral_equivalent_plate_px"]
    if not all(math.isfinite(v) and v > 0 for v in [neutral, target]):
        raise ValueError("anatomical calibration must be positive")
    px, py = placement["support_xy_on_plate"]
    if not (0 <= px <= 1 and 0 <= py <= 1):
        raise ValueError("support is outside physical master")
    if placement.get("support_surface") not in setup["support_zones"]:
        raise ValueError("unknown support surface")
    zone = setup["support_zones"][placement["support_surface"]]
    if not (zone[0] <= px <= zone[2] and zone[1] <= py <= zone[3]):
        raise ValueError("support leaves registered walkable zone")
    screen = project([px, py], setup)
    if not all(0 <= v <= 1 for v in screen) and not setup.get("allow_offscreen_support"):
        raise ValueError("offscreen support requires registered portrait permission")
    depth = placement.get("depth_projection_scale", 1.0)
    if depth != 1 and not placement.get("depth_calibration_id"):
        raise ValueError("depth movement needs a calibrated projection")
    if not math.isfinite(depth) or depth <= 0:
        raise ValueError("invalid depth projection")
    scale = target / neutral * depth
    sx, sy = calibration["source_support_px"]
    return {"source_scale_in_master": scale,
            "translation_px": [px * plate_size[0] - sx * scale, py * plate_size[1] - sy * scale],
            "crop_rect_norm": crop_for_setup(setup), "support_after_crop": screen}


def compose_master(plate, layers, setup):
    """Fresh clean plate each time; z-ordered premultiplied-alpha resampling.

    Shadows and props are explicit calibrated RGBA layers, including per-paw
    contacts. No invented contact ellipse for an airborne subject. All layers,
    masks and scenery receive exactly one common output/camera transform.
    """
    from PIL import Image
    master = plate.convert("RGBA").copy()
    for layer in layers:
        transform = calibrated_transform(layer["calibration"], layer["placement"], setup, master.size)
        scale = transform["source_scale_in_master"]
        tx, ty = transform["translation_px"]
        source = layer["image"].convert("RGBA")
        # RGBa is premultiplied; invisible source RGB cannot bleed into fibers.
        placed = source.convert("RGBa").transform(master.size, Image.Transform.AFFINE,
                    (1 / scale, 0, -tx / scale, 0, 1 / scale, -ty / scale),
                    Image.Resampling.BICUBIC).convert("RGBA")
        master = Image.alpha_composite(master, placed)
    x, y, w, h = crop_for_setup(setup)
    pw, ph = master.size
    box = (x * pw, y * ph, (x + w) * pw, (y + h) * ph)
    return master.convert("RGB").resize(tuple(setup["output_size"]), Image.Resampling.LANCZOS, box=box)


def protected_difference(start, end, allowed_mask):
    import numpy as np
    a, b = np.asarray(start.convert("RGB")), np.asarray(end.convert("RGB"))
    mask = np.asarray(allowed_mask.convert("L"))
    if a.shape != b.shape or mask.shape != a.shape[:2]:
        raise ValueError("pair/mask canvas mismatch")
    changed = np.any(a != b, axis=2)
    protected = changed & (mask == 0)
    return {"protected_changed_pixels": int(protected.sum()),
            "changed_pixels": int(changed.sum()), "pass": not bool(protected.any())}


def changed_paths(before, after, prefix=""):
    if isinstance(before, dict) and isinstance(after, dict):
        result = set()
        for key in before.keys() | after.keys():
            result |= changed_paths(before.get(key), after.get(key), f"{prefix}.{key}".strip("."))
        return result
    return set() if before == after else {prefix}


def validate(plan, characters, locations):
    """Return actionable structural errors. Pending geometry blocks image gate."""
    errors = []
    if plan.get("schema") != SCHEMA:
        return ["unsupported paired schema"]
    states, endpoints = plan["states"], plan["endpoints"]
    previous = None
    coverage = {}
    for p in plan["pieces"]:
        try:
            setup = locations["setups"][p["setup_id"]]
            crop_for_setup(setup)
            if p['lighting'] != setup['lighting'] or p['physical_location_id'] != setup['physical_location_id']:
                raise ValueError('piece light/location differs from registered setup')
            a, b = states[p["start_state"]], states[p["end_state"]]
            for e, s in [(p["start_image"], p["start_state"]), (p["end_image"], p["end_state"])]:
                if endpoints[e]["state_id"] != s or endpoints[e]["setup_id"] != p["setup_id"]:
                    raise ValueError("endpoint state/setup mismatch")
            changes = changed_paths(a, b)
            if changes - set(p["allowed_changes"]):
                raise ValueError(f"undeclared world changes: {sorted(changes - set(p['allowed_changes']))}")
            if p["visible_cast"] != sorted(set(p["visible_cast"])):
                raise ValueError("visible cast must be unique and sorted")
            if set(p["visible_cast"]) - set(a["actors"]):
                raise ValueError("visible cast absent from persistent world")
            if set(p["offscreen_cast"]) != set(a["actors"]) - set(p["visible_cast"]):
                raise ValueError("offscreen world cast was lost")
            for name in p["visible_cast"]:
                if name not in characters["characters"]:
                    raise ValueError("unknown canonical actor")
            event = p.get("event")
            for rule in plan.get("state_event_rules", []):
                def field(value, path):
                    for key in path.split("."):
                        value = value[key]
                    return value
                av, bv = field(a, rule["path"]), field(b, rule["path"])
                if av != bv:
                    transitions = rule["transitions"]
                    if not any(t["before"] == av and t["after"] == bv and t["event"] == event for t in transitions):
                        raise ValueError(f"{rule['path']}: changed without causal event")
                    for requirement in rule.get("requires", {}).get(event, []):
                        if field(a, requirement["path"]) != requirement["value"]:
                            raise ValueError(f"{rule['path']}: event prerequisite not satisfied")
            if previous:
                handoff = p["handoff"]["type"]
                prior = states[previous["end_state"]]
                if a["props"] != prior["props"]:
                    raise ValueError("cut reset persistent offscreen props")
                if handoff == "shared_boundary":
                    if (previous["end_image"], previous["end_state"], previous["setup_id"]) != (p["start_image"], p["start_state"], p["setup_id"]):
                        raise ValueError("shared boundary must reuse exact endpoint/state/setup")
                elif handoff == "camera_cut":
                    if previous["end_state"] != p["start_state"]:
                        raise ValueError("camera cut reset world state")
                elif handoff not in {"location_cut", "time_cut"}:
                    raise ValueError("unsupported handoff; camera moves need separate implementation")
                if not p["handoff"]["reason"]:
                    raise ValueError("handoff reason missing")
            for interval in p["audio_intervals"]:
                if interval["end"] <= interval["start"]:
                    raise ValueError("empty/reversed audio interval")
                coverage.setdefault(interval["line_id"], []).append((interval["start"], interval["end"]))
            if p.get("speaker") and (p["speaker"] == "NARRATOR" or p["speaker"] not in
                    {characters["characters"][c]["voice_speaker"] for c in p["visible_cast"]}):
                raise ValueError("mouth speaker must be an explicitly visible character")
        except (KeyError, ValueError, TypeError) as exc:
            errors.append(f"{p.get('id')}: {exc}")
        previous = p
    for line_id, span in plan["audio_spans"].items():
        cursor = span["start"]
        for start, end in sorted(coverage.get(line_id, [])):
            if abs(start - cursor) > 0.0001:
                errors.append(f"{line_id}: interval gap or overlap at {cursor}")
            cursor = end
        if abs(cursor - span["end"]) > 0.0001:
            errors.append(f"{line_id}: incomplete playback coverage")
    for unknown in coverage.keys() - plan["audio_spans"].keys():
        errors.append(f"unknown audio line {unknown}")
    return errors


def load_story(root, story):
    if (Path(root) / 'stories' / story / 'audio_visual_plan.json').is_file():
        raise ValueError('Historical paired tool refuses audio-line schema; use production/audio_visual_plan.py')
    folder = local(root, f"stories/{story}")
    plan, chars, locs = [read(folder / name) for name in
                         ("shot_plan.json", "character_library.json", "location_library.json")]
    errors = validate(plan, chars, locs)
    if errors:
        raise ValueError("\n".join(errors))
    return folder, plan, chars, locs


def packet(plan, chars, locs, piece_id, role, selection=None):
    """Generate role-limited prompts; planned refs stay explicit pending gates."""
    p = next(p for p in plan["pieces"] if p["id"] == piece_id)
    setup = locs["setups"][p["setup_id"]]
    state_id = p[f"{role}_state"]
    refs = []
    if role == "end":
        selected = (selection or {}).get("endpoints", {}).get(p["start_image"])
        refs.append({"role": "edit_base", "endpoint_id": p["start_image"],
                     "path": selected["path"] if selected else None,
                     "sha256": selected["sha256"] if selected else None})
    refs.append({"role": "locked_plate", **setup["plate"]})
    identity = []
    for name in p["visible_cast"]:
        actor = chars["characters"][name]
        refs.append({"role": "identity_root", **actor["canonical"]})
        identity.append(actor["portrait_identity"] if setup["framing"] == "portrait" else actor["identity"])
    framing = ("Head, ears or complete mane, shoulders and upper chest; support remains below the crop."
               if setup["framing"] == "portrait" else "Preserve registered visible silhouettes and intentional occlusions.")
    prompt = (f"Needle-felt story still, {role} endpoint of {piece_id}. Visible cast: "
              f"{', '.join(p['visible_cast']) or 'environment only'}. " + " ".join(identity) + " " + framing +
              f" Fixed setup {p['setup_id']}; crop {setup['crop_rect_norm']}; light {setup['lighting']}. "
              f"Action: {p['action']}. State: {json.dumps(plan['states'][state_id], sort_keys=True)}. "
              "Boundary mouths stay closed. Preserve intrinsic pigment and anatomy. "
              "Use reviewed anatomical calibration and master-space support anchors. "
              "Keep the registered clean plate and persistent props exact outside approved action/shadow masks.")
    # Full world record is provenance, not provider text: absent names must not summon cast.
    prompt = prompt[:prompt.index(" State:")] + " State: " + json.dumps({
        "actors": {c: plan["states"][state_id]["actors"][c] for c in p["visible_cast"]},
        "props": {k: v for k, v in plan["states"][state_id]["props"].items()
                  if k in setup.get('visible_prop_ids', [])}}, sort_keys=True) + ". Boundary mouths" + prompt.split("Boundary mouths", 1)[1]
    if len(p['visible_cast']) > 1:
        prompt += ' Same-depth neutral anatomical scale contract: ' + json.dumps(chars['scale_contract'], sort_keys=True) + '. This is not a ratio of arbitrary pose bounding boxes.'
    for absent in set(chars['characters']) - set(p['visible_cast']):
        prompt = prompt.replace(absent, "offscreen_eyeline")
    return {"piece_id": piece_id, "role": role, "endpoint_id": p[f"{role}_image"],
            "state_id": state_id, "setup_id": p["setup_id"], "ordered_references": refs,
            "prompt": prompt, "status": "planned_packet_requires_source_and_foundation_gate",
            "allowed_changes": p["allowed_changes"], "settings": {"canvas": setup["output_size"]}}


def check_references(root, refs, chars, setup, visible_cast):
    """A hash alone does not make an unreviewed atlas a performance authority."""
    for ref in refs:
        verify(root, ref)
        if ref["role"] in {"pose", "expression", "performance", "size_anchor"}:
            verify(root, ref, approved=True)
            authorities = chars.get('performance_references', []) + setup.get('approved_reference_bundle', [])
            if not any(a.get('path') == ref['path'] and a.get('sha256') == ref['sha256'] and a.get('status') == 'owner_approved' for a in authorities):
                raise ValueError('performance/anchor reference is absent from reviewed authority registry')
    identity = [r for r in refs if r["role"] == "identity_root"]
    required = {(chars["characters"][c]["canonical"]["path"], chars["characters"][c]["canonical"]["sha256"]) for c in visible_cast}
    if {(r["path"], r["sha256"]) for r in identity} != required:
        raise ValueError("actual canonical attachments must match visible cast exactly")
    plates = [r for r in refs if r["role"] == "locked_plate"]
    if len(plates) != 1 or any(plates[0].get(k) != setup["plate"][k] for k in ["path", "sha256"]):
        raise ValueError("missing or incompatible locked plate")


def endpoint_spec(plan, chars, locs, endpoint_id):
    e = plan["endpoints"][endpoint_id]
    return spec_hash({"endpoint": e, "state": plan["states"][e["state_id"]],
                      "setup": locs["setups"][e["setup_id"]], "characters": chars})


def register(root, story, endpoint_id, revision, image, provenance):
    """Publish image+receipt with one directory rename, selection untouched."""
    folder, plan, chars, locs = load_story(root, story)
    if not re.fullmatch(r"r[0-9]{3,}", revision):
        raise ValueError("revision must be r001 or later")
    spec = endpoint_spec(plan, chars, locs, endpoint_id)
    for actor in chars["characters"].values():
        verify(root, actor["canonical"], approved=True)
    if not provenance.get("prompt") or not provenance.get("tool"):
        raise ValueError("exact prompt and image tool are required")
    selected = read(folder / "selection.json") if (folder / "selection.json").exists() else {"endpoints": {}}
    role = provenance["role"]
    p = next(p for p in plan["pieces"] if p["id"] == provenance["piece_id"])
    if role not in {"start", "end"}:
        raise ValueError("registration role must be start or end")
    if p[f"{role}_image"] != endpoint_id:
        raise ValueError("endpoint role does not match piece")
    setup = locs["setups"][p["setup_id"]]
    check_references(root, provenance["ordered_references"], chars, setup, p["visible_cast"])
    if role == "end":
        start = selected["endpoints"].get(p["start_image"])
        if not start or start["sha256"] != provenance.get("start_sha256"):
            raise ValueError("stale or unselected prior start")
        verify(root, start)
        if not provenance["ordered_references"] or provenance["ordered_references"][0].get("role") != "edit_base" or provenance["ordered_references"][0].get("sha256") != start["sha256"]:
            raise ValueError("end edit must attach the exact selected start first")
    from PIL import Image
    with Image.open(image) as im:
        if im.size != tuple(locs["setups"][p["setup_id"]]["output_size"]):
            raise ValueError("candidate does not match delivery canvas")
        im.verify()
    receipt = {"endpoint_id": endpoint_id, "revision": revision, "spec_sha256": spec,
               "image_sha256": digest(image), "provenance": provenance, "status": "unreviewed_candidate"}
    parent = folder / "candidates" / endpoint_id
    parent.mkdir(parents=True, exist_ok=True)
    destination = parent / revision
    if destination.exists():
        if read(destination / "receipt.json") == receipt and digest(destination / "image.png") == receipt["image_sha256"]:
            return receipt
        raise ValueError("immutable revision already exists; use a new revision")
    staging = Path(tempfile.mkdtemp(dir=parent, prefix=".pending-"))
    try:
        shutil.copyfile(image, staging / "image.png")
        atomic_json(staging / "receipt.json", receipt)
        # mkdir lock serializes concurrent registration of the same revision.
        lock = parent / f".{revision}.lock"
        lock.mkdir()
        try:
            if destination.exists():
                raise ValueError("revision appeared concurrently; retry idempotently")
            staging.rename(destination)
        finally:
            lock.rmdir()
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return receipt


def select(root, story, endpoint_id, revision, expected_selection_hash):
    """Selection is distinct from approval. Lock plus CAS prevents lost writes."""
    root = Path(root).resolve()
    folder, plan, chars, locs = load_story(root, story)
    if endpoint_id not in plan['endpoints']:
        raise ValueError('unknown endpoint')
    if not re.fullmatch(r"r[0-9]{3,}", revision):
        raise ValueError("invalid immutable revision")
    candidate = folder / "candidates" / endpoint_id / revision
    receipt = read(candidate / "receipt.json")
    if receipt["spec_sha256"] != endpoint_spec(plan, chars, locs, endpoint_id):
        raise ValueError("candidate authority is stale")
    if digest(candidate / "image.png") != receipt["image_sha256"]:
        raise ValueError("candidate bytes changed")
    for ref in receipt["provenance"]["ordered_references"]:
        verify(root, ref)
    prov = receipt["provenance"]
    if prov["role"] == "end":
        p = next(p for p in plan["pieces"] if p["id"] == prov["piece_id"])
        start = read(folder / "selection.json")["endpoints"].get(p["start_image"])
        if not start or start["sha256"] != prov["start_sha256"]:
            raise ValueError("end candidate has stale edit base")
    lock = folder / ".selection.lock"
    lock.mkdir()
    try:
        path = folder / "selection.json"
        if digest(path) != expected_selection_hash:
            raise ValueError("selection changed; reread before adopting")
        selection = read(path)
        if prov['role'] == 'end':
            start = selection['endpoints'].get(p['start_image'])
            if not start or start['sha256'] != prov['start_sha256']:
                raise ValueError('start selection changed before atomic adoption')
        old = selection["endpoints"].get(endpoint_id)
        if old and old["sha256"] == receipt["image_sha256"]:
            return selection
        selection["endpoints"][endpoint_id] = {"path": str((candidate / "image.png").relative_to(root)),
            "sha256": receipt["image_sha256"], "revision": revision,
            "spec_sha256": receipt["spec_sha256"], "status": "selected_candidate"}
        for review in selection["reviews"].values():
            if endpoint_id in review.get("endpoint_ids", []):
                review["status"] = "stale"
        # Dependent end candidates retain bytes, but lose readiness when their edit base changes.
        for p in plan["pieces"]:
            if p["start_image"] == endpoint_id and p["end_image"] != endpoint_id:
                dependent = selection["endpoints"].get(p["end_image"])
                if dependent:
                    dependent["status"] = "stale_edit_base"
        atomic_json(path, selection)
        return selection
    finally:
        lock.rmdir()


def readiness(root, story, gate="image"):
    folder, plan, chars, locs = load_story(root, story)
    blockers = []
    for c in chars["characters"].values():
        try:
            verify(root, c["canonical"], approved=True)
        except ValueError as exc:
            blockers.append(str(exc))
    for setup_id, setup in locs["setups"].items():
        try:
            verify(root, setup["plate"])
        except ValueError as exc:
            blockers.append(str(exc))
        if gate != "source" and (setup.get("status") != "owner_approved" or not setup.get("support_zones") or not setup.get("foundation_review")):
            blockers.append(f"{setup_id}: foundation calibration/support/axis approval pending")
    if gate != "source":
        for p in plan["pieces"]:
            for c in p["visible_cast"]:
                calibration_id = p.get("pose_calibrations", {}).get(c)
                calibration = chars["pose_calibrations"].get(calibration_id, {})
                if calibration.get("status") != "owner_approved":
                    blockers.append(f"{p['id']}/{c}: approved pose/view calibration missing")
    if gate == "video":
        audio = read(folder / "audio_manifest.json")
        for entry in audio["lines"] + audio["scenes"]:
            try:
                verify(root, {"path": entry["runtime_path"], "sha256": entry["sha256"]})
            except ValueError as exc:
                blockers.append(str(exc))
        if plan["timing_status"] != "reviewed_audio_verified":
            blockers.append("piece timing is provisional; restore audio and review exact action/word boundaries")
        selection = read(folder / "selection.json")
        try:
            from .verify_audio_manifest import verify as verify_audio
        except ImportError:
            from verify_audio_manifest import verify as verify_audio
        blockers.extend(b for b in verify_audio(audio, story, root=Path(root)) if not b.startswith('missing WAV:'))
        for endpoint in plan["endpoints"]:
            chosen = selection["endpoints"].get(endpoint, {})
            try:
                if chosen.get("status") != "owner_approved" or chosen.get("spec_sha256") != endpoint_spec(plan, chars, locs, endpoint):
                    raise ValueError("hash-bound visual and owner approval pending/stale")
                verify(root, chosen)
                review = selection["reviews"].get(chosen.get("review_id"), {})
                if review.get("status") != "owner_approved" or review.get("image_hashes", {}).get(endpoint) != chosen["sha256"] or not review.get("reviewer"):
                    raise ValueError("owner review absent or stale")
                for evidence in review["evidence"]:
                    verify(root, evidence)
            except (ValueError, KeyError) as exc:
                blockers.append(f"{endpoint}: {exc}")
        for piece in plan['pieces']:
            review = selection['reviews'].get(piece['id'], {})
            expected = {e: selection['endpoints'].get(e, {}).get('sha256') for e in [piece['start_image'], piece['end_image']]}
            if review.get('status') != 'owner_approved' or review.get('image_hashes') != expected or not review.get('pair_visual_review') or not review.get('protected_pixels_pass'):
                blockers.append(f"{piece['id']}: current pair/sequence visual and protected-pixel evidence pending")
            if piece.get('speaker') and not review.get('dialogue_calibration_review'):
                blockers.append(f"{piece['id']}: dialogue mouth calibration review pending")
    return blockers


def wan_inputs(start, end, setup, *, width, height, preprocess=None):
    """CPU-testable handoff contract; pins/settings stay in feltwillow.wan."""
    from feltwillow.wan import fit, model_id
    if start.size != end.size or start.size != tuple(setup["output_size"]):
        raise ValueError("Wan pair has incompatible delivery canvases")
    if preprocess is None:
        preprocess = fit
    return {"image": preprocess(start, width, height),
            "last_image": preprocess(end, width, height), "model": model_id("i2v"),
            "planned_start_end": True, "actual_generated_first_last": None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story", required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    ready = sub.add_parser("readiness")
    ready.add_argument("--gate", choices=["source", "image", "video"], default="image")
    sub.add_parser("derive")
    pack = sub.add_parser("packet")
    pack.add_argument("piece")
    pack.add_argument("--role", choices=["start", "end"], default="start")
    reg = sub.add_parser("register")
    reg.add_argument("endpoint"); reg.add_argument("revision"); reg.add_argument("image"); reg.add_argument("provenance")
    adopt = sub.add_parser("select")
    adopt.add_argument("endpoint"); adopt.add_argument("revision"); adopt.add_argument("--expected-selection-hash", required=True)
    args = parser.parse_args()
    try:
        folder, plan, chars, locs = load_story(REPO, args.story)
        if args.command == "validate":
            print(json.dumps({"structural_errors": [], "pieces": len(plan["pieces"]), "unique_endpoints": len(plan["endpoints"])}))
        elif args.command == "readiness":
            blockers = readiness(REPO, args.story, args.gate)
            print(json.dumps({"gate": args.gate, "blockers": blockers}, indent=2))
            return bool(blockers)
        elif args.command == "packet":
            print(json.dumps(packet(plan, chars, locs, args.piece, args.role, read(folder / "selection.json")), indent=2))
        elif args.command == "derive":
            selection = read(folder / 'selection.json')
            packets = [packet(plan, chars, locs, p["id"], role, selection) for p in plan["pieces"] for role in ["start", "end"]]
            atomic_json(folder / "derived" / "generation_manifest.json", {"derived_from": "shot_plan.json + character_library.json + location_library.json", "authority_sha256": spec_hash([plan, chars, locs]), "packets": packets})
            atomic_json(folder / 'derived' / 'image_inventory.json', {'derived_from': 'shot_plan.json',
                'endpoints': {e: {**record, 'spec_sha256': endpoint_spec(plan, chars, locs, e),
                    'selection': selection['endpoints'].get(e)} for e, record in plan['endpoints'].items()}})
            atomic_json(folder / "derived" / "resume_queue.json", {"pieces": [{"id": p["id"],
                "foundation_status": locs['setups'][p['setup_id']]['status'],
                "start_selection": selection['endpoints'].get(p['start_image']),
                "end_selection": selection['endpoints'].get(p['end_image']),
                "pair_review": selection['reviews'].get(p['id']), "pilot": p.get("pilot", False)} for p in plan["pieces"]]})
            rows = ['# V7 paired shot inventory (derived)', '',
                    'Timing is provisional copied playback coverage; action windows are not reviewed word boundaries. Images and approvals are not implied.', '',
                    '| Piece | Original unit | Action | Handoff | Start → end | Playback intervals |',
                    '|---|---|---|---|---|---|']
            for p in plan['pieces']:
                intervals = '; '.join(f"{a['line_id']} {a['start']:.3f}–{a['end']:.3f}s" for a in p['audio_intervals'])
                rows.append(f"| {p['id']} | {', '.join(p['narrative_units'])} | {p['action']} | {p['handoff']['type']} | {p['start_image']} → {p['end_image']} | {intervals} |")
            (folder / 'derived' / 'SHOT_INVENTORY.md').write_text('\n'.join(rows) + '\n')
        elif args.command == "register":
            print(json.dumps(register(REPO, args.story, args.endpoint, args.revision, args.image, read(args.provenance))))
        elif args.command == "select":
            select(REPO, args.story, args.endpoint, args.revision, args.expected_selection_hash)
    except (ValueError, KeyError, OSError, StopIteration) as exc:
        parser.exit(1, f"PAIRED_IMAGE_BLOCKED: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
