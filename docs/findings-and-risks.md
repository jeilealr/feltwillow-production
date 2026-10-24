# Findings, fixes, and what you may be missing

## Historical v3 review and v4 response (2026-09-30)

The owner's v3 notes were at `docs/reviews/lion_and_mouse_v3_owner_notes_2026-09-30.txt`
and the v4 repair map was at `stories/lion_and_mouse_v4/REPAIR_PLAN.md`.
Those folders were removed; recover the historical files from Git history if needed.
For current production, begin with the [v6 packet](../stories/lion_and_mouse_v6/README.md).

| Observed failure | Required response | Evidence/status |
|---|---|---|
| Milo hair/body and Leo eyes/mane drift | new smooth-crown Milo root, approved brown-eye/mouth references, full rust mane, one tail | owner observations; new references pending |
| Milo shrinks between seated and standing images | calibrate skull/torso, then pose-specific silhouette heights | bbox scaling confirmed in code; clip-specific cause not measured |
| scene zoom and moving trunks | registered pairs, fixed camera/plate, gentle motion limited to local foliage/water/clouds | owner observations; new pilot pending |
| acorn disappears, rope resets or cuts away from bite, extra overhead net | explicit persistent object state, contacts/occlusion, single-net state chain | owner observations; storyboard/pair review required |
| unrequested hands/tails and bad late frames | limbs anchored, end keyframe, whole-clip review | owner observations; ordinal missing-end attribution ambiguous |
| expressive mouth changes unpredictably | closed baseline plus bounded mouth alternatives from approved mouth family | owner request; no lip-sync claim |
| premature assembly | individual clips -> owner exact take selection -> separately requested animatic | current standing instruction |

No v4 failure is marked solved. The source videos were not in this checkout.
The new JSON manifest and checklists are documentation, not enforced validators.
Known execution gaps and manual controls are in [v4-preflight.md](v4-preflight.md).
The coverage plan requires script/audio timing before it becomes a complete edit.

**Status 2026-10-02.** The v4 stills now exist: the smooth-crown Milo and Leo
canonicals, references, 22 expression studies, plates, props and 85 of the 86
scene start/end frames (`s02_place_acorn_end` is missing), accepted after
agent review and under owner review. The image-stage problems found on the way
became [creation-rules.md](creation-rules.md) CR-11 onward and the lessons in
[gemini-images.md](gemini-images.md); open image issues are listed in the
historical `stories/lion_and_mouse_v4/README.md`. English narration existed
and the historical `stories/lion_and_mouse_v4/TIMING_SHEET.md` shows that
the coverage shots it uses (42 of 43) fill 3.4 of its 11.4 minutes at normal
speed. No v4 clip has been rendered, so the video rows above stay unverified.

## Historical findings and risks (snapshot: 2026-09-26)

Sections A/B below retain experiment results, obsolete examples and dated external
research. A historical “solved” means that test, not all later shots. V1 black
eyes/1:6 scale, mandatory character LoRA, ElevenLabs narration, tracking-camera
advice and pre-render/automatic animatic recommendations are superseded. Current
cast uses brown eyes, Milo standing ratio 1:3, Gemini voices, fixed-camera I2V
without character LoRAs, and assembly only after owner selection and request.
External policy, prices and storage figures were not re-checked in this pass.

---

## A. Findings and their solutions

### Consistency

