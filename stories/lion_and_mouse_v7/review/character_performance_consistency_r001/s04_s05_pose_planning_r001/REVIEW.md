# S04–S05 Milo candidates — 15 saved, one unresolved request

The owner approved the exact 16-request Milo-only operation. Fifteen transparent PNG candidates and their immutable same-basename sidecars are saved under `character/characters/lion_and_mouse_v7/Milo/poses/`. All 16 requests were attempted once; no retries. Request 11 (`milo.trip.rear_paw.3q:forward_pitch`) returned a connection error without an image or provider request ID. Its submission/billing outcome is unresolved; do not resubmit automatically or claim it was free. OPERATION.json, AUTHORIZATION.json and EXECUTION.json preserve the exact operation and journal.

All 15 outputs are `candidate_pending_owner_review`. Their actual hashes, alpha channels, dimensions, creation inputs/settings and audio-image associations are recorded. Generation does not approve anatomy or scene use. Original canon, source PNGs, audio and the 26 selected S01–S03 images remain unchanged.

## Review the actual candidates

Use the existing pose-card gallery, with checkerboard transparency, native links, canonical measurements and local line audio:

- S04: `http://127.0.0.1:8765/stories/lion_and_mouse_v7/review/character_performance_consistency_r001/pose_library/review.html?q=S04`
- S05: `http://127.0.0.1:8765/stories/lion_and_mouse_v7/review/character_performance_consistency_r001/pose_library/review.html?q=S05`

The gallery has 37 current performance images: 22 previously selected assets plus these 15 new candidates. The missing forward-pitch request is called out explicitly, not shown as a fake image. The trip family is ordered approach → contact → missing forward pitch → tipping. Native fit-to-card display is not anatomical normalization.

`VISUAL_OBSERVATIONS.json` separates observations from verdicts. In particular, the contact key leans backward relative to the later forward motion; the running passing phase needs gait review; nose-landing contacts need the sleeping-Leo layout. All comparative anatomy/width/cream-patch/paw measurements remain pending. No pose has been automatically repaired or passed.

## Story/staging contract

S04 has five independent shortcut shots with style/material references, without mandatory repeated pixels. S05-L001 reveals sleeping Leo and the Great Tree; L002–L004 are independent detail framings of the same sleeping pose. L005–L009 use one planned locked background/camera and fixed sleeping Leo. Milo moves root → rear paw → flank → nose; he is not frozen in position. Explicit same-location cuts currently separate line keys; key timing remains pending alignment.

L008 has four authored keys: approach, rear-paw contact, forward pitch, tipping. Its trip event remains once at I02; later L008 keys retain unbalanced contact. L009 retains its original airborne support loss, tumble, roll and nose-landing phases. No equal timing windows or new world events were invented. Rear-paw tripping remains separate from the later S06 front-paw block.

L010 is an eye-opening Leo portrait pair; L011 is his question portrait. They share head/neck/upper-chest geometry and retain full mane/ears. Milo persists at Leo nose contact outside the crop; narration does not move mouths and dialogue uses later explicit lip-sync.

## Leo next

The owner confirmed the displayed local Leo canonical. `owner_leo_canonical_reconciliation_r001.json` now binds its exact actual SHA-256; the earlier inherited approval is preserved historically and the PNG was not changed. Visible Leo measurement baselines remain observations, not newly adopted design targets.

Two foundation requests are prepared in `leo_foundations_next_r001/OPERATION.md`: one full sleeping body and one portrait base, no retries, cost unknown. They are NOT authorized/submitted. Closed/open-eye variants will be proposed using exact reviewed portrait-base bytes, rather than independently rebuilding each portrait. This batch generated Milo only; no scene backgrounds, audio, video or GPU jobs were produced.

## Final verification

All 223 tests pass in the feltwillow conda environment. Planning and performance validators pass. The live gallery returned HTTP 200 and S04 WAV byte-range playback returned HTTP 206. Fifteen PNG/sidecar hash pairs and all 26 S01–S03 selected-image hashes were checked. No staging, commit or push was performed in this task.
