"""Freeze endpoint-chain runtimes and exact one-seed commands; never submit jobs."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import argparse, json, os, re, sys, tempfile
from pathlib import Path
import yaml
from production.sequence_plan import digest, fingerprint, local, frame_accounting
from production.sequence_readiness import evaluate
from feltwillow import wan


def atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError("nonidentical immutable destination: " + str(path))
        return
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".sequence-")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        # Link without overwriting a concurrent destination.
        os.link(tmp, path)
    finally:
        Path(tmp).unlink(missing_ok=True)


def compile_packet(
    packet, root, out, run_id, recipe, executable=sys.executable, mode="diagnostic"
):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", run_id):
        raise ValueError("invalid run ID")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", packet["sequence_id"]):
        raise ValueError("invalid sequence ID")
    ready = evaluate(packet, "execution", mode)
    if not ready["technical_render_ready"]:
        raise ValueError("sequence blocked: " + "; ".join(ready["blockers"]))
    unknown = set(recipe) - {
        "width",
        "height",
        "frames",
        "steps",
        "guidance",
        "guidance_2",
        "preset",
        "seed",
    }
    if unknown:
        raise ValueError("unsupported recipe fields: " + str(sorted(unknown)))
    if recipe["preset"] not in {"fast", "normal"}:
        raise ValueError("unsupported preset")
    if (
        isinstance(recipe["seed"], bool)
        or not isinstance(recipe["seed"], int)
        or recipe["seed"] < 0
        or recipe["seed"] > 2**64 - 1
    ):
        raise ValueError("invalid seed")
    wan.preflight(
        **{
            k: recipe[k]
            for k in ["width", "height", "frames", "steps", "guidance", "guidance_2"]
        },
        max_frames=81,
    )
    if (recipe["guidance"] > 1) != (recipe["guidance_2"] > 1):
        raise ValueError(
            "mixed CFG activation requires a separately verified endpoint recipe"
        )
    if recipe["frames"] < 5:
        raise ValueError("endpoint pieces require at least five frames")
    if packet["size"] != [recipe["width"], recipe["height"]]:
        raise ValueError("recipe size differs from reviewed fit")
    if recipe["preset"] == "fast" and any(
        recipe[k] != wan.LIGHTNING["render"][k]
        for k in ["steps", "guidance", "guidance_2"]
    ):
        raise ValueError("fast recipe differs from supported Lightning preset")
    timeline = frame_accounting(
        packet["timing"]["intervals"], packet["timing"]["sample_rate"]
    )
    root = Path(root).resolve()
    authored = root / "stories" / packet["story"] / "audio_visual_plan.json"
    if (
        authored.is_file()
        and fingerprint(json.loads(authored.read_text()))
        != packet["source_plan_sha256"]
    ):
        raise ValueError("authored plan changed; refresh scoped realization/evidence")
    out = Path(out).resolve()
    resolved = {u["id"]: u for u in packet["resolved_images"]}
    shots = []
    pieces = []
    commands = []
    for n, edge in enumerate(packet["edges"]):
        if edge["kind"] == "cut":
            continue
        a, b = [resolved[edge[k]] for k in ["from", "to"]]
        for u in [a, b]:
            source = local(root, u["source"]["path"])
            if digest(source) != u["source"]["sha256"]:
                raise ValueError("source bytes changed after review")
            from PIL import Image

            with Image.open(source) as im:
                fit = wan.fitted_record(im, recipe["width"], recipe["height"])
            if fit != u["fit"]:
                raise ValueError("fitted input changed after review")
        name = f"{packet['sequence_id']}_p{n:03d}"
        prompt = edge.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("complete per-piece prompt required")
        cast = a.get("visible_cast")
        if cast == [] and any(
            word in prompt.lower()
            for word in ["milo", "cream patch", "orange tail", "body proportions"]
        ):
            raise ValueError("empty-cast prompt contains character boilerplate")
        shot = {
            "name": name,
            "keyframe": str(local(root, a["source"]["path"])),
            "end_keyframe": str(local(root, b["source"]["path"])),
            "keyframe_sha256": a["source"]["sha256"],
            "end_keyframe_sha256": b["source"]["sha256"],
            "frames": recipe["frames"],
            "seeds": [recipe["seed"]],
            "prompt": prompt,
            "negative": edge.get("negative", ""),
            "render": {
                k: recipe[k]
                for k in [
                    "width",
                    "height",
                    "steps",
                    "guidance",
                    "guidance_2",
                    "preset",
                ]
            },
            "sequence_dependency_sha256": packet["dependency_sha256"],
            "alignment_sha256": fingerprint(packet["timing"]),
            "edge_sha256": fingerprint(edge),
            "source_key_order": [a["id"], b["id"]],
        }
        shots.append(shot)
        pieces.append(
            {
                "id": name,
                "edge": edge,
                "start": a["id"],
                "end": b["id"],
                "frames": recipe["frames"],
                "fps": 16,
                "sample_span": {"numerator": recipe["frames"] - 1, "denominator": 16},
                "encoded_duration": {"numerator": recipe["frames"], "denominator": 16},
                "timing_scope": mode,
                "boundary_motion_review": "pending rendered frames; matching source endpoints is insufficient",
            }
        )
    if mode == "production":
        allocations = packet["timing"].get("render_allocations", {})
        if set(allocations) != {p["id"] for p in pieces}:
            raise ValueError(
                "production requires an explicit frame/sample allocation for every piece"
            )
        for piece in pieces:
            allocation = allocations[piece["id"]]
            if (
                allocation.get("frames") != recipe["frames"]
                or allocation.get("fps") != 16
                or not allocation.get("reviewed")
            ):
                raise ValueError("unsupported or unreviewed production retiming")
            if allocation.get("join_policy") != "keep_all":
                raise ValueError(
                    "boundary deletion requires actual rendered join review"
                )
            slot = next(
                (v for v in timeline["intervals"] if v["id"] == piece["id"]), None
            )
            if slot is None or slot["frame_cells"] != recipe["frames"]:
                raise ValueError(
                    "production allocation would require undeclared trimming/retiming"
                )
            piece["editorial_allocation"] = allocation
    if not shots:
        raise ValueError("no render pieces; cuts-only packet needs explicit holds")
    runtime = {
        "schema": "feltwillow.sequence-runtime.v1",
        "endpoint_capability": packet["capability"],
        "implementation_sha256": {
            name: digest(root / name)
            for name in (
                "production/shot.py",
                "feltwillow/wan.py",
                "feltwillow/render_receipt.py",
            )
            if (root / name).is_file()
        },
        "run_id": run_id,
        "story": packet["story"],
        "sequence_dependency_sha256": packet["dependency_sha256"],
        "negative": "",
        "characters": {},
        "initial_operation_states": {
            f"{run_id}:{s['name']}:s{recipe['seed']}": "not_submitted" for s in shots
        },
        "scenes": {1: {"shots": shots}},
    }
    runtime_path = out / "runtime.yaml"
    runtime_bytes = yaml.safe_dump(runtime, sort_keys=False).encode()
    runtime_hash = __import__("hashlib").sha256(runtime_bytes).hexdigest()
    for s in shots:
        argv = [
            str(executable),
            str(root / "production/shot.py"),
            "--story",
            packet["story"],
            "--scene",
            "1",
            "--shot",
            s["name"],
            "--runtime",
            str(runtime_path),
            "--run-id",
            run_id,
            "--runtime-sha256",
            runtime_hash,
            "--seed",
            str(recipe["seed"]),
        ]
        commands.append(
            {
                "operation_id": f"{run_id}:{s['name']}:s{recipe['seed']}",
                "argv": argv,
                "runtime_sha256": runtime_hash,
                "run_id": run_id,
                "model_invocations": 1,
                "state": "not_submitted",
                "authorization": None,
                "maximum_retries": 0,
                "submission_authorized": False,
            }
        )
    # All validation precedes freezing. Multi-file commit marker is written last.
    manifest = {
        "schema": "feltwillow.sequence-packet.v1",
        "story": packet["story"],
        "run_id": run_id,
        "mode": mode,
        "runtime": {"path": str(runtime_path), "sha256": runtime_hash},
        "source_packet_sha256": fingerprint(packet),
        "sequence_dependency_sha256": packet["dependency_sha256"],
        "capability": packet["capability"],
        "timing": packet["timing"],
        "recipe": recipe,
        "frame_timeline": timeline,
        "render_pieces": pieces,
        "commands": commands,
        "technical_render_ready": True,
        "submission_authorized": False,
        "model_invocations": len(commands),
        "retry_limit": 0,
        "assembly_authorized": False,
    }
    atomic(runtime_path, runtime_bytes)
    atomic(out / "commands.json", (json.dumps(commands, indent=2) + "\n").encode())
    atomic(out / "realization.json", (json.dumps(packet, indent=2) + "\n").encode())
    atomic(out / "packet.json", (json.dumps(manifest, indent=2) + "\n").encode())
    return manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("packet", type=Path)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--recipe", type=Path, required=True)
    p.add_argument("--mode", choices=["diagnostic", "production"], default="diagnostic")
    a = p.parse_args()
    result = compile_packet(
        json.loads(a.packet.read_text()),
        a.root,
        a.out,
        a.run_id,
        json.loads(a.recipe.read_text()),
        mode=a.mode,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
