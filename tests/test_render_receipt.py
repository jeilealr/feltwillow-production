"""Receipt and work-root checks that run without GPU or production media."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from feltwillow.render_receipt import inspect_render
from production import render_story_inventory


class RenderReceiptTests(unittest.TestCase):
    def test_existing_clip_needs_matching_sidecar(self):
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary) / "shot_s1_fast.mp4"
            out.write_bytes(b"clip")
            expected = {"keyframe_sha256": "good", "model": "model@revision",
                        "lightning": {"revision": "new"}, "steps": 4, "seed": 1}
            self.assertEqual(inspect_render(out, expected)[0], "stale")
            out.with_suffix(".json").write_text(json.dumps(
                {**expected, "keyframe_sha256": "bad"}))
            self.assertIn("keyframe_sha256", inspect_render(out, expected)[1])
            out.with_suffix(".json").write_text(json.dumps(
                {**expected, "model": "model@old"}))
            self.assertIn("model", inspect_render(out, expected)[1])
            out.with_suffix(".json").write_text(json.dumps(
                {**expected, "steps": 40}))
            self.assertIn("steps", inspect_render(out, expected)[1])
            out.with_suffix(".json").write_text(json.dumps(
                {**expected, "lightning": {"revision": "old"}}))
            self.assertIn("lightning", inspect_render(out, expected)[1])
            out.with_suffix(".json").write_text(json.dumps(expected))
            self.assertEqual(inspect_render(out, expected), ("complete", None))

    def test_missing_clip_is_missing(self):
        self.assertEqual(inspect_render(Path("/no/such/render.mp4"), {}),
                         ("missing", None))

    def test_partial_seeds_queue_only_missing_shot(self):
        fake_story = {"scenes": {1: {"shots": [{"name": "one", "seeds": [1, 2]},
                                             {"name": "two", "seeds": [3]}]}}}
        fake_yaml = type("Yaml", (), {"safe_load": staticmethod(lambda _: fake_story)})
        results = [
            {"story": "sample", "scene": 1, "shot": "one", "seeds": [
                {"seed": 1, "output": "one_s1_fast.mp4", "status": "complete", "reason": None},
                {"seed": 2, "output": "one_s2_fast.mp4", "status": "missing", "reason": None}]},
            {"story": "sample", "scene": 1, "shot": "two", "seeds": [
                {"seed": 3, "output": "two_s3_fast.mp4", "status": "complete", "reason": None}]},
        ]
        with tempfile.TemporaryDirectory() as temporary, \
             patch.dict("sys.modules", {"yaml": fake_yaml}), \
             patch.object(render_story_inventory.paths, "STORIES", Path(temporary)), \
             patch.object(render_story_inventory.subprocess, "run",
                          side_effect=[subprocess.CompletedProcess([], 0, json.dumps(x), "")
                                       for x in results]):
            story_file = Path(temporary) / "sample" / "story.yaml"
            story_file.parent.mkdir()
            story_file.write_text("fixture")
            inventory = render_story_inventory.inventory_story("sample")
        self.assertEqual(inventory["counts"], {"complete": 2, "missing": 1, "stale": 0})
        self.assertEqual(len(inventory["commands"]), 1)
        self.assertIn("--shot one", inventory["commands"][0])

    def test_backup_dry_run_uses_overridden_work_root(self):
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            (work / "stories" / "sample").mkdir(parents=True)
            (work / "stories" / "sample" / "clip.mp4").write_bytes(b"clip")
            env = {**os.environ, "FELTWILLOW_WORK": str(work)}
            result = subprocess.run(["bash", str(repo / "lumi" / "backup_assets.sh"),
                                     "--dry-run"], env=env, cwd=repo, text=True,
                                    capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"work root: {work.resolve()} (1 files)", result.stdout)
        self.assertIn("dry run: no persistent lists written", result.stdout)

    def test_backup_lists_files_relative_to_external_work_root(self):
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            asset = work / "stories" / "sample" / "clip.mp4"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"clip")
            env = {**os.environ, "FELTWILLOW_WORK": str(work)}
            result = subprocess.run(["bash", str(repo / "lumi" / "backup_assets.sh")],
                                    env=env, cwd=repo, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            files = (work / "backup_work_files.txt").read_text().splitlines()
            self.assertEqual(files, ["stories/sample/clip.mp4"])
            self.assertIn(f"--files-from=:{work.resolve()}/backup_work_files.txt",
                          result.stdout)

    def test_render_inventory_files_follow_overridden_work_root(self):
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            work = base / "external-work"
            bin_dir = base / "bin"
            bin_dir.mkdir()
            python_stub = bin_dir / "python3"
            python_stub.write_text("""#!/bin/bash
if [ "$1" = "-c" ]; then exec "$REAL_PYTHON" "$@"; fi
if [ "$1" = "production/render_story_inventory.py" ]; then
  shift
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --output) output=$2; shift 2 ;;
      --commands) commands=$2; shift 2 ;;
      *) shift ;;
    esac
  done
  printf '{"counts":{"complete":0,"missing":0,"stale":0}}\n' > "$output"
  : > "$commands"
  exit 0
fi
exit 99
""")
            python_stub.chmod(0o755)
            env = {**os.environ, "FELTWILLOW_WORK": str(work),
                   "REAL_PYTHON": sys.executable,
                   "PATH": f"{bin_dir}:{os.environ['PATH']}"}
            result = subprocess.run(["bash", str(repo / "lumi" / "render_story.sh"),
                                     "sample", "--inventory-only"],
                                    env=env, cwd=repo, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f"FELTWILLOW_WORK={work.resolve()}", result.stdout)
            self.assertTrue((work / "tasks" / "sample_render_inventory.json").is_file())
            self.assertTrue((work / "tasks" / "sample_commands.txt").is_file())

    def test_bulk_driver_stops_before_submission_on_stale_inventory(self):
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            bin_dir = base / "bin"
            bin_dir.mkdir()
            python_stub = bin_dir / "python3"
            python_stub.write_text("""#!/bin/bash
if [ "$1" = "-c" ]; then exec "$REAL_PYTHON" "$@"; fi
if [ "$1" = "production/render_story_inventory.py" ]; then
  echo "stale render" >&2
  exit 2
fi
exit 99
""")
            python_stub.chmod(0o755)
            sbatch = bin_dir / "sbatch"
            sbatch.write_text(f"#!/bin/bash\ntouch '{base / 'submitted'}'\n")
            sbatch.chmod(0o755)
            env = {**os.environ, "FELTWILLOW_WORK": str(base / "work"),
                   "REAL_PYTHON": sys.executable,
                   "PATH": f"{bin_dir}:{os.environ['PATH']}"}
            result = subprocess.run(["bash", str(repo / "lumi" / "render_story.sh"),
                                     "sample"], env=env, cwd=repo, text=True,
                                    capture_output=True)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse((base / "submitted").exists())


if __name__ == "__main__":
    unittest.main()
