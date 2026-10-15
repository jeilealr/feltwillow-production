#!/usr/bin/env python3
"""Compose a shot's first frame: characters cut from their pose stills, placed
into a location plate.

Why: image-to-video keeps what is in the first frame. If that frame already
holds the exact character (from its canonical or a pose clip) in the exact
place (the location plate), the shot starts on-model and on-set, which text
alone cannot guarantee.

Cut-out: BiRefNet matting (a chroma key against the plain design backdrop if
the model cannot be loaded). Placement: the matte's bounding box is scaled to a
height `h` (fraction of the frame) with its bottom edge, the feet, at (x, y).
A soft contact shadow grounds it; only its brightness is matched to the plate,
never its hue. Optional: a virtual close-up of the plate (`crop`, Real-ESRGAN,
cached next to the plate) and a background blur.

  python production/keyframe.py --plate PLATE.png --out KEY.png \\
      --char STILL.png:x=0.5,y=0.82,h=0.45[,flip]  [--char ...] [--plate-crop x,y,w]

Output: KEY.png + KEY.json (where each character went). story.yaml `compose:`
recipes are built through `compose_recipe` (shot.py).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

try:
    from .keyframe_staging_recipe import resolve_staged_recipe
    from .materialize_plate_crop import materialize
except ImportError:  # pragma: no cover - script entry point
    from keyframe_staging_recipe import resolve_staged_recipe
    from materialize_plate_crop import materialize


BIREFNET = ("ZhengPeng7/BiRefNet", "e2bf8e4460fc8fa32bba5ea4d94b3233d367b0e4")   # MIT; pinned
_birefnet = None


def _vision_dependencies():
    """Load optional compositor libraries only when image work is requested."""
    try:
        import cv2
        import numpy as np
        from PIL import Image
    except ImportError as error:  # pragma: no cover - depends on local runtime
        raise RuntimeError("keyframe composition needs opencv-python, numpy and Pillow") from error
    return cv2, np, Image


def matte(img: np.ndarray) -> np.ndarray:
    """Soft alpha (0..1) of the character.

    BiRefNet (MIT licence, revision pinned because it runs remote code) is a
    learned matting model: it keeps a grey mouse whole against a grey-green
    backdrop and preserves thin tails and wispy felt, where colour keying cut
    holes. Falls back to the colour key if the model cannot be loaded.
    """
    global _birefnet
    cv2, np, Image = _vision_dependencies()
    try:
        import torch
        from torchvision import transforms
        from transformers import AutoModelForImageSegmentation

        if _birefnet is None:
            _birefnet = AutoModelForImageSegmentation.from_pretrained(
                BIREFNET[0], trust_remote_code=True, revision=BIREFNET[1]).eval().float()
            if torch.cuda.is_available():
                _birefnet = _birefnet.cuda()
        dev = next(_birefnet.parameters()).device
        tf = transforms.Compose([transforms.Resize((1024, 1024)), transforms.ToTensor(),
                                 transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
        with torch.no_grad():
            pred = _birefnet(tf(Image.fromarray(img))[None].to(dev))[-1].sigmoid()[0, 0].cpu().numpy()
        return cv2.resize(pred, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LINEAR)
    except Exception as err:                        # pragma: no cover
        print(f"BiRefNet unavailable ({type(err).__name__}: {err}); using the colour key")
        return matte_colour_key(img)


def matte_colour_key(img: np.ndarray, t_lo: float = 8.0, t_hi: float = 18.0) -> np.ndarray:
    """Soft alpha (0..1) for a character on the plain design backdrop.

    Measured on the design stills: backdrop chroma (Lab a/b distance from the
    per-row backdrop colour, sampled at the left and right edges) stays below
    ~3, while the characters sit at 20-60. So chroma alone separates them, and
    the character's shadow on the floor (darker, same hue) never qualifies.
    The alpha is a soft ramp between t_lo and t_hi, which keeps the felt's
    wispy fibres semi-transparent instead of cutting them into a hard edge.
    No GrabCut: it pulled floor and backdrop fringe in with the subject.
    Interior pixels close to the backdrop colour (a cream muzzle, a grey belly)
    are kept by filling holes in the solid core.
    """
    cv2, np, _ = _vision_dependencies()
    h, w = img.shape[:2]
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB).astype(np.float32)
    k = max(8, w // 20)
    bg = np.median(np.concatenate([lab[:, :k], lab[:, -k:]], axis=1), axis=1)
    bg = cv2.GaussianBlur(bg[:, None, :], (1, 0), sigmaX=0.1, sigmaY=6)[:, 0, :]
    d = lab - bg[:, None, :]
    chroma = np.hypot(d[..., 1], d[..., 2])
    soft = np.clip((chroma - t_lo) / (t_hi - t_lo), 0, 1)
    core = (soft > 0.5).astype(np.uint8)
    core = cv2.morphologyEx(core, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab_cc, stats, _ = cv2.connectedComponentsWithStats(core)
    if n < 2:
        raise ValueError("no subject found against the backdrop")
    keep = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    core = (lab_cc == keep).astype(np.uint8)
    solid = cv2.morphologyEx(core, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    flood = solid.copy()
    cv2.floodFill(flood, np.zeros((h + 2, w + 2), np.uint8), (0, 0), 1)
    solid = solid | (1 - flood)                                    # holes filled
    near = cv2.dilate(solid, np.ones((7, 7), np.uint8)).astype(np.float32)
    alpha = np.maximum(soft * near, solid.astype(np.float32))
    return cv2.GaussianBlur(alpha, (0, 0), 0.7)


def subject_bbox(img: np.ndarray) -> tuple[int, int, int, int]:
    """Tight box around the character, from the matte (x, y, w, h)."""
    _, np, _ = _vision_dependencies()
    ys, xs = np.nonzero(matte(img) > 0.5)
    if not ys.size:
        raise ValueError("no character found: the matte is empty")
    return int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)


def harmonise(rgb: np.ndarray, alpha: np.ndarray, plate_region: np.ndarray,
              amount: float = 0.35) -> np.ndarray:
    """Match the character's brightness to the plate's local light: luminance
    only, never hue. A character's colours are part of its identity; the first
    version matched each channel and turned the fox's white chest pale green
    in a green forest.
    """
    _, np, _ = _vision_dependencies()
    m = alpha > 0.5
    if m.sum() < 50 or amount <= 0:
        return rgb
    w = np.array([0.299, 0.587, 0.114])
    src = float((rgb[m] * w).sum(1).mean())
    dst = float((plate_region.reshape(-1, 3) * w).sum(1).mean())
    gain = 1 + amount * (dst / max(src, 1.0) - 1)
    return np.clip(rgb * float(np.clip(gain, 0.8, 1.1)), 0, 255)


def place(plate: np.ndarray, still: np.ndarray, x: float, y: float, height: float,
          flip: bool = False, shadow: float = 0.45, light: float = 0.35) -> tuple[np.ndarray, dict]:
    cv2, np, _ = _vision_dependencies()
    H, W = plate.shape[:2]
    # ImageGen RGBA layers already carry a reviewed matte. Recovering a new
    # matte from RGB would discard their transparency and fill holes/background.
    if still.ndim == 3 and still.shape[2] == 4:
        alpha = still[:, :, 3].astype(np.float32) / 255.0
        still = still[:, :, :3]
    else:
        alpha = matte(still)
    ys, xs = np.nonzero(alpha > 0.5)
    if not ys.size:
        raise ValueError("no character found in the still: the matte is empty")
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgb = still[y0:y1, x0:x1].astype(np.float32)
    a = alpha[y0:y1, x0:x1]
    if flip:
        rgb, a = rgb[:, ::-1], a[:, ::-1]
    scale = height * H / rgb.shape[0]
    nw, nh = max(1, int(rgb.shape[1] * scale)), max(1, int(rgb.shape[0] * scale))
    rgb = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA)
    a = cv2.resize(a, (nw, nh), interpolation=cv2.INTER_AREA)
    left, top = int(x * W - nw / 2), int(y * H - nh)              # feet at (x, y)
    out = plate.astype(np.float32).copy()
    # contact shadow: a soft dark ellipse under the feet
    sh = np.zeros((H, W), np.float32)
    cv2.ellipse(sh, (int(x * W), int(y * H)), (int(nw * 0.42), max(3, int(nh * 0.06))),
                0, 0, 360, 1.0, -1)
    sh = cv2.GaussianBlur(sh, (0, 0), max(3, nh * 0.03))
    out *= (1 - shadow * sh)[..., None]
    # paste, clipped to the frame
    sx0, sy0 = max(0, -left), max(0, -top)
    dx0, dy0 = max(0, left), max(0, top)
    dx1, dy1 = min(W, left + nw), min(H, top + nh)
    if dx1 <= dx0 or dy1 <= dy0:
        raise ValueError("character placed outside the frame")
    rgb_c = rgb[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0]
    a_c = a[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0][..., None]
    region = out[dy0:dy1, dx0:dx1]
    rgb_c = harmonise(rgb_c, a_c[..., 0], region, light)
    out[dy0:dy1, dx0:dx1] = region * (1 - a_c) + rgb_c * a_c
    shadow_blur = max(3, nh * 0.03)
    shadow_rx, shadow_ry = int(nw * 0.42), max(3, int(nh * 0.06))
    cx, cy = int(x * W), int(y * H)
    pad = int(shadow_blur * 5) + 1
    ex0 = max(0, min(dx0, cx - shadow_rx - pad))
    ey0 = max(0, min(dy0, cy - shadow_ry - pad))
    ex1 = min(W, max(dx1, cx + shadow_rx + pad))
    ey1 = min(H, max(dy1, cy + shadow_ry + pad))
    return out, dict(box=[dx0, dy0, dx1 - dx0, dy1 - dy0],
                     edit_region=[ex0, ey0, ex1, ey1], scale=round(scale, 3))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _portable_label(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(Path(__file__).resolve().parents[1]).as_posix()
    except ValueError:
        return path.name


def compose(plate: Path, chars: list[dict], out: Path, crop: list[float] | None = None,
            blur: float = 0.0, authority: dict | None = None,
            write_edit_mask: bool = False) -> dict:
    """Build a keyframe. `chars`: [{still, x, y, h, flip?}], x/y = feet position
    as fractions of the frame, h = height fraction. `crop`: [x, y, w] fractions of
    the plate for a virtual close-up (Real-ESRGAN; cached next to the plate).
    `blur`: Gaussian sigma (pixels) applied to the background only, for close-ups
    whose background should be out of focus."""
    if blur < 0:
        raise ValueError("background blur sigma cannot be negative")
    cv2, np, Image = _vision_dependencies()
    frame = np.asarray(Image.open(plate).convert("RGB")).astype(np.float32)
    if crop:
        H, W = frame.shape[:2]
        fx, fy, fw = map(float, crop[:3])
        x0, y0, cw = int(fx * W), int(fy * H), int(fw * W)
        ch = int(cw * H / W)
        # A crop past the plate edge would come back short and be stretched to W x H.
        if x0 < 0 or y0 < 0 or cw < 1 or x0 + cw > W or y0 + ch > H:
            raise ValueError(f"crop {crop} runs outside the {W}x{H} plate {plate}")
        cache = plate.parent / f"{plate.stem}_crop_{fx:.3f}_{fy:.3f}_{fw:.3f}.png"
        # The upscale takes ~15 min on a CPU, so it is cached; a cache older than
        # the plate would silently show the previous version of the set.
        if cache.is_file() and cache.stat().st_mtime >= plate.stat().st_mtime:
            frame = np.asarray(Image.open(cache).convert("RGB")).astype(np.float32)
        else:
            sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
            import torch

            from feltwillow import post

            piece = frame[y0:y0 + ch, x0:x0 + cw].astype(np.uint8)
            dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            frame = post.upscale(piece[None], W, H, dev)[0].astype(np.float32)
            Image.fromarray(frame.astype(np.uint8)).save(cache)
    if blur:                                  # defocus the background for close-ups
        frame = cv2.GaussianBlur(frame, (0, 0), sigmaX=float(blur))
    locked_background = frame.copy()
    editable = np.zeros(frame.shape[:2], dtype=np.uint8)
    placed = []
    for c in chars:
        still_path = Path(c["still"])
        source = Image.open(still_path)
        still = np.asarray(source.convert("RGBA" if "A" in source.getbands() else "RGB"))
        frame, info = place(frame, still, float(c.get("x", 0.5)), float(c.get("y", 0.85)),
                            float(c.get("h", 0.4)), flip=bool(c.get("flip", False)),
                            shadow=float(c.get("shadow", 0.45)), light=float(c.get("light", 0.35)))
        x0, y0, x1, y1 = info.pop("edit_region")
        editable[y0:y1, x0:x1] = 255
        placed.append({**{key: value for key, value in c.items() if key != "still"},
                       "still_source": {"label": _portable_label(still_path),
                                        "sha256": _sha256(still_path)}, **info})
    if not np.array_equal(frame[editable == 0], locked_background[editable == 0]):
        raise RuntimeError("compositor changed protected plate pixels outside its edit mask")
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).save(out)
    record = dict(stage="keyframe", plate_source={"label": _portable_label(plate),
                  "sha256": _sha256(plate)}, crop=crop, blur=blur, characters=placed,
                  authority=authority, protected_region_policy="pixels outside edit mask remain exact")
    record["output_sha256"] = _sha256(out)
    if write_edit_mask:
        mask_path = out.with_name(f"{out.stem}_edit_mask.png")
        Image.fromarray(editable, mode="L").save(mask_path)
        record["edit_mask"] = {"label": mask_path.name, "sha256": _sha256(mask_path),
                               "white": "character/contact-shadow edit region",
                               "black": "protected background region"}
    out.with_suffix(".json").write_text(json.dumps(record, indent=2, default=str))
    return record


def compose_recipe(work: Path, recipe: dict, out: Path) -> dict:
    """Build a keyframe from a story.yaml `compose:` / `end_compose:` recipe
    (plate, characters, crop, blur); its paths are relative to `work`."""
    chars = [{**c, "still": str(work / c["still"])} for c in recipe.get("characters", [])]
    return compose(work / recipe["plate"], chars, out, recipe.get("crop"), recipe.get("blur", 0.0))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plate", type=Path)
    ap.add_argument("--char", action="append", default=[],
                    help="STILL.png:x=..,y=..,h=..[,flip]  (x,y = feet, fractions of the frame)")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--plate-crop", help="x,y,w as fractions: a virtual close-up of the plate")
    ap.add_argument("--blur", type=float, default=None,
                    help="Gaussian background blur sigma in pixels (exposed for portrait composition)")
    ap.add_argument("--story", help="use registered staging for this story instead of manual x/y/h")
    ap.add_argument("--frame", help="staging frame ID; requires --story and --char ACTOR=STILL.png")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                    help="repository root for --story/--frame")
    ap.add_argument("--write-edit-mask", action="store_true",
                    help="write a white-edit/black-protected-background mask beside the base")
    args = ap.parse_args()
    authority = None
    if args.story or args.frame:
        if not args.story or not args.frame or args.plate or args.plate_crop:
            ap.error("--story and --frame must be used together and replace --plate/--plate-crop")
        try:
            recipe = resolve_staged_recipe(args.story, args.frame, args.char, args.root)
        except (ValueError, KeyError, FileNotFoundError) as error:
            ap.error(str(error))
        for character in recipe["characters"]:
            still = Path(character["still"])
            if not still.is_absolute():
                character["still"] = str(args.root / still)
        source_plate = args.root / recipe["plate"]
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="feltwillow-plate-crop-", dir=args.out.parent) as tmp:
            crop_path = Path(tmp) / "registered_crop.png"
            receipt = materialize(source_plate, recipe["crop_rect_on_plate"], crop_path)
            receipt["source_plate"] = recipe["plate"]
            blur = recipe["blur_sigma_px"] if args.blur is None else args.blur
            authority = {key: recipe[key] for key in (
                "story", "frame_id", "crop_rect_on_plate", "view", "camera_focus",
                "background_focus", "size_anchor_id")}
            authority["materialized_crop"] = receipt
            rec = compose(crop_path, recipe["characters"], args.out, blur=blur,
                          authority=authority, write_edit_mask=args.write_edit_mask)
            rec["plate_source"] = {"label": recipe["plate"],
                                   "sha256": receipt["source_sha256"]}
            args.out.with_suffix(".json").write_text(json.dumps(rec, indent=2) + "\n")
    else:
        if not args.plate or not args.char:
            ap.error("manual mode requires --plate and at least one --char")
        chars = []
        for spec in args.char:
            path, _, opts = spec.partition(":")
            kv = dict(o.split("=") if "=" in o else (o, "1") for o in opts.split(",") if o)
            chars.append(dict(still=path, x=float(kv.get("x", 0.5)), y=float(kv.get("y", 0.85)),
                              h=float(kv.get("h", 0.4)), flip="flip" in kv))
        crop = [float(v) for v in args.plate_crop.split(",")[:3]] if args.plate_crop else None
        rec = compose(args.plate, chars, args.out, crop,
                      blur=0.0 if args.blur is None else args.blur,
                      write_edit_mask=args.write_edit_mask)
    print(f"keyframe -> {args.out}  {rec['characters']}")


if __name__ == "__main__":
    main()
