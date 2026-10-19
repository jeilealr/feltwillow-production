"""Ensure advisory lint cannot conceal stale observations or grant approval."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from production.perceptual_world import validate


class PerceptualWorldTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / 'stories' / 'test'
        self.home.mkdir(parents=True)
        (self.root / 'frame.png').write_bytes(b'image bytes only; pixel inference forbidden')
        self.sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        self.write('keyframe_plan.json', {'story': 'test', 'images': [{
            'id': 'f1', 'scene': 1, 'candidate_path': 'frame.png',
            'sha256': self.sha(self.root / 'frame.png'), 'dialogue_speakers': [],
        }]})
        self.write('staging_plan.json', {'story': 'test', 'frames': [{
            'id': 'f1', 'view': 'medium', 'actors': {'small': {
                'standing_equivalent_height_fraction_after_crop': 0.1,
            }},
        }]})
        self.row = {
            'id': 'f1', 'scene': 1, 'candidate_path': 'frame.png',
            'sha256': self.sha(self.root / 'frame.png'), 'characters_present': ['small'],
            'current_view': 'medium', 'subject_priority': ['small'],
            'perceptual_world': 'small', 'composition_strategy': 'environmental_medium',
            'detail_floor_actor': 'small', 'detail_floor_min_frame_height_fraction': 0.25,
            'readability_result': 'pass',
        }
        self.advisory = {
            'schema': 'feltwillow.perceptual-world-plan.v1', 'story': 'test',
            'status': 'advisory_not_visual_approval',
            'source_sha256': {f: self.sha(self.home / f) for f in
                              ('keyframe_plan.json', 'staging_plan.json')},
            'frames': [self.row],
        }

    def write(self, name, data):
        (self.home / name).write_text(json.dumps(data))

    def check(self):
        self.write('perceptual_world_plan.json', self.advisory)
        return validate(self.home, self.root)

    def test_small_target_warns_without_rejecting_or_writing_sources(self):
        before = {p: p.read_bytes() for p in self.home.iterdir()}
        errors, warnings = self.check()
        self.assertEqual(errors, [])
        self.assertTrue(any('planned small' in w for w in warnings))
        self.assertTrue(all(p.read_bytes() == b for p, b in before.items()))

    def test_replaced_image_invalidates_observation(self):
        (self.root / 'frame.png').write_bytes(b'new revision')
        self.assertTrue(any('bytes differ' in e for e in self.check()[0]))

    def test_staging_changes_require_review_before_rebinding(self):
        path = self.home / 'staging_plan.json'
        path.write_text(path.read_text() + '\n')
        self.assertTrue(any('snapshot stale' in e for e in self.check()[0]))

    def test_duplicate_and_missing_rows_fail(self):
        self.advisory['frames'].append(dict(self.row))
        self.assertTrue(any('duplicate' in e for e in self.check()[0]))
        self.advisory['frames'] = []
        self.assertTrue(any('inventories differ' in e for e in self.check()[0]))

    def test_world_and_exception_cannot_silently_change_cast(self):
        self.row['perceptual_world'] = 'shared'
        self.row['composition_strategy'] = 'establishing_exception'
        errors, _ = self.check()
        self.assertTrue(any('world does not match' in e for e in errors))
        self.assertTrue(any('needs reason' in e for e in errors))

    def test_advisory_cannot_claim_approval(self):
        self.advisory['status'] = 'approved'
        self.assertTrue(any('remain advisory' in e for e in self.check()[0]))

    def test_audit_hash_cannot_follow_another_candidate(self):
        self.row['sha256'] = '0' * 64
        self.assertTrue(any('candidate binding' in e for e in self.check()[0]))

    def test_nonfinite_floor_is_invalid(self):
        self.row['detail_floor_min_frame_height_fraction'] = float('nan')
        self.assertTrue(any('finite fraction' in e for e in self.check()[0]))


if __name__ == '__main__':
    unittest.main()
