# Coverage mapping

No tests were renamed or removed. Existing case IDs remain.

| Changed check | Why | Preserved/replacement evidence |
|---|---|---|
| `test_audio_visual_plan...test_scene_composition_receipts_and_audio_links` | Historical sidecars were moved by the prior approved cleanup. | Uses the existing explicit, hash-checked `source_file` archive lookup; receipt/audio/hash assertions remain. |
| `test_character_performance...test_reuse_has_one_asset_and_one_off_is_allowed` | 44/28 were earlier production counts, not permanent limits. | Historical minimum coverage, exact owner hash/scope, generated/approved/pending partition, shared walk asset, its superseded history and one-off uniqueness remain checked. New accepted variants are allowed. |
| `...test_existing_images_receipts_and_audio_semantics_unchanged` | Later owner-approved S05 framing/S06 grouping legitimately changed visual coverage. | Exact world states/events/rules/script order and narration/audio remain protected; all 161 current recordings are asserted. Dedicated `test_sleeping_details_and_four_phase_landing`, `test_owner_acorn_has_contact_before_release`, `test_owner_rear_paw_and_scene_six_contract` and new sequence tests protect visual phases and ordering. |
| `...test_extra_review_page_does_not_serve_repository` | Fixed count 33 excluded later registered audio. | Only explicitly registered assets are served; WAVs remain inside story r001, private JSON and traversal stay forbidden. New sequence video route has an explicit run-scope/traversal test. |
| `SyntheticCandidateTests...test_distinct_candidate_and_approval_scopes_bytes_and_sidecars` | Resetting real files to planned without clearing their real binding hashes made a contradictory fixture. | Synthetic planned bindings reset their byte hashes. All sidecar/alpha/dimension/canonical/owner-scope mutation failures remain. |
| New `tests/test_sequence_pipeline.py` | End-to-end and distinct failure modes. | Known RGB A/B/C pixels through actual frozen command argv/copied renderer entrypoint; equal endpoints/cuts; scoped dependencies/aliases; hash invalidation; frame arithmetic; no-loader dry-run; interrupted-attempt claim; native floats; corrupt decode; take selection/downstream identity; protected pixels/transparent-input preview; explicit server video routing. |

Synthetic tests prove engineering behavior, not actual image integration, expression quality, model adherence or video beauty. Loopback tests require the sandbox exception; the full suite was not run because no commit was requested.
