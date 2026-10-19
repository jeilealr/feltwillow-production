# Feltwillow

**Preservation note, 19 October 2026:** Unavailable historical/local media links below are retained as code paths. Recover only exact historical bytes through the cleanup receipts/Git history or the verified local archive; these paths are not active generation authorities. Original dated results remain in source history.

**Current route (19 October 2026):** [approved images → Wan → reviewed continuity/dialogue → final edit](docs/production-direction.md). Blender and control/material research are preserved, paused and opt-in. [V6 readiness](stories/lion_and_mouse_v6/IMAGE_TO_VIDEO_READINESS.md) distinguishes selected images from production approval.

Felt-animal fables for children, each with a kind message, made with open
video models on the LUMI supercomputer, for the YouTube channel
*Feltwillow*.

Each story has a packet under `stories/<slug>/`. Manifest-backed stories export
`story.yaml` for rendering; the current Lion and Mouse v6 packet instead has
scene, staging, keyframe and video-boundary plans; owner image selection is complete and technical validation remains pending.
The tools compose references and generate candidate clips; visual
review checks that the same characters and forest remain consistent across shots. Narration and character
voices come from Gemini TTS (`voice/`); music and sound effects (none used yet)
may come from ElevenLabs later; the final mix is done in DaVinci Resolve.

## Project status (v6 reconciled 2026-10-16)

| Story | Status | Starting point |
|---|---|---|
| **The Lion and the Mouse v6** | 96 current 1920×1080 story images present and owner-selected (reconciled 2026-10-16); technical approval/evidence gates remain open. Owner-approved r03 full-body Milo master; older performance family pending refresh. Same unchanged English recordings as v5: 161 lines, 11:23.7. Experimental clips exist; no approved v6 production takes/edit. | [Current handoff](stories/lion_and_mouse_v6/README.md), [image selection ledger](stories/lion_and_mouse_v6/owner_visual_acceptance.json), [gallery](stories/lion_and_mouse_v6/KEYFRAME_REVIEW.md), [runtime contract](stories/lion_and_mouse_v6/RUNTIME_CONTRACT.md) |
| **The Lion and the Mouse v5** | Historical visual/render production. The initial 62-shot review covered 186 takes; a later three-seed bridge brought the documented expectation to 189. Actual local media/sidecars require a fresh inventory. The same unchanged English recordings also serve v6 and are hash-recorded there. | [v5 README](stories/lion_and_mouse_v5/README.md) and [render review](stories/lion_and_mouse_v5/RENDER_REVIEW.md) |
| **The Ugly Duckling v1** | Generated foundation and scene images, with 126 takes recorded for Scenes 1–9. Visual review, ignored prompt references missing from Git, Scene 11 identity repair and Scene 8 snow continuity remain open. Local lint passes only with those ignored files present. | [Ugly Duckling README](stories/ugly_duckling_v1/README.md) and [render review](stories/ugly_duckling_v1/RENDER_REVIEW.md) |

The v2-v4 folders were removed on 2026-10-06 and remain in Git history. The v5 script, bible and prompt records came from v4. See [CLAUDE.md](CLAUDE.md) for durable operating notes; v6 status and evidence are summarized in its story-local README.
Next stories in preparation (script and shot plan ready for review): [The Tortoise and the Hare](stories/tortoise_and_hare_v1/README.md) and [The Boy Who Cried Wolf](stories/boy_who_cried_wolf_v1/README.md).
The v5 stills are owner-made (ChatGPT Pro); the English narration exists; the runtime
`story.yaml` is exported by `production/export_runtime.py`.

