import json
from pathlib import Path
import unittest

from production.canonical_measurements import quantity,measure_actor


class CanonicalMeasurementTests(unittest.TestCase):
    def test_horizontal_width_is_registered_and_scale_invariant(self):
        points={'a':{'xy':[20,50],'uncertainty_pixels':2},'b':{'xy':[80,50],'uncertainty_pixels':2}}
        record={'method':'horizontal_span','points':['a','b'],'scope':'visible panel, arms excluded','station':{'canonical_fraction':0.51}}
        q=quantity(record,points)
        self.assertEqual(q['value_pixels'],60)
        self.assertEqual(q['uncertainty_pixels'],4)
        self.assertEqual(q['station']['canonical_fraction'],0.51)
        points['b']['xy'][1]=70
        with self.assertRaises(ValueError):quantity(record,points)

    def test_horizontal_profiles_separate_patch_body_and_occluded_anatomy(self):
        root=Path(__file__).resolve().parents[1]
        source=json.loads((root/'stories/lion_and_mouse_v7/canonical_proportion_landmarks.json').read_text())
        m=source['actors']['Milo'];l=source['actors']['Leo']
        measured=measure_actor(m)
        self.assertEqual(len(measured['ratios']),36)
        self.assertEqual(measured['quantities']['belly_visible_panel_width']['value_pixels'],220)
        self.assertEqual(measured['quantities']['cream_patch_belly_width']['value_pixels'],135)
        self.assertAlmostEqual(measured['ratios']['cream_belly_to_torso_panel_width']['value'],135/220)
        self.assertIn('full_chest_width',measured['unavailable'])
        self.assertNotIn('full_chest_width',measured['ratios'])
        self.assertIn('near_hind_thigh_to_hindpaw_width',measure_actor(l)['ratios'])
        self.assertNotIn('cream_belly_to_torso_panel_width',measure_actor(l)['ratios'])
        # Scaling source coordinates and their annotation uncertainty changes
        # pixel lengths, not the ratio or its conservative interval.
        import copy
        scaled=copy.deepcopy(m)
        for point in scaled['points'].values():
            point['xy']=[v*2 for v in point['xy']];point['uncertainty_pixels']*=2
        a=measure_actor(m)['ratios']['belly_panel_to_head_width']
        b=measure_actor(scaled)['ratios']['belly_panel_to_head_width']
        self.assertEqual(a,b)

    def test_paw_views_and_partial_occlusion_are_not_interchangeable(self):
        root=Path(__file__).resolve().parents[1]
        source=json.loads((root/'stories/lion_and_mouse_v7/canonical_proportion_landmarks.json').read_text())
        m=measure_actor(source['actors']['Milo']);l=measure_actor(source['actors']['Leo'])
        self.assertEqual(m['quantities']['near_foot_front_view_span']['value_pixels'],159)
        self.assertEqual(m['quantities']['far_foot_side_view_span']['value_pixels'],213)
        self.assertIn('CLOSED',m['quantities']['near_closed_hand_span']['scope'])
        self.assertIn('EXPOSED PART',l['quantities']['far_hindpaw_exposed_span']['scope'])
        self.assertIn('full_far_hindpaw_width',l['unavailable'])
        self.assertNotIn('full_far_hindpaw_width',l['ratios'])
        self.assertEqual(len(l['ratios']),29)

    def test_active_gallery_combines_all_annotations_once_per_character(self):
        root=Path(__file__).resolve().parents[1]
        folder=root/'stories/lion_and_mouse_v7/review/character_performance_consistency_r001'
        page=(folder/'pose_library/review.html').read_text()
        for actor in ('milo','leo'):
            self.assertEqual(page.count('src="../canonical_measurements_r001/'+actor+'_combined_annotated.jpg"'),1)
            self.assertNotIn('src="../canonical_measurements_r001/'+actor+'_widths_annotated.jpg"',page)
        self.assertNotIn('<summary>Show annotated canonical images: Milo and Leo</summary>',page)
        from production.serve_scene_review import review_assets
        assets=review_assets(root)
        for actor in ('milo','leo'):
            target=folder/'canonical_measurements_r001'/(actor+'_combined_annotated.jpg')
            self.assertIn('/'+target.relative_to(root).as_posix(),assets)

    def test_bent_surface_path_is_not_joint_or_chord(self):
        points={'a':{'xy':[0,0],'uncertainty_pixels':1},'b':{'xy':[3,0],'uncertainty_pixels':1},'c':{'xy':[3,4],'uncertainty_pixels':1}}
        q=quantity({'method':'polyline','points':['a','b','c'],'scope':'surface only'},points)
        self.assertEqual(q['value_pixels'],7)
        self.assertEqual(q['uncertainty_pixels'],4)
        self.assertEqual(q['scope'],'surface only')

    def test_observations_do_not_reconcile_identity_or_invent_hidden_joints(self):
        root=Path(__file__).resolve().parents[1]
        source=json.loads((root/'stories/lion_and_mouse_v7/canonical_proportion_landmarks.json').read_text())
        leo=measure_actor(source['actors']['Leo'])
        self.assertEqual(leo['identity_status'],'canonical_bytes_match_owner_reconciliation')
        self.assertIn('forelimb_segments',leo['unavailable'])
        self.assertNotIn('forelimb_segments',leo['ratios'])
        self.assertFalse(leo['ratios']['mane_to_visible_face_width']['owner_measurement_approval'])

    def test_milo_head_baseline_and_requested_band_are_separate(self):
        root=Path(__file__).resolve().parents[1]
        folder=root/'stories/lion_and_mouse_v7'
        source=json.loads((folder/'canonical_proportion_landmarks.json').read_text())
        obs=measure_actor(source['actors']['Milo'])['ratios']['projected_head_fraction']
        self.assertAlmostEqual(obs['value'],375/950)
        profile=json.loads((folder/'character_performance_library.json').read_text())['anatomy_policies']['Milo']['ratio_profile']
        self.assertEqual(profile['ratios']['projected_head_fraction']['target'],0.39)
        self.assertEqual(profile['ratios']['projected_head_fraction']['tolerance'],0.01)
        self.assertGreater(obs['interval'][1]-obs['interval'][0],0.02)


if __name__=='__main__':unittest.main()
