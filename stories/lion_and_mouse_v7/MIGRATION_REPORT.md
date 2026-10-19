# V7 audio-line visual migration report

This report records the initial migration before later owner shot revisions. For the current plan and counts, read [owner shot revision](OWNER_SHOT_REVISION_2026-10-19.md) and [derived inventory](derived/AUDIO_VISUAL_INVENTORY.md).

Branch `wan-new-image-approach`; starting and ending HEAD `33e65383e9d334c0b3227cf76d773480f69cfa74`. Started clean; final worktree contains unstaged, uncommitted migration changes. No unrelated branch work was reverted.

Active authored source: [audio_visual_plan.json](audio_visual_plan.json). Owner review: [chronological inventory](derived/AUDIO_VISUAL_INVENTORY.md). Detailed path/status/check records: [migration JSON](AUDIO_VISUAL_MIGRATION.json).

Current r001: 98 complete WAV/JSON pairs, S01–S12; 98 lines planned into 105 beats and 154 image slots (153 unique planned images; one explicit shared endpoint). 62 single beats, 37 pairs, 5 multi-key beats, 1 cut sequence; 7 continuity groups. Nine existing location masters preserved; 85 planned views in six existing families. No new physical location family.

S13–S16: 63 exact script lines retained, audio unavailable in r001, duration null, visual authoring/timing pending. Phrase/key timing throughout current beats awaits real alignment; no equal timing subdivisions were authored.

## Owner-directed excerpts

| Lines | Planned visual intent | Mode |
|---|---|---|
| S01-L002 | Separate stream-bank Milo-world berries → hollow log → winding path shots | single, single, pair; cuts |
| S01-L004 | Seeds under grass → berries beside stream → acorn pick-up and savoring | cut_sequence, single, multi_key (3 images) |
| S02-L003 | Startled Milo face portrait, blurred family background | single, portrait_cut |
| S03-L006–L008 | Sky → long path → shortcut gaze sequence, fork_decision group | three pairs; explicit related cuts |
| S03-L009 | Decisive Milo face portrait, separate from gaze group | single, portrait_cut |
| S05-L001–L004 | Sleeping Leo establish → mane on grass → closed eyes → paw blocking path | four singles, detail cuts; sleeping world state persists |
| S05-L009 | Support lost → airborne tumble → ground roll → nose-contact landing | multi_key, 4 images |

## Checks

- planning_validator: PASS
- audio_manifest_current_provenance: PASS: 98 available, 63 pending
- audio_archive_manifest: PASS: zero checksum errors
- audio_SHA256SUMS: PASS: 209 entries
- preserved_snapshot_hashes: PASS: 71 files
- pending_script_exact_text: PASS: all 63 lines match snapshot
- new_audio_visual_tests: PASS: 18 tests
- lightweight_input_auditor: PASS: 8 tests
- skill_validators: PASS: both skills
- compileall: PASS: feltwillow production experiments
- markdown_links: PASS
- diff_whitespace: PASS
- full_unit_suite: ----------------------------------------------------------------------
Ran 148 tests in 37.766s

OK

Image/video gates are deliberately BLOCKED: only planned placeholders/views exist, alignment and owner reviews remain pending, and Leo canonical bytes differ from the inherited approval ledger. Planning passes without future image bytes.

V5/v6 story and character assets were unchanged; legacy paired regression tests use the exact archived fixture and restored historical source bytes in isolated temporary directories. The starting suite had four failures and one error (Leo mismatch and snapshot-relative links); the final suite passes with those conditions explicitly handled, without granting artwork approval.

## Review items

- Leo actual canonical hash 1c4f773d04c5e6f7229448bfe00caf7f610d427f5dc0d145cba57e7671a59362 differs from approval ledger 6b587c8ee2739767bb7af056ee3176ec3d2e698a5bed0e013263814ee8059545; bytes and inherited scope preserved.
- All 105 semantic beats / 85 proposed views require owner plan review; no image selection or approval granted.
- S05 landing/nose contact and S06 scramble/paw contact require future staging review.
- Within-line phrase/key timing remains pending actual alignment; S13–S16 require 63 current r001 recordings before visual timing/authoring.

## New location views

All remain planned. Full family/master/camera/light/purpose/beat relationships are in location_library.json and the derived inventory.