**New here? See [Where to find things](#where-to-find-things) below.**

## How a story gets made

```
script + shot order review -> approved cast/places/props -> paired keyframes
-> individual pilot/clips -> owner take selection -> separately requested animatic -> post/edit
```

| Stage | Tool | What it produces |
|---|---|---|
| Story and prompt plan | Manifest-backed packets: `visual_bible.json`, `prompt_manifest.json`, then `story.yaml` via `production/export_runtime.py`. Current v6: `scene_plan.json`, `staging_plan.json`, `keyframe_plan.json`, `video_boundary_plan.json` | Story-specific image and video planning; v6 remains blocked from rendering until hash-bound visual review and a current-plan runtime preflight pass |
| Narration | `dialogue_coverage.json` + `voice/narrate_scenes.py`; `voice/` | the spoken lines; one WAV per scene with Gemini voices; `production/timing_sheet.py` maps lines to shots |
| Cast | `character/characters/<story>/<Name>/` | canonical, references, expressions |
| Places | `character/locations/<story>/<place>/` (bible `locations`) | empty plates, one per lighting; props |
| Scene stills | `character/characters/<story>/interactions/keyframes/` | candidate start/end images, recorded in that story's active plan or manifest |
| Shots | `production/shot.py` (`--fast`) | Wan 2.2 image-to-video between keyframes, one action per shot |
| Animatic (separate owner request) | `production/animatic.py` | assembly after actual take selection; source choices and dialogue timing need manual review |
| Post | `feltwillow/post.py` | RIFE 16->30 fps, Real-ESRGAN to 1080p, grade |

## Consistent images (start here before any image)

Every story keeps one visual bible (`stories/<slug>/visual_bible.json`): canonical character
descriptions written from the approved canonical images, the size lineup, locked location plates
and camera setups with measured character sizes. Manifest-backed stories build image and video
prompt templates from it:

```bash
python3 production/image_prompts.py --story ugly_duckling_v1 lint
python3 production/image_prompts.py --story lion_and_mouse_v5 show <record>
python3 production/image_prompts.py --story lion_and_mouse_v5 new-story <slug>
```

Current v6 uses its [keyframe review](stories/lion_and_mouse_v6/KEYFRAME_REVIEW.md) and
`production/keyframe_visual_gate.py --story lion_and_mouse_v6` for exact-image review; the
96 current images are owner-selected, with their exact hashes in the
[selection ledger](stories/lion_and_mouse_v6/owner_visual_acceptance.json). Structured
technical evidence and some foundation/setup approvals remain incomplete. The
[v6 runtime contract](stories/lion_and_mouse_v6/RUNTIME_CONTRACT.md) describes the
read-only `production/v6_runtime.py --story lion_and_mouse_v6 --preflight` and later
explicit-timing export. It does not use `image_prompts.py` against a nonexistent
v6 prompt manifest.

Claude Code loads the repo skill `consistent-image-prompts` (`.claude/skills/`) for any image
work; it walks through the setup for a new story, prompt writing, generation and review.
Details: `docs/image-prompts.md`; rules: `docs/creation-rules.md` (CR-11 to CR-18).

For a manifest-backed story, `python3 production/image_prompts.py --story <slug> show <record>`
(or `stories/<slug>/prompts/*.md`) gives the recorded prompt and ordered
references. For v6, inspect the scene/keyframe plans and recorded provenance;
the candidate prompts are history, and revised images need a new review-bound revision.

## Layout

```
stories/     one folder per story: manifest-backed runtime YAML or v6-native plans
production/  image_prompts, story_packet, export_runtime, shot, keyframe, timing_sheet, animatic
production/contracts/  pinned publishing contract (CONTRACT.lock + feltwillow-contracts/<version>/); never edit by hand
character/   characters/ and locations/ per story; gemini_image.py (optional)
voice/       Gemini TTS: tools, saved voices (cast/, narrators/), samples
feltwillow/        shared package: paths, ffmpeg helpers, Wan wrapper, post-processing
lumi/        site.sh (machine paths), container wrapper, venvs, task runner
docs/        guides, measured rules, findings, licensing, LUMI, provenance
work/        everything generated (git-ignored)
```

## Quick start (LUMI; existing v5 example)

```bash
cd /scratch/project_465002727/jelealro/feltwillow-production   # always from the repo root
W=lumi/run_in_container.sh
$W python production/shot.py --story lion_and_mouse_v5 --scene 1 --shot s01_explores --fast --dry-run
# GPU work: one command per line in a task file (commands run from the repo root)
sbatch --ntasks=3 --gpus-per-node=3 --mem=330G lumi/run_tasks.sbatch work/tasks/<name>.txt
# voices (no GPU)
source voice/gemini_env.sh && python voice/list_voices.py
```

These are v5 command examples, not v6 render authorization. Pass the story slug explicitly.

Machine-specific paths (venvs, model cache, container, Slurm account) are all
in `lumi/site.sh`; nothing depends on the repo's folder name.

## Where to find things

### Guides: which one to read

| I want to... | Read |
|---|---|
| **review the rebuilt Lion and Mouse v6 foundations** | **[v6 folder](stories/lion_and_mouse_v6/README.md)** and [foundation candidates](stories/lion_and_mouse_v6/FOUNDATION_REVIEW.md) |
| **review all Lion and Mouse v6 scene images** | **[keyframe review and contact sheets](stories/lion_and_mouse_v6/KEYFRAME_REVIEW.md)**; continuity audit (`stories/lion_and_mouse_v6/KEYFRAME_CONSISTENCY_AUDIT.md`) and [video boundaries](stories/lion_and_mouse_v6/VIDEO_BOUNDARIES.md); scene boards (`stories/lion_and_mouse_v6/SCENE_REVIEW.md`) are composition references |
| see v5 production history | [v5 folder](stories/lion_and_mouse_v5/README.md): script, shot plan, prompts and render review |
| **make or remake an image** | For v6, begin with the staging rules and known failures (`stories/lion_and_mouse_v6/KEYFRAME_CONSISTENCY_AUDIT.md`); prompts on already generated records are historical provenance, not approved regeneration instructions. Manifest-backed stories use readable prompts in `stories/<slug>/prompts/` and `python3 production/image_prompts.py --story <slug> show <record>`. |
| make still images with the Gemini API (optional) | [docs/gemini-images.md](docs/gemini-images.md): workflow, model choice, cost, lessons |
| preserve exact prompts and references | [Prompt records](docs/prompt-records.md) |
| approve images and prepare clip jobs | For current v6, [keyframe review](stories/lion_and_mouse_v6/KEYFRAME_REVIEW.md) and [video boundaries](stories/lion_and_mouse_v6/VIDEO_BOUNDARIES.md). [V4 preflight](docs/v4-preflight.md) is historical. |
| **write a script, an image prompt or a shot description** | **[docs/creation-rules.md](docs/creation-rules.md)**: rules for scripts, character and location images, interactions and shots, identity, scale, pair, prop, motion and review requirements |
| understand the whole pipeline, story to finished shots | [docs/production-guide.md](docs/production-guide.md) |
| check a video-prompt rule and the evidence behind it | [docs/prompting.md](docs/prompting.md): every measured rule, a checklist, the results log |
| know what went wrong before and how it was fixed | [docs/findings-and-risks.md](docs/findings-and-risks.md) |
| audit repository-wide consistency before image or video production | [Reusable consistency audit prompt](docs/repository-consistency-audit-prompt.md); [2026-10-11 audit snapshot](docs/audits/repository-consistency-2026-10-11.md); [current remediation disposition](docs/audits/repository-consistency-remediation-2026-10-11.md); [2026-10-10 historical audit](docs/audits/repository-consistency-2026-10-10.md). Use current gates for readiness. |
| hand finished stories to the publishing repository | [docs/publishing-handoff.md](docs/publishing-handoff.md): selection file, `production/export_handoff.py`, what it refuses |
| work with voices (Gemini TTS) | [voice/README.md](voice/README.md) |
| run things on LUMI (jobs, times, gotchas) | [docs/lumi.md](docs/lumi.md) |
| check a model's or service's licence | [docs/licensing.md](docs/licensing.md), [docs/google_gemini_terms_question.md](docs/google_gemini_terms_question.md) |
| see the current state, standing decisions and commands (also for AI agents) | [CLAUDE.md](CLAUDE.md) |
| read the first consistency experiments | [docs/character-consistency.md](docs/character-consistency.md) |
| know where code came from | [docs/provenance.md](docs/provenance.md) |

### Existing images, voices and generated files

| What | Where |
|---|---|
| **All images, by story** (since 2026-10-04) | `character/characters/<story>/<Name>/` (canonical, references, expressions), `character/characters/<story>/interactions/` (scene start/end frames), `character/locations/<story>/<place>/` (plates, props); `<story>` = the `stories/` folder name, e.g. `lion_and_mouse_v5` |
| Prompt records and their results | Manifest-backed stories: `stories/<slug>/prompt_manifest.json`; current v6: `keyframe_plan.json` and `keyframe_visual_reviews.json` |
| Saved voices (id, design prompt, samples in 6 languages) | `voice/cast/<role>/`, `voice/narrators/<name>/` |
| Rendered clips, keyframes, animatic (not in git) | `work/stories/<slug>/shots/`, `keyframes/`, `animatic.mp4` |
| GPU task files and logs | `work/tasks/`, `/scratch/project_465002727/jelealro/slurm_logs/` |
| Evidence images used in the docs | `docs/img/` |

## All docs

- [Lion and Mouse v5](stories/lion_and_mouse_v5/README.md): historical production
- [Prompt records](docs/prompt-records.md): exact text, references, revisions and execution provenance
- [V4 preflight](docs/v4-preflight.md): image, pair, clip and assembly gates
- [Gemini images](docs/gemini-images.md): making v4 stills with the Gemini API

- [CLAUDE.md](CLAUDE.md): operating manual and current state
- [Creation rules](docs/creation-rules.md): how to write scripts, image prompts and shot descriptions
- [Production guide](docs/production-guide.md): story to finished shots, with measured results
- [Writing prompts](docs/prompting.md): every measured prompt rule, and a checklist
- [Findings and risks](docs/findings-and-risks.md): every problem and its fix
- [Voices](voice/README.md): Gemini TTS setup, saved voices, languages
- [Licensing](docs/licensing.md): every model and service, checked for a monetised channel
- [Running on LUMI](docs/lumi.md): jobs, multi-GPU tasks, times, gotchas
- [Character consistency](docs/character-consistency.md): the first experiments
- [Provenance](docs/provenance.md): what came from where
