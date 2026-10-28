import importlib.util
from pathlib import Path
import tempfile
import json
import unittest
from production.check_shared_skills import check

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('image_route', ROOT / '.claude/skills/image-routing/scripts/route.py')
routing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(routing)

class ImageRoutingTests(unittest.TestCase):
    def test_artistic_requires_capable_gpt_or_handoff(self):
        for op in routing.ARTISTIC:
            self.assertEqual(routing.route(op), 'handoff_to_gpt')
            self.assertEqual(routing.route(op, True), 'gpt')

    def test_technical_images_remain_coding_work(self):
        for op in routing.TECHNICAL:
            self.assertEqual(routing.route(op), 'coding_model')

    def test_unknown_operation_fails(self):
        with self.assertRaises(ValueError):
            routing.route('guess')

class SharedSkillsTests(unittest.TestCase):
    def test_repository_discovery_paths(self):
        self.assertEqual(check(ROOT), [])

    def test_split_missing_and_inventory_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'.claude/skills/example').mkdir(parents=True)
            (root/'.claude/skills/example/SKILL.md').write_text('example')
            (root/'.claude/shared-skills.json').write_text(json.dumps(['example']))
            (root/'.agents').mkdir()
            (root/'.agents/skills').symlink_to('../.claude/skills', target_is_directory=True)
            self.assertEqual(check(root), [])
            (root/'.claude/skills/new').mkdir()
            self.assertTrue(check(root))
            (root/'.agents/skills').unlink()
            (root/'.agents/skills').mkdir()
            self.assertTrue(check(root))
