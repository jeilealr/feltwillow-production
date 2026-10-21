"""Hash-bound owner selection and safe CPU-only pilot staging."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from production import opening_handoff as h


class OpeningHandoffTests(unittest.TestCase):
    def test_actual_selection_and_local_audio(self):
        clips, missing = h.verify()
        self.assertEqual(len(clips['clips']), 26)
        self.assertEqual(len({c['id'] for c in clips['clips']}), 26)
        self.assertTrue(all(c['editorial_duration_seconds'] is None for c in clips['clips']))

    def test_escape_rejected(self):
        with self.assertRaises(ValueError):
            h.local(h.ROOT, '../outside.png')

    def test_prepare_refuses_existing_runtime_before_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / 'stories' / h.STORY
            folder.mkdir(parents=True)
            output = folder / 'story.yaml'
            output.write_text('owner runtime')
            proposal = {'clips': [{'id': 'pilot', 'scene': 1, 'keyframe': 'source.png',
                'keyframe_sha256': '0'*64, 'prompt': 'motion', 'negative': 'teeth',
                'frames': 81, 'seeds': [1], 'size': [1280,720]}]}
            with patch.object(h, 'verify', return_value=(proposal, [])):
                with self.assertRaises(ValueError):
                    h.prepare(root, root / 'work')
            self.assertEqual(output.read_text(), 'owner runtime')
            self.assertFalse((root / 'work').exists())
