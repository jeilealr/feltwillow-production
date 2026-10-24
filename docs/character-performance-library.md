# V7 character performance library

The active image-first route remains approved images → reviewed Wan clips. The [audio-visual plan](../stories/lion_and_mouse_v7/audio_visual_plan.json) owns story shots; [character_performance_library.json](../stories/lion_and_mouse_v7/character_performance_library.json), schema `feltwillow.character-performance.v1`, owns versioned performance requirements. The migration initially authored requirements only. A subsequent authorized three-request pass produced Milo walking, neutral portrait-base and upward-gaze candidates; all remain pending owner review. Blender, rigs, LoRA and historical fox experiments are separate, optional research.

See the [canonical-first, character-specific ratio framework](character-proportion-framework.md) for separate Milo/Leo metric definitions, articulated limb chains, portrait ratios, uncertainty and calibration. The reusable `production/performance_review_gallery.py` preserves the owner-preferred card/audio HTML layout. Active numerical targets live only in the performance registry, not in a second shot plan.

## Authorities and lifecycle

### Body proportions and prop fit — current owner review

The [Milo anatomy audit](../stories/lion_and_mouse_v7/review/character_performance_consistency_r001/milo_anatomy_r001/REVIEW.md) records owner acceptance of the current poses/acting with anatomy congruence and acorn fit still conditional. The acorn-holding and berry-harvesting images have a suspected projected head/torso mismatch; head pitch differs and camera metadata is unknown. Neither equal PNG dimensions nor equal actor height proves equal anatomy. Approximate annotated screening measurements are not production ratio thresholds.

`character_performance_library.json` owns `anatomy_policies.Milo` and per-variant `anatomy_review`. Preserve canonical identity; compare compatible views against the exact owner-preferred berry proportion reference. Image readiness and dry proposals block missing anatomy review even when the depiction is owner-selected. A matched review must bind current image/reference hashes and a comparison method/evidence file. Technical use blockers, such as the left-route body's unwanted turn, persist after pose approval. This validator checks evidence consistency; it cannot infer anatomy or authenticate an artistic verdict automatically.

Use uniform whole-actor scale for scene staging, never separate head/torso/hand resizing. Portraits and independent shots may vary in apparent size; fixed camera/depth sequences share root, scale and anatomical projection. Reference guidance may redraw anatomy; reviewed transparent layers preserve their anatomy under uniform transforms, while new perspectives/actions require new comparison. Keep neck/chest visibility, skull/ear ratios, articulated limb lengths and contacts in the review.

Empty grip spaces are not a prop-fit pass. Bind one approved acorn design/hash and a consistent size relative to Milo, then check supported grip, hand occlusion and held/placed custody across action phases. No automatic prop creation or independent prop resizing is authorized by this policy.

| Authority | Controls | Does not grant |
|---|---|---|
| Character canonical | Identity, anatomy/proportions, felt material, intrinsic palette | Pose, scene, camera or video approval |
| Performance record / variant | Depiction of pose/action, compatible view, head angle, gait/contact or expression | Universal screen size, world-state changes or scene approval |
| Audio-visual plan | Beat meaning, world state, key images, per-actor performance assignment | Generated files or implicit continuity |
| Location / shot staging | Geography, explicit background lock, camera, depth, placement, root/contact, scale, shadow and occlusion | Permission to redraw anatomy |
| Owner decision ledger | Exact hash/revision/variant and stated approval scope | Approval of other bytes or a finished scene |

Each semantic asset has a stable ID, revision, actor, family, view/body facing/head orientation, reference authorities and named variants. A walk family uses distinct contact, passing and opposite-contact keys; a still stamp is not a walk animation. Only the minimum keys needed for chosen endpoints should be produced later. A one-off berry reach or tumble interaction still requires anatomy, provenance and review.

