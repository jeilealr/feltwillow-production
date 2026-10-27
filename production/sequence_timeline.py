"""Sample-authoritative preview timelines with one cumulative frame quantization.

This module does not select takes or authorize final assembly. Every trim/retime
and generated-video join must be reviewed explicitly before preview rendering.
"""

from __future__ import annotations
import argparse, json, hashlib, math, subprocess, wave
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from production.sequence_plan import digest, fingerprint
from production.sequence_export import atomic
from feltwillow.local_video import executable, save
from PIL import Image
import numpy as np


def quantize(sample, rate, fps):
    return round(Fraction(sample * fps, rate))


def valid_mapping_review(review, source, mapping, target):
    return bool(
        review.get("reviewer")
        and review.get("status") == "pass"
        and review.get("source_sha256") == source["sha256"]
        and review.get("mapping_sha256")
        == fingerprint({k: v for k, v in mapping.items() if not k.endswith("_review")})
        and review.get("target_sha256") == fingerprint(target)
    )


def join_digest(left, right, sample_rate, fps):
    def state(row):
        return dict(
            source_sha256=row["source"]["sha256"],
            kind=row["kind"],
            source_mapping={
                k: v
                for k, v in row.get("source_mapping", {}).items()
                if not k.endswith("_review")
            },
            start_sample=row["start_sample"],
            end_sample=row["end_sample"],
            frame_start=row["frame_start"],
            frame_end=row["frame_end"],
        )

    return fingerprint(
        dict(
            left=state(left),
            right=state(right),
            sample_rate=sample_rate,
            fps=fps,
            policy="keep_declared_frame_cells",
        )
    )


