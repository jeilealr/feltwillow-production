"""Portable source-authority checks for keyframe regeneration contracts."""

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from production import keyframe_reference_gate as gate
from production.materialize_plate_crop import _write_png


def _png(path: Path, rgb: tuple[int, int, int]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    _write_png(path, 32, 18, 3, bytes(rgb) * (32 * 18))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fixture(root: Path) -> tuple[dict, dict, dict, dict]:
    plate = "character/locations/story/plate.png"
    canonical = "character/characters/story/Milo/canonical.png"
    anchor = "character/characters/story/anchors/a.png"
    candidate = "character/characters/story/interactions/keyframes/s01_p01.png"
    plate_hash = _png(root / plate, (1, 2, 3))
    canonical_hash = _png(root / canonical, (4, 5, 6))
    anchor_hash = _png(root / anchor, (7, 8, 9))
    candidate_hash = _png(root / candidate, (10, 11, 12))
    anchor_id = "tree_wide_milo"
    frame = {"id": "s01_p01", "location": "tree", "plate": plate,
             "view": "wide", "actors": {"milo": {"contact_xy_on_plate": [0.5, 0.8],
                "depth_t": 0.5, "standing_equivalent_height_fraction_after_crop": 0.2}},
             "size_anchor_id": anchor_id}
    staging = {"frames": [frame], "views": {"wide": {"magnification": 1.0}},
               "setup_anchors": {anchor_id: {"status": "approved_owner_hash_bound",
                  "image_path": anchor, "sha256": anchor_hash}}}
    bible = {"characters": {"milo": {"canonical": canonical}},
             "character_foundation_approval": {"milo_body_revision_status": "approved_owner_hash_bound"}}
    plan = {"images": [{"id": "s01_p01", "candidate_path": candidate,
                         "sha256": candidate_hash}]}
    contract = {"schema": gate.SCHEMA, "story": "story", "images": [{
        "id": "s01_p01", "actors": ["milo"], "location": "tree",
        "camera_family": "tree:wide", "view": "wide", "crop_rect_on_plate": [0, 0, 1, 1],
        "size_anchor": {"id": anchor_id, "status": "approved_owner_hash_bound",
                        "path": anchor, "sha256": anchor_hash},
        "foundation_authorities": {"milo": {"canonical_path": canonical,
            "sha256": canonical_hash, "approval_status": "approved_owner_hash_bound"}},
        "regeneration_inputs": [
            {"role": "approved_plate", "path": plate, "sha256": plate_hash,
             "required": True, "crop_rect_on_plate": [0, 0, 1, 1],
             "materializer": "normalized_crop.v1"},
            {"role": "identity_root", "actor": "milo", "path": canonical,
             "sha256": canonical_hash, "required": True},
            {"role": "size_anchor", "id": anchor_id, "path": anchor,
             "sha256": anchor_hash, "required": True},
        ],
        "mouth_policy": "closed_boundary_for_lipsync",
        "prompt": "Milo standing-equivalent anatomical height target 20% of this frame. No mane.",
        "active_candidate": {"path": candidate, "sha256": candidate_hash},
        "generation_history": {"historical_inputs": []},
    }]}
    return contract, staging, bible, plan


class KeyframeReferenceGateTests(unittest.TestCase):
    def test_valid_authority_stack_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, staging, bible, plan = _fixture(root)
            self.assertEqual(gate.validate_contract(contract, root, staging, bible, plan), [])

    def test_visible_actor_without_canonical_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, staging, bible, plan = _fixture(root)
            contract["images"][0]["regeneration_inputs"] = [
                item for item in contract["images"][0]["regeneration_inputs"]
                if item["role"] != "identity_root"]
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertTrue(any("visible actor milo needs" in error for error in errors))

    def test_plate_or_crop_authority_is_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, staging, bible, plan = _fixture(root)
            contract["images"][0]["regeneration_inputs"] = [
                item for item in contract["images"][0]["regeneration_inputs"]
                if item["role"] != "approved_plate"]
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertTrue(any("approved plate/crop authority" in error for error in errors))

    def test_missing_live_reference_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, staging, bible, plan = _fixture(root)
            contract["images"][0]["regeneration_inputs"][0]["path"] = "missing/plate.png"
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertTrue(any("live regeneration input is missing" in error for error in errors))

    def test_missing_historical_input_with_git_locator_is_provenance_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            history = root / "old.png"
            history.write_bytes(b"historical bytes")
            subprocess.run(["git", "add", "old.png"], cwd=root, check=True)
            env = dict(os.environ, GIT_AUTHOR_NAME="Test", GIT_AUTHOR_EMAIL="test@example.com",
                       GIT_COMMITTER_NAME="Test", GIT_COMMITTER_EMAIL="test@example.com")
            subprocess.run(["git", "commit", "-qm", "history"], cwd=root, env=env, check=True)
            locator = gate.git_locator(root, "old.png")
            history.unlink()
            contract, staging, bible, plan = _fixture(root)
            row = contract["images"][0]
            row["generation_history"]["historical_inputs"] = [{
                "path": "old.png", "status": "recoverable_from_git",
                "sha256": locator["sha256"], "git_locator": locator,
                "regeneration_allowed": False}]
            self.assertEqual(gate.validate_contract(contract, root, staging, bible, plan), [])
            row["regeneration_inputs"].append({"role": "edit_base", "path": "old.png",
                                                "sha256": locator["sha256"]})
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertTrue(any("live regeneration input is missing" in error for error in errors))

    def test_generated_image_as_only_reference_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, staging, bible, plan = _fixture(root)
            row = contract["images"][0]
            row["regeneration_inputs"] = [{"role": "edit_base",
                "path": row["active_candidate"]["path"],
                "sha256": row["active_candidate"]["sha256"], "visually_approved": False}]
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertTrue(any("approved plate/crop authority" in error for error in errors))
            self.assertTrue(any("visible actor milo needs" in error for error in errors))
            self.assertTrue(any("active generated image is being used" in error for error in errors))

    def test_owner_correction_target_is_hash_bound_and_never_authoritative(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, staging, bible, plan = _fixture(root)
            row = contract["images"][0]
            target = "character/characters/story/interactions/keyframes/reported_target.png"
            target_hash = _png(root / target, (12, 13, 14))
            row["regeneration_inputs"].append({
                "role": "owner_correction_target", "path": target,
                "sha256": target_hash, "required": False,
                "owner_directed_correction": True,
                "authority_scope": "correction target only; not identity, scale, camera, plate, or lighting authority",
            })
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertEqual(errors, [])

            row["regeneration_inputs"][-1]["owner_directed_correction"] = False
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertTrue(any("owner correction target must be optional and explicitly non-authoritative" in error
                                for error in errors))

    def test_reference_hash_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, staging, bible, plan = _fixture(root)
            contract["images"][0]["regeneration_inputs"][0]["sha256"] = "0" * 64
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertTrue(any("reference hash mismatch" in error for error in errors))

    def test_contract_camera_crop_and_candidate_must_match_current_records(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, staging, bible, plan = _fixture(root)
            row = contract["images"][0]
            row["camera_family"] = "tree:portrait"
            row["active_candidate"]["sha256"] = "0" * 64
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertTrue(any("camera family/view differs from staging" in error for error in errors))
            self.assertTrue(any("active candidate differs from keyframe plan" in error for error in errors))
            row["camera_family"] = "tree:wide"
            row["active_candidate"]["sha256"] = plan["images"][0]["sha256"]
            row["crop_rect_on_plate"] = [0.1, 0.1, 0.8, 0.8]
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertTrue(any("crop differs from current registered staging" in error for error in errors))

    def test_milo_positive_mane_wording_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, staging, bible, plan = _fixture(root)
            contract["images"][0]["prompt"] = "Milo has a large felt mane. Milo height target 20%."
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertTrue(any("positively requests a mane" in error for error in errors))

    def test_contradictory_height_targets_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, staging, bible, plan = _fixture(root)
            contract["images"][0]["prompt"] = (
                "Milo standing-equivalent anatomical height target 20% of frame; "
                "Milo height target 35% of frame.")
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertTrue(any("one standing-equivalent height target" in error for error in errors))

    def test_current_same_depth_cast_ratio_is_bound_to_visual_bible(self):
        prompt = (
            "Milo standing-equivalent anatomical height target 12% of frame; "
            "Leo standing-equivalent anatomical height target 50% of frame. "
            "At equal depth and camera Milo's upright ear-to-foot standing-equivalent height is "
            "about 40% of Leo's quadrupedal mane-top-to-supporting-front-paw height.")
        errors = gate.prompt_errors(prompt, ["leo", "milo"], "closed_boundary_for_lipsync",
                                    expected_cast_ratio=0.25)
        self.assertTrue(any("ratio must match" in error for error in errors))
        prompt = prompt.replace("about 40%", "about 25%")
        self.assertFalse(any("ratio must match" in error for error in gate.prompt_errors(
            prompt, ["leo", "milo"], "closed_boundary_for_lipsync", expected_cast_ratio=0.25)))

    def test_unrecoverable_old_inputs_are_warnings_but_active_candidate_is_a_blocker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, staging, bible, plan = _fixture(root)
            history = contract["images"][0]["generation_history"]
            history["historical_inputs"] = [{"path": "external.png", "status": "external_source_unavailable",
                                              "regeneration_allowed": False}]
            history["recorded_revisions"] = [{"state": "superseded_candidate",
                                                "candidate_path": "old.png",
                                                "status": "unrecoverable_recorded_revision"}]
            report = gate.validate_contract_report(contract, root, staging, bible, plan)
            self.assertEqual(report["current_authority_blockers"], [])
            self.assertEqual(len(report["historical_provenance_warnings"]), 2)
            history["recorded_revisions"][0]["state"] = "active_candidate"
            report = gate.validate_contract_report(contract, root, staging, bible, plan)
            self.assertTrue(any("candidate history lacks a recoverable Git locator" in error
                                for error in report["current_authority_blockers"]))

    def test_required_prop_cannot_be_silently_used_before_owner_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, staging, bible, plan = _fixture(root)
            prop = "character/locations/story/props/net.png"
            _png(root / prop, (13, 14, 15))
            row = contract["images"][0]
            row["required_props"] = [{"id": "hunter_net", "path": prop,
                                      "status": "design_candidate_pending_owner_review"}]
            errors = gate.validate_contract(contract, root, staging, bible, plan)
            self.assertTrue(any("required prop hunter_net is pending owner approval" in error
                                for error in errors))
            row["required_props"][0]["status"] = "approved_owner_hash_bound"
            row["regeneration_inputs"].append({"role": "prop", "id": "hunter_net",
                "path": prop, "sha256": hashlib.sha256((root / prop).read_bytes()).hexdigest(),
                "required": True})
            self.assertEqual(gate.validate_contract(contract, root, staging, bible, plan), [])

    def test_active_root_extra_and_missing_candidates_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract, _, _, plan = _fixture(root)
            folder = root / "character/characters/story/interactions/keyframes"
            self.assertEqual(gate.validate_active_inventory(plan, folder), [])
            (folder / "extra.png").write_bytes(b"extra")
            errors = gate.validate_active_inventory(plan, folder)
            self.assertTrue(any("unreferenced" in error for error in errors))
            (folder / "s01_p01.png").unlink()
            errors = gate.validate_active_inventory(plan, folder)
            self.assertTrue(any("missing" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
