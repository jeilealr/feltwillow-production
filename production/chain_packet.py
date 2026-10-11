#!/usr/bin/env python3
"""Write a chained story's packet (CR-21) from its source file and an earlier version.

    python3 production/chain_packet.py stories/<new-inherited-story>/chain_source.py
    python3 production/image_prompts.py --story <new-inherited-story> build

The source names the BASE story whose bible and
accepted images are reused, the NEW_IMAGES the chain still needs (boundary frames, open-mouth
frames, entrances, empty views) and the PIECES in film order. This writes stories/<slug>/:
visual_bible.json (the base bible with `chained_coverage` on), prompt_manifest.json (the base
image records it carries over, the new image records, one shot per piece), dialogue_coverage.json
(the base line list, each line mapped to its pieces), SHOT_PLAN.md and README.md.

Carried image assets are localized under the new story's character folders; the base story stays
intact. Expression studies remain accepted references rather than new generation jobs, and are
listed in the new story's generated `prompts/expressions.md`. A piece with `reuse` copies the base
variant verbatim, so its renders can be reused (lint checks endpoints, prompt and frames). Other
pieces get new video prompts that describe only what is in frame (the v5 scene 15 lesson: in fast
mode a named absent object is drawn in).

It rebuilds the structural packet and generated docs for an explicitly inherited story. It must
not be run for an independent asset revision such as Lion and Mouse v6. Unchanged image records retain their
review/production state; a changed record with generated state requires explicit `--invalidate
<image-id>` and carries its old record forward under `superseded`. Once image review begins, edit
source templates and packet records carefully and inspect the complete diff before generation.
"""
import argparse
import copy
import importlib.util
import json
import re
import sys
from pathlib import Path

from image_approval import SPEC_FIELDS
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from feltwillow.version_policy import INDEPENDENT_STORIES  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("source", type=Path)
ap.add_argument("--invalidate", action="append", default=[], metavar="IMAGE_ID",
                help="explicitly supersede changed production state for this image record")
ARGS = ap.parse_args()
_spec = importlib.util.spec_from_file_location("chain_source", ARGS.source)
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)

REPO = Path(__file__).resolve().parents[1]
D = REPO / "stories" / S.SLUG
BASE = REPO / "stories" / S.BASE
KEYFRAMES = f"character/characters/{S.SLUG}/interactions/keyframes"

bb = json.loads((BASE / "visual_bible.json").read_text())
bm = json.loads((BASE / "prompt_manifest.json").read_text())
bc = json.loads((BASE / "dialogue_coverage.json").read_text())
base_images = {r["id"]: r for r in bm["images"]}
base_variants = {v["id"]: (s, v) for s in bm["shots"] for v in s["variants"]}
LINES = {ln["id"]: ln for ln in bc["lines"]}
CHARS = bb["characters"]
NUM = {1: "one", 2: "two", 3: "three"}


def resolve_base_files():
    """Record id -> the file the base story's renders actually used. The owner renamed some v5 files after
    the records were written; export_runtime.py --images resolves them through the image-set READMEs, and
    so does this. A target that exists only with a doubled extension (`.png.png`) is taken as it is."""
    sys.path.insert(0, str(REPO / "production"))
    from export_runtime import image_map
    try:
        found = {rid: str(f.resolve().relative_to(REPO.resolve())) for rid, f in image_map(S.BASE).items()}
    except FileNotFoundError:
        found = {}
    for r in bm["images"]:
        t = REPO / r["target"]
        if r["id"] not in found and not t.exists() and Path(str(t) + ".png").exists():
            found[r["id"]] = r["target"] + ".png"
    return found


def local_asset_path(value):
    """Give v5 image assets a v6-local path while leaving history and non-asset text alone."""
    if not isinstance(value, str):
        return value
    return (value.replace("character/characters/lion_and_mouse_v5/",
                          "character/characters/lion_and_mouse_v6/")
                 .replace("character/locations/lion_and_mouse_v5/",
                          "character/locations/lion_and_mouse_v6/"))


