"""CPU synthetic regression tests: reference gating, staging, provenance and safety."""
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from production.pose_first_repair import (
    S05_BACKGROUND, S05_PREVIOUS, compose_unchanged_body,
    anchored_transform, digest, grounded_preview, phase_review, pilot_s05,
    repo_path, resolve_pose, s05_roll_staging, visible_alpha_bounds,
)


class PoseFirstRepairTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        folder = self.root / "stories/lion_and_mouse_v7"
        folder.mkdir(parents=True)
        poses = self.root / "character/characters/lion_and_mouse_v7/Milo/poses"
        poses.mkdir(parents=True)
        img = Image.new("RGBA", (120, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((12, 13, 96, 86), fill=(100, 90, 81, 255))
        draw.ellipse((3, 16, 25, 39), fill=(120, 112, 93, 255))
        self.posepath = poses / "milo_nose_landing.png"
        roll = poses / "milo_roll.png"
        img.save(self.posepath)
        img.save(roll)
        canonical = self.root / "character/characters/lion_and_mouse_v7/Milo/canonical/milo.png"
        canonical.parent.mkdir(parents=True)
        img.save(canonical)
        self.asset = "milo.tumble.flank_to_face.3q"
        self.nose_record = {"path": str(self.posepath.relative_to(self.root)), "sha256": digest(self.posepath)}
        self.roll_record = {"path": str(roll.relative_to(self.root)), "sha256": digest(roll)}
        canonical_rec = {"path": str(canonical.relative_to(self.root)), "sha256": digest(canonical)}
        self.posepath.with_suffix(".json").write_text(json.dumps({
            "image_sha256": digest(self.posepath), "asset_id": self.asset,
            "variant": "nose_landing", "status": "candidate_pending_owner_review",
        }))
        roll.with_suffix(".json").write_text(json.dumps({
            "image_sha256": digest(roll), "asset_id": self.asset,
            "variant": "roll", "status": "owner_selected_for_performance",
        }))
        lib = {"assets": {self.asset: {"actor": "Milo", "canonical": canonical_rec,
                              "variants": {
                                  "roll": {"file": self.roll_record, "status": "owner_selected_for_performance"},
                                  "nose_landing": {"file": self.nose_record,
                                                   "status": "candidate_pending_owner_review"},
                              }}}}
        (folder / "character_performance_library.json").write_text(json.dumps(lib))
        bg = self.root / S05_BACKGROUND
        bg.parent.mkdir(parents=True)
        Image.new("RGB", (1672, 941), (22, 48, 64)).save(bg)
        previous = self.root / S05_PREVIOUS
        Image.new("RGB", (1672, 941), (27, 47, 71)).save(previous)
        record = {
            "path": S05_PREVIOUS, "sha256": digest(previous),
            "creation": {
                "background": {"path": S05_BACKGROUND, "sha256": digest(bg)},
                "actor": self.roll_record,
                "scale": 0.32, "translate_pixels": [830, 490],
            },
        }
        previous.with_suffix(".json").write_text(json.dumps(record))
        self.bg = bg
        self.previous = previous
        self.prevside = previous.with_suffix(".json")

    def resolve(self, *, allow_provisional=False, actor="Milo", variant="nose_landing"):
        return resolve_pose(self.root, "lion_and_mouse_v7", actor, self.asset, variant,
                            allow_provisional=allow_provisional)

    def test_requires_owner_selected_pose_for_production(self):
        with self.assertRaises(PermissionError):
            self.resolve()
        row = self.resolve(allow_provisional=True)
        self.assertTrue(row["requires_owner_pose_review"])
        self.assertFalse(self.resolve(variant="roll")["requires_owner_pose_review"])

    def test_wrong_actor_and_tampered_source(self):
        with self.assertRaises(ValueError):
            self.resolve(allow_provisional=True, actor="Leo")
        self.posepath.write_bytes(self.posepath.read_bytes() + b"changed")
        with self.assertRaises(ValueError):
            self.resolve(allow_provisional=True)

    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError):
            repo_path(self.root, "../../untrusted.png")

    def test_roll_provenance_drives_camera(self):
        shot = s05_roll_staging(self.root)
        self.assertEqual(shot["origin"], [830, 490])
        self.assertEqual(shot["scale"], 0.32)
        self.assertEqual(shot["roll_pose"], self.roll_record)

    def test_rejects_wrong_actor_reference_in_roll_scene(self):
        record = json.loads(self.prevside.read_text())
        record["creation"]["actor"]["sha256"] = "0" * 64
        self.prevside.write_text(json.dumps(record))
        with self.assertRaises(ValueError):
            s05_roll_staging(self.root)

    def test_rejects_background_hash_mismatch(self):
        Image.new("RGB", (1672, 941), (0, 0, 0)).save(self.bg)
        with self.assertRaises(ValueError):
            s05_roll_staging(self.root)

    def test_rejects_cropped_pose(self):
        with Image.open(self.posepath) as im:
            actor = im.copy()
        with self.assertRaises(ValueError):
            compose_unchanged_body(Image.new("RGB", (100, 90)), actor, (75, 50), 1.)

    def test_protected_pixels(self):
        with Image.open(self.posepath) as im:
            actor = im.copy()
        plate = Image.new("RGB", (400, 300), (15, 25, 35))
        rendered, mask, checks = compose_unchanged_body(plate, actor, (93, 120), .70)
        delta = np.any(np.asarray(rendered) != np.asarray(plate), axis=2)
        bound = np.asarray(mask) > 0
        self.assertFalse((delta & ~bound).any())
        self.assertEqual(checks["changed_pixels_outside_effect_mask"], 0)
        self.assertFalse(checks["actor_semantically_redrawn"])
        self.assertIsNone(checks["physical_contact_pass"])

    def test_pilot_unselected_placement_immutable_and_gallery(self):
        dest = self.root / "candidate_review"
        with self.assertRaises(PermissionError):
            pilot_s05(self.root, dest)
        self.assertFalse(dest.exists())
        with self.assertRaisesRegex(ValueError, "review required"):
            pilot_s05(self.root, dest, allow_provisional=True)
        row = pilot_s05(self.root, dest, allow_provisional=True,
                        phase_evidence=self.review())
        self.assertEqual(len(row["candidates"]), 3)
        self.assertEqual(row["selection_effect"], "none")
        self.assertEqual([c["checks"]["origin_pixels"] for c in row["candidates"]],
                         [[780, 475], [830, 490], [880, 505]])
        self.assertTrue(all(c["owner_scene_selection"] is None for c in row["candidates"]))
        self.assertTrue((dest / "CONTACT_SHEET.jpg").is_file())
        self.assertIn("Previous roll scene", (dest / "REVIEW.html").read_text())
        self.assertTrue((dest / "RECEIPTS.json").is_file())
        with self.assertRaises(FileExistsError):
            pilot_s05(self.root, dest, allow_provisional=True,
                      phase_evidence=self.review())

    def review(self, verdict="plausible_for_preview"):
        return {"schema": "feltwillow.pose-phase-visual-review.v1",
                "image": self.nose_record, "asset_id": self.asset,
                "variant": "nose_landing",
                "expected": {"action_phase": "immediate_post_roll_grounded_impact"},
                "observed": {key: True for key in (
                    "low_side_grounded", "connected_limbs", "head_and_nose_correct",
                    "matches_roll_identity", "expression_matches_impact")},
                "technical_visual_verdict": verdict, "reviewer_basis": "synthetic fixture"}

    def test_phase_gate_rejects_upright_even_for_preview(self):
        with self.assertRaisesRegex(ValueError, "not visually suitable"):
            phase_review(self.root, self.review("unsuitable_upright_recovery"),
                         self.resolve(allow_provisional=True), preview=True)

    def test_provisional_rejects_forbidden_lifecycle(self):
        libpath = self.root / "stories/lion_and_mouse_v7/character_performance_library.json"
        for status in ("rejected", "superseded", "unknown"):
            lib = json.loads(libpath.read_text())
            lib["assets"][self.asset]["variants"]["nose_landing"]["status"] = status
            libpath.write_text(json.dumps(lib))
            side = json.loads(self.posepath.with_suffix(".json").read_text())
            side["status"] = status
            self.posepath.with_suffix(".json").write_text(json.dumps(side))
            with self.assertRaises(PermissionError):
                self.resolve(allow_provisional=True)

    def test_two_anchor_geometry_rejects_wrong_vector(self):
        translation, residual = anchored_transform((0, 0), (10, 0), (20, 30),
                                                    (25, 30), .5, 0)
        self.assertEqual(translation, (20, 30))
        self.assertEqual(residual, 0)
        with self.assertRaisesRegex(ValueError, "Incompatible"):
            anchored_transform((0, 0), (10, 0), (20, 30), (80, 30), .5, 2)

    def test_visible_alpha_ignores_edge_noise_and_keeps_render_pixels(self):
        actor = Image.new("RGBA", (40, 30))
        actor.putpixel((0, 1), (100, 100, 100, 1))
        ImageDraw.Draw(actor).rectangle((10, 10, 25, 25), fill=(80, 80, 80, 255))
        self.assertEqual(visible_alpha_bounds(actor), (10, 10, 26, 26))
        rendered, _, _ = compose_unchanged_body(Image.new("RGB", (100, 80), "white"), actor,
                                                  (20, 20), 1, ((18, 25),))
        self.assertEqual(actor.getpixel((0, 1))[3], 1)
        self.assertEqual(rendered.size, (100, 80))

    def test_grounded_preview_is_one_immutable_cpu_candidate(self):
        anchors = {"schema": "feltwillow.s05-grounded-anchors.v1",
                   "pose_sha256": self.nose_record["sha256"],
                   "plate_sha256": digest(self.bg), "provenance": "manual_native_review",
                   "actor": {"support": [20, 70], "nose": [70, 30]},
                   "scene": {"support": [850, 790], "nose": [866, 777.2]},
                   "scale": .32, "tolerance_px": 1}
        dest = self.root / "grounded"
        with self.assertRaisesRegex(ValueError, "not visually suitable"):
            grounded_preview(self.root, dest, self.review("unsuitable_upright_recovery"), anchors)
        self.assertFalse(dest.exists())
        row = grounded_preview(self.root, dest, self.review(), anchors)
        self.assertEqual(row["provider_calls"], 0)
        self.assertFalse(row["scene_ready"])
        self.assertIsNone(row["owner_scene_selection"])
        self.assertTrue((dest / "REVIEW.html").exists())
        with self.assertRaises(FileExistsError):
            grounded_preview(self.root, dest, self.review(), anchors)


if __name__ == "__main__":
    unittest.main()
