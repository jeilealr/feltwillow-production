# Feltwillow

Felt-animal fables for children, each with a kind message, made with open
video models on the LUMI supercomputer, for the YouTube channel
*Feltwillow*.

Every story is a data file (`stories/<slug>/story.yaml`): a style bible,
frozen character and location descriptions, the narration, and scenes broken
into shots. The tools compose references and generate candidate clips; visual
review checks that the same characters and forest remain consistent across shots. Narration and character
voices come from Gemini TTS (`voice/`); music and sound effects (none used yet)
may come from ElevenLabs later; the final mix is done in DaVinci Resolve.

## Project status (2026-10-11)

| Story | Status | Starting point |
|---|---|---|
| **The Lion and the Mouse v6** | Approved v6 character/location foundations. V6 uses the same unchanged English recordings as v5 (161 lines, 11:23.7); the audio was retained because it had no issue, not replaced. Sixteen overview boards plus six supplemental boards guide 52 visual units. All 92 individual 1920×1080 keyframes are candidates; the continuity audit found issues to resolve before video. No video takes or edit exist yet. | [v6 README](stories/lion_and_mouse_v6/README.md), [keyframe review](stories/lion_and_mouse_v6/KEYFRAME_REVIEW.md), [continuity audit](stories/lion_and_mouse_v6/KEYFRAME_CONSISTENCY_AUDIT.md), [video boundaries](stories/lion_and_mouse_v6/VIDEO_BOUNDARIES.md) |
| **The Lion and the Mouse v5** | Historical visual/render production. Its 186 rendered clips and take selection belong to v5; the same unchanged English recordings also serve v6 and are hash-recorded there. | [v5 README](stories/lion_and_mouse_v5/README.md) and [readable prompts](stories/lion_and_mouse_v5/prompts/) |

The v2-v4 folders were removed on 2026-10-06 and remain in Git history. The v5 script, bible and prompt records came from v4. See [CLAUDE.md](CLAUDE.md) for durable operating notes; v6 status and evidence are summarized in its story-local README.
Next stories in preparation (script and shot plan ready for review): [The Tortoise and the Hare](stories/tortoise_and_hare_v1/README.md), [The Boy Who Cried Wolf](stories/boy_who_cried_wolf_v1/README.md) and [The Ugly Duckling](stories/ugly_duckling_v1/README.md).
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
| Story and prompt plan | `visual_bible.json`, `prompt_manifest.json`; runtime `story.yaml` from `production/export_runtime.py` | complete image/video prompts, state/geometry records and each accepted image's result; current render scripts require story YAML |
| Narration | `dialogue_coverage.json` + `voice/narrate_scenes.py`; `voice/` | the spoken lines; one WAV per scene with Gemini voices; `production/timing_sheet.py` maps lines to shots |
| Cast | `character/characters/<story>/<Name>/` | canonical, references, expressions |
| Places | `character/locations/<story>/<place>/` (bible `locations`) | empty plates, one per lighting; props |
| Scene stills | `character/characters/<story>/interactions/keyframes/` | the start and end image of every shot, recorded in the manifest |
| Shots | `production/shot.py` (`--fast`) | Wan 2.2 image-to-video between keyframes, one action per shot |
| Animatic (separate owner request) | `production/animatic.py` | assembly after actual take selection; source choices and dialogue timing need manual review |
| Post | `feltwillow/post.py` | RIFE 16->30 fps, Real-ESRGAN to 1080p, grade |

## Consistent images (start here before any image)

Every story keeps one visual bible (`stories/<slug>/visual_bible.json`): canonical character
descriptions written from the approved canonical images, the size lineup, locked location plates
and camera setups with measured character sizes. All image and video prompts in
`prompt_manifest.json` are templates built from it:

```bash
python3 production/image_prompts.py --story lion_and_mouse_v6 build   # render the templates
python3 production/image_prompts.py --story lion_and_mouse_v6 lint    # must report 0 errors
python3 production/image_prompts.py --story lion_and_mouse_v6 md      # readable prompts in stories/<slug>/prompts/
python3 production/image_prompts.py --story lion_and_mouse_v6 review <record> --image <candidate>   # side-by-side gate
python3 production/image_prompts.py --story lion_and_mouse_v5 new-story <slug>   # skeleton for a new story
```

Claude Code loads the repo skill `consistent-image-prompts` (`.claude/skills/`) for any image
work; it walks through the setup for a new story, prompt writing, generation and review.
Details: `docs/image-prompts.md`; rules: `docs/creation-rules.md` (CR-11 to CR-18).

