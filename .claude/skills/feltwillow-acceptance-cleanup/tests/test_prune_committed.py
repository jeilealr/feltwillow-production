"""Synthetic-only destructive runner tests; creates isolated temporary Git repositories."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from cleanup_audit import sha256  # noqa
from prune_committed import apply, verify, _committed_sha  # noqa


class PruneTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name) / "repo"
        self.root.mkdir()
        self.git("init", "-q", "-b", "wan-new-image-approach")
        self.git("config", "user.email", "cleanup@example.invalid")
        self.git("config", "user.name", "Local Cleanup Test")
        self.old = "character/characters/lion_and_mouse_v7/interactions/scene_compositions/S08-L016-B01-I01_end_r007_candidate.png"
        self.new = self.old.replace("r007", "r008")
        self.owner = "stories/lion_and_mouse_v7/review/s08_owner/owner_acceptance/OWNER_SELECTION.json"
        self.resolve = "stories/lion_and_mouse_v7/derived/selection_uses.json"
        self.v6 = "stories/lion_and_mouse_v6/old_asset.json"
        self.chrono = "character/characters/_chrono_probe/Bramble/test.png"
        self.review = "stories/lion_and_mouse_v7/review/pose_first_s05_pilot_r001/CONTACT_SHEET.jpg"
        self.write(self.old, b"SUPERSEDED")
        self.write(self.new, b"ACCEPTED")
        self.write(self.review, b"PREVIEW")
        self.write(self.v6, b"OLD V6")
        self.write(self.chrono, b"PROBE")
        self.write(self.owner, json.dumps({"owner_selected_for_source_still":
                                               {"image": self.new, "sha256": sha256(self.root/self.new)}}).encode())
        self.write(self.resolve, json.dumps({"active": self.new,
                                              "sha256": sha256(self.root/self.new)}).encode())
        self.write("tests/test_current_selected.py", (
            "import pathlib\nimport unittest\n"
            "class T(unittest.TestCase):\n"
            " def test_selected(self):\n"
            "  self.assertTrue(pathlib.Path('" + self.new + "').is_file())\n"
        ).encode())
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "all artwork selections committed")
        self.head = self.git("rev-parse", "HEAD").strip()

    def write(self, rel: str, content: bytes):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)

    def git(self,*args):
        proc = subprocess.run(["git", "-C", str(self.root), *args],capture_output=True,text=True)
        if proc.returncode:
            raise AssertionError(proc.stderr)
        return proc.stdout

    def row(self, path: str):
        return {"path": path, "sha256": sha256(self.root/path)}

    def manifest(self, extras=None):
        base = {
            "schema": "feltwillow.cleanup-committed.v1",
            "source_branch": "wan-new-image-approach",
            "source_head": self.head,
            "authority_records": [
                {"role":"owner_selection", **self.row(self.owner)},
                {"role":"scene_use_resolution", **self.row(self.resolve)}
            ],
            "keep": [self.row(self.new)],
            "files": [{**self.row(self.old), "category":"superseded_revision",
                       "replacement":self.row(self.new),"owner_record":self.owner}],
            "validation_commands": [["python3","-m","unittest","discover","-s","tests","-q"]]
        }
        if extras:
            base.update(extras)
        return base

    def test_committed_cleanup_deletes_and_local_commits(self):
        result=apply(self.root,self.manifest())
        self.assertEqual(result["status"],"COMMITTED_LOCAL_NO_PUSH")
        self.assertFalse((self.root/self.old).exists())
        self.assertEqual((self.root/self.new).read_bytes(),b"ACCEPTED")
        self.assertNotEqual(self.git("rev-parse","HEAD").strip(),self.head)
        self.assertEqual(subprocess.run(["git","-C",str(self.root),"show",f"HEAD~1:{self.old}"],capture_output=True).stdout,b"SUPERSEDED")

    def test_dry_run_only_inspection(self):
        d=verify(self.root,self.manifest())
        self.assertEqual(d["count"],1)
        self.assertTrue((self.root/self.old).exists())
        self.assertEqual(self.git("rev-parse","HEAD").strip(),self.head)

    def test_refuses_uncommitted_tracked_changes(self):
        (self.root/self.old).write_bytes(b"NOT COMMITTED")
        with self.assertRaisesRegex(ValueError,"not committed"):
            verify(self.root,self.manifest())

    def test_refuses_stale_head(self):
        m=self.manifest();m["source_head"]="0"*40
        with self.assertRaisesRegex(ValueError,"stale"):
            verify(self.root,m)

    def test_refuses_selected_file_removal(self):
        m=self.manifest();m["files"]=[{"category":"review_derivative",**self.row(self.new)}]
        with self.assertRaisesRegex(ValueError,"narrowly allowed"):
            verify(self.root,m)

    def test_refuses_owner_record_removal(self):
        m=self.manifest();m["files"]=[{"category":"review_derivative",**self.row(self.owner)}]
        with self.assertRaisesRegex(ValueError,"protected"):
            verify(self.root,m)

    def test_retained_reference_to_old_png_blocks(self):
        self.write("docs/still_using_old.md",f"image: {self.old}".encode())
        self.git("add","-A")
        self.git("commit","-q","-m","add dangling reference")
        m=self.manifest();m["source_head"]=self.git("rev-parse","HEAD").strip()
        with self.assertRaisesRegex(ValueError,"Retained reference"):
            verify(self.root,m)

    def test_links_in_deleted_review_do_not_block(self):
        # The review is removed in the *same batch*, so its reference is obsolete.
        self.write(self.review,f"<img src='{self.old}'>".encode())
        self.git("add","-A")
        self.git("commit","-q","-m","old review reference")
        m=self.manifest();m["source_head"]=self.git("rev-parse","HEAD").strip()
        m["files"].append({**self.row(self.review),"category":"review_derivative"})
        d=verify(self.root,m)
        self.assertEqual(d["count"],2)

    def test_legacy_probe_and_v6_prune_without_second_approval(self):
        m=self.manifest();m["files"]= [{"category":"legacy_v6",**self.row(self.v6)},
                                         {"category":"chrono_probe",**self.row(self.chrono)}]
        r=apply(self.root,m)
        self.assertEqual(r["files_removed"],2)
        self.assertFalse((self.root/self.v6).exists())
        self.assertFalse((self.root/self.chrono).exists())

    def test_legacy_root_dynamic_reference_blocks(self):
        self.write("docs/v6_link.md",b"See stories/lion_and_mouse_v6 for old work")
        self.git("add","-A")
        self.git("commit","-q","-m","legacy dependency")
        m=self.manifest();m["source_head"]=self.git("rev-parse","HEAD").strip()
        m["files"]=[{"category":"legacy_v6",**self.row(self.v6)}]
        with self.assertRaisesRegex(ValueError,"legacy-root reference"):
            verify(self.root,m)

    def test_keep_bytes_protected(self):
        m=self.manifest();m["keep"][0]["sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"mismatched"):
            verify(self.root,m)

    def test_wrong_replacement_denied(self):
        m=self.manifest();m["files"][0]["replacement"]={"path":self.new,"sha256":"0"*64}
        with self.assertRaisesRegex(ValueError,"exact-hash KEEP"):
            verify(self.root,m)

    def test_missing_active_authority_denied(self):
        m=self.manifest();m["authority_records"]=m["authority_records"][:1]
        with self.assertRaisesRegex(ValueError,"required"):
            verify(self.root,m)

    def test_failed_after_test_rolls_back_only_managed_files(self):
        # Test only passes when old bytes exist: before passes, after fails.
        self.write("tests/test_old_needed.py", (
            "import pathlib\nimport unittest\n"
            "class T(unittest.TestCase):\n"
            " def test_old(self):\n"
            "  self.assertTrue(any(pathlib.Path('character/characters/lion_and_mouse_v7/interactions/scene_compositions').glob('*_r007_candidate.png')))\n"
        ).encode())
        self.git("add","-A")
        self.git("commit","-q","-m","legacy runtime fixture")
        m=self.manifest();m["source_head"]=self.git("rev-parse","HEAD").strip()
        with self.assertRaisesRegex(RuntimeError,"AFTER validation failed"):
            apply(self.root,m)
        self.assertTrue((self.root/self.old).exists())
        self.assertEqual(self.git("diff","--cached","--name-only"),"")
        self.assertEqual(self.git("diff","--name-only"),"")

    def test_dangling_approved_hash_in_authority_blocks(self):
        self.write(self.owner,json.dumps({"active":{"path":self.new,"sha256":sha256(self.root/self.new)},
                                          "historical":sha256(self.root/self.old)}).encode())
        self.git("add","-A")
        self.git("commit","-q","-m","historic reference")
        m=self.manifest();m["source_head"]=self.git("rev-parse","HEAD").strip()
        m["authority_records"][0] = {"role":"owner_selection",**self.row(self.owner)}
        with self.assertRaisesRegex(ValueError,"Retained reference"):
            verify(self.root,m)


if __name__=="__main__":
    unittest.main()
