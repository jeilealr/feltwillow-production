"""Exercise local gallery/media delivery, including browser seek requests."""
from functools import partial
import http.client
from http.server import ThreadingHTTPServer
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch, MagicMock
import errno
import contextlib
import io

from production.serve_scene_review import ReviewHandler, gallery_assets
from production import serve_scene_review as review


class ReviewLifecycleTests(unittest.TestCase):
    def test_interrupt_is_clean_exit(self):
        server = MagicMock()
        server.__enter__.return_value = server
        server.serve_forever.side_effect = KeyboardInterrupt
        with patch.object(review, 'ThreadingHTTPServer', return_value=server), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(review.main([]), 0)
        self.assertIn('stopped normally', output.getvalue())
        server.__exit__.assert_called_once()

    def test_occupied_port_reuses_only_matching_server(self):
        for matches, expected in [(True, 0), (False, 1)]:
            with patch.object(review, 'ThreadingHTTPServer', side_effect=OSError(errno.EADDRINUSE, 'busy')), patch.object(review, 'existing_review', return_value=matches), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(review.main([]), expected)

    def test_sandbox_denial_is_clear(self):
        with patch.object(review, 'ThreadingHTTPServer', side_effect=PermissionError(errno.EPERM, 'denied')), contextlib.redirect_stderr(io.StringIO()) as output:
            self.assertEqual(review.main([]), 1)
        self.assertIn('sandbox', output.getvalue())

    def test_live_allowlist_refreshes_without_serving_private_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'review.html').write_text('<img src="first.png">')
            (root/'first.png').write_bytes(b'first')
            (root/'second.png').write_bytes(b'second')
            (root/'private.txt').write_text('private')
            with patch.object(review, 'GALLERY', Path('review.html')), patch.object(review, 'review_assets', side_effect=lambda r: gallery_assets(r, Path('review.html'))):
                loader = review.LiveReviewAssets(root)
                self.assertIn('/first.png', loader())
                (root/'review.html').write_text('<img src="second.png"><p>updated</p>')
                self.assertIn('/second.png', loader())
                self.assertNotIn('/first.png', loader())
                self.assertNotIn('/private.txt', loader())


class QuietHandler(ReviewHandler):
    def log_message(self, *args):
        pass


class SceneReviewServerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root/'audio.wav').write_bytes(b'RIFF0123456789')
        (self.root/'private.txt').write_text('not served')
        (self.root/'review.html').write_text('<audio controls src="audio.wav"></audio>')
        handler = partial(QuietHandler, assets=gallery_assets(self.root, Path('review.html')), gallery_url='/review.html')
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.client = http.client.HTTPConnection('127.0.0.1', self.server.server_port)

    def tearDown(self):
        self.client.close()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    def request(self, method, path, headers=None):
        self.client.request(method, path, headers=headers or {})
        response = self.client.getresponse()
        return response, response.read()

    def test_audio_delivery_and_seek(self):
        response, data = self.request('GET', '/audio.wav')
        self.assertEqual(response.status, 200)
        self.assertEqual(data, b'RIFF0123456789')
        self.assertIn(response.getheader('Content-Type'), {'audio/x-wav', 'audio/wav', 'audio/vnd.wave'})
        for requested, expected in [('bytes=4-7', b'0123'), ('bytes=10-', b'6789'), ('bytes=-3', b'789')]:
            response, data = self.request('GET', '/audio.wav', {'Range': requested})
            self.assertEqual(response.status, 206)
            self.assertEqual(data, expected)
            self.assertEqual(response.getheader('Accept-Ranges'), 'bytes')
        response, data = self.request('HEAD', '/audio.wav')
        self.assertEqual(response.status, 200)
        self.assertEqual(data, b'')
        self.assertEqual(response.getheader('Content-Length'), '14')

    def test_invalid_ranges_and_unlisted_files(self):
        for requested in ['bytes=99-', 'bytes=4-2', 'bytes=-0', 'bytes=0-1,4-5']:
            response, _ = self.request('GET', '/audio.wav', {'Range': requested})
            self.assertEqual(response.status, 416)
        for url in ['/private.txt', '/../private.txt', '/%2e%2e/private.txt']:
            response, _ = self.request('GET', url)
            self.assertEqual(response.status, 404)
        response, _ = self.request('GET', '/')
        self.assertEqual(response.status, 302)
        self.assertEqual(response.getheader('Location'), '/review.html')

    def test_all_actual_gallery_media_exist(self):
        from production.serve_scene_review import ROOT, GALLERY
        assets = gallery_assets(ROOT, GALLERY)
        self.assertEqual(sum(path.suffix == '.wav' for path in assets.values()), 18)
        self.assertEqual(sum(path.suffix == '.png' for path in assets.values()), 24)
