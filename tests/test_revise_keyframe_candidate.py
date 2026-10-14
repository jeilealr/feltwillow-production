"""Safe revision adoption requires a real, strictly newer candidate."""

import json
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from production import revise_keyframe_candidate


class ReviseKeyframeCandidateTests(unittest.TestCase):
    def test_stale_candidate_cannot_be_marked_current_without_new_revision_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            story = "lion_and_mouse_v6"
            story_dir = root / "stories" / story
            story_dir.mkdir(parents=True)
            keyframe_dir = root / "character/characters" / story / "interactions/keyframes"
            keyframe_dir.mkdir(parents=True)
            current = {"story": story, "images": [{
                "id": "s08_p02",
                "candidate_path": f"character/characters/{story}/interactions/keyframes/s08_p02_r03_candidate.png",
                "sha256": "a" * 64,
                "status": "candidate_generated_pending_owner_review",
                "regeneration_status": "stale_pending_new_revision",
            }]}
            path = story_dir / "keyframe_plan.json"
            path.write_text(json.dumps(current))
            same_revision = "character/characters/lion_and_mouse_v6/interactions/keyframes/s08_p02_r03_candidate.png"
            with self.assertRaisesRegex(ValueError, "strictly newer revision"):
                revise_keyframe_candidate.revise(story, "s08_p02", same_revision,
                                                  "", [], "test", root)
            missing_newer = "character/characters/lion_and_mouse_v6/interactions/keyframes/s08_p02_r04_candidate.png"
            with self.assertRaisesRegex(ValueError, "1920x1080 PNG"):
                revise_keyframe_candidate.revise(story, "s08_p02", missing_newer,
                                                  "", [], "test", root)
            self.assertEqual(json.loads(path.read_text())["images"][0]["regeneration_status"],
                             "stale_pending_new_revision")

    def test_revision_refreshes_the_authoritative_plate_and_records_compositor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            story = "lion_and_mouse_v6"
            story_dir = root / "stories" / story
            story_dir.mkdir(parents=True)
            keyframe_dir = root / "character/characters" / story / "interactions/keyframes"
            keyframe_dir.mkdir(parents=True)
            relative_image = (
                "character/characters/lion_and_mouse_v6/interactions/keyframes/"
                "s08_p02_r04_candidate.png")
            image = keyframe_dir / "s08_p02_r04_candidate.png"
            # Minimal valid 1920x1080 PNG header; revise() only reads the PNG IHDR.
            image.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\0\0\0\0IHDR" +
                              (1920).to_bytes(4, "big") + (1080).to_bytes(4, "big") +
                              b"\x08\x02\0\0\0")
            old_relative = (
                "character/characters/lion_and_mouse_v6/interactions/keyframes/"
                "s08_p02_r03_candidate.png")
            old_image = keyframe_dir / "s08_p02_r03_candidate.png"
            old_image.write_bytes(b"prior candidate bytes")
            old_hash = hashlib.sha256(old_image.read_bytes()).hexdigest()
            anatomy_reference = (
                "character/characters/lion_and_mouse_v6/interactions/keyframes/"
                ".review/s08_p02_limb_correction_reference.png")
            anatomy_path = root / anatomy_reference
            anatomy_path.parent.mkdir(parents=True)
            anatomy_path.write_bytes(b"owner-directed anatomy guidance")
            refs = [
                "character/locations/lion_and_mouse_v6/great_tree/tree_dusk_r01.png",
                "character/characters/lion_and_mouse_v6/Leo/canonical/full-body_leo_neutral_pose_r01.png",
                "character/locations/lion_and_mouse_v6/size_anchors/tree_dusk_close_solo_leo_owner_selected_r01.png",
            ]
            inputs = []
            for path in refs:
                item = root / path
                item.parent.mkdir(parents=True, exist_ok=True)
                item.write_bytes(path.encode())
                inputs.append({"role": "authority", "path": path,
                               "sha256": hashlib.sha256(item.read_bytes()).hexdigest(),
                               "required": True})
            plan_path = story_dir / "keyframe_plan.json"
            plan_path.write_text(json.dumps({"images": [{
                "id": "s08_p02",
                "candidate_path": old_relative,
                "sha256": old_hash,
                "status": "stale_pending_new_revision",
                "scene": 8,
                "audio_line_ids": [],
                "visual_unit_ids": [],
                "staging_ref": "s08_p02",
                "reference_plate": "work/stories/lion_and_mouse_v6/keyframe_plate_crops/s08_p02.png",
            }]}))
            (story_dir / "visual_bible.json").write_text(json.dumps({
                "cast_scale": {"same_depth_standing_equivalent_height_ratio": {
                    "milo_to_leo": {"standing_equivalent_height": 0.25}}}}))
            (story_dir / "staging_plan.json").write_text(json.dumps({"setup_anchors": {
                "tree_dusk_close_solo_leo": {"status": "approved_owner_hash_bound",
                    "image_path": refs[2], "sha256": inputs[2]["sha256"]}}}))
            (story_dir / "video_boundary_config.json").write_text("{}")
            (story_dir / "keyframe_visual_reviews.json").write_text(
                json.dumps({"images": {}, "known_rejections": {}}))

            fresh = {"images": [{
                "id": "s08_p02", "prompt": "planned keyframe prompt",
                "scene": 8, "audio_line_ids": [], "visual_unit_ids": [],
                "staging_ref": "s08_p02", "actors": {"leo": {}},
                "size_anchor_id": "tree_dusk_close_solo_leo",
                "view": "close_solo", "crop_rect_on_plate": [0.2, 0.4, 0.45, 0.45],
                "camera_family": "tree_dusk:close_solo", "staging_signature": {},
                "mouth_policy": "closed_boundary_for_lipsync",
                "reference_plate": refs[0], "reference_crop": None,
                "board_reference": "character/characters/lion_and_mouse_v6/interactions/keyframes/.review/s08_storyboard_r01_candidate.png",
                "required_props": [{"id": "hunter_net", "path": "net.png",
                                    "status": "approved_owner_hash_bound"}],
                "planned_view": "close_solo", "planned_crop_rect_on_plate": [0.2, 0.4, 0.45, 0.45],
                "planned_size_anchor_id": "tree_dusk_close_solo_leo",
            }]}
            contract = {"images": [{"id": "s08_p02", "actors": ["leo"],
                "size_anchor": {"id": "tree_dusk_close_solo_leo"},
                "view": "close_solo", "crop_rect_on_plate": [0.2, 0.4, 0.45, 0.45],
                "camera_family": "tree_dusk:close_solo", "staging_signature": {},
                "mouth_policy": "closed_boundary_for_lipsync",
                "regeneration_inputs": inputs}]}
            with patch.object(revise_keyframe_candidate.keyframe_plan, "build", return_value=fresh), \
                 patch.object(revise_keyframe_candidate.keyframe_reference_gate, "build_contract",
                              return_value=contract), \
                 patch.object(revise_keyframe_candidate.keyframe_reference_gate, "validate_contract",
                              return_value=[]), \
                 patch.object(revise_keyframe_candidate.keyframe_reference_gate, "prompt_errors",
                              return_value=[]), \
                 patch.object(revise_keyframe_candidate.keyframe_reference_gate, "git_locator",
                              return_value={"sha256": old_hash, "commit": "test", "path": old_relative}), \
                 patch.object(revise_keyframe_candidate.video_boundary_plan, "build",
                              return_value={"schema": "test"}):
                revised, _ = revise_keyframe_candidate.revise(
                    story, "s08_p02", relative_image, "planned keyframe prompt", refs,
                    "regression test", root,
                    generation_tool="built-in imagegen + deterministic compositor")
                owner_fix_prompt = (
                    "Milo must have exactly two forearms and two hind legs. Remove the extra arm "
                    "and repair the felt flank. Preserve character identity and proportions, camera, "
                    "background, and lighting; do not alter unrelated parts of the shot.")
                owner_fix, _ = revise_keyframe_candidate.revise(
                    story, "s08_p02", relative_image, owner_fix_prompt,
                    [old_relative, anatomy_reference],
                    "Owner-directed correction of a reported extra arm", root,
                    generation_tool="built-in imagegen + localized compositor",
                    owner_correction_target=True)

            row = revised["images"][0]
            self.assertEqual(row["reference_plate"], refs[0])
            self.assertIsNone(row["reference_crop"])
            self.assertIn(".review/s08_storyboard", row["board_reference"])
            self.assertEqual(row["required_props"], fresh["images"][0]["required_props"])
            self.assertEqual(row["historical_candidate_tool"],
                             "built-in imagegen + deterministic compositor")
            self.assertEqual(row["status"], "candidate_generated_pending_owner_review")
            correction = owner_fix["images"][0]
            self.assertEqual(correction["historical_candidate_references"],
                             [old_relative, anatomy_reference])
            self.assertEqual(correction["historical_candidate_inputs"][0]["role"],
                             "owner_correction_target")
            self.assertFalse(correction["historical_candidate_inputs"][0]["required"])
            self.assertEqual(correction["historical_candidate_inputs"][0]["sha256"], old_hash)
            self.assertEqual(correction["historical_candidate_inputs"][1]["role"],
                             "owner_correction_reference")
            self.assertEqual(correction["historical_candidate_inputs"][1]["sha256"],
                             hashlib.sha256(anatomy_path.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
