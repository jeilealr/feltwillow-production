# Running on LUMI

Account `project_465002727`. Everything runs inside the LUMI PyTorch ROCm
container through `lumi/run_in_container.sh`, which activates the venv at
`ltx_env/venv` (rebuild with `lumi/setup_env.sh`).

```bash
W=lumi/run_in_container.sh   # from the repo root
$W python production/shot.py --help          # anything, on a login node
```

## Render inventory and generated-file root

`FELTWILLOW_WORK` selects the generated-file root; if unset, it resolves to
`<repo>/work`. Both `production/shot.py` and the LUMI bulk render/backup
scripts use this same resolved path. Set it to an absolute directory visible
inside the container before rendering. The scripts print the resolved root.

Before submitting GPU jobs, run:

```bash
FELTWILLOW_WORK=/scratch/project_465002727/jelealro/work \
  bash lumi/render_story.sh lion_and_mouse_v5 --inventory-only
```

The command writes `<work>/tasks/<story>_render_inventory.json` with a
complete/missing/stale result for every seed, plus
`<work>/tasks/<story>_commands.txt` for shots missing seeds. A clip counts
as complete only when its JSON sidecar matches current keyframes, prompts,
model and Lightning revisions, LoRAs, seed and render settings. Older fast
sidecars that did not record the Lightning revision also fail this audit.
Existing media with a
missing or mismatched sidecar is stale: the bulk script exits before any
submission and never overwrites it. Review and explicitly move stale output
aside before running the bulk command without `--inventory-only`. The
driver repeats the audit after each render round and exits nonzero if seeds
remain missing.

For a backup preview, run `FELTWILLOW_WORK=/scratch/... bash
lumi/backup_assets.sh --dry-run`. It prints the exact work and character
source roots and file counts without invoking rsync or writing persistent
lists. The normal command writes separate relative file lists under the
resolved work root and prints two rsync commands: one rooted at work, one at
the repository. This keeps an external work root in the backup.

## GPU jobs

- **Partition**: `dev-g` starts almost immediately but allows **2 jobs per user**
  and **3 h** per job. `small-g` / `standard-g` allow days but had 700–1000 jobs
  queued when this was written.
- **Several tasks in one job**: a `dev-g` job may use several GCDs of a node.
  `lumi/run_tasks.sbatch` runs one command per line of a task file, one GCD
  each, in parallel:
  ```bash
  sbatch --ntasks=3 --gpus-per-node=3 --mem=400G lumi/run_tasks.sbatch tasks.txt
  ```
  Each task reports `ROCR_VISIBLE_DEVICES=0`: that is its *own* GCD renumbered
  inside its task cgroup, not a shared device. Verified: the three tasks of job
  22348370 held `renderD133`, `renderD130` and `renderD131`.
- **Host RAM is the limit for Wan**, not VRAM: two 14B experts plus the text
  encoder are offloaded to host memory (~80–100 GB per task, ~34 GB VRAM). About
  4 Wan tasks fit on one 512 GB node.

## Measured times (one MI250X GCD)

| Work | Time |
|---|---|
| Wan A14B model load (fp32 on disk → bf16) | 10–21 min |
| Wan I2V 720p, 40 steps: 33 / 41 / 81 frames | ~25 min / ~42 min / ~2 h |
| Wan 720p, 97 frames | ~250 s per step: does not fit in 3 h |
| Wan T2V 81-frame shot, including load | ~2.5 h |
| RIFE + Real-ESRGAN, 10 s clip | ~20 min |
| Procedural ident, 10 s 1080p60 | ~2 min on 8 CPU cores |
| Score synthesis | seconds |

## Gotchas already solved

- No ffmpeg on PATH: `feltwillow.media.locate_ffmpeg` falls back to imageio-ffmpeg's binary.
- `deepspeed`/`apex` import failures: see `lumi/stubs/` and the "LUMI and
  training" table in `docs/findings-and-risks.md`.
- `Cannot open database file: /tmp/gfx90a…ukdb`: MIOpen cache moved to scratch,
  one directory per job *and task* (`lumi/env.sh`).
- tqdm progress bars do not flush through `srun`; a job that looks silent may be
  computing: check `rocm-smi` with `srun --overlap --jobid=<id>`.
- **Check deliverables for repeated frames**, not just duration. ffmpeg's `concat`
  after `trim` can lose the frame rate and fall back to **25 fps**; a later 30 fps
  step then resamples 30 -> 25 -> 30 (one frame in six dropped, one in five
  repeated: judder through the whole video, while duration still reads 10.00 s).
  Fix: `settb=1/30,setpts=N` on every branch plus `-r 30 -fps_mode cfr` (it was
  applied in the old intro's hybrid_cut.py, now in the git history). Count exact repeats of consecutive frames to verify; the
  only legitimate repeats are intentional holds and pure-white frames.
- Measure luma across a cut **by frame index over the whole file**. `-ss` seeking is
  not frame-exact and made a continuous join look like a 48-level step.
- Clips longer than 81 frames need `pipe.vae.enable_tiling()` and cost
  quadratically; prefer 81 frames and retime with RIFE.
