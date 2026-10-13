"""Keep active relative links usable from a clean tracked checkout."""

import tempfile
import unittest
from pathlib import Path

from production.check_markdown_links import broken_links, repository_links


class MarkdownLinkTests(unittest.TestCase):
    def test_relative_links_resolve(self):
        self.assertEqual(repository_links(), [])

    def test_reports_missing_relative_file_but_not_external_or_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root / "test.md"
            document.write_text(
                "[missing](missing.png) [external](https://example.com/x) [anchor](#part)\n"
            )
            self.assertEqual(broken_links(document, root), ["test.md:1: missing.png"])

    def test_untracked_local_target_is_not_clean_clone_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root / "test.md"
            target = root / "local.png"
            document.write_text("[local](local.png)\n")
            target.write_bytes(b"present only on this machine")
            self.assertEqual(broken_links(document, root, {document}), ["test.md:1: local.png"])

