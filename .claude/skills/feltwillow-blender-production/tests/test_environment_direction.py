import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from environment_direction import validate, pairs

class DirectionTests(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).resolve().parents[1] / 'assets/templates/environment-direction.json'
        self.doc = json.loads(path.read_text())
        self.doc['owner_direction'] = {'text': 'Use imagery as inspiration for a richer handmade world', 'scope': 'S05 new candidate only'}
        self.doc['target_environment']['id'] = 'great_tree'
        self.doc['story_requirements'] = ['Supported resting area and clear approach']
    def test_inspired_valid(self): self.assertEqual(validate(self.doc), [])
    def test_match_valid(self):
        self.doc['mode']='plate_match'; self.doc['source_roles']=['matching_target'];self.doc['review']['target']='plate_correspondence_and_style'
        self.assertEqual(validate(self.doc), [])
    def test_original_valid(self):
        self.doc['mode']='original_design';self.doc['source_roles']=[]
        self.assertEqual(validate(self.doc), [])
    def test_unknown_mode(self): self.doc['mode']='anything';self.assertTrue(validate(self.doc))
    def test_nonstring_mode(self): self.doc['mode']=[];self.assertTrue(validate(self.doc))
    def test_wrong_review_mode(self): self.doc['review']['target']='plate_correspondence_and_style';self.assertTrue(validate(self.doc))
    def test_inspired_cannot_require_old_match(self): self.doc['source_roles'].append('matching_target');self.assertTrue(validate(self.doc))
    def test_match_needs_target(self): self.doc['mode']='plate_match';self.assertTrue(validate(self.doc))
    def test_scale_invariant_required(self): self.doc['invariants'].remove('character_physical_scale');self.assertTrue(validate(self.doc))
    def test_automatic_approval_refused(self): self.doc['review']['automatic_visual_approval']=True;self.assertTrue(validate(self.doc))
    def test_publication_refused(self): self.doc['target_environment']['status']='approved';self.assertTrue(validate(self.doc))
    def test_spend_separate(self): self.doc['spend_approved']=True;self.assertTrue(validate(self.doc))
    def test_legacy_preserved(self): self.doc['legacy_outputs_policy']='overwrite';self.assertTrue(validate(self.doc))
    def test_missing_continuity(self): del self.doc['continuity_policy'];self.assertTrue(validate(self.doc))
    def test_owner_scope_required(self): self.doc['owner_direction']['scope']='';self.assertTrue(validate(self.doc))
    def test_template_not_ready(self):
        doc=json.loads((Path(__file__).resolve().parents[1]/'assets/templates/environment-direction.json').read_text());self.assertTrue(validate(doc))
    def test_not_mutated(self):
        before=copy.deepcopy(self.doc);validate(self.doc);self.assertEqual(before,self.doc)
    def test_duplicate_keys(self):
        with self.assertRaises(ValueError):json.loads('{"mode":1,"mode":2}',object_pairs_hook=pairs)
    def test_wrong_types(self):
        for field in ['source_roles','invariants','required_views','creative_freedoms']:
            with self.subTest(field=field):
                doc=copy.deepcopy(self.doc);doc[field]=None;self.assertTrue(validate(doc))
    def test_nonobject(self): self.assertTrue(validate([]))

if __name__ == '__main__': unittest.main()
