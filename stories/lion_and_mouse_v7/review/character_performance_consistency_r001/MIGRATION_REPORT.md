# V7 performance-library migration report

Implemented locally on `wan-new-image-approach`. Starting and ending HEAD: `ef2c6efb0fbf628e7da548a89f471bf4e9cb525f` (`ef2c6ef`, second iteration v7). Checkout started clean; changes remain uncommitted. No files were moved/deleted and no unrelated work was reset.

## Result and counts

- Active shot authority remains `audio_visual_plan.json`; optional per-image `performance` bindings and one shared fork staging contract were added. Canonical character records, line/beat/image IDs, sequence modes, WAV hashes/durations and all world-state/event content are unchanged (regression comparison strips only the added performance fields).
- New performance authority: `stories/lion_and_mouse_v7/character_performance_library.json`, schema `feltwillow.character-performance.v1`. Character library has a pointer; legacy empty performance slots are explicitly non-authoritative.
- 40 pose/action/portrait-base records: 17 poses, 7 locomotion families, 10 interaction families and 6 angle-specific portrait bases. 77 planned pose/action/base variants; 42 planned expression variants. All 119 are planned/null-file requirements, not a generation target.
- 179 actor-to-image assignments across 156 visible-cast image slots; environment-only slots declare no-library reason. All 98 available S01–S12 audio lines remain represented. S13–S16 retain 63 script lines with no current r001 readiness/timing.
- Zero generated performance candidates, zero approved performance variants, zero scene approvals inferred. The 24 existing scene candidates retain pending status and exact image/sidecar hashes.

## Audit conclusions

All 24 actual native PNGs were inspected, plus approved Milo identity and fork master. Four complete-frame contact sheets and a separate audio-enabled comparison page are provided. Walk compactness/head-body differences remain suspected or not comparable under unknown cameras and different gait phases; no universal pixel-height rule was introduced. S03-L004 is bound to stationary consideration before route commitment. S02-L003 is portrait inspiration only, with minimal top-ear clearance.

For S03-L006–L008, approximate root positions (±15 px) are `(720,803)`, `(878,815)`, `(749,775)` on 1672×941 canvases. These establish placement drift under the fixed-root contract; head turns confound an anatomical scale verdict. A native actor-free top ROI `[0,0,1672,200]` is not pixel-identical across candidates or master (about 99% changed pixels against master, mean channel difference roughly 5–6/255). This confirms failure of the exact-background contract, not large geographic drift. No historical observation was rewritten. See REVIEW.md, AUDIT.json and VISUAL_OBSERVATIONS.json.

## Implemented gates and limits

The validator checks exact actor/pose/expression IDs and revision/hash pins, canonical bindings, role/authority-labeled reference paths, candidate filename/sidecar/PNG/receipt facts, independent owner decision scopes, head view/orientation/portrait base, parent cycles, physical support and prop/trigger/net contact phases. Fixed fork shares one root/anatomical projection contract; pending measurements cannot masquerade as reviewed anchors. A planned pose cannot be used as approved. A performance decision never approves a scene.

Planning permits nonexistent planned files; image readiness is deliberately blocked. Leo canonical still has ledger SHA `6b587c8ee2739767bb7af056ee3176ec3d2e698a5bed0e013263814ee8059545` versus actual `1c4f773d04c5e6f7229448bfe00caf7f610d427f5dc0d145cba57e7671a59362`. Approved alpha poses, compatible expression geometry, shot measurements, contacts/shadows/occlusion and owner anchors are absent. Guided generation cannot guarantee anatomy/pixel identity. The deterministic path is a recipe plus synthetic-only CPU test, not a production compositor.

The dry-run proposal CLI has no submit/provider route. It records identity and required versioned performance references, staging/world state independently, reference limits, unknown costs and blockers. Native immutable-operation bytes remain tied to the archived pre-migration plan, not rewritten to match the new authoring file. The existing audio loader remains four-valued. V5/v6 tests/instructions remain version-local.

## Next owner-review pilot — draft only

NEXT_PERFORMANCE_PILOT.json proposes eight conditional performance requests, zero scene requests and no retries: contact + passing walking keys (2); full-ear portrait base + startled and determined variants (3); fixed-body sky/left-route/right-route gaze depictions (3). Opposite-contact gait key is deferred until a chosen endpoint needs it. Each row has the exact known Milo canonical path/hash, semantic target filename, draft prompt, transparent-background setting, proposed endpoint and dependency. Future parent hashes/paths and cost are unknown. First-stage candidates need individual review before dependent requests; this is not authorization-ready and no submission/approval request is made. Leo generation and scene repairs are deferred.

