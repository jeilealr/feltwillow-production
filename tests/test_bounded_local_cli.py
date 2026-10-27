"""Real frozen CLI and CPU encoder; no production media, models or scheduler."""

import copy, hashlib, io, json, runpy, sys, unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import numpy as np
from PIL import Image
from tests import test_sequence_pipeline as baseline
from production import sequence_export as export, sequence_plan as plan, shot
from feltwillow import wan
from feltwillow.local_video import bounded_frames
from feltwillow.render_receipt import inspect_media


class BoundedLocalCLITests(unittest.TestCase):
    setUp = baseline.SequencePipelineTests.setUp
    packet = baseline.SequencePipelineTests.packet

    def fixture(self):
        p = self.packet()
        p["resolved_images"] = p["resolved_images"][:1]
        p["edges"] = []
        source = np.array(Image.open(self.root / "A.png"))
        target = source.copy()
        target[8:16, 20:28] = [10, 20, 30]
        mask = np.zeros(source.shape[:2], np.uint8)
        mask[8:16, 20:28] = 255
        Image.fromarray(target).save(self.root / "target.png")
        Image.fromarray(mask).save(self.root / "mask.png")
        ref = lambda name: dict(
            path=str(self.root / name), sha256=plan.digest(self.root / name)
        )
        weights = [0, 0.5, 1, 0.5, 0]
        effect = dict(
            target=ref("target.png"),
            mask=ref("mask.png"),
            frame_weights=weights,
            review=dict(
                status="pass",
                reviewer="synthetic fixture only",
                source_sha256=plan.digest(self.root / "A.png"),
                target_sha256=plan.digest(self.root / "target.png"),
                mask_sha256=plan.digest(self.root / "mask.png"),
                frame_weights_sha256=hashlib.sha256(
                    json.dumps(weights, separators=(",", ":")).encode()
                ).hexdigest(),
            ),
        )
        p["sequence"].update(method="bounded_local_effect", local_effect=effect)
        p["visual_unit"] = dict(
            editorial_relationship="individual", composition="body_or_interaction"
        )
        p["dependency_sha256"] = plan.dependency_fingerprint(p)
        p["timing"]["dependency_sha256"] = p["dependency_sha256"]
        return p, effect

    def test_C26_C31_frozen_cli_resting_native_boundaries_and_no_model(self):
        p, effect = self.fixture()
        m = export.compile_packet(
            p, self.root, self.root / "packet", "local", self.recipe
        )
        with (
            patch.object(shot.paths, "story_work", return_value=self.root / "work"),
            patch.object(
                wan, "load", side_effect=AssertionError("model must not load")
            ),
            patch.object(
                wan,
                "verify_endpoint_environment",
                side_effect=AssertionError("no model capability query"),
            ),
            redirect_stdout(io.StringIO()),
        ):
            with patch.object(sys, "argv", m["commands"][0]["argv"][1:]):
                runpy.run_path(m["commands"][0]["argv"][1], run_name="__main__")
        path = next((self.root / "work/runs/local/shots").glob("*.mp4"))
        receipt = json.loads(path.with_suffix(".json").read_text())
        self.assertEqual(inspect_media(path, receipt)[0], "passed")
        self.assertEqual(m["model_invocations"], 0)
        start = np.array(Image.open(receipt["native_boundaries"]["first"]["path"]))
        end = np.array(Image.open(receipt["native_boundaries"]["last"]["path"]))
        np.testing.assert_array_equal(start, end)
        frames = bounded_frames(self.root / "A.png", 48, 32, 5, effect)
        base = np.asarray(frames[0])
        changed = np.asarray(frames[2])
        mask = np.array(Image.open(self.root / "mask.png")) > 0
        np.testing.assert_array_equal(base[~mask], changed[~mask])
        self.assertTrue(np.any(base[mask] != changed[mask]))
        self.assertEqual(receipt["method"], "bounded_local_effect")
        self.assertEqual(receipt["visual_review"], "pending")

    def test_C31_changed_mask_or_temporal_weights_fail_before_compile(self):
        for change in ("mask", "weights", "failed_review"):
            with self.subTest(change=change):
                p, effect = self.fixture()
                if change == "mask":
                    effect["mask"]["sha256"] = "0" * 64
                elif change == "weights":
                    effect["frame_weights"][2] = 0.2
                else:
                    effect["review"]["status"] = "failed"
                p["dependency_sha256"] = plan.dependency_fingerprint(p)
                p["timing"]["dependency_sha256"] = p["dependency_sha256"]
                with (
                    self.assertRaises(ValueError),
                    patch.object(wan, "load", side_effect=AssertionError()),
                ):
                    export.compile_packet(
                        p, self.root, self.root / change, change, self.recipe
                    )
                self.assertFalse((self.root / change / "packet.json").exists())

    def test_C29_invalid_frames_and_protected_target_changes_rejected(self):
        p, effect = self.fixture()
        for frames in (0, -1, True, 5.0):
            with self.subTest(frames=frames), self.assertRaises(ValueError):
                bounded_frames(self.root / "A.png", 48, 32, frames, effect)
        image = np.array(Image.open(self.root / "target.png"))
        image[0, 0] = 0
        Image.fromarray(image).save(self.root / "target.png")
        effect["target"]["sha256"] = plan.digest(self.root / "target.png")
        effect["review"]["target_sha256"] = effect["target"]["sha256"]
        with self.assertRaisesRegex(ValueError, "protected"):
            bounded_frames(self.root / "A.png", 48, 32, 5, effect)