def remap_asset_paths(value):
    if isinstance(value, dict):
        return {k: remap_asset_paths(v) for k, v in value.items()}
    if isinstance(value, list):
        return [remap_asset_paths(v) for v in value]
    return local_asset_path(value)


def copy_localized_assets(paths):
    """Copy referenced v5 assets to their matching v6 paths without changing v5 or overwriting v6."""
    import hashlib
    import shutil
    for raw in sorted(set(paths)):
        source = Path(raw)
        if not source.is_absolute():
            source = REPO / source
        try:
            rel = source.resolve().relative_to(REPO.resolve())
        except ValueError:
            continue
        if not source.is_file() or "lion_and_mouse_v5" not in rel.parts:
            continue
        target = REPO / local_asset_path(rel.as_posix())
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            digest = lambda p: hashlib.sha256(p.read_bytes()).digest()
            if digest(source) != digest(target):
                raise SystemExit(f"refusing to overwrite different v6 asset: {target.relative_to(REPO)}")
            continue
        shutil.copy2(source, target)


def bible():
    b = remap_asset_paths(copy.deepcopy(bb))
    b.update(revision=S.REVISION, version=S.SLUG, status="single_source_of_truth_for_all_prompts",
             chained_coverage=True, keyframe_chrono_naming=True)
    b["how_to"] = (f"Chained story (CR-21), built by production/chain_packet.py from {S.BASE}. Every prompt in "
                   f"prompt_manifest.json is a template rendered from this file by production/image_prompts.py --story "
                   f"{S.SLUG}; piece timing comes from production/chain_plan.py.")
    for cid, description in S.PORTRAITS.items():
        b["characters"][cid]["portrait"] = description
    for cid, speaker in S.VOICE_SPEAKERS.items():
        b["characters"][cid]["voice_speaker"] = speaker
    b["blocks"].update(S.BLOCKS)
    b["reference_roles"].update(S.REFERENCE_ROLES)
    return b


def ref(rid, role, images):
    if rid in images:
        return {"id": rid, "role": role, "path": images[rid]["target"]}
    if rid in base_images:            # an inherited expression study: its image is localized by the packet builder
        r = base_images[rid]
        chars = [c for c, n in r.get("counts", {}).items() if c in CHARS and n]
        return {"id": rid, "role": role, "path": local_asset_path(r["target"]), "character": chars[0] if chars else None,
                "note": r.get("label")}
    raise SystemExit(f"unknown reference {rid}")


def cast_line(counts):
    vis = [c for c in CHARS if counts.get(c)]
    if not vis:
        return "No character is visible in this frame."
    parts = [f"exactly {NUM[counts[c]]} {CHARS[c]['name']}" for c in vis]
    return "Visible cast: " + " and ".join(parts) + "; no other character, no duplicates."


