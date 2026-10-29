"""Portable inventory tests; real-media verification is a separate integration check."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from production.lumi_s01_s08_inputs import build, sha, verify


class LumiInputTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        story = self.root / "stories/lion_and_mouse_v7"
        story.mkdir(parents=True)
        self.still = self.root / "images/forest.png"
        self.still.parent.mkdir()
        self.still.write_bytes(b"forest pixels")
        self.wav = self.root / "voice/line.wav"
        self.wav.parent.mkdir()
        self.wav.write_bytes(b"PCM")
        self.meta = self.root / "voice/line.json"
        self.meta.write_text("{}")
        self.row = {"image_id": "S01-L001-B01-I01", "path": "images/forest.png",
                    "sha256": sha(self.still), "selection_record": {"path": "owner.json", "sha256": "a" * 64}}
        plan = {"lines": [{"line_id": "S01-L001", "speaker": "NARRATOR", "text": "forest",
                           "audio": {"wav": "voice/line.wav", "sha256": sha(self.wav),
                                     "metadata": "voice/line.json", "metadata_sha256": sha(self.meta),
                                     "sample_count": 3, "sample_rate_hz": 16000}}],
                "visual_units": {"s01_empty_hold": {"audio_line_ids": ["S01-L001"]}},
                "production_sequences": {"s01_empty_hold": {"uses": [{"id": "u1",
                    "image_id": "S01-L001-B01-I01", "source": {"path": self.row["path"],
                    "sha256": self.row["sha256"]}}], "edges": []}}}
        (story / "audio_visual_plan.json").write_text(json.dumps(plan))
        self.transfer = story / "handoff/lumi_s01_s08/AUDIO_FILES.txt"
        self.transfer.parent.mkdir(parents=True)
        self.transfer.write_text("voice/line.wav\n")

    def inventory(self, rows=None):
        with patch("production.lumi_s01_s08_inputs.selection_catalog",
                   return_value=[self.row] if rows is None else rows):
            return build(self.root)

    def checked(self, data, rows=None):
        with patch("production.lumi_s01_s08_inputs.selection_catalog",
                   return_value=[self.row] if rows is None else rows):
            return verify(self.root, data)

    def test_selection_authority_freshness(self):
        data = self.inventory()
        self.assertEqual(self.checked(data), [])
        changed = dict(self.row, selection_record={"path": "owner.json", "sha256": "b" * 64})
        self.assertTrue(self.checked(data, [changed]))
        self.assertEqual(self.inventory(rows=[])["sequences"]["s01_empty_hold"]["uses"][0]
                         ["source_status"], "explicit_source_unapproved")
        conflicting = dict(self.row, path="images/other.png", sha256="b" * 64)
        self.assertEqual(self.inventory(rows=[self.row, conflicting])["sequences"]["s01_empty_hold"]
                         ["uses"][0]["source_status"], "ambiguous_authority")

    def test_changed_media_paths_and_transfer_list(self):
        data = self.inventory()
        self.still.write_bytes(b"tampered")
        self.assertIn("images/forest.png", self.checked(data))
        self.still.write_bytes(b"forest pixels")
        self.wav.write_bytes(b"bad PCM")
        self.assertIn("voice/line.wav", self.checked(data))
        self.wav.write_bytes(b"PCM")
        for bad in ("../outside.png", "/tmp/outside.png"):
            altered = copy.deepcopy(data)
            altered["sequences"]["s01_empty_hold"]["uses"][0]["source"]["path"] = bad
            self.assertTrue(any("unsafe" in error for error in self.checked(altered)))
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        external = Path(outside.name) / "outside.png"
        external.write_bytes(b"forest pixels")
        (self.root / "images/escape.png").symlink_to(external)
        altered = copy.deepcopy(data)
        altered["sequences"]["s01_empty_hold"]["uses"][0]["source"]["path"] = "images/escape.png"
        self.assertTrue(any("escapes" in error for error in self.checked(altered)))
        self.transfer.write_text("voice/line.wav\nvoice/extra.wav\n")
        self.assertTrue(any("AUDIO_FILES" in error for error in self.checked(data)))

    def test_v1_requires_rebuild(self):
        data = self.inventory()
        data["schema"] = "feltwillow.lumi-s01-s08-inputs.v1"
        self.assertTrue(any("stale" in error for error in self.checked(data)))


if __name__ == "__main__":
    unittest.main()
