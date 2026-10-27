import tempfile, unittest
from pathlib import Path
from PIL import Image
from production.sequence_plan import digest
from production.sequence_timeline import compile_timeline, render_preview


class TimelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.image = self.root / "plate.png"
        Image.new("RGB", (32, 32), "green").save(self.image)

    def row(self, id, start, end):
        return dict(
            id=id,
            kind="static_hold",
            source=dict(path=str(self.image), sha256=digest(self.image)),
            start_sample=start,
            end_sample=end,
        )

    def test_C28_C40_C41_cumulative_frame_cells(self):
        rows = [
            self.row("forest", 0, 239040),
            self.row("pause", 239040, 249840),
            self.row("speech", 249840, 298800),
        ]
        t = compile_timeline(rows, 24000, 298800)
        self.assertEqual(t["frame_cells"], 199)
        self.assertEqual(sum(r["frame_cells"] for r in t["intervals"]), 199)
        self.assertEqual(t["intervals"][0]["frame_cells"], 159)
        self.assertIn(t["intervals"][2]["frame_cells"], [32, 33])

    def test_C28_gap_and_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            compile_timeline(
                [self.row("a", 0, 1000), self.row("b", 1001, 3000)], 24000, 3000
            )
        with self.assertRaises(ValueError):
            compile_timeline(
                [self.row("a", 0, 1000), self.row("a", 1000, 3000)], 24000, 3000
            )

    def test_C48_unreviewed_join_or_retime_rejected(self):
        video = self.row("v", 0, 24000)
        video["kind"] = "video"
        video["source_mapping"] = {"frame_count": 10}
        with self.assertRaisesRegex(ValueError, "whole-motion"):
            compile_timeline([video], 24000, 24000)
        video["whole_motion_review"] = {
            "status": "pass",
            "reviewer": "fixture",
            "source_sha256": digest(self.image),
        }
        with self.assertRaisesRegex(ValueError, "retime"):
            compile_timeline([video], 24000, 24000)

    def test_static_preview_is_encoded_and_pending(self):
        t = compile_timeline([self.row("plate", 0, 7500)], 24000, 7500)
        receipt = render_preview(t, self.root / "preview.mp4", 32, 32)
        self.assertEqual(receipt["frames"], 5)
        self.assertEqual(receipt["visual_review"], "pending")
        from feltwillow.render_receipt import inspect_media

        self.assertEqual(inspect_media(Path(receipt["output"]))[0], "passed")


class MappingInvalidationTests(unittest.TestCase):
    setUp = TimelineTests.setUp
    row = TimelineTests.row

    def video_row(self, end=12000, start=0, count=16, source_start=0):
        from feltwillow.local_video import save

        path = self.root / "source.mp4"
        if not path.exists():
            save(
                [Image.new("RGB", (32, 32), (n * 12, 40, 80)) for n in range(16)],
                path,
                16,
            )
        row = dict(
            id="video",
            kind="video",
            source=dict(path=str(path), sha256=digest(path)),
            start_sample=start,
            end_sample=end,
            source_mapping=dict(start_frame=source_start, frame_count=count),
        )
        row["whole_motion_review"] = dict(
            status="pass", reviewer="synthetic fixture only", source_sha256=digest(path)
        )
        return row

    def bind(self, row, rate=24000, fps=16):
        from production.sequence_plan import fingerprint
        from production.sequence_timeline import quantize

        target = dict(
            start_sample=row["start_sample"],
            end_sample=row["end_sample"],
            sample_rate=rate,
            fps=fps,
            frame_start=quantize(row["start_sample"], rate, fps),
            frame_end=quantize(row["end_sample"], rate, fps),
        )
        mapping = row["source_mapping"]
        review = dict(
            status="pass",
            reviewer="synthetic only",
            source_sha256=row["source"]["sha256"],
            mapping_sha256=fingerprint(
                {k: v for k, v in mapping.items() if not k.endswith("_review")}
            ),
            target_sha256=fingerprint(target),
        )
        mapping["retime_review"] = dict(review)
        mapping["trim_review"] = dict(review)
        return row

    def test_C49_target_end_frame_count_rate_and_fps_invalidate_retime(self):
        import copy

        row = self.bind(self.video_row())
        self.assertEqual(compile_timeline([row], 24000, 12000)["frame_cells"], 8)
        for field, value in [
            ("end_sample", 36000),
            ("sample_rate", 48000),
            ("fps", 24),
        ]:
            candidate = copy.deepcopy(row)
            rate = 24000
            fps = 16
            if field == "end_sample":
                candidate[field] = value
            elif field == "sample_rate":
                rate = value
            else:
                fps = value
            with (
                self.subTest(field=field),
                self.assertRaisesRegex(ValueError, "retime"),
            ):
                compile_timeline([candidate], rate, candidate["end_sample"], fps)

    def test_C49_changed_target_start_invalidates_retime(self):
        row = self.bind(self.video_row())
        row["start_sample"] = 3000
        row["end_sample"] = 15000
        with self.assertRaisesRegex(ValueError, "retime"):
            compile_timeline([self.row("before", 0, 3000), row], 24000, 15000)

    def test_C48_C49_changed_trim_target_and_source_mapping_rejected(self):
        import copy

        row = self.bind(self.video_row(end=12000, count=8, source_start=2))
        compile_timeline([row], 24000, 12000)
        candidate = copy.deepcopy(row)
        candidate["source_mapping"]["start_frame"] = 3
        with self.assertRaisesRegex(ValueError, "trim"):
            compile_timeline([candidate], 24000, 12000)
        candidate = copy.deepcopy(row)
        candidate["source_mapping"]["trim_review"]["status"] = "failed"
        with self.assertRaisesRegex(ValueError, "trim"):
            compile_timeline([candidate], 24000, 12000)

    def test_C28_reject_boolean_or_fractional_sample_boundaries(self):
        for field, value in [("start_sample", False), ("end_sample", 7500.0)]:
            row = self.row("bad", 0, 7500)
            row[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                compile_timeline([row], 24000, 7500)

    def test_C48_join_review_invalidates_with_reviewed_trim_change(self):
        from production.sequence_timeline import join_digest, quantize

        left = self.bind(self.video_row(end=12000, count=8))
        right = self.bind(
            self.video_row(start=12000, end=24000, count=8, source_start=8)
        )
        right["id"] = "right"

        def cells(row):
            return {
                **row,
                "frame_start": quantize(row["start_sample"], 24000, 16),
                "frame_end": quantize(row["end_sample"], 24000, 16),
            }

        right["join_review"] = dict(
            status="pass",
            reviewer="synthetic join fixture",
            source_sha256s=[left["source"]["sha256"], right["source"]["sha256"]],
            join_sha256=join_digest(cells(left), cells(right), 24000, 16),
        )
        compile_timeline([left, right], 24000, 24000)
        left["source_mapping"]["frame_count"] = 6
        self.bind(left)
        with self.assertRaisesRegex(ValueError, "join"):
            compile_timeline([left, right], 24000, 24000)

    def test_boolean_source_frame_window_rejected(self):
        row=self.video_row();row['source_mapping']['start_frame']=True
        with self.assertRaisesRegex(ValueError,'source frame window'):compile_timeline([row],24000,row['end_sample'])
