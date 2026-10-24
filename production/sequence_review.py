"""Render an offline sequence board with source/fitted inputs and explicit gates."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import argparse, html, json, os
from pathlib import Path
from production.sequence_readiness import evaluate
from production.sequence_plan import local, digest
from feltwillow import wan
from PIL import Image


def build(packet, root, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    h = html.escape
    cards = []
    for n, u in enumerate(packet["resolved_images"]):
        media = ""
        source = u.get("source")
        if source and local(root, source["path"]).is_file():
            p = local(root, source["path"])
            url = os.path.relpath(p, out)
            if digest(p) != source["sha256"]:
                raise ValueError("board source hash changed")
            media = f'<a href="{h(url)}"><img src="{h(url)}" alt="native source"></a>'
            if not u.get("fit"):
                media += "<p>No model-fit preview: input is incompatible or unverified. See blockers.</p>"
            else:
                try:
                    with Image.open(p) as im:
                        if wan.fitted_record(im, *packet["size"]) != u["fit"]:
                            raise ValueError(
                                "model fit changed; refresh realization before review"
                            )
                        fit = wan.fit(im, *packet["size"])
                        fitp = out / f"fit_{n:03d}.png"
                        fit.save(fitp)
                    media += f'<img src="{fitp.name}" alt="actual model fit">'
                except OSError:
                    media += "<p>Image decode unavailable</p>"
        cards.append(
            f"<article><h2>{h(u['id'])}</h2><p>{h(u['status'])}</p>{media}<pre>{h(json.dumps(u, indent=2))}</pre></article>"
        )
    edges = "<pre>" + h(json.dumps(packet["edges"], indent=2)) + "</pre>"
    ready = evaluate(packet)
    audio = []
    for line in packet.get("audio_lines", []):
        if not line.get("wav"):
            continue
        source = local(root, line["wav"])
        if source.is_file() and digest(source) == line["sha256"]:
            audio.append(
                "<p>"
                + h(line["line_id"] + " · " + line["speaker"] + " · " + line["text"])
                + '</p><audio controls preload="none" src="'
                + h(os.path.relpath(source, out))
                + '"></audio>'
            )
        else:
            audio.append(
                "<p>" + h(line["line_id"]) + ": audio unavailable or changed</p>"
            )
    outputs = []
    work_root = (Path(root).resolve().parent / "work").resolve()
    for take in packet.get("rendered_outputs", []):
        source = Path(take["path"]).resolve()
        if not source.is_relative_to(work_root):
            raise ValueError("review video escapes configured parent work root")
        if not source.is_file() or digest(source) != take["sha256"]:
            raise ValueError("review video missing or changed")
        outputs.append(
            "<article><h2>"
            + h(take["piece"])
            + '</h2><video controls preload="metadata" style="max-width:100%" src="'
            + h("/__sequence_work__/" + source.relative_to(work_root).as_posix())
            + '"></video><pre>'
            + h(json.dumps(take, indent=2))
            + "</pre><p>Watch the entire clip and joins at normal/reduced speed. Player availability is not a motion pass.</p></article>"
        )
    page = (
        '<!doctype html><meta charset="utf-8"><title>Sequence evidence</title><style>body{font:16px system-ui;background:#252821;color:#eee;margin:24px}article{margin:20px 0;padding:16px;background:#343a31}img{max-width:48%;height:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere}a{color:#bde2a8}</style><h1>'
        + h(packet["sequence_id"])
        + "</h1><p>Owner selection, technical readiness, submission authority and take review are separate. This board does not approve media.</p><pre>"
        + h(json.dumps(ready, indent=2))
        + "</pre>"
        + "".join(cards)
        + "<h2>Edges / cuts / prompts</h2>"
        + edges
        + "<h2>Timing / capability</h2><pre>"
        + h(json.dumps({k: packet.get(k) for k in ["timing", "capability"]}, indent=2))
        + "</pre>"
    )
    page += (
        "<h2>Associated audio (phrase alignment pending unless evidenced)</h2>"
        + "".join(audio)
        + "<h2>Full motion / joins</h2>"
        + (
            "".join(outputs)
            if outputs
            else "<p>No new rendered outputs. Motion and join review pending.</p>"
        )
    )
    (out / "review.html").write_text(page)
    return out / "review.html"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("packet", type=Path)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    print(build(json.loads(a.packet.read_text()), a.root, a.out))


def protected_pixels(base, candidate, allowed_mask):
    """Exact still preservation measurement, independent of visual integration."""
    import numpy as np

    with (
        Image.open(base) as a,
        Image.open(candidate) as b,
        Image.open(allowed_mask) as m,
    ):
        if a.size != b.size or a.size != m.size:
            raise ValueError("protected comparison requires identical native canvases")
        aa = np.asarray(a.convert("RGB"))
        bb = np.asarray(b.convert("RGB"))
        allowed = np.asarray(m.convert("L")) > 0
        differences = np.any(aa != bb, axis=2) & ~allowed
        return {
            "base_sha256": digest(base),
            "candidate_sha256": digest(candidate),
            "mask_sha256": digest(allowed_mask),
            "mask_policy": "nonzero permits change",
            "compared_pixels": int((~allowed).sum()),
            "changed_protected_pixels": int(differences.sum()),
            "status": "pass" if not differences.any() else "fail",
            "integration_review": "pending; equality cannot prove anatomy/contact/light",
        }


if __name__ == "__main__":
    main()
