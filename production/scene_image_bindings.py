"""Apply exact technical current-bindings over historical owner selections.

The manifest is not an owner decision. Every entry must resolve to an existing
owner-feedback record with the identical image path, hash and accepted decision.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


SCHEMA = "feltwillow.scene-image-technical-bindings.v1"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_pointer(value, pointer: str):
    if pointer == "":
        return value
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {pointer}")
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def apply_current_bindings(folder: Path, records: list[dict]) -> list[dict]:
    """Replace historical selections for explicitly bound image IDs.

    Only manifests marked ``current`` are considered. Invalid references fail
    closed so a stale or edited authority record cannot silently change bytes.
    """

    folder = Path(folder).resolve()
    root = folder.parents[1]
    manifests = sorted(
        (folder / "review").glob("**/SCENE_IMAGE_BINDINGS.json")
    )
    technical = []
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text())
        if manifest.get("status") != "current":
            continue
        if manifest.get("schema") != SCHEMA:
            raise ValueError(f"{manifest_path}: unsupported binding schema")
        manifest_sha = digest(manifest_path)
        authority_cache = {}
        for index, binding in enumerate(manifest.get("bindings", [])):
            label = f"{manifest_path}:bindings[{index}]"
            image_id = binding.get("image_id")
            path = binding.get("path")
            sha256 = binding.get("sha256")
            if not all(isinstance(v, str) and v for v in (image_id, path, sha256)):
                raise ValueError(f"{label}: image_id/path/sha256 required")
            asset = (root / path).resolve()
            if not asset.is_relative_to(root) or not asset.is_file():
                raise ValueError(f"{label}: bound image unavailable")
            if digest(asset) != sha256:
                raise ValueError(f"{label}: bound image hash changed")

            authority = binding.get("owner_authority") or {}
            authority_path = authority.get("path")
            authority_sha = authority.get("sha256")
            pointer = authority.get("record_pointer")
            if not all(
                isinstance(v, str) and v
                for v in (authority_path, authority_sha, pointer)
            ):
                raise ValueError(f"{label}: complete owner authority required")
            source = (root / authority_path).resolve()
            if not source.is_relative_to(root) or not source.is_file():
                raise ValueError(f"{label}: owner authority unavailable")
            if digest(source) != authority_sha:
                raise ValueError(f"{label}: owner authority hash changed")
            if source not in authority_cache:
                authority_cache[source] = json.loads(source.read_text())
            row = json_pointer(authority_cache[source], pointer)
            path_field = authority.get("path_field", "path")
            sha_field = authority.get("sha256_field", "sha256")
            decision_field = authority.get("decision_field", "decision")
            if (
                row.get(path_field) != path
                or row.get(sha_field) != sha256
                or row.get(decision_field) != authority.get("decision")
            ):
                raise ValueError(f"{label}: owner authority contradicts binding")

            image_ids = [image_id] + list(binding.get("all_image_ids", []))
            for bound_id in image_ids:
                technical.append(
                    {
                        "image_id": bound_id,
                        "path": path,
                        "sha256": sha256,
                        "scope": "scene_depiction_only",
                        "owner_decision": authority["decision"],
                        "owner_authority": {
                            "path": authority_path,
                            "sha256": authority_sha,
                            "record_pointer": pointer,
                        },
                        "selection_record": {
                            "path": str(manifest_path.relative_to(root)),
                            "sha256": manifest_sha,
                        },
                    }
                )

    by_image = {}
    for record in technical:
        key = record["image_id"]
        value = (record["path"], record["sha256"])
        if key in by_image and by_image[key] != value:
            raise ValueError(f"{key}: conflicting current technical bindings")
        by_image[key] = value
    if not by_image:
        return records
    return [r for r in records if r.get("image_id") not in by_image] + technical