Variant lifecycle is `planned` → `candidate_pending_owner_review` → `owner_selected_for_performance` / `approved_for_scene_use`. Both reviewed states mean **performance use only**; scene selection is a separate decision. Planned variants have null files/creation/owner decisions. Real candidates need a semantic filename, exact PNG hash/dimensions/alpha facts, matching JSON sidecar, immutable creation receipt, ordered role/authority-labeled source hashes, prompt/settings and an independent hash-bound owner ledger for reviewed status. A generated file is never automatically approved. The validator cannot authenticate a human's identity cryptographically; it checks the explicit scoped ledger against exact bytes and rejects missing, inconsistent or fabricated approval fields.

Milo's approved v7 canonical remains untouched. Old v6 expression boards/atlases are not imported; they need identity refresh and revalidation. Existing v7 scene crops are inspiration only. Leo requirements stay planned because his canonical ledger hash differs from actual local bytes; this migration preserves and reports that blocker.

## Shot bindings and camera-relative size

Every current key-image placeholder binds each visible actor under `performance`. Bindings name pose/variant and compatible expression/variant; view, body facing, head orientation, support and world-state reference are explicit. Environment-only images use an empty map and `no_library_pose_needed` reason. Exact line/beat/image IDs, audio hashes/timing, state events and sequence modes remain unchanged. S13–S16 have no current r001 audio and no invented performance readiness.

`performance_staging_contracts` in the same plan owns the shared fork camera/depth/root/anatomical projection. S03-L006–L008 points to one contract; an expression change cannot resize Milo's head/body or move his planted root. Measurements and anchor approval are pending. Coarse inherited world-state `pose`/`anchor` labels are narrative bookkeeping, not measured pixel staging; acorn custody and causal events remain authoritative. For example, the inherited label `standing_holding_acorn` later persists after the acorn-release event; the stationary fork performance must use the actual prop-owner state, not recreate a held acorn from that label.

Independent wide/medium/portrait shots may have different screen sizes. Compare anatomy at compatible angles and account for camera distance, lens/zoom, crop, depth and pose. Use `camera_unknown` with null measurements when unmeasured. A changed bounding box alone cannot prove anatomical drift. Gait flexion and head turns change projected extents; the strict fork contract still requires one shared root and calibrated anatomy. No camera-specific pixel height belongs in reusable pose identity.

Expressions are angle-registered full-head/upper-chest variants tied to the portrait-base revision; an optional facial overlay needs a separate narrow alignment/support contract. Do not paste a whole new face onto a different head silhouette, resize ears, introduce teeth or create mask halos. Narrator never drives mouth animation. Spoken dialogue keeps closed still boundaries and uses the later explicit lip-sync pipeline.

## Two realization strategies

**Performance-guided complete scene:** use ordered canonical identity → reviewed pose → compatible expression → explicitly required selected location/plate → approved prop design → edit base for an authorized edit. Each reference carries its ID/revision/hash and allowed property. A style-only location reference does not impose geography. A provider's reference limit must be declared; missing critical references block readiness rather than being silently dropped. Guidance can redraw anatomy, so native-resolution visual comparison is mandatory.

**Deterministic layers for strict continuity:** propose a reviewed transparent actor layer, uniform camera-relative scale/translation, source/target root contact, selected background, explicit occlusion and contact-shadow support. Background pixels outside those supports must remain identical. Perspective projection, wool-edge blending, lighting, face alignment and shadows require review. Any later finishing step gets its own narrowly bounded proposal; it may not repaint identity or recreate protected background freely.

`compose_synthetic_pilot` is a tiny CPU proof using synthetic RGBA test images only: positive uniform scale/translation, checked root mapping and a returned exact alpha support mask. Tests confirm protected pixels are unchanged. The CLI never produces production composites; actual assets, perspective/contact/shadow/occlusion review and finishing authorization are absent. This is deliberately a validated recipe contract, not a new compositor or a claim that every interaction is an alpha paste.

## Commands and readiness

Use `/Users/lealroja/miniconda3/envs/feltwillow/bin/python` (or activate `feltwillow` first):

```bash
python production/character_performance.py --story lion_and_mouse_v7 validate
python production/character_performance.py --story lion_and_mouse_v7 derive
python production/character_performance.py --story lion_and_mouse_v7 audit --review s01_s03_r001
python production/character_performance.py --story lion_and_mouse_v7 proposal --image-id S01-L001-B01-I02
python production/character_performance.py --story lion_and_mouse_v7 pilot
python production/character_performance.py --story lion_and_mouse_v7 validate --gate image
```

