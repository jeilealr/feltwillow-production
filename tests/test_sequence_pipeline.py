"""CPU-only integration of endpoint packets, runtime identity and receipt capture."""

import io
import json
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from PIL import Image
import yaml

from feltwillow import wan
from feltwillow.render_receipt import inspect_media, inspect_render
from production import sequence_plan as plan
from production import sequence_export as export
from production.sequence_readiness import evaluate
from production import shot, render_story_inventory


class SequencePipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "production").mkdir()
        shutil.copyfile(Path(shot.__file__), self.root / "production/shot.py")
        self.selected = []
        images = []
        for label, color in [("A", "red"), ("B", "green"), ("C", "blue")]:
            path = self.root / (label + ".png")
            Image.new("RGB", (48, 32), color).save(path)
            self.selected.append(
                dict(image_id=label, path=path.name, sha256=plan.digest(path))
            )
            images.append(dict(id=label, state="same", location_view="same"))
        self.plan = dict(
            story="sample",
            lines=[
                dict(
                    beats=[
                        dict(
                            id="beat", cast=["Milo"], image_sequence=dict(images=images)
                        )
                    ]
                )
            ],
            production_sequences={
                "chain": dict(
                    id="chain",
                    uses=[dict(id=i, image_id=i) for i in "ABC"],
                    edges=[
                        dict(
                            **{"from": "A", "to": "B"},
                            kind="motion",
                            prompt="Look left.",
                        ),
                        dict(
                            **{"from": "B", "to": "C"},
                            kind="motion",
                            prompt="Look right.",
                        ),
                    ],
                )
            },
        )
        self.recipe = dict(
            width=32,
            height=32,
            frames=5,
            steps=4,
            guidance=1.0,
            guidance_2=1.0,
            preset="fast",
            seed=1,
        )

    def packet(self):
        p = plan.resolve_sequence(
            self.plan, "chain", self.root, self.selected, size=(32, 32)
        )
        p["technical_evidence"] = {"uses": {}, "edges": {}}
        for u in p["resolved_images"]:
            p["technical_evidence"]["uses"][u["id"]] = {
                "reviewer": "synthetic fixture",
                "status": "pass",
                "source_sha256": u["source"]["sha256"],
                "fit_sha256": u["fit"]["pixel_sha256"],
            }
        byid = {u["id"]: u for u in p["resolved_images"]}
        for edge in p["edges"]:
            p["technical_evidence"]["edges"][edge["from"] + "->" + edge["to"]] = {
                "reviewer": "synthetic fixture",
                "status": "pass",
                "source_sha256s": [
                    byid[edge[k]]["source"]["sha256"] for k in ["from", "to"]
                ],
                "edge_sha256": plan.fingerprint(edge),
            }
        p["timing"] = dict(
            sample_rate=24000,
            status="reviewed",
            mode="diagnostic",
            reviewer="synthetic fixture only",
            dependency_sha256=p["dependency_sha256"],
            intervals=[dict(start_sample=0, end_sample=15000)],
            total_samples=15000,
        )
        p["capability"] = dict(
            endpoint_supported=True,
            evidence_level="inspected_source_config",
            source_sha256="fixture-not-installed-runtime",
            expand_timesteps=False,
        )
        return p

    def test_ordered_chain_reaches_backend_native_receipts_and_inventory(self):
        p = self.packet()
        manifest = export.compile_packet(
            p, self.root, self.root / "packet", "test", self.recipe
        )
        calls = []

        def generate(pipe, prompt, **kw):
            calls.append(
                (kw["image"].getpixel((0, 0)), kw["last_image"].getpixel((0, 0)))
            )
            return [wan.fit(kw["image"], kw["width"], kw["height"])] * 5

        def save(frames, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"fake encoded bytes; decode must fail")

        with (
            patch.object(shot.paths, "story_work", return_value=self.root / "work"),
            patch.object(wan, "load", return_value=object()) as loader,
            patch.object(
                wan,
                "endpoint_capability",
                return_value={
                    "endpoint_supported": True,
                    "source_sha256": "fixture-not-installed-runtime",
                },
            ),
            patch.object(
                wan, "verify_endpoint_environment", return_value={"fixture": True}
            ),
            patch.object(wan, "generate", side_effect=generate),
            patch.object(wan, "save", side_effect=save),
            redirect_stdout(io.StringIO()),
        ):
            for command in manifest["commands"]:
                with patch.object(sys, "argv", command["argv"][1:]):
                    runpy.run_path(command["argv"][1], run_name="__main__")
        self.assertEqual(loader.call_count, 2)
        self.assertEqual(
            calls, [((255, 0, 0), (0, 128, 0)), ((0, 128, 0), (0, 0, 255))]
        )
        receipt = json.loads(
            next((self.root / "work/runs/test/shots").glob("*.json")).read_text()
        )
        self.assertEqual(receipt["run_id"], "test")
        self.assertFalse(receipt["negative_conditioning_active"])
        self.assertEqual(set(receipt["native_boundaries"]), {"first", "last"})
        self.assertEqual(receipt["visual_review"], "pending")
        self.assertEqual(
            inspect_media(next((self.root / "work/runs/test/shots").glob("*.mp4")))[0],
            "failed",
        )
        # The inventory's audit subprocess must carry the same frozen identity.
        runtime = Path(manifest["runtime"]["path"])

        def audit(argv, **kw):
            self.assertIn("--runtime-sha256", argv)
            name = argv[argv.index("--shot") + 1]
            return subprocess.CompletedProcess(
                argv,
                0,
                json.dumps(
                    dict(
                        story="sample",
                        scene=1,
                        shot=name,
                        seeds=[dict(seed=1, status="missing")],
                    )
                ),
                "",
            )

        with patch.object(render_story_inventory.subprocess, "run", side_effect=audit):
            blocked = render_story_inventory.inventory_story("sample", runtime, "test")
            journal = dict(
                runtime_sha256=manifest["runtime"]["sha256"],
                operations={
                    c["operation_id"]: "not_submitted" for c in manifest["commands"]
                },
            )
            ready = render_story_inventory.inventory_story(
                "sample", runtime, "test", journal
            )
            journal["operations"][manifest["commands"][0]["operation_id"]] = "uncertain"
            uncertain = render_story_inventory.inventory_story(
                "sample", runtime, "test", journal
            )
        self.assertEqual(len(blocked["blocked_operations"]), 2)
        self.assertEqual(len(ready["command_records"]), 2)
        self.assertEqual(len(uncertain["command_records"]), 1)

    def test_hold_preserves_second_endpoint_and_cuts_are_separate(self):
        seq = self.plan["production_sequences"]["chain"]
        seq["uses"][1] = {
            "id": "B",
            "alias_of": "A",
            "hold": True,
            "hold_reason": "settled",
        }
        seq["edges"][0]["kind"] = "hold"
        seq["edges"][1]["kind"] = "cut"
        manifest = export.compile_packet(
            self.packet(), self.root, self.root / "hold", "hold", self.recipe
        )
        runtime = yaml.safe_load(Path(manifest["runtime"]["path"]).read_text())
        shots = runtime["scenes"][1]["shots"]
        self.assertEqual(len(shots), 1)
        self.assertEqual(shots[0]["keyframe"], shots[0]["end_keyframe"])
        self.assertIn("end_keyframe", shots[0])

    def test_scope_missing_alias_stale_and_conflicting_selection(self):
        self.plan["lines"][0]["beats"][0]["image_sequence"]["images"].append(
            dict(id="unused", state="later", location_view="elsewhere")
        )
        self.assertTrue(evaluate(self.packet())["technical_render_ready"])
        self.selected.pop()
        p = plan.resolve_sequence(
            self.plan, "chain", self.root, self.selected, size=(32, 32)
        )
        self.assertEqual(p["resolved_images"][2]["status"], "missing_distinct_state")
        self.assertFalse(evaluate(p, "realization")["stage_passed"])
        self.plan["production_sequences"]["chain"]["uses"][0]["alias_of"] = "C"
        self.assertTrue(plan.validate_sequences(self.plan))

    def test_changed_source_and_evidence_cannot_freeze(self):
        p = self.packet()
        Image.new("RGB", (48, 32), "white").save(self.root / "A.png")
        with self.assertRaisesRegex(ValueError, "bytes changed"):
            export.compile_packet(p, self.root, self.root / "bad", "bad", self.recipe)
        p = plan.resolve_sequence(
            self.plan, "chain", self.root, self.selected, size=(32, 32)
        )
        self.assertFalse(evaluate(p)["technical_render_ready"])

    def test_preflight_and_frozen_runtime_fail_before_load(self):
        manifest = export.compile_packet(
            self.packet(), self.root, self.root / "ok", "ok", self.recipe
        )
        command = manifest["commands"][0]["argv"][1:]
        with (
            patch.object(wan, "load") as loader,
            patch.object(
                wan, "verify_endpoint_environment", return_value={"fixture": True}
            ),
            redirect_stdout(io.StringIO()),
        ):
            with patch.object(sys, "argv", command + ["--dry-run"]):
                shot.main()
            loader.assert_not_called()
            runtime = Path(manifest["runtime"]["path"])
            runtime.write_text(runtime.read_text() + "\n# changed")
            with patch.object(sys, "argv", command), self.assertRaises(SystemExit):
                shot.main()
            loader.assert_not_called()
        for frames in [0, -3, True, 6, 85]:
            with self.assertRaises(ValueError):
                wan.preflight(
                    width=32,
                    height=32,
                    frames=frames,
                    steps=4,
                    guidance=1,
                    guidance_2=1,
                    max_frames=81,
                )
        with self.assertRaisesRegex(ValueError, "transparent"):
            wan.fitted_record(Image.new("RGBA", (32, 32), (1, 2, 3, 0)), 32, 32)

    def test_mixed_cfg_activation_is_rejected_before_freezing(self):
        recipe = dict(self.recipe, preset="normal", guidance=1.0, guidance_2=3.5)
        with self.assertRaisesRegex(ValueError, "mixed CFG"):
            export.compile_packet(
                self.packet(), self.root, self.root / "mixed", "mixed", recipe
            )

    def test_atomic_packet_and_production_timing_guard(self):
        p = self.packet()
        first = export.compile_packet(
            p, self.root, self.root / "freeze", "freeze", self.recipe
        )
        self.assertEqual(
            first,
            export.compile_packet(
                p, self.root, self.root / "freeze", "freeze", self.recipe
            ),
        )
        with self.assertRaisesRegex(ValueError, "immutable"):
            export.compile_packet(
                p, self.root, self.root / "freeze", "different", self.recipe
            )
        p["timing"].update(mode="production", pcm_verified=True)
        with self.assertRaisesRegex(ValueError, "allocation"):
            export.compile_packet(
                p, self.root, self.root / "prod", "prod", self.recipe, mode="production"
            )

    def test_decoded_take_is_hash_bound_and_unreviewed_motion_cannot_select(self):
        import numpy as np
        from production.sequence_take import selected_source

        path = self.root / "clip.mp4"
        subprocess.run(
            [
                str(Path(sys.executable).parent / "ffmpeg"),
                "-v",
                "error",
                "-f",
                "rawvideo",
                "-pix_fmt",
                "rgb24",
                "-s",
                "32x32",
                "-r",
                "16",
                "-i",
                "pipe:0",
                "-frames:v",
                "5",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                str(path),
            ],
            input=np.zeros((5, 32, 32, 3), dtype=np.uint8).tobytes(),
            check=True,
            capture_output=True,
        )
        boundary = self.root / "boundary.png"
        Image.new("RGB", (32, 32)).save(boundary)
        expected = dict(
            run_id="run",
            runtime_sha256="runtime",
            shot="piece",
            width=32,
            height=32,
            frames=5,
            fps=16,
        )
        receipt = dict(
            expected,
            output_sha256=plan.digest(path),
            native_boundaries={
                k: dict(path=str(boundary), sha256=plan.digest(boundary))
                for k in ["first", "last"]
            },
        )
        path.with_suffix(".json").write_text(json.dumps(receipt))
        self.assertEqual(inspect_render(path, expected)[0], "complete")
        row = dict(path=str(path), sha256=plan.digest(path), owner_decision="selected")
        doc = dict(
            schema="feltwillow.sequence-takes.v1",
            run_id="run",
            runtime_sha256="runtime",
            takes={"piece": row},
        )
        with self.assertRaisesRegex(ValueError, "review"):
            selected_source(doc, "piece")
        row["full_motion_review"] = dict(
            status="pass",
            reviewer="fixture only",
            output_sha256=row["sha256"],
            whole_clip_watched=True,
            joins_reviewed=True,
        )
        self.assertEqual(selected_source(doc, "piece")[0], path)
        path.write_bytes(b"corrupt")
        self.assertEqual(inspect_render(path, expected)[0], "stale")

    def test_protected_pixels_do_not_certify_integration(self):
        from production.sequence_review import protected_pixels

        mask = self.root / "mask.png"
        Image.new("L", (48, 32), 0).save(mask)
        measured = protected_pixels(self.root / "A.png", self.root / "B.png", mask)
        self.assertEqual(measured["status"], "fail")
        self.assertEqual(measured["changed_protected_pixels"], 48 * 32)
        Image.new("L", (48, 32), 255).save(mask)
        measured = protected_pixels(self.root / "A.png", self.root / "B.png", mask)
        self.assertEqual(measured["status"], "pass")
        self.assertIn("pending", measured["integration_review"])

    def test_alias_failure_modes_and_empty_prompt(self):
        seq = self.plan["production_sequences"]["chain"]
        seq["uses"][0]["alias_of"] = "missing"
        self.assertTrue(plan.validate_sequences(self.plan))
        del seq["uses"][0]["alias_of"]
        self.selected.append(dict(self.selected[0], sha256="different"))
        packet = plan.resolve_sequence(
            self.plan, "chain", self.root, self.selected, size=(32, 32)
        )
        self.assertEqual(packet["resolved_images"][0]["status"], "ambiguous_authority")
        self.selected.pop()
        for use in seq["uses"]:
            use["visible_cast"] = []
        # Explicit editorial sources do not relabel character-bearing planned slots.
        for use, selected in zip(seq["uses"], self.selected):
            del use["image_id"]
            use["source"] = {k: selected[k] for k in ["path", "sha256"]}
        seq["edges"][0]["prompt"] = "Milo cream patch orange tail"
        with self.assertRaisesRegex(ValueError, "empty-cast"):
            export.compile_packet(
                self.packet(), self.root, self.root / "empty", "empty", self.recipe
            )

    def test_realized_acting_evidence_does_not_flip_planned_lifecycle(self):
        u = self.packet()["resolved_images"][0]
        u["visible_cast"] = ["Milo"]
        record = dict(
            scene_sha256=u["source"]["sha256"],
            fit_sha256=u["fit"]["pixel_sha256"],
            reviewer="fixture only",
            scope="realized_scene_acting_projection",
            projection=dict(kind="reviewed_2d", landmarks={"foot": [20, 31]}),
            applied_expressions={
                "Milo": dict(
                    expression_id="fixture.worried",
                    source={k: self.selected[1][k] for k in ["path", "sha256"]},
                )
            },
        )
        result = plan.applied_performance_evidence(u, record, self.root)
        self.assertTrue(result["planned_lifecycle_unchanged"])
        record["scene_sha256"] = "wrong"
        with self.assertRaises(ValueError):
            plan.applied_performance_evidence(u, record, self.root)
        self.plan["world_states"] = {
            "same": dict(
                acorn_owner="stream_flat_stone", legacy_pose="standing_holding_acorn"
            )
        }
        self.plan["lines"][0]["beats"][0]["image_sequence"]["images"][0][
            "performance"
        ] = {"Milo": dict(binding_status="planned")}
        state = plan.resolved_visual_state(self.plan, "A")
        self.assertEqual(state["causal_state"]["acorn_owner"], "stream_flat_stone")
        self.assertEqual(state["depiction"]["Milo"]["binding_status"], "planned")

    def test_downstream_selection_cannot_guess_a_legacy_or_lipsynced_take(self):
        from production import chain_preview

        document = dict(schema="feltwillow.sequence-takes.v1", story="sample")
        selected = self.root / "exact.mp4"
        with (
            patch(
                "production.sequence_take.selected_source",
                return_value=(selected, dict(run_id="run")),
            ),
            patch.object(chain_preview, "resolve_synced_take") as legacy,
        ):
            result = chain_preview.find_take(
                "sample", dict(piece="piece", mode="mouth"), document, None
            )
        self.assertEqual(result[0], selected)
        legacy.assert_not_called()

    def test_started_operation_cannot_be_silently_retried(self):
        manifest = export.compile_packet(
            self.packet(), self.root, self.root / "claim", "claim", self.recipe
        )
        command = manifest["commands"][0]["argv"][1:]
        with (
            patch.object(shot.paths, "story_work", return_value=self.root / "work"),
            patch.object(
                wan, "verify_endpoint_environment", return_value=dict(fixture=True)
            ),
            patch.object(
                wan, "load", side_effect=RuntimeError("synthetic interrupted attempt")
            ) as loader,
            redirect_stdout(io.StringIO()),
        ):
            with patch.object(sys, "argv", command), self.assertRaises(RuntimeError):
                shot.main()
            self.assertEqual(loader.call_count, 1)
            with (
                patch.object(sys, "argv", command),
                self.assertRaisesRegex(SystemExit, "claimed"),
            ):
                shot.main()
            self.assertEqual(loader.call_count, 1)

    def test_unused_future_input_does_not_invalidate_scope(self):
        a = plan.resolve_sequence(
            self.plan, "chain", self.root, self.selected, size=(32, 32)
        )
        self.plan["lines"][0]["beats"][0]["image_sequence"]["images"].append(
            dict(id="unused", state="future", location_view="future")
        )
        b = plan.resolve_sequence(
            self.plan, "chain", self.root, self.selected, size=(32, 32)
        )
        self.assertEqual(a["dependency_sha256"], b["dependency_sha256"])
        self.assertNotEqual(a["source_plan_sha256"], b["source_plan_sha256"])

    def test_sequence_review_serves_only_explicit_run_video(self):
        from production.serve_scene_review import gallery_assets

        root = self.root / "repo"
        root.mkdir()
        video = self.root / "work/stories/lion_and_mouse_v7/runs/run/clip.mp4"
        video.parent.mkdir(parents=True)
        video.write_bytes(b"fixture only")
        page = Path(
            "stories/lion_and_mouse_v7/review/sequence_readiness_r001/chain/review.html"
        )
        (root / page).parent.mkdir(parents=True)
        url = "/__sequence_work__/stories/lion_and_mouse_v7/runs/run/clip.mp4"
        (root / page).write_text('<video src="' + url + '"></video>')
        assets = gallery_assets(root, page)
        self.assertEqual(assets[url], video.resolve())
        self.assertEqual(len(assets), 2)
        (root / page).write_text(
            '<video src="/__sequence_work__/../../private.txt"></video>'
        )
        with self.assertRaises(ValueError):
            gallery_assets(root, page)

    def test_transparent_scene_is_not_previewed_against_implicit_black(self):
        from production.sequence_review import build

        Image.new("RGBA", (48, 32), (1, 2, 3, 0)).save(self.root / "A.png")
        self.selected[0]["sha256"] = plan.digest(self.root / "A.png")
        packet = plan.resolve_sequence(
            self.plan, "chain", self.root, self.selected, size=(32, 32)
        )
        self.assertEqual(
            packet["resolved_images"][0]["status"], "incompatible_for_edge"
        )
        page = build(packet, self.root, self.root / "board")
        self.assertIn("No model-fit preview", page.read_text())
        self.assertFalse((page.parent / "fit_000.png").exists())

    def test_legacy_composition_dry_run_keeps_historical_behavior(self):
        stories = self.root / "stories"
        folder = stories / "sample"
        folder.mkdir(parents=True)
        work = self.root / "legacy"
        work.mkdir()
        Image.new("RGB", (32, 32)).save(work / "plate.png")
        runtime = dict(
            negative="",
            characters={},
            scenes={
                1: dict(
                    shots=[
                        dict(
                            name="legacy",
                            prompt="Legacy fixture.",
                            keyframe="unbuilt.png",
                            compose=dict(plate="plate.png", characters=[]),
                            seeds=[1],
                            frames=5,
                        )
                    ]
                )
            },
        )
        (folder / "story.yaml").write_text(yaml.safe_dump(runtime))
        capture = io.StringIO()
        with (
            patch.object(shot.paths, "STORIES", stories),
            patch.object(shot.paths, "story_work", return_value=work),
            patch.object(wan, "load") as loader,
            patch.object(
                sys,
                "argv",
                [
                    "shot.py",
                    "--story",
                    "sample",
                    "--scene",
                    "1",
                    "--shot",
                    "legacy",
                    "--dry-run",
                ],
            ),
            redirect_stdout(capture),
        ):
            shot.main()
        loader.assert_not_called()
        self.assertIn("keyframe will be composed", capture.getvalue())
        self.assertFalse((work / "unbuilt.png").exists())

    def test_semantic_alias_cannot_hide_a_new_causal_state(self):
        seq = self.plan["production_sequences"]["chain"]
        seq["uses"][0]["id"] = "established"
        seq["uses"][1]["alias_of"] = "established"
        seq["edges"][0]["from"] = "established"
        seq["edges"][0]["kind"] = "hold"
        self.plan["lines"][0]["beats"][0]["image_sequence"]["images"][1]["state"] = (
            "after_release"
        )
        packet = plan.resolve_sequence(
            self.plan, "chain", self.root, self.selected, size=(32, 32)
        )
        self.assertEqual(
            packet["resolved_images"][1]["status"], "incompatible_for_edge"
        )
        self.assertFalse(evaluate(packet, "realization")["stage_passed"])

    def test_native_float_preservation_and_capability_guard(self):
        import numpy as np

        raw = np.array([[[0.12345678, 0.5, 1.0]]], dtype=np.float32)
        record = wan.save_native_boundary(raw, self.root / "native.png")
        self.assertEqual(record["representation"], "float32")
        self.assertTrue(
            np.array_equal(raw, np.load(record["path"], allow_pickle=False))
        )

        class Unsupported:
            config = {"expand_timesteps": True}

            def __call__(self, last_image=None):
                pass

        self.assertFalse(wan.endpoint_capability(Unsupported())["endpoint_supported"])

    def test_rational_timeline_and_scope_invalidation(self):
        mapping = plan.frame_accounting(
            [
                dict(start_sample=0, end_sample=747600),
                dict(start_sample=747600, end_sample=764400),
            ],
            24000,
        )
        self.assertEqual(mapping["total_frame_cells"], 510)
        self.assertEqual(mapping["intervals"][0]["end_frame_exclusive"], 498)
        self.assertEqual(mapping["intervals"][1]["start_frame"], 498)
        with self.assertRaises(ValueError):
            plan.frame_accounting([dict(start_sample=1, end_sample=1000)], 24000)
        p = self.packet()
        p["edges"][0]["prompt"] = "changed"
        self.assertFalse(evaluate(p)["technical_render_ready"])
        p = self.packet()
        p["timing"]["intervals"][0]["start_sample"] = 1
        self.assertFalse(evaluate(p)["technical_render_ready"])

    def test_receipt_malformed_native_capture_is_controlled(self):
        path = self.root / "bad.mp4"
        path.write_bytes(b"bad")
        path.with_suffix(".json").write_text(
            json.dumps(
                dict(
                    run_id="r",
                    output_sha256=plan.digest(path),
                    native_boundaries={"first": {}, "last": {}},
                )
            )
        )
        self.assertEqual(inspect_render(path, dict(run_id="r"))[0], "stale")


if __name__ == "__main__":
    unittest.main()
