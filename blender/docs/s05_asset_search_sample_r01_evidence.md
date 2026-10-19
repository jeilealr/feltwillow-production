# S05 sample pilot r01 — detailed evidence and shortlist

**Useful stump study; no stock kit is approved for S05 integration.** The
existing native rock/moss/leaf construction remains the better baseline in
several areas. New maps did not automatically produce convincing needle felt.
This is an isolated test, not a new environment revision.

Skill **1.3.0** was read through `.agents/skills/feltwillow-blender-production`,
which resolves to the shared `.claude` source. Required external-assets,
asset-sources, environment direction and material-evidence modules were present.
No second skill copy, installation, login, paid operation, upload, commit,
production publication or scene migration occurred. Mode: `reference_inspired`.

Open the [isolated sample .blend](../../work/blender/external_assets/s05_kit_r01/tests/s05_external_craft_kit_r01.blend),
[neutral comparison](../renders/s05_asset_kit_r01/comparison_neutral_shot.png),
[dusk comparison](../renders/s05_asset_kit_r01/comparison_dusk_shot.png), and
[matched stump crop](../renders/s05_asset_kit_r01/stump_matched_crop.png).
All three stages remain in separate named collections; the adapted attempt
includes rejected rock/foliage components as diagnostic evidence, not approved
library content.

## Starting evidence and scope

Latest files found: `great_tree_environment_r04.blend` and relatively linked
`s05_environment_r04.blend`. Actual links, active material assignments, images
and sun visibility were inspected read-only with auto-execution disabled.
Current authority and prior S05 notes were read. Starting branch:
`feature/perceptual-world`, HEAD `fcea46b788f6df8423f84bf14e54169f15a383e3`.
Existing `.gitignore` modification and untracked Blender/skill/agent trees were
preserved. Current protected file hashes and all selected image hashes are
verified again at delivery.

The r04 hero trunk/root/path/stone use native shaders. The packed historical
PATINA height is present in older materials; r04's existing-height-only test
found negligible benefit at its tested scale/settings. That result is not a
blanket finding about every PATINA output. This sample reuses the existing
roughness map on one path test, bounded to roughness 0.82–0.98. Its individual
contribution is **not isolated**, so no map-specific success is claimed.

## Shortlist — exact sources checked, eight candidates maximum

