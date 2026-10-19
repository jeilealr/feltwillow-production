# Felt materials, grooming and PATINA

## Define the look at three scales

**Macro:** sculpted masses, mane locks, feather/leaf silhouettes and deliberately handmade unevenness. **Meso:** compressed wool variation, short fiber clumps, seams and slight tonal variation. **Micro:** small attached fibers, roughness and subtle surface relief. Solve in that order. A dense hair system cannot rescue the wrong face, and a normal map cannot create silhouette fuzz.

Review at intended delivery resolution as well as close inspection. A material that looks excellent enlarged can shimmer or disappear in motion. Keep references to the approved style, not generic photoreal fur or knitted fabric. Needle-felt has a different visual structure from woven cloth; use a fabric tutorial for node techniques, not as the aesthetic authority.

## Controlled look-development sequence

1. Clay render: assess shape and lighting without texture camouflage.
2. Flat canonical color regions: confirm eyes, ears, muzzle, body, mane and tail assignments.
3. Roughness and restrained micro-bump: inspect under neutral light and a soft grazing light.
4. Sheen/grazing response: use only where it improves miniature wool; the Principled sheen layer models a fiber-like reflection effect, not actual hair geometry [B07](sources.md#b07).
5. Sparse attached silhouette fibers and selected clumps: compare with and without them.
6. Story lighting and camera depth of field: hold white balance and exposure fixed during comparison.
7. Short animated render: inspect attachment, aliasing, highlights, denoising and temporal stability.

Use object/rest-space or stable UV coordinates rather than world-space noise that slides through the body during movement. Fix procedural seeds. Keep density/length masks away from eyelids, mouth contact and other sensitive areas unless the design requires fibers there. Do not let procedural groom change the number or pattern of hero mane locks randomly per build.

## PATINA selection

The provider distinguishes image-to-PBR, generated/varied material, and extraction from a photo [P01](sources.md#p01), [P02](sources.md#p02), [P03](sources.md#p03). Use the actual current schema.

| Input situation | Candidate endpoint | Acceptance focus |
|---|---|---|
| Clean flat swatch already resembling the desired felt | `fal-ai/patina` | Preserve color; examine inferred maps |
| New repeatable texture required | `fal-ai/patina/material` | Tile edges, repeat artifacts, scale and unwanted structure |
| Character/set photograph contains the wanted surface | `fal-ai/patina/material/extract` | Isolate only the selected material before mapping |

Do not feed a whole lion portrait into a material generator and apply the result across the entire lion. It can embed eyes, shadows, highlights or mane shapes in an inappropriate surface. Extract a clean body or mane swatch; preserve the existing UV color atlas and region masks if they are already correct. Generated PBR maps are estimates, not measured material properties.

Record input hash, cropped region, endpoint/settings, request ID and returned maps. Check cost and get approval before generating. Start with one material patch, not a character-wide retexture. Never infer that a successful map download proves physically accurate, seamless or color-faithful material.

## Blender connection rules

Use color-managed base color; treat normal/roughness/height/metalness as data rather than color. Match the normal map's convention and tangent space to the UV set; use a Normal Map node rather than plugging RGB straight into a shader normal input [B08](sources.md#b08). Test with a lit sphere and the character patch. Do not blindly add two RGB normal maps.

For ordinary wool, keep the metallic behavior non-metallic; a predicted metalness map with shiny fibers is a candidate error, not an instruction to turn Leo into metal. Preserve intentional stylized eye/nose highlights separately. Avoid duplicating baked dark shadows with heavy AO and scene contact shadows. Normal/AO baking is optional optimization, not a required paid feature [B05](sources.md#b05).

Real displacement changes geometry and may change scale, silhouette, contact or render cost. Begin with bump where sufficient. If displacement is justified, test bounds, intersections and skin/groom attachments. A flat height prediction from a lit photo can contain lighting errors; never assume it is actual depth.

## Material scale and color invariance

Specify texture scale in the asset's documented units; check the size of visible wool structures against the canonical and the shot. The same material on a tiny mouse and a huge tree need not use identical UV tiling. Variation may exist within a bounded palette, but must not shift identity by scene. Do not use a global orange grade to make a dusk scene feel warm.

Compare base-color regions under neutral light with the same render transform, then under selected daylight/dusk. Different illumination legitimately changes pixel color; no shader can guarantee identical RGB under all lighting. The invariant is the material definition and intended appearance, supported by calibrated comparisons, not a blind sampled-hex equality test.

## Feather, scale, shell and human variants

Keep the medium consistent while adapting construction: a bird may use layered felt feather shapes with sparse fibers, a fish stitched/felt scale shapes rather than wet metallic scales, a turtle a solid crafted shell, humans felt skin/hair/clothes. Do not assume every surface needs long fur. Clothing can be rigged or shape-driven for the restrained style; realistic cloth simulation is a choice, not a default.

## Temporal QA

Render a slow camera move and a deforming pose. Watch for fiber swimming, opacity sorting, popping cards, too-thin strands, noisy sheen, over-sharp bump, glossy plastic highlights and denoiser boiling. Reduce microdetail that cannot survive delivery resolution. Never vary a random seed by frame for organic life. Store a plain-material fallback to isolate whether a fault is geometry, light, groom or denoising.

## Required material-evidence audit

Before adding maps or declaring felt success, read [material evidence](material-evidence.md) and use `assets/templates/material-look-review.md`. Report provider provenance, packed/file presence, graph connection, assignment, rendered contribution and visual success separately. Tune the environment's distinct material families, not a single generic rough-noise material for every surface. For reference-inspired environments, judge craft and material hierarchy rather than old-plate pixel equality.

## External material sources (1.3.0)

Before another paid material call, compare existing maps/procedural options with a small verified free sample from [asset sources](asset-sources.md). Follow [external intake](external-assets.md) for exact license, original-file and derivative provenance. Conventional PBR fabric, bark or ground is not a finished felt look; prove the adapted surface at shot distance using material-evidence.md. Do not upload third-party assets to fal without separate permission.
