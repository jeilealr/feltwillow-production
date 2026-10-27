"""Pose-first, review-only V7 S05 nose-landing composition (CPU, no providers).

This module uses registered transparent performance pixels and recorded shot staging.
It does not approve poses, solve occlusion/contact, modify source art or produce video.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

APPROVED_POSE_STATES = {"owner_selected_for_performance", "approved_for_scene_use"}
STORY = "lion_and_mouse_v7"
ROLL_ASSET = "milo.tumble.flank_to_face.3q"
S05_BACKGROUND = (
    "character/characters/lion_and_mouse_v7/interactions/scene_compositions/"
    "S05-L001-B01-I01_single_sleeping_leo_reveal_r001_candidate.png"
)
S05_PREVIOUS = (
    "character/characters/lion_and_mouse_v7/interactions/scene_compositions/"
    "S05-L009-B01-I03_local_roll_r002_candidate.png"
)
REJECTED_CANDIDATE = (
    "character/characters/lion_and_mouse_v7/interactions/scene_compositions/"
    "S05-L009-B01-I04_grounded_nose_landing_r002_candidate.png"
)
# Relative to the recorded roll placement, NOT independent guessed world positions.
S05_OFFSETS = (("left", -50, -15), ("aligned", 0, 0), ("right", 50, 15))
HASH_RE = re.compile(r"^[a-f0-9]{64}$")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_path(root: Path, raw: str) -> Path:
    if not isinstance(raw, str) or not raw or Path(raw).is_absolute():
        raise ValueError(f"Expected repository-relative path: {raw!r}")
    path = (root / raw).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes repository: {raw}")
    return path


def check_sha(path: Path, expected: str) -> None:
    if not isinstance(expected, str) or not HASH_RE.fullmatch(expected):
        raise ValueError(f"Missing or invalid SHA256 for {path}")
    if not path.is_file() or digest(path) != expected:
        raise ValueError(f"Hash mismatch or missing source: {path}")


def checked_image(root: Path, record: dict, *, alpha: bool = False) -> Path:
    path = repo_path(root, record["path"])
    check_sha(path, record.get("sha256"))
    with Image.open(path) as im:
        if alpha and im.mode != "RGBA":
            raise ValueError(f"Pose must have RGBA alpha: {path}")
        # Pillow requires verify() before any pixel access.
        im.verify()
    if alpha:
        with Image.open(path) as im:
            lo, hi = im.getchannel("A").getextrema()
            if lo == hi or hi == 0:
                raise ValueError(f"Pose lacks usable transparent silhouette: {path}")
    return path


def resolve_pose(root: Path, story: str, actor: str, asset_id: str,
                 variant: str, *, allow_provisional: bool = False) -> dict:
    """Resolve the authoritative registered performance and exact source bytes."""
    lib_path = repo_path(root, f"stories/{story}/character_performance_library.json")
    library = json.loads(lib_path.read_text())
    asset = library["assets"][asset_id]
    if asset.get("actor") != actor:
        raise ValueError(f"Wrong actor for {asset_id}: {actor}")
    pose = asset["variants"][variant]
    file = pose.get("file")
    if not isinstance(file, dict) or not file.get("path"):
        raise ValueError(f"No registered pose file: {asset_id}/{variant}")
    state = pose.get("status")
    if state not in APPROVED_POSE_STATES and not allow_provisional:
        raise PermissionError(f"Pose not selected for performance: {asset_id}/{variant}: {state}")
    path = checked_image(root, file, alpha=True)
    sidecar = path.with_suffix(".json")
    if not sidecar.is_file():
        raise ValueError(f"Pose has no provenance sidecar: {sidecar}")
    details = json.loads(sidecar.read_text())
    if (details.get("image_sha256") != file["sha256"]
            or details.get("asset_id") != asset_id or details.get("variant") != variant
            or details.get("status") != state):
        raise ValueError(f"Pose registry/sidecar mismatch: {sidecar}")
    canonical = asset.get("canonical")
    if not isinstance(canonical, dict):
        raise ValueError(f"Missing canonical identity for {actor}")
    checked_image(root, canonical)
    return {
        "pose_path": path, "pose": file, "pose_status": state,
        "asset_id": asset_id, "variant": variant, "actor": actor,
        "canonical": canonical,
        "requires_owner_pose_review": state not in APPROVED_POSE_STATES,
    }


def s05_roll_staging(root: Path) -> dict:
    """Recover selected shot placement and exact references from its sidecar."""
    previous = repo_path(root, S05_PREVIOUS)
    sidecar = previous.with_suffix(".json")
    if not sidecar.is_file():
        raise ValueError(f"Missing S05 staging sidecar: {sidecar}")
    data = json.loads(sidecar.read_text())
    if data.get("path") != S05_PREVIOUS:
        raise ValueError("Roll sidecar does not identify the expected scene")
    check_sha(previous, data.get("sha256"))
    creation = data.get("creation") or {}
    background = creation.get("background") or {}
    if background.get("path") != S05_BACKGROUND:
        raise ValueError("Roll stage uses a different scene plate; no implicit camera change")
    bgpath = checked_image(root, background)
    registered_roll = resolve_pose(root, STORY, "Milo", ROLL_ASSET, "roll")
    actor = creation.get("actor") or {}
    if (actor.get("path") != registered_roll["pose"]["path"]
            or actor.get("sha256") != registered_roll["pose"]["sha256"]):
        raise ValueError("Roll scene does not use the selected registered roll pose")
    xy = creation.get("translate_pixels")
    scale = creation.get("scale")
    if (not isinstance(xy, list) or len(xy) != 2
            or any(type(x) is not int for x in xy)
            or not isinstance(scale, (int, float)) or not 0 < scale <= 2):
        raise ValueError("Missing safe uniform roll transform")
    with Image.open(bgpath) as im:
        if im.size != (1672, 941):
            raise ValueError("Changed S05 base camera/canvas; review required")
    return {
        "background": bgpath, "previous": previous,
        "background_ref": background,
        "roll_ref": {"path": S05_PREVIOUS, "sha256": data["sha256"]},
        "roll_pose": registered_roll["pose"], "origin": xy, "scale": float(scale),
    }


def compose_unchanged_body(background: Image.Image, actor: Image.Image,
                           xy: tuple[int, int], uniform_scale: float) -> tuple[Image.Image, Image.Image, dict]:
    """Place the complete pose without generative redrawing; protect scene pixels."""
    if (not isinstance(uniform_scale, (int, float)) or not 0 < uniform_scale <= 2
            or actor.mode != "RGBA" or len(xy) != 2):
        raise ValueError("Valid RGBA pose, translation and uniform scale required")
    base = background.convert("RGB")
    resized = actor.resize(
        (max(1, round(actor.width * uniform_scale)), max(1, round(actor.height * uniform_scale))),
        Image.Resampling.LANCZOS,
    )
    # Reject clipping instead of silently losing feet, tail or ears.
    a = resized.getchannel("A").getbbox()
    if a is None:
        raise ValueError("Pose is empty")
    if (xy[0] + a[0] < 0 or xy[1] + a[1] < 0
            or xy[0] + a[2] > base.width or xy[1] + a[3] > base.height):
        raise ValueError("Pose would be cropped outside the scene canvas")
    layer = Image.new("RGBA", base.size)
    layer.alpha_composite(resized, tuple(xy))
    x0, y0, x1, y1 = layer.getchannel("A").getbbox()
    # Shadow is an approximation. It is NOT a verified contact/support solution.
    shadow = Image.new("L", base.size)
    w, h = x1 - x0, y1 - y0
    sx, sy = (x0 + x1) // 2, y1 - max(3, round(h * 0.055))
    ImageDraw.Draw(shadow).ellipse(
        (sx - round(w * .38), sy - round(h * .038),
         sx + round(w * .38), sy + round(h * .038)), fill=55,
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(max(3, round(h * .022))))
    shade = Image.new("RGBA", base.size, (29, 23, 17, 0))
    shade.putalpha(shadow)
    result = Image.alpha_composite(Image.alpha_composite(base.convert("RGBA"), shade), layer).convert("RGB")
    effect = (np.asarray(layer.getchannel("A")) > 0) | (np.asarray(shadow) > 0)
    delta = np.any(np.asarray(result) != np.asarray(base), axis=2)
    violations = int(np.count_nonzero(delta & ~effect))
    if violations:
        raise AssertionError(f"Changed {violations} protected scene pixels")
    mask = Image.fromarray(np.where(effect, 255, 0).astype("uint8"), mode="L")
    return result, mask, {
        "changed_pixels_outside_effect_mask": violations,
        "changed_pixels_inside_effect_mask": int(np.count_nonzero(delta & effect)),
        "visible_pose_bbox": [x0, y0, x1, y1],
        "whole_actor_scale": uniform_scale, "origin_pixels": list(xy),
        "actor_semantically_redrawn": False,
        "resampling": "whole RGBA actor, Lanczos uniform resize",
        "shadow_contact_review": "UNVERIFIED: approximate bbox-based shadow",
        "occlusion_review": "UNVERIFIED: no Leo foreground mask applied",
        "anatomy_visual_pass": None, "physical_contact_pass": None,
    }


def _relative_link(page_dir: Path, source: Path) -> str:
    return html.escape(os.path.relpath(source, start=page_dir).replace(os.sep, "/"), quote=True)


def pilot_s05(root: Path, out_dir: Path, *, allow_provisional: bool = False) -> dict:
    """Write 3 immutable review candidates, derived from real S05 source staging."""
    root, out_dir = root.resolve(), out_dir.resolve()
    if out_dir.exists():
        raise FileExistsError(f"Immutable pilot output exists: {out_dir}; use new --out-dir")
    stage = s05_roll_staging(root)
    landing_pose = resolve_pose(root, STORY, "Milo", ROLL_ASSET, "nose_landing",
                                allow_provisional=allow_provisional)
    with Image.open(stage["background"]) as im:
        base = im.convert("RGB")
    with Image.open(landing_pose["pose_path"]) as im:
        actor = im.convert("RGBA")
    out_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out_dir.parent, prefix=".pose_first_candidate_") as temp:
        work = Path(temp)
        candidates = []
        tiles = []
        for tag, dx, dy in S05_OFFSETS:
            xy = tuple(stage["origin"][i] + off for i, off in enumerate((dx, dy)))
            image, mask, checks = compose_unchanged_body(base, actor, xy, stage["scale"])
            path = work / f"S05-L009-B01-I04_pose_first_{tag}_r001_candidate.png"
            mp = work / f"{tag}_effect_mask.png"
            image.save(path)
            mask.save(mp)
            preview = image.copy()
            preview.thumbnail((960, 540))
            preview.save(work / f"{tag}_preview.jpg", quality=80, optimize=True)
            row = {
                "status": "UNSELECTED_REVIEW_ONLY", "scene_image_id": "S05-L009-B01-I04",
                "variant": tag, "relative_to_roll": [dx, dy],
                "candidate": path.name, "candidate_sha256": digest(path),
                "effect_mask": mp.name, "effect_mask_sha256": digest(mp),
                "background": stage["background_ref"],
                "preceding_roll_scene": stage["roll_ref"],
                "selected_roll_performance": stage["roll_pose"],
                "performance": {
                    "actor": landing_pose["actor"], "asset_id": landing_pose["asset_id"],
                    "variant": landing_pose["variant"], "file": landing_pose["pose"],
                    "canonical": landing_pose["canonical"],
                    "status": landing_pose["pose_status"],
                },
                "checks": checks, "provider_calls": 0, "gpu_jobs": 0,
                "owner_pose_review_required": landing_pose["requires_owner_pose_review"],
                "owner_scene_selection": None,
                "limitations": [
                    "Projected actor fit, direction, contact, occlusion and approximate shadow are unverified.",
                    "No S05 scene, pose or later video is approved by this CPU pilot.",
                ],
            }
            candidates.append(row)
            tiles.append((tag, preview))
        sheet = Image.new("RGB", (3 * 520, 350), (27, 31, 27))
        draw = ImageDraw.Draw(sheet)
        for i, (tag, im) in enumerate(tiles):
            im.thumbnail((512, 306))
            sheet.paste(im, (i * 520 + 4, 32))
            draw.text((i * 520 + 12, 8), f"{tag.upper()} - REVIEW ONLY", fill=(250, 245, 225))
        sheet.save(work / "CONTACT_SHEET.jpg", quality=80, optimize=True)
        report = {
            "schema": "feltwillow.pose-first-repair-preview.v2",
            "source_branch": "wan-new-image-approach",
            "operation": "S05 nose landing: selected roll setup + registry landing pose",
            "cost": "CPU-only, zero image or GPU provider calls",
            "requires_owner_selection": True, "selection_effect": "none",
            "staging_source": {
                "scene": stage["roll_ref"], "pose": stage["roll_pose"],
                "original_transform": {"scale": stage["scale"], "translate_pixels": stage["origin"]},
            },
            "candidates": candidates,
        }
        (work / "RECEIPTS.json").write_text(json.dumps(report, indent=2) + "\n")
        predecessor = _relative_link(out_dir, stage["previous"])
        pose_href = _relative_link(out_dir, landing_pose["pose_path"])
        old_file = repo_path(root, REJECTED_CANDIDATE)
        old_link = _relative_link(out_dir, old_file) if old_file.is_file() else None
        cards = []
        for row in candidates:
            fname = html.escape(row["candidate"], quote=True)
            cards.append(
                "<section><h2>" + html.escape(row["variant"]) + " - review-only</h2>"
                "<div class='pair'>"
                f"<figure><a href='{predecessor}'><img src='{predecessor}'></a><figcaption>Previous roll scene</figcaption></figure>"
                f"<figure><a href='{fname}'><img src='{fname}'></a><figcaption>Proposed nose landing (native PNG)</figcaption></figure>"
                "</div><p>Inspect Milo's limbs, tail, muzzle/nose gap, foot support, Leo's paws and the approximate shadow. "
                "Nothing is selected; no contact or anatomy pass is implied.</p></section>"
            )
        old_section = (f"<p>Old rejected landing: <a href='{old_link}'>compare original candidate</a></p>"
                       if old_link else "<p>Old rejected candidate is not present in this checkout; comparison uses the previous roll.</p>")
        page = "<!doctype html><html lang='en'><meta charset='utf-8'><title>Feltwillow S05 pilot</title>"
        page += "<style>body{background:#171a17;color:#f3f0e8;font:16px system-ui;max-width:1450px;margin:2rem auto;padding:1rem}"
        page += ".pair{display:grid;grid-template-columns:1fr 1fr;gap:1rem}figure{margin:0}img{width:100%;height:auto}"
        page += "a{color:#9cdefb}section{border-top:1px solid #777;padding:1rem}figcaption{color:#bbb}"
        page += "@media(max-width:800px){.pair{grid-template-columns:1fr}}</style>"
        page += "<h1>S05 grounded nose landing - pose-first reconstruction</h1>"
        page += "<p>3 whole-actor staging previews, no generation provider, unchanged scene background outside mask.</p>"
        page += old_section
        page += f"<p>Registered landing pose: <a href='{pose_href}'>view the original transparent pose</a>"
        page += ". This pose is provisional and must be reviewed before production use.</p>"
        page += "<p><a href='RECEIPTS.json'>Exact-hash receipts</a> | <a href='CONTACT_SHEET.jpg'>Contact sheet</a></p>"
        page += "".join(cards) + "</html>\n"
        (work / "REVIEW.html").write_text(page)
        # Move the finished directory as a unit: no partially written named revision.
        if out_dir.exists():
            raise FileExistsError(f"Output created concurrently: {out_dir}")
        work.rename(out_dir)
    return report


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--out-dir", type=Path)
    ap.add_argument("--pilot-s05", action="store_true", required=True)
    ap.add_argument("--allow-unreviewed-pose", action="store_true",
                    help="Preview-only; never promote an unreviewed pose or scene")
    args = ap.parse_args()
    root = args.repo_root.resolve()
    dest = args.out_dir or root / "stories/lion_and_mouse_v7/review/pose_first_s05_pilot_r001"
    receipt = pilot_s05(root, dest, allow_provisional=args.allow_unreviewed_pose)
    print(json.dumps({
        "candidates": [c["candidate"] for c in receipt["candidates"]],
        "review": str(dest / "REVIEW.html"), "selection_effect": "none",
    }, indent=2))


if __name__ == "__main__":
    main()
