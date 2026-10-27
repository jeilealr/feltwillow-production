"""Read-only current selected bytes and their production blockers, not visual passes."""

import json, tempfile, unittest
from pathlib import Path
from production.sequence_plan import digest, selection_catalog, resolve_sequence
from production.visual_grammar import unit_for_sequence

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "stories/lion_and_mouse_v7"


class CurrentV7Assets(unittest.TestCase):
    def test_C13_exact_accepted_fork_r004_and_r001_anchor(self):
        expected = {
            "S03-L001-B01-I02": "5163cea0a436d27ec4b1ea4a16c857b5ffdb504a0309d587fe34d84a7d2beee6",
            "S03-L006-B01-I02": "7842d9c8a4c2f67848fb38195d11544e985f414a61e6a8f0a4658208bd80fb68",
        }
        records = selection_catalog(FOLDER)
        for iid, sha in expected.items():
            choices = [r for r in records if r.get("image_id") == iid]
            self.assertEqual({r["sha256"] for r in choices}, {sha})
            path = ROOT / choices[0]["path"]
            if not path.is_file():
                self.skipTest("selected raster unavailable on this host: " + str(path))
            self.assertEqual(digest(path), sha)

    def test_C05_landscape_prompt_cast_and_C39_support_block(self):
        plan = json.loads((FOLDER / "audio_visual_plan.json").read_text())
        sequence = plan["production_sequences"]["s02_line_002"]
        self.assertEqual(unit_for_sequence(plan, "s02_line_002")["visible_cast"], [])
        prompt = " ".join(e.get("prompt", "") for e in sequence["edges"]).lower()
        for text in ("cream patch", "orange tail", "body proportions", "milo is"):
            self.assertNotIn(text, prompt)
        self.assertTrue(
            any(
                "beside-stone" in b
                for b in plan["production_sequences"]["s02_acorn"]["blockers"]
            )
        )

    def test_C19_candidate_cannot_replace_three_blocked_selected_uses(self):
        from PIL import Image

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / "old.png"
            new = root / "new.png"
            Image.new("RGB", (32, 32), "red").save(old)
            Image.new("RGB", (32, 32), "green").save(new)
            keys = ["L016", "L017", "L018"]
            images = [dict(id=i, state="same", location_view="same") for i in keys]
            plan = dict(
                story="fixture",
                lines=[
                    dict(
                        beats=[
                            dict(
                                id="beat",
                                cast=["Leo"],
                                image_sequence=dict(images=images),
                            )
                        ]
                    )
                ],
                production_blocks={
                    digest(old): dict(status="needs_repair", reason="missing_paw")
                },
                production_sequences={
                    "uses": dict(
                        id="uses",
                        uses=[dict(id=i, image_id=i) for i in keys],
                        edges=[
                            dict(**{"from": a, "to": b}, kind="hold", prompt="Hold.")
                            for a, b in zip(keys, keys[1:])
                        ],
                    )
                },
            )
            selected = [
                dict(image_id=i, path="old.png", sha256=digest(old)) for i in keys
            ]
            packet = resolve_sequence(plan, "uses", root, selected, size=(32, 32))
            self.assertTrue(
                all(
                    u["status"] == "owner_selected_but_technically_blocked"
                    for u in packet["resolved_images"]
                )
            )
            # Merely returning a new candidate cannot change any selected use.
            packet = resolve_sequence(plan, "uses", root, selected, size=(32, 32))
            self.assertEqual(
                {u["source"]["sha256"] for u in packet["resolved_images"]},
                {digest(old)},
            )
            selected = [
                dict(image_id=i, path="new.png", sha256=digest(new)) for i in keys
            ]
            packet = resolve_sequence(plan, "uses", root, selected, size=(32, 32))
            self.assertTrue(
                all(u["status"] == "selected_exact" for u in packet["resolved_images"])
            )
            self.assertEqual(
                len({u["source"]["sha256"] for u in packet["resolved_images"]}), 1
            )
            self.assertTrue(old.is_file())
