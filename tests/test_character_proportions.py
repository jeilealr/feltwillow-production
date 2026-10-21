import copy
import math
from pathlib import Path
import unittest

from production import character_proportions as ratios
from production import character_performance as cp


class RatioTests(unittest.TestCase):
    def test_bent_limb_uses_joint_chain_not_chord(self):
        bent=[(0,0),(40,0),(40,40)]
        straight=[(0,0),(40,0),(80,0)]
        self.assertEqual(ratios.chain_length(bent),ratios.chain_length(straight))
        self.assertAlmostEqual(ratios.chain_length(bent),80)
        self.assertLess(math.dist(bent[0],bent[-1]),80)

    def test_scale_invariance_and_absolute_tolerance(self):
        a=ratios.ratio_screen(37,100,0.1,0.1,0.37,0.01,True)
        b=ratios.ratio_screen(370,1000,1,1,0.37,0.01,True)
        self.assertEqual(a,b)
        self.assertEqual(a['target_band'],[0.36,0.38])
        self.assertEqual(a['status'],'within_band')
        self.assertFalse(a['approval'])

    def test_uncertainty_and_foreshortening_do_not_false_pass(self):
        self.assertEqual(ratios.ratio_screen(37,100,4,4,0.37,0.01,True)['status'],'uncertain')
        self.assertEqual(ratios.ratio_screen(43,100,0.1,0.1,0.37,0.01,True)['status'],'outside_band')
        self.assertEqual(ratios.ratio_screen(37,100,0,0,0.37,0.01,False,'out-of-plane arm')['status'],'not_comparable')
        with self.assertRaises(ValueError):ratios.ratio_screen(37,100,0,100,0.37,0.01,True)

    def test_species_profiles_bind_own_canonical_and_do_not_copy_metrics(self):
        root=Path(__file__).resolve().parents[1]
        folder,plan,chars,locs,library=cp.load(root,'lion_and_mouse_v7')
        policies=library['anatomy_policies']
        for actor in ['Milo','Leo']:
            profile=policies[actor]['ratio_profile']
            self.assertEqual(profile['canonical'],cp.canonical_record(chars,actor))
            self.assertEqual(ratios.validate_profile(profile),[])
        m=policies['Milo']['ratio_profile'];l=policies['Leo']['ratio_profile']
        self.assertIn('projected_head_fraction',m['ratios'])
        self.assertNotIn('projected_head_fraction',l['ratios'])
        self.assertIn('mane_to_head',l['ratios'])
        self.assertNotIn('mane_to_head',m['ratios'])
        self.assertTrue(all(r['target'] is None for r in l['ratios'].values()))
        changed=copy.deepcopy(library)
        changed['anatomy_policies']['Leo']['ratio_profile']=copy.deepcopy(m)
        self.assertTrue(any('ratios belong' in e for e in cp.validate(changed,plan,chars)))

    def test_pending_calibration_never_invents_tolerance(self):
        profile={'tolerance_units':'absolute_ratio','ratios':{'arm':{'definition':'joint chain / torso','comparability':'in plane','target':None,'tolerance':0.1,'calibration_status':'pending_reference_measurement'}}}
        self.assertTrue(ratios.validate_profile(profile))

    def test_gallery_excludes_stale_comparison_after_replacement(self):
        from production.performance_review_gallery import comparison_is_current
        library={'assets':{'milo.pose':{'variants':{'default':{'file':{'path':'new.png','sha256':'a'*64}}}}}}
        old={'rows':[{'asset_id':'milo.pose','variant':'default','source':{'path':'old.png','sha256':'b'*64}}]}
        self.assertFalse(comparison_is_current(library,old))
        old['rows'][0]['source']={'path':'new.png','sha256':'a'*64}
        self.assertTrue(comparison_is_current(library,old))
        old['rows'][0]['source']['sha256']='b'*64
        self.assertFalse(comparison_is_current(library,old))

    def test_profile_change_invalidates_previously_bound_anatomy_review(self):
        root=Path(__file__).resolve().parents[1]
        folder,plan,chars,locs,library=cp.load(root,'lion_and_mouse_v7')
        library=copy.deepcopy(library)
        v=library['assets']['milo.acorn.pick_hold.3q']['variants']['hold']
        v['anatomy_review'].update(status='matched_reviewed_reference',comparison_method='synthetic review fixture only',evidence={'path':'synthetic.json','sha256':'0'*64},profile_sha256=cp.ratio_profile_digest(library['anatomy_policies']['Milo']['ratio_profile']))
        self.assertTrue(any('horizontal' in x for x in cp.anatomy_blockers(library,'Milo',v)))
        v['anatomy_review']['horizontal_review']={'scope':'body','evidence':{'path':'synthetic.json','sha256':'0'*64},'checks':{k:'matched_in_compatible_view' for k in ('body_bulk','cream_patch','limb_bulk')}}
        self.assertEqual(cp.anatomy_blockers(library,'Milo',v),[])
        library['anatomy_policies']['Milo']['ratio_profile']['ratios']['projected_head_fraction']['tolerance']=0.02
        self.assertTrue(cp.anatomy_blockers(library,'Milo',v))
        proposal=cp.proposal(root,folder,library,plan,chars,locs,'S01-L004-B03-I02')
        self.assertEqual(proposal['proportion_profiles']['Milo']['actor'],'Milo')
        self.assertNotIn('Leo',proposal['proportion_profiles'])

    def test_horizontal_review_requires_body_or_portrait_evidence_separately(self):
        root=Path(__file__).resolve().parents[1]
        folder,plan,chars,locs,library=cp.load(root,'lion_and_mouse_v7')
        library=copy.deepcopy(library)
        portrait=library['assets']['milo.portrait.base.3q']['variants']['default']
        review={'scope':'body','evidence':{'path':'synthetic.json','sha256':'0'*64},'checks':{k:'matched_in_compatible_view' for k in ('body_bulk','cream_patch','limb_bulk')}}
        portrait['anatomy_review']['horizontal_review']=review
        self.assertTrue(cp.horizontal_review_blockers(library,'Milo',portrait))
        review.update(scope='portrait',checks={k:'matched_in_compatible_view' for k in ('head_width','ear_width','eye_spacing')})
        self.assertEqual(cp.horizontal_review_blockers(library,'Milo',portrait),[])
        review['checks']['ear_width']='not_comparable'
        self.assertTrue(cp.horizontal_review_blockers(library,'Milo',portrait))


if __name__=='__main__':unittest.main()
