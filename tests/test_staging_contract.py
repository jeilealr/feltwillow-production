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

    def test_v6_cast_ratio_and_approved_net_are_hash_bound_references(self):
        ratio = self.contract["cast_scale"]["same_depth_standing_equivalent_height_ratio"]["milo_to_leo"]
        self.assertEqual(ratio["standing_equivalent_height"], 0.25)
        plan = {row["id"]: row for row in keyframe_plan.build("lion_and_mouse_v6")["images"]}
        expected_net = "character/locations/lion_and_mouse_v6/props/.review/hunter_net_prop_r01_candidate.png"
        for frame_id in ("s10_p01", "s10_p02"):
            self.assertIn(expected_net, plan[frame_id]["references"])
            prop = plan[frame_id]["required_props"][0]
            self.assertEqual(prop["id"], "hunter_net")
            self.assertEqual(prop["status"], "approved_owner_hash_bound")
            net_ref = next(ref for ref in plan[frame_id]["reference_roles"]
                           if ref.get("role") == "prop" and ref.get("id") == "hunter_net")
            self.assertEqual(net_ref["sha256"],
                             "666d29ec6e0f323bf10450d4abd5125bf6c3bdf12e56bffdab6cffeede9666d3")
            self.assertIn("trigger loop", plan[frame_id]["prompt"])
            self.assertNotIn("Leo remains trapped", plan[frame_id]["prompt"])
        self.assertIn(expected_net, plan["s15_p04"]["references"])
        self.assertEqual(plan["s15_p04"]["required_props"][0]["id"], "hunter_net")
        self.assertIn("discarded net stays behind", plan["s15_p04"]["prompt"])
        self.assertNotIn(expected_net, plan["s15x_p01"]["references"])
        self.assertIn("looks surprised", plan["s10_p03"]["prompt"])

    def test_scene_16_identical_wides_share_one_registered_anchor(self):
        frames = {row["id"]: row for row in self.contract["frames"]}
        ids = ("s16_p01", "s16_p05", "s16x_p01", "s16x_p03")
        self.assertEqual(len({frames[fid]["size_anchor_id"] for fid in ids}), 1)
        expected = frames[ids[0]]["actors"]
        for fid in ids[1:]:
            self.assertEqual(frames[fid]["view"], "wide")
            self.assertEqual(frames[fid]["actors"], expected)

    def test_tree_day_description_and_color_contract_are_daylight(self):
        day = self.bible["locations"]["tree_day"]
        self.assertIn("in daylight", day["description"])
        self.assertNotIn("at dusk", day["description"])
        self.assertIn("This is daylight, not dusk", day["image_generation_contract"]["prompt_clause"])
        self.assertTrue(day["image_generation_contract"]["forbid_global_color_grade"])

    def test_portrait_crop_preserves_standing_equivalent_anatomy_contract(self):
        records = {row["id"]: row for row in self.contract["frames"]}
        for fid in ("s08_p03", "s08_p05", "s12_p02", "s15x_p02"):
            frame = records[fid]
            self.assertEqual(frame["view"], "portrait_milo")
            self.assertEqual(set(frame["actors"]), {"milo"})
            self.assertEqual(frame["camera_focus"], "strong_blur")
            self.assertFalse(frame["crop_changes_physical_scale"])
            self.assertEqual(frame["size_anchor_id"], "tree_dusk_portrait_milo_milo" if fid.startswith("s08") else
                             "run_morning_portrait_milo_milo" if fid == "s12_p02" else
                             "trap_morning_portrait_milo_milo")
        self.assertEqual(staging_contract.validate_contract(self.contract, self.bible), [])
        planned = {row["id"]: row for row in keyframe_plan.build("lion_and_mouse_v6")["images"]}
        self.assertEqual(set(planned["s08_p03"]["actors"]), {"milo"})
        self.assertEqual(set(planned["s15x_p01"]["actors"]), {"leo"})
        self.assertEqual(set(planned["s16x_p03"]["actors"]), {"leo", "milo"})

    def test_dialogue_line_intent_is_separate_from_closed_boundary_mouth(self):
        story = staging_contract.REPO / "stories" / "lion_and_mouse_v6"
        scene_plan = json.loads((story / "scene_plan.json").read_text())
        self.assertEqual(scene_plan["production_boundary_mouth_policy"],
                         "closed_boundary_for_lipsync")
        panels = [panel for scene in scene_plan["scenes"] for panel in scene["panels"]]
        self.assertTrue(all(panel.get("boundary_mouth") == "closed" for panel in panels))
        self.assertTrue(all("mouth_open_only_on_line_ids" not in panel for panel in panels))
        dialogue = [panel for panel in panels if panel.get("dialogue_speakers")]
        self.assertTrue(all(panel.get("lip_sync_line_ids") for panel in dialogue))
        call = next(panel for panel in panels if panel["panel_id"] == "s12_p02")
        self.assertEqual(call["dialogue_speakers"], ["MOUSE"])
        self.assertNotIn("with an Milo", call["action"])

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
