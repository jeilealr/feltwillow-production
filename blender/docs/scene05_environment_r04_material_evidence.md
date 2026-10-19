# S05 r04 material evidence — 19 October 2026

**Preservation note, 19 October 2026:** Unavailable historical/local media links below are retained as code paths. Recover only exact historical bytes through the cleanup receipts/Git history or the verified local archive; these paths are not active generation authorities. Original dated results remain in source history.

The delivered r04 hero kit is **native procedural wool shading plus static
geometry/fibers**. It is not a full PATINA PBR material. No new provider request,
upload, retry or spend occurred. Old packed data are retained in the candidate;
the additional height test below was render-only and is not saved into r04.

## Evidence ladder

| Level | Verified evidence | Boundary |
|---|---|---|
| Provider receipt | Existing `patina_trial_01_receipt.json` records one completed `fal-ai/patina/material/extract` request, ID `01a14f67-38b6-75c2-a13d-7bbacd6ce06c`; source/output hashes match local bytes. | Historical recorded provenance, not account/billing authentication. Actual charge remains unknown. The old swatch provenance's “no upload yet” is stale relative to this receipt. |
| Available image | r03 safe-copy audit finds a packed 1024×1024 Non-Color height.png, 802207 bytes, SHA256 `a2dd640baaf3db07d80b37978f8a798402635ba44a1aa5d4dca8de4d8bad0563`. | One height image is not a full PBR set in the environment. Separate normal/roughness files exist on disk but are not thereby used. |
| Paths | Original library's `//../../materials/leo_felt_patina_trial/height.png` resolves to the existing local asset. | The relocated safe copy reports an absent external path because its base directory changed; packed bytes remain available. This is not a missing original dependency. |
| Graph/assignment | In r03 the image is output-reachable in GT_leaf_olive, GT_leaf_sage, GT_moss_wool, GT_olive_grass_felt, GT_stone_grey_taupe and GT_wool_bark_ridge. | Node-level reachability is potential contribution. Slot counts include hidden and superseded objects. It does not prove camera-visible benefit. |
| r03 main surfaces | R03_bark_compressed_wool → OAK_MAIN; R03_path_matted_earth → SURF_PATH; R03_stone_heather_felt → two hero rocks: no image nodes. | Those main surfaces are procedural, regardless of a packed PATINA image elsewhere. |
| r04 main surfaces | R04_WOOL_GROWTH_FOLDS, R04_CONTINUOUS_MATTED_CLEARING_EDGE, R04_HEATHER_SLATE_WOOL, moss and leaf families: native procedural recipes with real geometry/curves. | No new maps. Provider images retained in hidden source materials do not constitute r04 hero use. |
| Rendered contribution | Same-light native shader A/B and a separate existing-height-only trial, with render hashes and exact changed inputs. | These are local single-view still tests, not full-material or temporal qualification. |
| Visual success | Dense stone, moss cushions and cut leaf edges improve felt recognition. Broad trunk/root and plants remain weak. | No beauty approval or owner acceptance. |

## Kit and controlled tests

The reusable craft kit (`../assets/environments/great_tree/great_tree_craft_kit_r04.blend`)
was rendered under neutral and dusk light **before distribution**. It includes a
curved bark/root, shallow matted transition, unified moss cushion, heathered
rock and three thick cupped leaf families. Object coordinates attach detail to
each asset. Seed 510400. Sparse curved fibers supply selected silhouette pile;
sheen and bump alone do not. The kit is stronger than its full-world integration.

Native shader A/B (`../renders/scene05_environment_r04/material_contribution_AB.png`):
same root camera, geometry, fibers, saved dusk rig/world, exposure, Standard/None
transform, 1280×720, Cycles CPU, 40 samples, seed 510400 and denoising.
A removes procedural family color variation, bump/normal and sheen; B is the
delivered shader. Ground retains the earth/grass transition mask in A, with
flat family-color inputs. This tests **combined native shader contribution**,
not bump alone, a geometry comparison, or PATINA. The scene is never saved by
the review script. B visibly improves heathered stone, matted ground and woolly
root shading; root shape still reads as an overly regular rod.

Existing-height A/B (`../renders/scene05_environment_r04/existing_height_contribution_AB.png`):
A is the same native B render above. The extra B adds only the existing packed
height to OAK_MAIN and ROOT_APPROACH_A via a chained Bump: Object/BOX coordinates,
scale 4, strength 0.15, distance 0.003 BU, Non-Color. Same light/camera/geometry,
sampling/seed/denoising. No image color, normal or roughness map is added. Bump
does not alter geometry or fuzzy silhouettes. The trial is not saved in r04.

At full contact-view size and identical pixel crops, this height addition is
near-indistinguishable. Encoded channel differences average about
0.132/0.102/0.087 out of 255; these numbers document a changed render, not an
aesthetic score. **No meaningful felt improvement is established at these
settings.** Neither this result nor the historical receipt warrants a new paid
generation. Different regions/settings remain untested.

## Remaining material problems and decision

- Bark/root: directional relief survives, but broad forms remain smooth and
  molded; approach root is a regular tapered rod with an abrupt end.
- Moss: connected cushions replace flakes, but the two dominant strips are
  still too regular. More bump will not change that silhouette.
- Ground: coin carpet is gone; broad clearing can look airbrushed and sparse,
  with repeated comma-like fibers. Material variation needs authored scale.
- Leaves/plants: thick edges are useful; repeated squat crown masses with a
  few tabs do not create convincing plant construction.
- Rock: heathering works, but some curve fibers appear as a detached halo.
  Static surface sampling is not motion validation.

Recommendation: manually author principal root folds, buried root contact and
two or three convincing vegetation modules before additional scattering or
paid maps. No new PATINA proposal or spending request is made. If a later
swatch is justified, quote the exact endpoint/input hash/prompt/settings and
current cost for one operation before seeking approval.

Reports: `r03_material_audit.json`, `r04_linked_shot_material_audit.json`,
`material_AB_changes.json`, `existing_height_contribution.json`,
`comparison_metrics.json` under `blender/renders/scene05_environment_r04/`.
Independent material reviewer inspected kit, final stills and both A/Bs; verdict
was refinement prototype, no paid-map need established, no owner approval.
