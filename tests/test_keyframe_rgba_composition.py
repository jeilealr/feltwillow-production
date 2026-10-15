"""RGBA overlays must preserve alpha holes and the protected plate."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

from production.keyframe import compose


@unittest.skipUnless(all(importlib.util.find_spec(name) for name in ("numpy", "PIL", "cv2")),
                     "requires image runtime")
class RGBACompositionTests(unittest.TestCase):
    def test_transparent_holes_and_protected_pixels_survive_composition(self):
        import numpy as np
        from PIL import Image

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plate = np.full((100, 200, 3), (37, 83, 121), dtype=np.uint8)
            layer = np.zeros((30, 30, 4), dtype=np.uint8)
            layer[5:25, 5:25] = (220, 60, 30, 255)
            layer[12:18, 12:18] = (255, 255, 255, 0)
            Image.fromarray(plate).save(root / "plate.png")
            Image.fromarray(layer).save(root / "layer.png")
            record = compose(root / "plate.png", [{"still": str(root / "layer.png"),
                "h": 0.2, "x": 0.5, "y": 0.7, "shadow": 0, "light": 0}],
                root / "out.png", write_edit_mask=True)
            output = np.asarray(Image.open(root / "out.png"))
            mask = np.asarray(Image.open(root / "out_edit_mask.png"))
            self.assertTrue(np.array_equal(output[mask == 0], plate[mask == 0]))
            self.assertTrue(np.array_equal(output[60, 100], plate[60, 100]))
            self.assertTrue(np.array_equal(output[52, 92], (220, 60, 30)))
            self.assertEqual(record["characters"][0]["box"], [90, 50, 20, 20])


if __name__ == "__main__":
    unittest.main()
