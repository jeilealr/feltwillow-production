"""CPU static plates with explicit FFmpeg provenance; never a claim of action."""

from pathlib import Path
import shutil
import subprocess
import sys
import numpy as np
from PIL import Image
from feltwillow import wan


def executable(name):
    found = shutil.which(name)
    private = Path(sys.executable).parent / name
    if found:
        return found
    if private.is_file():
        return str(private)
    raise ValueError(name + " executable unavailable; no installation attempted")


def static_frames(source, width, height, frames):
    if isinstance(frames, bool) or not isinstance(frames, int) or frames <= 0:
        raise ValueError("positive integer static frame count required")
    with Image.open(source) as im:
        wan.fitted_record(im, width, height)  # reject unexpected alpha
        frame = wan.fit(im, width, height)
    return [frame] * frames


def save(frames, output, fps=16):
    output = Path(output)
    if output.exists():
        raise ValueError("refusing to overwrite local video")
    first = np.asarray(frames[0], dtype=np.uint8)
    height, width = first.shape[:2]
    argv = [
        executable("ffmpeg"),
        "-v",
        "error",
        "-nostdin",
        "-n",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{width}x{height}",
        "-r",
        str(fps),
        "-i",
        "pipe:0",
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(output),
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    with subprocess.Popen(argv, stdin=subprocess.PIPE) as process:
        try:
            for frame in frames:
                pixels = np.asarray(frame, dtype=np.uint8)
                if pixels.shape != first.shape:
                    raise ValueError("local frame size changed")
                process.stdin.write(pixels.tobytes())
        finally:
            process.stdin.close()
        if process.wait():
            raise ValueError("FFmpeg static encoding failed")


def bounded_frames(source, width, height, frames, effect):
    """Blend a reviewed same-canvas edit inside a protected mask only.

    This is a local 2D treatment, not a claim of physically simulated action.
    First/last weights must be zero; exposed surfaces are never reconstructed.
    """
    if isinstance(frames, bool) or not isinstance(frames, int) or frames <= 0:
        raise ValueError("positive integer local frame count required")
    import hashlib

    def checked(ref):
        path = Path(ref["path"])
        if (
            not path.is_file()
            or hashlib.sha256(path.read_bytes()).hexdigest() != ref["sha256"]
        ):
            raise ValueError("bounded effect input unavailable or changed")
        return path

    review = effect.get("review", {})
    if review.get("status") != "pass" or not review.get("reviewer"):
        raise ValueError("bounded local effect requires reviewed mask and source")
    if (
        review.get("source_sha256")
        != hashlib.sha256(Path(source).read_bytes()).hexdigest()
        or review.get("target_sha256") != effect["target"]["sha256"]
        or review.get("mask_sha256") != effect["mask"]["sha256"]
    ):
        raise ValueError("bounded effect review hashes stale")
    weights = effect.get("frame_weights")
    if (
        not isinstance(weights, list)
        or len(weights) != frames
        or any(
            isinstance(v, bool)
            or not isinstance(v, (int, float))
            or not np.isfinite(v)
            or not 0 <= v <= 1
            for v in weights
        )
        or weights[0] != 0
        or weights[-1] != 0
    ):
        raise ValueError(
            "bounded effect requires explicit finite frame weights and resting boundaries"
        )
    import json

    weights_sha = hashlib.sha256(
        json.dumps(weights, separators=(",", ":")).encode()
    ).hexdigest()
    if review.get("frame_weights_sha256") != weights_sha:
        raise ValueError("bounded effect temporal weights changed after review")
    with (
        Image.open(source) as im,
        Image.open(checked(effect["target"])) as target,
        Image.open(checked(effect["mask"])) as mask,
    ):
        if (
            target.size != im.size
            or mask.size != im.size
            or target.mode != "RGB"
            or mask.mode != "L"
        ):
            raise ValueError(
                "bounded local inputs require identical native canvas RGB target and L mask"
            )
        wan.fitted_record(im, width, height)
        original = np.asarray(im.convert("RGB"))
        edited = np.asarray(target)
        alpha = np.asarray(mask) / 255.0
        if np.any(original[alpha == 0] != edited[alpha == 0]):
            raise ValueError("local target changes protected pixels outside mask")
        result = []
        for amount in weights:
            pixels = np.rint(
                original * (1 - alpha[..., None] * amount)
                + edited * alpha[..., None] * amount
            ).astype(np.uint8)
            result.append(wan.fit(Image.fromarray(pixels), width, height))
    return result
