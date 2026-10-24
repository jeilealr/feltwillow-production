"""Compositor changes must invalidate previously rendered mouth takes."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from feltwillow import paths
from feltwillow.lipsync import recipe_sha256


class LipSyncRecipeTests(unittest.TestCase):
    def test_code_and_calibration_bytes_are_part_of_recipe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            story = root/'stories/story'
            audio = root/'work/stories/story/audio/en'
            story.mkdir(parents=True)
            (audio/'lines').mkdir(parents=True)
            (root/'production').mkdir()
            (root/'feltwillow').mkdir()
            for path in ('production/lip_sync.py','feltwillow/mouth_tracking.py','closed.png','open.png'):
                (root/path).write_bytes(b'original')
            (audio/'lines/line.wav').write_bytes(b'recorded audio')
            docs = {
                story/'timing_plan.json': {'segments':[{'piece':'p','mode':'mouth','variant':'v','lines':['line']}]},
                story/'prompt_manifest.json': {'shots':[{'id':'p','start_image':'closed','end_image':'closed','variants':[{'id':'v','mouth_open_image':'open'}]}],
                                              'images':[{'id':'open','target':'open.png'},{'id':'closed','target':'closed.png'}]},
                story/'visual_bible.json': {}, story/'dialogue_coverage.json': {},
                audio/'timing.json': {}, audio/'word_timings.json': {'lines':{'line':{'audio_file':'lines/line.wav'}}}}
            for path,doc in docs.items():
                path.write_text(json.dumps(doc))
            with patch.object(paths,'REPO',root), patch.object(paths,'STORIES',root/'stories'), patch.object(paths,'WORK',root/'work'):
                initial = recipe_sha256('story','p')
                self.assertIsNotNone(initial)
                self.assertEqual(initial,recipe_sha256('story','p'))
                (root/'feltwillow/mouth_tracking.py').write_bytes(b'tracker revision')
                revised = recipe_sha256('story','p')
                self.assertNotEqual(initial,revised)
                (root/'open.png').write_bytes(b'new calibration')
                self.assertNotEqual(revised,recipe_sha256('story','p'))


if __name__ == '__main__':
    unittest.main()
