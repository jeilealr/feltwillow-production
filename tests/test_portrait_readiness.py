import copy, unittest
from tests import test_sequence_pipeline as baseline
from production.sequence_readiness import evaluate
from production.sequence_plan import dependency_fingerprint
from tests.test_portrait_qa import fixture


class PortraitReadinessTests(unittest.TestCase):
    setUp = baseline.SequencePipelineTests.setUp
    packet = baseline.SequencePipelineTests.packet

    def portrait(self):
        p = self.packet()
        p["resolved_images"] = p["resolved_images"][:1]
        p["edges"] = []
        p["visual_unit"] = dict(
            editorial_relationship="individual",
            composition="portrait",
            mouth_policy="dialogue_lipsync",
            camera_and_crop_lock="fixture_view",
        )
        p["dependency_sha256"] = dependency_fingerprint(p)
        p["timing"]["dependency_sha256"] = p["dependency_sha256"]
        return p

    def test_C20_C22_portrait_source_requires_exact_crop_closed_mouth_review(self):
        p = self.portrait()
        self.assertTrue(any("portrait" in b for b in evaluate(p)["blockers"]))
        use = p["resolved_images"][0]
        contract = fixture()[1]
        contract.update(
            source_sha256=use["source"]["sha256"],
            fit_sha256=use["fit"]["pixel_sha256"],
            camera_and_crop_lock="fixture_view",
            closed_mouth_boundary=True,
            toothless_source=True,
            visible_crop_review=True,
            no_unplanned_limb=True,
        )
        p["technical_evidence"]["uses"]["A"]["portrait_contract"] = contract
        self.assertTrue(evaluate(p)["technical_render_ready"])
        for field, value in [
            ("source_sha256", "bad"),
            ("camera_and_crop_lock", "other"),
            ("closed_mouth_boundary", False),
            ("toothless_source", False),
            ("no_unplanned_limb", False),
        ]:
            altered = copy.deepcopy(p)
            altered["technical_evidence"]["uses"]["A"]["portrait_contract"][field] = (
                value
            )
            with self.subTest(field=field):
                self.assertFalse(evaluate(altered)["technical_render_ready"])

    def test_missing_media_and_edges_report_blockers_without_crashing(self):
        p = self.packet()
        p["resolved_images"][0].update(
            source=None, fit=None, status="unavailable_bytes"
        )
        p["dependency_sha256"] = dependency_fingerprint(p)
        p["timing"]["dependency_sha256"] = p["dependency_sha256"]
        for stage in ("realization", "still", "timing", "execution"):
            with self.subTest(stage=stage):
                self.assertFalse(evaluate(p, stage)["stage_passed"])

    def test_C34_leo_body_needs_manual_paw_and_support_review(self):
        p = self.portrait()
        p["visual_unit"].update(composition="body_or_interaction", visible_cast=["Leo"])
        p["dependency_sha256"] = dependency_fingerprint(p)
        p["timing"]["dependency_sha256"] = p["dependency_sha256"]
        self.assertTrue(any("manual paw" in b for b in evaluate(p)["blockers"]))
        u = p["resolved_images"][0]
        p["technical_evidence"]["uses"]["A"]["anatomy_review"] = dict(
            status="reviewed",
            reviewer="synthetic topology fixture",
            source_sha256=u["source"]["sha256"],
            fit_sha256=u["fit"]["pixel_sha256"],
            required_limbs_accounted=True,
            support_contact_reviewed=True,
            declared_occlusions=[],
        )
        self.assertTrue(evaluate(p)["technical_render_ready"])

    def test_C14_reviewed_2d_root_scale_and_background_are_locked(self):
        from production.sequence_geometry import validate_geometry

        p = self.packet()
        unit = dict(
            continuity_strength="camera_locked", camera_and_crop_lock="native_fixture"
        )
        observed = dict(
            root_xy=[24, 30],
            body_extent_wh=[20, 24],
            canvas_wh=[48, 32],
            crop_xywh=[8, 0, 32, 32],
            protected_background_pixel_sha256="synthetic protected RGB digest",
        )
        reviews = {
            u["id"]: dict(
                geometry=dict(
                    status="reviewed",
                    reviewer="synthetic measurements",
                    source_sha256=u["source"]["sha256"],
                    fit_sha256=u["fit"]["pixel_sha256"],
                    camera_and_crop_lock="native_fixture",
                    observed=copy.deepcopy(observed),
                )
            )
            for u in p["resolved_images"]
        }
        validate_geometry(unit, p["resolved_images"], reviews)
        for field, value in [
            ("root_xy", [25, 30]),
            ("body_extent_wh", [22, 24]),
            ("protected_background_pixel_sha256", "different"),
            ("canvas_wh", [47, 32]),
            ("crop_xywh", [0, 0, 32, 32]),
        ]:
            altered = copy.deepcopy(reviews)
            altered["B"]["geometry"]["observed"][field] = value
            with (
                self.subTest(field=field),
                self.assertRaisesRegex(ValueError, "differs"),
            ):
                validate_geometry(unit, p["resolved_images"], altered)
