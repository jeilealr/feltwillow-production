#!/usr/bin/env python3
"""One source of truth for the story's image and video prompts.

Every prompt in stories/<story>/prompt_manifest.json is stored as a template. Shared text
(character identity, setup size and background, studio, light, style) lives once in
stories/<story>/visual_bible.json and is pulled in through placeholders, so a character is
described with the same canonical words in every prompt. `lint` proves that.

    python3 production/image_prompts.py lint              # exit 1 on any error
    python3 production/image_prompts.py build             # re-render after editing the bible or a template
    python3 production/image_prompts.py show s14_opening_start
    python3 production/image_prompts.py md                # rewrite stories/<story>/prompts/*.md

Placeholders (double braces):
    {{identity:milo}}   full canonical description of a character (bible characters.<id>.identity)
    {{short:milo}}      one-sentence description for video prompts (characters.<id>.short)
    {{mouth:milo}}      the character's approved open-mouth design (characters.<id>.mouth)
    {{setup:trap_wide}} camera, background and character sizes of a camera setup (bible setups.<id>)
    {{plate:trap_morning}} location description, landmarks and light (bible locations.<id>)
    {{block:style}}     any shared text block (bible blocks.<name>)
    {{refs}}            the record's ordered references, numbered as attached, each with its role
                        in plain words (bible reference_roles) and its file name
    {{frame}}           what this frame shows (the record's `frame` text); {{frame:<record id>}} is
                        another record's, so a video prompt states exactly its start and end images

Image records:   prompt_template -> positive_prompt
Video variants:  positive_prompt_template -> positive_prompt,
                 full_prompt_specification_template -> full_prompt_specification
The rendered fields are what an image or video tool receives; never edit them by hand.
Workflow and review rules: .claude/skills/consistent-image-prompts/SKILL.md.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLACEHOLDER = re.compile(r"\{\{(identity|short|portrait|mouth|setup|plate|block|refs|frame):?([A-Za-z0-9_]*)\}\}")
CHARACTER_KINDS = {"scene", "character", "expression"}  # kinds that must describe every visible character
# An older version's image may leak its identity, so it may only supply composition or an expression.
OLD_VERSION_ROLES = {"staging_only", "expression", "camera_geometry"}
# Blocks that tell the model to edit the first attached image: that image must be the edit base.
EDIT_BLOCKS = {"edit_end_frame", "edit_reference", "edit_expression", "edit_open_mouth", "edit_chain_frame"}

# Conflict detector: a sentence written outside the canonical blocks that names a colour together
# with a body feature is a second, competing character description.
COLOUR_WORDS = r"grey|gray|brown|taupe|cream|ivory|white|black|pink|rose|rosy|coral|salmon|peach|red|crimson|" \
               r"scarlet|orange|rust|ginger|amber|ochre|golden|gold|yellow|mustard|tan|beige|blue|green|purple|violet"
FEATURE_WORDS = r"body|fur|belly|chest|muzzle|nose|eyes?|iris(?:es)?|sclera|brows?|eyebrows?|ears?|mane|tail|" \
                r"paws?|whiskers?|cheeks?|crown|face|legs?|arms?|toes?|snout"
COLOUR_RE = re.compile(rf"\b({COLOUR_WORDS})(?:-\w+)?\b", re.I)
FEATURE_RE = re.compile(rf"\b({FEATURE_WORDS})\b", re.I)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
PUNCTUATION_SLIP = re.compile(r"[.;,:]\s*[.;,]")  # e.g. a block ending in "." followed by a template "."


def story_paths(story):
    d = REPO / "stories" / story
    return d, d / "prompt_manifest.json", d / "visual_bible.json"


def load(story):
    d, mp, bp = story_paths(story)
    return json.loads(mp.read_text()), json.loads(bp.read_text())


def save_manifest(story, manifest):
    _, mp, _ = story_paths(story)
    mp.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- rendering

def plate_text(bible, loc_id, landmarks=True):
    loc = bible["locations"][loc_id]
    parts = [loc["description"]]
    if landmarks and loc.get("landmarks"):
        parts.append("Fixed landmarks: " + "; ".join(loc["landmarks"]) + ".")
    if loc.get("light"):
        parts.append(loc["light"])
    return " ".join(parts)


def setup_text(bible, setup_id, chars=()):
    """Camera, background and the measured sizes of the characters in this frame only, so a frame
    without a character never reads that character's size. Close-ups name the place without its
    landmark list, because the background is blurred."""
    s = bible["setups"][setup_id]
    treat = s.get("background_treatment")
    background = plate_text(bible, s["location"], landmarks=not treat)
    if treat:
        background = f"{treat} {background}"
    sizes = [s.get("size", {}).get(c, "") for c in chars]
    if len(chars) > 1:
        sizes.append(s.get("relation", ""))
    return " ".join(p for p in [s["camera"], background, *sizes] if p)


def ref_character(bible, ref, target):
    """Name of the single character a reference shows (its record's counts), else a neutral word."""
    chars = [c for c, n in ((target or {}).get("counts") or {}).items() if c in bible["characters"] and n > 0]
    if ref.get("character") in bible["characters"]:
        chars = [ref["character"]]
    return bible["characters"][chars[0]]["name"] if len(chars) == 1 else "the character"


def refs_text(bible, rec, images):
    """Numbered list of the attached reference images, so the prompt states what each one is for."""
    items = []
    for k, ref in enumerate(rec.get("ordered_references", []), 1):
        target = images.get(ref.get("id"))
        path = target["target"] if target else ref.get("path", "")
        what = (target or {}).get("label") or ref.get("note") or ref.get("id", "")
        sentence = bible["reference_roles"][ref["role"]].format(who=ref_character(bible, ref, target),
                                                                 what=what.rstrip("."))
        items.append(f"({k}) {sentence} [{Path(path).name}].")
    return ("Attached reference images, in this order: " + " ".join(items)) if items else ""


def resolve(bible, kind, arg, rec=None, images=None):
    if kind == "identity":
        return bible["characters"][arg]["identity"]
    if kind == "short":
        return bible["characters"][arg]["short"]
    if kind == "portrait":
        return bible["characters"][arg]["portrait"]
    if kind == "mouth":
        return bible["characters"][arg]["mouth"]
    if kind == "frame":
        return ((images or {})[arg] if arg else rec)["frame"].rstrip(".")
    if kind == "setup":
        return setup_text(bible, arg, visible_characters(rec or {}, bible))
    if kind == "plate":
        return plate_text(bible, arg)
    if kind == "refs":
        return refs_text(bible, rec or {}, images or {})
    return bible["blocks"][arg]


def render(bible, template, rec=None, images=None):
    out = PLACEHOLDER.sub(lambda m: resolve(bible, m.group(1), m.group(2), rec, images), template)
    return re.sub(r"\s+", " ", out).strip()


def placeholders(template):
    return [(m.group(1), m.group(2)) for m in PLACEHOLDER.finditer(template)]


def literal_text(template):
    return PLACEHOLDER.sub(" ", template)


def build(manifest, bible):
    """Render every template into its prompt field; returns the number of changed fields."""
    changed = 0
    images = {r["id"]: r for r in manifest["images"]}
    for rec in manifest["images"]:
        if "prompt_template" in rec:
            new = render(bible, rec["prompt_template"], rec, images)
            changed += rec.get("positive_prompt") != new
            rec["positive_prompt"] = new
    for shot in manifest["shots"]:
        for v in shot["variants"]:
            for tkey, key in (("positive_prompt_template", "positive_prompt"),
                              ("full_prompt_specification_template", "full_prompt_specification")):
                if tkey in v:
                    new = render(bible, v[tkey], None, images)
                    changed += v.get(key) != new
                    v[key] = new
            rt = v.get("runtime_export_candidate")
            if rt:
                sheets = {c: bible["characters"][c]["sheet"] for c in shot.get("cast", [])}
                changed += rt.get("character_sheets") != sheets
                rt["character_sheets"] = sheets
    return changed


# ---------------------------------------------------------------- lint

def visible_characters(rec, bible):
    return sorted(c for c in rec.get("counts", {}) if c in bible["characters"] and rec["counts"][c] > 0)


def identity_conflicts(text, where, allow=()):
    """Sentences outside the canonical blocks that pair a colour with a body feature."""
    hits = []
    for sentence in SENTENCE_SPLIT.split(text):
        if any(a in sentence for a in allow):
            continue
        if COLOUR_RE.search(sentence) and FEATURE_RE.search(sentence):
            hits.append(f"{where}: identity words outside the canonical block: \"{sentence.strip()[:160]}\"")
    return hits


def drift_hits(bible, text):
    hits = []
    for cid, c in bible["characters"].items():
        for phrase in c.get("drift_phrases", []):
            if re.search(rf"\b{re.escape(phrase)}\b", text, re.I):
                hits.append(f"{cid}: '{phrase}'")
    for phrase in bible.get("lint", {}).get("forbidden_in_prompts", []):
        if re.search(rf"\b{re.escape(phrase)}\b", text, re.I):
            hits.append(f"'{phrase}'")
    return hits


# ---------------------------------------------------------------- chained coverage (CR-21)

CUT_REASONS = {"film_start", "close_up", "camera_change", "time_change", "location_change", "dissolve"}
CLOSE_FRAMINGS = {"dialogue_close_up", "close_two_shot"}
HOLD_MODES = {"ambient"}


def place_of(bible, loc_id):
    """The physical place of a location profile: its `location`, else its plate's folder, so the
    afternoon and sunset plates of the stream bank are one place in two lights."""
    loc = bible["locations"][loc_id]
    return loc.get("location") or Path(loc.get("plate", loc_id)).parent.name


def wan_frames_ok(n):
    return isinstance(n, int) and 49 <= n <= 81 and (n - 1) % 4 == 0


def lint_chain(manifest, bible, images):
    """CR-21: pieces in film order; each piece chains onto its predecessor's end image or is a cut
    whose stated reason is true; landscape pieces use the setup's empty plate; holds are explicit."""
    errs = []
    plate_rec = {r["target"]: r["id"] for r in manifest["images"] if r.get("prompt_kind") == "plate"}
    others = {}
    prev = None
    for s in sorted(manifest["shots"], key=lambda x: x.get("order", 0)):
        sid = s["id"]
        setup = bible["setups"].get(s.get("setup") or "")
        if setup is None:
            errs.append(f"{sid}: piece needs a `setup` from the bible (found {s.get('setup')!r})")
            prev = s
            continue
        if len(s["variants"]) != 1:
            errs.append(f"{sid}: a chained piece has exactly one video variant (found {len(s['variants'])})")
        if not s.get("lines"):
            errs.append(f"{sid}: piece lists no narration `lines` (chain_plan.py times pieces from them)")
        own_plate = plate_rec.get(bible["locations"][setup["location"]].get("plate"))
        for which in ("start_image", "end_image"):
            rid = s[which]
            rec = images.get(rid)
            if rec is None:
                errs.append(f"{sid}: {which} {rid} is not an image record")
            elif rec.get("prompt_kind") == "plate":
                if rid != own_plate:
                    errs.append(f"{sid}: {which} {rid} is not the plate of setup {s['setup']} ({own_plate})")
            elif rec.get("setup") != s["setup"]:
                errs.append(f"{sid}: {which} {rid} is in setup {rec.get('setup')}, the piece in {s['setup']}")
        for v in s["variants"]:
            if v.get("start_image", s["start_image"]) != s["start_image"] or \
                    v.get("end_image", s["end_image"]) != s["end_image"]:
                errs.append(f"{v['id']}: variant endpoints differ from the piece's; a chained piece has one pair")
            if not wan_frames_ok(v.get("frames")):
                errs.append(f"{v['id']}: frames {v.get('frames')} must be 4k+1 between 49 and 81 (run chain_plan.py apply)")
            if s["start_image"] == s["end_image"] and not (s.get("hold") or v.get("mode") in HOLD_MODES):
                errs.append(f"{sid}: start = end without `hold: true` or an ambient mode (CR-04: holds are planned)")
            if v.get("mode") == "ambient" and s.get("cast"):
                errs.append(f"{sid}: an ambient (landscape) piece has no cast")
            reuse = s.get("reuse")
            if reuse:
                try:
                    om, _ = load(reuse["story"])
                    ov = next(x for sh in om["shots"] for x in sh["variants"] if x["id"] == reuse["variant"])
                    osh = next(sh for sh in om["shots"] if ov in sh["variants"])
                except (OSError, StopIteration, KeyError):
                    errs.append(f"{sid}: reuse {reuse} names no variant")
                else:
                    ends = (ov.get("start_image", osh["start_image"]), ov.get("end_image", osh["end_image"]))
                    if ends != (s["start_image"], s["end_image"]):
                        errs.append(f"{sid}: reuse {reuse['variant']} has endpoints {ends}, the piece "
                                    f"{(s['start_image'], s['end_image'])}")
                    if ov.get("positive_prompt") != v.get("positive_prompt"):
                        errs.append(f"{sid}: reuse {reuse['variant']} but the runtime prompt differs; "
                                    "its renders do not show this piece")
                    if ov.get("frames") != v.get("frames"):
                        errs.append(f"{sid}: reuse {reuse['variant']} rendered {ov.get('frames')} frames, the piece "
                                    f"plans {v.get('frames')}")
        join, reason = s.get("join_in"), s.get("cut_reason")
        if prev is None:
            if (join, reason) != ("cut", "film_start"):
                errs.append(f"{sid}: the first piece is join_in 'cut' with cut_reason 'film_start'")
        elif join == "chain":
            if s["start_image"] != prev["end_image"]:
                errs.append(f"{sid}: chains on {prev['id']} but starts on {s['start_image']}, "
                            f"not its end image {prev['end_image']}")
        elif join == "cut":
            psetup = bible["setups"].get(prev.get("setup") or "")
            if reason not in CUT_REASONS - {"film_start"}:
                errs.append(f"{sid}: cut_reason {reason!r} must be one of {sorted(CUT_REASONS - {'film_start'})}")
            elif psetup is None:
                pass
            elif reason == "dissolve":
                if s.get("transition") not in ("crossfade", "dip"):
                    errs.append(f"{sid}: a dissolve needs transition crossfade or dip")
            elif prev["setup"] == s["setup"]:
                errs.append(f"{sid}: cut from {prev['id']} in the same setup {s['setup']} is a jump cut; "
                            "chain it, or make it a dissolve (time passes)")
            else:
                a, b = psetup["location"], setup["location"]
                truth = {"close_up": psetup["framing"] in CLOSE_FRAMINGS or setup["framing"] in CLOSE_FRAMINGS,
                         "camera_change": place_of(bible, a) == place_of(bible, b),
                         "time_change": a != b and place_of(bible, a) == place_of(bible, b),
                         "location_change": place_of(bible, a) != place_of(bible, b)}
                if not truth[reason]:
                    errs.append(f"{sid}: cut_reason {reason} does not hold between {prev['setup']} ({a}) "
                                f"and {s['setup']} ({b})")
            if s.get("transition", "cut") not in ("cut", "crossfade", "dip"):
                errs.append(f"{sid}: transition {s.get('transition')!r} must be cut, crossfade or dip")
        else:
            errs.append(f"{sid}: join_in must be 'chain' or 'cut' (found {join!r})")
        prev = s
    return errs


def chain_chrono_names(manifest, bible, images):
    """Chained stories: a new scene image (one in this story's own folders) is named
    sNN_KK_<name>_rNN.png, KK = the order in which the scene's pieces first use it. Images reused
    from an earlier version keep their names."""
    version = bible.get("version", "")
    own = f"/{version}/"
    own_folder = f"character/characters/{version}/interactions/keyframes/"
    errs, seen = [], {}
    for s in sorted(manifest["shots"], key=lambda x: x.get("order", 0)):
        scene = f"s{s['scene']:02d}"
        used = [s["start_image"], s["end_image"]]
        used.extend(v["mouth_open_image"] for v in s.get("variants", []) if v.get("mouth_open_image"))
        for rid in used:
            rec = images.get(rid)
            if not rec or rec.get("prompt_kind") != "scene" or rid in seen:
                continue
            k = sum(1 for v in seen.values() if v[0] == scene) + 1
            seen[rid] = (scene, k)
            if own in rec["target"] and not rec.get("carried_from") and \
                    not Path(rec["target"]).name.startswith(f"{scene}_{k:02d}_"):
                errs.append(f"{rid}: chained keyframe file '{Path(rec['target']).name}' must start with "
                            f"'{scene}_{k:02d}_' (its first use in the scene)")
    return errs


def lint(manifest, bible):
    errors, warnings = [], []
    E, W = errors.append, warnings.append
    images = {r["id"]: r for r in manifest["images"]}
    allow = bible.get("lint", {}).get("allow_phrases", [])
    # New stories carry an explicit staging contract. A scene image cannot be
    # prepared without its own grounded placement and depth-derived size.
    staging_path = bible.get("staging_contract")
    scene_records = [r for r in manifest["images"] if r.get("prompt_kind") == "scene"]
    if staging_path and scene_records:
        path = REPO / staging_path
        if not path.is_file():
            E(f"staging contract is missing: {staging_path}")
        else:
            try:
                from production.staging_contract import validate_contract
            except ModuleNotFoundError:
                from staging_contract import validate_contract
            try:
                contract = json.loads(path.read_text())
            except (OSError, json.JSONDecodeError) as exc:
                E(f"staging contract cannot be read: {exc}")
            else:
                for problem in validate_contract(contract, bible, REPO,
                                                 (r["id"] for r in scene_records), scene_records):
                    E("staging: " + problem)
    if bible.get("asset_revision_policy") == "v6_native_assets":
        from image_handoff import scene_reference_cycles
        for cycle in scene_reference_cycles(images):
            E("scene references form a generation cycle: " + " -> ".join(cycle))
        version = bible.get("version")
        if manifest.get("base_story") or manifest.get("audio_story") != version:
            E(f"{version}: independent packet must use its own audio story and no base story")
        for shot in manifest["shots"]:
            if shot.get("reuse") or any(v.get("reused_from") for v in shot.get("variants", [])):
                E(f"{shot['id']}: independent packet cannot reuse an older render")
        for rec in manifest["images"]:
            if rec.get("carried_from"):
                E(f"{rec['id']}: independent packet cannot carry an older image record")
            active_paths = [rec.get("target", "")] + [r.get("path", "") for r in rec.get("ordered_references", [])]
            for path in active_paths:
                match = re.search(r"lion_and_mouse_v\d+", path)
                if match and match.group() != version:
                    E(f"{rec['id']}: active asset path crosses into {match.group()}: {path}")

    # The bible itself must be coherent: the short description may not introduce colour words that
    # the full canonical description does not use, and no block may contain a drift phrase.
    for cid, c in bible["characters"].items():
        full_colours = {w.lower() for w in COLOUR_RE.findall(c["identity"])}
        for w in COLOUR_RE.findall(c["short"]) + COLOUR_RE.findall(c["sheet"]):
            if w.lower() not in full_colours:
                E(f"bible characters.{cid}: short/sheet colour '{w}' is not in the canonical identity")
        if not c["short"].startswith(c["name"] + " is " + c["sheet"]):
            E(f"bible characters.{cid}: short must read '<Name> is <sheet>...'")
    for name, text in [(f"blocks.{k}", v) for k, v in bible["blocks"].items()] + \
                      [(f"characters.{k}.identity", v["identity"]) for k, v in bible["characters"].items()]:
        for h in drift_hits(bible, text):
            E(f"bible {name}: drift phrase {h}")
    for sid, s in bible["setups"].items():
        if s["location"] not in bible["locations"]:
            E(f"bible setups.{sid}: unknown location {s['location']}")
        if s.get("anchor_record") and s["anchor_record"] not in images:
            E(f"bible setups.{sid}: anchor_record {s['anchor_record']} is not a manifest record")
        elif s.get("anchor_record") and images[s["anchor_record"]].get("setup") != sid:
            E(f"bible setups.{sid}: anchor_record {s['anchor_record']} belongs to another setup")
        size_text = " ".join(list(s.get("size", {}).values()) + [s.get("relation", "")])
        for h in identity_conflicts(s["camera"] + " " + size_text, f"bible setups.{sid}", allow):
            E(h)
        for c in s.get("size", {}):
            if c not in bible["characters"]:
                E(f"bible setups.{sid}: size for unknown character {c}")
        if bible.get("asset_revision_policy") == "v6_native_assets" and s.get("framing") in ("scene_wide", "close_two_shot"):
            if not s.get("numeric_size_targets") or not s.get("walkable_surface"):
                E(f"bible setups.{sid}: sharp scene setup needs numeric size targets and walkable surface")

    chained = bible.get("chained_coverage")
    shot_of = {}
    if chained:
        # an image is shared by consecutive pieces; the pair rules apply where it first appears
        for s in sorted(manifest["shots"], key=lambda x: x.get("order", 0)):
            for which in ("start", "end"):
                shot_of.setdefault(s[f"{which}_image"], (s, which))
        for e in lint_chain(manifest, bible, images):
            E(e)
    for s in [] if chained else manifest["shots"]:
        # a bridge shot reuses the end of one shot and the start of the next (same camera):
        # its endpoints are checked as images of their own shots, not as a new pair
        if s.get("bridge"):
            continue
        shot_of[s["start_image"]] = (s, "start")
        shot_of[s["end_image"]] = (s, "end")

    # Keyframe chronological-order file names (opt-in per story via bible.keyframe_chrono_naming).
    # Each scene keyframe FILE is sNN_CC_name_<which>_rNN.png, CC counting shots in story order
    # within the scene, so they sort chronologically on disk; the record id stays <shot>_<which>.
    # A chained story numbers its own new images by first appearance instead (chain_chrono_names).
    if bible.get("keyframe_chrono_naming") and chained:
        for e in chain_chrono_names(manifest, bible, images):
            E(e)
    elif bible.get("keyframe_chrono_naming"):
        pos = {}
        for s in sorted(manifest["shots"], key=lambda x: x.get("order", 0)):
            if s.get("bridge"):
                continue
            sid = s["id"]
            prefix, _, name = sid.partition("_")
            pos[prefix] = pos.get(prefix, 0) + 1
            stem = f"{prefix}_{pos[prefix]:02d}_{name}"
            checks = [(s.get("start_image"), "start"), (s.get("end_image"), "end")]
            if f"{sid}_open" in images:
                checks.append((f"{sid}_open", "open"))
            for key, which in checks:
                krec = images.get(key)
                if not krec:
                    continue
                base = Path(krec["target"]).name
                want = f"{stem}_{which}_"
                if not base.startswith(want):
                    E(f"{key}: keyframe file name '{base}' must start with '{want}' "
                      f"(keyframe_chrono_naming: per-scene order from the shot order)")

    for rec in manifest["images"]:
        rid = rec["id"]
        tpl = rec.get("prompt_template")
        if tpl is None:
            E(f"{rid}: no prompt_template")
            continue
        try:
            rendered = render(bible, tpl, rec, images)
        except KeyError as e:
            E(f"{rid}: placeholder refers to a missing bible entry {e}")
            continue
        if rendered != rec.get("positive_prompt"):
            E(f"{rid}: positive_prompt differs from its rendered template (run build; never edit it by hand)")
        ph = placeholders(tpl)
        kind = rec.get("prompt_kind")
        vis = visible_characters(rec, bible)
        ids = [a for k, a in ph if k == "identity"]
        if kind in CHARACTER_KINDS:
            for c in vis:
                if ids.count(c) != 1:
                    E(f"{rid}: visible character {c} needs exactly one {{{{identity:{c}}}}} (found {ids.count(c)})")
        for c in ids:
            if c not in vis:
                E(f"{rid}: {{{{identity:{c}}}}} but {c} is not in counts")
        own_text = " ".join([literal_text(tpl), rec.get("label", ""), rec.get("frame", "")])
        for h in identity_conflicts(own_text, rid, allow + rec.get("lint_allow", [])):
            E(h)
        if rec.get("ordered_references") and not rec.get("label"):
            W(f"{rid}: no label (used when other prompts name this image as a reference)")
        for h in drift_hits(bible, rendered):
            E(f"{rid}: drift phrase {h}")
        if PUNCTUATION_SLIP.search(rendered):
            E(f"{rid}: doubled punctuation in the rendered prompt: '{PUNCTUATION_SLIP.search(rendered).group(0)}'")

        frames = [a for k, a in ph if k == "frame"]
        if kind == "scene" and (frames != [""] or not rec.get("frame")):
            E(f"{rid}: a scene prompt needs a `frame` text and exactly one {{{{frame}}}}")
        if any(k == "block" and a in EDIT_BLOCKS for k, a in ph):
            first = (rec.get("ordered_references") or [{}])[0]
            if first.get("role") != "edit_base":
                E(f"{rid}: the prompt edits the first attached image, but its role is '{first.get('role')}', not edit_base")

        if kind == "scene":
            setups = [a for k, a in ph if k == "setup"]
            if len(setups) != 1:
                E(f"{rid}: scene prompt needs exactly one {{{{setup:...}}}} (found {len(setups)})")
                continue
            sid = setups[0]
            if sid not in bible["setups"]:
                continue
            s = bible["setups"][sid]
            if rec.get("setup") != sid:
                E(f"{rid}: record setup '{rec.get('setup')}' but template uses {sid}")
            if rec.get("framing") != s["framing"]:
                E(f"{rid}: framing '{rec.get('framing')}' but setup {sid} is '{s['framing']}'")
            if s["framing"] in ("scene_wide", "close_two_shot"):
                for c in vis:
                    if c not in s.get("size", {}):
                        E(f"{rid}: setup {sid} has no measured size for visible character {c}")
            # Sharp/recognizable-background cast frames need a concrete same-setup size guide.
            # Numeric prompt text alone is not evidence that the generator kept scale stable.
            if bible.get("scale_anchor_gate") and vis and not s.get("background_treatment") \
                    and s["framing"] in ("scene_wide", "close_two_shot") \
                    and rid not in s.get("bootstrap_records", []):
                anchor_id = s.get("anchor_record")
                if not anchor_id or anchor_id not in images:
                    E(f"{rid}: setup {sid} needs a valid anchor_record before sharp-background frames can be generated")
                elif anchor_id != rid:
                    anchor = images[anchor_id]
                    if anchor.get("setup") != sid:
                        E(f"{rid}: size anchor {anchor_id} belongs to setup {anchor.get('setup')}, not {sid}")
                    missing_anchor_chars = set(vis) - set(visible_characters(anchor, bible))
                    if missing_anchor_chars:
                        E(f"{rid}: size anchor {anchor_id} does not show visible character(s) {sorted(missing_anchor_chars)}")
                    attached_anchor = [r for r in rec.get("ordered_references", [])
                                       if r.get("role") == "size_anchor" and r.get("id") == anchor_id]
                    if not attached_anchor:
                        E(f"{rid}: sharp-background frame must attach setup size anchor {anchor_id} (role size_anchor)")
            plate = bible["locations"][s["location"]].get("plate")
            refs = [r["path"] for r in rec.get("ordered_references", [])]
            if plate and plate not in refs and not (rid.endswith(("_end", "_open")) and not chained):
                own_image = (f"/{bible.get('version', '')}/" in rec.get("target", "")
                             and not rec.get("carried_from"))
                if own_image or not chained:
                    (E if own_image and chained else W)(
                        f"{rid}: locked plate {plate} is not among the references")
            if rid in shot_of:
                shot, which = shot_of[rid]
                other = images.get(shot["end_image" if which == "start" else "start_image"])
                # an empty plate has no setup: lint_chain checks it is the piece's plate
                if other and other.get("setup") and other.get("setup") != rec.get("setup"):
                    E(f"{rid}: start and end of {shot['id']} use different setups "
                      f"({rec.get('setup')} / {other.get('setup')})")
                # chained stories: only a new image (in this story's own folders) must be an edit of
                # its first piece's start; an earlier version's accepted image keeps its provenance
                if which == "end" and shot["start_image"] != rid and \
                        (not chained or not rec.get("carried_from")):
                    first = (rec.get("ordered_references") or [{}])[0]
                    if first.get("id") != shot["start_image"]:
                        E(f"{rid}: first reference must be its start frame {shot['start_image']} (edit base)")

        refs = rec.get("ordered_references", [])
        n_refs = [k for k, _ in ph].count("refs")
        if refs and n_refs != 1:
            E(f"{rid}: {len(refs)} reference images but {n_refs} {{{{refs}}}} placeholders; the prompt must name them")
        canon_of = {c.get("canonical_record"): cid for cid, c in bible["characters"].items()}
        attached = {canon_of[r["id"]] for r in refs if r.get("id") in canon_of}
        for ref in refs:
            attached.update(c for c in ref.get("covers_characters", []) if c in bible["characters"])
        if kind in CHARACTER_KINDS:
            for c in vis:
                if c not in attached and bible["characters"][c].get("canonical_record") != rid:
                    E(f"{rid}: {c} is visible but its canonical {bible['characters'][c].get('canonical_record')} "
                      f"is not attached")
        for ref in refs:
            shown = visible_characters(images[ref["id"]], bible) if ref.get("id") in images else []
            if ref.get("role") not in ("staging_only", "empty_copy", "size_anchor") and set(shown) - set(vis):
                E(f"{rid}: reference {ref['id']} shows {sorted(set(shown) - set(vis))}, who is not in this frame")
        for c in sorted(attached - set(vis)):
            E(f"{rid}: canonical of {c} attached although {c} is not visible (it may be drawn into the frame)")
        for ref in refs:
            if ref.get("role") not in bible["reference_roles"]:
                E(f"{rid}: reference {ref.get('id')} has unknown role '{ref.get('role')}' (see bible reference_roles)")
            p = ref.get("path", "")
            if ref.get("id") in images:
                cur = images[ref["id"]]["target"]
                if p != cur:
                    E(f"{rid}: reference {ref['id']} points to {p}, current target is {cur}")
                p = cur
            # a record carried over from an earlier story keeps its provenance; that story's lint checks it
            if p and not (REPO / p).exists() and images.get(ref.get("id"), {}).get("status") != "planned" \
                    and not rec.get("carried_from"):
                (W if ref.get("id") in images else E)(f"{rid}: reference file missing: {p}")
            if re.search(r"/v[0-9]+/", p) and f"/{bible.get('version', 'v4')}/" not in p \
                    and ref.get("role") not in OLD_VERSION_ROLES:
                E(f"{rid}: older-version reference {p} may only be {sorted(OLD_VERSION_ROLES)}")
        for word in bible.get("lint", {}).get("warn_words", []):
            if re.search(rf"\b{word}\b", rendered, re.I):
                W(f"{rid}: rendered prompt contains '{word}'")

    for shot in manifest["shots"]:
        cast = shot.get("cast", [])
        for v in shot["variants"]:
            vid = v["id"]
            close_variant = (shot.get("setup") in bible.get("setups", {})
                             and bible["setups"][shot["setup"]].get("framing") == "dialogue_close_up")
            # The crop-safe portrait schema was introduced with chained coverage. Older
            # packets have no portrait blocks and keep their existing prompt contract.
            uses_portrait = bool(chained and close_variant and not shot.get("reuse"))
            for tkey, key, want in (("positive_prompt_template", "positive_prompt", "portrait" if uses_portrait else "short"),
                                    ("full_prompt_specification_template", "full_prompt_specification", "portrait" if uses_portrait else "identity")):
                tpl = v.get(tkey)
                if tpl is None:
                    E(f"{vid}: no {tkey}")
                    continue
                try:
                    rendered = render(bible, tpl, None, images)
                except KeyError as e:
                    E(f"{vid}: placeholder refers to a missing bible entry or record {e}")
                    continue
                if rendered != v.get(key):
                    E(f"{vid}: {key} differs from its rendered template (run build)")
                endpoints = (v.get("start_image", shot["start_image"]), v.get("end_image", shot["end_image"]))
                for k, a in placeholders(tpl):
                    if k == "frame" and a not in endpoints:
                        E(f"{vid}: {{{{frame:{a}}}}} is not this variant's start or end image")
                got = [a for k, a in placeholders(tpl) if k == want]
                for c in cast:
                    if got.count(c) != 1:
                        E(f"{vid}: {key} needs exactly one {{{{{want}:{c}}}}}")
                for h in identity_conflicts(literal_text(tpl), f"{vid}.{key}", allow):
                    E(h)
                for h in drift_hits(bible, v.get(key, "")):
                    E(f"{vid}.{key}: drift phrase {h}")
                if PUNCTUATION_SLIP.search(rendered):
                    E(f"{vid}.{key}: doubled punctuation: '{PUNCTUATION_SLIP.search(rendered).group(0)}'")
            if uses_portrait:
                for tkey, key in (("positive_prompt_template", "positive_prompt"),
                                  ("full_prompt_specification_template", "full_prompt_specification")):
                    tpl = v.get(tkey, "")
                    rendered = v.get(key, "")
                    if not re.search(r"\{\{portrait:[A-Za-z0-9_]+\}\}", tpl):
                        E(f"{vid}: dialogue close-up must use a crop-safe {{portrait:character}} description")
                    if re.search(r"\b(?:paws?|tails?|legs?|limbs?)\b", rendered, re.I):
                        E(f"{vid}.{key}: dialogue close-up prompt names anatomy outside the approved crop")
                    if not re.search(r"exact approved crop|visible silhouette", rendered, re.I):
                        E(f"{vid}.{key}: dialogue close-up needs an explicit crop and silhouette lock")
    return errors, warnings


# ---------------------------------------------------------------- markdown

def md_image(rec, images):
    lines = [f"## Image {rec['id']}", ""]
    tgt = rec["target"]
    exists = (REPO / tgt).exists()
    review = ((rec.get("result") or {}).get("review") or {})
    lines += [f"- Target: `{tgt}`{'' if exists else ' (missing)'}",
              f"- Status: `{rec.get('status')}` · revision `{rec.get('revision')}`"
              + (f" · review `{review.get('status')}`" if isinstance(review, dict) and review.get("status") else ""),
              f"- Kind: `{rec.get('prompt_kind')}`"
              + (f" · setup `{rec['setup']}` · framing `{rec.get('framing')}`" if rec.get("setup") else ""),
              f"- Canvas: {rec['canvas'][0]} × {rec['canvas'][1]}",
              "- Ordered references:"]
    for k, ref in enumerate(rec.get("ordered_references", []), 1):
        p = images[ref["id"]]["target"] if ref.get("id") in images else ref.get("path")
        lines.append(f"  {k}. `{p}` — {ref.get('role', '')}{'' if (REPO / p).exists() else ' (missing)'}")
    lines += ["", "**Prompt (rendered from the template)**", "", rec["positive_prompt"], ""]
    if rec.get("negative_prompt"):
        lines += ["**Review-only exclusions** (not sent: no negative pass)", "", rec["negative_prompt"], ""]
    if rec.get("acceptance"):
        lines += ["**Acceptance**", ""] + [f"- [ ] {a}" for a in rec["acceptance"]] + [""]
    return lines


def md_shot(shot):
    lines = [f"## Video {shot['id']}", "",
             f"- Start `{shot['start_image']}` → end `{shot['end_image']}` · cast: {', '.join(shot.get('cast', [])) or 'none'}", ""]
    for v in shot["variants"]:
        ends = f" · start `{v['start_image']}` → end `{v['end_image']}`" if v.get("start_image") else ""
        lines += [f"### {v['id']} ({v.get('mode')}){ends}", "", v["positive_prompt"], ""]
    return lines


def write_md(story, manifest):
    d, _, _ = story_paths(story)
    out_dir = d / "prompts"
    out_dir.mkdir(exist_ok=True)
    images = {r["id"]: r for r in manifest["images"]}
    groups = {}
    for rec in manifest["images"]:
        groups.setdefault(rec["group"], []).append(rec)
    shots_by_group = {}
    for s in manifest["shots"]:
        shots_by_group.setdefault(f"scene-{s['scene']:02d}", []).append(s)
    written = []
    for group, recs in groups.items():
        lines = [f"# {group}: prompt records", "",
                 "Generated by `python3 production/image_prompts.py md` from `../prompt_manifest.json` and "
                 "`../visual_bible.json`; do not edit by hand. Shared character, setup and style text comes "
                 "from the bible, so every prompt describes the characters identically.", ""]
        for rec in recs:
            lines += md_image(rec, images)
        for shot in shots_by_group.get(group, []):
            lines += md_shot(shot)
        (out_dir / f"{group}.md").write_text("\n".join(lines).rstrip() + "\n")
        written.append(group)
    studies = manifest.get("expression_studies", [])
    if studies and not groups.get("expressions"):
        lines = ["# expressions: accepted inherited studies", "",
                 f"Generated by `python3 production/image_prompts.py --story {story} md` from `../prompt_manifest.json`. "
                 "These approved v5 expression images are carried into this story as references; no new expression image is required.", "",
                 "| Study | Character | Asset | Status | Source |", "|---|---|---|---|---|"]
        for rec in studies:
            lines.append(f"| `{rec['id']}` | {rec.get('character') or '—'} | `{rec['target']}` | "
                         f"{rec.get('status', 'accepted')} | `{rec.get('carried_from', manifest.get('base_story', 'base story'))}` |")
        (out_dir / "expressions.md").write_text("\n".join(lines) + "\n")
        written.append("expressions")
    elif studies and groups.get("expressions"):
        # Prompt records are primary; append the carried approved references for context.
        path = out_dir / "expressions.md"
        lines = ["", "## Accepted inherited v5 studies (reference assets)", "",
                 "These remain available as visual references. New v6 outputs use the prompts above and separate `_r02` targets.", "",
                 "| Study | Character | Asset | Status | Source |", "|---|---|---|---|---|"]
        for rec in studies:
            lines.append(f"| `{rec['id']}` | {rec.get('character') or '—'} | `{rec['target']}` | "
                         f"{rec.get('status', 'accepted')} | `{rec.get('carried_from', manifest.get('base_story', 'base story'))}` |")
        path.write_text(path.read_text() + "\n".join(lines) + "\n")
    return written


# ---------------------------------------------------------------- review sheet

def review_sheet(story, manifest, bible, rid, candidate=None, out=None):
    """Side-by-side gate for one record: canonicals, setup anchor, plate and previous shot above,
    the candidate below, scene images with a 0.1 grid so sizes can be compared."""
    from PIL import Image, ImageDraw, ImageFont
    images = {r["id"]: r for r in manifest["images"]}
    rec = images[rid]
    font = ImageFont.load_default(size=18)
    top = []
    for c in visible_characters(rec, bible):
        canon = bible["characters"][c].get("canonical")
        if canon:
            top.append((REPO / canon, f"{c} canonical"))
    for ref in rec.get("ordered_references", []):
        if "expression" in ref.get("role", ""):
            top.append((REPO / ref["path"], ref["id"]))
    s = bible["setups"].get(rec.get("setup") or "", {})
    if s.get("anchor_record") in images and s["anchor_record"] != rid:
        top.append((REPO / images[s["anchor_record"]]["target"], f"size anchor {s['anchor_record']}"))
    plate = bible["locations"].get(s.get("location", ""), {}).get("plate")
    if plate:
        top.append((REPO / plate, "locked plate"))
    shots = {sh["id"]: sh for sh in manifest["shots"]}
    own = next((sh for sh in manifest["shots"] if rid in (sh["start_image"], sh["end_image"])), None)
    prev = shots.get(own.get("previous_shot")) if own else None
    if prev and prev["end_image"] in images:
        top.append((REPO / images[prev["end_image"]]["target"], f"previous shot end ({prev['id']})"))
    cand = Path(candidate) if candidate else REPO / rec["target"]
    bottom = [(cand, f"{rid} {'candidate' if candidate else 'current'}")]

    def tile(path, label, w, h, grid):
        im = Image.new("RGB", (w, h + 26), "white")
        if path.exists():
            src = Image.open(path).convert("RGB")
            src.thumbnail((w, h))
            if grid:
                d = ImageDraw.Draw(src)
                for k in range(1, 10):
                    d.line([(src.width * k / 10, 0), (src.width * k / 10, src.height)], fill=(255, 0, 255))
                    d.line([(0, src.height * k / 10), (src.width, src.height * k / 10)], fill=(0, 255, 255))
            im.paste(src, (0, 0))
        ImageDraw.Draw(im).text((4, h + 4), label if path.exists() else label + " (missing)", fill="black", font=font)
        return im

    tw, th = 420, 300
    row1 = [tile(p, lab, tw, th, "canonical" not in lab and "EXPR" not in lab) for p, lab in top]
    big = tile(bottom[0][0], bottom[0][1], tw * 2, th * 2, True)
    width = max(len(row1) * (tw + 6), big.width)
    sheet = Image.new("RGB", (width, th + 32 + big.height), "white")
    for k, t in enumerate(row1):
        sheet.paste(t, (k * (tw + 6), 0))
    sheet.paste(big, (0, th + 32))
    out = Path(out) if out else REPO / "work" / "review" / f"{rid}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88)
    return out


# ---------------------------------------------------------------- new story

def new_story(slug, template_story):
    """Create stories/<slug>/ with an empty manifest and a bible skeleton that keeps the shared
    blocks and lint settings of an existing story; characters, locations and setups start empty."""
    d, mp, bp = story_paths(slug)
    if any(path.exists() for path in (bp, mp, d / "staging_plan.json",
                                       d / "video_boundary_config.json",
                                       d / "keyframe_visual_reviews.json")):
        sys.exit(f"{d} already has story production files")
    _, _, tbp = story_paths(template_story)
    tb = json.loads(tbp.read_text())
    bible = {
        "revision": f"{slug}-draft",
        "scale_anchor_gate": True,
        "staging_contract": f"stories/{slug}/staging_plan.json",
        "how_to": "Fill in order: characters (from approved prop-free canonicals), cast_scale, locations "
                  "(one approved plate each), staging_plan (walkable positions + depth-derived sizes), "
                  "setups (camera + measured size anchor), then manifest records "
                  "with prompt templates. See .claude/skills/consistent-image-prompts/SKILL.md.",
        "characters": {"example_id": {
            "name": "Example", "canonical": "character/characters/<story>/Example/canonical/<file>.png",
            "identity": "Full canonical description written from the approved canonical image: silhouette, "
                        "head, ears, eyes, brows, nose, muzzle, mouth, whiskers, seams, torso, limbs, tail, "
                        "colours with hex codes, proportions, feature counts, surface, brightness.",
            "sheet": "one-line predicate for video prompts", "short": "Example is one-line predicate for video prompts.",
            "palette": {}, "proportions": {}, "checklist": [], "drift_phrases": []}},
        "cast_scale": {"lineup": "Same-depth standing heights and head widths of every character, as ratios."},
        "locations": {}, "setups": {},
        # only story-independent text; the size lineup and props are rewritten per story
        "blocks": {k: v for k, v in tb["blocks"].items() if k in tb.get("generic_blocks", [])},
        "generic_blocks": tb.get("generic_blocks", []),
        "reference_roles": tb.get("reference_roles", {}),
        "lint": tb.get("lint", {}),
    }
    d.mkdir(parents=True, exist_ok=True)
    bp.write_text(json.dumps(bible, indent=2, ensure_ascii=False) + "\n")
    mp.write_text(json.dumps({"revision": f"{slug}-draft", "images": [], "shots": []}, indent=2) + "\n")
    (d / "staging_plan.json").write_text(json.dumps({
        "schema_version": 1, "story": slug, "status": "draft",
        "visual_bible": f"stories/{slug}/visual_bible.json",
        "coordinate_system": "Normalized contact x/y on each approved full background plate before camera crop.",
        "cast_scale": bible["cast_scale"],
        "depth_model": {"far_scale": 0.55, "near_scale": 1.0,
                        "movement_rule": "Interpolate size continuously with depth on a fixed camera; record camera cuts separately."},
        "views": {"wide": {"magnification": 1.0}}, "locations": {}, "frames": []
    }, indent=2, ensure_ascii=False) + "\n")
    (d / "video_boundary_config.json").write_text(json.dumps({
        "schema": "feltwillow.video-boundary-config.v1", "story": slug,
        "scene_order_overrides": {}, "shared_entries": {}, "cut_reasons": {}
    }, indent=2, ensure_ascii=False) + "\n")
    (d / "keyframe_visual_reviews.json").write_text(json.dumps({
        "schema": "feltwillow.keyframe-visual-reviews.v1", "story": slug,
        "status": "pending_full_resolution_review", "images": {}
    }, indent=2, ensure_ascii=False) + "\n")
    return d


# ---------------------------------------------------------------- CLI

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", default="lion_and_mouse_v5")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("lint", help="check every prompt; exit 1 on errors")
    b = sub.add_parser("build", help="render templates into the prompt fields")
    b.add_argument("--check", action="store_true", help="only report whether a build would change anything")
    s = sub.add_parser("show", help="print one record's template and rendered prompt")
    s.add_argument("record")
    sub.add_parser("md", help="rewrite stories/<story>/prompts/*.md from the manifest")
    r = sub.add_parser("review", help="side-by-side review sheet for one record -> work/review/<id>.jpg")
    r.add_argument("record")
    r.add_argument("--image", help="candidate file to review instead of the record's current target")
    r.add_argument("--out")
    a = sub.add_parser("approve", help="record explicit approval for the exact current image file")
    a.add_argument("record")
    a.add_argument("--reviewed-by", required=True)
    a.add_argument("--note", default="")
    n = sub.add_parser("new-story", help="create stories/<slug>/ with an empty manifest and a bible skeleton")
    n.add_argument("slug")
    args = ap.parse_args()
    if args.cmd == "new-story":
        print("created", new_story(args.slug, args.story).relative_to(REPO))
        return
    manifest, bible = load(args.story)
    if args.cmd == "approve":
        from image_approval import reference_files, spec_sha256
        errors, _ = lint(manifest, bible)
        if errors:
            sys.exit("cannot approve an image while prompt lint has errors; run lint and fix them first")
        rec = next((r for r in manifest["images"] if r["id"] == args.record), None)
        if rec is None:
            sys.exit(f"no image record {args.record}")
        if rec.get("prompt_kind") == "scene":
            from image_handoff import scene_errors
            approvals_path = REPO / "stories" / args.story / "image_approvals.json"
            existing = json.loads(approvals_path.read_text()).get("images", {}) if approvals_path.exists() else {}
            problems = scene_errors(rec, {r["id"]: r for r in manifest["images"]}, bible,
                                    existing, for_approval=True)
            if problems:
                sys.exit("cannot approve scene image:\n" + "\n".join(problems))
        path = REPO / rec["target"]
        if not path.is_file():
            sys.exit(f"cannot approve missing target image: {path}")
        approvals_path = REPO / "stories" / args.story / "image_approvals.json"
        data = json.loads(approvals_path.read_text()) if approvals_path.exists() else {"images": {}}
        try:
            refs = reference_files(rec, REPO)
        except FileNotFoundError as error:
            sys.exit(f"cannot approve image with a missing prompt reference: {error}")
        data.setdefault("images", {})[args.record] = {
            "file": rec["target"], "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "spec_sha256": spec_sha256(rec), "references": refs, "reviewed_by": args.reviewed_by, "reviewed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "note": args.note}
        approvals_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print(f"approved {args.record}: {rec['target']} (sha256 bound) -> {approvals_path.relative_to(REPO)}")
        return

    if args.cmd == "lint":
        errors, warnings = lint(manifest, bible)
        for w in warnings:
            print("warning:", w)
        for e in errors:
            print("ERROR:", e)
        print(f"{len(errors)} errors, {len(warnings)} warnings")
        sys.exit(1 if errors else 0)
    if args.cmd == "build":
        n = build(manifest, bible)
        if args.check:
            print(f"{n} prompt fields would change")
            sys.exit(1 if n else 0)
        save_manifest(args.story, manifest)
        print(f"{n} prompt fields re-rendered")
    elif args.cmd == "show":
        rec = next((r for r in manifest["images"] if r["id"] == args.record), None)
        if rec is None:
            sys.exit(f"no image record {args.record}")
        images = {r["id"]: r for r in manifest["images"]}
        print("TEMPLATE:\n" + rec.get("prompt_template", "(none)") + "\n\nRENDERED:\n"
              + render(bible, rec["prompt_template"], rec, images))
    elif args.cmd == "md":
        print("wrote", ", ".join(f"prompts/{g}.md" for g in write_md(args.story, manifest)))
    elif args.cmd == "review":
        print(review_sheet(args.story, manifest, bible, args.record, args.image, args.out))


if __name__ == "__main__":
    main()
