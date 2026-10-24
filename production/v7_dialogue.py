"""V7-native, exact-audio tracked-mouth packets without legacy story manifests.

No command downloads models, generates audio, invokes a provider or submits GPU
work. Real word alignments, take selection and mouth calibration remain separate
reviewed inputs. The compositor approximates word opening pulses, not phonemes.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import wave

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
from PIL import Image

from feltwillow import mouth_tracking
from feltwillow.portrait_qa import assess_frames, region_mask
from production.sequence_take import selected_source

SCHEMA = "feltwillow.v7-dialogue-operation.v1"
ACTORS = {"MOUSE": "Milo", "LION": "Leo"}
CODE_FILES = ("production/v7_dialogue.py", "feltwillow/mouth_tracking.py", "feltwillow/portrait_qa.py")


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def local(root, name):
    path = (Path(root) / name).resolve()
    if not path.is_relative_to(Path(root).resolve()):
        raise ValueError("dialogue reference escapes repository")
    return path


def file_ref(root, ref):
    if not isinstance(ref, dict) or not ref.get("path") or not ref.get("sha256"):
        raise ValueError("missing exact file reference")
    path = local(root, ref["path"])
    if not path.is_file() or digest(path) != ref["sha256"]:
        raise ValueError("dialogue reference unavailable or changed: " + str(path))
    return path


def integer(value, label, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(label + " must be an integer in range")
    return value


def audio_record(line, root):
    audio = line["audio"]
    path = file_ref(root, dict(path=audio["wav"], sha256=audio["sha256"]))
    meta_path = file_ref(root, dict(path=audio["metadata"], sha256=audio["metadata_sha256"]))
    metadata = json.loads(meta_path.read_text())
    if metadata.get("text") != line["text"] or metadata.get("speaker") != line["speaker"]:
        raise ValueError("line transcript/speaker differs from its actual audio metadata")
    with wave.open(str(path)) as wav:
        count, rate = wav.getnframes(), wav.getframerate()
    if count != audio["sample_count"] or rate != audio["sample_rate_hz"]:
        raise ValueError("WAV sample facts differ from authored source")
    return dict(line_id=line["line_id"], speaker=line["speaker"], transcript=line["text"], wav=dict(path=audio["wav"], sha256=audio["sha256"]), metadata=dict(path=audio["metadata"], sha256=audio["metadata_sha256"]), sample_count=count, sample_rate=rate)


def scene_offsets(plan, scene_id):
    cursor, previous, offsets = 0, None, {}
    scene_rate = None
    for line in (l for l in plan["lines"] if l["audio_scene"] == scene_id):
        rate = integer(line["audio"]["sample_rate_hz"], "sample rate", 1)
        if scene_rate is not None and rate != scene_rate:
            raise ValueError("mixed scene sample rates require a reviewed conversion")
        scene_rate = rate
        if previous is not None:
            cursor += rate * (45 if previous == line["speaker"] else 70) // 100
        offsets[line["line_id"]] = cursor
        cursor += integer(line["audio"]["sample_count"], "sample count", 1)
        previous = line["speaker"]
    return offsets


def reviewed_words(line, alignment, root):
    if alignment.get("status") != "reviewed" or not alignment.get("reviewer"):
        raise ValueError(line["line_id"] + ": word timing requires a reviewer")
    for key, expected in (("audio_sha256", line["wav"]["sha256"]), ("metadata_sha256", line["metadata"]["sha256"]), ("transcript", line["transcript"]), ("speaker", line["speaker"]), ("sample_rate", line["sample_rate"])):
        if alignment.get(key) != expected:
            raise ValueError(line["line_id"] + ": stale/mismatched word " + key)
    words, cursor = [], 0
    for word in alignment.get("words", []):
        start = integer(word["start_sample"], "word start")
        end = integer(word["end_sample"], "word end", 1)
        if not start < end <= line["sample_count"] or start < cursor or not isinstance(word.get("text"), str) or not word["text"].strip():
            raise ValueError("invalid, overlapping or out-of-range word interval")
        words.append(dict(text=word["text"], start_sample=start, end_sample=end))
        cursor = end
    if not words:
        raise ValueError("speaking line has no reviewed words")
    expected = re.findall(r"[\w']+", line["transcript"].casefold())
    actual = [token for word in words for token in re.findall(r"[\w']+", word["text"].casefold())]
    if expected != actual:
        raise ValueError("alignment omits/reorders transcript words; review required")
    return words


def calibration_arrays(calibration, mapping, actor, root):
    if calibration.get("actor") != actor or calibration.get("purpose") != "speech_calibration":
        raise ValueError("calibration actor/purpose mismatch (bite references are not speech calibration)")
    for field in ("view", "camera_and_crop_lock"):
        if not mapping.get(field) or calibration.get(field) != mapping[field]:
            raise ValueError("incompatible calibration " + field)
    if calibration.get("no_teeth_design") is not True:
        raise ValueError("toothless calibration design required")
    closed_path = file_ref(root, calibration.get("closed_base"))
    open_path = file_ref(root, calibration.get("open_candidate"))
    for name in ("owner_selection", "anatomy_review"):
        review = calibration.get(name, {})
        expected_status = "selected" if name == "owner_selection" else "pass"
        if review.get("status") != expected_status or not review.get("reviewer") or review.get("closed_sha256") != calibration["closed_base"]["sha256"] or review.get("open_sha256") != calibration["open_candidate"]["sha256"]:
            raise ValueError("exact closed/open " + name + " is missing or stale")
    if calibration["owner_selection"].get("scope") != "mouth_calibration":
        raise ValueError("scene or pose approval cannot select a mouth calibration")
    with Image.open(closed_path) as im:
        if im.mode not in {"RGB", "RGBA"} or ("A" in im.getbands() and im.getchannel("A").getextrema() != (255, 255)):
            raise ValueError("mouth calibration requires opaque scene-matched pixels")
        closed = np.asarray(im.convert("RGB"))
    with Image.open(open_path) as im:
        if "A" in im.getbands() and im.getchannel("A").getextrema() != (255, 255):
            raise ValueError("transparent mouth calibration requires explicit composition first")
        opened = np.asarray(im.convert("RGB"))
    if closed.shape != opened.shape or closed.shape[:2] != (mapping["height"], mapping["width"]):
        raise ValueError("calibration size differs; no head resizing fallback")
    roi = calibration["mouth_roi_normalized"]
    allowed = region_mask(closed.shape, roi)
    changed = np.any(closed != opened, axis=2)
    if np.any(changed & ~allowed):
        raise ValueError("calibration changes pixels outside mouth ROI (view/lighting/geometry mismatch)")
    if not changed.any():
        raise ValueError("open calibration has no mouth difference")
    motion_region = region_mask(closed.shape, mapping["allowed_mouth_motion_roi"])
    if np.any(allowed & ~motion_region):
        raise ValueError("mouth ROI is outside the reviewed motion envelope")
    return closed, opened, changed.astype(np.float32), roi, motion_region


def compile_dialogue(plan, unit_id, selected_takes, calibrations, alignments, mapping, root):
    """Compile one selected V7 source piece; no legacy manifests or model calls."""
    root = Path(root).resolve()
    unit = copy.deepcopy(plan.get("visual_units", {}).get(unit_id))
    if unit is None:
        raise ValueError("unknown authored V7 visual unit")
    if unit.get("status") == "blocked":
        raise ValueError("authored visual unit is blocked")
    if selected_takes.get("story") != plan["story"]:
        raise ValueError("take ledger belongs to another story")
    piece = mapping["source_piece"]
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", piece):
        raise ValueError("invalid source piece ID")
    source, identity = selected_source(selected_takes, piece)
    receipt_path = source.with_suffix(".json")
    receipt = json.loads(receipt_path.read_text())
    count = integer(mapping["frame_count"], "frame count", 3)
    width, height = integer(mapping["width"], "width", 1), integer(mapping["height"], "height", 1)
    fps, rate = integer(mapping["fps"], "fps", 1), integer(mapping["sample_rate"], "sample rate", 1)
    if width * height * count * 3 > 512 * 1024 * 1024:
        raise ValueError("source exceeds bounded local decode memory; split the reviewed operation")
    for key, value in (("frames", count), ("width", width), ("height", height), ("fps", fps)):
        if receipt.get(key) != value:
            raise ValueError("source receipt differs from frame mapping: " + key)
    review = mapping.get("review", {})
    if review.get("status") != "reviewed" or not review.get("reviewer") or review.get("source_sha256") != identity["source_sha256"] or review.get("frame_mapping_sha256") != fingerprint(mapping["frame_scene_samples"]):
        raise ValueError("reviewed source-to-scene mapping missing or stale")
    quality = mapping.get("source_review", {})
    if quality.get("source_sha256") != identity["source_sha256"] or quality.get("status") != "pass" or not quality.get("reviewer") or any(quality.get(k) is not True for k in ("closed_boundaries", "teeth_absent", "whole_clip_watched")):
        raise ValueError("selected source must have closed boundaries and reviewed toothless full motion")
    if unit.get("composition") == "portrait" and quality.get("portrait_no_intrusion") is not True:
        raise ValueError("portrait_intrusion: raw source needs review/repair before mouth compositing")
    if mapping.get("boundary_mouth") != "closed":
        raise ValueError("open dialogue boundary is forbidden; open calibration is auxiliary only")
    samples = mapping["frame_scene_samples"]
    if len(samples) != count or any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in samples) or any(a >= b for a, b in zip(samples, samples[1:])):
        raise ValueError("one strictly increasing scene-sample position is required per source frame")
    line_by_id = {line["line_id"]: line for line in plan["lines"]}
    ids = unit["audio_line_ids"]
    if not ids or len(ids) != len(set(ids)) or any(lid not in line_by_id for lid in ids):
        raise ValueError("unknown/duplicate dialogue line IDs")
    lines = [line_by_id[lid] for lid in ids]
    scene_ids = {line["audio_scene"] for line in lines}
    if len(scene_ids) != 1:
        raise ValueError("one dialogue operation cannot cross scene masters")
    scene = next(iter(scene_ids))
    offsets = scene_offsets(plan, scene)
    audio_hashes = {line["line_id"]: line["audio"]["sha256"] for line in lines}
    if review.get("audio_sha256s") != audio_hashes:
        raise ValueError("source mapping was reviewed against other line audio")
    actor = mapping.get("actor")
    if actor is None and unit.get("mouth_policy") == "dialogue_lipsync" and any(ACTORS.get(line["speaker"]) in unit.get("visible_cast", []) for line in lines):
        raise ValueError("visible dialogue requires an explicit named mouth actor")
    if actor is not None and actor not in unit.get("visible_cast", []):
        raise ValueError("mouth actor is offscreen")
    if mapping.get("camera_and_crop_lock") != unit.get("camera_and_crop_lock"):
        raise ValueError("source crop differs from authored portrait family")
    cues, records, exclusions = [], [], []
    for raw in lines:
        line = audio_record(raw, root)
        if line["sample_rate"] != rate:
            raise ValueError("mixed audio sample rates require an explicit reviewed conversion")
        line["scene_start_sample"] = offsets[line["line_id"]]
        line["scene_end_sample"] = line["scene_start_sample"] + line["sample_count"]
        if line["speaker"] not in {"NARRATOR", "MOUSE", "LION"}:
            raise ValueError("unknown V7 speaker")
        visible_speaker = ACTORS.get(line["speaker"])
        if unit.get("composition") == "portrait" and visible_speaker in unit.get("visible_cast", []) and unit.get("mouth_policy") != "dialogue_lipsync":
            raise ValueError("speaking portrait is missing dialogue_lipsync policy")
        reason = None
        if line["speaker"] == "NARRATOR":
            reason = "narrator_never_drives_mouth"
        elif visible_speaker != actor:
            reason = "other_or_offscreen_speaker"
        elif unit.get("mouth_policy") != "dialogue_lipsync":
            reason = "no_dialogue_driver"
        if reason:
            exclusions.append(dict(line_id=line["line_id"], reason=reason))
        else:
            words = reviewed_words(line, alignments.get(line["line_id"], {}), root)
            for word in words:
                cues.append(dict(line_id=line["line_id"], speaker=line["speaker"], actor=actor, text=word["text"], start_sample=line["scene_start_sample"] + word["start_sample"], end_sample=line["scene_start_sample"] + word["end_sample"]))
        records.append(line)
    if samples[0] < records[0]["scene_start_sample"] or samples[-1] >= records[-1]["scene_end_sample"] + rate:
        raise ValueError("frame mapping escapes the declared line scope/tail")
    calibration = None
    if cues:
        calibration = copy.deepcopy(calibrations.get(mapping.get("calibration_id")))
        if calibration is None:
            raise ValueError("selected same-view toothless calibration unavailable")
        calibration_arrays(calibration, mapping, actor, root)
    portrait = mapping.get("portrait_contract")
    if unit.get("composition") == "portrait":
        if not portrait or portrait.get("source_sha256") != identity["source_sha256"]:
            raise ValueError("reviewed portrait ROI/protected geometry contract required")
    packet = dict(schema=SCHEMA, story=plan["story"], unit_id=unit_id, visual_unit=unit, scene=scene, source=dict(path=str(source), sha256=identity["source_sha256"], receipt_path=str(receipt_path), receipt_sha256=digest(receipt_path), piece=piece, **identity), selected_takes=copy.deepcopy(selected_takes), mapping=copy.deepcopy(mapping), audio=records, cues=cues, exclusions=exclusions, calibration=calibration, alignment_sha256=fingerprint(alignments), source_plan_scope_sha256=fingerprint(dict(unit=unit, lines=lines)), code_sha256={name: digest(ROOT / name) for name in CODE_FILES}, method="tracked-mouth-delta" if cues else "no_mouth_driver_pass_through", post_sync_review="pending", owner_selection="pending", assembly_authorized=False)
    packet["packet_sha256"] = fingerprint(packet)
    return packet


def validate_packet(packet, root):
    if packet.get("schema") != SCHEMA:
        raise ValueError("unsupported V7 dialogue packet")
    copy_packet = dict(packet)
    expected = copy_packet.pop("packet_sha256", None)
    if fingerprint(copy_packet) != expected:
        raise ValueError("dialogue packet changed after compilation")
    for name, sha in packet["code_sha256"].items():
        if digest(ROOT / name) != sha:
            raise ValueError("mouth implementation changed; recompile/review")
    source, _ = selected_source(packet["selected_takes"], packet["source"]["piece"])
    if str(source) != packet["source"]["path"] or digest(source.with_suffix(".json")) != packet["source"]["receipt_sha256"]:
        raise ValueError("selected source receipt changed")
    for line in packet["audio"]:
        file_ref(root, line["wav"])
        meta_path = file_ref(root, line["metadata"])
        meta = json.loads(meta_path.read_text())
        if meta.get("text") != line["transcript"] or meta.get("speaker") != line["speaker"]:
            raise ValueError("cached dialogue audio metadata differs")
    if packet["calibration"] is not None:
        calibration_arrays(packet["calibration"], packet["mapping"], packet["mapping"]["actor"], root)


def activations(packet):
    """Broad word pulses at exact mapped samples; silence/other voices stay zero."""
    amounts = []
    for sample in packet["mapping"]["frame_scene_samples"]:
        amount = 0.0
        for word in packet["cues"]:
            if word["start_sample"] <= sample < word["end_sample"]:
                phase = (sample - word["start_sample"]) / (word["end_sample"] - word["start_sample"])
                amount = max(amount, math.sin(math.pi * phase) ** 2)
        amounts.append(amount)
    amounts[0] = amounts[-1] = 0.0
    return amounts


def process_frames(packet, frames, root):
    """Run real bounded tracking; return lossless arrays and explicit diagnostics."""
    validate_packet(packet, root)
    frames = np.asarray(frames)
    mapping = packet["mapping"]
    if frames.dtype != np.uint8 or frames.shape != (mapping["frame_count"], mapping["height"], mapping["width"], 3):
        raise ValueError("decoded source geometry differs from reviewed mapping")
    portrait_report = None
    if packet["visual_unit"].get("composition") == "portrait":
        portrait_report = assess_frames(frames[0], frames, mapping["portrait_contract"])
        if portrait_report["warnings"]:
            raise ValueError("portrait_intrusion/crop warning requires source review: " + json.dumps(portrait_report["warnings"]))
    amounts = activations(packet)
    if packet["calibration"] is None:
        output = frames.copy()
        tracking = dict(version=mouth_tracking.VERSION, frames=[dict(frame=n, status="unchanged", amount=0.) for n in range(len(frames))], rejected_active_frames=0)
    else:
        closed, opened, mask, roi, motion_region = calibration_arrays(packet["calibration"], mapping, mapping["actor"], root)
        output, tracking = mouth_tracking.composite_frames(frames, closed, opened, mask, roi, amounts)
        if np.any(output[:, ~motion_region] != frames[:, ~motion_region]):
            raise mouth_tracking.TrackingError("tracked mouth escaped the reviewed motion ROI")
    inactive = [n for n, value in enumerate(amounts) if value == 0 or n in (0, len(frames) - 1)]
    if not np.array_equal(output[inactive], frames[inactive]):
        raise AssertionError("silent/boundary frame preservation failed")
    report = dict(method=packet["method"], packet_sha256=packet["packet_sha256"], frame_scene_samples=mapping["frame_scene_samples"], activation=amounts, tracking=tracking, portrait=portrait_report, raw_inactive_frames_pixel_identical=True, raw_boundary_frames_pixel_identical=True, codec_pixel_equality="not claimed", post_sync_review="pending", owner_selection="pending", assembly_authorized=False)
    return output, report


def ffmpeg_binary():
    import shutil
    path = Path(sys.executable).parent / "ffmpeg"
    binary = str(path) if path.is_file() else shutil.which("ffmpeg")
    if not binary:
        raise ValueError("FFmpeg unavailable; no encoding was performed")
    return binary


def apply_packet(packet, root, output_dir, frames=None):
    """Apply one immutable CPU post-sync operation; encode only after all QA."""
    validate_packet(packet, root)
    out = Path(output_dir).resolve()
    marker = out / "dialogue_receipt.json"
    if out.exists():
        if not marker.is_file():
            raise ValueError("partial dialogue operation exists; reconcile instead of overwriting")
        old = json.loads(marker.read_text())
        if old.get("packet_sha256") != packet["packet_sha256"] or not (out / "dialogue.mp4").is_file() or digest(out / "dialogue.mp4") != old.get("output_sha256"):
            raise ValueError("stale dialogue operation destination")
        return old
    if frames is None:
        # Private conda ffmpeg is made available only to this subprocess helper.
        mapping = packet["mapping"]
        raw = subprocess.run([ffmpeg_binary(), "-v", "error", "-i", packet["source"]["path"], "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], check=True, capture_output=True).stdout
        frames = np.frombuffer(raw, np.uint8).reshape(-1, mapping["height"], mapping["width"], 3)
    output, report = process_frames(packet, frames, root)
    binary = ffmpeg_binary()
    out.mkdir(parents=True, exist_ok=False)
    for label, frame in (("first", output[0]), ("last", output[-1])):
        Image.fromarray(frame).save(out / ("native_" + label + ".png"))
    video = out / "dialogue.mp4"
    if packet["method"] == "no_mouth_driver_pass_through":
        shutil.copyfile(packet["source"]["path"], video)
    else:
        subprocess.run([binary, "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{output.shape[2]}x{output.shape[1]}", "-r", str(packet["mapping"]["fps"]), "-i", "pipe:0", "-an", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(video)], input=output.tobytes(), check=True, capture_output=True)
    receipt = dict(report, stage="v7_tracked_mouth", story=packet["story"], unit_id=packet["unit_id"], source=packet["source"], fps=packet["mapping"]["fps"], frames=len(output), output_path=str(video), output_sha256=digest(video), native_boundaries={label:dict(path=str(out / ("native_" + label + ".png")), sha256=digest(out / ("native_" + label + ".png")), origin="decoded_source_then_bounded_mouth_preencode") for label in ("first", "last")})
    (out / "operation.json").write_text(json.dumps(packet, indent=2) + "\n")
    marker.write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


def inventory(plan, calibrations):
    rows = []
    byline = {line["line_id"]:line for line in plan["lines"]}
    for uid, unit in plan.get("visual_units", {}).items():
        lines = [byline[lid] for lid in unit["audio_line_ids"]]
        if unit.get("mouth_policy") != "dialogue_lipsync":
            continue
        rows.append(dict(unit_id=uid, camera_and_crop_lock=unit.get("camera_and_crop_lock"), lines=[dict(line_id=l["line_id"], speaker=l["speaker"], audio_sha256=l["audio"]["sha256"], mouth_driver=l["speaker"] != "NARRATOR") for l in lines], calibration_ids=[k for k, v in calibrations.items() if v.get("camera_and_crop_lock") == unit.get("camera_and_crop_lock")], status="needs_selected_source_take_and_reviewed_alignment_calibration"))
    return dict(schema="feltwillow.v7-dialogue-inventory.v1", units=rows, whisperx_installed=importlib.util.find_spec("whisperx") is not None, cached_alignment_model_verified=False, alignment_execution="not run; no download permitted", video_review="pending")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    inv = commands.add_parser("inventory")
    inv.add_argument("--story", required=True)
    inv.add_argument("--calibrations", type=Path)
    comp = commands.add_parser("compile")
    for name in ("story", "unit"):
        comp.add_argument("--" + name, required=True)
    for name in ("takes", "calibrations", "alignments", "mapping", "out"):
        comp.add_argument("--" + name, type=Path, required=True)
    apply = commands.add_parser("apply")
    apply.add_argument("packet", type=Path)
    apply.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "apply":
            result = apply_packet(json.loads(args.packet.read_text()), args.root, args.out)
        else:
            plan = json.loads((args.root / "stories" / args.story / "audio_visual_plan.json").read_text())
            calibration_path = args.calibrations or args.root / "stories" / args.story / "character_performance_library.json"
            calibrations = json.loads(calibration_path.read_text())
            calibrations = calibrations.get("mouth_references", {} if "assets" in calibrations else calibrations)
            if args.command == "inventory":
                result = inventory(plan, calibrations)
            else:
                result = compile_dialogue(plan, args.unit, json.loads(args.takes.read_text()), calibrations, json.loads(args.alignments.read_text()), json.loads(args.mapping.read_text()), args.root)
                if args.out.exists():
                    raise ValueError("dialogue packet destination already exists")
                args.out.parent.mkdir(parents=True, exist_ok=True)
                args.out.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        parser.exit(1, "V7_DIALOGUE_BLOCKED: " + str(error) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
