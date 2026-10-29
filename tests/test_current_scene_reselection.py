"""Current source-still choices supersede historical ledger rows without editing them."""

import json
import unittest
from pathlib import Path

from production.sequence_plan import selection_catalog
from production.selected_scene_review import verify


ROOT = Path(__file__).resolve().parents[1]
STORY = ROOT / "stories/lion_and_mouse_v7"


class CurrentSceneReselectionTests(unittest.TestCase):
    def test_current_s05_s06_choices_and_historical_ledger(self):
        expected = {
            "S05-L008-B01-I02": ("r006_candidate.png", "85e66871fee731d49fc883479566330036c9c9b8341edbd9560ccc6e28f27390"),
            "S05-L008-B01-I04": ("r003_candidate.png", "10a3eeaca9a28e2f889f12569813edddc895a610d5e90c35fc97421326a99b6a"),
            "S06-L002-B01-I01": ("r008_candidate.png", "1269b655db35c289a98268e75419cc84c49b8abeba7776b14d5dc87301979f80"),
            "S06-L002-B01-I02": ("r008_candidate.png", "9caf62625858af027d27735b973a114d7e42a1edcf37829d9a69169480dea84e"),
        }
        current = {row.get("image_id"): row for row in selection_catalog(STORY)}
        for image_id, (suffix, sha) in expected.items():
            self.assertTrue(current[image_id]["path"].endswith(suffix))
            self.assertEqual(current[image_id]["sha256"], sha)
            self.assertTrue((ROOT / current[image_id]["path"]).is_file())
        historical = json.loads((STORY / "scene_image_selection_s01_s05.json").read_text())
        old = next(row for row in historical["images"] if row["image_id"] == "S05-L008-B01-I04")
        self.assertTrue(old["path"].endswith("r002_candidate.png"))
        _, gallery, _ = verify(ROOT, "lion_and_mouse_v7")
        now = next(row for row in gallery["images"] if row["image_id"] == "S05-L008-B01-I04")
        self.assertTrue(now["path"].endswith("r003_candidate.png"))
        s04 = next(row for row in gallery["images"] if row["image_id"] == "S04-L005-B01-I01")
        self.assertTrue(s04["path"].endswith("r002_candidate.png"))


if __name__ == "__main__":
    unittest.main()
