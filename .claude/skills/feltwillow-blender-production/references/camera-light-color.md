# Camera calibration, lighting and color continuity

**Select the design mode first:** Read [environment direction](environment-art-direction.md). Use [environment image matching](environment_image_matching.md) only for `plate_match`; evaluate `reference_inspired` and `original_design` against their authorized brief. A blockout can be structurally valid while failing the handmade look.

## Establish the mode-appropriate view first

In `plate_match`, reconstruct the approved view. In `reference_inspired` or `original_design`, compose useful views of the new candidate and verify its retained story requirements; old-image residuals are not the acceptance target. A single image admits many possible 3D scenes. Fit a usable reconstruction for the intended shots, and mark hidden forms as inferred. Establish ground orientation, horizon and major landmark correspondences before detailed geometry. Perspective vanishing-point tools can help when straight parallel structures exist; organic painted/generated scenes may not support an exact camera solve. Do not report a guessed lens as measured fact.

Record camera type, transform, lens or orthographic scale, sensor fit, image aspect, shift, clipping, focus and depth-of-field settings. Use exact render resolution in comparisons. Treat a zoom/crop differently from moving the camera: a crop preserves perspective, a dolly changes it. Focal length and camera distance can trade off in a single view but yield different motion parallax.

## From existing 2D staging to 3D

Normalized contact `(x,y)` is a projection target. `depth_t` in the current staging file is a planning parameter, not Blender Z or meters. Cast calibrated camera rays onto an explicit support surface, then compare projected positions and neutral anatomical dimensions. If the 2D targets cannot all be satisfied with one coherent camera/world, report the inconsistency and propose a scoped calibration decision. Never deform the character or rescale a landmark per frame just to fit every pixel.

For physical scale, compare neutral anatomical markers at known depth. Pixel height changes with pose, occlusion and perspective; annotate standing-equivalent measurements separately. Preserve current approved perspective exceptions explicitly. Distant hills cannot serve as rulers for a foreground mouse.

## View families versus exact cameras

A label such as `medium_two` or `tree_dusk:medium_two` is a broad family, not proof of identical camera matrices or crops. Store an exact camera/setup revision and calibration for each distinct view. Share it only when the geometry and framing truly match. Use a stable family ID for organization plus exact settings/hashes for continuity.

For portraits preserve head, full ears/mane, shoulders and upper chest; exclude feet/lower torso/tail as the current owner standard requires. Use the same environment, now defocused, not a different generic forest. Keep eyes and important muzzle features in focus. Prevent DOF from hiding a bad model during diagnostic review.

## Lighting

Separate character material colors from illumination. Work first in neutral comparison lighting, then match the location's direction, softness, contrast, background exposure and white balance. For Great Tree dusk, retain cool/neutral ambient influence with localized warm sunset/rim contribution rather than a global amber wash. Use a day variant of the same geometry where appropriate, not a rebuilt scene.

Keep world/HDRI, light transforms, strengths, colors, exposure and color transform fixed within a setup unless a story light event says otherwise. A moving cloud card need not cast a moving dark shadow across Leo. Avoid automatic exposure changing between shots. Large soft sources and plausible miniature lighting are candidates to test, not a guarantee of the reference look.

## Color pipeline

Pin Blender version, view transform/look, display/output space, exposure and relevant OCIO configuration. AgX, Standard and a PBR-oriented neutral transform have different highlight behavior; choose by a controlled reference comparison, not by fashion [B12](sources.md#b12). Do not convert or grade twice. Treat scene-linear EXR masters differently from display-referred review PNGs.

Review imported base color with correct color-space interpretation. A material being too orange may come from light or view transform rather than the texture. Diagnose separately with neutral light and flat-color checks. Preserve artist-approved eye highlights without turning felt into glossy plastic.

## Mode-appropriate comparison evidence

For `plate_match`, produce reference/candidate at the same resolution with aligned landmarks, an optional overlay, and annotated residuals. For other modes, record intentional layout/camera changes and compare the craft, palette, narrative identity and candidate brief; use fixed new-camera before/after views, not a compulsory old-plate overlay. Compare silhouette, composition, material regions, lighting and depth separately. Pixel differences are useful diagnostics but not a scalar artistic approval: shadows and fiber microstructure may differ legitimately while a distinctive muzzle mismatch is unacceptable.

For 2.5D sets, add envelope-extreme renders and one slow camera move. For any new exact camera revision, record whether shared state joins remain valid and which shots need re-review. Never label a camera change as a character-scale correction.
