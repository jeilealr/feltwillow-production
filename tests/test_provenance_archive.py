"""The archive must be present in the committed tree, not only on one host."""

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from production.provenance_archive import INDEX, PERFORMANCE, audit


class ProvenanceArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.root, check=True)
        self.archive = self.root / "stories/lion_and_mouse_v7/history/retained_sources/files/old.png"
        self.archive.parent.mkdir(parents=True)
        self.archive.write_bytes(b"exact image")
        self.index = self.root / INDEX
        self.index.write_text(json.dumps({"schema": "feltwillow.retained-sources.v1", "files": {
            "old.png": {"archived_path": str(self.archive.relative_to(self.root)),
                        "sha256": hashlib.sha256(b"exact image").hexdigest()}}}))
        self.registry = self.root / PERFORMANCE
        self.registry.write_text("{}")

    def commit(self, include_image=True):
        paths = [str(INDEX), str(PERFORMANCE)]
        if include_image:
            paths.append(str(self.archive.relative_to(self.root)))
        subprocess.run(["git", "add", "--", *paths], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.root, check=True)

    def test_tracked_exact_archive_passes(self):
        self.commit()
        self.assertEqual(audit(self.root)["status"], "PASS")

    def test_ignored_archive_fails_even_if_local_bytes_match(self):
        (self.root / ".gitignore").write_text("*.png\n")
        self.commit(include_image=False)
        result = audit(self.root)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["findings"][0]["status"], "UNTRACKED_IN_GIT")

    def test_changed_worktree_fails(self):
        self.commit()
        self.archive.write_bytes(b"changed")
        self.assertEqual(audit(self.root)["findings"][0]["status"], "HASH_MISMATCH")

    def test_missing_selected_performance_reference_fails(self):
        self.commit()
        self.registry.write_text(json.dumps({"file": {"path": "selected/pair.png",
                                                      "sha256": hashlib.sha256(b"pair").hexdigest()}}))
        self.assertEqual(audit(self.root)["performance_references"][0]["status"], "MISSING")
        selected = self.root / "selected/pair.png"
        selected.parent.mkdir()
        selected.write_bytes(b"pair")
        self.assertEqual(audit(self.root)["performance_references"][0]["status"], "UNTRACKED_IN_GIT")

    def test_unsafe_index_path_fails_before_read(self):
        self.commit()
        record = json.loads(self.index.read_text())
        record["files"]["old.png"]["archived_path"] = "../../outside.png"
        self.index.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, "unsafe repository path"):
            audit(self.root)

    def test_symlink_archive_is_rejected(self):
        self.commit()
        target = self.root / "same_bytes.png"
        target.write_bytes(b"exact image")
        self.archive.unlink()
        self.archive.symlink_to(target)
        with self.assertRaisesRegex(ValueError, "symlink in archived path"):
            audit(self.root)


if __name__ == "__main__":
    unittest.main()
