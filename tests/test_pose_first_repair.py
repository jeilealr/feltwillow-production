"""CPU synthetic regression tests: reference gating, staging, provenance and safety."""
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from production.pose_first_repair import (
    S05_BACKGROUND, S05_PREVIOUS, compose_unchanged_body,
    digest, pilot_s05, repo_path, resolve_pose, s05_roll_staging,
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
        row = pilot_s05(self.root, dest, allow_provisional=True)
        self.assertEqual(len(row["candidates"]), 3)
        self.assertEqual(row["selection_effect"], "none")
        self.assertEqual([c["checks"]["origin_pixels"] for c in row["candidates"]],
                         [[780, 475], [830, 490], [880, 505]])
        self.assertTrue(all(c["owner_scene_selection"] is None for c in row["candidates"]))
        self.assertTrue((dest / "CONTACT_SHEET.jpg").is_file())
        self.assertIn("Previous roll scene", (dest / "REVIEW.html").read_text())
        self.assertTrue((dest / "RECEIPTS.json").is_file())
        with self.assertRaises(FileExistsError):
            pilot_s05(self.root, dest, allow_provisional=True)


if __name__ == "__main__":
    unittest.main()
