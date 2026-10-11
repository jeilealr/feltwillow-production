# Feltwillow repository drift audit and documentation repair prompt

Give the text below to an agent working from the root of `feltwillow-production`. It is a **repo-wide audit and documentation-repair assignment**, not a list of already proven defects. Replace the bracketed inputs. The agent should investigate beyond the examples named here and make safe, reviewable documentation corrections during the audit.

---

You are auditing Feltwillow production for anything that could cause a future agent, script, artist or renderer to make a wrong production decision. Inspect the **current repository state**, find verified drift sources in documentation and code-to-documentation contracts, correct unambiguous documentation defects, register every material finding, and write a dependency-ordered action plan for remaining work. Do not limit the search to known Lion and Mouse v6 issues.

Inputs:

- Repository root: `[absolute path to feltwillow-production]`
- Primary story, if any: `[story slug or "all active stories"]`
- Audit date: `[YYYY-MM-DD]`
- Report: `docs/audits/repository-consistency-YYYY-MM-DD.md` (add a suffix if occupied)
- Issue register: `docs/audits/repository-consistency-YYYY-MM-DD-issues.json`
- Action plan: `docs/audits/repository-consistency-YYYY-MM-DD-action-plan.md`

## Authority and scope

1. Read the latest owner decisions in the active conversation or task packet, then the current story README, visual bible, staging and sequence plans, asset records and approvals. Treat old docs, comments, examples, changelogs and earlier audits as evidence to test, not as automatically current authority. When two sources conflict, record both and their dates; do not guess which owner choice was intended.
2. Inspect all active stories, shared production code, tests, templates, skills, creation rules, top-level instructions and README files. Search for other relevant files instead of relying on a fixed checklist. Include tracked, untracked and ignored local files where accessible, and say exactly which evidence was unavailable.
3. For `lion_and_mouse_v6`, visual assets and approvals must stay v6-specific. V6 uses the **same unchanged English recordings and text as v5** because that audio had no issue; the owner is retaining it, not replacing or rerecording it. Its local audio manifest records exact hashes. Do not turn a historical “no cross-version reuse” sentence into a ban on this unchanged audio. Verify any active cross-version visual edge separately. Derive current counts, statuses and approved revisions from live files; do not hardcode older numbers from this prompt.
4. Make reversible **documentation** corrections when evidence establishes the intended rule. Update the source-of-truth page and links/examples that would otherwise continue to mislead. Preserve historical facts as clearly labeled history. Do not silently change approved artistic decisions, image/audio/video files, hashes, approvals, runtime outputs or code behavior. Put needed asset or code changes in the action plan unless the owner separately authorized them.
5. Keep the work auditable: capture branch, commit, dirty files and commands before editing; do not overwrite unrelated user changes. Every edited document must appear in the report with its previous conflict, authoritative evidence and new wording. Do not expose secrets or copy private media into the report.

## Discovery: find drift, not just broken links

Build a **source-of-truth map** for each active story and shared workflow. For every production fact, identify the authoritative file, code that reads or writes it, validation gate, human review step, and duplicate claims elsewhere. Cover at least:

- character identity, canonical revisions, expression and pose derivation, felt texture, palette, species anatomy, silhouette and visible feature counts;
- same-depth cast ratio, standing-equivalent versus pose-box height, camera crop/zoom, depth movement, same-ground-plane environment scale, contact points, shadows and occlusion;
- approved location masters, lighting variants, landmarks, crops, walkable areas, props, net/rope state and background continuity across shots;
- script text, audio source and hashes, line IDs, duration, coverage, visual units, supplemental inserts, chronology and word-level cut timing;
- per-shot and per-scene start/end images, exact shared boundaries, deliberate cuts versus zooms, video motion feasibility, dialogue-only lip-sync and narrator voice-over;
- generated candidate versus owner-approved asset, exact prompt/reference provenance, image hashes, stale approvals, review gates, runtime export, selected take and final edit lineage.

Inspect the **actual bytes and code paths** behind claims. A plan with correct arithmetic cannot prove a rendered character's size or face; an attached plate does not prove identical background pixels; a file named `approved` does not prove hash-bound owner approval. Conversely, a current untracked asset can be real even if Git does not transport it. Separate verified current state, desired state, historical record and unknown evidence.

