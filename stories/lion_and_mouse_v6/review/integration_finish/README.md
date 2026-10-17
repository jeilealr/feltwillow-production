# V6 focused integration — complete

The owner preferred trial C for `s04_p03` and authorized applying the same focused finish where needed. All 96 active frames were screened. 51 slots (39 distinct images) were trialled; **47 slots (35 distinct images) were adopted, 49 retained**. Four Scene 5 trials added no clear improvement to already integrated originals, so those originals remain selected. Deliberate duplicate frames retain identical finished bytes.

Open [owner_review.html](owner_review.html) for original/finish pairs. Selected images are already active; the four unselected trials are clearly labeled. The owner individually preferred C; the other 46 adopted slots were inspected and selected by the agent under explicit owner authorization. This does not claim individual owner inspection of every finish or new production approval.

`audit.json` records all decisions, original/current paths and hashes, comparison scope and counts. `adoption_paths.json` maps replaced paths to preserved originals and active revisions. Original PNGs are under `character/characters/lion_and_mouse_v6/interactions/sources/integration_originals/`. `before_adoption/` preserves original plans, selection and technical reviews. Earlier accepted geometry, scene exceptions and closing expressions remain unchanged.

`frames/<id>/` stores exact prompts, raw built-in ImageGen suggestions, bounded finishes, edit/protected-feature masks and hash-bound receipts. Trial C retains its own original receipt folder. Portraits and contact-sensitive frames transfer only smooth bounded lighting into original pixels. Other finishes use selected RGBA support and restore original central features and scenery. The net, knot contacts and Leo are protected. Raw generated backgrounds are excluded.

`verification.json` records pixel/metadata checks. Recheck with Pillow and numpy:

```bash
python3 stories/lion_and_mouse_v6/review/integration_finish/verify_finish.py
```

`update_review.py` only refreshes navigation. The completed `finish_frame.py`, `adopt_finish.py` and trial builder preserve processing provenance and refuse to overwrite this completed selection. Start a new scoped review for another pass. Historical composition metadata in `legacy_selected_compositions.json` and explicit inspected regions in `manual_regions.json` document older flattened sources; they grant no authority to restore rejected images.

The reusable [integration rules](../../../../docs/character-background-integration.md) preserve deterministic composition as the geometric base. Current selection hashes, boundary image pointers and 16 scene sheets are updated. Previous technical reviews are preserved as history; new-hash technical checks remain pending. No video-control implementation was changed. Temporary runs use `/scratch/project_465002727/jelealro/tmp`.

A subsequent owner inspection identified a bright facial mask seam in `s04_p02_r13`. The [scoped lighting repair](../milo_scene04_identity_and_lighting/owner_review.html) is now active as r14, with r13 preserved. The audit records this follow-up explicitly; original finishing receipts remain historical evidence. Pixel protection alone did not prove lighting continuity, and the reusable rules now require a native mask-boundary check.
