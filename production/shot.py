#!/usr/bin/env python3
"""Render a story shot: Wan 2.2 image-to-video from its keyframe(s).

  python production/shot.py --story lion_and_mouse_v5 --scene 1 --shot s01_explores_closed_r01 \\
      [--seed 5101] [--fast] [--recompose] [--dry-run]

The shot is defined in stories/<story>/story.yaml under its scene (`shots:`).
The prompt is the shot's action, then each character's frozen sheet, then the
location sheet (or the shot's `background:`) and the style bible. `--dry-run`
checks the inputs and prints the assembled prompt and negative.

First frame, in order of precedence: `continue_from: {shot, take, frame}` (a
frame of another shot's render), a `compose:` recipe (built when the keyframe
is missing or with --recompose), or the `keyframe:` file itself. Optional
`end_keyframe:` (+ `end_compose:`) pins the last frame.

A shot's own `prompt:` (and `negative:`) is used verbatim instead: v5 runtime
stories exported from a prompt manifest carry the complete reviewed prompt.

Paths in story.yaml are relative to <FELTWILLOW_WORK>/stories/<story>/.
Output: <FELTWILLOW_WORK>/stories/<story>/shots/<shot>_s<seed>[_fast].mp4
+ .json sidecar (prompt,
negative, seed, model revision, LoRAs, settings and input hashes). An existing
output is reused only when its sidecar proves the recipe and inputs still match.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from feltwillow import paths, wan  # noqa: E402
from feltwillow.render_receipt import inspect_render  # noqa: E402

RENDER = dict(width=1280, height=720, steps=40, guidance=3.5, guidance_2=3.5)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def check_existing_render(out: Path, expected: dict) -> None:
    """Never silently reuse a clip made from different or unrecorded inputs."""
    status, reason = inspect_render(out, expected)
    if status != "complete":
        raise SystemExit(f"{out}: {reason or 'render is missing'}; "
                         "review it and move it aside before rendering again")


def check_recipe(work: Path, recipe: dict, what: str) -> None:
    """Every input of a compose recipe must exist before any GPU time is spent."""
    for c in recipe.get("characters", []):
        if not (work / c["still"]).is_file():
            raise SystemExit(f"{what}: missing still {work / c['still']}")
    if not (work / recipe["plate"]).is_file():
        raise SystemExit(f"{what}: missing plate {work / recipe['plate']}")


def compose_recipe(work: Path, recipe: dict, out: Path) -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import keyframe as kf             # cv2 + BiRefNet: only when a keyframe is built

    kf.compose_recipe(work, recipe, out)
    print(f"composed keyframe {out}", flush=True)


def main() -> None:
    import yaml

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", required=True)
    ap.add_argument("--scene", type=int, required=True)
    ap.add_argument("--shot", required=True)
    ap.add_argument("--seed", type=int, help="default: every seed listed for the shot")
    ap.add_argument("--recompose", action="store_true",
                    help="rebuild the keyframe from the shot's compose: recipe even if it exists")
    ap.add_argument("--fast", action="store_true",
                    help="Wan2.2-Lightning 4-step LoRA (~20x faster); output gets a _fast suffix")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--audit-existing", action="store_true",
                    help="read-only JSON inventory of each seed and its input receipt; no GPU")
    args = ap.parse_args()
    if args.audit_existing and (args.dry_run or args.recompose):
        ap.error("--audit-existing cannot be combined with --dry-run or --recompose")

    story = yaml.safe_load((paths.STORIES / args.story / "story.yaml").read_text())
    scene = story["scenes"].get(args.scene)
    if scene is None:
        raise SystemExit(f"{args.story}: no scene {args.scene}")
    shot = next((s for s in scene.get("shots", []) if s["name"] == args.shot), None)
    if shot is None:
        raise SystemExit(f"{args.story} scene {args.scene}: no shot named {args.shot}")
    work = paths.story_work(args.story)
    keyframe = work / shot["keyframe"]
    parts = [shot.get("action", "").strip()]
    # `lora: true` on a shot: every character in it that has a chosen LoRA
    # (`lora:` under the character) gets it, and its trigger word in the prompt,
    # the way the training captions put it: "<trigger>, <description>".
    loras = []
    for c in ([] if shot.get("prompt") else shot.get("characters", scene.get("characters", []))):
        ch = story["characters"][c]
        use = shot.get("lora") and ch.get("lora")
        if use:
            d = paths.WORK / "lora" / ch["lora"]["name"]
            suf = f"-step{int(ch['lora']['step']):08d}" if ch["lora"].get("step") else ""
            loras.append(dict(name=c, weight=ch["lora"].get("weight", 1.0),
                              high=d / "out_high" / f"{ch['lora']['name']}_high{suf}.safetensors",
                              low=d / "out_low" / f"{ch['lora']['name']}_low{suf}.safetensors"))
        name = ch["name"][0].upper() + ch["name"][1:]
        parts.append(f"{name} is {ch['trigger'] + ', ' if use else ''}{ch['sheet']}.")
    # `background:` replaces the location sheet, for close-ups: the full sheet
    # names landmarks (a tree trunk...) that the model then tries to show,
    # wandering away from the keyframes mid-shot (v2 s04_leo_softens).
    if shot.get("prompt"):
        pass
    elif shot.get("background"):
        parts.append(f"The background is {shot['background'].strip()}.")
    else:
        parts.append(f"The scene is {story['locations'][scene['location']]['sheet']}.")
    prompt = shot["prompt"].strip() if shot.get("prompt") else " ".join(parts + [story["style"] + "."])
    negative = shot.get("negative") or (
        story["negative"] + (", " + shot["negative_extra"] if shot.get("negative_extra") else ""))
    seeds = [args.seed] if args.seed is not None else shot["seeds"]
    frames = shot.get("frames", 81)
    if not args.audit_existing:
        print(f"[{args.shot}] keyframe {keyframe.name}, {frames} frames, seeds {seeds}\n{prompt}\n",
              flush=True)
    # Fast mode runs CFG 1: diffusers skips the negative pass, so the text is logged only.
    if not args.audit_existing:
        print(f"NEGATIVE{' (not applied: --fast has no negative pass)' if args.fast else ''}: "
              f"{negative}\n", flush=True)
    # `continue_from: {shot, take, frame}`: the keyframe is a frame (default: the
    # last) of another shot's render, so the cut is continuous.
    cont = shot.get("continue_from")
    src = None
    if cont:
        if cont.get("file"):
            src = Path(cont["file"])
            if not src.is_absolute():
                src = paths.WORK / src
        else:
            src_work = paths.story_work(cont.get("story", args.story))
            src = src_work / "shots" / f"{cont['shot']}_s{cont['take']}.mp4"
        if not src.is_file():
            raise SystemExit(f"continue_from: missing render {src}")
        expected_hash = cont.get("sha256")
        if expected_hash:
            actual_hash = sha256(src)
            if actual_hash != expected_hash:
                raise SystemExit(f"continue_from: source hash changed for {src}; recreate the repair override")
        if not args.audit_existing:
            print(f"keyframe = frame {cont.get('frame', -1)} of {src.name}")
    recipe = shot.get("compose")
    if recipe and not cont:
        check_recipe(work, recipe, "keyframe recipe")
    elif not cont and not keyframe.is_file():
        raise SystemExit(f"missing keyframe {keyframe} and no compose: recipe")
    for lo in loras:
        for f in (lo["high"], lo["low"]):
            if not f.is_file():
                raise SystemExit(f"missing LoRA {f}")
        if not args.audit_existing:
            print(f"LoRA {lo['name']}: {lo['high'].name} + {lo['low'].name} x{lo['weight']}")
    # `end_keyframe:` (+ optional `end_compose:` recipe): the frame the shot must
    # arrive at. Wan 2.2 I2V-A14B then animates between two stills (first/last
    # frame), which pins identity and pose at both ends (docs/prompting.md 3.4).
    # An end keyframe equal to the start keyframe is the start file itself.
    end_key = work / shot["end_keyframe"] if shot.get("end_keyframe") else None
    end_recipe = shot.get("end_compose")
    build_end = bool(end_key and end_key != keyframe and end_recipe
                     and (args.recompose or not end_key.is_file()))
    if build_end:
        check_recipe(work, end_recipe, "end_compose")
    elif end_key and end_key != keyframe and not end_key.is_file():
        raise SystemExit(f"missing end keyframe {end_key} and no end_compose: recipe")
    if args.dry_run:
        print("dry run: inputs ok" + (" (keyframe will be composed)" if recipe else ""))
        return
    if args.audit_existing and (not keyframe.is_file() or (end_key and not end_key.is_file())):
        # A missing derived keyframe may be composed by the queued render. An
        # existing MP4 cannot be verified without the original input hashes.
        inventory = []
        for seed in seeds:
            out = work / "shots" / f"{args.shot}_s{seed}{'_fast' if args.fast else ''}.mp4"
            inventory.append(dict(seed=seed, output=str(out),
                                  status="stale" if out.is_file() else "missing",
                                  reason="keyframe unavailable for receipt audit" if out.is_file() else None))
        print(json.dumps(dict(story=args.story, scene=args.scene, shot=args.shot,
                              seeds=inventory), sort_keys=True))
        return
    if not args.audit_existing:
        from PIL import Image
    if cont:
        if not args.audit_existing:
            from feltwillow import media

            frames_ = media.read_frames(src)
            keyframe.parent.mkdir(parents=True, exist_ok=True)
            Image.fromarray(frames_[int(cont.get("frame", -1))]).save(keyframe)
            print(f"keyframe from {src.name} -> {keyframe}", flush=True)
    elif recipe and (args.recompose or not keyframe.is_file()):
        if not args.audit_existing:
            compose_recipe(work, recipe, keyframe)
    if build_end:
        if not args.audit_existing:
            compose_recipe(work, end_recipe, end_key)
    render = {**RENDER, **(wan.LIGHTNING["render"] if args.fast else {})}
    if shot.get("size"):          # e.g. [1248, 832] to match 3:2 reference images
        render["width"], render["height"] = (int(v) for v in shot["size"])
    lora_details = [{k: str(v) for k, v in lo.items()} for lo in loras]
    lora_hashes = [{"high": sha256(lo["high"]), "low": sha256(lo["low"])} for lo in loras]
    expected = dict(
        stage="shot", scene=args.scene, shot=args.shot, keyframe=str(keyframe),
        end_keyframe=str(end_key) if end_key else None,
        keyframe_sha256=sha256(keyframe),
        end_keyframe_sha256=sha256(end_key) if end_key else None,
        continuation_sha256=sha256(src) if src else None,
        model=wan.model_id("i2v"), frames=frames, prompt=prompt,
        negative=negative, loras=lora_details, lora_sha256=lora_hashes,
        fast=args.fast,
        lightning=({key: wan.LIGHTNING[key] for key in ("repo", "revision", "folder", "shift")}
                   if args.fast else None),
        **render)
    if args.audit_existing:
        inventory = []
        for seed in seeds:
            out = work / "shots" / f"{args.shot}_s{seed}{'_fast' if args.fast else ''}.mp4"
            status, reason = inspect_render(out, {**expected, "seed": seed})
            inventory.append(dict(seed=seed, output=str(out), status=status, reason=reason))
        print(json.dumps(dict(story=args.story, scene=args.scene, shot=args.shot,
                              seeds=inventory), sort_keys=True))
        return
    pending = []
    for seed in seeds:
        out = work / "shots" / f"{args.shot}_s{seed}{'_fast' if args.fast else ''}.mp4"
        if out.is_file():
            check_existing_render(out, {**expected, "seed": seed})
            print(f"verified existing render {out.name}")
        else:
            pending.append((seed, out))
    if not pending:
        return
    pipe = wan.load("i2v", frames, loras=loras, fast=args.fast)
    print("model loaded", flush=True)
    for seed, out in pending:
        t0 = time.time()
        video = wan.generate(pipe, prompt, negative=negative, frames=frames, seed=seed,
                             image=Image.open(keyframe),
                             last_image=Image.open(end_key) if end_key else None, **render)
        wan.save(video, out)
        out.with_suffix(".json").write_text(json.dumps(
            {**expected, "seed": seed, "seconds": round(time.time() - t0)}, indent=2))
        print(f"saved {out} ({time.time() - t0:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
