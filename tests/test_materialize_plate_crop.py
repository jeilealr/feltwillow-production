"""Registered plate crops can be rebuilt without ignored work/ assets."""

import tempfile
import unittest
from pathlib import Path

from production.materialize_plate_crop import _read_png, _write_png, materialize


class MaterializePlateCropTests(unittest.TestCase):
    def test_crop_receipt_binds_source_rect_pixels_and_output_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plate = root / "plate.png"
            pixels = b"".join(bytes((x, y, 0)) for y in range(50) for x in range(100))
            _write_png(plate, 100, 50, 3, pixels)
            output = root / "crop.png"
            receipt = materialize(plate, [0.2, 0.2, 0.4, 0.4], output)
            self.assertEqual(receipt["source_plate"], "plate.png")
            self.assertFalse(Path(receipt["source_plate"]).is_absolute())
            self.assertEqual(receipt["crop_rect_on_plate"], [0.2, 0.2, 0.4, 0.4])
            self.assertEqual(receipt["pixel_box"], [20, 10, 60, 30])
            self.assertEqual(receipt["sha256"], __import__("hashlib").sha256(output.read_bytes()).hexdigest())
            width, height, channels, cropped = _read_png(output)
            self.assertEqual((width, height, channels), (40, 20, 3))
            self.assertEqual(cropped[:3], bytes((20, 10, 0)))
            self.assertTrue(output.with_suffix(".png.json").is_file())

    def test_invalid_crop_outside_plate_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            plate = Path(directory) / "plate.png"
            _write_png(plate, 20, 10, 3, bytes((1, 2, 3)) * (20 * 10))
            with self.assertRaisesRegex(ValueError, "contained"):
                materialize(plate, [0.9, 0.1, 0.2, 0.2], Path(directory) / "bad.png")


if __name__ == "__main__":
    unittest.main()
