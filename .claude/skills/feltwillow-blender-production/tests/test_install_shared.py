"""Shared installation tests on temporary repositories; no real client/Blender calls."""
import contextlib
import io
from pathlib import Path
import os
import shutil
import stat
import sys
import tempfile
import unittest
from zipfile import ZipFile, ZipInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from install_shared import NAME, RELATIVE_TARGET, setup


class SharedInstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repository with spaces'
        self.repo.mkdir()
        (self.repo / '.git').mkdir()
        self.source = self.repo / '.claude/skills' / NAME
        self.alias = self.repo / '.agents/skills' / NAME
        self.archive = self.root / 'skill.zip'
        self.backups = self.root / 'backups'
        self.payload = {
            'SKILL.md': f'---\nname: {NAME}\ndescription: Test fixture.\n---\nTest instructions.\n',
            'agents/openai.yaml': 'interface:\n  display_name: Test\n',
            'references/installation.md': 'Test installation\n',
        }
        with ZipFile(self.archive, 'w') as z:
            for name, data in self.payload.items():
                z.writestr(NAME + '/' + name, data)

    def install(self, apply=True):
        with contextlib.redirect_stdout(io.StringIO()):
            setup(self.repo, self.archive, self.backups, apply)

    def populate(self, destination, extra=None):
        for name, data in self.payload.items():
            path = destination / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data)
        if extra is not None:
            (destination / 'local-edits.md').write_text(extra)

    def assert_shared(self):
        self.assertTrue(self.source.is_dir())
        self.assertFalse(self.source.is_symlink())
        self.assertTrue(self.alias.is_symlink())
        self.assertEqual(os.readlink(self.alias), RELATIVE_TARGET)
        self.assertTrue(os.path.samefile(self.source / 'SKILL.md', self.alias / 'SKILL.md'))

    def test_fresh_install(self):
        self.install()
        self.assert_shared()

    def test_dry_run_makes_no_changes(self):
        self.install(False)
        self.assertEqual(sorted(p.name for p in self.repo.iterdir()), ['.git'])
        self.assertFalse(self.backups.exists())

    def test_claude_edits_preserved(self):
        self.populate(self.source, 'Preserve my changes.')
        self.install()
        self.assert_shared()
        self.assertEqual((self.alias / 'local-edits.md').read_text(), 'Preserve my changes.')

    def test_codex_only_migrated_without_loss(self):
        self.populate(self.alias, 'Codex-only edits.')
        self.install()
        self.assert_shared()
        self.assertEqual((self.source / 'local-edits.md').read_text(), 'Codex-only edits.')

    def test_identical_duplicate_backed_up(self):
        self.populate(self.source, 'Shared content')
        self.populate(self.alias, 'Shared content')
        self.install()
        self.assert_shared()
        saved = list(self.backups.glob('*/codex-copy/local-edits.md'))
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0].read_text(), 'Shared content')

    def test_conflicting_copies_stop_without_changes(self):
        self.populate(self.source, 'Claude edits')
        self.populate(self.alias, 'Codex edits')
        with self.assertRaisesRegex(ValueError, 'folders differ'):
            self.install()
        self.assertFalse(self.alias.is_symlink())
        self.assertEqual((self.source / 'local-edits.md').read_text(), 'Claude edits')
        self.assertEqual((self.alias / 'local-edits.md').read_text(), 'Codex edits')
        self.assertFalse(self.backups.exists())

    def test_repeated_install_is_noop(self):
        self.install()
        before = (self.source / 'SKILL.md').stat().st_mtime_ns
        self.install()
        self.assert_shared()
        self.assertEqual((self.source / 'SKILL.md').stat().st_mtime_ns, before)

    def test_existing_wrong_symlink_stops(self):
        self.alias.parent.mkdir(parents=True)
        self.alias.symlink_to('../../somewhere-else')
        with self.assertRaisesRegex(ValueError, 'somewhere else'):
            self.install()
        self.assertFalse(self.source.exists())
        self.assertEqual(os.readlink(self.alias), '../../somewhere-else')

    def test_correct_dangling_link_repaired_by_install(self):
        self.alias.parent.mkdir(parents=True)
        self.alias.symlink_to(RELATIVE_TARGET)
        self.install()
        self.assert_shared()

    def test_source_symlink_refused(self):
        self.populate(self.alias)
        self.source.parent.mkdir(parents=True)
        self.source.symlink_to('../../.agents/skills/' + NAME)
        with self.assertRaisesRegex(ValueError, 'already a symlink'):
            self.install()
        self.assertTrue(self.alias.is_dir())

    def test_parent_symlink_refused(self):
        external = self.root / 'external'; external.mkdir()
        (self.repo / '.agents').symlink_to(external)
        with self.assertRaisesRegex(ValueError, 'Parent is a symlink'):
            self.install()
        self.assertFalse(self.source.exists())

    def test_archive_traversal_refused(self):
        with ZipFile(self.archive, 'a') as z:
            z.writestr(NAME + '/../escape', 'bad')
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            self.install()
        self.assertFalse(self.source.exists())

    def test_archive_extra_skill_refused(self):
        with ZipFile(self.archive, 'a') as z:
            z.writestr(NAME + '/nested/SKILL.md', 'bad')
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            self.install()

    def test_archive_symlink_refused(self):
        with ZipFile(self.archive, 'a') as z:
            info = ZipInfo(NAME + '/outside')
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            z.writestr(info, '../../outside')
        with self.assertRaisesRegex(ValueError, 'Link/special'):
            self.install()

    def test_not_a_repository_stops(self):
        (self.repo / '.git').rmdir()
        with self.assertRaisesRegex(ValueError, 'Not a Git checkout'):
            self.install()

    def test_backup_inside_repository_refused(self):
        self.backups = self.repo / 'backups'
        with self.assertRaisesRegex(ValueError, 'outside the repository'):
            self.install()

    def test_resource_changes_visible_through_link(self):
        self.install()
        (self.source / 'references/installation.md').write_text('One source updated.')
        self.assertEqual((self.alias / 'references/installation.md').read_text(), 'One source updated.')

    def test_relative_link_survives_repository_relocation(self):
        self.install()
        moved = self.root / 'moved-repository'
        self.repo.rename(moved)
        self.assertTrue(os.path.samefile(moved / '.claude/skills' / NAME / 'SKILL.md',
                                        moved / '.agents/skills' / NAME / 'SKILL.md'))


if __name__ == '__main__':
    unittest.main()