| Finding | Cause | Solution | Status |
|---|---|---|---|
| Same text gives a different character every shot (4 different foxes) | text describes a *kind* of character, the model samples one | start every shot from an image (keyframe); train a LoRA per main character | solved |
| Characters stay consistent within a shot but not between shots | nothing ties shots together but words | same as above | solved |
| LoRA learns the training background (forest prompt returns the meadow from step 1000) | every training image had the same meadow | composite the cut-out character into varied plates (`composite:` in the dataset file); pick the earliest good checkpoint | **solved** (`fox_v2`: no leak at any checkpoint) |
| LoRA can't do poses it never saw ("sleeping curled up" came out lying stretched) | no such pose in the data | put every pose the story needs into the character pack before training | rule |
| Design picked that contradicts its text sheet gets pulled back to the text | the sheet is in every prompt | make canonical and sheet agree | rule |
| Model ignores some sheet details (Leo's eyes always black, not brown) | model prior | decide and edit the sheet, or keep asking | **resolved**: owner keeps black eyes; sheet edited |

### Prompting (full rules in `docs/prompting.md`)

| Finding | Solution |
|---|---|
| "looks up at the clouds" animated a cloud, not the fox | the action names only the character's body |
| head raise from a still barely registers | one whole-body action; make a gesture the whole shot, described big |
| "walks slowly and calmly" did not travel; "runs quickly, a scamper" did | locomotion needs an energetic verb and a direction |
| a runner leaves a fixed frame | give the camera a job ("follows alongside") |
| Milo faced left, the prompt said run right | read the keyframe first; direction must match |
| "hops three times": the bunny teleported | no repeated fast actions |
| sleeping Leo woke up in one seed | state what must not change + its opposite in `negative_extra`; render 2 seeds (**confirmed**, Scene 1 v2) |
| Leo/Milo LoRAs: identity at every checkpoint; "side view walking" became a back view by step 750 | choose step 500 (confirmed a second time) |
| LoRA inside keyframe (I2V) shots: identity no better, the location drifted (new canopy, different forest) | render shots without LoRAs; keep LoRAs for text-to-video and for making stills (A/B Scenes 2, 3) |
| LoRA pose freedom shrinks with training (fox_v2 sleeps at step 500, sits awake later) | ~1000 steps; choose the earliest checkpoint that holds identity; train every story pose |
| keyframe with a sharp character over a blurred foreground object reads as floating | place the character on the in-focus plane |
| camera orbit around a still character: only ~30 degrees | turn the character instead |
| Scene 2: Milo ran away into depth, not across | explicit side-on geometry + sideways camera + negate "running away" (v2 testing) |
| Scene 2: a tilt-up revealed a canopy the keyframe lacked; the model invented a different tree | push-ins, or keyframes that contain what the move reveals |
| Scene 2 showed Leo's tree without Leo | keep character-tied landmarks out of frame or include the character |
| a secondary character with only a text sheet (butterfly) came out on-model | a specific sheet is enough for small, simple secondary characters |
| net prop design: all 6 candidates were nearly the same net (cream braided rope, square gaps, round knots), but every one filled the frame instead of showing the whole net | a simple prop is consistent from its sheet alone, like the butterfly; the design still fixes the reference (picked 1001). "Whole object in frame" is ignored for a net: fine, it is a material |
| location prompt drew props on a table | say the scene fills the frame, no backdrop |

### Tools and pipeline

| Finding | Solution |
|---|---|
| colour-key matting cut a notch out of the grey mouse on a grey-green backdrop | BiRefNet matting (MIT) |
| colour-matching a pasted character turned its white chest green | brightness-only matching; none at all for training data |
| a reframe step produced an image of empty floor, silently | tools assert their results (`design.py reframe`) |
| ffmpeg concat after trim fell back to 25 fps, every hybrid intro juddered | exact timestamps + forced 30 fps; count repeated frames on deliverables |
| a luma check with `-ss` seeking showed a false 48-level jump | measure by frame index |
| 97-frame clips cost ~250 s per step, could not finish in 3 h | 81 frames max; retime with RIFE |
| a keyframe composed on the login node took 15-25 min (Real-ESRGAN + BiRefNet on CPU) and blocked the shot | the keyframe recipe lives in the shot (`compose:` in story.yaml); `shot.py` composes it on the GPU node when missing; upscaled plate crops are cached |
| a wait loop `while pgrep -f "keyframe.py"` never ended: pgrep matched the waiting shell's own command line | wait on the output file (timestamp or existence) or a PID, never on `pgrep -f` of a pattern the loop itself contains |
| ffmpeg minterpolate warped fast motion; lanczos upscale was soft | RIFE (MIT) + Real-ESRGAN (BSD-3) |

### LUMI and training

| Finding | Solution |
|---|---|
| deepspeed/apex/aiter in the container break model imports | stubs (default venv), `sitecustomize.py` hider (musubi venv) |
| musubi-tuner and the generation code need incompatible library versions | two venvs in one container (`FELTWILLOW_ENV=musubi`) |
| training both Wan experts in one run: 11-13 s/step (28 GB swapped per expert change) | one LoRA per expert, trained in parallel: 2.6-3.5 s/step |
| accelerate aborted in multi-task jobs ("MASTER_ADDR") | unset Cray PMI variables (`lora/musubi_env.sh`) |
| work launched with `srun --overlap` died when the host job ended | submit every workload as its own job's task |
| GPU index k inside an overlap step is not task k's GPU | never assume; measure |
| musubi flag mismatches (boundary int; `--lora_weight`; `--save_path` is a dir) | recorded in `CLAUDE.md` and scripts |
| LoRA merge on GPU ran out of memory | `--blocks_to_swap 10 --lazy_loading` |
| training could not survive a job ending | `--save_state`, automatic `--resume` |
| MIOpen cache in /tmp unwritable on some nodes | per-job/task cache on scratch |
| a dependent job (`--dependency=afterok`) was refused with `AssocMaxSubmitJobLimit` | dev-g's limit of 2 counts pending jobs too; submit the follow-up from a waiter once the first job has finished |
| an environment variable set by the caller was ignored | `lumi/env.sh` overwrote it; env files only set defaults (`${VAR:-...}`) |
| login node refused to memory-map a 28 GB file | streaming fp16 -> bf16 converter |

---

## B. What you may be missing

### 1. Historical scratch-retention warning (reported deadline: 30 March 2027)

The LUMI project's data is removed on about **30 March 2027**. Everything in
`work/` (47 GB: the chosen designs, character packs, LoRAs, rendered shots) is
git-ignored and exists **only on LUMI scratch**. The code is safe in git; the
assets are not.

*Recommendation:* back up the irreplaceable part regularly to your laptop:
canonical stills, `packs` clips, trained LoRAs, finished shots. Model weights
(~420 GB) can be re-downloaded and need no backup.
**Done:** `bash lumi/backup_assets.sh` lists the set (632 files,
9.4 GB on 2026-09-26: everything in `work/` except LoRA training states,
intermediate checkpoints and latent caches, plus the final and step-500 LoRAs
and the channel videos) and prints the `rsync` to run on your computer. Re-run it
after every session; rsync copies only what changed.

### 2. The narration should come before the video

Professional animation times pictures to a finished voice track, not the
other way round. Each shot here is at most 5 seconds and costs about 2 GPU
hours; a narration line that runs 9 seconds needs two shots, and you only
find out after rendering.

*Recommendation:* for each story, first produce the ElevenLabs narration per
scene, measure each line's length, then plan shots to fit. Before rendering
any video, cut an **animatic**: the keyframe stills (cheap, minutes on a CPU)
laid on the narration with the planned durations. It shows pacing problems for
free.
**Done:** `python production/animatic.py` cuts
`work/stories/<slug>/animatic.mp4` in seconds: chosen takes (`take:` on a
shot), keyframe stills where nothing is rendered yet, and a text card for
scenes without shots. Put narration at `audio/<slug>/sceneNN.wav` and each
scene takes its narration's length; the report flags scenes whose narration
needs more 5-second shots than they have. Today it runs 39 s with placeholder
timings: the story needs narration before it has a real length.
*(Later: narration lives at `work/stories/<slug>/audio/<lang>/sceneNN.wav`,
made by `voice/narrate_scenes.py`; per-line timing for v4 is planned by
`production/timing_sheet.py`; an animatic is run only on the owner's separate
request.)*

### 3. Who speaks, and how (dialogue)

Milo has a line ("Please let me go. Maybe one day I can help you too."). The
characters have stitched mouths, and Wan cannot lip-sync to audio.

*Recommendation:* decide the convention once for the channel. The simplest
that fits felt stop-motion: a narrator tells the story and reads the lines; the
character "speaks" with body language (paws together, a nod), mouth still. Avoid
tight face close-ups during spoken lines, which invite the viewer to expect
moving lips.

### 4. Two characters touching: the hardest shots are untested

Scenes 3, 4, 8 and 9 need contact: Milo running over Leo's paw, climbing his
mane, Leo's paw stopping Milo, Milo nibbling the net. None of that is tested.
Risks: identity blending between the two, Milo's tiny size (at 1/6 of Leo's
height in a two-shot he may be only a few dozen pixels high), and two LoRAs
active at once (untested; they can bleed into each other).