| Candidate / creator | Current free tier / rights evidence | Intended role / effort | Decision |
|---|---|---|---|
| [Nature Kit 2.1 — Kenney](https://kenney.nl/assets/nature-kit) | Official 330-file kit; archive contains GLB, OBJ, FBX, DAE, STL. Packaged License.txt confirms CC0/commercial use; [support](https://kenney.nl/support). ZIP 10,537,521 bytes, HEAD bounded before transfer. | Selected stump, rock, leaf and bush bases; moderate topology/shape/felt adaptation. | **Adapt further:** stump only. **Reject current rock/plant adaptations.** |
| [Curly Teddy Natural — Rico Cilliers / colormass, Poly Haven](https://polyhaven.com/a/curly_teddy_natural) | Exact page CC0, community-unlocked 5 September 2025; free 1K–10K maps, Blend/glTF/MaterialX options. Four selected 1K JPG/PNG maps total 9,273,519 bytes; [license](https://polyhaven.com/license). | Plush relief/marling source for compressed moss; moderate scale/color/roughness adaptation. | **Adapt further:** modest surface contribution; raw plush too bright/coarse. |
| [Fabric 060 — ambientCG / Lennart Demes](https://ambientcg.com/a/Fabric060) | Official documented API returns free 1K JPG ZIP 8,646,092 bytes and larger variants; tags include tartan/plain/smooth. [CC0 license](https://docs.ambientcg.com/license/). | Conventional textile relief; wrong construction for nonwoven needle felt. | **Reject for this pilot; not acquired.** |
| [Moss 01 — Rob Tuytel, Poly Haven](https://polyhaven.com/a/moss_01) | Exact page CC0, model with alpha/maps, about 246K triangles. Free format/resolution choices; full selected payload not requested. | Realistic fronds/ground-cover; substantial simplification and felt conversion, alpha/geometry complexity. | **Reject for this small pilot; not acquired.** Native cushion is cheaper and more coherent. |
| [Stylized Nature MegaKit — Quaternius](https://quaternius.com/packs/stylizednaturemegakit.html) | Free Standard about 99 MB, OBJ/FBX/glTF; .blend source is paid. Pack CC0 claim conflicts with current [QAL v1.0 general terms](https://quaternius.com/license.html) restricting standalone original/modified asset redistribution. | Potential vegetation/root forms; moderate adaptation plus unresolved rights. | **Blocked; not acquired.** Owner approval and exact package clarification required. |
| [Felt Textile — Paco Salas, Blendkit](https://www.blendkit.com/asset-gallery-detail/77348e1a-2018-4a4f-b77d-cb80ec6c7402/) | Free 257.1 KiB material, Royalty Free; account/add-on acquisition flow. [License distinctions](https://www.blendkit.com/docs/licenses/). | Relevant felt lead, but outside automatic CC0 acquisition permission. | **Blocked; not acquired.** Free price is not CC0. |
| [Stump 12 — Martin Košťál, Blendkit](https://www.blendkit.com/asset-gallery-detail/45888695-2dcc-40de-857d-7ebd79dd2071/) | Free 15.9 MiB, 1,810 polygons, Royalty Free, scan/cleanup tags. | Stump base, moderate cleanup/retopology and full felt conversion. | **Blocked; not acquired.** No login/add-on attempt. |

All five requested providers were checked. Asset-specific CC0 labels plus
packaged/download evidence controlled acquisition; provider-wide descriptions
were not substituted for exact rights. Quaternius conflicts were preserved,
not resolved by choosing the more permissive label. Commercial render,
modification and raw redistribution are separate decisions in the two pending
[registry records](../asset_library/registry/).

## What was downloaded and inspected

**Two packages; 19,811,040 asset bytes (18.9 MiB)**, plus small API metadata,
against five-package/500 MiB caps. Kenney archive expansion totals 29,443,234
bytes; only four GLBs plus License.txt (40,511 bytes) were extracted. Including
all selected Poly Haven maps gives a conservative expanded-payload upper bound
of 38,716,753 bytes (36.9 MiB), below 1 GiB. No need to acquire more assets to
use the allowance. Exact original/selected-file hashes and bounded download
plans are retained in ignored `work/blender/external_assets/s05_kit_r01/`.

GLB JSON was inspected before import: embedded mesh data, no image dependencies,
external URI dependencies, scripts, animation or required add-ons. Blender
import checked UV layers, material slots, normals, units and negative scales.
All selected meshes have UVMap; alpha is opaque, no cutout cards. Source glTF
meter convention was explicitly normalized to miniature BU for samples only.
No downloaded `.blend` or executable was used. Safe scripts/imports run with
`--disable-autoexec`.

The rock has 104 coincident split vertices; hypothetical welding closes its
base topology, but **no repair was applied or visually validated** after the
render cap. The leaf mesh remains open after a hypothetical weld, so it needs
actual thickness/connectivity design before smoothing. Raw flat-shading splits
are not inherently wrong; the failed bevel/subdivision treatment exposed them.
This is a failed adaptation, not a claim that the stock download is corrupt.

Poly Haven's API was used with identifying `FeltwillowAssetPilot/1.0` User-Agent.
**Selected map source: Poly Haven, Rico Cilliers / colormass (CC0)**; source credit
appears on the boards, independent of CC0's optional asset attribution. The
[live API terms](https://polyhaven.com/our-api) are distinct from asset rights.

## Controlled comparisons and findings

Twelve actual stills: prior/imported/adapted × neutral/dusk × shot/close.
Camera, lighting, exposure, color transform, sampling and seed are fixed within
each comparison. Geometry differs intentionally between stages; this is a kit
comparison, not an isolated texture-only A/B. Original-pixel crops retain those
differences honestly. Blender 5.2.2 LTS, Cycles CPU, Standard/None, exposure 0,
gamma 1, 1280×720, 40 samples, denoising, seed 510501. True render times:
9.1–13.7 s per still, 129.6 s total. Measured cumulative process peak resident
set: 1,998,274,560 bytes (~1.86 GiB on macOS); not per-asset memory or a benchmark.

| Sample | Verdict and visible effect |
|---|---|
| Rooted chopped stump | **Adapt further.** Gives the root an understandable attachment and flared base; fused sample is closed. Still regular/blocky, with carved-timber appearance, jagged cut rim and repetitive short surface burrs. No approval for integration. |
| Kenney rock_largeA | **Reject current adaptation.** Grass-capped platform silhouette is a poor hero rock; bevel/subdivision opens facet gaps. Existing rounded native rock wins. |
| Kenney leaf/bush | **Reject current smoothing.** Detached flattened faces and dark backs weaken felt construction. Existing thick cupped native leaves remain a better baseline. |
| Existing native moss cushion | **Keep for swatches.** Coherent and already fuzzy; its shape is more useful than importing realistic moss. |
| Adapted Poly Haven cushion | **Adapt further.** Recolored relief is visible close up but modest at shot distance; raw plush clips pale highlights and is not needle felt. New map does not demonstrably outperform the prior cushion overall. |
| Path/PATINA roughness sample | **Diagnostic only / adapt further.** Shows a matted surface; does not establish a blended ground edge, individual map benefit or integrated contact. |

The maps are 1024×1009 (the selected “1K” source aspect), diffuse sRGB and data
maps Non-Color. Raw baseline connects diffuse, tangent-space OpenGL normal,
roughness and height with explicit planar UVs on the test cushion/patch.
Adapted moss uses recolored diffuse marling and restrained object-space
height-to-bump; loaded normal/roughness nodes are **inactive** there. It is not
a full PBR claim. Fiber geometry supplies silhouette pile; bump cannot.

Independent design review reached the same mixed verdict. Repetition, overly
regular fibers and generic CG surfaces remain. Static sample support is not
an actor-route test; S05's real contacts were not altered. Temporal stability,
texture swimming and motion aliasing remain untested. The planned still budget
was reached; no more acquisition, repair-render loop or world dressing followed.

## Precise later integration plan — not executed

1. Start a new S05/environment revision, leaving r04/Leo/Milo/approved images
   unchanged. Refine the stump sample first: authored asymmetrical cut rim,
   natural root taper/burial and coherent compressed-wool folds. Attach it at
   the existing approach root's thick end using world anchors, not sample
   display coordinates. Preserve bypass, supported resting area and paw/nose
   causality; Milo still trips at Leo's forepaw, not a substituted root.
2. Re-run root/route and rest-support tests at unchanged character sizes. Do
   not populate the set with rejected rock/leaf/bush meshes. Retain native
   stone and foliage until a repaired component beats them under fixed tests.
3. Keep one canonical sunset disk in the future revision. The saved r04 has
   `R04_FIXED_SUN` plus legacy `SUNSET_FIXED_DISK`; render/viewport visibility
   is inventoried in `current_material_sun_audit.json`. Preserve the owner's
   two-sun report and remove the ambiguity in both viewport and beauty. **No
   sun fix is claimed in this sample task.**
4. Owner reviews the refined stump and any proposed material change before
   production-library publication or replacing the scene. No seamless old
   imagery/Wan/new-environment sequence is implied.

Bulk originals and sample `.blend` are intentionally in already ignored work
storage; a fresh clone cannot restore those bytes without the preserved
downloads. All images are packed, with safe relative source paths. CC0 rights
for new inputs do not automatically clear the whole sample for publication:
it also packs the existing PATINA roughness, whose raw redistribution is not
reviewed here. No original or derivative publication is selected.

Offline intake checks for both acquired packages pass supplied metadata/hashes,
**not legal clearance or visual approval**. Seven scoped sample/preservation
checks pass. Records remain `owner_approval: pending`. Manifest, exact commands,
import/material audits, source hashes, render settings and check outputs are
under `blender/renders/s05_asset_kit_r01/`; originals and API file-size metadata
are under ignored work. No S05, character or production authority file changed.
