# Helper contracts and limitations

## These are new proposal schemas

The JSON templates in this package are for a proposed Blender layer. They are **not drop-in replacements** for the repository's existing v6 keyframe, review or runtime schemas. Do not overwrite current story files with them. A later adapter requires explicit design and regression tests.

Templates intentionally contain missing hashes, pending decisions and a zero spend cap. They must fail readiness checks until actual inputs and evidence exist. Filling values is a recording operation, not permission to invent owner approval. The supplied validators verify declared metadata and bytes, not the identity or authority of the person entering the fields.

## Commands

From the skill directory, with paths adapted to actual files:

```bash
python3 scripts/context_snapshot.py --root REPO --story lion_and_mouse_v6 --out NEW_CONTEXT.json
python3 scripts/preflight.py asset ASSET.json --root REPO
python3 scripts/preflight.py asset ASSET.json --root REPO --require-approved
python3 scripts/preflight.py fingerprint ASSET.json --exclude review
python3 scripts/preflight.py job JOB.json --root REPO --ledger LEDGER.json
python3 scripts/preflight.py chain CHAIN.json
python3 scripts/ambient_motion.py --id grass_tip_01 --frame 120 --period 8 --amplitude 0.01
python3 scripts/contact_sheet.py FRONT.png SIDE.png REAR.png --out NEW_SHEET.png
```

The example ambient amplitude/period are arbitrary diagnostic inputs, not recommended canonical wind values. File outputs are exclusive-create: choose a new path rather than overwriting. The contact sheet is not color-managed and is for navigation/composition, not precise color acceptance.

## Asset manifest

Use `feltwillow.blender.asset.v1`; name asset ID, kind, candidate path/hash, source bindings and design intent. Character manifests require an explicit anatomy profile, semantic appendage list, locomotion capabilities and positive neutral anatomical measurement. A limbless design may have an empty appendage list. No universal animal limb count is imposed.

Environment manifests require a camera envelope and support surface inventory. The validator verifies presence/type, not that the envelope is correctly calibrated or the surfaces support weight. Detailed geometry, 2.5D limits and interaction reviews remain in the environment contract and evidence.

With `--require-approved`, check a recorded approved decision, reviewer/date, spec fingerprint, evidence files and kind-specific check fields. This is a freshness/record-completeness gate, not a way to acquire approval. Source files and evidence bytes are hashed; changes invalidate matching records. An evidence file can contain an incorrect human judgment, which the helper cannot detect.

`fingerprint --exclude review` hashes canonical JSON with sorted keys and compact separators, excluding the top-level review. Generate the fingerprint for the finalized candidate specification, then record the actual review against it. Changes to the candidate or source bindings need a new review. Do not use a fingerprint to imply visual correctness.

## Paid request manifest

Use `feltwillow.blender.job.v1`. Bind provider, endpoint, settings, input file hashes and requested submission count. Quote `maximum_usd` is the **total upper estimate for this whole approved operation**, including all listed requests and options, not the unit price. Include a pricing source, timezone-aware quote time and validity window. The helper allows a stated window up to 168 hours; the default template uses 24 hours. This is a proposed policy, not a provider price guarantee.

Approval binds the entire request except the approval block. Record actual owner consent, not a fabricated `approved` string. The budget ledger counts unresolved reserved/submitted/unknown jobs at their maximum and settled jobs at actual cost. A timeout remains unknown; polling a request is different from another submission. Reusing an already-recorded job requires investigation, not silent resubmission.

**Limit:** these scripts neither reserve atomically nor intercept remote calls. They are advisory preflight. Real multi-agent automation requires a single submission gateway with locking, validated approval binding, idempotency, permission controls and accounting. An agent with direct fal access can bypass a prompt-only procedure; do not advertise this package as preventing that.

## Chain manifest

Use positive rational FPS and half-open global frame intervals. Declare start/end snapshots with exact environment, camera, lighting and render-setting signatures, asset hashes, actors, props, ambient parameters and velocities. Each actor requires a 16-number world root matrix plus pose signature; velocity data includes linear/angular vectors and a pose-velocity signature.

