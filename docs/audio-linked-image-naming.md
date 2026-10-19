# Audio-linked image naming

This is the standard for new v7 images and future audio-line-driven stories. Every new story image starts with its exact audio-line and beat ID. The filename is the quick human connection; a same-basename JSON sidecar and derived audio/image index provide exact provenance and all reuse associations.

## Filenames

Location-view candidate:

```text
S01-L002-B01_location_berry_world_r001_candidate.png
```

Planned scene key-image candidate:

```text
S01-L002-B03-I01_start_winding_path_r001_candidate.png
S01-L002-B03-I02_end_winding_path_r001_candidate.png
```

- `S01-L002` matches `S01-L002.wav` and `S01-L002.json` in the active audio revision.
- `B01` is the stable authored visual beat within that line. `I01` identifies an actual planned key image; empty location views have no invented key-image ID.
- Role is `location` for a background view; scene image roles are `single`, `start`, `key`, or `end`.
- Subject is a short lowercase underscore slug.
- `r001` is the **image** revision. The sidecar separately records the audio revision. A new image revision gets a new filename; never overwrite existing bytes.
- `_candidate` describes its original generation status. Later selection/approval is hash-bound metadata; do not rename immutable files merely to make their name say approved.

Use `production.audio_visual_plan.image_filename(beat_id, subject, revision, image_id=..., role=...)` to construct names. Location candidates are validated against this helper during normal plan validation. Paths remain under the relevant story/character/location folders; the audio itself is not copied into image folders.

## Same-basename sidecar

Each generated file has a JSON file with the same basename, for example `S01-L002-B01_location_berry_world_r001_candidate.json`. Record:

- Story association through beat/view IDs, primary beat, all used-by beats, and all audio-line links.
- Active audio revision, exact WAV and line-metadata paths, and their SHA-256 hashes.
- Image revision, role, path, dimensions and SHA-256.
- Exact submitted prompt, tool/endpoint, input reference paths/hashes and generation receipt.
- Model, seed, request ID and actual cost only when exposed; otherwise null/explicitly unknown.
- Candidate/selection/owner-review status without inventing approvals.

The validator checks candidate names, primary beat, all audio associations, sidecar basename, image/sidecar hashes and sidecar bindings. Actual WAV/metadata truth is checked by the normal audio validator.

## Shared images and existing canon

A reusable location view or deliberately shared key image keeps one physical file. Name it after its primary/first authored beat; record every subsequent use in the library, sidecar and derived index. A new use requires updating associations and provenance, not duplicating pixels or silently relabelling the file as belonging exclusively to another line.

Keep approved character canonicals and existing location-master filenames unchanged. This naming rule applies to new story-linked outputs. For an owner-requested rename of an unselected candidate, preserve image bytes and hashes, update all live references, and retain old/new paths and the reason in its receipt. Never rewrite the original submitted prompt or approved operation to describe a later naming choice.

## Finding the connection

Run `python production/audio_visual_plan.py --story lion_and_mouse_v7 derive`. Open [the audio/image index](../stories/lion_and_mouse_v7/derived/AUDIO_IMAGE_INDEX.md) for audio → beat → actual file, or the [full visual inventory](../stories/lion_and_mouse_v7/derived/AUDIO_VISUAL_INVENTORY.md) for planned and generated coverage. The JSON index is derived, not a second authored plan.
