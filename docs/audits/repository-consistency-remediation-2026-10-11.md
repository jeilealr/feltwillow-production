# Repository consistency remediation — 2026-10-11

This disposition rechecks the [2026-10-11 audit](repository-consistency-2026-10-11.md)
against local `working-cloud-branch` at its audited starting commit
`1c29c2e96ee53890ca72c20b5d695e9471041bd0`. The checkout was clean before
remediation. This file describes the working-tree changes made after that commit;
it is not a production approval or a claim that local-only media exist in Git.

**Current decision: NO-GO for v6 GPU rendering, edit export and publishing.**
The runtime preflight now understands the native v6 plans, but all 92 active
keyframes lack owner visual approvals. Reviewed piece and word timing, a renderer
translation/pilot, and selected-take receipts are also still required.

| Finding | Recheck classification | Disposition and evidence |
|---|---|---|
| FWA-001 | PARTIALLY FIXED | 92/92 original candidate hashes matched the plan; the gate initially reported 94 blockers (92 missing reviews, 2 active rejected hashes). New `s14_p04`/`s14_p05` r02 candidates replace the active paths. Old r01 PNGs, SHA-256s and rejection records remain; the gate now reports 92 missing-review blockers. No review entry was invented. The new pair and all other frames still need full-size owner review. |
| FWA-002 | PARTIALLY FIXED | `production/v6_runtime.py --preflight` validates the current v6 bible, audio, keyframes, reviews and rebuilt boundaries without legacy manifests. It reports only the 92 visual blockers. Explicit-timing export can atomically produce a hash-bound `runtime_plan.json` after approvals, verified local audio and reviewed intra-line cut anchors. It deliberately does not synthesize `story.yaml` or GPU prompts; a reviewed renderer translation and pilot are still needed. |
| FWA-003 | CONFIRMED → REMEDIATED | Active handoff instructions now use `audit --strict`; strict join instructions include `--fail-on-flagged-joins`. The informational `audit` remains report-only. A pending-image fixture confirms strict handoff exits nonzero. |
| FWA-004 | CONFIRMED → REMEDIATED IN CODE | `shot.py --audit-existing` compares MP4 sidecars with current source/continuation hashes, recipe, model and Lightning revision. The bulk inventory checks every seed before submission and after each round; stale media stops the script without deleting or overwriting it. Unit tests cover missing/stale/current receipts. Actual LUMI media were not present here. |
| FWA-005 | CONFIRMED → REMEDIATED IN CODE | Render tasks/inventory and backup lists now resolve `FELTWILLOW_WORK` through `feltwillow.paths.WORK`. Backup offers `--dry-run` and separate relative lists for work and repository character art. Override tests passed; an actual LUMI backup was not run. |
| FWA-006 | CONFIRMED → REMEDIATED | Current README/CLAUDE/policy text distinguishes v5 source provenance from v6 runtime audio ownership and labels the old “no v6 images” instruction superseded. `verify_audio_manifest.py --require-source` validated all 161 local line source/runtime pairs and 16 scene WAVs against the tracked hashes and WAV format. |
| FWA-007 | PARTIALLY FIXED | Ugly Duckling is described as generated/rendered work with unresolved Scene 8 and 11 issues. Local prompt lint returned 0 errors/0 warnings because all 18 formerly missing references exist as ignored local files. They are absent from a clean Git checkout; contact-sheet paths are no longer misleading links. Exact reference preservation and the owner's visual decisions remain open. |
| FWA-008 | CONFIRMED → REMEDIATED | Broken active/historical relative links and deleted-story defaults were corrected or rendered as historical code paths. `production/check_markdown_links.py` reports zero broken repository-relative links in a clean-clone-style index scan. |
| FWA-009 | CONFIRMED → REMEDIATED | The 2026-10-10 audit now has a superseded banner and disposition note; the 2026-10-11 snapshot is tracked beside it. Neither snapshot overrides current gates. |
| FWA-010 | CONFIRMED → PARTIALLY FIXED | Focused runtime, receipt, path, policy, strict handoff and link tests plus a GitHub Actions workflow were added. Locally, 38 available tests passed. Full discovery loaded 39 tests but the existing lip-sync module could not import `numpy` from this system Python; CI installs lightweight test dependencies and still needs its first remote run. |
| FWA-011 | PARTIALLY FIXED — NEEDS LOCAL/LUMI EVIDENCE | Current docs distinguish the initial 186 reviewed v5 takes from the later three-seed bridge and call 189 an expected historical count. This checkout has no `work/stories/lion_and_mouse_v5/shots/` directory, so actual MP4/sidecar validity and a tracked inventory receipt cannot be asserted. |
| FWA-012 | CONFIRMED → PARTIALLY FIXED | README, active skills and CR-21 now branch by pipeline and direct v6 to staging, visual and native runtime preflight. Legacy prompt-manifest commands are scoped to stories with those files. The v6 renderer handoff remains pending FWA-002's reviewed runtime translation. |
| FWA-013 | PARTIALLY FIXED — NEEDS LOCAL/LUMI EVIDENCE | The tracked v6 audio manifest and new read-only verifier now prove the local WAV set; runtime export also records input hashes. Ignored Ugly references/contact sheets, v5 takes and future LUMI renders still need transportable hash receipts or an exact archive. |
| FWA-014 | CONFIRMED → REMEDIATED | The unused, v5→v6-specific `chain_packet.py` was removed from active production code. Its history remains in Git; active docs label it retired. |

