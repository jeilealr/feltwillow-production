"""Scene-specific style authority is carried into future generation prompts."""

import unittest
import json
from pathlib import Path

from production.keyframe_plan import build


class KeyframeSceneStyleTests(unittest.TestCase):
    def test_scene_05_uses_s05_p01_style_without_borrowing_its_composition(self):
        plan = build("lion_and_mouse_v6")
        frames = {row["id"]: row for row in plan["images"]}
        standard = frames["s05_p01"]
        bible = json.loads((Path(__file__).resolve().parents[1] /
                            "stories/lion_and_mouse_v6/visual_bible.json").read_text())
        style_master = bible["scene_style_standards"]["5"]["standard_frame"]["path"]
        self.assertFalse(any(ref["role"] == "style_reference"
                             for ref in standard["reference_roles"]))

        for frame_id in ("s05_p02", "s05_p03", "s05_p04", "s05x_p04"):
            row = frames[frame_id]
            styles = [ref for ref in row["reference_roles"]
                      if ref["role"] == "style_reference"]
            self.assertEqual(len(styles), 1, frame_id)
            self.assertEqual(styles[0]["derived_from_path"], style_master)
            self.assertIn("brightness", styles[0]["authority_scope"])
            self.assertIn("no character pigment", styles[0]["authority_scope"])
            self.assertIn("character fiber density or scale", styles[0]["authority_scope"])
            self.assertIn("environment_swatch", styles[0]["path"])
            self.assertIn("SCENE STYLE LOCK:", row["prompt"])
            self.assertIn("Do not copy shapes or layout from the swatch", row["prompt"])
            self.assertIn("canonical controls intrinsic coat and mane pigment", row["prompt"])

        self.assertFalse(any(ref["role"] == "style_reference"
                             for ref in frames["s06_p01"]["reference_roles"]))

    def test_canonical_material_controls_all_leo_and_milo_frames(self):
        plan = build("lion_and_mouse_v6")
        for row in plan["images"]:
            for actor in row["actors"]:
                self.assertIn(
                    f"{actor.title()} must match the registered {actor.title()} canonical exactly",
                    row["prompt"], row["id"])
                self.assertIn("canonical also controls the intrinsic felt pigment", row["prompt"])
                self.assertIn("Do not recolor the whole character to match a sunset", row["prompt"])


if __name__ == "__main__":
    unittest.main()
