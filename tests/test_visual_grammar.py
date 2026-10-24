"""r004 editorial regression: source semantics, no model/media-quality claims."""
import copy
import json
from pathlib import Path
import subprocess
import unittest
from production.visual_grammar import validate_grammar, unit_for_sequence, classification_matrix

ROOT = Path(__file__).resolve().parents[1]
PATH = 'stories/lion_and_mouse_v7/audio_visual_plan.json'

class VisualGrammarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads((ROOT / PATH).read_text())

    def test_r004_source_valid(self):
        self.assertEqual(validate_grammar(self.plan), [])

    def test_every_s01_s08_line_classified_without_future_guess(self):
        expected={l['line_id'] for l in self.plan['lines'] if l['audio_scene'] in {f'S{n:02}' for n in range(1,9)}}
        actual={lid for u in self.plan['visual_units'].values() for lid in u['audio_line_ids']}
        self.assertEqual(actual,expected)
        order=self.plan['owner_editorial_direction']['active_sequence_order']
        self.assertEqual(len(order),len(set(order)))
        self.assertEqual(set(order),set(self.plan['visual_units']))

    def test_legacy_optional(self):
        self.assertEqual(validate_grammar({'lines': []}), [])

    def test_opening_one_forest_unit_no_milo(self):
        unit = unit_for_sequence(self.plan, 's01_opening')
        self.assertEqual(unit, unit_for_sequence(self.plan, 's01_empty_hold'))
        self.assertEqual(unit['visible_cast'], [])
        sequence = self.plan['production_sequences'][unit['sequence_id']]
        self.assertTrue(all(not u.get('image_id', '').startswith('S01-L001') for u in sequence['uses']))
        self.assertEqual(sequence['edges'][0]['method'], 'environment_equal_endpoint')
        self.assertEqual(len([u for u in self.plan['visual_units'].values() if 'S01-L001' in u['audio_line_ids']]), 1)

    def test_s04_and_s02_single_do_not_require_phantom_end(self):
        for sid in ['s02_line_001'] + [f's04_line_{n:03}' for n in range(1,6)]:
            sequence = self.plan['production_sequences'][sid]
            self.assertEqual(len(sequence['uses']), 1)
            self.assertEqual(sequence['edges'], [])
            self.assertEqual(unit_for_sequence(self.plan, sid)['visual_motion'], 'single_i2v')

    def test_shared_root_individual_not_fake_motion(self):
        for sid in ['s05_line_005', 's05_line_006']:
            self.assertEqual(unit_for_sequence(self.plan, sid)['editorial_relationship'], 'individual')
            self.assertEqual(self.plan['production_sequences'][sid]['edges'], [])
        self.assertEqual(self.plan['production_sequences']['s05_line_006']['uses'][0]['alias_of'], 'S05-L005-B01-I01')

    def test_four_placement_uses_two_real_edges_offscreen_rise(self):
        seq = self.plan['production_sequences']['s02_acorn']
        self.assertEqual([u['id'] for u in seq['uses']], ['S02-L004-B01-I02','S02-L004-B02-I01','S02-L004-B02-I02','S02-L004-B02-I03'])
        self.assertEqual([e['kind'] for e in seq['edges']], ['shared_boundary','motion','motion'])
        self.assertEqual(seq['narrated_offscreen_actions'][0]['coverage'], 'narrated_offscreen')
        self.assertNotIn('S02-L004-B01-I01', [u['id'] for u in seq['uses']])
        self.assertTrue(any('beside' in b for b in seq['blockers']))

    def test_fork_all_eight_states_seven_transitions(self):
        seq = self.plan['production_sequences']['s03_fork']
        ends = [u for u in seq['uses'] if u.get('image_id','').endswith('I02')]
        self.assertTrue({f'S03-L{n:03}-B01-I02' for n in range(1,9)}.issubset({u['image_id'] for u in ends}))
        self.assertEqual(sum(e['kind']=='motion' for e in seq['edges']), 7)

    def test_connected_portrait_orthogonal_and_speakers(self):
        for sid, speaker, count in [('s03_portraits','MOUSE',2),('s07_leo_portraits','LION',2),('s07_milo_portraits','MOUSE',3)]:
            u=unit_for_sequence(self.plan,sid)
            self.assertEqual((u['editorial_relationship'],u['composition']),('connected','portrait'))
            self.assertEqual(u['speaker'],speaker)
            self.assertEqual(len(u['audio_line_ids']),count)
        self.assertEqual(unit_for_sequence(self.plan,'s02_line_003')['editorial_relationship'],'individual')

    def test_mixed_narrator_dialogue_is_line_scoped(self):
        u=unit_for_sequence(self.plan,'s08_leo_portraits')
        self.assertIsNone(u['speaker'])
        self.assertEqual(u['mouth_policy'],'dialogue_lipsync')
        self.assertEqual(u['audio_line_ids'],[f'S08-L{n:03}' for n in range(7,12)])
        self.assertEqual(unit_for_sequence(self.plan,'s05_line_010')['mouth_policy'],'no_mouth_driver')

    def test_paw_block_hash_all_three_uses_no_approval_transfer(self):
        block=self.plan['production_blocks']['516ea912c1a726927232e3e6df83a7e7f9eb3a3f54719e24a148f60c6dd94604']
        self.assertEqual(block['affected_image_ids'],[f'S08-L{n:03}-B01-I01' for n in (16,17,18)])
        self.assertEqual(block['status'],'needs_repair')

    def test_wrong_speaker_and_narrator_lipsync_rejected(self):
        p=copy.deepcopy(self.plan);p['visual_units']['s05_line_010']['mouth_policy']='dialogue_lipsync'
        self.assertTrue(any('narrator' in e for e in validate_grammar(p)))
        p=copy.deepcopy(self.plan);p['visual_units']['s02_line_003']['speaker']='LION'
        self.assertTrue(any('speaker conflicts' in e for e in validate_grammar(p)))

    def test_camera_group_reset_rejected(self):
        p=copy.deepcopy(self.plan);p['production_sequences']['s03_portraits']['uses'][0]['camera_and_crop_lock']='different_view'
        self.assertTrue(any('camera/crop' in e for e in validate_grammar(p)))

    def test_duplicate_audio_coverage_and_order_rejected(self):
        p=copy.deepcopy(self.plan);p['visual_units']['s03_portraits']['audio_line_ids'].reverse()
        self.assertTrue(any('story order' in e for e in validate_grammar(p)))
        p=copy.deepcopy(self.plan);p['visual_units']['s01_l002_b01']['audio_scope']='line'
        self.assertTrue(any('duplicate editorial audio' in e for e in validate_grammar(p)))

    def test_display_copy_cannot_mutate_authority(self):
        out=classification_matrix(self.plan);out['units']['s03_portraits']['speaker']='LION'
        self.assertEqual(self.plan['visual_units']['s03_portraits']['speaker'],'MOUSE')

    def test_original_audio_world_and_planned_slots_unchanged(self):
        old=json.loads(subprocess.check_output(['git','show','1a74ab85c605ea864fc249c0346cebbe1e60d8c1:'+PATH],cwd=ROOT))
        for key in ['lines','world_events','world_states','initial_world_state','script_line_order','audio_scenes']:
            self.assertEqual(self.plan[key],old[key],key)

if __name__=='__main__':unittest.main()