def new_image(spec, images, b):
    """A scene record built like the base story's scene records (CR-18 template order)."""
    setup = b["setups"][spec["setup"]]
    world = images.get(spec.get("world_from") or "") or base_images.get(spec.get("world_from") or "")
    counts = dict(spec.get("counts") or (world or {}).get("counts") or {})
    if spec.get("chars") is not None:   # the cast is the spec's; only prop counts come from the world frame
        counts = {k: v for k, v in counts.items() if k not in CHARS} | {c: 1 for c in spec["chars"]}
    vis = [c for c in CHARS if counts.get(c)]
    refs = [ref(rid, role, images) for rid, role in spec["refs"]]
    anchor = setup.get("anchor_record")
    if vis and not setup.get("background_treatment") and setup.get("framing") in ("scene_wide", "close_two_shot") \
            and anchor and anchor != spec["id"] and not any(r.get("id") == anchor and r.get("role") == "size_anchor" for r in refs):
        refs.append(ref(anchor, "size_anchor", images))
    parts = [f"Create one 1920x1080 16:9 still image: {spec['what']}, {setup['label']}.", "{{refs}}"]
    if refs and refs[0]["role"] == "edit_base":
        parts.append("{{block:edit_open_mouth}}" if spec.get("mouth") else "{{block:edit_chain_frame}}")
    parts.append(cast_line(counts))
    parts += [f"{{{{identity:{c}}}}}" for c in vis]
    if len(vis) > 1:
        parts.append("{{block:cast_scale}}")
    parts.append(f"{{{{setup:{spec['setup']}}}}}")
    if vis:
        parts.append("{{block:light_and_colour}}")
    if world:                         # the world-state blocks (acorn, net) of the frame it continues
        parts += re.findall(r"\{\{block:(?:acorn|net)_[a-z_]+\}\}", world["prompt_template"])
    if spec.get("state"):
        parts.append(spec["state"])
    if spec.get("mouth"):
        parts.append(f"{{{{mouth:{spec['mouth']}}}}}")
    parts += ["This frame shows: {{frame}}.", "{{block:style}}"]
    if vis:
        parts.append("{{block:final_check}}")
    return {"id": spec["id"], "group": None, "revision": "r01", "status": "planned", "bible_revision": S.REVISION,
            "target": None, "canvas": [1920, 1080], "purpose": spec["why"], "label": spec["what"],
            "prompt_kind": "scene", "counts": counts, "ordered_references": refs, "setup": spec["setup"],
            "framing": setup["framing"], "frame": spec["frame"], "prompt_template": " ".join(parts),
            "mouth_character": spec.get("mouth"),
            "allowed_delta": spec.get("delta", "Only what `frame` describes changes from the first reference."),
            "protected": "Identity, anatomical scale, plate landmarks, camera, crop and light; prop state unless stated.",
            "acceptance": [], "result": None}


def mouth_sentence(mode, start, end):
    if mode == "ambient":
        return "No character is in the scene; only the ambient motion moves."
    if mode != "mouth":
        return "No character speaks in this piece. Keep each visible mouth exactly in its approved start/end pose; do not animate speech or mouth movement."
    return ("Keep both boundary mouths closed in their approved poses; do not invent speech-mouth shapes. "
            "Animate only the specified head and eye motion. The approved open-mouth calibration image "
            "is used only for word-timed mouth motion composited after the video render. Close the mouth "
            "between words and throughout silent pauses.")


def endpoint_text(rid, images):
    rec = images[rid]
    return "{{frame:" + rid + "}}" if rec.get("frame") else "the empty approved view of this place"


