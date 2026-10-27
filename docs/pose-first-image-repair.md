# Pose-first scene repair: S05 pilot, r003

## Purpose and existing code

Use the existing v7 performance registry as the source of the actor's anatomy and
approval status. The original selected S05 roll scene was staged with a transparent
Milo performance, uniform scale and recorded translation. The later flattened-image
redo loop created a new Milo body by generative editing and masked the surrounding
scene. Background-mask verification never certified actor anatomy or physical contact.

The existing code already supports portions of this workflow:
- `production/character_performance.py` validates performance registry and creates dry
  reference proposals; it is **not** a production renderer.
- `production/keyframe.py` and S05 historical scripts support transparent cutout
  compositing; they do **not** prove a particular scene contact is physically correct.
- `.claude/skills/consistent-image-prompts/SKILL.md` already requires performance
  references. The r003 addendum is deliberately short to avoid duplicating that skill.
- The October 27 `image_repair_s01_s08_r001/` pixel verifier checks exact exterior
  protection only, not Milo/Leo anatomy or grounding.

## Exact S05 pilot behavior

`production/pose_first_repair.py` reads S05-L009-B01-I03's sidecar and verifies:
1. the previous scene PNG matches its recorded hash;
2. the locked S05 Leo/background matches the recorded source/hash;
3. the selected `milo.tumble.flank_to_face.3q:roll` asset, exact hash and JSON
   sidecar match the live performance registry and previous S05 composition;
4. the `nose_landing` pose and canonical image match the live registry/sidecar;
5. the actual prior roll uniform scale and translation exist and are sane.

The script then composes the *whole existing RGBA nose-landing performance* onto
that same source camera with three small, documented offsets from the prior roll's
location. It never reconstructs a full Milo from a flattened scene image.

The transparent `nose_landing` performance is **not yet selected for production**.
The explicit `--allow-unreviewed-pose` flag only authorizes a review-only preview.
Without that flag, staging with this pose fails closed. The older selected roll
and scene pixels remain untouched.

The r001 pose is now recorded as an upright recovery in
`review/pose_first_s05_grounded_r002/POSE_PHASE_REVIEW.json`. A native, exact-hash
phase review is required before the older placement pilot can write any new scene
candidate; this r001 review fails that gate even with the preview flag. A new
grounded pose must receive its own visual review, then measured support/nose
landmarks. `grounded_preview` checks the two-anchor vector before using the same
whole-actor compositor for one immutable CPU preview. Its receipt keeps scene
readiness false while contact shadow, foreground overlap and owner selection
remain unreviewed. The prepared source-hash request and unmeasured anchor recipe
are under `review/pose_first_s05_grounded_r002/`.

The computed contact shadow is only an approximation based on the visible actor
bounding box, and **no Leo foreground-occlusion mask has been applied**. Correct
support, body scale, nose collision, limb attachments, shadows and motion are
human-review gates, not automated passes. If the pose itself looks wrong, repair
its transparent performance and re-review before trying a new scene composition.

## Commands: same existing branch

```bash
cd /Users/lealroja/Documents/feltwillow/feltwillow-production
git branch --show-current  # must read wan-new-image-approach
# The old ZIP runner is historical; do not reinstall or rerun it.
```

The runner adds/updates only the three pilot source/doc/test files and appends a
short block to the image-prompt skill. It recognizes exact, unmodified pilot r001
or r002 files, but refuses to overwrite other edits. It never checks out or creates
branches, uses an image model, starts Wan/GPU jobs, changes selections, or commits.

Outputs are written *atomically as a new directory* to
`stories/lion_and_mouse_v7/review/pose_first_s05_pilot_r001/`. The existing
output directory is immutable. To create a further revision manually:

```bash
python production/pose_first_repair.py --pilot-s05 --allow-unreviewed-pose \
  --phase-review /path/to/new_pose_native_visual_review.json \
  --out-dir stories/lion_and_mouse_v7/review/pose_first_s05_pilot_r002
```

Open `REVIEW.html` or `CONTACT_SHEET.jpg`; each candidate links to its native PNG.
The review page compares the previous roll with each landing. If the previous
rejected landing is present locally, it links to that too. `RECEIPTS.json`
records hashes, original scene transform, per-candidate offsets, revision and the
unselected, unverified status.

## Definition of success

- Technical: all exact hashes and registry/sidecar checks pass; no previous PNG,
  selection or index changed; 0 changed pixels outside actor/shadow support; tests
  pass; 3 review-only PNGs/receipts/gallery exist.
- Visual: the same Milo identity/limbs/head/ears/tail, coherent scale and heading,
  correct body support beside Leo's nose, no penetration or severe incorrect
  overdraw, and proper contact/shadow/occlusion at actual scene scale. Leo's four
  attached paws remain visually sound.
- Editorial: the owner explicitly approves exact resulting PNG hashes before any
  selected image ledger is rebound. Neither CPU tests nor HTML existence approves
  an image, a Wan take or a finished scene.

## Reuse and limits

The pose resolver and whole-actor compositor can be reused for other character
repairs. **Existing legacy image-generation scripts do not yet call this gate**;
adding one script does not prove global enforcement. Extending that policy across
S06/S08 requires additional integration and anatomy/camera-specific evidence.
For S08, a complete aligned four-paw Leo layer or foreleg must be approved, rather
than repeatedly trying to add an isolated paw to a flattened scene.

No provider calls, automatic retries, downloads, video output, Git writes, or
owner selections are authorized by this pilot. No real source-image quality result
can be asserted until the pilot runs on the full-resolution local assets.