*Recommendation:* test one interaction shot early (Scene 3 "paw in front of
Milo"), before producing the easy shots. Use close-ups for Milo's moments
rather than wide two-shots.

### 5. Props are not designed yet

The rope net appears in scenes 6, 8 and 9 and changes state (ropes break one
by one). `design.py` handles characters and locations only.

*Recommendation:* design the net as a third kind of entity (canonical still,
frozen sheet), and plan its states (whole / one rope broken / open) as
separate keyframes.
**Started:** `design.py` handles props (laid flat on a contrasting deep-green
floor so it cuts out cleanly). The net's sheet was rewritten before its first
render to use positive words only (see prompting Rule 3.5). Designed: 1001
(`design/net/contact_sheet.png`). Next: the net's states as keyframes (falling
onto Leo, over him, one rope broken, open).

### 6. The trap scene is close to YouTube's own example of distressing content

YouTube's July 2026 clarification names "animals in distress followed by a
rescue" as an example of off-putting content. That is the shape of scenes 6-9.

*Recommendation:* keep the peril short and mild (the brief already says soft
rope, worried not suffering; keep it that way in every shot), make the roar a
call for help rather than something frightening (sound design matters here for
toddlers), never use the trapped lion in the thumbnail or title, and let the
kindness message carry the video.

