#!/usr/bin/env python3
"""Verify local WAV bytes against a tracked story audio manifest without modifying them."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from feltwillow import paths  # noqa: E402


def work_file(relative: str, work: Path = paths.WORK) -> Path:
    """Resolve legacy `work/...` receipt paths under the configured work root."""
    p = Path(relative)
    if p.is_absolute() or not p.parts or p.parts[0] != "work" or ".." in p.parts:
        raise ValueError(f"audio path is not a work-relative path: {relative!r}")
    resolved = (work / Path(*p.parts[1:])).resolve()
    if work.resolve() not in resolved.parents:
        raise ValueError(f"audio path escapes work root: {relative!r}")
    return resolved


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_wav(path: Path, row: dict, sample_rate: int, channels: int,
               sample_width_bits: int) -> list[str]:
    errors = []
    if not path.is_file():
        return [f"missing WAV: {path}"]
    if sha256(path) != row.get("sha256"):
        errors.append(f"SHA-256 mismatch: {path}")
    try:
        with wave.open(str(path), "rb") as wav:
            actual = (wav.getframerate(), wav.getnchannels(), wav.getsampwidth() * 8)
            expected = (sample_rate, channels, sample_width_bits)
            if actual != expected:
                errors.append(f"format mismatch: {path}: {actual} != {expected}")
            duration = wav.getnframes() / wav.getframerate()
            if abs(duration - float(row["duration_seconds"])) > 0.02:
                errors.append(f"duration mismatch: {path}: {duration:.4f}s")
    except (wave.Error, EOFError, OSError, ValueError) as error:
        errors.append(f"unreadable WAV: {path}: {error}")
    return errors


def verify(manifest: dict, story: str, work: Path = paths.WORK,
           require_source: bool = False) -> list[str]:
    errors = []
    if manifest.get("story") != story:
        errors.append("manifest story does not match requested story")
    if manifest.get("source_story") != story and not manifest.get("owner_authorized_reuse"):
        errors.append("foreign audio provenance lacks owner-authorized reuse")
    lines = manifest.get("lines", [])
    scenes = manifest.get("scenes", [])
    if len(lines) != manifest.get("line_count") or len(scenes) != manifest.get("scene_count"):
        errors.append("line/scene count does not match manifest")
    if len({row.get("id") for row in lines}) != len(lines):
        errors.append("duplicate line ID")
    if len({row.get("scene") for row in scenes}) != len(scenes):
        errors.append("duplicate scene number")
    sample_rate = int(manifest["sample_rate_hz"])
    channels = int(manifest["channels"])
    sample_width_bits = int(manifest["sample_width_bits"])
    for row in lines:
        label = row.get("id", "unknown line")
        try:
            target = work_file(row["v6_path"], work)
            expected_root = (work / "stories" / story / "audio").resolve()
            if expected_root not in target.parents:
                raise ValueError("runtime line is outside this story's audio namespace")
            errors.extend(f"{label}: {error}" for error in verify_wav(
                target, row, sample_rate, channels, sample_width_bits))
            source = work_file(row["source_path"], work)
            if source.is_file() or require_source:
                errors.extend(f"{label} source: {error}" for error in verify_wav(
                    source, row, sample_rate, channels, sample_width_bits))
        except (KeyError, ValueError) as error:
            errors.append(f"{label}: {error}")
    for row in scenes:
        label = f"scene {row.get('scene')}"
        try:
            target = work_file(row["path"], work)
            expected_root = (work / "stories" / story / "audio").resolve()
            if expected_root not in target.parents:
                raise ValueError("runtime scene is outside this story's audio namespace")
            errors.extend(f"{label}: {error}" for error in verify_wav(
                target, row, sample_rate, channels, sample_width_bits))
            if row.get("line_count") != sum(line.get("scene") == row.get("scene") for line in lines):
                errors.append(f"{label}: line count mismatch")
        except (KeyError, ValueError) as error:
            errors.append(f"{label}: {error}")
    if abs(sum(float(row["duration_seconds"]) for row in scenes)
           - float(manifest["total_duration_seconds"])) > 0.05:
        errors.append("total scene duration mismatch")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story", required=True)
    parser.add_argument("--require-source", action="store_true",
                        help="also require original provenance WAVs to be present")
    args = parser.parse_args()
    manifest = json.loads((paths.STORIES / args.story / "audio_manifest.json").read_text())
    errors = verify(manifest, args.story, require_source=args.require_source)
    for error in errors[:25]:
        print("BLOCKED:", error)
    if len(errors) > 25:
        print(f"...and {len(errors) - 25} more")
    print(f"{len(errors)} blockers; {len(manifest['lines'])} lines, "
          f"{len(manifest['scenes'])} scenes; work root {paths.WORK}")
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
