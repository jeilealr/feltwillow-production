"""Tests for deriving deterministic compositor inputs from staging."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from production import keyframe_plan
from production.keyframe_staging_recipe import parse_actor_source, resolve_staged_recipe


class KeyframeStagingRecipeTests(unittest.TestCase):
    def test_upper_body_camera_aim_keeps_physical_ground_contact_below_crop(self):
        frame = {"actors": {"leo": {"contact_xy_on_plate": [0.52, 0.83]}},
                 "camera_center_xy_on_plate": [0.52, 0.49]}
        left, top, width, height = keyframe_plan.crop_for_frame(frame, 3.4)
        self.assertAlmostEqual(left + width / 2, 0.52, places=4)
        self.assertAlmostEqual(top + height / 2, 0.49, places=4)
        self.assertGreater((0.83 - top) / height, 1)
        self.assertEqual(frame["actors"]["leo"]["contact_xy_on_plate"], [0.52, 0.83])

    def test_keyframe_cli_help_does_not_require_image_runtime_dependencies(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run([sys.executable, str(root / "production/keyframe.py"), "--help"],
                                cwd=root, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--write-edit-mask", result.stdout)
        self.assertIn("--blur", result.stdout)

    def test_parse_actor_source_and_flip(self):
        actor, source = parse_actor_source("milo=poses/milo.png,flip")
        self.assertEqual(actor, "milo")
        self.assertEqual(source, {"still": "poses/milo.png", "flip": True})
        with self.assertRaises(ValueError):
            parse_actor_source("milo=poses/milo.png,unknown")

    def test_frame_id_derives_crop_contact_and_anatomy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            story = root / "stories/test"
            story.mkdir(parents=True)
            frame = {"id": "s01_p01", "plate": "plate.png", "view": "medium_solo",
                     "camera_focus": "registered_plate_focus", "size_anchor_id": "tree_wide_milo",
                     "actors": {"milo": {"contact_xy_on_plate": [0.55, 0.65],
                                           "standing_equivalent_height_fraction_after_crop": 0.4}}}
            staging = {"views": {"medium_solo": {"magnification": 2.0,
                                                   "background_focus": "soft_blur",
                                                   "blur_sigma_px": 2.0}},
                       "frames": [frame]}
            (story / "staging_plan.json").write_text(json.dumps(staging))
            recipe = resolve_staged_recipe("test", "s01_p01", ["milo=poses/milo.png"], root)
            expected_crop = keyframe_plan.crop_for_frame(frame, 2.0)
            self.assertEqual(recipe["crop_rect_on_plate"], expected_crop)
            left, top, width, height = expected_crop
            self.assertAlmostEqual(recipe["characters"][0]["x"], (0.55 - left) / width)
            self.assertAlmostEqual(recipe["characters"][0]["y"], (0.65 - top) / height)
            self.assertEqual(recipe["characters"][0]["h"], 0.4)
            self.assertEqual(recipe["size_anchor_id"], "tree_wide_milo")
            self.assertEqual(recipe["blur_sigma_px"], 2.0)

    def test_staged_character_inputs_must_match_cast(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            story = root / "stories/test"
            story.mkdir(parents=True)
            (story / "staging_plan.json").write_text(json.dumps({
                "views": {"wide": {"magnification": 1.0}},
                "frames": [{"id": "s01_p01", "plate": "plate.png", "view": "wide",
                            "actors": {}}]}))
            with self.assertRaisesRegex(ValueError, "actors must match staging exactly"):
                resolve_staged_recipe("test", "s01_p01", ["milo=poses/milo.png"], root)


if __name__ == "__main__":
    unittest.main()
