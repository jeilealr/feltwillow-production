#!/usr/bin/env python3
"""Fail-closed adapter for keyframe-plan stories (currently Lion and Mouse v6).

``--preflight`` reads the current packet and reports structural, audio, and
hash-bound visual-review blockers without writing anything. ``--export`` also
requires an explicit per-piece timing file; it never invents cuts within a
spoken line or translates candidate images into approvals.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath

from keyframe_visual_gate import validate as validate_visual_reviews
from keyframe_reference_gate import validate_contract_report as validate_reference_contract_report
from video_boundary_plan import build as build_boundaries

REPO = Path(__file__).resolve().parents[1]
SCHEMA = "feltwillow.keyframe-runtime.v1"
TIMING_SCHEMA = "feltwillow.video-piece-timing.v1"
WORD_SCHEMA = "feltwillow.reviewed-word-timing.v1"
POLICY = "independent_native_visuals"
PIPELINE = "keyframe_boundary_v1"


def _read(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def _path(root: Path, relative: str, work: Path) -> Path:
    if not isinstance(relative, str) or not relative:
        raise ValueError("empty or non-string repository path")
    parts = PurePosixPath(relative)
    if (parts.is_absolute() or "\\" in relative or
            any(part in ("", ".", "..") for part in relative.split("/"))):
        raise ValueError(f"unsafe relative path: {relative}")
    if parts.parts[0] == "work":
        base = work.resolve()
        result = base.joinpath(*parts.parts[1:]).resolve()
    else:
        base = root.resolve()
        result = base.joinpath(*parts.parts).resolve()
    if not result.is_relative_to(base):
        raise ValueError(f"path escapes its designated root: {relative}")
    return result


def _native_path(root: Path, relative: str, prefix: str) -> Path:
    if not relative.startswith(prefix + "/"):
        raise ValueError(f"path is outside native story namespace: {relative}")
    path = _path(root, relative, root / "work")
    native_root = (root / prefix).resolve()
    if not path.is_relative_to(native_root):
        raise ValueError(f"path resolves outside native story namespace: {relative}")
    return path


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _audio_errors(audio: dict, coverage: dict, root: Path, work: Path,
                  require_local_audio: bool) -> list[str]:
    errors: list[str] = []
    story = audio.get("story")
    if audio.get("owner_authorized_reuse") is not True or audio.get("source_story") != "lion_and_mouse_v5":
        errors.append("AUDIO: v6 reuse authorization or v5 provenance is missing")
    source_prefix = "work/the_lion_and_the_mouse/lines/"
    target_prefix = f"work/stories/{story}/audio/en/lines/"
    line_rows = audio.get("lines", [])
    coverage_rows = coverage.get("lines", [])
    if not isinstance(line_rows, list) or not isinstance(coverage_rows, list):
        return errors + ["AUDIO: line collections must be arrays"]
    if audio.get("line_count") != len(line_rows) or len(coverage_rows) != len(line_rows):
        errors.append("AUDIO: line count differs between manifest and coverage")
    by_id = {row.get("id"): row for row in coverage_rows if isinstance(row, dict)}
    if len(by_id) != len(coverage_rows):
        errors.append("AUDIO: duplicate or invalid coverage line IDs")
    seen: set[str] = set()
    for line in line_rows:
        lid = line.get("id")
        if lid in seen:
            errors.append(f"AUDIO: duplicate line {lid}")
        seen.add(lid)
        source = line.get("source_path", "")
        target = line.get("v6_path", "")
        if (not isinstance(source, str) or not source.startswith(source_prefix) or
                not isinstance(target, str) or not target.startswith(target_prefix)):
            errors.append(f"AUDIO: {lid} has invalid source/runtime namespace")
            continue
        row = by_id.get(lid, {})
        if (row.get("audio_path") != target or row.get("audio_sha256") != line.get("sha256") or
                row.get("speaker") != line.get("speaker") or row.get("scene") != line.get("scene")):
            errors.append(f"AUDIO: {lid} coverage/provenance mismatch")
        for label, relative in (("source", source), ("v6", target)):
            try:
                path = _path(root, relative, work)
                namespace_root = (work / ("the_lion_and_the_mouse/lines" if label == "source"
                                          else f"stories/{story}/audio/en/lines")).resolve()
                if not path.is_relative_to(namespace_root):
                    raise ValueError("audio path resolves outside its source/runtime namespace")
            except ValueError as exc:
                errors.append(f"AUDIO: {lid} {label} {exc}")
                continue
            if not path.is_file():
                if require_local_audio:
                    errors.append(f"AUDIO: {lid} {label} WAV is missing: {path}")
                continue
            if _hash(path) != line.get("sha256"):
                errors.append(f"AUDIO: {lid} {label} WAV differs from manifest SHA-256")
    scene_rows = audio.get("scenes", [])
    if not isinstance(scene_rows, list) or audio.get("scene_count") != len(scene_rows):
        errors.append("AUDIO: scene count differs from manifest")
    else:
        for row in scene_rows:
            number = row.get("scene")
            expected = f"work/stories/{story}/audio/en/scene{number:02d}.wav" if isinstance(number, int) else ""
            if row.get("path") != expected:
                errors.append(f"AUDIO: scene {number} has wrong runtime namespace")
                continue
            try:
                path = _path(root, expected, work)
                if not path.is_relative_to((work / f"stories/{story}/audio/en").resolve()):
                    raise ValueError("scene audio escapes runtime namespace")
            except ValueError as exc:
                errors.append(f"AUDIO: scene {number} {exc}")
                continue
            if not path.is_file():
                if require_local_audio:
                    errors.append(f"AUDIO: scene {number} WAV is missing: {path}")
            elif _hash(path) != row.get("sha256"):
                errors.append(f"AUDIO: scene {number} WAV differs from manifest SHA-256")
    return errors


def _speech_intervals(audio: dict) -> tuple[dict[int, list[tuple[str, float, float]]], list[str]]:
    """Reconstruct line windows from the tracked assembly rule, not guessed words."""
    errors: list[str] = []
    rule = audio.get("assembly_rule", {})
    try:
        same = float(rule["pause_same_speaker_seconds"])
        changed = float(rule["pause_speaker_change_seconds"])
        tail = float(rule["tail_silence_seconds_per_scene"])
        if min(same, changed, tail) < 0:
            raise ValueError("negative pause")
    except (KeyError, TypeError, ValueError):
        return {}, ["AUDIO: assembly pauses are missing or invalid"]
    by_scene: dict[int, list[dict]] = {}
    for line in audio.get("lines", []):
        by_scene.setdefault(line["scene"], []).append(line)
    intervals: dict[int, list[tuple[str, float, float]]] = {}
    for scene in audio.get("scenes", []):
        number = scene["scene"]
        lines = by_scene.get(number, [])
        if not lines:
            errors.append(f"AUDIO: scene {number} has no line audio")
            continue
        position = 0.0
        windows = []
        for index, line in enumerate(lines):
            start = round(position, 6)
            duration = line.get("duration_seconds")
            if not isinstance(duration, (int, float)) or duration <= 0:
                errors.append(f"AUDIO: {line.get('id')} has invalid duration")
                continue
            position += duration
            windows.append((line["id"], start, round(position, 6)))
            if index < len(lines) - 1:
                position += same if line["speaker"] == lines[index + 1]["speaker"] else changed
        position += tail
        if abs(position - scene["duration_seconds"]) > 0.005:
            errors.append(f"AUDIO: scene {number} assembly duration differs from scene WAV")
        intervals[number] = windows
    return intervals, errors


def _word_anchor(word_timing: dict | None, scene: int, line_id: str, second: float,
                 audio_hash: str) -> bool:
    if not word_timing or word_timing.get("schema") != WORD_SCHEMA:
        return False
    packet = word_timing.get("scenes", {}).get(str(scene), {})
    if (packet.get("audio_sha256") != audio_hash or not packet.get("reviewer") or
            not packet.get("reviewed_at")):
        return False
    for anchor in packet.get("anchors", []):
        if (anchor.get("line_id") == line_id and
                isinstance(anchor.get("seconds"), (int, float)) and
                abs(anchor["seconds"] - second) <= 0.001 and
                isinstance(anchor.get("word_index"), int) and anchor["word_index"] >= 1 and
                isinstance(anchor.get("word"), str) and anchor["word"].strip()):
            return True
    return False


def preflight(story: str = "lion_and_mouse_v6", root: Path = REPO,
              require_reviews: bool = True, require_local_audio: bool = False,
              work: Path | None = None) -> tuple[dict | None, list[str]]:
    """Return an untimed runtime draft and blockers, without writing files.

    Missing ignored audio is reported only when local bytes are required. If
    present, those bytes are always checked against the tracked hashes.
    """
    if not re.fullmatch(r"[a-z][a-z0-9_]*", story):
        return None, ["STRUCTURE: invalid story slug"]
    root = Path(root).resolve()
    work = Path(work or os.environ.get("FELTWILLOW_WORK", root / "work")).resolve()
    story_dir = root / "stories" / story
    names = ("visual_bible", "audio_manifest", "dialogue_coverage", "keyframe_plan",
             "keyframe_visual_reviews", "video_boundary_plan", "video_boundary_config",
             "staging_plan", "keyframe_regeneration_contract")
    files = {name: story_dir / f"{name}.json" for name in names}
    missing = [f"STRUCTURE: missing {path}" for path in files.values() if not path.is_file()]
    if missing:
        return None, missing
    try:
        data = {name: _read(path) for name, path in files.items()}
    except (ValueError, json.JSONDecodeError) as exc:
        return None, [f"STRUCTURE: {exc}"]
    bible, audio, coverage, keys, reviews, boundaries, config, staging, reference_contract = (
        data[name] for name in names)
    errors: list[str] = []
    for name, value in data.items():
        if name != "keyframe_visual_reviews" and value.get("story") != story:
            errors.append(f"STRUCTURE: {name} belongs to {value.get('story')!r}, expected {story!r}")
    if reviews.get("story") != story:
        errors.append("STRUCTURE: visual reviews belong to another story")
    if (bible.get("version") != "v6" or bible.get("pipeline") != PIPELINE or
            bible.get("asset_revision_policy") != POLICY):
        errors.append("STRUCTURE: visual bible version/pipeline/native-visual policy is incompatible")
    if keys.get("keyframe_count") != len(keys.get("images", [])):
        errors.append("STRUCTURE: keyframe count does not match records")
    images = keys.get("images", [])
    if not isinstance(images, list):
        return None, errors + ["STRUCTURE: keyframe images must be an array"]
    by_id = {row.get("id"): row for row in images if isinstance(row, dict)}
    if len(by_id) != len(images):
        errors.append("STRUCTURE: duplicate or invalid keyframe IDs")
    try:
        rebuilt = build_boundaries(keys, config, staging=staging)
        if rebuilt != boundaries:
            errors.append("STRUCTURE: video_boundary_plan.json differs from the current keyframes/config")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"STRUCTURE: video boundary plan cannot be rebuilt: {exc}")
    line_ids = {row.get("id") for row in audio.get("lines", [])}
    for row in images:
        for field, prefix in (("candidate_path", f"character/characters/{story}"),
                              ("approved_plate", f"character/locations/{story}")):
            try:
                path = _native_path(root, row.get(field, ""), prefix)
                if not path.is_file():
                    errors.append(f"STRUCTURE: {row.get('id')} {field} file is missing")
            except ValueError as exc:
                errors.append(f"STRUCTURE: {row.get('id')} {field}: {exc}")
        if any(lid not in line_ids for lid in row.get("audio_line_ids", [])):
            errors.append(f"STRUCTURE: {row.get('id')} refers to unknown audio lines")
        if not row.get("audio_line_ids"):
            errors.append(f"STRUCTURE: {row.get('id')} has no audio line association")
        if any(next((line.get("scene") for line in audio["lines"] if line.get("id") == lid), None)
               != row.get("scene") for lid in row.get("audio_line_ids", [])):
            errors.append(f"STRUCTURE: {row.get('id')} crosses audio-scene identity")
    if len(boundaries.get("scenes", [])) != len(audio.get("scenes", [])):
        errors.append("STRUCTURE: boundary scene count differs from audio")
    errors.extend(_audio_errors(audio, coverage, root, work, require_local_audio))
    reference_report = validate_reference_contract_report(
        reference_contract, root=root, staging=staging, bible=bible, active_plan=keys)
    errors.extend(f"REFERENCE: {err}" for err in reference_report["current_authority_blockers"])
    _, interval_errors = _speech_intervals(audio)
    errors.extend(interval_errors)
    if require_reviews:
        errors.extend(f"VISUAL: {err}" for err in validate_visual_reviews(
            keys, reviews, root, staging=staging, bible=bible))
    draft = {
        "schema": SCHEMA,
        "story": story,
        "version": bible.get("version"),
        "pipeline": bible.get("pipeline"),
        "asset_revision_policy": bible.get("asset_revision_policy"),
        "audio_source_story": audio.get("source_story"),
        "audio_manifest": f"stories/{story}/audio_manifest.json",
        "keyframe_plan": f"stories/{story}/keyframe_plan.json",
        "visual_reviews": f"stories/{story}/keyframe_visual_reviews.json",
        "video_boundary_plan": f"stories/{story}/video_boundary_plan.json",
        "staging_plan": f"stories/{story}/staging_plan.json",
        "keyframe_regeneration_contract": f"stories/{story}/keyframe_regeneration_contract.json",
        "input_receipts": {name: _hash(path) for name, path in files.items()},
        "historical_provenance_warnings": reference_report["historical_provenance_warnings"],
        "scenes": boundaries.get("scenes", []),
    }
    return draft, errors


def _timed_plan(draft: dict, timing: dict, root: Path,
                word_timing: dict | None = None,
                word_timing_hash: str | None = None) -> tuple[dict | None, list[str]]:
    errors: list[str] = []
    story = draft["story"]
    if timing.get("schema") != TIMING_SCHEMA or timing.get("story") != story:
        return None, ["TIMING: schema or story identity mismatch"]
    story_dir = root / "stories" / story
    keys = _read(story_dir / "keyframe_plan.json")
    reviews = _read(story_dir / "keyframe_visual_reviews.json")
    audio = _read(story_dir / "audio_manifest.json")
    images = {row["id"]: row for row in keys["images"]}
    lines = {row["id"]: row for row in audio["lines"]}
    scenes = {row["scene"]: row for row in audio["scenes"]}
    speech, speech_errors = _speech_intervals(audio)
    if speech_errors:
        return None, speech_errors
    if word_timing and (word_timing.get("schema") != WORD_SCHEMA or
                        word_timing.get("story") != story):
        return None, ["TIMING: reviewed word-timing schema/story mismatch"]
    pieces = timing.get("pieces")
    if not isinstance(pieces, list) or not pieces:
        return None, ["TIMING: pieces must be a nonempty array"]
    ordered: dict[int, list[dict]] = {number: [] for number in scenes}
    used: set[str] = set()
    output: list[dict] = []
    for index, piece in enumerate(pieces, 1):
        if not isinstance(piece, dict):
            errors.append(f"TIMING: piece {index} is not an object")
            continue
        number = piece.get("scene")
        if number not in scenes:
            errors.append(f"TIMING: piece {index} has unknown scene")
            continue
        start_id, end_id = piece.get("start_keyframe"), piece.get("end_keyframe")
        start, end = images.get(start_id), images.get(end_id)
        if not start or not end or end["scene"] != number or start["scene"] not in (number, number - 1):
            errors.append(f"TIMING: piece {index} uses missing/wrong-scene endpoints")
            continue
        boundary = draft["scenes"][number - 1]
        if start["scene"] == number - 1 and start_id != boundary["start_keyframe"]:
            errors.append(f"TIMING: piece {index} does not use the registered shared boundary")
        if end_id not in boundary["ordered_keyframes"]:
            errors.append(f"TIMING: piece {index} end is outside scene chronology")
        a, b = piece.get("start_seconds"), piece.get("end_seconds")
        if (not isinstance(a, (int, float)) or isinstance(a, bool) or
                not isinstance(b, (int, float)) or isinstance(b, bool) or
                a < 0 or b <= a or b > scenes[number]["duration_seconds"] + 0.001):
            errors.append(f"TIMING: piece {index} has invalid audio interval")
            continue
        ids = piece.get("audio_line_ids")
        if not isinstance(ids, list) or any(lid not in lines or lines[lid]["scene"] != number for lid in ids):
            errors.append(f"TIMING: piece {index} has missing/wrong-scene line IDs")
            continue
        overlapping = {lid for lid, speech_start, speech_end in speech[number]
                       if min(b, speech_end) - max(a, speech_start) > 0.001}
        if set(ids) != overlapping or len(ids) != len(set(ids)):
            errors.append(f"TIMING: piece {index} line IDs do not match the exact speech interval")
            continue
        for second in (a, b):
            for lid, speech_start, speech_end in speech[number]:
                if speech_start + 0.001 < second < speech_end - 0.001:
                    if not _word_anchor(word_timing, number, lid, second, scenes[number]["sha256"]):
                        errors.append(f"TIMING: piece {index} cuts inside {lid} at {second:.3f}s without reviewed word-timing evidence")
        mode = piece.get("mouth_mode")
        speakers = {lines[lid]["speaker"] for lid in ids}
        if mode == "silent":
            speaker = None
        elif mode == "character_dialogue" and len(speakers) == 1 and "NARRATOR" not in speakers:
            speaker = next(iter(speakers))
            if (speaker not in start.get("dialogue_speakers", []) or
                    speaker not in end.get("dialogue_speakers", [])):
                errors.append(f"TIMING: piece {index} lip-sync speaker is not staged at both endpoints")
                continue
        else:
            errors.append(f"TIMING: piece {index} has invalid speaker/mouth mode")
            continue
        if start_id != end_id:
            transition = next((item for item in boundary["internal_transitions"]
                               if item["from"] == start_id and item["to"] == end_id), None)
            shared = (boundary["entry"] == "shared_boundary_candidate" and
                      start_id == boundary["start_keyframe"] and end_id == boundary["first_own_keyframe"])
            if not shared and (not transition or transition["kind"] != "same_view_motion_candidate"):
                errors.append(f"TIMING: piece {index} interpolates across an unregistered cut")
                continue
        ordered[number].append(piece)
        used.update((start_id, end_id))
        output.append({
            "id": f"{story}_s{number:02d}_p{len(ordered[number]):03d}",
            "scene": number,
            "audio_track": scenes[number]["path"],
            "audio_sha256": scenes[number]["sha256"],
            "audio_start_seconds": a,
            "audio_end_seconds": b,
            "audio_line_ids": ids,
            "speaker": speaker,
            "mouth_mode": mode,
            "start_keyframe": start_id,
            "start_image": start["candidate_path"],
            "start_sha256": start["sha256"],
            "start_review_sha256": reviews["images"][start_id]["sha256"],
            "end_keyframe": end_id,
            "end_image": end["candidate_path"],
            "end_sha256": end["sha256"],
            "end_review_sha256": reviews["images"][end_id]["sha256"],
            "boundary_kind": "hold" if start_id == end_id else "same_view_motion",
            "entry_kind": ("scene_cut" if boundary["entry"] == "cut" else "shared_boundary")
            if not ordered[number][:-1] else "shared_endpoint",
        })
    for number, group in ordered.items():
        if not group:
            errors.append(f"TIMING: scene {number} has no pieces")
            continue
        if group != sorted(group, key=lambda row: row["start_seconds"]):
            errors.append(f"TIMING: scene {number} pieces are out of chronological order")
        boundary = draft["scenes"][number - 1]
        cursor = 0.0
        represented_lines: set[str] = set()
        previous = None
        for piece in group:
            if abs(piece["start_seconds"] - cursor) > 0.001:
                errors.append(f"TIMING: scene {number} has a gap/overlap at {cursor:.3f}s")
            cursor = piece["end_seconds"]
            represented_lines.update(piece["audio_line_ids"])
            if previous is not None and previous["end_keyframe"] != piece["start_keyframe"]:
                join = next((item for item in boundary["internal_transitions"]
                             if item["from"] == previous["end_keyframe"] and
                             item["to"] == piece["start_keyframe"]), None)
                if join is None or join["kind"] == "same_view_motion_candidate":
                    errors.append(f"TIMING: scene {number} jumps between unconnected endpoints")
                else:
                    output_piece = next(row for row in output if row["scene"] == number and
                                        row["audio_start_seconds"] == piece["start_seconds"])
                    output_piece["entry_kind"] = join["kind"]
            previous = piece
        if abs(cursor - scenes[number]["duration_seconds"]) > 0.001:
            errors.append(f"TIMING: scene {number} does not cover the complete WAV")
        expected_lines = {lid for lid, row in lines.items() if row["scene"] == number}
        if represented_lines != expected_lines:
            errors.append(f"TIMING: scene {number} does not cover every audio line")
        character_lines = {lid for lid in expected_lines if lines[lid]["speaker"] != "NARRATOR"}
        lipsynced_lines = {lid for row in output if row["scene"] == number and
                           row["mouth_mode"] == "character_dialogue"
                           for lid in row["audio_line_ids"]}
        if not character_lines.issubset(lipsynced_lines):
            errors.append(f"TIMING: scene {number} has character dialogue without a staged lip-sync piece")
        expected = set(boundary["ordered_keyframes"])
        if not expected.issubset(used):
            errors.append(f"TIMING: scene {number} leaves keyframes unused: {sorted(expected - used)}")
        if group[0]["start_keyframe"] != draft["scenes"][number - 1]["start_keyframe"]:
            errors.append(f"TIMING: scene {number} does not start at its registered boundary")
        if group[-1]["end_keyframe"] != draft["scenes"][number - 1]["last_keyframe"]:
            errors.append(f"TIMING: scene {number} does not end at its registered boundary")
    if errors:
        return None, errors
    plan = {key: value for key, value in draft.items() if key != "scenes"}
    plan.update({
        "status": "validated_hash_bound_runtime_inputs",
        "timing_schema": TIMING_SCHEMA,
        "timing_sha256": hashlib.sha256(json.dumps(timing, sort_keys=True,
                                                 separators=(",", ":")).encode()).hexdigest(),
        "reviewed_word_timing_sha256": word_timing_hash,
        "scenes": draft["scenes"],
        "pieces": output,
    })
    return plan, []


def export(story: str, timing_file: Path, root: Path = REPO,
           work: Path | None = None,
           word_timing_file: Path | None = None) -> tuple[Path | None, list[str]]:
    """Validate all inputs before atomically writing a runtime plan."""
    root = Path(root).resolve()
    work = Path(work or os.environ.get("FELTWILLOW_WORK", root / "work")).resolve()
    draft, errors = preflight(story, root, require_reviews=True,
                              require_local_audio=True, work=work)
    if errors:
        return None, errors
    try:
        timing = _read(Path(timing_file))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return None, [f"TIMING: cannot read explicit piece timing: {exc}"]
    word_timing = None
    word_hash = None
    if word_timing_file is not None:
        try:
            word_timing_file = Path(word_timing_file)
            word_timing = _read(word_timing_file)
            word_hash = _hash(word_timing_file)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            return None, [f"TIMING: cannot read reviewed word timing: {exc}"]
    plan, errors = _timed_plan(draft, timing, root, word_timing, word_hash)
    if errors:
        return None, errors
    target = root / "stories" / story / "runtime_plan.json"
    encoded = (json.dumps(plan, indent=2, ensure_ascii=False) + "\n").encode()
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".runtime-plan-",
                                     suffix=".json", delete=False) as handle:
        temporary = Path(handle.name)
        try:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    temporary.replace(target)
    return target, []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story", default="lion_and_mouse_v6")
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("--preflight", action="store_true")
    operation.add_argument("--export", action="store_true")
    parser.add_argument("--timing", type=Path, help="explicit reviewed video-piece timing JSON for --export")
    parser.add_argument("--word-timing", type=Path,
                        help="reviewed, scene-WAV-hash-bound word anchors for cuts inside spoken lines")
    args = parser.parse_args()
    if args.export and args.timing is None:
        parser.error("--export requires --timing")
    if args.preflight:
        draft, errors = preflight(args.story)
        warnings = (draft or {}).get("historical_provenance_warnings", [])
        if warnings:
            print(f"HISTORICAL PROVENANCE WARNINGS (not readiness blockers): {len(warnings)}")
            for warning in warnings[:10]:
                print("WARN:", warning)
            if len(warnings) > 10:
                print(f"...and {len(warnings) - 10} more")
        if errors:
            for error in errors[:25]:
                print("BLOCKED:", error)
            if len(errors) > 25:
                print(f"...and {len(errors) - 25} more")
            print(f"{len(errors)} blockers; no files written")
            return 1
        print("Preflight passed; no files written. Export still requires explicit piece timing.")
        return 0
    target, errors = export(args.story, args.timing, word_timing_file=args.word_timing)
    if errors:
        for error in errors[:25]:
            print("BLOCKED:", error)
        if len(errors) > 25:
            print(f"...and {len(errors) - 25} more")
        print(f"{len(errors)} blockers; no files written")
        return 1
    print(f"Exported {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
