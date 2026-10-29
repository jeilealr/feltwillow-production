"""LUMI handoff is derived from current exact-hash still and audio authority."""

import json
import unittest
from pathlib import Path

from production.lumi_s01_s08_inputs import build, verify


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "stories/lion_and_mouse_v7/handoff/lumi_s01_s08/INPUT_MAP.json"


class LumiInputTests(unittest.TestCase):
    def test_current_map_and_transfer_inventory(self):
        recorded = json.loads(MAP.read_text())
        self.assertEqual(build(ROOT), recorded)
        self.assertEqual(verify(ROOT, recorded), [])
        self.assertEqual(len(recorded["audio_lines"]), 68)
        self.assertNotIn("s01_opening", recorded["sequences"])
        self.assertEqual(recorded["sequences"]["s01_empty_hold"]["edges"][0]["kind"], "hold")
        self.assertEqual(recorded["sequences"]["s02_line_002"]["edges"][0]["kind"], "hold")
        transfer = (MAP.parent / "AUDIO_FILES.txt").read_text().splitlines()
        self.assertEqual(transfer, sorted(row["wav"] for row in recorded["audio_lines"].values()))

    def test_missing_wav_is_reported(self):
        recorded = json.loads(MAP.read_text())
        first = next(iter(recorded["audio_lines"].values()))
        first["wav"] = "voice/narration/lion_and_mouse_v7/en/r001/lines/DOES-NOT-EXIST.wav"
        self.assertIn(first["wav"], verify(ROOT, recorded))


if __name__ == "__main__":
    unittest.main()
