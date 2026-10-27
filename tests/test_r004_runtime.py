"""CPU proof through frozen CLI arguments; no models or scheduler."""

import io, json, runpy, sys
from contextlib import redirect_stdout
from unittest.mock import patch
import unittest
from tests import test_sequence_pipeline as baseline
from production import sequence_plan as plan, sequence_export as export, shot
from feltwillow import wan


class R004RuntimeTests(unittest.TestCase):
    setUp = baseline.SequencePipelineTests.setUp
    packet = baseline.SequencePipelineTests.packet

    def execute(self, manifest):
        calls = []

        def generate(pipe, prompt, **kw):
            calls.append(kw)
            return [wan.fit(kw["image"], kw["width"], kw["height"])] * kw["frames"]

        def save(frames, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"CPU fixture; not playable")

        with (
            patch.object(shot.paths, "story_work", return_value=self.root / "work"),
            patch.object(wan, "load", return_value=object()),
            patch.object(wan, "verify_endpoint_environment", return_value={}),
            patch.object(
                wan,
                "endpoint_capability",
                return_value={
                    "endpoint_supported": True,
                    "source_sha256": "fixture-not-installed-runtime",
                },
            ),
            patch.object(wan, "generate", side_effect=generate),
            patch.object(wan, "save", side_effect=save),
            redirect_stdout(io.StringIO()),
        ):
            for command in manifest["commands"]:
                with patch.object(sys, "argv", command["argv"][1:]):
                    runpy.run_path(command["argv"][1], run_name="__main__")
        return calls

    def test_C06_single_reaches_backend_without_last_image(self):
        p = self.packet()
        p["resolved_images"] = p["resolved_images"][:1]
        p["edges"] = []
        p["visual_unit"] = {
            "editorial_relationship": "individual",
            "composition": "body_or_interaction",
        }
        p["dependency_sha256"] = plan.dependency_fingerprint(p)
        p["timing"]["dependency_sha256"] = p["dependency_sha256"]
        m = export.compile_packet(
            p, self.root, self.root / "single", "single", self.recipe
        )
        calls = self.execute(m)
        self.assertEqual(len(calls), 1)
        self.assertIsNone(calls[0]["last_image"])
        self.assertEqual(m["render_pieces"][0]["method"], "wan_i2v_single")

    def test_C29_piece_frames_reach_actual_backend(self):
        p = self.packet()
        recipe = {**self.recipe, "pieces": {"chain_p001": {"frames": 9}}}
        m = export.compile_packet(p, self.root, self.root / "varied", "varied", recipe)
        self.assertEqual([c["frames"] for c in self.execute(m)], [5, 9])
        self.assertEqual([v["frames"] for v in m["render_pieces"]], [5, 9])

    def test_C37_alias_retained_without_extra_model_job(self):
        p = self.packet()
        alias = {**p["resolved_images"][1], "id": "B_alias"}
        p["resolved_images"].insert(2, alias)
        p["edges"].insert(1, {"from": "B", "to": "B_alias", "kind": "shared_boundary"})
        p["edges"][2]["from"] = "B_alias"
        edge = p["edges"][2]
        p["technical_evidence"]["edges"]["B_alias->C"] = {
            **p["technical_evidence"]["edges"]["B->C"],
            "edge_sha256": plan.fingerprint(edge),
        }
        p["technical_evidence"]["uses"]["B_alias"] = p["technical_evidence"]["uses"][
            "B"
        ]
        p["dependency_sha256"] = plan.dependency_fingerprint(p)
        p["timing"]["dependency_sha256"] = p["dependency_sha256"]
        m = export.compile_packet(
            p, self.root, self.root / "alias", "alias", self.recipe
        )
        self.assertEqual(len(self.execute(m)), 2)
        self.assertEqual(len(p["resolved_images"]), 4)

    def test_static_negative_piece_frames_rejected(self):
        p = self.packet()
        p["sequence"]["method"] = "static_frame_hold"
        p["dependency_sha256"] = plan.dependency_fingerprint(p)
        p["timing"]["dependency_sha256"] = p["dependency_sha256"]
        with self.assertRaisesRegex(ValueError, "positive integer effective"):
            export.compile_packet(
                p,
                self.root,
                self.root / "negative",
                "negative",
                {**self.recipe, "pieces": {"chain_p000": {"frames": -3}}},
            )

    def test_C40_static_long_hold_no_model_load(self):
        p = self.packet()
        p["resolved_images"] = p["resolved_images"][:1]
        p["edges"] = []
        p["sequence"]["method"] = "static_frame_hold"
        p["visual_unit"] = {
            "editorial_relationship": "individual",
            "composition": "environment_only",
        }
        p["dependency_sha256"] = plan.dependency_fingerprint(p)
        p["timing"]["dependency_sha256"] = p["dependency_sha256"]
        m = export.compile_packet(
            p, self.root, self.root / "static", "static", {**self.recipe, "frames": 159}
        )
        with (
            patch.object(shot.paths, "story_work", return_value=self.root / "work"),
            patch.object(
                wan, "load", side_effect=AssertionError("CPU hold loaded model")
            ),
            patch.object(
                wan,
                "verify_endpoint_environment",
                side_effect=AssertionError("CPU hold probed model"),
            ),
            redirect_stdout(io.StringIO()),
        ):
            with patch.object(sys, "argv", m["commands"][0]["argv"][1:]):
                runpy.run_path(m["commands"][0]["argv"][1], run_name="__main__")
        self.assertEqual(m["model_invocations"], 0)
        receipt = json.loads(
            next((self.root / "work/runs/static/shots").glob("*.json")).read_text()
        )
        self.assertEqual(receipt["frames"], 159)
        self.assertIsNone(receipt["model"])
        self.assertEqual(receipt["method"], "static_frame_hold")

    def test_C10_four_distinct_inputs_all_reach_backend(self):
        from PIL import Image

        Image.new("RGB", (48, 32), "white").save(self.root / "D.png")
        self.selected.append(
            dict(image_id="D", path="D.png", sha256=plan.digest(self.root / "D.png"))
        )
        self.plan["lines"][0]["beats"][0]["image_sequence"]["images"].append(
            dict(id="D", state="same", location_view="same")
        )
        seq = self.plan["production_sequences"]["chain"]
        seq["uses"].append(dict(id="D", image_id="D"))
        seq["edges"].append(
            dict(**{"from": "C", "to": "D"}, kind="motion", prompt="Settle.")
        )
        m = export.compile_packet(
            self.packet(), self.root, self.root / "four", "four", self.recipe
        )
        calls = self.execute(m)
        self.assertEqual(
            [
                (c["image"].getpixel((0, 0)), c["last_image"].getpixel((0, 0)))
                for c in calls
            ],
            [
                ((255, 0, 0), (0, 128, 0)),
                ((0, 128, 0), (0, 0, 255)),
                ((0, 0, 255), (255, 255, 255)),
            ],
        )

    def test_C11_composition_change_requires_cut(self):
        seq = self.plan["production_sequences"]["chain"]
        seq["uses"][0]["composition"] = "portrait"
        seq["uses"][1]["composition"] = "environment_only"
        self.assertTrue(
            any("composition" in e for e in plan.validate_sequences(self.plan))
        )
        seq["edges"][0]["kind"] = "cut"
        self.assertEqual(plan.validate_sequences(self.plan), [])

    def test_C30_identical_motion_cannot_become_new_action(self):
        from production.sequence_readiness import evaluate

        p = self.packet()
        p["resolved_images"][1]["source"] = dict(p["resolved_images"][0]["source"])
        p["resolved_images"][1]["fit"] = dict(p["resolved_images"][0]["fit"])
        p["dependency_sha256"] = plan.dependency_fingerprint(p)
        p["timing"]["dependency_sha256"] = p["dependency_sha256"]
        self.assertTrue(any("identical raster" in b for b in evaluate(p)["blockers"]))
