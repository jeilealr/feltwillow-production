# Lion and Mouse v6 — character material continuity, Scenes 05–08

This is a visual triage of the **25 active** Scene 05–08 candidates in the
14 October working tree, using the current scene contact sheets and selected
full-resolution frames. It is not owner approval of any frame. The contact
sheets remain the required navigation view and the active plan/manifest bind
their exact source revisions.

## Material authority

Leo's approved canonical is
[`full-body_leo_neutral_pose_r01.png`](../../character/characters/lion_and_mouse_v6/Leo/canonical/full-body_leo_neutral_pose_r01.png)
(SHA-256 `6b587c8ee2739767bb7af056ee3176ec3d2e698a5bed0e013263814ee8059545`).
Its softly lit coat and paws are pale honey-cream, the mane and tail tuft are
natural tawny/chestnut brown, and the surface has dense matte needle-felt
fibers. [`s08_p02_r04_candidate.png`](../../character/characters/lion_and_mouse_v6/interactions/keyframes/s08_p02_r04_candidate.png)
(SHA-256 `6897037efcb63903e98e7d5d7a87ffdd6267a1932cd5fec4a5f746e8faba7b55`)
is a useful *screen rendering comparison* under dusk light, not a replacement
canonical. Milo's approved canonical remains warm neutral-grey with a cream
muzzle/belly and fine felt. Both canonicals are byte-unchanged in this review.

Sunset should warm the sun-facing edge and exposed surfaces. It should not
turn the whole coat orange or replace fine felt with large, open yarn loops.
Judge pigment in softly lit midtones and shadows, not from the brightest rim.
Scene 05's owner-liked `s05_p01` remains the brightness/exposure standard; it
does not supersede the canonical character material.

## Frame-by-frame triage

“Review material” means a targeted edit is warranted **after** preserving the
current geometry, four-paw/toe anatomy, expressions, tree roots and camera.
“Monitor” means the visible warmth may plausibly come from the sun and needs
full-resolution comparison before replacement. No row below is promoted to an
approved replacement.

| Scene | Active frames | Observation | Material action |
| --- | --- | --- | --- |
| 05 | `s05_p01_r02` | Establishing scale and distant Leo make pigment judgment uncertain; scene light is strongly warm. | Monitor; keep current scene geography and tonal benchmark. |
| 05 | `s05x_p01_r02`, `s05x_p02_r02` | Sleep closeups show warm coat, with less obvious material drift than the later reaction closeup. | Compare shaded coat/fiber at full size before any edit. |
| 05 | `s05x_p03_r02` | Forepaw insert has enlarged warm fibers relative to canonical paw. | Review material; preserve paw shape and toe count. |
| 05 | `s05_p02_r02`, `s05x_p05_r01` | Warm golden light is credible, but coat midtones are more orange than canonical. Milo remains recognizably grey. | Review material; preserve root, Leo paw and Milo trajectory. |
| 05 | `s05_p03_r10`, `s05_p04_r08` | Leo coat/mane read more orange/coarse than the canonical, especially at the face/paws; these shots also carry recent anatomy corrections. | Review material without changing pose, gaze, paw or root. |
| 05 | `s05x_p04_r08` | Clear closeup drift: orange coat and visibly larger open mane/fur loops versus canonical and `s08_p02`. | High priority material correction. |
| 06 | `s06_p01_r05`, `s06x_p01_r02` | Wide shots are warm; small on-screen Leo limits reliable fiber judgment. | Monitor at full size; preserve newly aligned Scene 05/06 background. |
| 06 | `s06_p02_r07`, `s06_p03_r04` | Leo's coat reads orange in midtones, with coarser fibers in the closer view. Milo's grey stays generally recognizable. | Review material; retain corrected Milo arms and all support paws. |
| 07 | `s07_p01_r02`, `s07_p02_r03`, `s07_p03_r02`, `s07_p04_r02` | Repeated two-shot family carries the orange Leo coat/coarser felt appearance into the conversation. | Review as one material-consistent family; preserve each story beat. |
| 07 | `s07x_p01_r01` | Leo portrait is warmer than the canonical, but is an owner-liked reference with usable character shape. | Preserve original; consider only a strictly geometry-preserving material edit. |
| 07 | `s07x_p02_r01` | Milo-only portrait: neutral-grey and fine felt remain reasonably close to canonical. | Keep for this material pass. |
| 08 | `s08_p01_r02` | Clear Leo coat/mane shift to saturated orange/coarser loops compared with the immediate `s08_p02` closeup. | High priority material correction. |
| 08 | `s08_p02_r04` | Leo's lit and shaded material is the preferred on-screen comparison. | Preserve; comparison only. |
| 08 | `s08_p03_r03`, `s08_p05_r04` | Milo-only frames; no comparable color/texture drift apparent in the sheet. | Keep for this material pass. |
| 08 | `s08_p04_r03`, `s08_p06_r02` | Leo looks closer to the canonical; some warmth is consistent with the dusk light. | Monitor, no automatic replacement. |

