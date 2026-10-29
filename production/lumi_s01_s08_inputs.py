"""Freeze and verify the S01-S08 still/audio input inventory for LUMI.

This is a transfer and planning inventory, never a render authorization.
"""

import argparse
import hashlib
import json
from pathlib import Path

from production.audio_visual_plan import local
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
    catalog = selection_catalog(story)
    by_id = {}
    for row in catalog:
        if row.get("image_id"):
            by_id.setdefault(row["image_id"], []).append(row)
    selected = {iid: rows[0] for iid, rows in by_id.items()
                if len({(r["path"], r["sha256"]) for r in rows}) == 1}
    conflicting = {iid for iid, rows in by_id.items()
                   if len({(r["path"], r["sha256"]) for r in rows}) > 1}
    authority = sorted(
        ({"image_id": r.get("image_id"), "path": r["path"],
          "sha256": r["sha256"], "selection_record": r.get("selection_record")}
         for r in catalog),
        key=lambda r: json.dumps(r, sort_keys=True),
    )
    selection_sha = hashlib.sha256(json.dumps(authority, sort_keys=True).encode()).hexdigest()
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
            target = local(root, path)
            if not target.is_file() or sha(target) != digest:
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
            direct = use.get("source")
            ref = direct or selected.get(use.get("image_id"))
            if ref:
                item["source"] = {"path": ref["path"], "sha256": ref["sha256"]}
                authorized = use.get("image_id") not in conflicting and (not direct or any(
                    row["path"] == ref["path"] and row["sha256"] == ref["sha256"]
                    and (not use.get("image_id") or row.get("image_id") == use["image_id"])
                    for row in catalog
                ))
                item["source_status"] = ("ambiguous_authority" if use.get("image_id") in conflicting
                                         else "selected_exact" if authorized else "explicit_source_unapproved")
                target = local(root, ref["path"])
                if not target.is_file() or sha(target) != ref["sha256"]:
                    raise ValueError(f"missing or changed selected still: {ref['path']}")
            elif use.get("alias_of"):
                item["source_status"] = "alias"
            else:
                item["source_status"] = "missing_or_unselected"
            uses.append(item)
        sequences[sid] = {"audio_line_ids": line_ids, "alias_of_sequence": seq.get("alias_of_sequence"),
                          "classification": {k: unit.get(k) for k in ("editorial_relationship", "composition", "mouth_policy", "visual_motion", "speaker")},
                          "uses": uses, "edges": seq.get("edges", [])}
    return {"schema": "feltwillow.lumi-s01-s08-inputs.v2", "story": "lion_and_mouse_v7",
            "source_plan_sha256": sha(plan_path), "source_authority": "audio_visual_plan.json + current exact-hash selection bindings",
            "source_selection_snapshot_sha256": selection_sha,
            "authorization": "inventory_only_no_gpu_authorization", "audio_lines": audio, "sequences": sequences}


def verify(root, data):
    failures = []
    root = root.resolve()
    if data.get("schema") != "feltwillow.lumi-s01-s08-inputs.v2":
        return ["inventory schema is stale; rebuild v2 from current authority"]
    plan = root / "stories/lion_and_mouse_v7/audio_visual_plan.json"
    if not plan.is_file() or sha(plan) != data.get("source_plan_sha256"):
        failures.append("source plan missing or changed")
    try:
        for line in data["audio_lines"].values():
            for path, digest in ((line["wav"], line["sha256"]), (line["metadata"], line["metadata_sha256"])):
                target = local(root, path)
                if not target.is_file() or sha(target) != digest:
                    failures.append(path)
        for seq in data["sequences"].values():
            for use in seq["uses"]:
                if use.get("source_status") in {"explicit_source_unapproved", "ambiguous_authority"}:
                    failures.append(f"{use.get('id')}: {use['source_status']}")
                ref = use.get("source")
                if ref:
                    target = local(root, ref["path"])
                    if not target.is_file() or sha(target) != ref["sha256"]:
                        failures.append(ref["path"])
        transfer = root / "stories/lion_and_mouse_v7/handoff/lumi_s01_s08/AUDIO_FILES.txt"
        expected = sorted(line["wav"] for line in data["audio_lines"].values())
        if not transfer.is_file() or transfer.read_text().splitlines() != expected:
            failures.append("AUDIO_FILES.txt differs from the ordered WAV inventory")
        current = build(root)
        if current != data:
            failures.append("inventory differs from current plan or owner selection authority")
    except (KeyError, TypeError, ValueError, OSError) as error:
        failures.append(str(error))
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
