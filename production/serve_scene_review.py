"""Serve the scene gallery and its referenced media on loopback only."""
import argparse
import errno
import hashlib
import http.client
from functools import partial
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import mimetypes
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

try:
    from .audio_visual_plan import source_file
except ImportError:
    from audio_visual_plan import source_file

ROOT = Path(__file__).resolve().parents[1]
GALLERY = Path('stories/lion_and_mouse_v7/review/scene_compositions/s01_s03_r001/review.html')
PERFORMANCE_GALLERY = Path('stories/lion_and_mouse_v7/review/character_performance_consistency_r001/review.html')
MILO_GALLERY = PERFORMANCE_GALLERY.parent / 'milo_foundations_r001/review.html'
MILO_WALK_GALLERY = PERFORMANCE_GALLERY.parent / 'milo_walk_correction_r002/review.html'
MILO_LEAN_GALLERY = PERFORMANCE_GALLERY.parent / 'milo_walk_lean_r003/review.html'
MILO_OPENING_GALLERY = PERFORMANCE_GALLERY.parent / 'milo_opening_poses_r001/review.html'
MILO_REPAIR_GALLERY = PERFORMANCE_GALLERY.parent / 'milo_proportion_repairs_r002/review.html'
MILO_SEED_GALLERY = PERFORMANCE_GALLERY.parent / 'milo_seed_correction_r003/review.html'
MILO_SEED_R004_GALLERY = PERFORMANCE_GALLERY.parent / 'milo_seed_correction_r004/review.html'
MILO_MISSING_GALLERY = PERFORMANCE_GALLERY.parent / 'milo_s01_s03_missing_r001/review.html'
MILO_ANATOMY_GALLERY = PERFORMANCE_GALLERY.parent / 'milo_anatomy_r001/review.html'
POSE_LIBRARY_GALLERY = PERFORMANCE_GALLERY.parent / 'pose_library/review.html'
CANONICAL_RATIOS_GALLERY = PERFORMANCE_GALLERY.parent / 'canonical_measurements_r001/review.html'
PERFORMANCE_SCENES_GALLERY = GALLERY.parent.parent / 's01_s03_performance_r002/review.html'
CORRECTION_SCENES_GALLERY = GALLERY.parent.parent / 's01_s03_corrections_r003/review.html'


class MediaLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag in {'img', 'audio', 'source'}:
            self.sources.extend(value for key, value in attrs if key == 'src')


def gallery_assets(root, gallery):
    page = (root / gallery).resolve()
    parser = MediaLinks()
    parser.feed(page.read_text())
    paths = [page] + [(page.parent / source).resolve() for source in parser.sources]
    assets = {}
    for path in paths:
        relative = path.relative_to(root.resolve())
        source = source_file(root, relative.as_posix())
        if not source.is_file():
            raise FileNotFoundError(path)
        assets['/' + relative.as_posix()] = source
    return assets


def review_assets(root):
    """Explicit page allowlist; never crawl arbitrary links or serve the repo."""
    assets = gallery_assets(root, GALLERY)
    if (root / PERFORMANCE_GALLERY).is_file():
        assets.update(gallery_assets(root, PERFORMANCE_GALLERY))
    if (root / MILO_GALLERY).is_file():
        assets.update(gallery_assets(root, MILO_GALLERY))
    if (root / MILO_WALK_GALLERY).is_file():
        assets.update(gallery_assets(root, MILO_WALK_GALLERY))
    if (root / MILO_LEAN_GALLERY).is_file():
        assets.update(gallery_assets(root, MILO_LEAN_GALLERY))
    if (root / MILO_OPENING_GALLERY).is_file():
        assets.update(gallery_assets(root, MILO_OPENING_GALLERY))
    if (root / MILO_REPAIR_GALLERY).is_file():
        assets.update(gallery_assets(root, MILO_REPAIR_GALLERY))
    if (root / MILO_SEED_GALLERY).is_file():
        assets.update(gallery_assets(root, MILO_SEED_GALLERY))
    if (root / MILO_SEED_R004_GALLERY).is_file():
        assets.update(gallery_assets(root, MILO_SEED_R004_GALLERY))
    if (root / MILO_MISSING_GALLERY).is_file():
        assets.update(gallery_assets(root, MILO_MISSING_GALLERY))
    if (root / MILO_ANATOMY_GALLERY).is_file():
        assets.update(gallery_assets(root, MILO_ANATOMY_GALLERY))
    if (root / POSE_LIBRARY_GALLERY).is_file():
        assets.update(gallery_assets(root, POSE_LIBRARY_GALLERY))
    if (root / CANONICAL_RATIOS_GALLERY).is_file():
        assets.update(gallery_assets(root, CANONICAL_RATIOS_GALLERY))
    if (root / PERFORMANCE_SCENES_GALLERY).is_file():
        assets.update(gallery_assets(root, PERFORMANCE_SCENES_GALLERY))
    if (root / CORRECTION_SCENES_GALLERY).is_file():
        assets.update(gallery_assets(root, CORRECTION_SCENES_GALLERY))
    return assets


class ReviewHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, assets, gallery_url, asset_loader=None, identity=None, **kwargs):
        self.assets = assets
        self.asset_loader = asset_loader
        self.identity = identity
        self.gallery_url = gallery_url
        super().__init__(*args, **kwargs)

    def do_HEAD(self):
        self.respond(head=True)

    def do_GET(self):
        self.respond(head=False)

    def respond(self, head):
        url = unquote(urlsplit(self.path).path)
        if url == '/__feltwillow_review_health' and self.identity:
            body = self.identity.encode('ascii')
            self.send_response(200)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            if not head:
                self.wfile.write(body)
            return
        if self.asset_loader:
            try:
                self.assets = self.asset_loader()
            except (OSError, ValueError):
                self.send_error(503, 'Review media update incomplete; retry after gallery rebuild')
                return
        if url == '/':
            self.send_response(302)
            self.send_header('Location', self.gallery_url)
            self.send_header('Content-Length', '0')
            self.end_headers()
            return
        path = self.assets.get(url)
        if path is None:
            self.send_error(404)
            return
        size = path.stat().st_size
        start, end = 0, size - 1
        requested = self.headers.get('Range')
        if requested:
            match = re.fullmatch(r'bytes=(\d*)-(\d*)', requested)
            valid = match and any(match.groups()) and size > 0
            if valid:
                first, last = match.groups()
                if first:
                    start = int(first)
                    end = min(int(last), size - 1) if last else size - 1
                else:
                    start = max(0, size - int(last))
                valid = 0 <= start <= end < size
            if not valid:
                self.send_response(416)
                self.send_header('Content-Range', f'bytes */{size}')
                self.send_header('Content-Length', '0')
                self.end_headers()
                return
        self.send_response(206 if requested else 200)
        self.send_header('Content-Type', mimetypes.guess_type(str(path))[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(end - start + 1))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-cache')
        if requested:
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.end_headers()
        if not head:
            with path.open('rb') as source:
                source.seek(start)
                remaining = end - start + 1
                while remaining:
                    block = source.read(min(65536, remaining))
                    if not block:
                        break
                    try:
                        self.wfile.write(block)
                    except (BrokenPipeError, ConnectionResetError):
                        break
                    remaining -= len(block)


class LiveReviewAssets:
    """Refresh the explicit media allowlist when registered HTML pages change."""
    def __init__(self, root):
        self.root = root
        self.signature = None
        self.assets = None

    def __call__(self):
        pages = [value for name, value in globals().items()
                 if name.endswith('GALLERY') and isinstance(value, Path)]
        signature = tuple((str(p), (self.root/p).stat().st_mtime_ns,
                           (self.root/p).stat().st_size)
                          for p in pages if (self.root/p).is_file())
        if signature != self.signature:
            assets = review_assets(self.root)
            self.assets, self.signature = assets, signature
        return self.assets


def server_identity(root):
    return 'feltwillow-review-v2:' + hashlib.sha256(str(root.resolve()).encode()).hexdigest()


def existing_review(port, identity):
    connection = http.client.HTTPConnection('127.0.0.1', port, timeout=2)
    try:
        connection.request('GET', '/__feltwillow_review_health')
        response = connection.getresponse()
        return response.status == 200 and response.read(200).decode('ascii', errors='replace') == identity
    except (OSError, http.client.HTTPException):
        return False
    finally:
        connection.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--gallery', choices=['scenes', 'performance'], default='scenes')
    args = parser.parse_args(argv)
    if not 0 <= args.port <= 65535:
        parser.error('port must be between 0 and 65535')
    loader = LiveReviewAssets(ROOT)
    assets = loader()
    gallery = PERFORMANCE_GALLERY if args.gallery == 'performance' else (CORRECTION_SCENES_GALLERY if (ROOT/CORRECTION_SCENES_GALLERY).is_file() else GALLERY)
    if '/' + gallery.as_posix() not in assets:
        parser.error('Run the character performance audit to build that gallery first')
    identity = server_identity(ROOT)
    handler = partial(ReviewHandler, assets=assets, gallery_url='/' + gallery.as_posix(),
                      asset_loader=loader, identity=identity)
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), handler)
    except OSError as exc:
        if exc.errno == errno.EADDRINUSE:
            if existing_review(args.port, identity):
                print(f'Review server already running: http://127.0.0.1:{args.port}/{gallery.as_posix()}')
                print('Reuse it; registered gallery/media updates reload automatically.')
                return 0
            print(f'Port {args.port} is occupied by another or older server. No process was stopped. '
                  'Reuse its existing page, stop it in its own terminal, or choose --port 8766.', file=sys.stderr)
            return 1
        if exc.errno in {errno.EACCES, errno.EPERM}:
            print('Loopback port binding was denied by the execution sandbox. Run with the required '
                  'tool approval or from your local feltwillow terminal.', file=sys.stderr)
            return 1
        raise
    with server:
        print(f'Scene review ready: http://127.0.0.1:{server.server_port}/', flush=True)
        print('Open this URL in the VS Code browser. Ctrl+C stops the server.', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nReview server stopped normally.', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
