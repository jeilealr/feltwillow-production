"""CPU-only retained call trace. Synthetic colors are never production media.

Run this harness, not its frozen renderer commands. The Wan loader and endpoint
capability are patched only inside this process; no framework is imported.
"""

import io
import argparse
import json
import runpy
import shutil
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from tests.test_sequence_pipeline import SequencePipelineTests
from production import sequence_export, shot
from production.sequence_plan import digest
from feltwillow import wan


def main():
    folder = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=folder / "cpu_fixture_r003")
    args = parser.parse_args()
    out = args.out.resolve()
    if out.exists():
        trace = out / "TRACE.json"
        if not trace.is_file():
            raise SystemExit(
                "Partial fixture exists; inspect it before choosing a fresh revision"
            )
        prior = json.loads(trace.read_text())
        hashes = prior.get("implementation_sha256", {})
        if not hashes or any(
            digest(ROOT / name) != sha for name, sha in hashes.items()
        ):
            raise SystemExit(
                "Fixture code is stale; preserve it and choose a fresh unused --out"
            )
        if not all((out / (label + ".png")).is_file() for label in "ABC"):
            raise SystemExit(
                "Retained fixture input bytes unavailable; restore them or choose a new revision"
            )
        from feltwillow.render_receipt import inspect_render

        for receipt in (out / "work/runs/fixture/shots").glob("*.json"):
            result = inspect_render(
                receipt.with_suffix(".mp4"), json.loads(receipt.read_text())
            )
            if result[0] != "complete":
                raise SystemExit(
                    "Retained fixture output unavailable/stale: " + str(result)
                )
        print("Verified retained CPU fixture; no calls repeated:", trace)
        return
    case = SequencePipelineTests()
    case.setUp()
    try:
        shutil.copytree(case.root, out)
        case.root = out
        packet = case.packet()
        manifest = sequence_export.compile_packet(
            packet, out, out / "packet", "fixture", case.recipe
        )
        calls = []

        def generate(pipe, prompt, **kwargs):
            from PIL import Image

            a = wan.fit(kwargs["image"], 32, 32)
            b = wan.fit(kwargs["last_image"], 32, 32)
            calls.append(
                dict(
                    start_pixel=list(a.getpixel((0, 0))),
                    end_pixel=list(b.getpixel((0, 0))),
                    prompt=prompt,
                    seed=kwargs["seed"],
                    backend="synthetic RGB blend; no Wan",
                )
            )
            return [Image.blend(a, b, i / 4) for i in range(5)]

        def save(frames, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                [
                    str(Path(sys.executable).parent / "ffmpeg"),
                    "-v",
                    "error",
                    "-f",
                    "rawvideo",
                    "-pix_fmt",
                    "rgb24",
                    "-s",
                    "32x32",
                    "-r",
                    "16",
                    "-i",
                    "pipe:0",
                    "-frames:v",
                    "5",
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    str(path),
                ],
                input=b"".join(frame.tobytes() for frame in frames),
                check=True,
                capture_output=True,
            )

        captured = io.StringIO()
        with (
            patch.object(shot.paths, "story_work", return_value=out / "work"),
            patch.object(wan, "load", return_value=object()),
            patch.object(
                wan,
                "endpoint_capability",
                return_value=dict(
                    endpoint_supported=True,
                    source_sha256="fixture-not-installed-runtime",
                ),
            ),
            patch.object(
                wan, "verify_endpoint_environment", return_value=dict(synthetic=True)
            ),
            patch.object(wan, "generate", side_effect=generate),
            patch.object(wan, "save", side_effect=save),
            redirect_stdout(captured),
        ):
            for command in manifest["commands"]:
                with (
                    patch.object(sys, "argv", command["argv"][1:]),
                    patch.object(sys, "path", sys.path.copy()),
                ):
                    runpy.run_path(command["argv"][1], run_name="__main__")
        expected = [([255, 0, 0], [0, 128, 0]), ([0, 128, 0], [0, 0, 255])]
        if [(c["start_pixel"], c["end_pixel"]) for c in calls] != expected:
            raise AssertionError("intermediate lost")
        (out / "execution.log").write_text(captured.getvalue())
        (out / "TRACE.json").write_text(
            json.dumps(
                dict(
                    scope="synthetic_cpu_fixture_only",
                    implementation_sha256={
                        name: digest(ROOT / name)
                        for name in [
                            "production/shot.py",
                            "feltwillow/wan.py",
                            "feltwillow/render_receipt.py",
                            "production/sequence_plan.py",
                            "production/sequence_readiness.py",
                            "production/sequence_export.py",
                            "production/sequence_review.py",
                            "tests/test_sequence_pipeline.py",
                        ]
                    },
                    commands=manifest["commands"],
                    calls=calls,
                    model_loads=0,
                    gpu_jobs=0,
                    paid_requests=0,
                    real_media_readiness=False,
                ),
                indent=2,
            )
            + "\n"
        )
        print(out / "TRACE.json")
    finally:
        case.temp.cleanup()


if __name__ == "__main__":
    main()