### 7. Channel settings for children's content

*Recommendation:* mark every video **Made for kids** in YouTube Studio (legally
required for child-directed content; it disables comments and personalised
ads, and changes what end screens can do). Keep kids videos out of playlists
mixed with the channel's other content.

### 8. Reproducibility: model versions are not pinned

Each output's sidecar records prompt, seed and settings, but not the model
revision. Hugging Face repos can be updated, and the same seed could then give
a different image. Revisions in use on 2026-09-26:

| Model | Revision |
|---|---|
| Wan-AI/Wan2.2-I2V-A14B-Diffusers | `596658fd9ca6b7b71d5057529bbf319ecbc61d74` |
| Wan-AI/Wan2.2-T2V-A14B-Diffusers | `5be7df9619b54f4e2667b2755bc6a756675b5cd7` |
| Comfy-Org/Wan_2.2_ComfyUI_Repackaged | `ee6f4a40737a995bf5818954cfce6d59443b0f04` |
| Wan-AI/Wan2.1-T2V-14B (VAE, T5) | `a064a6c71f5be440641209c07bf2a5ce7a2ff5e4` |
| TensorForger/RIFE-safetensors | `78a62b7c2dd910536432d6c2c3a25e76f14fbf78` |
| Comfy-Org/Real-ESRGAN_repackaged | `5fd49b7b278836f48af63ecd314d0f98ab336105` |
| ZhengPeng7/BiRefNet | `e2bf8e4460fc8fa32bba5ea4d94b3233d367b0e4` (pinned in code) |

**Done:** `feltwillow/wan.py` (`REVISIONS`), `feltwillow/post.py`, the download scripts and
BiRefNet load these commits; sidecars record `repo@commit`. Verified that all
of them resolve offline from the local cache. Changing a revision is a
deliberate edit: re-render one known shot and compare before relying on it.

### 9. Time, not GPU budget, is the limit

GPU hours used: 9,030 of 250,000 (3.6%). A fable is cheap in budget. Wall
time is the constraint: `dev-g` allows 2 jobs of 4 GCDs, about 8 shots per
2.5 hours. A 3-minute fable is roughly 36 five-second shots; with ~50% retakes,
about 55 renders, which is about 17 hours of `dev-g` time spread over a few
days.

*Recommendation:* plan a story's renders in batches of 8, and lock the animatic
(point 2) first so renders are not wasted on shots that get cut.

### 10. One style for the whole channel

The style bible sits inside `story.yaml`. If future fables are meant to look
like the same series, the style should live in one shared file that every
story uses, and recurring characters would need one shared character bible.

*Recommendation:* decide whether Leo and Milo are a one-off or the channel's
recurring cast; if recurring, move style and characters to a shared place
before the second story.

### Historical open decisions (not the current owner decision list)

- ~~Leo's eyes~~: decided, black (the sheet now matches the images).
- Leo's look: 1003 (fluffy mane, chosen) or 1005 (felt-ball mane).
- The story brief stops mid-sentence at Scene 9; the rest of the scenes are needed.
- Narration convention (point 3).


## Current r004 contract

Owner-reported defects include teeth during Milo’s bite, an intrusive hand in S02 L003 and a missing visible image-top-right Leo paw in S08 L016. These require actual native/full-motion review; the latter exact-hash production block covers L016/L017/L018 while preserving historical scene selection. Shared endpoints do not guarantee matching generated joins. Automated crop/contour/mouth warnings are not semantic anatomy approval. Real art/word alignment/installed-host capability and video acceptance remain separately evidenced.

Read [sequence production](sequence-production.md) for the implemented grammar/runtime contracts and [the current work record](../stories/lion_and_mouse_v7/review/owner_sequence_feedback_r004/README.md) for exact story decisions, evidence and remaining blockers. No source or CPU pass grants artwork selection, spending, GPU execution or final-video approval.
