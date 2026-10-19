"""Synthetic filesystem upgrade tests; no actual Codex/Claude/Blender instance."""
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import unittest
from unittest import mock
from zipfile import ZipFile, ZipInfo

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from update_shared import update, NAME, SCHEMA, RELATIVE_TARGET, digest

class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.repo=self.root/'repo with spaces';self.repo.mkdir();(self.repo/'.git').mkdir()
        self.source=self.repo/'.claude/skills'/NAME;self.source.mkdir(parents=True)
        self.alias=self.repo/'.agents/skills'/NAME;self.alias.parent.mkdir(parents=True);self.alias.symlink_to(RELATIVE_TARGET)
        self.backups=self.root/'backups';self.archive=self.root/'skill.zip'
        self.old={'SKILL.md':b'old instructions','VERSION':b'1.0.1\n','references/old.md':b'unchanged','agents/openai.yaml':b'interface: {}\n'}
        self.new={**self.old,'SKILL.md':b'improved instructions','VERSION':b'1.1.0\n','references/new.md':b'new module'}
        self.new['release-update.json']=json.dumps({'schema':SCHEMA,'skill_name':NAME,'version':'1.1.0',
            'baseline_version':'1.0.1','baseline_sha256':{k:digest(v) for k,v in self.old.items()}}).encode()
        for name,data in self.old.items():p=self.source/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        self.write_zip()

    def write_zip(self):
        with ZipFile(self.archive,'w') as z:
            for name,data in self.new.items():z.writestr(NAME+'/'+name,data)

    def run_update(self,apply=True):
        with contextlib.redirect_stdout(io.StringIO()):
            return update(self.repo,self.archive,apply,self.backups)

    def test_dry_run_no_writes(self):
        self.run_update(False)
        self.assertEqual((self.source/'SKILL.md').read_bytes(),self.old['SKILL.md']);self.assertFalse(self.backups.exists())

    def test_upgrade_and_backup(self):
        r=self.run_update()
        self.assertEqual((self.source/'SKILL.md').read_bytes(),self.new['SKILL.md'])
        self.assertTrue(os.path.samefile(self.source/'SKILL.md',self.alias/'SKILL.md'))
        self.assertEqual((Path(r['backup'])/'source-before/SKILL.md').read_bytes(),self.old['SKILL.md'])

    def test_conflict_no_changes(self):
        (self.source/'SKILL.md').write_text('my own changes')
        with self.assertRaisesRegex(ValueError,'overlap'):self.run_update()
        self.assertEqual((self.source/'SKILL.md').read_text(),'my own changes');self.assertFalse(self.backups.exists())
        self.assertFalse((self.source/'references/new.md').exists())

    def test_local_edits_to_unchanged_file_preserved(self):
        (self.source/'references/old.md').write_text('local learning')
        r=self.run_update()
        self.assertIn('references/old.md',r['preserved_local_edits'])
        self.assertEqual((self.source/'references/old.md').read_text(),'local learning')

    def test_local_only_file_preserved(self):
        (self.source/'my-notes.md').write_text('extra')
        self.run_update();self.assertEqual((self.source/'my-notes.md').read_text(),'extra')

    def test_repeat_is_noop(self):
        self.run_update();before=(self.source/'SKILL.md').stat().st_mtime_ns;count=len(list(self.backups.iterdir()))
        self.run_update();self.assertEqual((self.source/'SKILL.md').stat().st_mtime_ns,before)
        self.assertEqual(len(list(self.backups.iterdir())),count)

    def test_local_deletion_conflict(self):
        (self.source/'references/old.md').unlink()
        with self.assertRaisesRegex(ValueError,'deleted locally'):self.run_update()
        self.assertFalse(self.backups.exists())

    def test_wrong_codex_link_conflict(self):
        self.alias.unlink();self.alias.symlink_to('../../other')
        with self.assertRaisesRegex(ValueError,'somewhere else'):self.run_update()

    def test_codex_directory_copy_conflict(self):
        self.alias.unlink();self.alias.mkdir()
        with self.assertRaisesRegex(ValueError,'separate copy'):self.run_update()

    def test_missing_link_created(self):
        self.alias.unlink();self.run_update();self.assertEqual(os.readlink(self.alias),RELATIVE_TARGET)

    def test_internal_symlink_conflict(self):
        (self.source/'external').symlink_to(self.root/'other')
        with self.assertRaisesRegex(ValueError,'Linked'):self.run_update()

    def test_parent_symlink_conflict(self):
        self.alias.unlink();self.alias.parent.rmdir();self.alias.parent.symlink_to(self.root/'somewhere')
        with self.assertRaisesRegex(ValueError,'symlink'):self.run_update()

    def test_old_archive_refused(self):
        del self.new['release-update.json'];self.write_zip()
        with self.assertRaisesRegex(ValueError,'older/non-upgrade'):self.run_update()

    def test_directory_obstruction_conflict(self):
        (self.source/'references/new.md').mkdir()
        with self.assertRaisesRegex(ValueError,'directory occupies'):self.run_update()
        self.assertFalse(self.backups.exists())

    def test_zip_traversal_refused(self):
        with ZipFile(self.archive,'a') as z:z.writestr(NAME+'/../../escape','bad')
        with self.assertRaisesRegex(ValueError,'Unsafe'):self.run_update()

    def test_zip_symlink_refused(self):
        with ZipFile(self.archive,'a') as z:
            i=ZipInfo(NAME+'/link');i.create_system=3;i.external_attr=(stat.S_IFLNK|0o777)<<16;z.writestr(i,'/tmp')
        with self.assertRaisesRegex(ValueError,'Link'):self.run_update()

    def test_other_skill_refused(self):
        with ZipFile(self.archive,'a') as z:z.writestr('another/SKILL.md','bad')
        with self.assertRaises(ValueError):self.run_update()

    def test_case_collision_refused(self):
        (self.source/'references/NEW.md').write_text('different')
        with self.assertRaisesRegex(ValueError,'case-colliding'):self.run_update()

    def test_backup_inside_repo_refused(self):
        self.backups=self.repo/'backups'
        with self.assertRaisesRegex(ValueError,'outside'):self.run_update()

    def test_unrelated_repository_files_untouched(self):
        other=self.repo/'.claude/skills/other';other.mkdir();(other/'SKILL.md').write_text('other')
        blend=self.repo/'leo.blend';blend.write_bytes(b'not a real blend')
        self.run_update()
        self.assertEqual((other/'SKILL.md').read_text(),'other');self.assertEqual(blend.read_bytes(),b'not a real blend')

    def test_relocation_keeps_link(self):
        self.run_update();moved=self.root/'moved';self.repo.rename(moved)
        self.assertTrue(os.path.samefile(moved/'.claude/skills'/NAME/'SKILL.md',moved/'.agents/skills'/NAME/'SKILL.md'))

    def test_swap_failure_rolls_back(self):
        original=Path.rename
        def fail_new(path,target):
            if path.name=='new-source':raise OSError('synthetic swap failure')
            return original(path,target)
        with mock.patch.object(Path,'rename',fail_new):
            with self.assertRaisesRegex(OSError,'synthetic'):self.run_update()
        self.assertEqual((self.source/'SKILL.md').read_bytes(),self.old['SKILL.md'])
        self.assertTrue(os.path.samefile(self.source/'SKILL.md',self.alias/'SKILL.md'))

    def test_missing_version_refused(self):
        del self.new['VERSION'];self.write_zip()
        with self.assertRaises(ValueError):self.run_update()
        self.assertFalse(self.backups.exists())

    def test_new_file_local_conflict(self):
        (self.source/'references/new.md').write_text('my competing new module')
        with self.assertRaisesRegex(ValueError,'overlap'):self.run_update()
        self.assertFalse(self.backups.exists())

    def test_non_repository_refused(self):
        (self.repo/'.git').rmdir()
        with self.assertRaisesRegex(ValueError,'Git checkout'):self.run_update()

if __name__=='__main__':unittest.main()
