import copy
import json
import unittest
from production import staging_contract

class OwnerScaleOverrideTests(unittest.TestCase):
    def test_selected_home_scale_passes_and_changed_reference_fails(self):
        home = staging_contract.REPO / 'stories/lion_and_mouse_v6'
        contract = json.loads((home/'staging_plan.json').read_text())
        bible = json.loads((home/'visual_bible.json').read_text())
        self.assertEqual(staging_contract.validate_contract(contract, bible), [])
        broken = copy.deepcopy(contract)
        frame = next(x for x in broken['frames'] if x['id']=='s09_p02')
        frame['actors']['milo']['owner_scale_override']['sha256'] = '0'*64
        errors = staging_contract.validate_contract(broken, bible)
        self.assertTrue(any('owner scale override' in e for e in errors))

    def test_unapproved_override_cannot_bypass_depth_sizing(self):
        home = staging_contract.REPO / 'stories/lion_and_mouse_v6'
        contract = json.loads((home/'staging_plan.json').read_text())
        bible = json.loads((home/'visual_bible.json').read_text())
        frame = next(x for x in contract['frames'] if x['id']=='s09_p02')
        frame['actors']['milo']['owner_scale_override']['status'] = 'pending_owner_review'
        errors = staging_contract.validate_contract(contract, bible)
        self.assertTrue(any('owner scale override' in e for e in errors))
        self.assertTrue(any('height must follow' in e for e in errors))
