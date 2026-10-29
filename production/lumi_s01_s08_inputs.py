"""Freeze and verify the S01-S08 still/audio input inventory for LUMI.

This is a transfer and planning inventory, never a render authorization.
"""

import argparse
import hashlib
import json
from pathlib import Path

from production.sequence_plan import selection_catalog


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build(root):
    root = root.resolve()
    story = root / "stories/lion_and_mouse_v7"
    plan_path = story / "audio_visual_plan.json"
    plan = json.loads(plan_path.read_text())
    selected = {r["image_id"]: r for r in selection_catalog(story) if r.get("image_id")}
    audio = {}
    for line in plan["lines"]:
        lid = line["line_id"]
        if lid[:3] not in {f"S{i:02d}" for i in range(1, 9)}:
            continue
        source = line["audio"]
        wav = source["wav"]
        metadata = source["metadata"]
        audio[lid] = {"speaker": line["speaker"], "text": line["text"],
                      "wav": wav, "sha256": source["sha256"],
                      "metadata": metadata, "metadata_sha256": source["metadata_sha256"],
                      "sample_count": source["sample_count"],
                      "sample_rate_hz": source["sample_rate_hz"]}
        for path, digest in ((wav, source["sha256"]), (metadata, source["metadata_sha256"])):
            if not (root / path).is_file() or sha(root / path) != digest:
                raise ValueError(f"missing or changed audio input: {path}")
    sequences = {}
    for sid, seq in plan["production_sequences"].items():
        unit = plan.get("visual_units", {}).get(sid, {})
        line_ids = unit.get("audio_line_ids", [])
        if not line_ids or not all(lid in audio for lid in line_ids):
            continue
        uses = []
        for use in seq.get("uses", []):
            item = {k: use[k] for k in ("id", "image_id", "alias_of", "hold", "required_phase", "visible_cast") if k in use}
            ref = use.get("source") or selected.get(use.get("image_id"))
            if ref:
                item["source"] = {"path": ref["path"], "sha256": ref["sha256"]}
                item["source_status"] = "selected_exact"
                if not (root / ref["path"]).is_file() or sha(root / ref["path"]) != ref["sha256"]:
                    raise ValueError(f"missing or changed selected still: {ref['path']}")
            elif use.get("alias_of"):
                item["source_status"] = "alias"
            else:
                item["source_status"] = "missing_or_unselected"
            uses.append(item)
        sequences[sid] = {"audio_line_ids": line_ids, "alias_of_sequence": seq.get("alias_of_sequence"),
                          "classification": {k: unit.get(k) for k in ("editorial_relationship", "composition", "mouth_policy", "visual_motion", "speaker")},
                          "uses": uses, "edges": seq.get("edges", [])}
    return {"schema": "feltwillow.lumi-s01-s08-inputs.v1", "story": "lion_and_mouse_v7",
            "source_plan_sha256": sha(plan_path), "source_authority": "audio_visual_plan.json + current exact-hash selection bindings",
            "authorization": "inventory_only_no_gpu_authorization", "audio_lines": audio, "sequences": sequences}


def verify(root, data):
    failures = []
    root = root.resolve()
    plan = root / "stories/lion_and_mouse_v7/audio_visual_plan.json"
    if not plan.is_file() or sha(plan) != data["source_plan_sha256"]:
        failures.append("source plan missing or changed")
    for line in data["audio_lines"].values():
        for path, digest in ((line["wav"], line["sha256"]), (line["metadata"], line["metadata_sha256"])):
            if not (root / path).is_file() or sha(root / path) != digest:
                failures.append(path)
    for seq in data["sequences"].values():
        for use in seq["uses"]:
            ref = use.get("source")
            if ref and (not (root / ref["path"]).is_file() or sha(root / ref["path"]) != ref["sha256"]):
                failures.append(ref["path"])
    return sorted(set(failures))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--out", type=Path)
    p.add_argument("--verify", type=Path)
    a = p.parse_args()
    if a.verify:
        data = json.loads(a.verify.read_text())
        missing = verify(a.repo, data)
        print(json.dumps({"status": "PASS" if not missing else "BLOCKED", "missing_or_changed": missing}, indent=2))
        raise SystemExit(bool(missing))
    if not a.out:
        p.error("--out is required unless --verify is used")
    data = build(a.repo)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(data, indent=2) + "\n")
    print(f"wrote {len(data['sequences'])} sequences and {len(data['audio_lines'])} line WAVs to {a.out}")


if __name__ == "__main__":
    main()
