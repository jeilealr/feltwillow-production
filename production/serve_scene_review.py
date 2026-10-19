"""Serve the scene gallery and its referenced media on loopback only."""
import argparse
from functools import partial
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import mimetypes
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
GALLERY = Path('stories/lion_and_mouse_v7/review/scene_compositions/s01_s03_r001/review.html')


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
        if not path.is_file():
            raise FileNotFoundError(path)
        assets['/' + relative.as_posix()] = path
    return assets


class ReviewHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, assets, gallery_url, **kwargs):
        self.assets = assets
        self.gallery_url = gallery_url
        super().__init__(*args, **kwargs)

    def do_HEAD(self):
        self.respond(head=True)

    def do_GET(self):
        self.respond(head=False)

    def respond(self, head):
        url = unquote(urlsplit(self.path).path)
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    assets = gallery_assets(ROOT, GALLERY)
    handler = partial(ReviewHandler, assets=assets, gallery_url='/' + GALLERY.as_posix())
    with ThreadingHTTPServer(('127.0.0.1', args.port), handler) as server:
        print(f'Scene review ready: http://127.0.0.1:{server.server_port}/', flush=True)
        print('Open this URL in the VS Code browser. Ctrl+C stops the server.', flush=True)
        server.serve_forever()


if __name__ == '__main__':
    main()