- `stream_bank__explorer_path__afternoon`
- `stream_bank__berry_world__afternoon`
- `stream_bank__hollow_log_world__afternoon`
- `stream_bank__winding_path_world__afternoon`
- `stream_bank__farther_path__afternoon`
- `stream_bank__seed_world__afternoon`
- `stream_bank__seed_world_second_shot__afternoon`
- `stream_bank__berries_stream__afternoon`
- `stream_bank__acorn_world__afternoon`
- `stream_bank__sunset_look_up__sunset`
- `stream_bank__long_shadows__sunset`
- `stream_bank__milo_realization__sunset`
- `stream_bank__acorn_stand__sunset`
- `stream_bank__stone_acorn_placement__sunset`
- `fork__homeward_distance__sunset`
- `fork__two_routes__sunset`
- `fork__safe_left_meadow__sunset`
- `fork__short_right_route__sunset`
- `fork__shortcut_entrance__sunset`
- `fork__decision_sky__sunset`
- `fork__decision_long_path__sunset`
- `fork__decision_shortcut__sunset`
- `fork__milo_decision__sunset`
- `shortcut__shortcut_entry__dusk`
- `shortcut__mossy_stone_pass__dusk`
- `shortcut__fallen_branch_pass__dusk`
- `shortcut__stump_turn__dusk`
- `shortcut__shortcut_speed__dusk`
- `great_tree__sleeping_leo_reveal__dusk`
- `great_tree__sleeping_mane_grass__dusk`
- `great_tree__sleeping_eyes__dusk`
- `great_tree__paw_path_obstacle__dusk`
- `great_tree__root_paw_approach__dusk`
- `great_tree__milo_whoa__dusk`
- `great_tree__paw_trip_contact__dusk`
- `great_tree__tumble_roll_nose__dusk`
- `great_tree__leo_eye_opening__dusk`
- `great_tree__leo_startled_portrait__dusk`
- `great_tree__head_raise__dusk`
- `great_tree__milo_scramble_path__dusk`
- `great_tree__paw_block__dusk`
- `great_tree__milo_freeze__dusk`
- `great_tree__milo_priorities__dusk`
- `great_tree__leo_questioning__dusk`
- `great_tree__milo_apology__dusk`
- `great_tree__milo_promise__dusk`
- `great_tree__leo_looks_down__dusk`
- `great_tree__milo_trembling__dusk`
- `great_tree__power_without_threat__dusk`
- `great_tree__leo_restraint__dusk`
- `great_tree__strength_scale_bridge__dusk`
- `great_tree__leo_considers_kindness__dusk`
- `great_tree__leo_softening__dusk`
- `great_tree__leo_kind_dialogue__dusk`
- `great_tree__paw_release__dusk`
- `great_tree__milo_relief__dusk`
- `great_tree__kindness_two_shot__dusk`
- `great_tree__milo_thanks__dusk`
- `great_tree__milo_hope__dusk`
- `great_tree__sky_gesture__dusk`
- `shortcut__homeward_return__dusk`
- `shortcut__careful_feet__dusk`
- `great_tree__days_pass__day`
- `stream_bank__familiar_routines__day`
- `great_tree__daytime_rest__day`
- `trap_path__noticing_trigger__morning`
- `trap_path__hidden_trigger__morning`
- `trap_path__trigger_approach__morning`
- `trap_path__trigger_drop__morning`
- `trap_path__net_settle__morning`
- `trap_path__tug_rope_hold__morning`
- `trap_path__leo_trapped_portrait__morning`
- `trap_path__strength_under_net__morning`
- `trap_path__leo_realizes_limits__morning`
- `trap_path__leo_calls__morning`
- `trap_path__forest_echo__morning`
- `forest_run__milo_hears__morning`
- `forest_run__milo_recognition__morning`
- `forest_run__run_toward_call__morning`
- `forest_run__run_over_roots__morning`
- `forest_run__run_between_bushes__morning`
- `forest_run__run_under_branches__morning`
- `forest_run__run_with_purpose__morning`
- `forest_run__run_concern__morning`
- `forest_run__run_final_approach__morning`

## Created files

