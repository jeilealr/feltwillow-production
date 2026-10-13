"""Contract tests for the native keyframe-plan runtime adapter."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "production"))

from keyframe_visual_gate import CHECKS
from keyframe_reference_gate import SCHEMA as REFERENCE_SCHEMA
from v6_runtime import PIPELINE, POLICY, REPO, TIMING_SCHEMA, WORD_SCHEMA, export, preflight
from video_boundary_plan import build


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def _fixture(root: Path) -> tuple[Path, dict]:
    story = "lion_and_mouse_v6"
    folder = root / "stories" / story
    folder.mkdir(parents=True)
    audio_bytes = b"synthetic WAV bytes"
    audio_hash = hashlib.sha256(audio_bytes).hexdigest()
    source = root / "work/the_lion_and_the_mouse/lines/S01-L001.wav"
    target = root / f"work/stories/{story}/audio/en/lines/S01-L001.wav"
    scene_wav = root / f"work/stories/{story}/audio/en/scene01.wav"
    for path in (source, target, scene_wav):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(audio_bytes)
    canonical = root / f"character/characters/{story}/Milo/canonical.png"
    canonical.parent.mkdir(parents=True, exist_ok=True)
    canonical.write_bytes(b"Milo canonical")
    canonical_hash = hashlib.sha256(canonical.read_bytes()).hexdigest()
    anchor = root / f"character/characters/{story}/anchors/tree.png"
    anchor.parent.mkdir(parents=True, exist_ok=True)
    anchor.write_bytes(b"approved anchor")
    anchor_hash = hashlib.sha256(anchor.read_bytes()).hexdigest()
    plate = root / "character/locations/lion_and_mouse_v6/stream.png"
    plate.parent.mkdir(parents=True, exist_ok=True)
    plate.write_bytes(b"location plate")
    plate_hash = hashlib.sha256(plate.read_bytes()).hexdigest()
    _write(folder / "visual_bible.json", {"story": story, "version": "v6",
                                         "pipeline": PIPELINE,
                                         "asset_revision_policy": POLICY,
                                         "characters": {"milo": {"canonical": f"character/characters/{story}/Milo/canonical.png"}},
                                         "character_foundation_approval": {"milo_body_revision_status": "approved_owner_hash_bound"}})
    line = {"id": "S01-L001", "scene": 1, "speaker": "NARRATOR",
            "duration_seconds": 0.8,
            "source_path": "work/the_lion_and_the_mouse/lines/S01-L001.wav",
            "v6_path": f"work/stories/{story}/audio/en/lines/S01-L001.wav",
            "sha256": audio_hash}
    audio = {"story": story, "owner_authorized_reuse": True,
             "source_story": "lion_and_mouse_v5", "line_count": 1,
             "scene_count": 1, "lines": [line],
             "assembly_rule": {"pause_same_speaker_seconds": 0.45,
                               "pause_speaker_change_seconds": 0.7,
                               "tail_silence_seconds_per_scene": 0.2},
             "scenes": [{"scene": 1, "path": f"work/stories/{story}/audio/en/scene01.wav",
                         "duration_seconds": 1.0, "sha256": audio_hash}]}
    _write(folder / "audio_manifest.json", audio)
    _write(folder / "dialogue_coverage.json", {"story": story,
            "lines": [{"id": "S01-L001", "scene": 1, "speaker": "NARRATOR",
                       "audio_path": line["v6_path"], "audio_sha256": audio_hash}]})
    frames = []
    stage_frames = []
    reviews = {}
    for name, contents in (("s01_p01", b"PNG frame one"), ("s01_p02", b"PNG frame two")):
        relative = f"character/characters/{story}/interactions/keyframes/{name}.png"
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(contents)
        digest = hashlib.sha256(contents).hexdigest()
        frames.append({"id": name, "scene": 1, "candidate_path": relative,
                       "approved_plate": "character/locations/lion_and_mouse_v6/stream.png",
                       "crop_rect_on_plate": [0, 0, 1, 1],
                       "audio_line_ids": ["S01-L001"], "sha256": digest,
                       "planned_actors": {"milo": {}},
                       "planned_size_anchor_id": "stream_wide_milo",
                       "planned_camera_family": "stream:wide"})
        stage_frames.append({"id": name, "scene": 1, "location": "stream", "plate": "character/locations/lion_and_mouse_v6/stream.png",
                             "view": "wide", "size_anchor_id": "stream_wide_milo",
                             "actors": {"milo": {"contact_xy_on_plate": [0.5, 0.8], "depth_t": 0.5,
                                                   "standing_equivalent_height_fraction_after_crop": 0.2}}})
        reviews[name] = {"sha256": digest, "reviewer": "fixture reviewer",
                         "reviewed_at": "2026-10-11", "size_anchor_id": "stream_wide_milo",
                         "size_anchor_sha256": anchor_hash, "camera_family": "stream:wide",
                         "identity_reference_sha256": {"milo": canonical_hash},
                         "size_evidence": "measured fixture", "checks": {check: True for check in CHECKS}}
    keys = {"story": story, "keyframe_count": 2, "images": frames}
    config = {"schema": "feltwillow.video-boundary-config.v1", "story": story,
              "cut_reasons": {"1": "Opening"}}
    _write(folder / "keyframe_plan.json", keys)
    staging = {"story": story, "frames": stage_frames, "views": {"wide": {"magnification": 1.0}},
               "setup_anchors": {"stream_wide_milo": {"status": "approved_owner_hash_bound",
                    "image_path": f"character/characters/{story}/anchors/tree.png", "sha256": anchor_hash}}}
    _write(folder / "staging_plan.json", staging)
    contract_images = []
    for row in frames:
        contract_images.append({"id": row["id"], "actors": ["milo"], "location": "stream",
            "camera_family": "stream:wide", "view": "wide", "crop_rect_on_plate": [0, 0, 1, 1],
            "size_anchor": {"id": "stream_wide_milo", "status": "approved_owner_hash_bound",
                            "path": f"character/characters/{story}/anchors/tree.png", "sha256": anchor_hash},
            "foundation_authorities": {"milo": {"canonical_path": f"character/characters/{story}/Milo/canonical.png",
                "sha256": canonical_hash, "approval_status": "approved_owner_hash_bound"}},
            "regeneration_inputs": [
                {"role": "approved_plate", "path": "character/locations/lion_and_mouse_v6/stream.png", "sha256": plate_hash,
                 "required": True, "crop_rect_on_plate": [0, 0, 1, 1], "materializer": "normalized_crop.v1"},
                {"role": "identity_root", "actor": "milo", "path": f"character/characters/{story}/Milo/canonical.png",
                 "sha256": canonical_hash, "required": True},
                {"role": "size_anchor", "id": "stream_wide_milo",
                 "path": f"character/characters/{story}/anchors/tree.png", "sha256": anchor_hash,
                 "required": True}],
            "mouth_policy": "closed_boundary_for_lipsync",
            "prompt": "Milo standing-equivalent anatomical height target 20% of this frame. No mane.",
            "active_candidate": {"path": row["candidate_path"], "sha256": row["sha256"]},
            "generation_history": {"historical_inputs": []}})
    _write(folder / "keyframe_regeneration_contract.json", {"schema": REFERENCE_SCHEMA,
        "story": story, "images": contract_images})
    _write(folder / "video_boundary_config.json", config)
    _write(folder / "video_boundary_plan.json", build(keys, config, staging=staging))
    _write(folder / "keyframe_visual_reviews.json", {
        "schema": "feltwillow.keyframe-visual-reviews.v1", "story": story,
        "known_rejections": {}, "images": reviews})
    return folder, keys


def _check_current_packet_reaches_only_visual_approval_blockers() -> None:
    _, errors = preflight(root=REPO)
    assert errors
    assert all(error.startswith(("VISUAL:", "REFERENCE:")) for error in errors)
    reviews = json.loads((REPO / "stories/lion_and_mouse_v6/keyframe_visual_reviews.json").read_text())
    plan = json.loads((REPO / "stories/lion_and_mouse_v6/keyframe_plan.json").read_text())
    assert len(errors) >= plan["keyframe_count"]
    by_id = {row["id"]: row for row in plan["images"]}
    for frame_id in ("s14_p04", "s14_p05"):
        assert by_id[frame_id]["superseded"][-1]["sha256"] == reviews["known_rejections"][frame_id]["sha256"]
        assert by_id[frame_id]["sha256"] != reviews["known_rejections"][frame_id]["sha256"]


def _check_approved_fixture_preflights_and_exports_without_legacy_manifest(tmp_path: Path) -> None:
    folder, _ = _fixture(tmp_path)
    draft, errors = preflight(root=tmp_path, require_local_audio=True)
    assert not errors
    assert draft["story"] == "lion_and_mouse_v6"
    assert not (folder / "prompt_manifest.json").exists()
    timing = {"schema": TIMING_SCHEMA, "story": "lion_and_mouse_v6", "pieces": [
        {"scene": 1, "start_seconds": 0, "end_seconds": 1,
         "start_keyframe": "s01_p01", "end_keyframe": "s01_p02",
         "audio_line_ids": ["S01-L001"], "mouth_mode": "silent"}]}
    timing_file = tmp_path / "timing.json"
    _write(timing_file, timing)
    target, errors = export("lion_and_mouse_v6", timing_file, root=tmp_path)
    assert not errors and target == (folder / "runtime_plan.json").resolve()
    plan = json.loads(target.read_text())
    assert plan["pieces"][0]["start_image"] == draft["scenes"][0]["start_image"]
    assert plan["pieces"][0]["start_sha256"] == plan["pieces"][0]["start_review_sha256"]
    assert plan["pieces"][0]["audio_sha256"] == hashlib.sha256(b"synthetic WAV bytes").hexdigest()
    assert len(plan["pieces"]) == 1


def _check_review_and_identity_fail_closed(tmp_path: Path) -> None:
    folder, keys = _fixture(tmp_path)
    bible = json.loads((folder / "visual_bible.json").read_text())
    bible["story"] = "wrong_story"
    _write(folder / "visual_bible.json", bible)
    _, errors = preflight(root=tmp_path)
    assert any("visual_bible belongs" in error for error in errors)
    bible["story"] = "lion_and_mouse_v6"
    _write(folder / "visual_bible.json", bible)

    reviews = json.loads((folder / "keyframe_visual_reviews.json").read_text())
    del reviews["images"]["s01_p01"]
    _write(folder / "keyframe_visual_reviews.json", reviews)
    _, errors = preflight(root=tmp_path)
    assert any("no full-resolution visual review" in error for error in errors)
    reviews["known_rejections"]["s01_p02"] = {"sha256": keys["images"][1]["sha256"],
                                                "reason": "identity drift"}
    _write(folder / "keyframe_visual_reviews.json", reviews)
    _, errors = preflight(root=tmp_path)
    assert any("known rejected PNG" in error for error in errors)
    assert not (folder / "runtime_plan.json").exists()


def _check_wrong_hash_and_audio_provenance_fail_closed(tmp_path: Path) -> None:
    folder, keys = _fixture(tmp_path)
    frame = tmp_path / keys["images"][0]["candidate_path"]
    frame.write_bytes(b"changed candidate")
    _, errors = preflight(root=tmp_path)
    assert any("differs from keyframe_plan.json SHA-256" in error for error in errors)
    frame.write_bytes(b"PNG frame one")
    audio = json.loads((folder / "audio_manifest.json").read_text())
    audio["lines"][0]["v6_path"] = "work/stories/lion_and_mouse_v5/audio/en/lines/S01-L001.wav"
    _write(folder / "audio_manifest.json", audio)
    _, errors = preflight(root=tmp_path)
    assert any("invalid source/runtime namespace" in error for error in errors)


def _check_missing_boundary_image_and_invalid_timing_leave_no_partial_output(tmp_path: Path) -> None:
    folder, keys = _fixture(tmp_path)
    (tmp_path / keys["images"][1]["candidate_path"]).unlink()
    _, errors = preflight(root=tmp_path)
    assert any("candidate PNG is missing" in error for error in errors)
    (tmp_path / keys["images"][1]["candidate_path"]).write_bytes(b"PNG frame two")
    timing_file = tmp_path / "timing.json"
    _write(timing_file, {"schema": TIMING_SCHEMA, "story": "lion_and_mouse_v6",
                         "pieces": [{"scene": 1, "start_seconds": 0, "end_seconds": 2,
                                     "start_keyframe": "s01_p01", "end_keyframe": "s01_p02",
                                     "audio_line_ids": ["S01-L001"], "mouth_mode": "silent"}]})
    target, errors = export("lion_and_mouse_v6", timing_file, root=tmp_path)
    assert target is None and any(error.startswith("TIMING:") for error in errors)
    assert not (folder / "runtime_plan.json").exists()


class V6RuntimeTests(unittest.TestCase):
    def test_current_packet_reaches_only_visual_approval_blockers(self) -> None:
        _check_current_packet_reaches_only_visual_approval_blockers()

    def test_approved_fixture_preflights_and_exports_without_legacy_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _check_approved_fixture_preflights_and_exports_without_legacy_manifest(Path(directory))

    def test_review_and_identity_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _check_review_and_identity_fail_closed(Path(directory))

    def test_wrong_hash_and_audio_provenance_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _check_wrong_hash_and_audio_provenance_fail_closed(Path(directory))

    def test_missing_boundary_image_and_invalid_timing_leave_no_partial_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _check_missing_boundary_image_and_invalid_timing_leave_no_partial_output(Path(directory))

    def test_intra_line_cut_requires_reviewed_audio_hash_bound_word_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder, _ = _fixture(root)
            pieces = [
                {"scene": 1, "start_seconds": 0, "end_seconds": 0.4,
                 "start_keyframe": "s01_p01", "end_keyframe": "s01_p01",
                 "audio_line_ids": ["S01-L001"], "mouth_mode": "silent"},
                {"scene": 1, "start_seconds": 0.4, "end_seconds": 1,
                 "start_keyframe": "s01_p01", "end_keyframe": "s01_p02",
                 "audio_line_ids": ["S01-L001"], "mouth_mode": "silent"},
            ]
            timing_file = root / "timing.json"
            _write(timing_file, {"schema": TIMING_SCHEMA,
                                 "story": "lion_and_mouse_v6", "pieces": pieces})
            target, errors = export("lion_and_mouse_v6", timing_file, root=root)
            self.assertIsNone(target)
            self.assertTrue(any("without reviewed word-timing evidence" in error for error in errors))
            self.assertFalse((folder / "runtime_plan.json").exists())
            word_file = root / "words.json"
            _write(word_file, {"schema": WORD_SCHEMA, "story": "lion_and_mouse_v6",
                               "scenes": {"1": {
                                   "audio_sha256": hashlib.sha256(b"synthetic WAV bytes").hexdigest(),
                                   "reviewer": "fixture reviewer", "reviewed_at": "2026-10-11",
                                   "anchors": [{"seconds": 0.4, "line_id": "S01-L001",
                                                "word_index": 2, "word": "fixture"}]}}})
            target, errors = export("lion_and_mouse_v6", timing_file, root=root,
                                    word_timing_file=word_file)
            self.assertFalse(errors)
            self.assertEqual(target, (folder / "runtime_plan.json").resolve())

    def test_native_image_symlink_cannot_escape_v6_namespace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, keys = _fixture(root)
            frame = root / keys["images"][0]["candidate_path"]
            outside = root / "character/characters/lion_and_mouse_v5/legacy.png"
            outside.parent.mkdir(parents=True)
            outside.write_bytes(frame.read_bytes())
            frame.unlink()
            frame.symlink_to(outside)
            _, errors = preflight(root=root)
            self.assertTrue(any("resolves outside native story namespace" in error for error in errors))

    def test_unapproved_shared_boundary_is_not_exportable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder, keys = _fixture(root)
            digest = hashlib.sha256(b"synthetic WAV bytes").hexdigest()
            source = root / "work/the_lion_and_the_mouse/lines/S02-L001.wav"
            runtime_line = root / "work/stories/lion_and_mouse_v6/audio/en/lines/S02-L001.wav"
            scene_wav = root / "work/stories/lion_and_mouse_v6/audio/en/scene02.wav"
            for path in (source, runtime_line, scene_wav):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"synthetic WAV bytes")
            audio = json.loads((folder / "audio_manifest.json").read_text())
            audio["lines"].append({"id": "S02-L001", "scene": 2, "speaker": "NARRATOR",
                                   "duration_seconds": 0.8,
                                   "source_path": "work/the_lion_and_the_mouse/lines/S02-L001.wav",
                                   "v6_path": "work/stories/lion_and_mouse_v6/audio/en/lines/S02-L001.wav",
                                   "sha256": digest})
            audio["scenes"].append({"scene": 2,
                                    "path": "work/stories/lion_and_mouse_v6/audio/en/scene02.wav",
                                    "duration_seconds": 1, "sha256": digest})
            audio["line_count"] = 2
            audio["scene_count"] = 2
            _write(folder / "audio_manifest.json", audio)
            coverage = json.loads((folder / "dialogue_coverage.json").read_text())
            coverage["lines"].append({"id": "S02-L001", "scene": 2,
                                      "speaker": "NARRATOR",
                                      "audio_path": audio["lines"][-1]["v6_path"],
                                      "audio_sha256": digest})
            _write(folder / "dialogue_coverage.json", coverage)
            image = keys["images"][0].copy()
            image.update({"id": "s02_p01", "scene": 2,
                          "candidate_path": "character/characters/lion_and_mouse_v6/interactions/keyframes/s02_p01.png",
                          "audio_line_ids": ["S02-L001"]})
            (root / image["candidate_path"]).write_bytes(b"PNG frame one")
            keys["images"].append(image)
            keys["keyframe_count"] = 3
            _write(folder / "keyframe_plan.json", keys)
            config = json.loads((folder / "video_boundary_config.json").read_text())
            config["shared_entries"] = {"2": 1}
            _write(folder / "video_boundary_config.json", config)
            boundaries = build(keys, config)
            self.assertEqual(boundaries["scenes"][1]["start_keyframe"], "s01_p02")
            _write(folder / "video_boundary_plan.json", boundaries)
            reviews = json.loads((folder / "keyframe_visual_reviews.json").read_text())
            reviews["images"]["s02_p01"] = reviews["images"]["s01_p01"].copy()
            del reviews["images"]["s01_p02"]
            _write(folder / "keyframe_visual_reviews.json", reviews)
            _, errors = preflight(root=root)
            self.assertTrue(any("s01_p02: no full-resolution visual review" in error
                                for error in errors))
