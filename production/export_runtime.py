#!/usr/bin/env python3
"""Export a runtime story.yaml for production/shot.py from a prompt manifest and
an owner-made image set.

  python3 production/export_runtime.py --manifest stories/lion_and_mouse_v5/prompt_manifest.json \\
      --images lion_and_mouse_v5 --story lion_and_mouse_v5
  python3 production/export_runtime.py --manifest stories/ugly_duckling_v1/prompt_manifest.json \\
      --story ugly_duckling_v1 --scenes 1 2 3 4 5 6 7 8 9

One runtime shot per video variant of the manifest (name = variant id, e.g.
`s03_two_paths_closed_r01`), with
  keyframe / end_keyframe  copies of the image set's files for the variant's
                           start/end records (exact hash-recorded file when
                           available; exact hash-approved target for chained stories), frozen in
                           work/stories/<story>/keyframes/ so that
                           moving or replacing source images cannot change a run
  prompt / negative        the variant's reviewed runtime prompts, verbatim
  frames, size, seeds      from the variant
Without --images each record's `target` in the manifest is its file. With
--images, exact hash-verified sources from an existing runtime_inputs.json take
priority, then existing manifest targets, then an unambiguous README file. Also
writes stories/<story>/runtime_inputs.json: every endpoint file with its sha256,
so a later change of an image is visible.
Variants without seeds get 1 2 3; without size, 1280x720. --scenes limits the
export to scenes whose images exist (the others are listed as skipped).
A chained story's piece with `reuse` (CR-21) is not exported: its renders are the
earlier story's; it is listed under `reused:` in story.yaml instead.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from feltwillow import paths  # noqa: E402
from feltwillow.version_policy import INDEPENDENT_STORIES  # noqa: E402
from image_approval import reference_files, spec_sha256  # noqa: E402
from keyframe_visual_gate import validate as validate_keyframe_visual_reviews  # noqa: E402


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def version_isolation_failure(reason: str) -> None:
    """Stop an export whose declared story inputs do not identify one story."""
    sys.exit(f"VERSION_ISOLATION_FAILURE: {reason}")


def require_independent_image_path(image_set: str, file: Path) -> None:
    """A protected story may resolve image bytes only from its own version roots."""
    if image_set not in INDEPENDENT_STORIES:
        return
    resolved = file.resolve()
    roots = ((paths.REPO / "character/characters" / image_set).resolve(),
             (paths.REPO / "character/locations" / image_set).resolve())
    if not any(root == resolved or root in resolved.parents for root in roots):
        version_isolation_failure(
            f"image source escapes {image_set}'s character/location roots: {file}"
        )


def image_map(image_set: str) -> dict[str, Path]:
    """Resolve exact, previously frozen sources before manifest and README fallbacks.

    A README supplies a candidate only when it has one matching revision. Never
    silently change an already recorded input to a newer image revision.
    """
    roots = [paths.REPO / "character/characters" / image_set / n for n in ("Leo", "Milo", "interactions")]
    roots.append(paths.REPO / "character/locations" / image_set)
    out: dict[str, Path] = {}
    recorded_path = paths.STORIES / image_set / "runtime_inputs.json"
    if recorded_path.is_file():
        recorded = json.loads(recorded_path.read_text())
        for rid, row in recorded.items():
            file = paths.REPO / row["file"]
            require_independent_image_path(image_set, file)
            if not file.is_file():
                raise FileNotFoundError(f"recorded source for {rid} is missing: {file}")
            if file_sha256(file) != row["sha256"]:
                raise ValueError(f"recorded source for {rid} changed hash: {file}; "
                                 "review it before exporting a new runtime")
            out[rid] = file
    manifest_path = paths.STORIES / image_set / "prompt_manifest.json"
    if manifest_path.is_file():
        for rec in json.loads(manifest_path.read_text())["images"]:
            target = rec.get("target")
            file = paths.REPO / target if target else None
            if rec["id"] not in out and file:
                require_independent_image_path(image_set, file)
                if file.is_file():
                    out[rec["id"]] = file
    for root in roots:
        readme = root / "README.md"
        if not readme.is_file():
            continue
        folder = None
        for line in readme.read_text().splitlines():
            m = re.match(r"## `(.+?)/?`", line)
            if m:
                folder = paths.REPO / m.group(1)
                continue
            m = re.match(r"\| `([^`]+)_r01\.png` \| `([^`]+)`", line)
            if m and folder and m.group(2) not in out:
                # Exact stem only: l_side_r01 must not select l_side_r_r01.
                rev = re.compile(rf"{re.escape(m.group(1))}_r(\d+)\.png")
                found = [f for f in folder.glob("*.png") if rev.fullmatch(f.name)]
                if len(found) > 1:
                    raise ValueError(f"{m.group(2)} has multiple README image revisions: "
                                     f"{', '.join(str(f) for f in sorted(found))}; "
                                     "record an exact source before runtime export")
                if found:
                    out[m.group(2)] = found[0]
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--images", help="image set with hash-recorded sources, manifest targets and README "
                    "fallbacks, e.g. lion_and_mouse_v5; default: the manifest's record targets")
    ap.add_argument("--story", required=True)
    ap.add_argument("--scenes", nargs="+", type=int)
    args = ap.parse_args()
    # Resolve the manifest and establish its owning story before loading any
    # output paths or source images. A manifest from another story must never
    # be combined with this story's approvals, repairs, or runtime directory.
    expected_manifest = (paths.STORIES / args.story / "prompt_manifest.json").resolve()
    manifest_path = (paths.REPO / args.manifest).resolve()
    if manifest_path != expected_manifest:
        version_isolation_failure(
            f"--manifest must be stories/{args.story}/prompt_manifest.json; got {args.manifest}"
        )
    man = json.loads(manifest_path.read_text())
    candidate_plan_path = paths.STORIES / args.story / "keyframe_plan.json"
    if candidate_plan_path.is_file():
        visual_review_path = paths.STORIES / args.story / "keyframe_visual_reviews.json"
        visual_reviews = (json.loads(visual_review_path.read_text())
                          if visual_review_path.is_file() else {})
        visual_errors = validate_keyframe_visual_reviews(
            json.loads(candidate_plan_path.read_text()), visual_reviews, paths.REPO)
        if visual_errors:
            sys.exit("VISUAL_REVIEW_BLOCKED: candidate keyframes need full-resolution, "
                     "hash-bound approval before runtime export. First blockers:\n  "
                     + "\n  ".join(visual_errors[:10])
                     + (f"\n  ...and {len(visual_errors) - 10} more" if len(visual_errors) > 10 else ""))
    native_assets = (man.get("asset_revision_policy") == "v6_native_assets"
                     or args.story in INDEPENDENT_STORIES)
    if native_assets:
        if args.images and args.images != args.story:
            version_isolation_failure(
                f"--images {args.images} does not match independent --story {args.story}"
            )
        if man.get("audio_story") != args.story:
            version_isolation_failure(
                f"manifest audio_story {man.get('audio_story')!r} does not match --story {args.story}"
            )
        bible_file = paths.STORIES / args.story / "visual_bible.json"
        if not bible_file.is_file():
            version_isolation_failure(f"native-assets story bible is missing: {bible_file}")
        bible = json.loads(bible_file.read_text())
        bible_version = bible.get("version")
        if bible_version != args.story:
            version_isolation_failure(
                f"visual_bible version {bible_version!r} does not match --story {args.story}"
            )
        if bible.get("asset_revision_policy") != "v6_native_assets":
            version_isolation_failure(
                f"visual_bible asset_revision_policy must be v6_native_assets; "
                f"got {bible.get('asset_revision_policy')!r}"
            )
        foreign_repairs = sorted({
            repair.get("source_story")
            for rows in (json.loads((paths.STORIES / args.story / "repair_overrides.json").read_text())
                         .get("repairs", {}) if (paths.STORIES / args.story / "repair_overrides.json").is_file()
                         else {}).values()
            for repair in rows
            if repair.get("source_story") != args.story
        })
        if foreign_repairs:
            version_isolation_failure(
                f"repair source story must be {args.story}; found {', '.join(map(str, foreign_repairs))}"
            )
    if args.images:
        files = image_map(args.images)
    else:
        files = {}
        for image in man["images"]:
            if not image.get("target"):
                continue
            file = paths.REPO / image["target"]
            require_independent_image_path(args.story, file)
            if file.is_file():
                files[image["id"]] = file
    work = paths.story_work(args.story)
    sd = paths.STORIES / args.story
    bible_path = sd / "visual_bible.json"
    chained = bible_path.is_file() and json.loads(bible_path.read_text()).get("chained_coverage")
    approval_file = sd / "image_approvals.json"
    approvals = json.loads(approval_file.read_text()).get("images", {}) if approval_file.is_file() else {}
    image_records = {i["id"]: i for i in man["images"]}
    repair_path = sd / "repair_overrides.json"
    repair_doc = json.loads(repair_path.read_text()) if repair_path.is_file() else {"repairs": {}}
    repairs = repair_doc.get("repairs", {})
    scenes, inputs, missing, reused = {}, {}, [], {}
    pending_copies: dict[Path, Path] = {}
    invalid_carried: set[str] = set()
    for s in sorted(man["shots"], key=lambda s: (s["scene"], s["order"])):
        if args.scenes and s["scene"] not in args.scenes:
            continue
        if chained:
            for v in s["variants"]:
                for rid in (v["start_image"], v["end_image"]):
                    rec = image_records[rid]
                    if rec.get("carried_from") and rec.get("status") != "accepted" and rid not in invalid_carried:
                        invalid_carried.add(rid)
                        missing.append(f"{s['id']}: carried image {rid} has status "
                                       f"{rec.get('status')!r}, not accepted")
        is_reuse = bool(s.get("reuse"))
        if is_reuse:
            reused[s["id"]] = s["reuse"]
            if not repairs.get(s["id"]):
                continue
        for v in s["variants"]:
            ends = {}
            for key in ("start_image", "end_image"):
                f = files.get(v[key])
                rec = image_records[v[key]]
                if chained and not rec.get("carried_from") and rec.get("prompt_kind") == "scene":
                    approval = approvals.get(v[key])
                    if not approval:
                        missing.append(f"{v['id']}: image {v[key]} has no explicit approval in {approval_file}")
                        continue
                    if approval.get("file") != rec["target"]:
                        missing.append(f"{v['id']}: approval for {v[key]} names a different manifest target")
                        continue
                    f = paths.REPO / approval["file"]
                    if not f.is_file():
                        missing.append(f"{v['id']}: approved image file is missing: {f}")
                        continue
                    digest = hashlib.sha256(f.read_bytes()).hexdigest()
                    if approval.get("sha256") != digest:
                        missing.append(f"{v['id']}: approval for {v[key]} does not match current file hash")
                        continue
                    if approval.get("spec_sha256") != spec_sha256(rec):
                        missing.append(f"{v['id']}: approval for {v[key]} is stale for the current image prompt/specification")
                        continue
                    try:
                        refs_now = reference_files(rec, paths.REPO)
                    except FileNotFoundError as error:
                        missing.append(f"{v['id']}: {error}")
                        continue
                    if approval.get("references") != refs_now:
                        missing.append(f"{v['id']}: approval for {v[key]} is stale because a prompt reference changed")
                        continue
                if f is None:
                    missing.append(f"{v['id']}: {v[key]}")
                    continue
                frozen = work / "keyframes" / f.name
                previous = pending_copies.get(frozen)
                if previous is not None and previous != f:
                    missing.append(f"{v['id']}: frozen keyframe name collision: {previous} and {f}")
                    continue
                pending_copies[frozen] = f
                ends[key] = f"keyframes/{f.name}"
                inputs[v[key]] = dict(file=str(f.relative_to(paths.REPO)), frozen=ends[key],
                                      sha256=file_sha256(f))
            if len(ends) < 2:
                continue
            runtime = dict(
                name=v["id"], shot=s["id"], mode=v["mode"], speaker=v.get("speaker"),
                dialogue_line_ids=v.get("dialogue_line_ids", []),
                keyframe=ends["start_image"], end_keyframe=ends["end_image"],
                prompt=v["positive_prompt"], negative=v.get("negative_prompt", ""),
                frames=v["frames"], size=v.get("size") or [1280, 720], seeds=v.get("seeds") or [1, 2, 3])
            if not is_reuse:
                scenes.setdefault(s["scene"], {"shots": []})["shots"].append(runtime)
            for repair in repairs.get(s["id"], []):
                candidate = dict(runtime)
                candidate_name = f"{v['id']}_repair{int(repair['revision']):02d}"
                candidate.update(name=candidate_name,
                                 keyframe=f"keyframes/repairs/{candidate_name}.png",
                                 continue_from={"file": repair["source_file"], "sha256": repair["sha256"],
                                                "frame": repair.get("frame", -1),
                                                "story": repair["source_story"],
                                                "piece": repair["source_piece"]},
                                 repair_revision=int(repair["revision"]), seeds=[1])
                scenes.setdefault(s["scene"], {"shots": []})["shots"].append(candidate)
    if missing:
        sys.exit("missing or unapproved images:\n  " + "\n  ".join(missing))
    for frozen, source in pending_copies.items():
        frozen.parent.mkdir(parents=True, exist_ok=True)
        if not frozen.is_file() or file_sha256(frozen) != file_sha256(source):
            shutil.copy2(source, frozen)
    sd.mkdir(parents=True, exist_ok=True)
    story = dict(
        title=man.get("title") or args.story, slug=args.story,
        source=dict(manifest=str(args.manifest), manifest_revision=man.get("revision"),
                    images=args.images or "manifest targets", scenes=args.scenes or "all"),
        note="Generated by production/export_runtime.py; do not edit by hand. "
             "Each shot carries its full prompt (shot.py uses `prompt:` verbatim).",
        negative="", style="", scenes=scenes)
    if reused:
        story["reused"] = reused
    (sd / "story.yaml").write_text(yaml.safe_dump(story, sort_keys=False, width=100, allow_unicode=True))
    (sd / "runtime_inputs.json").write_text(json.dumps(inputs, indent=2, sort_keys=True))
    n = sum(len(sc["shots"]) for sc in scenes.values())
    print(f"{n} runtime shots in {len(scenes)} scenes -> {sd / 'story.yaml'}"
          + (f"; {len(reused)} pieces reuse earlier renders" if reused else ""))


if __name__ == "__main__":
    main()
