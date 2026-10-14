"""Supplementary review sheets must not silently outlive their active source."""

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from production.check_keyframe_review import validate_material_comparison


class MaterialComparisonTests(unittest.TestCase):
    def test_trial_sheet_is_hash_bound_to_active_source_and_trial(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sheets = root / "current"
            sheets.mkdir()
            source = root / "source.png"
            trial = root / "trial.png"
            source.write_bytes(b"current image")
            trial.write_bytes(b"trial image")
            (sheets / "material_color_comparison.png").write_bytes(b"sheet")
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            trial_hash = hashlib.sha256(trial.read_bytes()).hexdigest()
            plan = {"images": [{"id": "s05x_p04", "candidate_path": "source.png",
                                "sha256": source_hash}]}
            manifest = {"entries": [{"frame_id": "s05x_p04",
                                     "source_path": "source.png", "source_sha256": source_hash,
                                     "trial_path": "trial.png", "trial_sha256": trial_hash}]}
            (sheets / "material_color_comparison.json").write_text(json.dumps(manifest))
            self.assertEqual(validate_material_comparison(plan, root, sheets), [])

            source.write_bytes(b"new active image")
            self.assertIn("s05x_p04: material comparison source bytes are missing or stale",
                          validate_material_comparison(plan, root, sheets))


if __name__ == "__main__":
    unittest.main()
