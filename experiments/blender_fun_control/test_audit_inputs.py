"""Safety tests for experimental source auditing; no media/model dependencies."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("audit_inputs", Path(__file__).with_name("audit_inputs.py"))
audit_inputs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_inputs)


class AuditInputsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.base = self.root / "stories" / audit_inputs.STORY
        self.base.mkdir(parents=True)
        (self.root / "start.png").write_bytes(b"fixture start bytes")
        (self.root / "end.png").write_bytes(b"fixture end bytes")
        (self.root / "plate.png").write_bytes(b"fixture plate bytes")
        rows = []
        for key, name in (("a", "start.png"), ("b", "end.png")):
            rows.append({"id": key, "scene": 1, "candidate_path": name,
                         "sha256": audit_inputs.sha256(self.root / name),
                         "approved_plate": "plate.png", "view": "medium_solo",
                         "planned_view": "medium_solo", "crop_rect_on_plate": [0, 0, 1, 1],
                         "planned_crop_rect_on_plate": [0, 0, 1, 1],
                         "planned_actors": {"milo": {"depth_t": 0.5}}})
        self.plan = {"story": audit_inputs.STORY, "images": rows}
        self.boundary = {"story": audit_inputs.STORY, "scenes": [{"internal_transitions": [
            {"from": "a", "to": "b", "kind": "same_view_motion_candidate",
             "start_image": "start.png", "end_image": "end.png"}]}]}
        self.write("keyframe_plan.json", self.plan)
        self.write("video_boundary_plan.json", self.boundary)
        for name in ("staging_plan.json", "keyframe_visual_reviews.json", "owner_visual_acceptance.json"):
            self.write(name, {"story": audit_inputs.STORY})
        (self.base / "RUNTIME_CONTRACT.md").write_text("fixture contract")

    def write(self, name, data):
        (self.base / name).write_text(json.dumps(data))

    def test_same_view_never_grants_production_approval(self):
        result = audit_inputs.audit(self.root, "a", "b")
        self.assertTrue(result["metadata_consistent"])
        self.assertFalse(result["production_eligible"])
        self.assertFalse(result["visual_review_performed"])
        self.assertEqual(len(result["document_sha256"]), 6)

    def test_hold_is_supported(self):
        self.assertEqual(audit_inputs.audit(self.root, "a", "a")["boundary"], "hold")

    def test_camera_cut_is_rejected(self):
        self.boundary["scenes"][0]["internal_transitions"][0]["kind"] = "camera_cut"
        self.write("video_boundary_plan.json", self.boundary)
        with self.assertRaisesRegex(ValueError, "cuts excluded"):
            audit_inputs.audit(self.root, "a", "b")

    def test_same_view_label_does_not_override_geometry(self):
        self.plan["images"][1].update(view="portrait_milo", planned_view="portrait_milo")
        self.write("keyframe_plan.json", self.plan)
        with self.assertRaisesRegex(ValueError, "plate/view/crop mismatch"):
            audit_inputs.audit(self.root, "a", "b")

    def test_stale_candidate_is_rejected(self):
        (self.root / "start.png").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "hash differs"):
            audit_inputs.audit(self.root, "a", "b")

    def test_boundary_endpoint_must_match_selection(self):
        self.boundary["scenes"][0]["internal_transitions"][0]["end_image"] = "old.png"
        self.write("video_boundary_plan.json", self.boundary)
        with self.assertRaisesRegex(ValueError, "boundary endpoint path"):
            audit_inputs.audit(self.root, "a", "b")

    def test_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "foreign.png"
            target.write_bytes(b"outside")
            (self.root / "escape.png").symlink_to(target)
            with self.assertRaisesRegex(ValueError, "outside repository"):
                audit_inputs.contained_file(self.root, "escape.png")

    def test_invalid_crop_is_rejected(self):
        self.plan["images"][0].update(crop_rect_on_plate=[0.8, 0, 0.5, 1],
                                      planned_crop_rect_on_plate=[0.8, 0, 0.5, 1])
        self.write("keyframe_plan.json", self.plan)
        with self.assertRaisesRegex(ValueError, "invalid normalized"):
            audit_inputs.audit(self.root, "a", "a")


if __name__ == "__main__":
    unittest.main()