The new Scene 14 active candidates are:

| Frame | Active r02 SHA-256 | Historical rejected r01 SHA-256 |
|---|---|---|
| `s14_p04` | `92066afa75a3ba884ece2e567bded4415e689d0406fa031141057e17f67deff8` | `93abc605530d0c61f777d7c11f066fe416d0794bb6484ae2baeb9fa9d1a504cc` |
| `s14_p05` | `5361b04c1f6dc1748afb07ad0eb267c0f99c21e762c044594ad4b7d786045f08` | `4d61b32eada6e4fbec9ad9c7dad7258948280c371b21a37a52454821ffb2bf12` |

`production/revise_keyframe_candidate.py` adopted each new 1920×1080 PNG,
checked its version-local path and revision, recorded the previous row under
`superseded`, and rebuilt the boundary JSON. The exact generation prompts and
reference paths are in `keyframe_plan.json`. [Scene 14 review](../../stories/lion_and_mouse_v6/KEYFRAME_REVIEW.md)
links the new images; its older contact sheet is explicitly historical.
Generation used the built-in imagegen skill with the registered trap-path crop,
Milo canonical, prior action and net reference for the first insert, then used
that insert as the edit source for the parted strand. The images were normalized
to the 1920×1080 video canvas. The new images are **candidates**, not approvals.

Next actions, in dependency order:

1. Owner reviews all 92 active PNG hashes at full size, especially the new Scene
   14 pair and previously flagged scale/background pairs. Record measured anchors,
   identity/plate/grounding/net checks and decisions in
   `keyframe_visual_reviews.json`; revise failures under new filenames.
2. Run the visual gate to zero blockers. Verify a reviewed piece timing plan
   covers all 16 WAVs and word-timing receipts support every intra-line cut.
3. Export the native v6 `runtime_plan.json`, then implement/review the renderer
   translation and validate a one-to-three-scene pilot with exact endpoint,
   audio, prompt, model and take receipts. Do not reuse v5 visuals or renders.
4. On LUMI, run read-only receipt inventory against existing v5 media, verify
   the alternate work root and backup dry run, and record the real MP4/sidecar
   counts before reconciling v5's expected 189 takes.
5. Preserve or register the 18 exact ignored Ugly references and required
   contact sheets for clean-clone reproducibility. Resolve the Scene 8 snow
   state and Scene 11 Ollie canonical before resuming dependent image work.

Local checks: 92 active keyframe hashes match the plan; v5/v6 tracked PNG byte
overlap is zero; v6 staging reports 0 errors for 92 frames; audio verification
reports 0 blockers for 161 lines and 16 scenes; Markdown links report zero
broken repository-relative targets; 38 environment-available unit tests pass;
`git diff --check` and `compileall` pass. Full unit discovery needs `numpy` in
the selected Python environment. No GPU render, media deletion, visual approval
or publishing action was performed.
