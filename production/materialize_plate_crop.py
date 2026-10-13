#!/usr/bin/env python3
"""Materialize a registered normalized plate crop without a work/ cache."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import zlib
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _portable_source_label(path: Path) -> str:
    resolved = path.resolve()
    repo = Path(__file__).resolve().parents[1]
    try:
        return resolved.relative_to(repo).as_posix()
    except ValueError:
        return path.name


def _read_png(path: Path) -> tuple[int, int, int, bytes]:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("plate must be a PNG")
    offset = len(PNG_SIGNATURE)
    width = height = color_type = bit_depth = interlace = None
    compressed = bytearray()
    while offset < len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        offset += 12 + length
        if kind == b"IHDR":
            width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(
                ">IIBBBBB", payload)
            if compression != 0 or filtering != 0:
                raise ValueError("unsupported PNG compression/filter method")
        elif kind == b"IDAT":
            compressed.extend(payload)
        elif kind == b"IEND":
            break
    if bit_depth != 8 or color_type not in (2, 6) or interlace != 0:
        raise ValueError("registered crop supports non-interlaced 8-bit RGB/RGBA PNG plates")
    channels = 3 if color_type == 2 else 4
    bpp = channels
    row_bytes = width * bpp
    packed = zlib.decompress(compressed)
    rows = []
    cursor = 0
    previous = bytearray(row_bytes)
    for _ in range(height):
        filter_type = packed[cursor]
        cursor += 1
        scan = bytearray(packed[cursor:cursor + row_bytes])
        cursor += row_bytes
        for i in range(row_bytes):
            left = scan[i - bpp] if i >= bpp else 0
            up = previous[i]
            upper_left = previous[i - bpp] if i >= bpp else 0
            if filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = up
            elif filter_type == 3:
                predictor = (left + up) // 2
            elif filter_type == 4:
                p = left + up - upper_left
                pa, pb, pc = abs(p-left), abs(p-up), abs(p-upper_left)
                predictor = left if pa <= pb and pa <= pc else up if pb <= pc else upper_left
            elif filter_type == 0:
                predictor = 0
            else:
                raise ValueError(f"unsupported PNG row filter {filter_type}")
            scan[i] = (scan[i] + predictor) & 255
        rows.append(bytes(scan))
        previous = scan
    return width, height, channels, b"".join(rows)


def _chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xffffffff)


def _write_png(path: Path, width: int, height: int, channels: int, pixels: bytes) -> None:
    color_type = 2 if channels == 3 else 6
    header = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    stride = width * channels
    scanlines = b"".join(b"\0" + pixels[y * stride:(y + 1) * stride] for y in range(height))
    encoded = PNG_SIGNATURE + _chunk(b"IHDR", header) + _chunk(b"IDAT", zlib.compress(scanlines)) + _chunk(b"IEND", b"")
    path.write_bytes(encoded)


def materialize(plate: Path, rect: list[float], output: Path) -> dict:
    if len(rect) != 4 or not all(isinstance(n, (int, float)) for n in rect):
        raise ValueError("crop rectangle must be normalized x, y, width, height")
    x, y, width, height = map(float, rect)
    if (x < 0 or y < 0 or width <= 0 or height <= 0 or
            x + width > 1.0000001 or y + height > 1.0000001):
        raise ValueError("normalized crop must be positive and contained in the plate")
    source_label = _portable_source_label(plate)
    plate = plate.resolve()
    if not plate.is_file():
        raise ValueError(f"approved plate does not exist: {plate}")
    source_hash = hashlib.sha256(plate.read_bytes()).hexdigest()
    w, h, channels, pixels = _read_png(plate)
    # Floor the top-left and ceil the bottom-right so the crop never loses a
    # registered edge. These integer rules are stable across callers.
    dx, dy, dw, dh = map(Decimal, map(str, (x, y, width, height)))
    box = (int((dx * w).to_integral_value(rounding=ROUND_FLOOR)),
           int((dy * h).to_integral_value(rounding=ROUND_FLOOR)),
           int(((dx + dw) * w).to_integral_value(rounding=ROUND_CEILING)),
           int(((dy + dh) * h).to_integral_value(rounding=ROUND_CEILING)))
    if box[2] <= box[0] or box[3] <= box[1]:
        raise ValueError("crop rectangle resolves to an empty pixel region")
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    out_w, out_h = box[2] - box[0], box[3] - box[1]
    stride = w * channels
    cropped = bytearray()
    for pixel_y in range(box[1], box[3]):
        start = pixel_y * stride + box[0] * channels
        cropped.extend(pixels[start:start + out_w * channels])
    _write_png(output, out_w, out_h, channels, bytes(cropped))
    output_hash = hashlib.sha256(output.read_bytes()).hexdigest()
    receipt = {
        "schema": "feltwillow.materialized-plate-crop.v1",
        "source_plate": source_label,
        "source_sha256": source_hash,
        "crop_rect_on_plate": [x, y, width, height],
        "pixel_box": list(box),
        "crop_px": [out_w, out_h],
        "resampling": "none; source pixels copied exactly",
        "sha256": output_hash,
    }
    output.with_suffix(output.suffix + ".json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plate", type=Path, required=True)
    parser.add_argument("--crop", nargs=4, type=float, required=True,
                        metavar=("X", "Y", "WIDTH", "HEIGHT"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    receipt = materialize(args.plate, args.crop, args.out)
    print(f"{args.out}: {receipt['sha256']} from {receipt['source_sha256']}")


if __name__ == "__main__":
    main()
