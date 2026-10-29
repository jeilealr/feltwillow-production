# S01–S08 inputs for a LUMI video pilot

`INPUT_MAP.json` is a **derived, exact-hash inventory**, generated from the
current `audio_visual_plan.json` and scene selection/binding records. It lists
53 production sequences, 68 recorded audio lines, ordered image uses, aliases,
edges, prompts and the three-axis classification. `s01_opening` is an alias of
`s01_empty_hold` and must **not** be rendered a second time. A selected still
is a source input, not a reviewed video take or permission to submit a job.

## Obtain and verify the bytes on LUMI

1. Pull the `wan-new-image-approach` branch and check its HEAD. Run the
   inventory verifier from the trusted checkout:

   ```sh
   python -m production.lumi_s01_s08_inputs --repo . --verify stories/lion_and_mouse_v7/handoff/lumi_s01_s08/INPUT_MAP.json
   ```

2. The selected PNGs and audio **metadata JSONs** are tracked by Git. The 68
   line **WAVs are Git-ignored and a pull will not supply them**. Copy only the
   files named in `AUDIO_FILES.txt` from the Mac checkout to the same relative
   paths under the LUMI checkout. For example, run on the Mac, replacing the
   destination with the real LUMI host and checkout path:

   ```sh
   cd /Users/lealroja/Documents/feltwillow/feltwillow-production
   rsync -av --files-from=stories/lion_and_mouse_v7/handoff/lumi_s01_s08/AUDIO_FILES.txt ./ USER@LUMI:/REAL/PATH/feltwillow-production/
   ```

   Re-run the verifier on LUMI. It checks every WAV, metadata JSON, selected
   PNG and the authored plan against the map. Do not substitute similarly
   named media or re-record dialogue to satisfy a missing hash.

## Use the map correctly

- Each `sequence` names its ordered `uses` and `edges`. `source_status` is
  `selected_exact`, `alias`, or `missing_or_unselected`. An alias reuses the
  preceding named source; it is **not another Wan call**. A `cut` is editorial;
  never interpolate across different views or actors.
- S01 L001 and S02 L002 are separate same-image environment holds. Use each
  selected image at both endpoints of **its own** hold; never pair the S01
  forest directly with the S02 shadowed forest.
- One-image individual shots use the selected PNG as `image` and
  `last_image=None`. Connected actions feed each distinct adjacent state as
  a real pair boundary. Preserve source order, camera/background and actor
  scale. Do not skip contact or action keys to save GPU time.
- `audio_lines` gives exact line WAVs, speaker, transcript and PCM sample
  counts. Line audio does not prescribe equal video-piece lengths. Use the
  reviewed scene intervals, gaps, phrase markers and frame allocations in
  the sequence pipeline before freezing a render packet. NARRATOR never
  drives character lip-sync; speaking portraits require the V7 dialogue
  workflow after selecting a stable raw take.
- The two unselected S01 tiny-bite pickup uses remain explicit. Selected
  PNG availability alone does not clear known S02/S03/S05/S06/S08 contact,
  background, portrait or paw review gates. Run scoped readiness for each
  packet; do not turn an inventory row into `video_ready`.

## Production path

Read `docs/portable-sequence-production.md` and actual `--help` output for
`production/sequence_package.py`. Verify the LUMI Wan/ROCm environment,
model/config hashes, storage and Slurm settings. Freeze only eligible pieces,
build and verify exact-input packages, and run CPU `worker` preflight first.
An actual GPU operation additionally requires a separate exact-package owner
authorization and a durable external journal with zero automatic retries.
Use `lumi/sequence_job.sbatch` for an authorized operation; do not use the
legacy bulk render loop. Return resulting bytes and receipts for full-motion,
join, mouth and owner-take review. No complete S01–S08 film is claimed here.

Regenerate after any selection or audio-plan change on the machine holding
the recorded WAVs:

```sh
python -m production.lumi_s01_s08_inputs --repo . --out stories/lion_and_mouse_v7/handoff/lumi_s01_s08/INPUT_MAP.json
```
