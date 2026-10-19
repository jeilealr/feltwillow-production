"""Consolidation authority and optional-dependency regressions; no models or media generation."""
import ast
import hashlib
import json
from pathlib import Path
import unittest

from production import keyframe_plan

ROOT = Path(__file__).resolve().parents[1]
STORY = ROOT / 'stories/lion_and_mouse_v6'


class WanFirstRoutingTests(unittest.TestCase):
    def test_current_milo_identity_does_not_attach_superseded_performance_family(self):
        bible = json.loads((STORY / 'visual_bible.json').read_text())
        master = bible['characters']['milo']['canonical']
        self.assertEqual(hashlib.sha256((ROOT / master).read_bytes()).hexdigest(),
                         'c0d500c1a9644eed94b121d1e3205654901ac414fb07723c4a8f7996cdc8ae3f')
        self.assertIsNone(bible['characters']['milo']['expression_board'])
        self.assertIsNone(bible['characters']['milo']['turnaround'])
        for row in keyframe_plan.build('lion_and_mouse_v6')['images']:
            for path in row['references']:
                self.assertNotIn('m_complete_reference_r03_candidate.png', path)
                self.assertNotIn('full-body_milo_neutral_pose_r02_candidate.png', path)

    def test_shared_skill_links_are_contained_single_sources(self):
        for name in ('consistent-image-prompts', 'audio-chained-coverage',
                     'feltwillow-blender-production'):
            source = ROOT / '.claude/skills' / name
            link = ROOT / '.agents/skills' / name
            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), source.resolve())
            self.assertTrue(link.resolve().is_relative_to(ROOT))
            self.assertEqual((link / 'SKILL.md').read_bytes(), (source / 'SKILL.md').read_bytes())

    def test_normal_wan_entrypoints_do_not_import_optional_research(self):
        forbidden = ('bpy', 'VideoX', 'videox', 'tripo', 'patina', 'blender_fun_control')
        for relative in ('feltwillow/wan.py', 'production/shot.py', 'production/v6_runtime.py'):
            tree = ast.parse((ROOT / relative).read_text())
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.append(node.module)
            self.assertFalse([name for name in imports if any(part in name for part in forbidden)], relative)

    def test_v6_has_no_fake_legacy_runtime_inputs(self):
        for name in ('prompt_manifest.json', 'timing_plan.json', 'story.yaml'):
            self.assertFalse((STORY / name).exists())
        direction = (ROOT / 'docs/production-direction.md').read_text()
        self.assertIn('paused, opt-in research', direction)
        self.assertIn('not automatic regeneration', direction)
        self.assertIn('renderer', direction)


if __name__ == '__main__':
    unittest.main()