Planning passes with planned/null assets. Image readiness blocks missing or unreviewed required variants, changed files, Leo canonical mismatch and unresolved strict staging anchors. The existing audio validator also checks performance planning and includes performance image-readiness blockers; its four-value `load` interface is unchanged. It derives [requirements](../stories/lion_and_mouse_v7/derived/PERFORMANCE_REQUIREMENTS.md), [audio/performance index](../stories/lion_and_mouse_v7/derived/AUDIO_PERFORMANCE_INDEX.md) and `performance_usage.json`. Reuse/impact counts come from actual plan assignments; no manually maintained duplicate used-by list or duplicate pose PNGs.

`proposal` and `pilot` print JSON only. They have no provider client or submit path. Proposals include reference requirements, source/plan hashes, independent staging, sidecar contract, costs explicitly unknown and blockers. They cannot authorize generation. The eight-request pilot draft covers two walking keys, one full-ear portrait base plus two expressions, and three fixed-body fork gaze variants. Dependencies require real source hashes and owner review before a later concrete generation proposal can be approved; it is not a batch authorization.

## Read-only consistency review

[Audit and evidence](../stories/lion_and_mouse_v7/review/character_performance_consistency_r001/REVIEW.md) records all 24 native PNG inspections, before hashes, uncertainty, approximate landmarks and background pixel metrics. Contact sheets contain existing images only. Original image/sidecar/operation/receipt bytes remain unchanged; new review observations are appended separately. Exact pixel failure does not automatically prove perceptual geometry or anatomical failure.

For the separate audio-enabled comparison gallery:

```bash
python production/serve_scene_review.py --gallery performance
```

Open `http://127.0.0.1:8765/` in VS Code's browser. The server binds loopback and serves only the explicitly allowed galleries and referenced media, with WAV byte ranges for seeking. Original gallery and full-line recordings remain available. Native-size and approximate landmark overlays aid review; unsaved browser verdict controls do not write approval ledgers.

Current generated candidates: [Milo foundation review](../stories/lion_and_mouse_v7/review/character_performance_consistency_r001/milo_foundations_r001/REVIEW.md). Exact approved prompts/inputs/settings are preserved in its OPERATION.json; cost remains unknown, with three calls and no retries.

## Local review-server operation

Use `/Users/lealroja/miniconda3/envs/feltwillow/bin/python production/serve_scene_review.py --port 8765`. The v2 server reloads registered HTML/media allowlists as gallery pages change, so routine candidate updates need no restart. Re-running the command recognises a compatible server for this checkout and prints its URL. An unrelated/older occupied port yields a short message; it never kills a process. Stop a server in its own terminal with Ctrl+C; updated servers exit cleanly. Loopback binding tests need sandbox network permission; rerun with tool escalation when denied rather than changing Python or skipping tests. `measured_anatomy_pass: false` and unknown cost are honest review/provenance fields, not execution failures.

### Matching prepared performances must be used

Before composing a v7 actor, find the best matching existing pose/action phase and expression. A compatible reviewed pose is the depicted body reference, not optional stylistic inspiration. Put its exact revision/path/hash and property role in both the binding and actual submitted references; verify it remains attached after reference limits. Canonical still owns identity, materials and intrinsic colors (including paws); shot staging owns scale, depth, lighting and contact. If view/support differ, record why reuse is incompatible and propose a local variant. Do not silently redraw a new body or force a mismatched pose.

A supplied reference does not prove reuse: inspect the result against it for hip/limb connections, paw construction/color, torso/head proportions and cream-patch boundaries. Visible drift blocks scene acceptance even when the face is liked. Preserve the scope of face-only feedback. Repair defective performance bytes in a new revision before scene use; keep earlier files/receipts. For anatomy or exact-background locks, prefer reviewed transparent layers with uniform whole-actor transforms and explicit occlusion/contact/shadow staging; any generative finishing must be bounded and checked for drift. Pose reuse never implies identical placement across unrelated shots or automatic continuity.