These signatures must come from complete evaluated state or a deliberately defined canonical state serialization; do not hash merely an object's name. The validator checks completeness of its small declared schema, finite values and exact equality at a continuous join. It does not interrogate Blender, understand arbitrary event graphs or prove collision/pixel correctness. A cut needs a reason; changed prop state across a cut needs an explicit event entry. Review event legitimacy independently.

Implement tolerances/quantization in a future state extractor with documented precision, rather than relaxing the equality gate ad hoc. Camera exposure, visibility, constraints and simulation state not represented by a signature can still change the result. Include those in the extractor's state definition and tests.

## Context and Blender inventory

`context_snapshot.py` reads a small explicit list of repository documents, source paths and hashes; it does not scan user home credentials or read every file. It reports Git status names, not diff contents. An unpushed Blender directory is not ignored simply because the remote snapshot lacked one.

`blender_inspect.py` runs inside Blender and inventories object hierarchy, meshes, rigs, cameras, image paths, linked libraries, scene/color settings and embedded text-block names. It does not execute embedded code, save the scene, audit all topology, measure anatomy, or validate deformation. Safe loading should disable automatic script execution. The helper has not been tested with `bpy` in this release; validate it against the installed Blender on a disposable file before use.

## Schema evolution

Keep schema version changes explicit. Add tested fields when a real pilot needs them, and write adapters rather than silently breaking old assets. Retain failed examples as regression fixtures. Maintain separate owner selection and technical readiness in any production integration, matching the current repository's distinction.

## Environment comparison helper (1.1.0)

This is separate from production preflight; no existing story schema is replaced.

```bash
python3 scripts/scene_match.py --reference APPROVED_DISPLAY.png \
  --render NEW_RENDER_DISPLAY.png --out-dir NEW_REVIEW_DIRECTORY \
  --assume-srgb
```

Use `--assume-srgb` only when the untagged exports are known to be sRGB display images. Embedded ICC profiles are converted to sRGB; raw EXR, transparent images, unsupported modes and unequal sizes are refused. There is no auto-crop, warp or histogram matching. The output includes native-size overlay/split/difference images and `report.json`; the side-by-side adds labels but does not resample the source panels.

For manually measured correspondences add `--landmarks FILLED_LANDMARKS.json`, based on `assets/templates/scene-match-landmarks.json`. Bind exact input file hashes. Coordinates use top-left normalized pixel centers: (0,0) is the first center and (1,1) the last. Pixel offsets therefore scale by width-1 and height-1. Unobserved positions remain null and are counted as unmeasured. Uncertainty is recorded text, not modeled statistically. The helper does not identify objects, solve a camera, validate the frame's artistic quality or fill approval fields.

Do not apply `preflight.py asset` to a landmark or comparison report. Follow the explicit per-domain CLI/schema and keep proposed Blender records separate from current production contracts.

## Environment direction and material evidence (1.2.0)

`environment-direction.json` is a task-scoped design brief, not a replacement for production staging. `scripts/environment_direction.py` checks explicit mode, preserved invariants, legacy-output protection and non-automatic approval. It never assesses visual quality or authenticates owner consent. `scripts/blender_material_audit.py` records material graphs and image bindings inside Blender without changing them; upstream connections are potential contributions, not visibility or provider proof.

## External asset record (1.3.0)

`assets/templates/external-asset-record.json` proposes schema `feltwillow.external-asset.v1`. Use it only if the repository has no equivalent registry; otherwise map these fields into that registry. `origin.evidence`, `files.originals` and `files.derivatives` contain `{path, sha256}` entries relative to the supplied root. File existence and hashes can be checked offline with `scripts/asset_intake.py RECORD --root REPO --intent research|local_test|public_bundle`.

Research permits documented unknown rights, not unbounded downloads. Local-test intent requires recorded commercial/modification permission, rights evidence, resolved conditions, credit handling and safe automatic-execution settings. Public-bundle intent additionally checks raw/embedded source-redistribution declarations and dependency review. The checker never decides whether statements in a record are true, reads license meaning, opens .blend content, contacts providers or authorizes publication. A true metadata_ok and false production_approved are intentional.

Use stable HTTPS asset/license page URLs without credentials or query tokens; put necessary query-based source identifiers in a separate non-secret note and use a canonical landing URL for the record. Keep pending templates pending until actual evidence exists.
