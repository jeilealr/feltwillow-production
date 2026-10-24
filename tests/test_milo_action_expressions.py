"""Action-specific face references preserve scoped body review and source bytes."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from production import character_performance as cp

ROOT=Path(__file__).resolve().parents[1]
REVIEW='review/character_performance_consistency_r001/s04_s05_acting_repairs_r002'

class MiloActionExpressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder,cls.plan,cls.chars,cls.locs,cls.lib=cp.load(ROOT,'lion_and_mouse_v7')
        cls.review=cls.folder/REVIEW

    def binding(self,lid,index=0,plan=None):
        line=next(l for l in (plan or self.plan)['lines'] if l['line_id']==lid)
        return line['beats'][0]['image_sequence']['images'][index]['performance']['Milo']

    def test_emotion_tracks_action_not_one_smile(self):
        for lid,intent in [('S04-L001','hurried_focus'),('S04-L003','low_clearance_focus'),('S05-L005','hurried_focus'),('S05-L007','startled')]:
            self.assertEqual(self.binding(lid)['acting']['intent'],intent)
        self.assertEqual([self.binding('S05-L008',n)['acting']['intent'] for n in range(4)],['startled','startled','falling_panic','falling_panic'])
        self.assertEqual(self.binding('S05-L009',3)['acting']['intent'],'stunned_landing')
        p=copy.deepcopy(self.plan)
        self.binding('S04-L001',plan=p)['expression_id']='milo.expression.hopeful_confidence.3q'
        self.assertTrue(any('action intent' in e for e in cp.validate(self.lib,p,self.chars,ROOT)))

    def test_turn_exit_reused_without_duplicate_file(self):
        self.assertEqual([self.binding('S04-L004',n)['pose_variant'] for n in range(2)],['turn_exit','turn_exit'])
        p=copy.deepcopy(self.plan);self.binding('S04-L004',plan=p)['pose_variant']='turn_entry'
        self.assertTrue(any('superseded turn-entry' in e for e in cp.validate(self.lib,p,self.chars,ROOT)))

    def test_body_only_feedback_preserves_original_receipts(self):
        feedback=json.loads((self.review/'OWNER_FEEDBACK.json').read_text())
        self.assertEqual(sum(r['body']=='owner_retained_body_only' for r in feedback['entries']),12)
        for row in feedback['entries']:
            v=self.lib['assets'][row['asset_id']]['variants'][row['variant']]
            if v['status'] in cp.APPROVED:
                self.assertEqual(v['owner_decision']['scope'],'performance_use_only')
                self.assertEqual(v['owner_decision']['sha256'],v['file']['sha256'])
            else:
                self.assertIsNone(v['owner_decision'])
                self.assertEqual(v['status'],'candidate_pending_owner_review')
            for f in [row['image'],row['image']['sidecar'],v['creation']['receipt']]:
                self.assertEqual(hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest(),f['sha256'])
        changed=copy.deepcopy(self.lib)
        changed['assets']['milo.run.rescue.3q']['variants']['contact']['component_review']['image_sha256']='0'*64
        self.assertTrue(any('component review' in e for e in cp.validate(changed,self.plan,self.chars,ROOT)))

    def test_approved_operation_is_bounded_and_hash_pinned(self):
        op=json.loads((self.review/'OPERATION.json').read_text())
        self.assertEqual((op['request_count'],len(op['requests']),op['automatic_retries']),(7,7,0))
        self.assertEqual(op['status'],'prepared_pending_concrete_owner_approval')
        auth=json.loads((self.review/'AUTHORIZATION.json').read_text())
        self.assertEqual(auth['operation_sha256'],hashlib.sha256((self.review/'OPERATION.json').read_bytes()).hexdigest())
        execution=json.loads((self.review/'EXECUTION.json').read_text())
        self.assertEqual((execution['completed'],len(execution['attempts'])),(7,7))
        self.assertEqual(execution['automatic_retries'],0)
        self.assertIsNone(op['estimated_total_cost'])
        self.assertEqual(sum('/expressions/' in q['output'] for q in op['requests']),5)
        for q in op['requests']:
            variant=self.lib['assets'][q['asset_id']]['variants'][q['variant']]
            self.assertEqual(variant['file']['path'],q['output'])
            self.assertEqual(hashlib.sha256((ROOT/q['output']).read_bytes()).hexdigest(),variant['file']['sha256'])
            self.assertEqual(variant['status'],'candidate_pending_owner_review')
            self.assertIsNone(variant['owner_decision'])
            self.assertNotEqual(q['variant'],'forward_pitch')
            for ref in q['inputs']:
                self.assertEqual(hashlib.sha256((ROOT/ref['path']).read_bytes()).hexdigest(),ref['sha256'])

    def test_faces_are_not_applied_and_no_existing_story_events_change(self):
        old=json.loads((self.review/'before_audio_visual_plan.json').read_text())
        for key in ['world_states','world_events','initial_world_state','state_rules','audio_source','audio_scene_order']:
            self.assertEqual(old[key],self.plan[key])
        self.assertEqual([l for l in old['lines'] if l['line_id'].startswith(('S01-','S02-','S03-'))],[l for l in self.plan['lines'] if l['line_id'].startswith(('S01-','S02-','S03-'))])
        errors=cp.validate(self.lib,self.plan,self.chars,ROOT,gate='image')
        self.assertTrue(any('action expression not applied' in e for e in errors))
        self.assertFalse(cp.validate(self.lib,self.plan,self.chars,ROOT))
