"""Depth and ground-placement checks for reusable scene staging contracts."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from production import image_prompts, keyframe_plan, staging_contract


class StagingContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        story = staging_contract.REPO / "stories" / "lion_and_mouse_v6"
        cls.contract = json.loads((story / "staging_plan.json").read_text())
        cls.bible = json.loads((story / "visual_bible.json").read_text())

    def test_v6_all_panels_have_grounded_depth_sizes(self):
        self.assertEqual(staging_contract.validate_contract(self.contract, self.bible), [])
        self.assertEqual(len(self.contract["frames"]), self.bible["scene_coverage"]["panel_count"])

    def test_v6_cast_ratio_and_trap_prompt_survive_regeneration(self):
        ratio = self.contract["cast_scale"]["same_depth_standing_equivalent_height_ratio"]["milo_to_leo"]
        self.assertEqual(ratio["standing_equivalent_height"], 0.25)
        plan = {row["id"]: row for row in keyframe_plan.build("lion_and_mouse_v6")["images"]}
        for frame_id in ("s10_p01", "s10_p02"):
            self.assertIn("hunter_net", " ".join(plan[frame_id]["references"]))
            self.assertIn("trigger loop", plan[frame_id]["prompt"])
            self.assertNotIn("Leo remains trapped", plan[frame_id]["prompt"])
        self.assertIn("looks surprised", plan["s10_p03"]["prompt"])

    def test_small_movement_cannot_make_an_actor_jump_in_size(self):
        broken = copy.deepcopy(self.contract)
        actor = broken["frames"][0]["actors"]["milo"]
        actor["standing_equivalent_height_fraction_after_crop"] += 0.12
        errors = staging_contract.validate_contract(broken, self.bible)
        self.assertTrue(any("height must follow cast scale, depth and camera crop" in e for e in errors))

    def test_contact_outside_walkable_ground_fails(self):
        broken = copy.deepcopy(self.contract)
        broken["frames"][0]["actors"]["milo"]["contact_xy_on_plate"] = [0.9, 0.82]
        errors = staging_contract.validate_contract(broken, self.bible)
        self.assertTrue(any("outside walkable zone" in e for e in errors))

    def test_scene_image_needs_matching_staging_frame(self):
        errors = staging_contract.validate_contract(self.contract, self.bible,
                                                    required_frame_ids=["missing_scene_start"])
        self.assertTrue(any("has no staging frame" in e for e in errors))

    def test_new_story_scaffolds_staging_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            template = root / "stories" / "template"
            template.mkdir(parents=True)
            (template / "visual_bible.json").write_text(json.dumps({
                "blocks": {"style": "felt"}, "generic_blocks": ["style"],
                "reference_roles": {}, "lint": {}
            }))
            with patch.object(image_prompts, "REPO", root):
                created = image_prompts.new_story("next_fable_v1", "template")
            bible = json.loads((created / "visual_bible.json").read_text())
            contract = json.loads((created / "staging_plan.json").read_text())
            self.assertEqual(bible["staging_contract"], "stories/next_fable_v1/staging_plan.json")
            self.assertEqual(contract["cast_scale"], bible["cast_scale"])
            self.assertEqual(contract["frames"], [])
            boundaries = json.loads((created / "video_boundary_config.json").read_text())
            reviews = json.loads((created / "keyframe_visual_reviews.json").read_text())
            self.assertEqual(boundaries["story"], "next_fable_v1")
            self.assertEqual(boundaries["shared_entries"], {})
            self.assertEqual(reviews["images"], {})

    def test_prompt_lint_requires_a_staging_frame_for_scene_images(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "staging_plan.json"
            path.write_text(json.dumps({
                "schema_version": 1, "story": "test", "cast_scale": {},
                "depth_model": {"far_scale": 0.55, "near_scale": 1.0},
                "views": {"wide": {"magnification": 1.0}},
                "locations": {}, "frames": []
            }))
            bible = {"staging_contract": "staging_plan.json", "cast_scale": {},
                     "characters": {}, "locations": {}, "setups": {}, "blocks": {}, "lint": {}}
            manifest = {"images": [{"id": "scene_start", "prompt_kind": "scene"}], "shots": []}
            with patch.object(image_prompts, "REPO", root):
                errors, _ = image_prompts.lint(manifest, bible)
            self.assertTrue(any("scene image scene_start has no staging frame" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
