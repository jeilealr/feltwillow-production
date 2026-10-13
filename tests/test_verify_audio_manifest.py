"""The audio reuse exception must retain exact bytes in the v6 runtime namespace."""

import hashlib
import tempfile
import unittest
import wave
from pathlib import Path

from production.verify_audio_manifest import verify, work_file


class AudioManifestTests(unittest.TestCase):
    def test_provenance_and_runtime_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            payload = b"\0\0" * 240
            paths = ["work/the_lion_and_the_mouse/lines/S01-L001.wav",
                     "work/stories/lion_and_mouse_v6/audio/en/lines/S01-L001.wav",
                     "work/stories/lion_and_mouse_v6/audio/en/scene01.wav"]
            for relative in paths:
                target = work_file(relative, work)
                target.parent.mkdir(parents=True, exist_ok=True)
                with wave.open(str(target), "wb") as wav:
                    wav.setnchannels(1)
                    wav.setsampwidth(2)
                    wav.setframerate(24000)
                    wav.writeframes(payload)
            digest = hashlib.sha256(work_file(paths[0], work).read_bytes()).hexdigest()
            manifest = {
                "story": "lion_and_mouse_v6", "source_story": "lion_and_mouse_v5",
                "owner_authorized_reuse": True, "sample_rate_hz": 24000,
                "channels": 1, "sample_width_bits": 16, "line_count": 1,
                "scene_count": 1, "total_duration_seconds": 0.01,
                "lines": [{"id": "S01-L001", "scene": 1, "source_path": paths[0],
                           "v6_path": paths[1], "duration_seconds": 0.01,
                           "sha256": digest}],
                "scenes": [{"scene": 1, "path": paths[2], "duration_seconds": 0.01,
                            "sha256": digest, "line_count": 1}],
            }
            self.assertEqual(verify(manifest, "lion_and_mouse_v6", work, True), [])
            work_file(paths[1], work).write_bytes(b"changed")
            self.assertTrue(any("SHA-256 mismatch" in e for e in
                                verify(manifest, "lion_and_mouse_v6", work, True)))
            manifest["owner_authorized_reuse"] = False
            self.assertTrue(any("owner-authorized" in e for e in
                                verify(manifest, "lion_and_mouse_v6", work, True)))

    def test_work_path_cannot_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            for path in ("../escape.wav", "work/../escape.wav", "/tmp/escape.wav"):
                with self.assertRaises(ValueError):
                    work_file(path, Path(directory))


if __name__ == "__main__":
    unittest.main()