def piece(p, order, prev, images, b):
    if any(images[rid].get("mouth_character") or images[rid].get("mouth")
           for rid in (p["start"], p["end"])):
        raise SystemExit(f"{p['id']}: open-mouth calibration images cannot be scene-chain boundaries")
    if p.get("mode") == "mouth" and not p.get("mouth_image"):
        raise SystemExit(f"{p['id']}: mouth mode needs a separate approved open-mouth calibration image")
    setup = b["setups"][p["setup"]]
    loc = b["locations"][setup["location"]]
    cast = [c for c in CHARS if any(images[i].get("counts", {}).get(c) for i in (p["start"], p["end"]))]
    shot = {"id": p["id"], "scene": p["scene"], "order": order, "status": "planned", "bible_revision": S.REVISION,
            "setup": p["setup"], "location_profile": setup["location"], "cast": cast,
            "start_image": p["start"], "end_image": p["end"], "lines": p["lines"],
            "join_in": p.get("join", "chain"), "previous_shot": prev, "owner_selection": None}
    for k in ("cut", "transition", "hold", "reuse"):
        if p.get(k) is not None:
            shot[{"cut": "cut_reason"}.get(k, k)] = p[k]
    if p.get("reuse"):
        _, v = base_variants[p["reuse"]]
        v = copy.deepcopy(v)
        speakers = sorted({LINES[i]["speaker"] for i in p["lines"]} - {"NARRATOR"})
        mouth_speaker = p.get("mouth_speaker") or (speakers[0] if len(speakers) == 1 else None)
        if v.get("mode") == "mouth" and (not mouth_speaker or mouth_speaker not in speakers):
            raise SystemExit(f"{p['id']}: a reused mouth variant needs one explicit character speaker; narrator audio never drives lips")
        v.update(id=f"{p['id']}_{v['mode']}_reuse", start_image=p["start"], end_image=p["end"],
                 mouth_open_image=p.get("mouth_image"),
                 speaker=mouth_speaker if v.get("mode") == "mouth" else None,
                 dialogue_line_ids=p["lines"], reused_from={"story": S.BASE, "variant": p["reuse"]})
        shot["reuse"] = {"story": S.BASE, "variant": p["reuse"]}
        shot["variants"] = [v]
        return shot
    mode = p.get("mode", "closed")
    close = setup["framing"] == "dialogue_close_up"
    descriptions = " ".join(f"{{{{{'portrait' if close else 'short'}:{c}}}}}" for c in cast)
    idents = " ".join(f"{{{{{'portrait' if close else 'identity'}:{c}}}}}" for c in cast)
    ambient = "The softly blurred background stays calm." if close else loc["ambient"]
    body = (" Head-and-shoulders portrait. Keep the exact approved crop and visible silhouette from the start and end frames for the whole clip. "
            "Nothing new enters from any frame edge; animate only the stated facial action.") if close else ""
    speech = mouth_sentence(mode, p["start"], p["end"])
    speakers = sorted({LINES[i]["speaker"] for i in p["lines"]} - {"NARRATOR"})
    mouth_speaker = p.get("mouth_speaker") or (speakers[0] if len(speakers) == 1 else None)
    if mode == "mouth" and (not mouth_speaker or mouth_speaker not in speakers):
        raise SystemExit(f"{p['id']}: mouth mode needs exactly one explicit character speaker in its covered lines; narrator audio never drives lips")
    pos = (f"{p['action']}{body} {speech} Fixed camera. {ambient} {descriptions} The view is {setup['label']}, "
           "unchanged framing and light. {{block:runtime_style}}")
    full = (f"{p['action']}{body} {speech} The camera stays fixed in framing, crop and background scale for the "
            f"whole clip. {idents} Start frame: {endpoint_text(p['start'], images)}. End frame: "
            f"{endpoint_text(p['end'], images)}. Ambient: {loc['ambient']} {{{{plate:{setup['location']}}}}} "
            "{{block:style}}")
    shot["variants"] = [{
        "id": f"{p['id']}_{mode}_r01", "mode": mode, "action_text": p["action"],
        "start_image": p["start"], "end_image": p["end"], "mouth_open_image": p.get("mouth_image"),
        "positive_prompt_template": re.sub(r"\s+", " ", pos).strip(),
        "full_prompt_specification_template": re.sub(r"\s+", " ", full).strip(),
        "negative_prompt": S.REVIEW_NEGATIVE, "frames": 81, "fps": 16, "size": [1280, 720],
        "seeds": [1, 2] if (p["start"] == p["end"]) else [1, 2, 3],
        "speaker": mouth_speaker if mode == "mouth" else None,
        "dialogue_line_ids": p["lines"], "result": None}]
    return shot


