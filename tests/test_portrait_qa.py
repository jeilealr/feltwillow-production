import copy
import unittest
import numpy as np
from feltwillow.portrait_qa import assess_frames, region_mask


def fixture():
    frame = np.random.default_rng(4).integers(0, 256, (96, 96, 3), dtype=np.uint8)
    contract = dict(status='reviewed', reviewer='synthetic-qa', allowed_change_roi=[.3,.3,.7,.65], body_exclusion_roi=[0,.8,1,1], limits=dict(pixel_delta=4, protected_change_fraction=.01, body_change_fraction=.01, max_translation_px=1, max_scale_delta=.02))
    return frame, contract


class PortraitQATests(unittest.TestCase):
    def test_stable_source_and_local_expression_are_structurally_valid(self):
        frame, contract=fixture(); frames=np.stack([frame]*3)
        frames[1,40:44,40:44]=0
        report=assess_frames(frame, frames, contract)
        self.assertEqual([], report['warnings'])
        self.assertEqual('pending; metrics cannot certify limbs, teeth, identity or whole-motion quality',report['visual_review'])

    def test_new_hand_in_body_exclusion_flags_intrusion(self):
        frame, contract=fixture(); frames=np.stack([frame]*3);frames[1,80:96,40:60]=255
        report=assess_frames(frame,frames,contract)
        self.assertIn('portrait_intrusion',{w['kind'] for w in report['warnings']})

    def test_camera_zoom_or_shift_flags_geometry(self):
        frame, contract=fixture(); frames=np.stack([frame,np.roll(frame,5,axis=1)])
        report=assess_frames(frame,frames,contract)
        self.assertTrue(any(w['kind'] in {'portrait_crop_or_protected_change','portrait_camera_or_scale_drift'} for w in report['warnings']))

    def test_featureless_source_is_unavailable_not_pass(self):
        frame, contract=fixture();frame[:]=100
        report=assess_frames(frame,np.stack([frame]*2),contract)
        self.assertIn('portrait_motion_measurement_unavailable',{w['kind'] for w in report['warnings']})

    def test_regions_and_review_fail_closed(self):
        frame,contract=fixture()
        for roi in ([0,0,0,1],[0,0,1,2],[0,0,float('nan'),1]):
            with self.assertRaises(ValueError):region_mask(frame.shape,roi)
        bad=copy.deepcopy(contract);bad['body_exclusion_roi']=[0,.5,1,1]
        with self.assertRaisesRegex(ValueError,'overlap'):assess_frames(frame,np.stack([frame]),bad)
        bad=copy.deepcopy(contract);bad['status']='pending'
        with self.assertRaises(ValueError):assess_frames(frame,np.stack([frame]),bad)
        bad=copy.deepcopy(contract);bad['limits']['body_change_fraction']=2
        with self.assertRaises(ValueError):assess_frames(frame,np.stack([frame]),bad)
