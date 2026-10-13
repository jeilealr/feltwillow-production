"""Operator instructions must invoke the blocking gates, not report-only modes."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DocumentedCommandTests(unittest.TestCase):
    def test_chained_skill_uses_strict_operator_commands(self):
        skill = (ROOT / ".claude/skills/audio-chained-coverage/SKILL.md").read_text()
        self.assertIn("image_handoff.py --story <slug> audit --strict", skill)
        self.assertIn("--require-takes --fail-on-flagged-joins", skill)
        self.assertIn("v6_runtime.py --story lion_and_mouse_v6 --preflight", skill)

    def test_root_readme_does_not_run_manifest_tools_on_v6(self):
        readme = (ROOT / "README.md").read_text()
        self.assertNotIn("image_prompts.py --story lion_and_mouse_v6", readme)
        self.assertIn("stories/lion_and_mouse_v6/RUNTIME_CONTRACT.md", readme)

