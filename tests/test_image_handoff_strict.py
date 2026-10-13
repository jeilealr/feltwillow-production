"""A readiness audit must exit nonzero when an image still awaits approval."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from production import image_handoff


class HandoffStrictTests(unittest.TestCase):
    def test_strict_gate_blocks_pending_scene(self):
        manifest = {"images": [{"id": "frame", "prompt_kind": "scene",
                                "status": "planned", "setup": "wide",
                                "ordered_references": []}]}
        bible = {"setups": {"wide": {"framing": "scene_wide"}}}
        with patch.object(image_handoff, "load", return_value=(manifest, bible, {})):
            with patch("sys.argv", ["image_handoff.py", "--story", "fixture", "audit", "--strict"]):
                with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as failure:
                    image_handoff.main()
                self.assertEqual(failure.exception.code, 1)
            with patch("sys.argv", ["image_handoff.py", "--story", "fixture", "audit"]):
                with redirect_stdout(io.StringIO()):
                    image_handoff.main()


if __name__ == "__main__":
    unittest.main()
