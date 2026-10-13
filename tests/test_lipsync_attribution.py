"""Speaker attribution and silent-mouth boundaries for timed dialogue."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from feltwillow import paths
from production.lip_sync import piece_word_cues, render_piece


class LipSyncAttributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.stories = root / "stories"
        self.story = self.stories / "test_story"
        self.story.mkdir(parents=True)
        self.audio = root / "audio"
        self.audio.mkdir()
        self.audio_lines = self.audio / "lines"
        self.audio_lines.mkdir()
        self.lines = [
            {"id": "n", "scene": 1, "speaker": "NARRATOR", "text": "A lion."},
            {"id": "l", "scene": 1, "speaker": "LION", "text": "Hello."},
            {"id": "m", "scene": 1, "speaker": "MOUSE", "text": "Hi."},
        ]
        self.row = {"piece": "p", "variant": "lion_mouth", "mode": "mouth", "scene": 1,
                    "film_start": 0.0, "seconds": 5.0, "lines": ["n", "l", "m"]}
        self._write(self.story / "timing_plan.json", {"audio_story": "audio_story", "lang": "en",
                                                       "segments": [self.row]})
        self._write(self.story / "dialogue_coverage.json", {"lines": self.lines})
        self._write(self.story / "prompt_manifest.json", {"shots": [{"id": "p", "variants": [
            {"id": "mouse_mouth", "mode": "mouth", "speaker": "MOUSE"},
            {"id": "lion_mouth", "mode": "mouth", "speaker": "LION"}]}]})
        self._write(self.audio / "timing.json", {"1": {"seconds": 6.0, "lines": [
            {"id": line["id"], "seconds": 1.0} for line in self.lines]}})
        self.words = {"lines": {}}
        for line in self.lines:
            audio = self.audio_lines / f"{line['id']}.wav"
            audio.write_bytes(line["id"].encode())
            self.words["lines"][line["id"]] = {
                "scene": 1, "speaker": line["speaker"], "transcript": line["text"],
                "audio_file": str(audio), "audio_sha256": hashlib.sha256(audio.read_bytes()).hexdigest(),
                "alignment_status": "aligned", "words": [
                    {"text": line["text"].rstrip("."), "start": 0.2, "end": 0.5}]}
        p = patch.object(paths, "STORIES", self.stories)
        p.start()
        self.addCleanup(p.stop)
        p = patch.object(paths, "story_audio", return_value=self.audio)
        p.start()
        self.addCleanup(p.stop)

    @staticmethod
    def _write(path, obj):
        path.write_text(json.dumps(obj), encoding="utf-8")

    def test_selected_variant_animates_only_its_speaker(self):
        cues = piece_word_cues("test_story", self.row, self.words)
        self.assertEqual([c["line_id"] for c in cues], ["l"])
        self.assertGreater(cues[0]["start"], 1.0)

    def test_stale_speaker_or_audio_fails_closed(self):
        self.words["lines"]["l"]["speaker"] = "NARRATOR"
        with self.assertRaisesRegex(SystemExit, "differs from dialogue coverage"):
            piece_word_cues("test_story", self.row, self.words)
        self.words["lines"]["l"]["speaker"] = "LION"
        (self.audio_lines / "l.wav").write_bytes(b"new recording")
        with self.assertRaisesRegex(SystemExit, "audio changed"):
            piece_word_cues("test_story", self.row, self.words)

    def test_open_mouth_boundary_is_rejected_before_render(self):
        manifest = {"shots": [{"id": "p", "variants": [{"id": "lion_mouth", "mode": "mouth"}]}],
                    "_image_index": {"open": {"id": "open", "mouth_character": "LION"},
                                     "closed": {"id": "closed"}}}
        manifest["shots"][0].update(start_image="open", end_image="closed")
        with self.assertRaisesRegex(SystemExit, "open-mouth boundary"):
            render_piece("test_story", self.row, Path("source.mp4"), Path("out.mp4"),
                         [], manifest, {}, 16)


if __name__ == "__main__":
    unittest.main()
