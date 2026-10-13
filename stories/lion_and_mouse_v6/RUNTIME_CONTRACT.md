# v6 keyframe runtime contract

This story uses `visual_bible.json` pipeline `keyframe_boundary_v1`. The tracked
`audio_manifest.json`, `dialogue_coverage.json`, `keyframe_plan.json`,
`keyframe_visual_reviews.json`, `video_boundary_config.json`, and
`video_boundary_plan.json` are its inputs. It does not have a
`prompt_manifest.json`, legacy `timing_plan.json`, or renderable `story.yaml`.

Run the read-only preflight from the repository root:

```bash
python3 production/v6_runtime.py --story lion_and_mouse_v6 --preflight
```

Current active candidates deliberately fail the full-resolution visual review
gate. The reference gate also remains blocked while required Milo/anchor/prop
approvals are pending and historical source bytes are unavailable. The two
recorded rejected r01 hashes, `s14_p04` and `s14_p05`, remain in the rejection
ledger; new r02 image bytes are the active unapproved candidates. Do not fill
review records without inspection. See [`../../docs/keyframe-regeneration.md`](../../docs/keyframe-regeneration.md)
for source authority and regeneration rules.
The preflight also checks story/pipeline identity, native asset paths and
symlink containment, boundary-plan freshness, audio namespace/provenance, and
all locally present audio hashes. With `FELTWILLOW_WORK` set, `work/` audio paths
resolve beneath that directory. Missing ignored audio is tolerated by the
read-only preflight; export requires the local bytes.

After every referenced image has a current hash-bound visual approval, author
an explicit timing file with schema `feltwillow.video-piece-timing.v1`:

```json
{
  "schema": "feltwillow.video-piece-timing.v1",
  "story": "lion_and_mouse_v6",
  "pieces": [
    {
      "scene": 1,
      "start_seconds": 0.0,
      "end_seconds": 9.28,
      "start_keyframe": "s01_p01",
      "end_keyframe": "s01_p01",
      "audio_line_ids": ["S01-L001"],
      "mouth_mode": "silent"
    }
  ]
}
```

That is only an **illustrative single piece**, not a complete or approved
timing plan. All pieces together must cover each scene WAV without gaps or
overlaps, include every audio line and keyframe, start/end at registered scene
boundaries, and follow the registered transition order. A piece may hold one
image or move between the two endpoints of a registered same-view/shared
transition. Camera/location cuts occur between adjacent pieces; an
unregistered same-view jump is rejected. `mouth_mode` is `silent` for narration
and silent acting, or `character_dialogue` only for a piece containing one
character speaker and no narrator speech. Piece line IDs must match the
spoken intervals, reconstructed from tracked line durations and assembly
pauses. Every character dialogue line needs a lip-sync piece, and the speaker
must be staged at both endpoints of that piece.

A piece boundary inside a spoken line needs reviewed word-timing evidence.
The optional `--word-timing` file uses schema
`feltwillow.reviewed-word-timing.v1` and binds anchors to a scene WAV hash:

```json
{
  "schema": "feltwillow.reviewed-word-timing.v1",
  "story": "lion_and_mouse_v6",
  "scenes": {
    "1": {
      "audio_sha256": "<scene01.wav SHA-256 from audio_manifest.json>",
      "reviewer": "<person who checked the word timing>",
      "reviewed_at": "<ISO date>",
      "anchors": [
        {
          "seconds": 4.2,
          "line_id": "S01-L001",
          "word_index": 7,
          "word": "<word at the cut>"
        }
      ]
    }
  }
}
```

Anchor values above are placeholders, **not actual timing measurements**.
The adapter validates the source WAV hash, reviewer fields, and that each
inside-line piece boundary matches a recorded anchor. A reviewer must check
the actual word alignment against audio; the adapter cannot infer words from
line durations.

Only after visual review and timing are complete, run:

```bash
python3 production/v6_runtime.py --story lion_and_mouse_v6 --export \
  --timing <reviewed-video-piece-timing.json> \
  --word-timing <reviewed-word-timing.json>
```

`--word-timing` may be omitted only if every piece boundary is at a verified
whole-line edge or in a silence interval. Export validates all local v5-source
and v6-runtime line audio and all scene WAV hashes, then atomically writes
`runtime_plan.json`. It records exact endpoint paths/hashes, visual review
hashes, audio track hashes, line IDs, mouth mode, cuts, timing hash, word-timing
hash, and hashes of the tracked input documents. A failed export writes no
partial plan. This runtime plan is an input receipt; GPU rendering still needs
a separate renderer translation and a pilot validation before bulk work.
