"""Performance sources must retain their recorded approval and exact bytes."""
import hashlib
import tempfile
import unittest
from pathlib import Path

from production.keyframe_plan import performance_references, _prompt_action


class PerformanceAuthorityTests(unittest.TestCase):
    def test_storyboard_mouth_directions_do_not_leak_into_boundaries(self):
        for action in ("Leo warns Milo; mouth open for Leo, all paws supported.",
                       "Milo explains; his mouth opens for his own dialogue, paws planted.",
                       "Leo reacts; open mouth for Leo only."):
            self.assertNotIn("open", _prompt_action(action))

    def test_candidate_atlas_is_not_promoted_and_absent_actor_is_not_attached(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "expression.png").write_bytes(b"approved expression")
            digest = hashlib.sha256(b"approved expression").hexdigest()
            plan = {"expression_authorities": {"milo": {
                "sheet": "expression.png", "sha256": digest, "status": "approved"}},
                "frames": {"f": {"milo": ["run"], "leo": ["sleep"]}},
                "poses": {"run": {"sheet": "pending.png", "status": "candidate_pending_owner_review"}}}
            refs = performance_references({"id": "f", "actors": {"milo": {}}}, {}, plan, root)
            self.assertEqual([r["role"] for r in refs], ["expression"])
            self.assertEqual(refs[0]["sha256"], digest)
            (root / "expression.png").write_bytes(b"changed bytes")
            with self.assertRaisesRegex(ValueError, "hash is stale"):
                performance_references({"id": "f", "actors": {"milo": {}}}, {}, plan, root)

    def test_explicit_owner_liked_pose_is_used_and_missing_approved_source_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pose.png").write_bytes(b"pose")
            plan = {"frames": {"f": {"milo": ["trip"]}}, "poses": {"trip": {
                "sheet": "pose.png", "status": "owner_liked_scene_anchor",
                "sha256": hashlib.sha256(b"pose").hexdigest()}}}
            refs = performance_references({"id": "f", "actors": {"milo": {}}}, {}, plan, root)
            self.assertEqual(refs[0]["role"], "pose")
            (root / "pose.png").unlink()
            with self.assertRaisesRegex(ValueError, "source is missing"):
                performance_references({"id": "f", "actors": {"milo": {}}}, {}, plan, root)