Search all Markdown/JSON/YAML, templates, skill files, command examples, comments and active scripts for contradictory or obsolete statements: wrong paths or revisions, deleted files/tools, old story counts, older cast-scale rules, hidden prompt multipliers, unregistered camera changes, stale start/end terminology, false “final” status, cross-version inputs, mismatched actor counts, broken links and commands that mutate when presented as checks. Examine both **readers and writers** so a corrected doc cannot be overwritten by a generator that still emits the old claim. Check whether a supposed safety gate actually blocks export/render or only prints a warning.

For images and transitions, enumerate **all** active keyframe records and their PNG hashes first. Review canonicals, each recurring setup anchor, every owner-flagged image, each same-view start/end pair, every shared scene boundary, every change of location/light/crop, and high-risk two-character or prop-contact shots at full size. If the collection is too large for complete visual review, disclose the exact sample and list unviewed files; do not call the unviewed set visually consistent. Record measured frame fractions, pose/anatomy metric, contact depth, camera crop and a landmark at the **same depth**. Check physical character-to-background ratios, not only character height divided by frame height. Compare lying Leo by head/mane/paw dimensions, not flattened pose height. Flag face or texture drift even when body color and metadata pass.

Trace each active visual path from audio line to visual unit, chronological keyframe, planned video endpoint, runtime input and rendered take where those stages exist. Check gaps, duplicate coverage, temporal reversals, unintentional background jumps, actor teleportation, scale jumps, inconsistent net or prop state, missing endpoint pairs and false continuous joins. A camera crop defaults to a cut; a zoom must have a registered camera path and compatible geometry. A shared boundary means the **exact same image bytes** at one scene's end and the next scene's start, followed by a reviewed next target. If video does not exist yet, report a planning risk rather than claiming a rendered defect.

## Checks and repair method

Use read-only inspections or `--check`/dry-run modes for generators. Run relevant static validators, image-hash checks and tests in the available environment. Do not install an environment or run external/GPU services merely to complete this audit; record missing dependencies and the exact check they prevent. Do not run image generation, TTS, rendering, approval commands, destructive cleanup or mutating exports. Documentation files, the report, issue register and action plan are the authorized writes.

For each potential defect:

1. Reproduce it with a path and line, record ID, command/exit code, hash, or visual frame locator. Label the finding `verified`, `inferred` or `unverified`.
2. Explain what downstream decision it could change: character identity, physical scale, plate/crop, dialogue timing, transition, render input or approval state.
3. Decide whether the safe fix is documentation wording/link, metadata/code, asset revision, owner artistic decision, or external evidence. Apply only the documentation fix when the intended rule is established.
4. Re-run the relevant check and search for the old conflicting wording. Do not declare the repository clean merely because a local test suite passes or because a review gate correctly blocks unapproved assets.

## Deliverables

Write three standalone files at the paths above:

1. **Audit report:** snapshot (date, branch/commit/dirty state, accessible and missing inputs), stories and stages inventoried, source-of-truth map, checks/exit codes, exact visual coverage, documentation changes made, and unresolved limitations. Give each finding a stable ID (`CONS-001`, …), severity (`P0` render/approval blocker, `P1` likely visible or lineage defect, `P2` process/documentation drift, `P3` cleanup), evidence status, expected/actual behavior, downstream risk and smallest fix. Include a go/no-go table for still generation, still approval, pilot export, bulk render and edit handoff with evidence or finding IDs.
2. **Issue register JSON:** one object per finding with ID, severity, evidence status, story/stage, exact paths/records, evidence, impact, authoritative source, fix category, current status (`fixed_in_docs`, `open`, `needs_owner_decision`, `needs_external_evidence`), dependencies, validation and owner question only if truly needed. Include a schema/version and audit date so later agents can update it without losing provenance.
3. **Action plan:** prioritize source-of-truth and gate fixes before dependent asset revisions, then video/timing work. For every step give owner, affected files, prerequisites, concrete action, acceptance criterion and validation command or visual review. Separate safe documentation work already completed from code/metadata tasks, image revisions, owner decisions and unavailable-environment checks. Do not propose regenerating all assets when a focused correction suffices.

Before finishing, verify links and JSON syntax, rerun relevant non-mutating checks, list exactly which documents changed, and ensure the report's issue IDs match the register and action plan. Return the three links and the highest-priority open blockers. A clean report must say what was actually inspected and what remains unknown.
