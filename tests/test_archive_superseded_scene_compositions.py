"""Archive only verified revisions superseded by a selected scene still."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from production.archive_superseded_scene_compositions import SCENES, candidates, digest, explicit_candidates, run


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

    def test_explicit_newer_attempt_keeps_selected_older_source(self):
        self.row["path"] = str(self.old.relative_to(self.root))
        self.row["sha256"] = digest(self.old)
        self.new.with_suffix(".json").write_text(json.dumps({
            "output_path": str(self.new.relative_to(self.root)), "output_sha256": digest(self.new)}))
        self.assertEqual(explicit_candidates(self.root, [self.row], [self.new.name]),
                         [(self.new, self.new.with_suffix(".json"))])
        with self.assertRaisesRegex(ValueError, "no distinct selected source"):
            explicit_candidates(self.root, [self.row], [self.old.name])

    def test_ignored_archive_destination_fails_before_removal(self):
        subprocess.run(["git", "init", "-qb", "wan-new-image-approach"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.root, check=True)
        (self.root / ".gitignore").write_text("*.png\n!character/characters/**/*.png\n")
        index = self.root / "stories/lion_and_mouse_v7/history/retained_sources/INDEX.json"
        index.parent.mkdir(parents=True)
        index.write_text(json.dumps({"schema": "feltwillow.retained-sources.v1", "files": {}}))
        subprocess.run(["git", "add", "--", ".gitignore", str(index.relative_to(self.root)),
                        str(self.old.relative_to(self.root)), str(self.old.with_suffix(".json").relative_to(self.root)),
                        str(self.new.relative_to(self.root))], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.root, check=True)
        with patch("production.archive_superseded_scene_compositions.selection_catalog", return_value=[self.row]):
            with self.assertRaisesRegex(ValueError, "Git-ignored"):
                run(self.root, apply=True)
        self.assertTrue(self.old.is_file())
        self.assertEqual(json.loads(index.read_text())["files"], {})


if __name__ == "__main__":
    unittest.main()
