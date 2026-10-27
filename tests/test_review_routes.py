import tempfile, unittest
from pathlib import Path
from production.serve_scene_review import sequence_pages, gallery_assets


class GroupedReviewRoutes(unittest.TestCase):
    def test_explicit_grouped_pages_and_media_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "stories/lion_and_mouse_v7/review/mac_engineering_r006"
            folder.mkdir(parents=True)
            (folder / "OWNER_REVIEW.html").write_text(
                '<a href="native.png"><img src="fit.png"></a>'
            )
            (folder / "fit.png").write_bytes(b"fixture")
            (folder / "native.png").write_bytes(b"native")
            (folder / "private.html").write_text("not registered")
            pages = sequence_pages(root)
            self.assertEqual(pages, [(folder / "OWNER_REVIEW.html").relative_to(root)])
            assets = gallery_assets(root, pages[0])
            self.assertEqual(len(assets), 3)
            self.assertNotIn(
                "/stories/lion_and_mouse_v7/review/mac_engineering_r006/private.html",
                assets,
            )
