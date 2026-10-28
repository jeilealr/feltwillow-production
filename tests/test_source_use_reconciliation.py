"""Current source-use regression: approved portrait reuse is not a world-state alias."""
import json
from pathlib import Path
import unittest
from production.sequence_plan import resolve_sequence

ROOT = Path(__file__).resolve().parents[1]

class SourceUseReconciliationTests(unittest.TestCase):
    def test_s08_reuse_resolves_each_authored_state(self):
        plan = json.loads((ROOT/'stories/lion_and_mouse_v7/audio_visual_plan.json').read_text())
        result = resolve_sequence(plan, 's08_leo_portraits', ROOT)
        wanted = {'S08-L008-B01-I01', 'S08-L009-B01-I01', 'S08-L010-B01-I01', 'S08-L010-B01-I02'}
        rows = [r for r in result['resolved_images'] if r['id'] in wanted]
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertEqual(row['status'], 'selected_exact')
            self.assertEqual(row['source']['sha256'], '42a0353c33ab781fcc5a4b796ddbbda84abd49a93b503ffc9c52279bb5d0f81c')
            self.assertNotIn('alias_target', row)
        images = {i['id']:i for line in plan['lines'] for beat in line['beats'] for i in beat['image_sequence']['images']}
        self.assertNotEqual(images['S08-L010-B01-I01']['state'], images['S08-L010-B01-I02']['state'])
        self.assertEqual(images['S08-L010-B01-I02']['location_view'], 'great_tree__paw_release__dusk')

    def test_bite_contact_does_not_falsify_pickup_slots(self):
        plan = json.loads((ROOT/'stories/lion_and_mouse_v7/audio_visual_plan.json').read_text())
        result = resolve_sequence(plan, 's01_tiny_bite', ROOT)
        for row in result['resolved_images'][:2]:
            self.assertEqual(row['status'], 'missing_distinct_state')
            self.assertNotIn('source', row)