def compile_timeline(intervals, sample_rate, total_samples, fps=16, audio=None):
    for value in (sample_rate, total_samples, fps):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError("positive integer sample/rate/frame facts required")
    cursor = 0
    rows = []
    used = set()
    for row in intervals:
        row = dict(row)
        if (
            any(
                isinstance(row.get(k), bool) or not isinstance(row.get(k), int)
                for k in ("start_sample", "end_sample")
            )
            or row.get("start_sample") != cursor
            or row["end_sample"] <= cursor
        ):
            raise ValueError("timeline gap, overlap or invalid sample interval")
        identity = row.get("id")
        if not identity or identity in used:
            raise ValueError("unique editorial interval identity required")
        used.add(identity)
        if row.get("kind") not in {"static_hold", "video"}:
            raise ValueError(
                "explicit static_hold/video interval kind required; cuts are boundary metadata"
            )
        source = row.get("source", {})
        path = Path(source.get("path", ""))
        if not path.is_file() or digest(path) != source.get("sha256"):
            raise ValueError("timeline source unavailable or stale")
        first = quantize(cursor, sample_rate, fps)
        last = quantize(row["end_sample"], sample_rate, fps)
        if last <= first:
            raise ValueError("interval too short for a distinct frame cell")
        row.update(frame_start=first, frame_end=last, frame_cells=last - first)
        if row["kind"] == "video":
            mapping = row.get("source_mapping", {})
            count = mapping.get("frame_count")
            start = mapping.get("start_frame", 0)
            if (
                not isinstance(count, int)
                or isinstance(count, bool)
                or count <= 0
                or isinstance(start,bool)
                or not isinstance(start, int)
                or start < 0
            ):
                raise ValueError("video requires explicit source frame window")
            if (
                not row.get("whole_motion_review", {}).get("reviewer")
                or row["whole_motion_review"].get("source_sha256") != source["sha256"]
                or row["whole_motion_review"].get("status") != "pass"
            ):
                raise ValueError("whole-motion review missing/stale")
            target = {
                "start_sample": row["start_sample"],
                "end_sample": row["end_sample"],
                "sample_rate": sample_rate,
                "fps": fps,
                "frame_start": first,
                "frame_end": last,
            }
            if mapping.get("frame_count") != row[
                "frame_cells"
            ] and not valid_mapping_review(
                mapping.get("retime_review", {}), source, mapping, target
            ):
                raise ValueError("retime requires explicit reviewed mapping")
            probe = subprocess.run(
                [
                    executable("ffprobe"),
                    "-v",
                    "error",
                    "-select_streams",
                    "v:0",
                    "-count_frames",
                    "-show_entries",
                    "stream=nb_read_frames,r_frame_rate",
                    "-of",
                    "json",
                    str(path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            streams = json.loads(probe.stdout)["streams"]
            if len(streams) != 1:
                raise ValueError("missing/ambiguous source video stream")
            facts = streams[0]
            actual_count = int(facts["nb_read_frames"])
            actual_fps = Fraction(facts["r_frame_rate"])
            if start + count > actual_count:
                raise ValueError("source frame window exceeds decoded video")
            if Fraction(count, 1) / actual_fps != Fraction(
                row["frame_cells"], fps
            ) and not valid_mapping_review(
                mapping.get("retime_review", {}), source, mapping, target
            ):
                raise ValueError("source FPS/duration change requires reviewed retime")
            row["decoded_source"] = {
                "frame_count": actual_count,
                "fps": str(actual_fps),
            }
            if (
                start
                or start + count != actual_count
                or mapping.get("trimmed_end_frames", 0)
            ):
                if not valid_mapping_review(
                    mapping.get("trim_review", {}), source, mapping, target
                ):
                    raise ValueError("trim requires actual contact/word review")
        if (
            rows
            and row.get("boundary") != "cut"
            and (row["kind"] == "video" or rows[-1]["kind"] == "video")
        ):
            join = row.get("join_review", {})
            if (
                join.get("status") != "pass"
                or not join.get("reviewer")
                or join.get("source_sha256s")
                != [rows[-1]["source"]["sha256"], source["sha256"]]
                or join.get("join_sha256")
                != join_digest(rows[-1], row, sample_rate, fps)
            ):
                raise ValueError(
                    "continuous video join requires actual native/decoded boundary review"
                )
        cursor = row["end_sample"]
        rows.append(row)
    if cursor != total_samples:
        raise ValueError("timeline does not cover whole PCM master exactly once")
    audio_facts = None
    if audio:
        path = Path(audio["path"])
        if digest(path) != audio["sha256"]:
            raise ValueError("audio master changed")
        with wave.open(str(path)) as wav:
            if wav.getnframes() != total_samples or wav.getframerate() != sample_rate:
                raise ValueError("audio master sample facts mismatch")
        audio_facts = dict(audio)
    result = dict(
        schema="feltwillow.editorial-timeline.v1",
        sample_rate=sample_rate,
        total_samples=total_samples,
        fps=fps,
        frame_cells=quantize(total_samples, sample_rate, fps),
        intervals=rows,
        audio=audio_facts,
        final_assembly_authorized=False,
        owner_take_selection="not granted by timeline",
    )
    result["dependency_sha256"] = fingerprint(result)
    return result


def render_preview(timeline, output, width, height):
    check = {k: v for k, v in timeline.items() if k != "dependency_sha256"}
    if fingerprint(check) != timeline.get("dependency_sha256"):
        raise ValueError("timeline changed after compilation")
    from feltwillow import wan

    frames = []
    for row in timeline["intervals"]:
        source = Path(row["source"]["path"])
        if digest(source) != row["source"]["sha256"]:
            raise ValueError("preview source changed")
        if row["kind"] == "static_hold":
            with Image.open(source) as im:
                wan.fitted_record(im, width, height)
                frame = wan.fit(im, width, height)
            frames.extend([frame] * row["frame_cells"])
        else:
            import cv2

            cap = cv2.VideoCapture(str(source))
            decoded = []
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                decoded.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            cap.release()
            mapping = row["source_mapping"]
            start = mapping.get("start_frame", 0)
            count = mapping["frame_count"]
            if len(decoded) < start + count:
                raise ValueError("source clip too short or corrupt")
            for i in range(row["frame_cells"]):
                index = start + min(count - 1, (i * count) // row["frame_cells"])
                if decoded[index].size != (width, height):
                    raise ValueError(
                        "video preview may not silently crop/resize a take"
                    )
                frames.append(decoded[index])
    output = Path(output)
    if output.exists():
        raise ValueError("preview destination already exists")
    # Store silent native edit separately; never overwrite source clips.
    silent = output.with_name(output.stem + ".silent.mp4")
    save(frames, silent, timeline["fps"])
    audio = timeline.get("audio")
    if audio:
        if digest(audio["path"]) != audio["sha256"]:
            raise ValueError("preview audio changed")
        subprocess.run(
            [
                executable("ffmpeg"),
                "-v",
                "error",
                "-nostdin",
                "-n",
                "-i",
                str(silent),
                "-i",
                audio["path"],
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                str(output),
            ],
            check=True,
        )
    else:
        output = silent
    receipt = dict(
        schema="feltwillow.preview-receipt.v1",
        timeline_sha256=timeline["dependency_sha256"],
        output=str(output),
        output_sha256=digest(output),
        frames=len(frames),
        audio=audio,
        visual_review="pending",
        owner_selection="pending",
        final_assembly_authorized=False,
    )
    atomic(output.with_suffix(".json"), (json.dumps(receipt, indent=2) + "\n").encode())
    return receipt


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    source = json.loads(a.source.read_text())
    result = compile_timeline(**source)
    atomic(a.out, (json.dumps(result, indent=2) + "\n").encode())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
