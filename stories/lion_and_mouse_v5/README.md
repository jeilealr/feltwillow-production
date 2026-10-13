# The Lion and the Mouse, v5

The historical Lion and Mouse visual/render production. The owner made the v5 stills (ChatGPT Pro) from the v4 prompt records;
v2 to v4 were deleted on 2026-10-06 and remain in git history (`git show b880c23:stories/lion_and_mouse_v4/...`).

Status (2026-10-11): narration done (English, 11:23.7). The tracked review covers an initial
62-shot, 186-take batch and records a later three-seed `s05_tumble` bridge, giving 63 runtime
shots and 189 expected takes. The local v5 `work/stories/lion_and_mouse_v5/shots/` directory is
absent from this checkout, so actual MP4/sidecar validity cannot be confirmed here. The owner
still needs to select takes. Review: [RENDER_REVIEW.md](RENDER_REVIEW.md).

| File | What it is |
|---|---|
| `SCRIPT_REVIEW.md` | the owner's script, line by line |
| `dialogue_coverage.json` | the line list (narration input and line-to-shot mapping) |
| `SHOT_PLAN.md` | shot order |
| `visual_bible.json` | identities, camera setups, size anchors, plates |
| `prompt_manifest.json` | every image and video prompt record (paths rewritten from v4 to v5) |
| `prompts/*.md` | readable prompts, rendered from the bible |
| `TIMING_SHEET.md`, `timing_plan.json` | which shot covers which narration line |
| `story.yaml`, `runtime_inputs.json` | the runtime story for `production/shot.py`, exported by `production/export_runtime.py` with frozen keyframe hashes |
| `RENDER_REVIEW.md` | review of the rendered clips |

Images: `character/characters/lion_and_mouse_v5/` and `character/locations/lion_and_mouse_v5/`
(same file names and revisions as v4). Generated audio and clips (not in git):
`work/stories/lion_and_mouse_v5/`.

Re-export the runtime story (after an image change):

```bash
python3 production/export_runtime.py --manifest stories/lion_and_mouse_v5/prompt_manifest.json \
    --story lion_and_mouse_v5 --images lion_and_mouse_v5
```

Known lint state: `python3 production/image_prompts.py --story lion_and_mouse_v5 lint` reports 70
errors for v3 reference images named by the expression records (deleted history; only needed to
regenerate those expressions) and 8 warnings for images the owner renamed in v5.

Runtime audit (2026-10-09): the 86 frozen `work/.../keyframes/` copies named by
`runtime_inputs.json` were missing after the owner renamed working copies. Their
86 source images all existed and matched the recorded SHA-256 values, so the exact
frozen copies were restored. All 126 runtime shot endpoints now exist; `shot.py
--dry-run` passes in scenes 1, 8 and 16. Re-export with the command above resolves
those exact hash-verified sources and now names the v5 manifest in `story.yaml`.
It does not generate or alter the 189 historically reported takes. The old take sidecars lack
input-image hashes; the renderer now refuses to silently treat them as a match
on a future render run. Review and preserve an existing take before replacing it.

The prompt packet still has six `accepted` records whose named target files are
absent: `M_SIDE_R`, `M_SIDE_L`, `M_BACK`, `s08_milo_surprised_start`,
`s08_milo_surprised_end`, and `s12_runs_end`. The three shot endpoints have
separately recorded, hash-verified source files in `runtime_inputs.json`; this
does not make the missing manifest targets available for prompt regeneration.
The 70 legacy-reference lint errors and 8 rename warnings above also remain.
