"""Resolve a staged story frame into a deterministic compositor recipe."""

from __future__ import annotations

import json
from pathlib import Path

try:
    from . import keyframe_plan
except ImportError:  # pragma: no cover - script entry point
    import keyframe_plan


REPO = Path(__file__).resolve().parents[1]


def parse_actor_source(spec: str) -> tuple[str, dict]:
    """Parse ``actor=still.png[,flip]`` used by the staged compositor CLI."""
    actor, separator, remainder = spec.partition("=")
    if not separator or not actor.strip() or not remainder.strip():
        raise ValueError("staged --char must be ACTOR=STILL.png[,flip]")
    still, *flags = remainder.split(",")
    options = {flag.strip() for flag in flags if flag.strip()}
    if options - {"flip"}:
        raise ValueError(f"unknown staged character option(s): {sorted(options - {'flip'})}")
    return actor.strip(), {"still": still.strip(), "flip": "flip" in options}


def resolve_staged_recipe(story: str, frame_id: str, char_specs: list[str],
                          root: Path = REPO) -> dict:
    """Derive plate, registered crop, contacts and anatomy targets from staging."""
    root = Path(root).resolve()
    story_dir = root / "stories" / story
    staging = json.loads((story_dir / "staging_plan.json").read_text())
    frames = {frame["id"]: frame for frame in staging["frames"]}
    if frame_id not in frames:
        raise ValueError(f"unknown staged frame: {frame_id}")
    frame = frames[frame_id]
    specs = dict(parse_actor_source(spec) for spec in char_specs)
    staged_actors = set(frame.get("actors", {}))
    if set(specs) != staged_actors:
        raise ValueError(f"{frame_id}: --char actors must match staging exactly; "
                         f"expected={sorted(staged_actors)}, got={sorted(specs)}")
    view = staging["views"][frame["view"]]
    crop = keyframe_plan.crop_for_frame(frame, view["magnification"])
    left, top, width, height = crop
    characters = []
    for actor in sorted(staged_actors):
        placement = frame["actors"][actor]
        plate_x, plate_y = placement["contact_xy_on_plate"]
        x = (plate_x - left) / width
        y = (plate_y - top) / height
        if not (0 <= x <= 1 and 0 <= y <= 1):
            raise ValueError(f"{frame_id}: registered crop excludes {actor}'s staged contact point")
        characters.append({
            **specs[actor],
            "actor": actor,
            "x": x,
            "y": y,
            "h": placement["standing_equivalent_height_fraction_after_crop"],
        })
    return {
        "story": story,
        "frame_id": frame_id,
        "plate": frame["plate"],
        "crop_rect_on_plate": crop,
        "characters": characters,
        "view": frame["view"],
        "camera_focus": frame.get("camera_focus", "registered_plate_focus"),
        "background_focus": view.get("background_focus", "registered_plate_focus"),
        "blur_sigma_px": view.get("blur_sigma_px", 0.0),
        "size_anchor_id": frame.get("size_anchor_id"),
    }
