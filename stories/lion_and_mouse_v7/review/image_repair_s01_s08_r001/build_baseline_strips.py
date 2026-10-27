"""CPU-only contact sheets for existing, immutable historical pilot videos."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
from PIL import Image, ImageDraw


OUT = Path(__file__).resolve().parent
WORK = Path("/Users/lealroja/Documents/feltwillow/work/stories/lion_and_mouse_v7/shots")
NAMES = (
    "s01_l004_b03_i03_s1_fast",
    "s02_l001_b01_i02_s1_fast",
    "s02_l003_b01_i01_s1_fast",
)


def main() -> None:
    report = {"scope": "existing pilot contact sheets; no new render or quality pass", "videos": []}
    for name in NAMES:
        source = WORK / f"{name}.mp4"
        if not source.is_file():
            report["videos"].append({"name": name, "status": "unavailable", "path": str(source)})
            continue
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        cap = cv2.VideoCapture(str(source))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = []
        while True:
            ok, bgr = cap.read()
            if not ok:
                break
            frames.append(Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)))
        cap.release()
        if not frames:
            report["videos"].append({"name": name, "status": "decode_failed", "sha256": digest})
            continue
        tile_w = 320
        tile_h = round(frames[0].height * tile_w / frames[0].width)
        label_h = 26
        cols = 8
        rows = (len(frames) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tile_w, rows * (tile_h + label_h)), "#161616")
        draw = ImageDraw.Draw(sheet)
        for i, frame in enumerate(frames):
            col, row = i % cols, i // cols
            x, y = col * tile_w, row * (tile_h + label_h)
            sheet.paste(frame.resize((tile_w, tile_h), Image.Resampling.LANCZOS), (x, y + label_h))
            draw.text((x + 6, y + 5), f"frame {i:02d} · {i / fps:.3f}s", fill="white")
        target = OUT / f"{name}_all_frames.jpg"
        sheet.save(target, quality=91)
        for frame_index in ({5, 74} if name != "s02_l001_b01_i02_s1_fast" else {0, 40, 80}):
            if frame_index < len(frames):
                frames[frame_index].save(OUT / f"{name}_frame_{frame_index:02d}.jpg", quality=96)
        report["videos"].append(
            {
                "name": name,
                "status": "decoded",
                "path": str(source),
                "sha256": digest,
                "fps": fps,
                "frame_count": len(frames),
                "frame_size": list(frames[0].size),
                "sheet": target.name,
                "sheet_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            }
        )
    (OUT / "BASELINE_STRIPS.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
