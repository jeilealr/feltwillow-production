"""Boundary planning must preserve chronology and never imply an accidental zoom."""

import json
import copy
import unittest

from production import keyframe_plan, video_boundary_plan
from production import keyframe_reference_gate


class VideoBoundaryPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = video_boundary_plan.REPO / "stories/lion_and_mouse_v6/keyframe_plan.json"
        cls.existing = json.loads(path.read_text())
        cls.config = video_boundary_plan.load_config("lion_and_mouse_v6")
        cls.plan = video_boundary_plan.build(cls.existing, cls.config)
        cls.staging = json.loads((path.parent / "staging_plan.json").read_text())
        cls.proposed = video_boundary_plan.build(cls.existing, cls.config, staging=cls.staging)

    def test_every_candidate_has_one_chronological_scene_assignment(self):
        scenes = self.plan["scenes"]
        ordered = [fid for scene in scenes for fid in scene["ordered_keyframes"]]
        self.assertEqual(len(scenes), 16)
        self.assertEqual(len(ordered), self.existing["keyframe_count"])
        self.assertEqual(set(ordered), {image["id"] for image in self.existing["images"]})
        self.assertEqual(len(ordered), len(set(ordered)))
        self.assertEqual(scenes[0]["ordered_keyframes"][-4:],
                         ["s01x_p01", "s01x_p02", "s01x_p03", "s01_p04"])

    def test_only_registered_compatible_scene_joins_share_exact_file(self):
        scenes = {scene["scene"]: scene for scene in self.plan["scenes"]}
        for number_text, prior in self.config["shared_entries"].items():
            number = int(number_text)
            self.assertEqual(scenes[number]["entry"], "shared_boundary_candidate")
            self.assertEqual(scenes[number]["start_image"], scenes[prior]["end_image"])
            self.assertEqual(scenes[number]["entry_motion"]["start_image"],
                             scenes[prior]["end_image"])
        for number, scene in scenes.items():
            if str(number) not in self.config["shared_entries"]:
                self.assertEqual(scene["entry"], "cut")
                self.assertEqual(scene["start_image"], scene["first_own_image"])

    def test_crop_changes_are_cuts_not_actor_size_animation(self):
        scene = next(item for item in self.plan["scenes"] if item["scene"] == 4)
        edge = next(item for item in scene["internal_transitions"]
                    if item["from"] == "s04_p02" and item["to"] == "s04x_p02")
        self.assertEqual(edge["kind"], "camera_cut")
        self.assertEqual(edge["start_image"], edge["end_image"])
        self.assertNotEqual(edge["end_image"], edge["next_start_image"])

    def test_supplemental_views_cannot_fall_back_to_record_order(self):
        config = copy.deepcopy(self.config)
        del config["scene_order_overrides"]["1"]
        with self.assertRaisesRegex(ValueError, "explicit chronological order"):
            video_boundary_plan.build(self.existing, config)

    def test_future_prompts_use_one_anatomical_height_and_no_off_camera_leo(self):
        fresh = keyframe_plan.build("lion_and_mouse_v6")
        records = {image["id"]: image for image in fresh["images"]}
        staging_path = video_boundary_plan.REPO / "stories/lion_and_mouse_v6/staging_plan.json"
        staging = json.loads(staging_path.read_text())
        expected = next(frame for frame in staging["frames"] if frame["id"] == "s04x_p02")
        height = expected["actors"]["milo"]["standing_equivalent_height_fraction_after_crop"]
        self.assertIn(f"standing-equivalent anatomical height target {height:.0%}",
                      records["s04x_p02"]["prompt"])
        self.assertNotIn("staging QA target", records["s04x_p02"]["prompt"])
        self.assertIn("No mane", records["s07x_p02"]["prompt"])
        self.assertNotRegex(records["s07x_p02"]["prompt"], r"full ears and mane")
        self.assertEqual(records["s07x_p02"]["mouth_policy"], "closed_boundary_for_lipsync")
        self.assertNotRegex(records["s07x_p02"]["prompt"], r"(?i)open mouth|speaking mouth")
        self.assertIn("Do not apply a global amber/orange grade",
                      records["s08_p04"]["prompt"])
        for fid in ("s14_p04", "s14_p05"):
            prompt = records[fid]["prompt"]
            self.assertIn("exactly ONE animal", prompt)
            self.assertIn("do not include a second animal", prompt)
            self.assertNotIn("Leo", prompt)

    def test_milo_portrait_never_positively_requests_mane(self):
        fresh = keyframe_plan.build("lion_and_mouse_v6")
        records = {image["id"]: image for image in fresh["images"]}
        self.assertIn("Milo's sharp canonical face", records["s12_p02"]["prompt"])
        self.assertIn("No mane", records["s12_p02"]["prompt"])
        self.assertIsNone(keyframe_reference_gate.POSITIVE_MANE_RE.search(records["s12_p02"]["prompt"]))

    def test_scene_12_portrait_to_wide_run_is_an_explicit_camera_cut(self):
        transition = next(item for item in self.proposed["proposed_camera_transitions"]
                          if item["from"] == "s12_p02" and item["to"] == "s12_p03")
        self.assertEqual(transition["kind"], "camera_cut")
        self.assertIn("pending_regenerated_keyframes", transition["status"])

    def test_view_family_change_is_a_cut_even_if_crop_rectangle_matches(self):
        staging = copy.deepcopy(self.staging)
        staging["views"]["same_crop_new_family"] = {"magnification": 1.0}
        frame = next(row for row in staging["frames"] if row["id"] == "s01_p02")
        frame["view"] = "same_crop_new_family"
        plan = video_boundary_plan.build(self.existing, self.config, staging=staging)
        transition = next(row for row in plan["proposed_camera_transitions"]
                          if row["from"] == "s01_p01" and row["to"] == "s01_p02")
        self.assertEqual(transition["source_crop"], transition["target_crop"])
        self.assertEqual(transition["kind"], "camera_cut")

    def test_scene_16_wide_family_resolves_to_one_size_anchor_id(self):
        anchors = {row["id"]: row for row in self.staging["frames"]}
        ids = ("s16_p01", "s16_p05", "s16x_p01", "s16x_p03")
        self.assertEqual(len({anchors[fid]["size_anchor_id"] for fid in ids}), 1)
        medium_ids = ("s16_p02", "s16_p03", "s16_p04", "s16x_p02")
        self.assertEqual(len({anchors[fid]["size_anchor_id"] for fid in medium_ids}), 1)
        self.assertNotEqual(anchors[ids[0]]["size_anchor_id"],
                            anchors[medium_ids[0]]["size_anchor_id"])


if __name__ == "__main__":
    unittest.main()
