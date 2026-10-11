"""The video review gate must reject missing and stale visual decisions."""

import hashlib
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
            plan = {"images": [{"id": "s01_p01", "candidate_path": "frame.png", "sha256": digest}]}
            reviews = {"schema": "feltwillow.keyframe-visual-reviews.v1", "images": {}}
            self.assertTrue(any("no full-resolution visual review" in error
                                for error in keyframe_visual_gate.validate(plan, reviews, root)))
            reviews["images"]["s01_p01"] = {
                "sha256": digest, "reviewer": "owner", "reviewed_at": "2026-10-11",
                "size_anchor": "same-camera approved anchor",
                "size_evidence": "measured ear height and nearby ground-plane stone",
                "checks": {name: True for name in keyframe_visual_gate.CHECKS},
            }
            self.assertEqual(keyframe_visual_gate.validate(plan, reviews, root), [])
            reviews["known_rejections"] = {"s01_p01": {
                "sha256": digest, "reason": "face differs from canonical"}}
            self.assertTrue(any("known rejected PNG" in error
                                for error in keyframe_visual_gate.validate(plan, reviews, root)))
            image.write_bytes(b"changed image")
            self.assertTrue(any("stale" in error
                                for error in keyframe_visual_gate.validate(plan, reviews, root)))


if __name__ == "__main__":
    unittest.main()
