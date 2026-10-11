"""Hash-checked lookup for post-render lip-synced chained takes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from . import paths
from .version_policy import require_story_local_audio


def entry_for(story: str, piece: str) -> dict | None:
    index = paths.story_work(story) / "lipsync" / "lipsync_manifest.json"
    if not index.is_file():
        return None
    try:
        return json.loads(index.read_text(encoding="utf-8")).get("pieces", {}).get(piece)
    except (OSError, json.JSONDecodeError):
        return None


def line_audio_path(audio_dir: Path, locator: str) -> Path | None:
    """Resolve old absolute or new audio-relative line locators inside one story root."""
    try:
        raw = Path(locator)
        relative = Path("lines") / raw.name if raw.is_absolute() else raw
        root = audio_dir.resolve()
        path = (root / relative).resolve()
        if root not in path.parents or not path.is_file():
            return None
        return path
    except (OSError, TypeError, ValueError):
        return None



def recipe_sha256(story: str, piece: str) -> str | None:
    """Fingerprint the current timing, speaker assignment and approved mouth anchors."""
    story_dir = paths.STORIES / story
    try:
        plan_path = story_dir / "timing_plan.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        row = next(r for r in plan["segments"] if r["piece"] == piece)
        if row.get("mode") != "mouth":
            return None
        manifest_path = story_dir / "prompt_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        shot = next(s for s in manifest["shots"] if s["id"] == piece)
        variant = next(v for v in shot["variants"] if v["id"] == row["variant"])
        audio_story = plan.get("audio_story") or story
        require_story_local_audio(story, audio_story, consumer="lipsync recipe")
        audio_dir = paths.story_audio(audio_story, plan.get("lang", "en"))
        word_path = audio_dir / "word_timings.json"
        words = json.loads(word_path.read_text(encoding="utf-8"))
        images = {r["id"]: r for r in manifest["images"]}
        image_ids = {variant.get("start_image", shot["start_image"]),
                     variant.get("end_image", shot["end_image"]), variant.get("mouth_open_image")}
        files = [plan_path, manifest_path, story_dir / "visual_bible.json",
                 story_dir / "dialogue_coverage.json", audio_dir / "timing.json", word_path]
        files.extend(paths.REPO / images[i]["target"] for i in image_ids if i)
        audio_files = [line_audio_path(audio_dir, words["lines"][lid]["audio_file"])
                       for lid in row["lines"]]
        if any(path is None for path in audio_files):
            return None
        files.extend(audio_files)
        digest = hashlib.sha256(b"feltwillow-lipsync-recipe-v2\0")
        for index, path in enumerate(files):
            # Input order is fixed above by semantic role; only bytes enter the
            # identity so the same approved inputs hash equally after transfer.
            digest.update(index.to_bytes(4, "big"))
            file_digest, size = hashlib.sha256(), 0
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    file_digest.update(block)
                    size += len(block)
            digest.update(size.to_bytes(8, "big"))
            digest.update(file_digest.digest())
        return digest.hexdigest()
    except (OSError, KeyError, StopIteration, TypeError, ValueError, json.JSONDecodeError):
        return None


def resolve_synced_take(story: str, piece: str, source: Path) -> Path | None:
    """Return a lipsynced take only when it was made from this unchanged source clip."""
    entry = entry_for(story, piece)
    current_recipe = recipe_sha256(story, piece)
    if not entry or current_recipe is None or entry.get("recipe_sha256") != current_recipe:
        return None
    try:
        source = source.resolve()
        output_name = Path(entry["output_file"]).name
        if not output_name or output_name in (".", ".."):
            return None
        output_root = (paths.story_work(story) / "lipsync").resolve()
        output = output_root / output_name
        if output.resolve().parent != output_root:
            return None
    except (KeyError, OSError):
        return None
    if not source.is_file() or not output.is_file():
        return None
    # Paths, mtimes and sizes vary when work moves between hosts. Byte hashes
    # are the identity check for both the selected source and synced output.
    for path, field in ((source, "source_sha256"), (output, "output_sha256")):
        digest = hashlib.sha256()
        try:
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
        except OSError:
            return None
        if digest.hexdigest() != entry.get(field):
            return None
    return output