Owner review needed: select walking silhouette/head-body design; choose portrait-base angle and ear margin; confirm fixed-fork root/depth/head angles against one selected background; decide whether the suspected anatomical differences need repair. Measured camera distances must not be invented.

## Commands and results

Commands used the documented conda Python (`/Users/lealroja/miniconda3/envs/feltwillow/bin/python`):

```bash
python production/audio_visual_plan.py --story lion_and_mouse_v7 validate
python production/audio_visual_plan.py --story lion_and_mouse_v7 derive
python production/audio_visual_plan.py --story lion_and_mouse_v7 readiness --gate planning
python production/character_performance.py --story lion_and_mouse_v7 validate
python production/character_performance.py --story lion_and_mouse_v7 derive
python production/character_performance.py --story lion_and_mouse_v7 audit --review s01_s03_r001
python production/character_performance.py --story lion_and_mouse_v7 proposal --image-id S01-L001-B01-I02
python production/character_performance.py --story lion_and_mouse_v7 pilot
python production/character_performance.py --story lion_and_mouse_v7 validate --gate image
python -m unittest discover -s tests -q
python production/check_markdown_links.py
git diff --check
```

All planning/derive checks pass. Image readiness exits 1 as intended; image-readiness.log lists blockers. All 186 CPU tests pass (unit-tests.log), including v5/v6 behavior, synthetic alpha composition/protected pixels, performance validation, audio coverage, local gallery/media access and path security. Both repo skills validate; Markdown links and whitespace checks pass. Socket tests ran outside the socket-restricted sandbox using loopback only. Actual localhost HEAD checks returned HTML 200, WAV range 206 and unlisted repository file 404.

## Review access

The new comparison page is running on `http://127.0.0.1:8765/`; its link opens the unchanged original gallery. Restart with `python production/serve_scene_review.py --gallery performance`. Both pages retain original full-line WAV playback. The server allowlist is explicit and remains loopback-only. Browser verdict controls are unsaved placeholders, not owner decisions.

## Hash evidence

VERIFICATION.json lists before/after SHA-256 for every protected source and both changed authored files. BEFORE.json and before_audio_visual_plan.json / before_character_library.json preserve the initial revision. All protected sources, including 24 original PNGs, 24 sidecars, receipts, original batch operation/authorization and original gallery, are byte-unchanged. No generation, image-editing service, audio synthesis, video/GPU job, paid request, asset download/upload or remote publication occurred. Contact sheets use only existing raster bytes and synthetic tests use temporary fixture images.

## Created paths

- `docs/character-performance-library.md`
- `production/character_performance.py`
- `production/character_performance_audit.py`
- `stories/lion_and_mouse_v7/character_performance_library.json`
- `stories/lion_and_mouse_v7/derived/AUDIO_PERFORMANCE_INDEX.md`
- `stories/lion_and_mouse_v7/derived/PERFORMANCE_REQUIREMENTS.md`
- `stories/lion_and_mouse_v7/derived/performance_usage.json`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/AUDIT.json`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/BEFORE.json`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/MIGRATION_REPORT.md`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/NEXT_PERFORMANCE_PILOT.json`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/REVIEW.md`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/S01-L001-B01-I02_DRY_PROPOSAL.json`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/VERIFICATION.json`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/VISUAL_OBSERVATIONS.json`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/audio-validate.json`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/before_audio_visual_plan.json`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/before_character_library.json`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/before_location_library.json`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/image-readiness.log`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/planning-readiness.json`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/review.html`
- `stories/lion_and_mouse_v7/review/character_performance_consistency_r001/unit-tests.log`
- `tests/test_character_performance.py`

## Changed paths

- `.claude/skills/audio-chained-coverage/SKILL.md`
- `.claude/skills/consistent-image-prompts/SKILL.md`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/audio-line-visual-workflow.md`
- `docs/audio-linked-image-naming.md`
- `docs/scene-continuity-policy.md`
- `production/audio_visual_plan.py`
- `production/serve_scene_review.py`
- `stories/lion_and_mouse_v7/CHARACTER_STAGING.md`
- `stories/lion_and_mouse_v7/README.md`
- `stories/lion_and_mouse_v7/SOURCE_OF_TRUTH.md`
- `stories/lion_and_mouse_v7/audio_visual_plan.json`
- `stories/lion_and_mouse_v7/character_library.json`
- `stories/lion_and_mouse_v7/derived/audio_visual_summary.json`
- `tests/test_audio_visual_plan.py`
