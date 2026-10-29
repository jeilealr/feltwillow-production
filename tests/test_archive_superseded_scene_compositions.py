"""Archive only verified revisions superseded by a selected scene still."""

import json
import tempfile
import unittest
from pathlib import Path

from production.archive_superseded_scene_compositions import SCENES, candidates, digest


class ArchiveSceneTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.old = self.root / SCENES / "S03-L001-B01-I02_end_homeward_distance_r003_candidate.png"
        self.new = self.root / SCENES / "S03-L001-B01-I02_end_homeward_distance_r004_candidate.png"
        self.old.parent.mkdir(parents=True)
        self.old.write_bytes(b"old pixels")
        self.new.write_bytes(b"selected pixels")
        self.old.with_suffix(".json").write_text(json.dumps({
            "image_id": "S03-L001-B01-I02",
            "path": str(self.old.relative_to(self.root)),
            "sha256": digest(self.old),
        }))
        self.row = {"image_id": "S03-L001-B01-I02", "path": str(self.new.relative_to(self.root)),
                    "sha256": digest(self.new)}

    def test_only_old_hash_bound_pair_moves(self):
        self.assertEqual(candidates(self.root, [self.row]), [(self.old, self.old.with_suffix(".json"))])
        self.assertEqual(candidates(self.root, []), [])

    def test_selected_source_and_sidecar_mismatch_fail_closed(self):
        self.new.write_bytes(b"unexpected replacement")
        with self.assertRaisesRegex(ValueError, "selected source missing or changed"):
            candidates(self.root, [self.row])
        self.row["sha256"] = digest(self.new)
        self.old.with_suffix(".json").write_text(json.dumps({"image_id": "S03-L001-B01-I02",
                                                         "path": str(self.old.relative_to(self.root)),
                                                         "sha256": "wrong"}))
        with self.assertRaisesRegex(ValueError, "candidate sidecar mismatch"):
            candidates(self.root, [self.row])

    def test_unselected_newer_revision_remains_active(self):
        self.row["path"] = str(self.old.relative_to(self.root))
        self.row["sha256"] = digest(self.old)
        self.assertEqual(candidates(self.root, [self.row]), [])

    def test_exact_selected_scene_outside_active_folder_replaces_attempt(self):
        selected = self.root / "stories/lion_and_mouse_v7/review/approved_scene.png"
        selected.parent.mkdir(parents=True)
        selected.write_bytes(b"owner selected separate scene")
        self.row["path"] = str(selected.relative_to(self.root))
        self.row["sha256"] = digest(selected)
        self.new.unlink()
        self.assertEqual(candidates(self.root, [self.row]), [(self.old, self.old.with_suffix(".json"))])


if __name__ == "__main__":
    unittest.main()