To make an image yourself: `python3 production/image_prompts.py show <record>` (or
`stories/<slug>/prompts/*.md`) gives the exact prompt; attach the references it lists, in that
order.

## Layout

```
stories/     one folder per story: story.yaml, story.txt, narration/, packs/
production/  image_prompts, story_packet, export_runtime, shot, keyframe, timing_sheet, animatic
production/contracts/  pinned publishing contract (CONTRACT.lock + feltwillow-contracts/<version>/); never edit by hand
character/   characters/ and locations/ per story; gemini_image.py (optional)
voice/       Gemini TTS: tools, saved voices (cast/, narrators/), samples
feltwillow/        shared package: paths, ffmpeg helpers, Wan wrapper, post-processing
lumi/        site.sh (machine paths), container wrapper, venvs, task runner
docs/        guides, measured rules, findings, licensing, LUMI, provenance
work/        everything generated (git-ignored)
```

## Quick start (LUMI; existing v3 example)

```bash
cd /scratch/project_465002727/jelealro/feltwillow-production   # always from the repo root
W=lumi/run_in_container.sh
$W python production/shot.py --story lion_and_mouse_v5 --scene 1 --shot s01_explores --fast --dry-run
# GPU work: one command per line in a task file (commands run from the repo root)
sbatch --ntasks=3 --gpus-per-node=3 --mem=330G lumi/run_tasks.sbatch work/tasks/<name>.txt
# voices (no GPU)
source voice/gemini_env.sh && python voice/list_voices.py
```

V4 has no runnable `story.yaml` yet. These are command examples, not a v4 task list.
Pass the story slug explicitly; some tools default to v2.

Machine-specific paths (venvs, model cache, container, Slurm account) are all
in `lumi/site.sh`; nothing depends on the repo's folder name.

## Where to find things

### Guides: which one to read

| I want to... | Read |
|---|---|
| **review the rebuilt Lion and Mouse v6 foundations** | **[v6 folder](stories/lion_and_mouse_v6/README.md)** and [foundation candidates](stories/lion_and_mouse_v6/FOUNDATION_REVIEW.md) |
| **review all Lion and Mouse v6 scene images** | **[keyframe review and contact sheets](stories/lion_and_mouse_v6/KEYFRAME_REVIEW.md)**; [continuity audit](stories/lion_and_mouse_v6/KEYFRAME_CONSISTENCY_AUDIT.md) and [video boundaries](stories/lion_and_mouse_v6/VIDEO_BOUNDARIES.md); [scene boards](stories/lion_and_mouse_v6/SCENE_REVIEW.md) are composition references |
| see v5 production history | [v5 folder](stories/lion_and_mouse_v5/README.md): script, shot plan, prompts and render review |
| **make or remake an image** | For v6, begin with the [staging rules and known failures](stories/lion_and_mouse_v6/KEYFRAME_CONSISTENCY_AUDIT.md); prompts on already generated records are historical provenance, not approved regeneration instructions. Manifest-backed stories use readable prompts in `stories/<slug>/prompts/` and `python3 production/image_prompts.py --story <slug> show <record>`. |
| make still images with the Gemini API (optional) | [docs/gemini-images.md](docs/gemini-images.md): workflow, model choice, cost, lessons |
| preserve exact prompts and references | [Prompt records](docs/prompt-records.md) |
| approve images and prepare clip jobs | [V4 preflight](docs/v4-preflight.md): manual gates and current tooling gaps |
| **write a script, an image prompt or a shot description** | **[docs/creation-rules.md](docs/creation-rules.md)**: rules for scripts, character and location images, interactions and shots, identity, scale, pair, prop, motion and review requirements |
| understand the whole pipeline, story to finished shots | [docs/production-guide.md](docs/production-guide.md) |
| check a video-prompt rule and the evidence behind it | [docs/prompting.md](docs/prompting.md): every measured rule, a checklist, the results log |
| know what went wrong before and how it was fixed | [docs/findings-and-risks.md](docs/findings-and-risks.md) |
| audit repository-wide consistency before image or video production | [Reusable consistency audit prompt](docs/repository-consistency-audit-prompt.md); [2026-10-10 audit findings](docs/audits/repository-consistency-2026-10-10.md) |
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
| Prompt records and their results | `stories/<slug>/prompt_manifest.json`; each record names its image path, hash and review |
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
