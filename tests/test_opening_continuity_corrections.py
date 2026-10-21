"""Owner-directed continuity contracts; no providers or image editing."""
import copy,unittest
from pathlib import Path
from production import audio_visual_plan as av
class ContinuityCorrectionsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.folder,cls.plan,cls.chars,cls.locs=av.load(Path(__file__).resolve().parents[1],'lion_and_mouse_v7')
 def test_fork_root_and_background(self):
  p=copy.deepcopy(self.plan);self.assertEqual(av.shot_continuity_errors(p),[])
  c=p['shot_continuity_contracts']['fork_stationary'];self.assertEqual(len(c['image_ids']),16)
  self.assertEqual(c['reference']['image_id'],'S03-L006-B01-I02')
  line=next(l for l in p['lines'] if l['line_id']=='S03-L001');line['beats'][0]['image_sequence']['images'][0]['performance']['Milo']['travel_direction']='screen_right'
  self.assertTrue(av.shot_continuity_errors(p))
 def test_portrait_body_and_stone_reference(self):
  p=copy.deepcopy(self.plan);c=p['shot_continuity_contracts']['decision_portrait_body']
  self.assertEqual(c['reference']['image_id'],'S03-L010-B01-I01');c['lock_crop']=False;self.assertTrue(av.shot_continuity_errors(p))
  c=p['shot_continuity_contracts']['acorn_background'];self.assertEqual(c['reference']['image_id'],'S02-L004-B01-I02');self.assertEqual(len(c['image_ids']),7)
 def test_acorn_continuous_squat_and_damage(self):
  line=next(l for l in self.plan['lines'] if l['line_id']=='S02-L004');a,b=line['beats']
  self.assertEqual(a['transition_out'],'shared_boundary');self.assertEqual(b['transition_in'],'shared_boundary')
  self.assertEqual(b['image_sequence']['images'][0]['reuse_of'],a['image_sequence']['images'][-1]['id'])
  self.assertEqual(b['image_sequence']['mode'],'multi_key')
  self.assertEqual(self.plan['continuity_groups']['acorn_placement']['motion_policy'],'continuous_no_cut')
  contract=self.plan['prop_visual_contracts']['story_acorn_tasted']
  self.assertEqual(contract['size_reference']['image_id'],'S02-L004-B01-I02')
  self.assertEqual(contract['condition_state'],'tasted');self.assertTrue(contract['no_visible_character_teeth'])
  self.assertEqual(len(contract['image_ids']),6)
  self.assertEqual(av.validate(self.plan,self.chars,self.locs),[])
 def test_whole_acorn_precedes_taste_and_shared_setup(self):
  p=copy.deepcopy(self.plan)
  b=next(l for l in p['lines'] if l['line_id']=='S01-L004')['beats'][2]
  a,z=b['image_sequence']['images'][-2:]
  self.assertEqual((a['id'],a['role']),('S01-L004-B03-I03','key'))
  self.assertEqual((z['id'],z['role']),('S01-L004-B03-I04','end'))
  self.assertEqual(p['world_states'][a['state']]['props']['acorn']['condition'],'whole')
  self.assertEqual(p['world_states'][z['state']]['props']['acorn']['condition'],'tasted')
  event=p['prop_visual_contracts']['story_acorn_whole_before_eating']['next_event']
  self.assertNotIn(event,a['events_before']);self.assertIn(event,z['events_before'])
  self.assertEqual(z['status'],'planned');self.assertFalse(z.get('path'))
  first=next(l for l in p['lines'] if l['line_id']=='S02-L001')['beats'][0]
  later=next(l for l in p['lines'] if l['line_id']=='S02-L004')['beats'][0]
  self.assertEqual(first['location_view'],later['location_view'])
  self.assertEqual(first['background_continuity'],'locked_background')
  for im in first['image_sequence']['images']:
   self.assertEqual(im['shot_continuity_contract'],'acorn_background')
  a['state']=z['state']
  self.assertTrue(any('pre-eating' in e for e in av.shot_continuity_errors(p)))
 def test_opening_honest_alignment(self):
  line=self.plan['lines'][0];coverage=line['editorial_coverage'];self.assertEqual(coverage['total_seconds'],line['audio']['duration_seconds']);self.assertEqual(coverage['alignment_status'],'pending_alignment');self.assertIsNone(coverage['cut_time_seconds']);self.assertTrue(all(s['duration_seconds'] is None for s in coverage['stages']))
if __name__=='__main__':unittest.main()
