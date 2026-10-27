"""Frozen export→actual fake-backend CLI→selected bytes→sample edit proof."""

import io, json, runpy, sys, unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from tests import test_sequence_pipeline as baseline
from production import sequence_export as export, sequence_plan as plan, shot
from production.sequence_editor import edit_review_digest, bind_takes
from production.sequence_timeline import quantize
from feltwillow import wan
from feltwillow.local_video import save


class SequenceEditorTests(unittest.TestCase):
    setUp = baseline.SequencePipelineTests.setUp
    packet = baseline.SequencePipelineTests.packet

    def production_packet(self):
        p = self.packet()
        p["timing"].update(mode="production", pcm_verified=True, total_samples=24000)
        p["timing"]["intervals"] = [
            dict(
                id="chain_p000",
                kind="render_piece",
                start_sample=0,
                end_sample=12000,
                boundary="cut",
            ),
            dict(
                id="hold",
                kind="static_hold",
                start_sample=12000,
                end_sample=16500,
                use_id="B",
                boundary="cut",
                hold_review=dict(
                    status="pass",
                    reviewer="fixture",
                    source_sha256=p["resolved_images"][1]["source"]["sha256"],
                    fit_sha256=p["resolved_images"][1]["fit"]["pixel_sha256"],
                    settled=True,
                    resting_mouth=True,
                ),
            ),
            dict(
                id="chain_p001",
                kind="render_piece",
                start_sample=16500,
                end_sample=24000,
                boundary="cut",
            ),
        ]
        p["timing"]["render_allocations"] = {
            name: dict(
                frames=5,
                fps=16,
                reviewed=True,
                source_mapping=dict(start_frame=0, frame_count=5),
            )
            for name in ["chain_p000", "chain_p001"]
        }
        pieces = [
            dict(
                id=f"chain_p{n:03d}",
                frames=5,
                fps=16,
                method="wan_i2v_pair",
                start=a,
                end=b,
            )
            for n, (a, b) in enumerate([("A", "B"), ("B", "C")])
        ]
        p["timing"]["editorial_review"] = dict(
            status="reviewed",
            reviewer="synthetic timing fixture",
            allocation_sha256=edit_review_digest(p, pieces),
        )
        return p

    def test_C28_C48_export_to_selected_take_editor(self):
        p = self.production_packet()
        m = export.compile_packet(
            p,
            self.root,
            self.root / "production",
            "edit",
            self.recipe,
            mode="production",
        )

        def generate(pipe, prompt, **kw):
            return [wan.fit(kw["image"], 32, 32)] * kw["frames"]

        with (
            patch.object(shot.paths, "story_work", return_value=self.root / "work"),
            patch.object(wan, "load", return_value=object()),
            patch.object(wan, "verify_endpoint_environment", return_value={}),
            patch.object(
                wan,
                "endpoint_capability",
                return_value=dict(
                    endpoint_supported=True,
                    source_sha256="fixture-not-installed-runtime",
                ),
            ),
            patch.object(wan, "generate", side_effect=generate),
            patch.object(wan, "save", side_effect=save),
            redirect_stdout(io.StringIO()),
        ):
            for command in m["commands"]:
                with patch.object(sys, "argv", command["argv"][1:]):
                    runpy.run_path(command["argv"][1], run_name="__main__")
        selection = dict(
            schema="feltwillow.sequence-takes.v1",
            story="sample",
            run_id="edit",
            runtime_sha256=m["runtime"]["sha256"],
            takes={},
        )
        for path in (self.root / "work/runs/edit/shots").glob("*.mp4"):
            receipt = json.loads(path.with_suffix(".json").read_text())
            pid = receipt["shot"]
            sha = plan.digest(path)
            selection["takes"][pid] = dict(
                path=str(path),
                sha256=sha,
                owner_decision="selected",
                full_motion_review=dict(
                    status="pass",
                    reviewer="synthetic fixture only",
                    output_sha256=sha,
                    whole_clip_watched=True,
                    joins_reviewed=True,
                ),
            )
            self.assertEqual(
                receipt["editorial_plan_sha256"], m["editorial_plan"]["sha256"]
            )
        with self.assertRaisesRegex(ValueError, "retime"):
            bind_takes(m["editorial_plan"], selection, {}, self.root)
        row = m["editorial_plan"]["intervals"][0]
        mapping = row["source_mapping"]
        target = {k: row[k] for k in ("start_sample", "end_sample")}
        target.update(sample_rate=24000, fps=16, frame_start=0, frame_end=8)
        review = dict(
            status="pass",
            reviewer="synthetic after-return review",
            source_sha256=selection["takes"]["chain_p000"]["sha256"],
            mapping_sha256=plan.fingerprint(mapping),
            target_sha256=plan.fingerprint(target),
        )
        result = bind_takes(
            m["editorial_plan"],
            selection,
            {"chain_p000": {"retime_review": review}},
            self.root,
        )
        self.assertEqual([r["frame_cells"] for r in result["intervals"]], [8, 3, 5])
        self.assertFalse(result["final_assembly_authorized"])
        self.assertEqual(result["total_samples"], 24000)

    def test_C49_changed_allocations_fail_before_freezing(self):
        p = self.production_packet()
        p["timing"]["intervals"][0]["end_sample"] = 11000
        p["timing"]["intervals"][1]["start_sample"] = 11000
        with self.assertRaisesRegex(ValueError, "allocations pending/stale"):
            export.compile_packet(
                p,
                self.root,
                self.root / "stale",
                "stale",
                self.recipe,
                mode="production",
            )
        self.assertFalse((self.root / "stale/runtime.yaml").exists())