- `docs/audio-line-visual-workflow.md`
- `production/audio_visual_plan.py`
- `stories/lion_and_mouse_v7/AUDIO_VISUAL_MIGRATION.json`
- `stories/lion_and_mouse_v7/MIGRATION_REPORT.md`
- `stories/lion_and_mouse_v7/audio_inventory_r001.json`
- `stories/lion_and_mouse_v7/audio_visual_plan.json`
- `stories/lion_and_mouse_v7/derived/AUDIO_VISUAL_INVENTORY.md`
- `stories/lion_and_mouse_v7/derived/audio_visual_summary.json`
- `stories/lion_and_mouse_v7/derived/future_clip_candidates.json`
- `stories/lion_and_mouse_v7/derived/image_readiness.json`
- `stories/lion_and_mouse_v7/derived/planning_readiness.json`
- `stories/lion_and_mouse_v7/derived/validation/planning-validation.log`
- `stories/lion_and_mouse_v7/derived/validation/unit-tests.log`
- `stories/lion_and_mouse_v7/derived/video_readiness.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/BASELINE_TESTS.log`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/CHARACTER_STAGING.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/GENERATION_PROMPTS.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/HISTORY_NOTICE.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/LOCATION_REVIEW.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/README.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/SCRIPT.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/SNAPSHOT_MANIFEST.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/SOURCE_OF_TRUTH.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/VISUAL_SEQUENCE.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/audio/en/timing.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/audio_manifest.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/audio_regeneration_plan.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/build_audio_visual_plan.py`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/character_library.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/derived/SHOT_INVENTORY.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/derived/audio_regeneration_requests.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/derived/audio_resume_requests.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/derived/audio_scene01_dryrun.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/derived/generation_manifest.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/derived/image_inventory.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/derived/resume_queue.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/dialogue_coverage.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/location_library.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/migrate_paired.py`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/migration_report.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/narration_candidate_manifest_r001.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/narration_pilot/DRY_RUN.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/narration_pilot/OPERATION.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/narration_pilot/README.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/narration_pilot/lines.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/owner_foundation_acceptance.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/register_generated.py`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/.claude/skills/audio-chained-coverage/SKILL.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/.claude/skills/consistent-image-prompts/SKILL.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/AGENTS.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/CLAUDE.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/docs/paired-image-workflow.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/docs/production-direction.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/production/keyframe_staging_recipe.py`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/production/paired_composition.py`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/production/paired_images.py`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/production/paired_review.py`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/production/v7_runtime.py`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/production/verify_audio_manifest.py`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/tests/test_gemini_narration_setup.py`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/repository_sources/tests/test_paired_images.py`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/PAIR_REVIEW_TEMPLATE.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/QA_REPORT.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/README.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/archive/rejected_background_redraw/S01-U01_review.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/contact_sheets/v7_locations.svg`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/contact_sheets/v7_sequence_review.svg`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/foundation/LEO_TRANSPARENCY_OPERATION.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/foundation/LEO_TRANSPARENCY_REVIEW.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/foundation/NEXT_IMAGE_OPERATION.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/foundation/NEXT_IMAGE_OPERATION.md`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/foundation/canonical_sources.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/sequence/sequence.html`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/sequence/sequence_manifest.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/validation/gemini-setup-tests.log`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/validation/gemini_access.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/validation/input-auditor-tests.log`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/validation/narration_lumi_backup.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/validation/narration_resume_operation.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/validation/paired-tests.log`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/validation/temp_cleanup.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/validation/unit-tests.log`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/validation/validation_summary.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/review/paired/validation/video-preflight.log`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/selection.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/shot_plan.json`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/tools_compose.py`
- `stories/lion_and_mouse_v7/history/pre_audio_line_visual_2026-10-19/visual_unit_plan.json`
- `tests/test_audio_visual_plan.py`

## Changed files

- `.claude/skills/audio-chained-coverage/SKILL.md`
- `.claude/skills/consistent-image-prompts/SKILL.md`
- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `docs/changelog.md`
- `docs/paired-image-workflow.md`
- `docs/production-direction.md`
- `production/check_markdown_links.py`
- `production/keyframe_staging_recipe.py`
- `production/paired_images.py`
- `production/paired_review.py`
- `production/v7_runtime.py`
- `production/verify_audio_manifest.py`
- `stories/lion_and_mouse_v7/CHARACTER_STAGING.md`
- `stories/lion_and_mouse_v7/LOCATION_REVIEW.md`
- `stories/lion_and_mouse_v7/README.md`
- `stories/lion_and_mouse_v7/SCRIPT.md`
- `stories/lion_and_mouse_v7/SOURCE_OF_TRUTH.md`
- `stories/lion_and_mouse_v7/audio_manifest.json`
- `stories/lion_and_mouse_v7/dialogue_coverage.json`
- `stories/lion_and_mouse_v7/location_library.json`
- `stories/lion_and_mouse_v7/review/README.md`
- `tests/test_gemini_narration_setup.py`
- `tests/test_paired_images.py`
- `voice/narration/lion_and_mouse_v7/README.md`

