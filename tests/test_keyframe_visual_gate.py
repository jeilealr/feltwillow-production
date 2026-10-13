"""The video review gate must reject missing and stale visual decisions."""

import hashlib
import copy
import tempfile
import unittest
from pathlib import Path

from production import keyframe_visual_gate


class KeyframeVisualGateTests(unittest.TestCase):
    def test_hash_bound_review_requires_all_visual_checks_and_size_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = root / "frame.png"
            image.write_bytes(b"candidate bytes")
            digest = hashlib.sha256(image.read_bytes()).hexdigest()
            canonical = root / "canonical.png"
            canonical.write_bytes(b"canonical bytes")
            canonical_hash = hashlib.sha256(canonical.read_bytes()).hexdigest()
            plan = {"images": [{"id": "s01_p01", "candidate_path": "frame.png", "sha256": digest,
                                "planned_actors": {"milo": {}},
                                "planned_size_anchor_id": "same-camera-anchor",
                                "planned_camera_family": "tree_dusk:wide"}]}
            reviews = {"schema": "feltwillow.keyframe-visual-reviews.v1", "images": {}}
            reviews["frame_dispositions"] = keyframe_visual_gate.build_frame_dispositions(plan, reviews)
            self.assertTrue(any("no full-resolution visual review" in error
                                for error in keyframe_visual_gate.validate(plan, reviews, root)))
            reviews["images"]["s01_p01"] = {
                "sha256": digest, "reviewer": "owner", "reviewed_at": "2026-10-11",
                "size_anchor_id": "same-camera-anchor",
                "size_anchor_sha256": "a" * 64,
                "size_evidence": "measured ear height and nearby ground-plane stone",
                "camera_family": "tree_dusk:wide",
                "identity_reference_sha256": {"milo": canonical_hash},
                "anatomy_evidence": {"milo": {
                    "expected_visible_paw_count": 2,
                    "observed_visible_paw_count": 2,
                    "missing_or_duplicated_limbs": False,
                    "support_contact": "Both visible feet contact the registered path."}},
                "checks": {name: True for name in keyframe_visual_gate.CHECKS},
            }
            reviews["frame_dispositions"] = keyframe_visual_gate.build_frame_dispositions(plan, reviews)
            staging = {"setup_anchors": {"same-camera-anchor": {
                "status": "approved_owner_hash_bound", "sha256": "a" * 64}}}
            bible = {"characters": {"milo": {"canonical": "canonical.png"}}}
            self.assertEqual(keyframe_visual_gate.validate(plan, reviews, root, staging, bible), [])
            wrong_anchor = copy.deepcopy(reviews)
            wrong_anchor["images"]["s01_p01"]["size_anchor_id"] = "different-anchor"
            self.assertTrue(any("size anchor ID must match" in error for error in
                                keyframe_visual_gate.validate(plan, wrong_anchor, root, staging, bible)))
            wrong_camera = copy.deepcopy(reviews)
            wrong_camera["images"]["s01_p01"]["camera_family"] = "tree_dusk:close_solo"
            self.assertTrue(any("camera_family differs" in error for error in
                                keyframe_visual_gate.validate(plan, wrong_camera, root, staging, bible)))
            missing_anatomy = copy.deepcopy(reviews)
            missing_anatomy["images"]["s01_p01"].pop("anatomy_evidence")
            missing_anatomy["frame_dispositions"] = keyframe_visual_gate.build_frame_dispositions(
                plan, missing_anatomy)
            self.assertTrue(any("expected_visible_paw_count" in error for error in
                                keyframe_visual_gate.validate(plan, missing_anatomy, root, staging, bible)))
            reviews["known_rejections"] = {"s01_p01": {
                "sha256": digest, "reason": "face differs from canonical"}}
            reviews["frame_dispositions"] = keyframe_visual_gate.build_frame_dispositions(plan, reviews)
            self.assertTrue(any("known rejected PNG" in error
                                for error in keyframe_visual_gate.validate(plan, reviews, root, staging, bible)))
            self.assertTrue(any("active candidate hash is explicitly rejected" in error
                                for error in keyframe_visual_gate.validate(plan, reviews, root, staging, bible)))
            image.write_bytes(b"changed image")
            self.assertTrue(any("stale" in error
                                for error in keyframe_visual_gate.validate(plan, reviews, root, staging, bible)))

    def test_stale_camera_candidate_is_not_misreported_as_visual_rejection(self):
        plan = {"images": [{"id": "s08_p02", "candidate_path": "missing.png", "sha256": "a" * 64,
                            "regeneration_status": "stale_pending_new_revision",
                            "planned_actors": {"leo": {}}}]}
        reviews = {"schema": "feltwillow.keyframe-visual-reviews.v1", "images": {},
                   "known_rejections": {}}
        reviews["frame_dispositions"] = keyframe_visual_gate.build_frame_dispositions(plan, reviews)
        row = reviews["frame_dispositions"]["s08_p02"]
        self.assertEqual(row["staging_freshness"], "stale")
        self.assertEqual(row["visual_disposition"], "supersede_for_camera_plan")
        errors = keyframe_visual_gate.validate_frame_dispositions(plan, reviews)
        self.assertTrue(any("camera/staging changed" in error for error in errors))
        self.assertFalse(any("explicitly rejected" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
