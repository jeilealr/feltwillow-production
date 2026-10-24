"""Read-only validation of a rendered clip against its recorded inputs."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path


def inspect_render(out: Path, expected: dict) -> tuple[str, str | None]:
    """Return (complete|missing|stale, reason); never modify existing media."""
    if not out.is_file():
        return "missing", None
    sidecar = out.with_suffix(".json")
    try:
        recorded = json.loads(sidecar.read_text())
    except (OSError, ValueError) as error:
        return "stale", f"no readable render sidecar: {error}"
    if not isinstance(recorded, dict):
        return "stale", "render sidecar is not a JSON object"
    changed = [key for key, value in expected.items() if recorded.get(key) != value]
    if changed:
        return "stale", "stale or unrecorded render inputs: " + ", ".join(changed)
    if expected.get("run_id"):
        if recorded.get("output_sha256") != hashlib.sha256(out.read_bytes()).hexdigest():
            return "stale", "output bytes differ from the sequence receipt"
        boundaries = recorded.get("native_boundaries")
        if not isinstance(boundaries, dict) or set(boundaries) != {"first", "last"}:
            return "stale", "native boundary capture is incomplete"
        for boundary in boundaries.values():
            if not isinstance(boundary, dict) or not boundary.get("path") or not boundary.get("sha256"):
                return "stale", "malformed native boundary"
            source = Path(boundary["path"])
            if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != boundary["sha256"]:
                return "stale", "native boundary is missing or changed"
    if expected.get("run_id"):
        status, reason = inspect_media(out, expected)
        if status != "passed":return "stale", reason
    return "complete", None


def inspect_media(out: Path, expected: dict | None = None) -> tuple[str, str | None]:
    """Fully decode independently of receipt matching; never grant visual approval."""
    import shutil
    import subprocess
    import sys
    from fractions import Fraction

    def binary(name):
        private = Path(sys.executable).parent / name
        found = str(private) if private.is_file() else shutil.which(name)
        if not found:raise ValueError(f"{name} unavailable for decode verification")
        return found
    try:
        probe=subprocess.run([binary('ffprobe'),'-v','error','-count_frames','-select_streams','v:0',
                              '-show_entries','stream=width,height,r_frame_rate,nb_read_frames','-of','json',str(out)],
                             check=True,capture_output=True,text=True,timeout=60)
        streams=json.loads(probe.stdout)['streams']
        if len(streams)!=1:return 'failed','missing or ambiguous video stream'
        stream=streams[0];count=int(stream['nb_read_frames'])
        if count<1:return 'failed','no decoded frames'
        if expected:
            for key in ('width','height'):
                if stream[key]!=expected[key]:return 'failed','decoded size differs from receipt'
            if count!=expected['frames']:return 'failed','decoded frame count differs from receipt'
            if Fraction(stream['r_frame_rate'])!=Fraction(str(expected['fps'])):return 'failed','decoded frame rate differs from receipt'
        subprocess.run([binary('ffmpeg'),'-v','error','-xerror','-i',str(out),'-map','0:v:0','-f','null','-'],
                       check=True,capture_output=True,timeout=60)
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as error:
        return 'failed',f'video decode failed: {error}'
    return 'passed',None