## Moved/retired active paths

- `stories/lion_and_mouse_v7/GENERATION_PROMPTS.json`
- `stories/lion_and_mouse_v7/VISUAL_SEQUENCE.md`
- `stories/lion_and_mouse_v7/audio/en/timing.json`
- `stories/lion_and_mouse_v7/audio_regeneration_plan.json`
- `stories/lion_and_mouse_v7/derived/SHOT_INVENTORY.md`
- `stories/lion_and_mouse_v7/derived/audio_regeneration_requests.json`
- `stories/lion_and_mouse_v7/derived/audio_resume_requests.json`
- `stories/lion_and_mouse_v7/derived/audio_scene01_dryrun.json`
- `stories/lion_and_mouse_v7/derived/generation_manifest.json`
- `stories/lion_and_mouse_v7/derived/image_inventory.json`
- `stories/lion_and_mouse_v7/derived/resume_queue.json`
- `stories/lion_and_mouse_v7/migrate_paired.py`
- `stories/lion_and_mouse_v7/migration_report.json`
- `stories/lion_and_mouse_v7/narration_candidate_manifest_r001.json`
- `stories/lion_and_mouse_v7/narration_pilot/DRY_RUN.json`
- `stories/lion_and_mouse_v7/narration_pilot/OPERATION.json`
- `stories/lion_and_mouse_v7/narration_pilot/README.md`
- `stories/lion_and_mouse_v7/narration_pilot/lines.json`
- `stories/lion_and_mouse_v7/register_generated.py`
- `stories/lion_and_mouse_v7/review/PAIR_REVIEW_TEMPLATE.md`
- `stories/lion_and_mouse_v7/review/QA_REPORT.md`
- `stories/lion_and_mouse_v7/review/README.md`
- `stories/lion_and_mouse_v7/review/archive/rejected_background_redraw/S01-U01_review.json`
- `stories/lion_and_mouse_v7/review/contact_sheets/v7_locations.svg`
- `stories/lion_and_mouse_v7/review/contact_sheets/v7_sequence_review.svg`
- `stories/lion_and_mouse_v7/review/paired/foundation/LEO_TRANSPARENCY_OPERATION.json`
- `stories/lion_and_mouse_v7/review/paired/foundation/LEO_TRANSPARENCY_REVIEW.md`
- `stories/lion_and_mouse_v7/review/paired/foundation/NEXT_IMAGE_OPERATION.json`
- `stories/lion_and_mouse_v7/review/paired/foundation/NEXT_IMAGE_OPERATION.md`
- `stories/lion_and_mouse_v7/review/paired/foundation/canonical_sources.json`
- `stories/lion_and_mouse_v7/review/paired/foundation/canonical_sources.png`
- `stories/lion_and_mouse_v7/review/paired/sequence/sequence.html`
- `stories/lion_and_mouse_v7/review/paired/sequence/sequence_manifest.json`
- `stories/lion_and_mouse_v7/review/paired/validation/gemini-setup-tests.log`
- `stories/lion_and_mouse_v7/review/paired/validation/gemini_access.json`
- `stories/lion_and_mouse_v7/review/paired/validation/input-auditor-tests.log`
- `stories/lion_and_mouse_v7/review/paired/validation/narration_lumi_backup.json`
- `stories/lion_and_mouse_v7/review/paired/validation/narration_resume_operation.json`
- `stories/lion_and_mouse_v7/review/paired/validation/paired-tests.log`
- `stories/lion_and_mouse_v7/review/paired/validation/temp_cleanup.json`
- `stories/lion_and_mouse_v7/review/paired/validation/unit-tests.log`
- `stories/lion_and_mouse_v7/review/paired/validation/validation_summary.json`
- `stories/lion_and_mouse_v7/review/paired/validation/video-preflight.log`
- `stories/lion_and_mouse_v7/selection.json`
- `stories/lion_and_mouse_v7/shot_plan.json`
- `stories/lion_and_mouse_v7/tools_compose.py`
- `stories/lion_and_mouse_v7/visual_unit_plan.json`

All retired paths have exact hashed copies in `history/pre_audio_line_visual_2026-10-19/`; shared paired CLIs remain deprecated/fail-closed for migrated v7. Snapshot copies are historical evidence, not alternate active authorities.

No image/audio/video generation, spending, asset download, GPU job, upload, remote publication, staging, commit or push occurred.
