"""Moving-mouth regression tests with known geometry and exact raw pixels."""
import unittest
import cv2
import numpy as np
from feltwillow.mouth_tracking import MouthTracker, TrackingError, composite_frames


class MouthTrackingTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(73)
        self.closed = cv2.GaussianBlur(rng.integers(40, 210, (160, 220, 3), dtype=np.uint8), (3, 3), 0)
        self.opened = self.closed.copy()
        self.opened[82:94, 98:119] = 15
        self.mask = np.zeros((160, 220, 1), np.float32)
        self.mask[82:94, 98:119] = 1
        self.roi = (.43, .49, .57, .63)

    def test_translation_rotation_and_scale_follow_the_face(self):
        tracker = MouthTracker(self.closed, self.opened, self.mask, self.roi)
        for angle, scale, dx, dy in [(0, 1, 13, -7), (7, 1.06, 4, 3)]:
            with self.subTest(angle=angle):
                matrix = cv2.getRotationMatrix2D((110, 80), angle, scale)
                matrix[:, 2] += [dx, dy]
                frame = cv2.warpAffine(self.closed, matrix, (220, 160))
                result, info = tracker.composite(frame, .8)
                found = np.array(info['transform'])
                point = np.array([108, 88, 1.])
                self.assertLess(np.linalg.norm(found @ point-matrix @ point), .6)
                expected_mask = cv2.warpAffine(self.mask[:, :, 0], matrix, (220, 160))
                actual = np.any(result != frame, axis=2)
                self.assertGreater(actual[expected_mask > .9].mean(), .95)
                self.assertTrue(np.array_equal(result[expected_mask == 0], frame[expected_mask == 0]))

    def test_silence_and_boundaries_are_pixel_exact_even_when_occluded(self):
        frames = np.array([self.closed, np.zeros_like(self.closed), self.closed])
        result, report = composite_frames(frames, self.closed, self.opened, self.mask, self.roi, [1, 0, 1])
        np.testing.assert_array_equal(result, frames)
        self.assertEqual(report['rejected_active_frames'], 0)

    def test_mouth_only_occlusion_is_rejected(self):
        frame = self.closed.copy()
        frame[79:97, 95:122] = 255
        with self.assertRaises(TrackingError):
            MouthTracker(self.closed, self.opened, self.mask, self.roi).composite(frame, .8)

    def test_lost_face_fails_production_and_is_reported_in_diagnostic(self):
        frames = np.array([self.closed, np.zeros_like(self.closed), self.closed])
        with self.assertRaisesRegex(TrackingError, 'Frame 1'):
            composite_frames(frames, self.closed, self.opened, self.mask, self.roi, [0, 1, 0])
        result, report = composite_frames(frames, self.closed, self.opened, self.mask, self.roi,
                                         [0, 1, 0], diagnostic=True)
        np.testing.assert_array_equal(result, frames)
        self.assertEqual(report['rejected_active_frames'], 1)

    def test_large_turn_is_rejected(self):
        matrix = cv2.getRotationMatrix2D((110, 80), 40, 1.)
        frame = cv2.warpAffine(self.closed, matrix, (220, 160))
        with self.assertRaises(TrackingError):
            MouthTracker(self.closed, self.opened, self.mask, self.roi).composite(frame, .8)


if __name__ == '__main__':
    unittest.main()


class MouthMaskTests(unittest.TestCase):
    def test_calibration_chin_lighting_is_excluded_from_mask(self):
        import tempfile
        from pathlib import Path
        from PIL import Image
        from production.lip_sync import _anchors_and_mask
        closed = np.full((256,256,3),140,np.uint8)
        opened = closed.copy()
        opened[120:130,110:140] = 20
        opened[150:175,110:145] = 220  # unrelated brighter chin
        with tempfile.TemporaryDirectory() as tmp:
            c,o=Path(tmp)/'closed.png',Path(tmp)/'open.png'
            Image.fromarray(closed).save(c)
            Image.fromarray(opened).save(o)
            _,_,mask=_anchors_and_mask(c,o,(256,256),(.35,.4,.65,.75))
            self.assertGreater(float(mask[123:127,115:135].mean()),.9)
            self.assertEqual(float(mask[150:175,110:145].max()),0)
            self.assertEqual(float(mask[:100].max()),0)
