#!/usr/bin/env python3
"""Adopt a new, separately saved keyframe revision and rebuild its boundary plan.

The prior image and its review/rejection history remain untouched. This changes
the active candidate, not its approval state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import struct
import tempfile
from pathlib import Path

try:
    from . import keyframe_plan, keyframe_reference_gate, video_boundary_plan
    from .keyframe_visual_gate import CHECKS as VISUAL_CHECKS
except ImportError:  # pragma: no cover - direct script entry point
    import keyframe_plan
    import keyframe_reference_gate
    from keyframe_visual_gate import CHECKS as VISUAL_CHECKS
    import video_boundary_plan

REPO = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as source:
        head = source.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", head[16:24])


def revise(story: str, frame_id: str, relative_image: str, prompt: str,
           references: list[str], reason: str, root: Path = REPO,
           generation_tool: str = "built-in imagegen",
           owner_correction_target: bool = False) -> tuple[dict, dict]:
    root = root.resolve()
    story_dir = root / "stories" / story
    existing = json.loads((story_dir / "keyframe_plan.json").read_text())
    current = {row["id"]: row for row in existing["images"]}
    if frame_id not in current:
        raise ValueError(f"unknown keyframe {frame_id}")
    old = current[frame_id]
    keyframe_dir = (root / "character" / "characters" / story / "interactions" / "keyframes").resolve()
    new_path = (root / relative_image).resolve()
    if new_path.parent != keyframe_dir or new_path != root / relative_image:
        raise ValueError("revised image must be a direct, version-local keyframe path")
    old_match = re.fullmatch(rf"{re.escape(frame_id)}_r(\d+)_candidate\.png",
                             Path(old["candidate_path"]).name)
    new_match = re.fullmatch(rf"{re.escape(frame_id)}_r(\d+)_candidate\.png", new_path.name)
    if not old_match or not new_match or int(new_match[1]) <= int(old_match[1]):
        raise ValueError("candidate filename must have a strictly newer revision")
    if not new_path.is_file() or dimensions(new_path) != (1920, 1080):
        raise ValueError("candidate must exist as a 1920x1080 PNG")
    if not prompt.strip() or not references or not reason.strip():
        raise ValueError("exact revision prompt, references and reason are required")
    for reference in references:
        path = (root / reference).resolve()
        if not path.is_file() or (root not in path.parents and path != root):
            raise ValueError(f"missing or external reference: {reference}")
    fresh = keyframe_plan.build(story, root=root)
    planned = {row["id"]: row for row in fresh["images"]}[frame_id]
    immutable = ("scene", "audio_line_ids", "visual_unit_ids", "staging_ref")
    changed = [field for field in immutable if old.get(field) != planned.get(field)]
    if changed:
        raise ValueError(f"staging changed before revision: {', '.join(changed)}")
    contract = keyframe_reference_gate.build_contract(story, root=root)
    authority = next(row for row in contract["images"] if row["id"] == frame_id)
    actors = authority["actors"]
    anchors = json.loads((story_dir / "staging_plan.json").read_text()).get("setup_anchors", {})
    anchor = anchors.get(authority.get("size_anchor", {}).get("id"), {})
    if actors and (anchor.get("status") != "approved_owner_hash_bound" or
            not anchor.get("image_path") or not anchor.get("sha256")):
        raise ValueError(f"{frame_id}: select and hash-approve its same-setup size anchor before revision")
    gate_errors = keyframe_reference_gate.validate_contract(contract, root=root,
                                                             active_plan=existing)
    # Old generated inputs are provenance only; their unrecoverability is
    # reported by the audit gate but does not block a new revision built from
    # a complete, hash-verified authority stack. The old candidate itself must
    # still have an exact Git locator before it can be superseded below.
    revision_blockers = [error for error in gate_errors
                         if error.startswith(f"{frame_id}:") and
                         "historical generation input lacks recoverable provenance" not in error and
                         "candidate history lacks a recoverable Git locator" not in error and
                         "active candidate staging is stale and needs a new revision" not in error]
    if revision_blockers:
        raise ValueError(f"{frame_id}: regeneration contract is not ready: " +
                         "; ".join(revision_blockers))
    bible = json.loads((story_dir / "visual_bible.json").read_text())
    expected_ratio = float(bible["cast_scale"]["same_depth_standing_equivalent_height_ratio"]
                           ["milo_to_leo"]["standing_equivalent_height"])
    expected_inputs = authority["regeneration_inputs"]
    expected_paths = [item["path"] for item in expected_inputs]
    if owner_correction_target:
        correction_path = old.get("candidate_path")
        if references != [correction_path]:
            raise ValueError("owner correction mode must use exactly the active candidate as its correction target")
        correction_file = (root / correction_path).resolve()
        if not correction_file.is_file() or sha256(correction_file) != old.get("sha256"):
            raise ValueError("owner correction target must match the exact active candidate hash")
        required_correction_text = ("exactly two forearms and two hind legs",
                                    "remove the extra arm", "do not redraw, move, resize")
        if any(text not in prompt.lower() for text in required_correction_text):
            raise ValueError("owner correction prompt must name the limb-count fix and preserve the shot")
        inputs = [{"role": "owner_correction_target", "path": correction_path,
                   "sha256": sha256(correction_file), "required": False,
                   "owner_directed_correction": True,
                   "authority_scope": "correction target only; not identity, scale, camera, plate, or lighting authority"}]
    else:
        for error in keyframe_reference_gate.prompt_errors(
                prompt, actors, authority["mouth_policy"], expected_ratio):
            raise ValueError(f"{frame_id}: {error}")
        if references[:len(expected_paths)] != expected_paths:
            raise ValueError("references must begin with the registered plate, each visible actor canonical, "
                             "the approved size anchor, then any approved pose/prop authorities")
        if len(references) not in (len(expected_paths), len(expected_paths) + 1):
            raise ValueError("only the registered authorities and one optional approved edit base may be attached")
        inputs = [dict(item) for item in expected_inputs]
    if not owner_correction_target and len(references) > len(expected_paths):
        edit_path = references[-1]
        eligible = {row.get("candidate_path"): row for row in existing["images"]}
        base = eligible.get(edit_path)
        review_ledger = json.loads((story_dir / "keyframe_visual_reviews.json").read_text())
        review = review_ledger.get("images", {}).get(base.get("id") if base else "", {})
        rejection = review_ledger.get("known_rejections", {}).get(base.get("id") if base else "", {})
        base_path = (root / edit_path).resolve()
        if (base is None or not base_path.is_file() or
                rejection.get("sha256") == sha256(base_path) or
                review.get("sha256") != sha256(base_path) or
                not review.get("reviewer") or not review.get("reviewed_at") or
                not all(review.get("checks", {}).get(check) is True for check in VISUAL_CHECKS)):
            raise ValueError("optional generated edit base must have a current full-resolution visual approval")
        inputs.append({"role": "edit_base", "path": edit_path,
                       "sha256": sha256(base_path), "required": False,
                       "visually_approved": True})
    if prompt.strip() != planned["prompt"].strip():
        # Revision prompts are allowed to describe the focused correction, but
        # the immutable source locks must still be present in the sent text.
        required_clauses = (() if owner_correction_target else
                            ("WORLD AND LIGHT LOCK:", "SIZE ANCHOR:", "IDENTITY LOCK:",
                             "MOUTH POLICY: closed production boundary"))
        missing_clauses = [clause for clause in required_clauses if clause not in prompt]
        if missing_clauses:
            raise ValueError(f"revision prompt omits required source locks: {', '.join(missing_clauses)}")
    for reference in references:
        path = (root / reference).resolve()
        if not path.is_file() or (root not in path.parents and path != root):
            raise ValueError(f"missing or external reference: {reference}")
        record = next((item for item in inputs if item.get("path") == reference), None)
        if record is None or sha256(path) != record.get("sha256"):
            raise ValueError(f"reference is not a hashed authority in the regeneration contract: {reference}")
    updated = json.loads(json.dumps(existing))
    row = next(item for item in updated["images"] if item["id"] == frame_id)
    history = row.setdefault("generation_history", [])
    old_locator = row.get("git_locator") or keyframe_reference_gate.git_locator(
        root, row.get("candidate_path", ""))
    if not old_locator or old_locator.get("sha256") != row.get("sha256"):
        raise ValueError("superseded candidate needs an exact recoverable Git locator before replacement")
    history.append({"candidate_path": row.get("candidate_path"), "sha256": row.get("sha256"),
                    "prompt": row.get("historical_candidate_prompt"),
                    "references": row.get("historical_candidate_references", []),
                    "generation_inputs": row.get("historical_candidate_inputs", []),
                    "git_locator": old_locator,
                    "status": "historical_superseded_candidate",
                    "reason": reason})
    new_sha = sha256(new_path)
    row.update(candidate_path=relative_image, sha256=new_sha,
               historical_candidate_prompt=prompt.strip(),
               historical_candidate_references=references,
               historical_candidate_inputs=inputs,
               historical_candidate_reference_roles=(inputs if owner_correction_target
                   else authority["regeneration_inputs"]),
               historical_candidate_tool=generation_tool, revision_note=reason,
               status="candidate_generated_pending_owner_review",
               canvas_px=[1920, 1080], mouth_policy=authority["mouth_policy"],
               reference_plate=planned["reference_plate"],
               reference_crop=planned.get("reference_crop"),
               board_reference=planned.get("board_reference"),
               required_props=planned.get("required_props", []),
               actors=planned["actors"],
               size_anchor_id=authority["size_anchor"]["id"],
               view=authority["view"], crop_rect_on_plate=authority["crop_rect_on_plate"],
               camera_family=authority["camera_family"],
               staging_signature=authority["staging_signature"],
               regeneration_status="current_staging_matches_candidate_record",
               planned_view=planned["view"],
               planned_crop_rect_on_plate=planned["crop_rect_on_plate"],
               planned_size_anchor_id=planned["size_anchor_id"],
               planned_actors=planned["actors"],
               planned_camera_family=planned["camera_family"])
    for field in ("prompt", "references", "reference_roles", "generation_inputs",
                  "generation_tool", "planned_staging_changes"):
        row.pop(field, None)
    row.pop("generated_source", None)
    row.pop("revision_prompt", None)
    row.pop("revision_references", None)
    config = json.loads((story_dir / "video_boundary_config.json").read_text())
    staging = json.loads((story_dir / "staging_plan.json").read_text())
    boundaries = video_boundary_plan.build(updated, config, staging=staging)
    return updated, boundaries


def write_plan(story: str, plan: dict, boundaries: dict, root: Path = REPO) -> None:
    story_dir = root / "stories" / story
    outputs = {
        story_dir / "keyframe_plan.json": json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
        story_dir / "video_boundary_plan.json": json.dumps(boundaries, indent=2, ensure_ascii=False) + "\n",
        story_dir / "VIDEO_BOUNDARIES.md": video_boundary_plan.markdown(boundaries),
        story_dir / "keyframe_regeneration_contract.json": json.dumps(
            keyframe_reference_gate.build_contract(story, root=root, active_plan=plan), indent=2,
            ensure_ascii=False) + "\n",
    }
    review_path = story_dir / "keyframe_visual_reviews.json"
    reviews = json.loads(review_path.read_text())
    try:
        from .keyframe_visual_gate import build_frame_dispositions
    except ImportError:  # pragma: no cover - direct script entry point
        from keyframe_visual_gate import build_frame_dispositions
    reviews["frame_dispositions"] = build_frame_dispositions(plan, reviews)
    outputs[review_path] = json.dumps(reviews, indent=2, ensure_ascii=False) + "\n"
    staged = []
    try:
        for target, content in outputs.items():
            with tempfile.NamedTemporaryFile(mode="w", dir=story_dir, prefix=".revision-",
                                             delete=False, encoding="utf-8") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
                staged.append((Path(handle.name), target))
        for temporary, target in staged:
            temporary.replace(target)
    finally:
        for temporary, _ in staged:
            temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story", required=True)
    parser.add_argument("--frame", required=True)
    parser.add_argument("--image", required=True, help="repository-relative new candidate PNG")
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--reference", action="append", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--generation-tool", default="built-in imagegen",
                        help="generator/compositor used for this revision")
    parser.add_argument("--owner-correction-target", action="store_true",
                        help="record the exact active candidate as a user-directed correction target, not a source authority")
    args = parser.parse_args()
    plan, boundaries = revise(args.story, args.frame, args.image,
                              args.prompt_file.read_text(), args.reference, args.reason,
                              generation_tool=args.generation_tool,
                              owner_correction_target=args.owner_correction_target)
    write_plan(args.story, plan, boundaries)
    print(f"{args.frame}: active candidate {args.image}; visual review still required")


if __name__ == "__main__":
    main()
