"""Synthetic Git tests only; no production data or deletion operations."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from cleanup_audit import inventory, reference_leads, repo_root, sha256, validate_path  # noqa
from archive_verified import archive, verify_manifest  # noqa


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name) / "repo"
        self.root.mkdir()
        self.run_git("init", "-q", "-b", "wan-new-image-approach")
        self.run_git("config", "user.name", "Test")
        self.run_git("config", "user.email", "test@example.invalid")
        self.old = "character/characters/lion_and_mouse_v7/interactions/scene_compositions/S08-L016-B01-I01_end_r007_candidate.png"
        self.new = self.old.replace("r007", "r008")
        self.record = "stories/lion_and_mouse_v7/review/s08_accept_r001/owner_acceptance/OWNER_SELECTION.json"
        self.review = "stories/lion_and_mouse_v7/review/s08_accept_r001/REVIEW.html"
        self.v6 = "stories/lion_and_mouse_v6/keyframe_plan.json"
        self.chrono = "character/characters/_chrono_probe/Bramble/probe.png"
        self.write(self.old, b"OLD")
        self.write(self.new, b"NEW")
        self.write(self.record, json.dumps({"selected_path": self.new, "sha256": sha256(self.root / self.new)}).encode())
        self.write(self.review, f"<img src='{Path(self.new).name}'>".encode())
        self.write(self.v6, b"{}")
        self.write(self.chrono, b"PROBE")
        self.write("stories/lion_and_mouse_v7/audio_visual_plan.json", json.dumps({"scene": self.new}).encode())
        self.run_git("add", "-A")
        self.run_git("commit", "-q", "-m", "fixtures")
        self.head = self.run_git("rev-parse", "HEAD").strip()
        self.external = Path(self.t.name) / "external"
        self.external.mkdir()

    def write(self, rel, data):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)

    def run_git(self, *args):
        p = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, text=True)
        if p.returncode != 0:
            raise AssertionError(p.stderr)
        return p.stdout

    def manifest(self, rels):
        return {"schema": "feltwillow.cleanup-archive.v1", "source_branch": "wan-new-image-approach",
                "source_head": self.head, "files": [{"path": rel, "sha256": sha256(self.root / rel)} for rel in rels]}

    def test_inventory_protects_acceptance_and_lists_old_revision(self):
        d = inventory(self.root, {"S08"})
        by_path = {x["path"]: x for x in d["entries_requiring_investigation"]}
        self.assertIn(self.old, by_path)
        self.assertEqual(by_path[self.old]["classification"], "OLDER_REVISION_DEPENDENCY_CHECK")
        self.assertNotIn(self.new, by_path)  # newest is NOT automatically identified as selected
        self.assertEqual(by_path[self.record]["classification"], "PROTECT_AUTHORITY_EVIDENCE")
        self.assertEqual(by_path[self.v6]["classification"], "LEGACY_V6_DEPENDENCY_CHECK")
        self.assertEqual(by_path[self.chrono]["classification"], "CHRONO_PROBE_DEPENDENCY_CHECK")
        self.assertTrue(all(not r["deletion_authorized"] for r in by_path.values()))

    def test_scene_filter_skips_other_scene_old_revisions(self):
        d = inventory(self.root, {"S07"})
        self.assertNotIn(self.old, {r["path"] for r in d["entries_requiring_investigation"]})

    def test_reference_leads_are_only_evidence(self):
        r = reference_leads(self.root, self.new)
        self.assertEqual(r["sha256"], sha256(self.root / self.new))
        self.assertGreaterEqual(r["literal_hits_count"], 2)
        self.assertIn("LEADS ONLY", r["conclusion"])

    def test_reference_leads_blocks_traversal(self):
        for bad in ("../anything", "/tmp/anything", "./story.png", "a\\b", "a/../b"):
            with self.assertRaises((ValueError, FileNotFoundError)):
                validate_path(self.root, bad)

    def test_archive_copies_and_verifies_without_removing(self):
        manifest = self.manifest([self.old, self.review])
        mpath = self.external / "owner.json"
        mpath.write_text(json.dumps(manifest))
        destination = self.external / "archive.zip"
        r = archive(self.root, mpath, destination)
        self.assertEqual(r["status"], "VERIFIED_COPY_ONLY_NO_FILES_REMOVED")
        with ZipFile(destination) as z:
            self.assertEqual(z.read(self.old), b"OLD")
            self.assertEqual(z.read(self.review), (self.root / self.review).read_bytes())
            self.assertIn("FELTWILLOW_ARCHIVE_MANIFEST.json", z.namelist())
        self.assertEqual((self.root / self.old).read_bytes(), b"OLD")
        self.assertTrue((self.root / self.review).exists())

    def test_archive_rejects_mismatched_hash(self):
        m = self.manifest([self.old]);m["files"][0]["sha256"] = "0" * 64
        p = self.external / "bad.json";p.write_text(json.dumps(m))
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            archive(self.root, p, self.external / "no.zip")
        self.assertFalse((self.external / "no.zip").exists())

    def test_archive_rejects_stale_head(self):
        m = self.manifest([self.old]);m["source_head"] = "a" * 40
        with self.assertRaisesRegex(ValueError, "branch/HEAD mismatch"):
            verify_manifest(self.root, m)

    def test_archive_rejects_dirty_tracked_files(self):
        m = self.manifest([self.old]);(self.root / self.old).write_bytes(b"EDIT")
        with self.assertRaisesRegex(ValueError, "dirty"):
            verify_manifest(self.root, m)

    def test_archive_rejects_duplicate_file(self):
        m = self.manifest([self.old]);m["files"].append(dict(m["files"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            verify_manifest(self.root, m)

    def test_archive_rejects_inside_repo(self):
        m = self.manifest([self.old]);p = self.external / "m.json";p.write_text(json.dumps(m))
        with self.assertRaisesRegex(ValueError, "OUTSIDE"):
            archive(self.root, p, self.root / "do-not-create.zip")

    def test_archive_rejects_overwrite(self):
        m = self.manifest([self.old]);p = self.external / "m.json";p.write_text(json.dumps(m))
        dest = self.external / "existing.zip";dest.write_text("BEFORE")
        with self.assertRaises(FileExistsError):
            archive(self.root, p, dest)
        self.assertEqual(dest.read_text(), "BEFORE")

    def test_symlink_entry_blocked(self):
        link = self.root / "escape.bin"
        link.symlink_to(self.root / self.old)
        with self.assertRaisesRegex(ValueError, "Symlink"):
            validate_path(self.root, "escape.bin")


if __name__ == "__main__":
    unittest.main()
