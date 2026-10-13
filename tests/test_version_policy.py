"""Runtime namespace and recorded source provenance are separate contracts."""

import json
import unittest
from pathlib import Path

from feltwillow.version_policy import require_story_local_audio


ROOT = Path(__file__).resolve().parents[1]


class VersionPolicyTests(unittest.TestCase):
    def test_v6_runtime_audio_is_local_even_with_v5_provenance(self):
        manifest = json.loads(
            (ROOT / "stories/lion_and_mouse_v6/audio_manifest.json").read_text()
        )
        self.assertEqual(manifest["story"], "lion_and_mouse_v6")
        self.assertEqual(manifest["source_story"], "lion_and_mouse_v5")
        self.assertIs(manifest["owner_authorized_reuse"], True)
        self.assertEqual(len(manifest["lines"]), 161)
        for line in manifest["lines"]:
            self.assertTrue(line["v6_path"].startswith("work/stories/lion_and_mouse_v6/"))
            self.assertTrue(line["source_path"].startswith("work/the_lion_and_the_mouse/"))
            self.assertRegex(line["sha256"], r"^[0-9a-f]{64}$")
        require_story_local_audio(manifest["story"], manifest["story"])

        with self.assertRaisesRegex(SystemExit, "runtime namespace"):
            require_story_local_audio(manifest["story"], manifest["source_story"])