The previous Scene 05 style swatch (`s05_p01_style_texture_swatch_r03.png`)
visibly contained Leo's warm-lit paws, body and mane, and its metadata assigned
it felt fiber-scale authority. The process-level effect is **an inference**:
the model could blend that warm character crop with the canonical and carry
orange/coarse felt into later scenes. The swatch reference is now a 480 × 480
environment-only crop of the *same preserved owner-liked master*:
[`s05_p01_environment_swatch_r04.png`](../../character/characters/lion_and_mouse_v6/interactions/keyframes/.review/history/s05_p01_environment_swatch_r04.png)
(SHA-256 `677887b26ac35cb673771f58282120fa156d4e904cdf5aa01e5bfe19ba1371e0`).
`visual_bible.json` and `keyframe_plan.py` now state the authority boundary
explicitly: canonical for character pigment/fiber; swatch for illumination,
exposure, contrast and environmental finish. The 96-frame prompt contract was
rebuilt with this source. The old swatch and master remain in history.

## Image edit calibration

Two built-in imagegen edits were made to test the revised target:

| Source | Material trial | Result |
| --- | --- | --- |
| [`s05x_p04_r08`](../../character/characters/lion_and_mouse_v6/interactions/keyframes/s05x_p04_r08_candidate.png) (`ff4b4ab5facf6d345e35f00d6aa2ea279671e1dfd53d87ce59553898410479c8`) | [`s05x_p04_material_r01_candidate.png`](../../character/characters/lion_and_mouse_v6/interactions/keyframes/.review/material_calibration/s05x_p04_material_r01_candidate.png) (`815f6bc862edf1f58822c66959221bdf49d6399855a168c8dc51d74dc938f0c3`) | Pigment/fibers improve, but Leo's framing/pose shift. Calibration only. |
| [`s08_p01_r02`](../../character/characters/lion_and_mouse_v6/interactions/keyframes/s08_p01_r02_candidate.png) (`add1e8fd434aacb94f5f79ed7a3a4a737a62ae440d148d96877e8cb1f8cce925`) | [`s08_p01_material_r01_candidate.png`](../../character/characters/lion_and_mouse_v6/interactions/keyframes/.review/material_calibration/s08_p01_material_r01_candidate.png) (`02f2d52e42151b8f2f403fc1fcf82b1412cd3eab90690945688e4caabfb99b2e`) | Pigment/fibers improve, but Leo/Milo placement and tree composition shift. Calibration only. |

These 1672 × 941 trial PNGs are deliberately outside the active keyframe
directory. They must not be renamed into the 1920 × 1080 production sequence,
adopted by `revise_keyframe_candidate.py`, or shown in the `current/` contact
sheets **as active frames**. The separate
[`current/material_color_comparison.png`](../../character/characters/lion_and_mouse_v6/interactions/keyframes/.review/contact_sheets/current/material_color_comparison.png)
now shows them side-by-side with the active originals and labels their rejected
status. The existing active candidates are the safer continuity baseline until
a targeted revision passes full-resolution pigment, texture, limb/toe,
camera/scale and background checks. When one does pass, save it as a new
version-local revision, adopt it through the revision tool, rebuild the
`current/` contact sheets, and check the sheet manifest.
