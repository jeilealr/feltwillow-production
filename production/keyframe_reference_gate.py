#!/usr/bin/env python3
"""Validate portable source authorities for future keyframe regeneration.

This gate checks metadata and byte hashes. It cannot certify visual approval.
Run with ``--write-contract`` after changing staging to refresh the proposed
regeneration contract, then resolve every blocker before generating images.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

try:
    from . import keyframe_plan
except ImportError:  # pragma: no cover - script entry point
    import keyframe_plan

REPO = Path(__file__).resolve().parents[1]
SCHEMA = "feltwillow.keyframe-regeneration-contract.v1"
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
HEIGHT_RE = re.compile(
    r"(?:standing-equivalent anatomical height target|(?:whole[- ]character )?height target)\s*"
    r"(?:=|of)?\s*(\d+(?:\.\d+)?)\s*%", re.IGNORECASE)
POSITIVE_MANE_RE = re.compile(
    r"(?:\bmilo(?:'s|’s)\s+(?:full\s+|curly\s+|tawny\s+|golden\s+|brown\s+)?mane\b)"
    r"|(?:\bmilo\s+(?:has|with)\b[^.!?]{0,50}\bmane\b)"
    r"|(?:\b(?:full|curly|tawny|golden|brown)\s+mane\b[^.!?]{0,50}\bmilo\b)",
    re.IGNORECASE)
OPEN_MOUTH_RE = re.compile(r"\b(?:open|opening)\s+(?:the\s+)?mouth\b|\bspeaking mouth\b",
                           re.IGNORECASE)
CAST_RATIO_RE = re.compile(
    r"At equal depth and camera Milo's upright ear-to-foot standing-equivalent height is "
    r"about\s+(\d+(?:\.\d+)?)%\s+of Leo's quadrupedal mane-top-to-supporting-front-paw height",
    re.IGNORECASE)


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_repo_path(root: Path, value: str) -> Path | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("", ".", "..") for part in value.split("/")):
        return None
    resolved = (root / Path(*path.parts)).resolve()
    if not resolved.is_relative_to(root.resolve()):
        return None
    return resolved


@lru_cache(maxsize=8)
def _latest_commit_by_path(root_label: str) -> dict[str, str]:
    root = Path(root_label)
    result = subprocess.run(
        ["git", "log", "--all", "--format=__FELTWILLOW_COMMIT__%H", "--name-only",
         "--diff-filter=AM"], cwd=root, capture_output=True, text=True, check=False)
    if result.returncode:
        return {}
    latest: dict[str, str] = {}
    commit = None
    for line in result.stdout.splitlines():
        if line.startswith("__FELTWILLOW_COMMIT__"):
            commit = line.removeprefix("__FELTWILLOW_COMMIT__")
        elif commit and line:
            latest.setdefault(line, commit)
    return latest


@lru_cache(maxsize=8)
def _tree_blobs(root_label: str, commit: str) -> dict[str, str]:
    result = subprocess.run(["git", "ls-tree", "-r", "-z", commit], cwd=root_label,
                            capture_output=True, check=False)
    if result.returncode:
        return {}
    blobs = {}
    for entry in result.stdout.split(b"\0"):
        if not entry or b"\t" not in entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split(b" ", 2)
        if kind == b"blob":
            blobs[raw_path.decode("utf-8", errors="surrogateescape")] = oid.decode("ascii")
    return blobs


def _git_blob_oid(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def git_locator(root: Path, relative: str) -> dict | None:
    """Return a recoverable commit/path/blob locator for a tracked file."""
    if not relative or relative.startswith("/") or "\\" in relative:
        return None
    root = Path(root).resolve()
    root_label = str(root)
    commit = _latest_commit_by_path(root_label).get(relative)
    if not commit:
        return None
    blob_id = _tree_blobs(root_label, commit).get(relative)
    if not blob_id:
        return None
    local = _safe_repo_path(root, relative)
    data = local.read_bytes() if local and local.is_file() else None
    if data is None or _git_blob_oid(data) != blob_id:
        contents = subprocess.run(["git", "show", f"{commit}:{relative}"], cwd=root,
                                  capture_output=True, check=False)
        if contents.returncode:
            return None
        data = contents.stdout
    return {"commit": commit, "path": relative, "blob": blob_id,
            "sha256": hashlib.sha256(data).hexdigest()}


def _legacy_provenance(root: Path, row: dict) -> list[dict]:
    result = []
    refs = row.get("historical_candidate_references", [])
    input_metadata = {item.get("path"): item
                      for item in row.get("historical_candidate_inputs", [])
                      if isinstance(item, dict) and item.get("path")}
    for reference in refs:
        metadata = input_metadata.get(reference, {})
        role = metadata.get("role", "historical_generation_input")
        if isinstance(reference, str) and reference.startswith("/"):
            cache = Path(reference)
            item = {"path": None, "source_label": cache.name,
                    "role": role, "regeneration_allowed": False}
            if role == "owner_correction_target":
                item.update(owner_directed_correction=metadata.get("owner_directed_correction"),
                            authority_scope=metadata.get("authority_scope"))
            if cache.is_file():
                item.update(sha256=_hash(cache), status="external_cache_only")
            else:
                item.update(status="external_source_unavailable", sha256=None)
            result.append(item)
            continue
        item = {"path": reference, "role": role,
                "regeneration_allowed": False}
        if role == "owner_correction_target":
            item.update(owner_directed_correction=metadata.get("owner_directed_correction"),
                        authority_scope=metadata.get("authority_scope"))
        local = _safe_repo_path(root, reference)
        if local and local.is_file():
            item["sha256"] = _hash(local)
            item["status"] = "recoverable_in_checkout"
            locator = git_locator(root, reference)
            if locator and locator["sha256"] == item["sha256"]:
                item["git_locator"] = locator
        else:
            locator = git_locator(root, reference)
            if locator:
                item.update(sha256=locator["sha256"], git_locator=locator,
                            status="recoverable_from_git")
            elif reference.startswith("work/") and row.get("approved_plate"):
                item.update(status="legacy_crop_rebuild_required",
                            source_plate=row["approved_plate"],
                            crop_rect_on_plate=row.get("crop_rect_on_plate"),
                            materializer="normalized_crop.v1")
            else:
                item.update(status="legacy_source_unavailable", sha256=None,
                            git_locator=None)
        result.append(item)
    return result


def _recorded_revisions(root: Path, row: dict) -> list[dict]:
    revisions = [{"candidate_path": row.get("candidate_path"),
                  "sha256": row.get("sha256"),
                  "prompt": row.get("historical_candidate_prompt"),
                  "state": "active_candidate"}]
    revisions.extend({**revision, "state": "superseded_candidate"}
                     for revision in row.get("superseded", []))
    revisions.extend({**revision, "state": "unavailable_recorded_revision"}
                     for revision in row.get("generation_history", []))
    for revision in revisions:
        if revision.get("state") == "unavailable_recorded_revision" and revision.get("status") == "declared_bytes_not_found_reverted_to_recoverable_prior_candidate":
            revision["status"] = "declared_bytes_not_found_reverted_to_prior_candidate"
            revision["git_locator"] = None
            continue
        candidate_path = revision.get("candidate_path")
        if candidate_path:
            local = _safe_repo_path(root, candidate_path)
            if local and local.is_file():
                actual = _hash(local)
                if revision.get("sha256") == actual:
                    revision["status"] = "recoverable_in_checkout"
                    locator = revision.get("git_locator") or git_locator(root, candidate_path)
                    if locator and locator.get("sha256") == actual:
                        revision["git_locator"] = locator
                    else:
                        revision["status"] = "checkout_only_without_git_locator"
                    continue
        locator = revision.get("git_locator") or (git_locator(root, candidate_path)
                   if isinstance(candidate_path, str) and not candidate_path.startswith("/") else None)
        if locator and locator.get("sha256") == revision.get("sha256"):
            revision["git_locator"] = locator
            revision["status"] = "recoverable_from_git"
        else:
            revision["git_locator"] = None
            revision["status"] = "unrecoverable_recorded_revision"
    return revisions


def build_contract(story: str, root: Path = REPO,
                   active_plan: dict | None = None) -> dict:
    root = Path(root).resolve()
    story_dir = root / "stories" / story
    staging = json.loads((story_dir / "staging_plan.json").read_text())
    bible = json.loads((story_dir / "visual_bible.json").read_text())
    active = active_plan or json.loads((story_dir / "keyframe_plan.json").read_text())
    fresh = keyframe_plan.build(story, root=root)
    active_by_id = {row["id"]: row for row in active["images"]}
    staged_by_id = {row["id"]: row for row in staging["frames"]}
    records = []
    for planned in fresh["images"]:
        fid = planned["id"]
        frame = staged_by_id[fid]
        plate = frame["plate"]
        plate_path = _safe_repo_path(root, plate)
        if plate_path is None or not plate_path.is_file():
            plate_hash = None
        else:
            plate_hash = _hash(plate_path)
        inputs = [{"role": "approved_plate", "path": plate, "sha256": plate_hash,
                   "required": True, "crop_rect_on_plate": planned["crop_rect_on_plate"],
                   "materializer": "normalized_crop.v1", "canvas_px": [1920, 1080]}]
        foundations = {}
        for actor in sorted(frame["actors"]):
            path = bible["characters"][actor]["canonical"]
            local = _safe_repo_path(root, path)
            digest = _hash(local) if local and local.is_file() else None
            approval = bible.get("character_foundation_approval", {})
            if actor == "milo":
                approval_status = approval.get("milo_body_revision_status", "pending_owner_hash_bound_review")
            else:
                approval_status = "approved_canonical"
            inputs.append({"role": "identity_root", "actor": actor, "path": path,
                           "sha256": digest, "required": True,
                           "approval_status": approval_status})
            foundations[actor] = {"canonical_path": path, "sha256": digest,
                                  "approval_status": approval_status}
        anchor_id = frame.get("size_anchor_id")
        anchor = staging.get("setup_anchors", {}).get(anchor_id, {})
        if (anchor.get("status") == "approved_owner_hash_bound" and anchor.get("image_path") and
                anchor.get("sha256")):
            inputs.append({"role": "size_anchor", "id": anchor_id,
                           "path": anchor["image_path"], "sha256": anchor["sha256"],
                           "required": True})
        for ref in planned.get("reference_roles", []):
            if ref.get("role") in ("prop", "pose"):
                inputs.append({key: value for key, value in ref.items()
                               if key in ("role", "actor", "path", "sha256", "required", "id")})
        history = _legacy_provenance(root, active_by_id.get(fid, {}))
        revisions = _recorded_revisions(root, active_by_id.get(fid, {}))
        records.append({
            "id": fid,
            "actors": sorted(frame["actors"]),
            "location": frame["location"],
            "camera_family": f"{frame['location']}:{frame['view']}",
            "view": frame["view"],
            "crop_rect_on_plate": planned["crop_rect_on_plate"],
            "staging_signature": {name: {"contact_xy_on_plate": actor["contact_xy_on_plate"],
                                           "depth_t": actor["depth_t"],
                                           "standing_equivalent_height_fraction_after_crop": actor["standing_equivalent_height_fraction_after_crop"]}
                                  for name, actor in sorted(frame["actors"].items())},
            "size_anchor": {"id": anchor_id, "status": anchor.get("status"),
                            "path": anchor.get("image_path"), "sha256": anchor.get("sha256")},
            "foundation_authorities": foundations,
            "regeneration_inputs": inputs,
            "required_props": planned.get("required_props", []),
            "mouth_policy": planned["mouth_policy"],
            "prompt": planned["prompt"],
            "active_candidate": {"path": active_by_id[fid].get("candidate_path"),
                                 "sha256": active_by_id[fid].get("sha256")},
            "generation_history": {
                "candidate_path": active_by_id[fid].get("candidate_path"),
                "candidate_sha256": active_by_id[fid].get("sha256"),
                "historical_prompt": active_by_id[fid].get("historical_candidate_prompt"),
                "historical_inputs": history,
                "recorded_revisions": revisions,
                "history_status": ("recoverable" if all(x.get("sha256") and
                                     (x.get("git_locator") or x.get("status") == "recoverable_in_checkout" or
                                      x.get("status") == "legacy_crop_rebuild_required") for x in history)
                                   else "incomplete_legacy_provenance")},
        })
    return {"schema": SCHEMA, "story": story, "status": "regeneration_contract_pending_review",
            "materializer": "production/materialize_plate_crop.py",
            "images": records}


def _input_by_role(inputs: list[dict], role: str, actor: str | None = None) -> list[dict]:
    return [item for item in inputs if item.get("role") == role and
            (actor is None or item.get("actor") == actor)]


def prompt_errors(prompt: str, actors: list[str], mouth_policy: str,
                  expected_cast_ratio: float | None = None) -> list[str]:
    errors = []
    if "milo" in actors and POSITIVE_MANE_RE.search(prompt):
        errors.append("Milo prompt positively requests a mane")
    if mouth_policy == "closed_boundary_for_lipsync" and OPEN_MOUTH_RE.search(prompt):
        errors.append("closed production boundary prompt requests an open mouth")
    targets = HEIGHT_RE.findall(prompt)
    if len(targets) != len(actors):
        errors.append(f"expected one standing-equivalent height target per visible actor; found {len(targets)}")
    if expected_cast_ratio is not None and set(actors) == {"leo", "milo"}:
        ratios = CAST_RATIO_RE.findall(prompt)
        if (len(ratios) != 1 or
                abs(float(ratios[0]) / 100 - expected_cast_ratio) > 0.005):
            errors.append("same-depth Milo/Leo ratio must match the current visual_bible.json authority")
    return errors


def _git_locator_resolves(root: Path, locator: dict, expected_sha: str) -> bool:
    commit, relative = locator.get("commit"), locator.get("path")
    if not commit or not relative:
        return False
    root = Path(root).resolve()
    blob_id = _tree_blobs(str(root), commit).get(relative)
    if not blob_id or blob_id != locator.get("blob"):
        return False
    local = _safe_repo_path(root, relative)
    data = local.read_bytes() if local and local.is_file() else None
    if data is None or _git_blob_oid(data) != blob_id:
        contents = subprocess.run(["git", "show", f"{commit}:{relative}"], cwd=root,
                                  capture_output=True, check=False)
        if contents.returncode:
            return False
        data = contents.stdout
    return hashlib.sha256(data).hexdigest() == expected_sha == locator.get("sha256")


def validate_contract(contract: dict, root: Path = REPO,
                      staging: dict | None = None, bible: dict | None = None,
                      active_plan: dict | None = None,
                      historical_warnings: list[str] | None = None) -> list[str]:
    root = Path(root).resolve()
    errors: list[str] = []
    warnings = historical_warnings if historical_warnings is not None else []
    if contract.get("schema") != SCHEMA:
        errors.append("reference contract has missing or unsupported schema")
    story = contract.get("story")
    if not story or not isinstance(contract.get("images"), list):
        return errors + ["reference contract needs story and images"]
    story_dir = root / "stories" / story
    if staging is None:
        path = story_dir / "staging_plan.json"
        staging = json.loads(path.read_text()) if path.is_file() else {}
    if bible is None:
        path = story_dir / "visual_bible.json"
        bible = json.loads(path.read_text()) if path.is_file() else {}
    if active_plan is None:
        path = story_dir / "keyframe_plan.json"
        active_plan = json.loads(path.read_text()) if path.is_file() else {}
    anchors = staging.get("setup_anchors", {})
    frames = {item.get("id"): item for item in staging.get("frames", [])}
    plan_rows = {item.get("id"): item for item in active_plan.get("images", [])}
    fresh_rows = None
    if ((story_dir / "scene_plan.json").is_file() and
            (story_dir / "visual_sequence_plan.json").is_file()):
        fresh_rows = {item["id"]: item for item in keyframe_plan.build(story, root=root)["images"]}
    ids: set[str] = set()
    for row in contract["images"]:
        fid = row.get("id")
        if not fid or fid in ids:
            errors.append(f"duplicate or missing contract frame id: {fid}")
            continue
        ids.add(fid)
        frame = frames.get(fid)
        if frame is None:
            errors.append(f"{fid}: no matching staging frame")
            continue
        actors = set(row.get("actors", []))
        if actors != set(frame.get("actors", {})):
            errors.append(f"{fid}: contract actors differ from staging")
        expected_camera = f"{frame.get('location')}:{frame.get('view')}"
        if row.get("camera_family") != expected_camera or row.get("view") != frame.get("view"):
            errors.append(f"{fid}: contract camera family/view differs from staging")
        expected_crop = keyframe_plan.crop_for_frame(
            frame, staging.get("views", {}).get(frame.get("view"), {}).get("magnification", 0))
        if row.get("crop_rect_on_plate") != expected_crop:
            errors.append(f"{fid}: contract crop differs from current registered staging")
        if fresh_rows is not None:
            fresh = fresh_rows.get(fid, {})
            for field in ("prompt", "mouth_policy", "required_props"):
                if row.get(field) != fresh.get(field):
                    errors.append(f"{fid}: regeneration contract {field} is stale")
        inputs = row.get("regeneration_inputs", [])
        plates = _input_by_role(inputs, "approved_plate")
        if len(plates) != 1:
            errors.append(f"{fid}: exactly one approved plate/crop authority is required")
        else:
            plate = plates[0]
            if plate.get("path") != frame.get("plate"):
                errors.append(f"{fid}: plate reference differs from the registered staging plate")
            if plate.get("crop_rect_on_plate") != row.get("crop_rect_on_plate"):
                errors.append(f"{fid}: crop authority differs from the registered crop")
            if plate.get("materializer") != "normalized_crop.v1":
                errors.append(f"{fid}: crop must use normalized_crop.v1")
        rect = row.get("crop_rect_on_plate")
        if (not isinstance(rect, list) or len(rect) != 4 or
                not all(isinstance(n, (int, float)) for n in rect) or
                rect[0] < 0 or rect[1] < 0 or rect[2] <= 0 or rect[3] <= 0 or
                rect[0] + rect[2] > 1.000001 or rect[1] + rect[3] > 1.000001):
            errors.append(f"{fid}: invalid normalized crop rectangle")
        for item in inputs:
            if item.get("role") not in ("approved_plate", "identity_root", "size_anchor", "pose", "prop", "edit_base", "owner_correction_target"):
                errors.append(f"{fid}: unsupported regeneration reference role {item.get('role')!r}")
            path = _safe_repo_path(root, item.get("path"))
            if path is None:
                errors.append(f"{fid}: regeneration input path is not repository-relative")
                continue
            if not path.is_file():
                errors.append(f"{fid}: live regeneration input is missing: {item.get('path')}")
                continue
            expected = item.get("sha256")
            if not isinstance(expected, str) or not HASH_RE.fullmatch(expected):
                errors.append(f"{fid}: regeneration input has no SHA-256: {item.get('path')}")
            elif _hash(path) != expected:
                errors.append(f"{fid}: reference hash mismatch: {item.get('path')}")
            if item.get("role") == "edit_base" and not item.get("visually_approved", False):
                errors.append(f"{fid}: generated edit base is not visually approved")
            if item.get("role") == "owner_correction_target" and (
                    item.get("owner_directed_correction") is not True or
                    item.get("required") is not False or
                    item.get("authority_scope") != "correction target only; not identity, scale, camera, plate, or lighting authority"):
                errors.append(f"{fid}: owner correction target must be optional and explicitly non-authoritative")
        for actor in sorted(actors):
            identity = _input_by_role(inputs, "identity_root", actor)
            canonical = bible.get("characters", {}).get(actor, {}).get("canonical")
            if len(identity) != 1:
                errors.append(f"{fid}: visible actor {actor} needs exactly one identity_root reference")
            elif identity[0].get("path") != canonical:
                errors.append(f"{fid}: {actor} identity_root differs from visual_bible canonical")
            if actor == "milo" and row.get("foundation_authorities", {}).get(actor, {}).get("approval_status") != "approved_owner_hash_bound":
                errors.append(f"{fid}: Milo canonical/body approval is not hash-bound")
            if actor == "milo" and bible.get("character_foundation_approval", {}).get(
                    "milo_body_revision_status") != "approved_owner_hash_bound":
                errors.append(f"{fid}: visual bible does not record approved Milo canonical/body hash")
        for prop in row.get("required_props", []):
            if prop.get("status") not in ("approved", "approved_owner_hash_bound"):
                errors.append(f"{fid}: required prop {prop.get('id')} is pending owner approval")
            attached = [item for item in inputs if item.get("role") == "prop" and
                        item.get("id") == prop.get("id") and item.get("path") == prop.get("path")]
            if prop.get("status") in ("approved", "approved_owner_hash_bound") and len(attached) != 1:
                errors.append(f"{fid}: approved required prop {prop.get('id')} needs one regeneration input")
        anchor_id = row.get("size_anchor", {}).get("id")
        staged_anchor = frame.get("size_anchor_id")
        if not anchor_id or anchor_id != staged_anchor:
            errors.append(f"{fid}: size anchor ID differs from staging")
        registered = anchors.get(anchor_id, {})
        anchor = row.get("size_anchor", {})
        if not actors:
            pass
        elif (registered.get("status") != "approved_owner_hash_bound" or
                not anchor.get("path") or not anchor.get("sha256")):
            errors.append(f"{fid}: setup size anchor {anchor_id} is not approved and hash-bound")
        else:
            anchor_path = _safe_repo_path(root, anchor.get("path"))
            if anchor_path is None or not anchor_path.is_file():
                errors.append(f"{fid}: approved size-anchor image is missing")
            elif not HASH_RE.fullmatch(anchor["sha256"]) or _hash(anchor_path) != anchor["sha256"]:
                errors.append(f"{fid}: size-anchor hash mismatch")
            anchor_inputs = _input_by_role(inputs, "size_anchor")
            if (len(anchor_inputs) != 1 or anchor_inputs[0].get("path") != anchor.get("path") or
                    anchor_inputs[0].get("sha256") != anchor.get("sha256") or
                    anchor_inputs[0].get("id") != anchor_id):
                errors.append(f"{fid}: approved size anchor must be an attached hashed regeneration input")
        if row.get("mouth_policy") != "closed_boundary_for_lipsync":
            errors.append(f"{fid}: production boundary mouth policy is not closed")
        prompt = row.get("prompt", "")
        try:
            expected_ratio = float(bible["cast_scale"]["same_depth_standing_equivalent_height_ratio"]
                                   ["milo_to_leo"]["standing_equivalent_height"])
        except (KeyError, TypeError, ValueError):
            expected_ratio = None
        errors.extend(f"{fid}: {error}" for error in prompt_errors(
            prompt, sorted(actors), row.get("mouth_policy"), expected_ratio))
        candidate_path = row.get("active_candidate", {}).get("path")
        if candidate_path and any(item.get("path") == candidate_path for item in inputs):
            errors.append(f"{fid}: active generated image is being used as a regeneration input")
        for history in row.get("generation_history", {}).get("historical_inputs", []):
            if history.get("regeneration_allowed") is not False:
                errors.append(f"{fid}: historical input is not explicitly barred from regeneration")
            if history.get("role") == "owner_correction_target" and (
                    history.get("owner_directed_correction") is not True or
                    history.get("authority_scope") != "correction target only; not identity, scale, camera, plate, or lighting authority"):
                errors.append(f"{fid}: historical owner correction target is missing its non-authority record")
            if history.get("status") == "recoverable_from_git":
                locator = history.get("git_locator", {})
                if (not isinstance(history.get("sha256"), str) or
                        not HASH_RE.fullmatch(history.get("sha256", "")) or
                        locator.get("sha256") != history.get("sha256") or
                        not locator.get("commit") or not locator.get("path") or not locator.get("blob")):
                    errors.append(f"{fid}: historical Git locator is incomplete")
                elif not _git_locator_resolves(root, locator, history["sha256"]):
                    errors.append(f"{fid}: historical Git locator does not recover the recorded bytes")
            elif history.get("status") in ("legacy_source_unavailable", "external_source_unavailable",
                                               "external_cache_only"):
                warnings.append(f"{fid}: historical generation input lacks recoverable provenance: {history.get('path')}")
        for revision in row.get("generation_history", {}).get("recorded_revisions", []):
            if revision.get("status") in ("unrecoverable_recorded_revision",
                                            "checkout_only_without_git_locator"):
                message = (f"{fid}: candidate history lacks a recoverable Git locator: "
                           f"{revision.get('candidate_path')}")
                if revision.get("state") == "active_candidate":
                    errors.append(message)
                else:
                    warnings.append(message)
            if revision.get("status") == "recoverable_from_git":
                locator = revision.get("git_locator", {})
                if (not isinstance(revision.get("sha256"), str) or
                        not HASH_RE.fullmatch(revision.get("sha256", "")) or
                        not _git_locator_resolves(root, locator, revision["sha256"])):
                    message = f"{fid}: candidate Git locator does not recover the recorded bytes"
                    if revision.get("state") == "active_candidate":
                        errors.append(message)
                    else:
                        warnings.append(message)
        active = plan_rows.get(fid, {})
        if (row.get("active_candidate", {}).get("path") != active.get("candidate_path") or
                row.get("active_candidate", {}).get("sha256") != active.get("sha256")):
            errors.append(f"{fid}: contract active candidate differs from keyframe plan")
        if active.get("regeneration_status") == "stale_pending_new_revision":
            errors.append(f"{fid}: active candidate staging is stale and needs a new revision")
    expected_ids = set(frames)
    if ids != expected_ids:
        errors.append(f"reference contract frame set differs from staging: missing={sorted(expected_ids-ids)}, extra={sorted(ids-expected_ids)}")
    return errors


def validate_contract_report(contract: dict, root: Path = REPO,
                             staging: dict | None = None, bible: dict | None = None,
                             active_plan: dict | None = None) -> dict[str, list[str]]:
    """Separate readiness blockers from historical provenance debt."""
    warnings: list[str] = []
    blockers = validate_contract(contract, root, staging, bible, active_plan, warnings)
    return {"current_authority_blockers": blockers,
            "historical_provenance_warnings": warnings}


def validate_active_inventory(plan: dict, keyframes_dir: Path) -> list[str]:
    expected = {Path(row.get("candidate_path", "")).name for row in plan.get("images", [])}
    actual = {path.name for path in Path(keyframes_dir).glob("*.png")}
    errors = []
    if expected - actual:
        errors.append(f"active plan candidates are missing: {sorted(expected-actual)}")
    if actual - expected:
        errors.append(f"unreferenced active-root candidates exist: {sorted(actual-expected)}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story", required=True)
    parser.add_argument("--write-contract", action="store_true",
                        help="write the current portable regeneration contract before validating")
    args = parser.parse_args()
    story_dir = REPO / "stories" / args.story
    target = story_dir / "keyframe_regeneration_contract.json"
    if args.write_contract:
        contract = build_contract(args.story)
        target.write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n")
    elif target.is_file():
        contract = json.loads(target.read_text())
    else:
        print(f"BLOCKED: missing {target.relative_to(REPO)}; run with --write-contract")
        raise SystemExit(1)
    report = validate_contract_report(contract)
    errors = report["current_authority_blockers"]
    warnings = report["historical_provenance_warnings"]
    if errors:
        print("CURRENT AUTHORITY BLOCKERS:")
    for error in errors[:30]:
        print("BLOCKED:", error)
    if len(errors) > 30:
        print(f"...and {len(errors)-30} more")
    if warnings:
        print("HISTORICAL PROVENANCE WARNINGS (not current generation blockers):")
        for warning in warnings[:15]:
            print("WARN:", warning)
        if len(warnings) > 15:
            print(f"...and {len(warnings)-15} more")
    print(f"{len(errors)} current authority blockers; {len(warnings)} historical provenance warnings; "
          f"{len(contract.get('images', []))} regeneration contracts")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
