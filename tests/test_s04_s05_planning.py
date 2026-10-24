"""Owner-directed shortcut, rear-paw trip and portrait planning regressions."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from production import audio_visual_plan as av
from production import character_performance as cp

ROOT=Path(__file__).resolve().parents[1]
REVIEW='review/character_performance_consistency_r001/s04_s05_pose_planning_r001'


class S04S05PlanningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder,cls.plan,cls.chars,cls.locs,cls.lib=cp.load(ROOT,'lion_and_mouse_v7')

    def line(self,lid,plan=None):
        return next(l for l in (plan or self.plan)['lines'] if l['line_id']==lid)

    def test_s04_independent_style_only_views(self):
        for n in range(1,6):
            b=self.line(f'S04-L{n:03d}')['beats'][0]
            self.assertEqual(b['background_continuity'],'independent_scene')
            self.assertIsNone(b['continuity_group'])
            v=self.locs['views'][b['location_view']]
            self.assertEqual(v['reference_usage'],'style_and_material_only')
            self.assertFalse(v['inherit_reference_geography'])

    def test_sleeping_details_and_fixed_action_world(self):
        for n in range(1,5):
            b=self.line(f'S05-L{n:03d}')['beats'][0]
            self.assertEqual(b['background_continuity'],'same_place_new_view')
            for im in b['image_sequence']['images']:
                self.assertFalse(self.plan['world_states'][im['state']]['actors']['Leo']['awake'])
                self.assertEqual(im['performance']['Leo']['pose_id'],'leo.sleep.rear_paw_path.3q')
        beats=[self.line(f'S05-L{n:03d}')['beats'][0] for n in range(8,10)]
        self.assertEqual(len({b['location_view'] for b in beats}),1)
        self.assertTrue(all(b['background_continuity']=='locked_background' for b in beats))
        self.assertEqual(self.plan['continuity_groups']['great_tree_trip']['obstacle_limb'],'rear_paw')
        self.assertEqual(self.plan['continuity_groups']['great_tree_trip']['later_blocking_limb'],'front_paw')
        root=self.line('S05-L005')['beats'][0]
        conjunction=self.line('S05-L006')['beats'][0]
        portrait=self.line('S05-L007')['beats'][0]
        for b in [root,conjunction,portrait]:
            self.assertEqual(b['cast'],['Milo'])
            self.assertEqual(b['offscreen_cast'],['Leo'])
            self.assertTrue(all(set(i['performance'])=={'Milo'} for i in b['image_sequence']['images']))
        self.assertEqual(root['image_sequence']['mode'],'single')
        self.assertEqual(root['transition_out'],'shared_boundary')
        self.assertEqual(conjunction['image_sequence']['images'][0]['reuse_of'],root['image_sequence']['images'][-1]['id'])
        self.assertEqual(portrait['shot_type'],'portrait')
        self.assertEqual(portrait['image_sequence']['images'][0]['performance']['Milo']['pose_id'],'milo.portrait.base.3q')

    def test_four_trip_keys_and_distinct_tumble_event_order(self):
        b=self.line('S05-L008')['beats'][0];images=b['image_sequence']['images']
        self.assertEqual(len(images),4)
        self.assertEqual([i['role'] for i in images],['start','key','key','end'])
        self.assertEqual([i['performance']['Milo']['pose_variant'] for i in images],['approach','paw_contact','forward_pitch','trip'])
        self.assertEqual([e for i in images for e in i['events_before']],['S05-L008-B01-E01'])
        self.assertTrue(all(self.plan['world_states'][i['state']]['actors']['Milo']['support']=='unbalanced_paw_contact' for i in images[1:]))
        later=self.line('S05-L009')['beats'][0]['image_sequence']['images']
        self.assertEqual([i['performance']['Milo']['pose_variant'] for i in later],['support_lost','tumble','roll','nose_landing'])
        p=copy.deepcopy(self.plan);self.line('S05-L008',p)['beats'][0]['image_sequence']['images'].pop(2)
        # Keep numbering valid so the authored minimum itself must fail.
        self.line('S05-L008',p)['beats'][0]['image_sequence']['images'][-1]['id']='S05-L008-B01-I03'
        self.assertTrue(any('minimum image' in e for e in av.validate(p,self.chars,self.locs)))

    def test_portraits_preserve_offscreen_mouse_state(self):
        for lid in ['S05-L010','S05-L011']:
            b=self.line(lid)['beats'][0]
            self.assertEqual((b['shot_type'],b['cast'],b['offscreen_cast']),('portrait',['Leo'],['Milo']))
            self.assertEqual(b['portrait_geometry_group'],'leo_wake_portrait')
            for im in b['image_sequence']['images']:
                self.assertEqual(self.plan['world_states'][im['state']]['actors']['Milo']['anchor'],'leo_nose_contact')
                self.assertEqual(set(im['performance']),{'Leo'})
        self.assertTrue(self.plan['portrait_geometry_groups']['leo_wake_portrait']['lock_visible_body_extent'])

    def test_original_media_audio_and_opening_unchanged(self):
        old=av.read(self.folder/REVIEW/'before_audio_visual_plan.json')
        for a,b in zip(self.plan['lines'],old['lines']):
            self.assertEqual(a['audio'],b['audio'])
            if a['audio_scene'] in ['S01','S02','S03']:
                self.assertEqual(a,b)
        for key in ['world_events','world_states','state_rules']:
            self.assertEqual(self.plan[key],old[key])
        self.assertEqual(cp.immutable_errors(ROOT,self.folder),[])

    def test_exact_milo_proposal_does_not_include_leo_or_fake_assets(self):
        op=av.read(self.folder/REVIEW/'OPERATION.json')
        self.assertEqual((op['request_count'],op['automatic_retries']),(16,0))
        self.assertIsNone(op['estimated_total_cost'])
        for q in op['requests']:
            self.assertEqual(q['actor'],'Milo');self.assertTrue(q['arguments']['transparent_background'])
            variant=self.lib['assets'][q['asset_id']]['variants'][q['variant']]
            if q['sequence']==11:
                self.assertEqual(variant['status'],'planned');self.assertIsNone(variant['file'])
                self.assertFalse((ROOT/q['output']).exists())
            else:
                if variant['status'] in cp.APPROVED:
                    self.assertEqual(variant['owner_decision']['scope'],'performance_use_only')
                    self.assertEqual(variant['owner_decision']['sha256'],variant['file']['sha256'])
                else:
                    self.assertEqual(variant['status'],'candidate_pending_owner_review')
                    self.assertIsNone(variant['owner_decision'])
                current_or_history=[variant['file']]+[r['file'] for r in variant.get('superseded_candidates',[])]
                self.assertIn(q['output'],[f['path'] for f in current_or_history])
                self.assertTrue((ROOT/q['output']).is_file())
            for ref in q['inputs']:
                self.assertEqual(hashlib.sha256((ROOT/ref['path']).read_bytes()).hexdigest(),ref['sha256'])
        self.assertEqual(av.validate(self.plan,self.chars,self.locs),[])

    def test_generated_batch_journal_and_leo_reconciliation(self):
        execution=av.read(self.folder/REVIEW/'EXECUTION.json')
        self.assertEqual(execution['completed'],15)
        self.assertEqual(len(execution['attempts']),16)
        self.assertEqual(execution['automatic_retries'],0)
        self.assertEqual(execution['attempts']['10']['status'],'connection_failure_no_output_returned_outcome_unresolved')
        record=av.read(self.folder/'owner_leo_canonical_reconciliation_r001.json')
        canonical=self.chars['characters']['Leo']['canonical']
        self.assertEqual(canonical['sha256'],record['canonical']['sha256'])
        self.assertEqual(hashlib.sha256((ROOT/canonical['path']).read_bytes()).hexdigest(),canonical['sha256'])
        self.assertFalse(record['image_bytes_changed'])
        self.assertFalse(record['Leo_generation_authorized'])
