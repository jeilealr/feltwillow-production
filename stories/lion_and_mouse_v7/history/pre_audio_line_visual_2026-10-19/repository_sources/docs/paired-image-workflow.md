# Paired-image workflow

V7 uses `paired_keyframes_v1`; v6 remains on its existing runtime and approval contracts. The active route is approved 2D references → compatible start/end images → separately authorized Wan trials. No Blender/model download is needed.

## Authority and gates

Edit `character_library.json` (identity imports, anatomy and reviewed pose/view calibrations), `location_library.json` (physical places, lighting variants, fixed setups and measured support zones), and `shot_plan.json` (persistent states, pieces, audio coverage and causal events). Keep script text and recordings unchanged. `derived/` is reproducible output, never a competing staging authority.

Run from the repository root in the `feltwillow` conda environment:

```bash
python production/paired_images.py --story lion_and_mouse_v7 validate
python production/paired_images.py --story lion_and_mouse_v7 readiness --gate source
python production/paired_images.py --story lion_and_mouse_v7 readiness --gate image
python production/paired_images.py --story lion_and_mouse_v7 derive
python production/paired_review.py --story lion_and_mouse_v7 --out stories/lion_and_mouse_v7/review/paired/sequence
python production/v7_runtime.py --story lion_and_mouse_v7 --preflight
```

Structural validation verifies interval coverage, fixed setup references, shared endpoints, camera-cut state continuity, offscreen props and story-data event prerequisites. Source readiness checks exact canonical/plate bytes independently of audio. Image readiness also requires reviewed support/axis/setup foundations and pose calibrations. Video readiness additionally needs restored, verified audio, reviewed timing, current visual/owner evidence and dialogue preparation. A gate failure can mean missing evidence; it does not automatically diagnose a visible image defect.

The provisional plan partitions copied playback spans, including pauses and tails. Equal provisional action windows are **not** word alignment or reviewed acting timing. Restore exact WAVs, align and review the action boundaries, then adjust piece intervals. Do not render the provisional windows as if they were final direction. Narrator voice-over never drives lips. Dialogue requires one visible assigned speaker, reviewed speech calibration, timed processing and playback review.

## Foundation and construction

Start a foundation candidate from exact canonical and plate bytes. The candidate does not need to approve itself. Review a neutral shared-scale chart, minimum pose/expression views, native crop resolution, visible silhouettes, landmarks, axis, walkable support polygons and contact anchors together. Only the owner grants the corresponding scope. Existing canonical identity approval excludes new poses, measured scale anchors, scenes and video.

`pose_calibrations.<id>` records `source` (path/hash/status), `status`, `kind`, `neutral_equivalent_source_px` and `source_support_px`. A combined group also needs member-level `internal_scale_reviewed` evidence. Pose landmarks must be view aware. Neutral anatomical size is distinct from visible alpha-box height. A lying or crouching character keeps the same underlying anatomy; it is never stretched to standing silhouette height.

A setup owns `crop_rect_norm`, `output_size`, `lighting`, `plate`, `support_zones`, `foundation_review`, framing and offscreen-support permission. A placement owns `neutral_equivalent_plate_px`, `support_xy_on_plate`, `support_surface`, and calibrated depth projection. Support zones use master-normalized `[left, top, right, bottom]` bounds; ground support is resolved before cropping. Intentional portraits may crop away feet without moving the actor. A depth scale other than one needs a reviewed depth calibration ID.

`production/keyframe.py --paired-recipe RECIPE.json --out NEW.png` resolves approved calibration sources, composes z-ordered RGBA layers over a fresh clean plate, and applies one shared camera/output transform. Props, shadows and occluders are explicit layers. It does not invent per-paw shadows, segment an unreviewed matte or automatically harmonize pigment. Use a reviewed premultiplied-alpha source and explicit contact/cast-shadow layers, including airborne support rules. The old v7 bbox-sizing compositor is retained solely in the migration history; active wrappers reject it. The legacy v5/v6 path remains unchanged.

Recipe fields: `story`, `endpoint_id`, `layers`, with each layer containing `calibration_id` and `placement`. The output and receipt need a new path; they remain candidates. Keep reusable mattes, masks and sources under version-local `sources/` or the character tree, outside disposable review directories.

## Candidate registration and selection

```bash
python production/paired_images.py --story lion_and_mouse_v7 register ENDPOINT r001 IMAGE.png PROVENANCE.json
python production/paired_images.py --story lion_and_mouse_v7 select ENDPOINT r001 --expected-selection-hash CURRENT_SELECTION_SHA256
```

Provenance contains `piece_id`, `role` (`start`/`end`), exact `prompt`, `tool`, ordered references with role/path/hash, and known provider/model/settings/seed/request ID/cost values. Unknown values remain null. An end additionally records `start_sha256` and attaches that selected start first as `edit_base`. Required plate/canonical references cannot be dropped. Unapproved performance references are rejected.

Registration validates before publishing a candidate directory and receipt with one rename. Repeating the identical registration is idempotent; changed bytes or provenance require a new revision. Selection is a separate lock-protected compare-and-swap transaction. A changed selection marks affected reviews and downstream edit bases stale, preserving all old bytes and receipts. No selection grants owner approval. Do not edit immutable candidate directories or historical executed prompts.

## Pair and sequence review

```bash
python production/paired_review.py --story lion_and_mouse_v7 --piece PIECE_ID --mask-ref MASK_REFERENCE.json --geometry GEOMETRY.json --out NEW_REVIEW_DIRECTORY
```

The mask reference contains `path` and `sha256`; white/grey is approved edit support and black is protected. It must cover the union of old/new actors, justified shadows, occlusions and prop action. Restore vacated regions from the clean plate and persistent props; do not mask arbitrary drift away. The tool compares decoded RGB pixels exactly outside that support and saves full-frame start/end PNGs, a difference view, requested native detail crops, an HTML review and hash-bound report.

Geometry has `start` and `end`, each recording `setup_id`, `crop_rect_norm`, `output_size`, `lighting`, `identity_hashes`, `actors` and optional `detail_boxes_px`. Actor evidence includes `pose_calibration_id`, `support_valid`, `neutral_equivalent_plate_px`, `depth_projection_scale`, `anatomy_measurements`, `support` and `planted_contact_shadow`. Numeric evidence must come from actual inspection/calibration, never fabricated to pass a test. Review anatomy, visibility, intrinsic pigment, thin alpha edges, contacts, shadows, gaze, prop topology, readability and reachability at full resolution and delivery size. Geometry and protected-pixel checks cannot certify identity or visual quality.

Use the [pair review template](../stories/lion_and_mouse_v7/review/PAIR_REVIEW_TEMPLATE.md). Sequence pages discover pieces and endpoints from the manifest and show missing images honestly. For a shared boundary, the next start is the same asset/state/setup as the previous end. A camera cut uses another setup of the same world state; time/location cuts document travel or time and retain offscreen props. Camera moves are unsupported until a separate measured implementation exists.

## Wan handoff

`production/v7_runtime.py` is a fail-closed CPU adapter. It preserves the A14B model revision and normal/Lightning recipe pins from `feltwillow/wan.py`; it does not load weights or submit work. `paired_images.wan_inputs()` passes both `image` and `last_image` through the same spatial preprocessing. Planned target endpoints stay distinct from future actual first/last rendered frames. Review intermediate motion, lossless actual last-frame identity/state/scale, direction and velocity before continuation. Passing planned-input checks is not video approval.