def main():
    if S.SLUG in INDEPENDENT_STORIES:
        raise SystemExit(
            f"{S.SLUG} is an independent production and cannot be built by chain_packet.py; "
            "use its native visual bible and manifest workflow."
        )
    existing_bible = D / "visual_bible.json"
    if existing_bible.is_file():
        current = json.loads(existing_bible.read_text())
        if current.get("asset_revision_policy") == "v6_native_assets":
            raise SystemExit(
                f"{S.SLUG} now uses its own approved character and plate assets. "
                "chain_packet.py still copies the older story's image records and would overwrite "
                "the current v6 visual bible. Edit the v6 bible/manifest directly; use "
                "image_prompts.py build, lint, and md after a prompt change."
            )
    b = bible()
    base_files = resolve_base_files()
    # Resolve records first, then copy all existing referenced v5 assets into the v6 tree.
    asset_sources = set(base_files.values())
    def collect_asset_paths(value):
        if isinstance(value, dict):
            for item in value.values(): collect_asset_paths(item)
        elif isinstance(value, list):
            for item in value: collect_asset_paths(item)
        elif isinstance(value, str) and value.startswith("character/") and "lion_and_mouse_v5/" in value:
            asset_sources.add(value)
    collect_asset_paths(bb)
    collect_asset_paths(bm)
    copy_localized_assets(asset_sources)
    for rid, f in base_files.items():
        if rid in base_images:
            base_images[rid]["target"] = local_asset_path(f)
    images = {r["id"]: remap_asset_paths(dict(copy.deepcopy(r), carried_from=S.BASE))
              for r in bm["images"] if r["group"] != "expressions"}
    # Keep accepted v5 studies as reference assets and create separate, manifest-backed
    # v6 prompts. Each edits the v6 closed portrait and uses the v6 canonical as authority;
    # old v3 expression art is not attached because those files are unreliable.
    for base_rec in bm["images"]:
        if base_rec.get("group") != "expressions":
            continue
        char = next((c for c, n in base_rec.get("counts", {}).items() if n), None)
        if char not in ("milo", "leo"):
            raise SystemExit(f"{base_rec['id']}: expression prompt needs exactly one known character")
        prefix = "M" if char == "milo" else "L"
        fresh = remap_asset_paths(copy.deepcopy(base_rec))
        old_target = local_asset_path(base_rec["target"])
        new_target = old_target.replace("_r01.png", "_r02.png")
        if new_target == old_target:
            raise SystemExit(f"{base_rec['id']}: expected r01 expression target")
        fresh.update(id=f"V6_{base_rec['id']}", revision="r02", status="planned",
                     bible_revision=S.REVISION, target=new_target,
                     ordered_references=[
                         {"id": f"{prefix}_CLOSED", "role": "edit_base"},
                         {"id": "MILO_CANON" if char == "milo" else "LEO_CANON", "role": "identity_root"},
                     ], result=None, carried_from=None)
        images[fresh["id"]] = fresh
    for rid, f in base_files.items():
        if rid in images and images[rid]["target"] != local_asset_path(f):
            images[rid]["base_target"] = images[rid]["target"]
            images[rid]["target"] = local_asset_path(f)
    order = list(images)
    for spec in S.NEW_IMAGES:
        if spec["id"] in images:
            raise SystemExit(f"duplicate image id {spec['id']}")
        images[spec["id"]] = new_image(spec, images, b)
        order.append(spec["id"])
    ids = [p["id"] for p in S.PIECES]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate piece ids")
    shots, prev = [], None
    for n, p in enumerate(S.PIECES, 1):
        for k in ("start", "end"):
            if p[k] not in images:
                raise SystemExit(f"{p['id']}: unknown {k} image {p[k]}")
        shots.append(piece(p, n, prev, images, b))
        prev = p["id"]
    # new images: group, chronological file name (first use in the scene) and the pieces they join
    seen, users, mouth_users = {}, {}, {}
    def mark_new_use(rid, scene_num):
        rec = images[rid]
        if rec.get("prompt_kind") != "scene" or rid in seen:
            return
        scene = f"s{scene_num:02d}"
        seen[rid] = (scene, sum(1 for value in seen.values() if value[0] == scene) + 1)
    for s in shots:
        for which, rid in (("start", s["start_image"]), ("end", s["end_image"])):
            users.setdefault(rid, []).append(f"{which} of {s['id']}")
            mark_new_use(rid, s["scene"])
        for variant in s.get("variants", []):
            rid = variant.get("mouth_open_image")
            if rid:
                mouth_users.setdefault(rid, []).append(s["id"])
                mark_new_use(rid, s["scene"])
    for spec in S.NEW_IMAGES:
        rec = images[spec["id"]]
        if spec["id"] not in seen:
            raise SystemExit(f"new image {spec['id']} is used by no piece")
        scene, k = seen[spec["id"]]
        name = spec["id"].split("_", 1)[1]
        rec["group"] = f"scene-{int(scene[1:]):02d}"
        rec["target"] = f"{KEYFRAMES}/{scene}_{k:02d}_{name}_r01.png"
        rec["acceptance"] = [
            "Identity: every checklist item of each visible character against its canonical (CR-13, CR-17).",
            "Size: the setup's measured sizes and the size anchor; same depth, same size (CR-16).",
            "Plate: landmarks, light and crop as in the locked plate (CR-06)."]
        if spec["id"] in mouth_users:
            rec["acceptance"].append("Mouth-animation anchor: only the named character's mouth differs from "
                                     "the closed source; match the approved mouth study. This is a calibration "
                                     "image, not a scene-chain boundary.")
        else:
            rec["acceptance"].append("Boundary image (CR-21): it must work as "
                                     + " and as ".join(sorted(set(users[spec["id"]])))
                                     + "; one simple action reaches it from the neighbouring images.")
        if spec.get("mouth") and spec["id"] not in mouth_users:
            rec["acceptance"].append("Open mouth (CR-19): only the mouth differs from the first reference; the "
                                     "opening matches the approved *_OPEN study.")
    # references point at current targets (new images got theirs above; carried ones may be resolved)
    for rec in images.values():
        for r in rec.get("ordered_references", []):
            if r.get("id") in images and images[r["id"]].get("target"):
                r["path"] = images[r["id"]]["target"]
    # Preserve review and generation state when the image specification is unchanged. If a
    # source edit changes an image that already has production state, require explicit invalidation.
    old_manifest_path = D / "prompt_manifest.json"
    old_records = {}
    if old_manifest_path.is_file():
        old_manifest = json.loads(old_manifest_path.read_text(encoding="utf-8"))
        old_records = {r["id"]: r for r in old_manifest.get("images", [])}
    structural = SPEC_FIELDS
    invalidated = set(ARGS.invalidate)
    for spec in S.NEW_IMAGES:
        rid = spec["id"]
        fresh, old = images[rid], old_records.get(rid)
        if old is None:
            if rid in invalidated:
                raise SystemExit(f"--invalidate {rid}: no existing record")
            continue
        same = all(old.get(k) == fresh.get(k) for k in structural)
        has_state = (old.get("status", "planned") != "planned" or old.get("result") is not None or
                     any(old.get(k) for k in ("approval", "approved", "review", "review_note", "generation",
                         "provenance", "sha256", "accepted_hash", "accepted_at", "output_hash", "tool",
                         "model", "actual_prompt", "actual_references", "attempts")))
        if has_state and not same and rid not in invalidated:
            raise SystemExit(f"{rid} has generated/review state but its specification changed; "
                             f"rerun with --invalidate {rid} only after preserving/reviewing the old result")
        if same:
            fresh.update(old)  # keep approval, result, hashes, notes and future metadata verbatim
        elif rid in invalidated:
            fresh["superseded"] = old
            fresh["status"], fresh["result"] = "planned", None
    unknown = invalidated - set(r["id"] for r in S.NEW_IMAGES)
    if unknown:
        raise SystemExit(f"--invalidate names unknown new image records: {sorted(unknown)}")
    expression_studies = []
    for r in bm["images"]:
        if r.get("group") != "expressions":
            continue
        expression_studies.append({
            "id": r["id"], "character": next((c for c, n in r.get("counts", {}).items() if n), None),
            "label": r.get("label", r["id"]), "target": local_asset_path(base_files.get(r["id"], r["target"])),
            "status": r.get("status", "accepted"), "carried_from": S.BASE
        })
    manifest = {"revision": S.REVISION, "status": "planned_awaiting_owner_review", "title": S.TITLE,
                "base_story": S.BASE, "audio_story": S.AUDIO_STORY,
                "schema_note": "Chained coverage (CR-21): one shot per piece, in film order, each with one variant.",
                "expression_studies": expression_studies,
                "images": [images[i] for i in order], "shots": shots}
    D.mkdir(parents=True, exist_ok=True)
    (REPO / KEYFRAMES).mkdir(parents=True, exist_ok=True)
    (REPO / KEYFRAMES / ".gitkeep").touch()
    (D / "visual_bible.json").write_text(json.dumps(b, indent=2, ensure_ascii=False) + "\n")
    (D / "prompt_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    cov = copy.deepcopy(bc)
    cov.update(revision=S.REVISION, note=f"Line list of {S.BASE} (narration rendered there); "
               "candidate_coverage_shots = the v6 pieces that cover each line.")
    for ln in cov["lines"]:
        ln["candidate_coverage_shots"] = [s["id"] for s in shots if ln["id"] in s["lines"]]
    (D / "dialogue_coverage.json").write_text(json.dumps(cov, indent=2, ensure_ascii=False) + "\n")
    write_docs(manifest, b, images, users)
    n_reuse = sum(1 for s in shots if s.get("reuse"))
    print(f"{len(shots)} pieces ({n_reuse} reuse {S.BASE} renders), {len(S.NEW_IMAGES)} new images, "
          f"{len(manifest['images'])} image records")


def write_docs(m, b, images, users):
    shots = m["shots"]
    new = [images[s["id"]] for s in S.NEW_IMAGES]
    holds = sum(1 for s in shots if s["start_image"] == s["end_image"])
    out = [f"# {S.TITLE}: chained shot plan", "",
           f"Generated by `production/chain_packet.py` from `chain_source.py`; do not edit by hand. {len(shots)} pieces "
           f"in film order (CR-21): each is one clip of 49 to 81 frames whose length comes from the narration lines it "
           f"covers (`production/chain_plan.py`, see `TIMING_SHEET.md` for times, frames and speeds). `chain` = starts "
           f"on the previous piece's end image; `cut (reason)` = a planned cut. {sum(1 for s in shots if s.get('reuse'))} "
           f"pieces reuse a {S.BASE} render; {holds} are holds or landscapes (start = end).", "",
           "| # | Piece | Setup | Join | Start → end | Lines | Action |", "|---|---|---|---|---|---|---|"]
    for s in shots:
        join = "chain" if s["join_in"] == "chain" else f"cut ({s['cut_reason']}" + (
            f", {s['transition']})" if s.get("transition") else ")")
        mark = lambda rid: f"**`{rid}`**" if rid in {r['id'] for r in new} else f"`{rid}`"
        act = s["variants"][0]["action_text"]
        if s.get("reuse"):
            act = f"(reuses `{s['reuse']['variant']}`) {act}"
        out.append(f"| {s['order']} | `{s['id']}` | `{s['setup']}` | {join} | {mark(s['start_image'])} → "
                   f"{mark(s['end_image'])} | {', '.join(x.split('-')[1] for x in s['lines'])} | {act} |")
    out += ["", "Bold = a new image (list below).", "", "## New images", "",
            f"{len(new)} images, all `planned`. Each prompt and its ordered references: `prompts/scene-NN.md` or "
            f"`python3 production/image_prompts.py --story {S.SLUG} show <id>`.", "",
            "| Image | File | Setup | Shows | Joins |", "|---|---|---|---|---|"]
    mouth_users = {}
    for shot in shots:
        for variant in shot.get("variants", []):
            if variant.get("mouth_open_image"):
                mouth_users.setdefault(variant["mouth_open_image"], []).append(shot["id"])
    for r in new:
        use_text = "; ".join(sorted(set(users.get(r["id"], []))))
        if not use_text and r["id"] in mouth_users:
            use_text = "mouth-animation anchor for " + ", ".join(sorted(set(mouth_users[r["id"]])))
        out.append(f"| `{r['id']}` | `{Path(r['target']).name}` | `{r['setup']}` | {r['frame']} | {use_text} |")
    (D / "SHOT_PLAN.md").write_text("\n".join(out) + "\n")
    readme = S.README.format(pieces=len(shots), new=len(new), reuse=sum(1 for s in shots if s.get("reuse")),
                             holds=holds, renders=len(shots) - sum(1 for s in shots if s.get("reuse")))
    (D / "README.md").write_text(readme)


if __name__ == "__main__":
    main()
