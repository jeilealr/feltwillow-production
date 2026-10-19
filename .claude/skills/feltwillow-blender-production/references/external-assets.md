# External assets: discover, verify, adapt, reuse

## Contents
1. Scope and routing
2. Define a small search brief
3. Review rights per deliverable
4. Record evidence and download safely
5. Inspect the imported asset
6. Convert to the Feltwillow medium
7. Prove usefulness before dressing the set
8. Publish and reuse
9. Example S05 application

## 1. Scope and routing

Use this workflow for third-party meshes, complete scenes, textures, HDRIs, brushes, node assets and motions. Read [the source catalog](asset-sources.md) for dated official leads, then check the exact current asset and downloaded license. A catalog is not approval of every file on a domain. Read materials/material-evidence for look development and environment-art-direction for the selected scene mode.

Prefer, in order: suitable reviewed assets already in the repository; a small Blender-native construction; a verified external asset; an explicitly authorized paid/generative alternative. Compare effort and visual quality, not ideology. Do not force free assets into the scene if adapting them costs more than making an appropriate simple element. No additional MCP service is required just to browse a website and import files; use available supported tools rather than automatically installing add-ons.

Retain nine specialist roles. The environment builder owns geometry selection, the look-development specialist owns surface adaptation, and the provenance steward checks rights/access/evidence. A coordinator resolves the choice; one writer edits a scene. No role can grant itself owner approval.

## 2. Define a small search brief

Start from an observed gap and story need, not a general instruction to download a forest. List required asset kind, intended screen size, support/contact behavior, style conversion, formats, performance limit, price ceiling and distribution target. Distinguish **free of charge**, **open content**, **open-source software**, **royalty-free** and **included in a paid subscription**.

Useful search buckets:
- Character-neutral surfaces: wool/felt, heathered fabric, matted fibers, roughness/height detail.
- Environment meshes: tree/branch structures, rocks, ground, roots, plants, flowers, buildings and props.
- Lighting: a neutral inspection HDRI or a deliberately chosen story-light base; not a new exposure/color recipe per asset.
- Specialty references: bird perches, nests, furniture, bridges, water banks and animal movement, with their own rights and technical review.

Write a shortlist with the [template](../assets/templates/asset-shortlist.md). Default to research-only until downloads are authorized. Ask for a bounded number of candidate packages and total transfer/storage limit. A task may authorize a small zero-cost pilot explicitly. Do not subscribe, start a trial, buy an add-on, bypass account restrictions or run paid fal generation under a 'free asset' request.

A source may have suitable 3D geometry but the wrong material. A texture may be useful only for fine relief. Label these roles. Catalog counts may cover paid tiers; do not promise every displayed model, source .blend or shader is in the free download.

## 3. Review rights per deliverable

Use [source/licensing notes](asset-sources.md). This is conservative production policy, not a legal opinion or automated verification of ownership. Record the exact license/version and acquisition evidence. Public-domain dedications and permissive licenses do not establish that a third-party uploader actually held the rights or cleared trademarks/likenesses [L09](sources.md#l09).

Make separate decisions for:
1. Monetized rendered images/video using the asset.
2. Modifying geometry, maps, shaders and derived library files.
3. Sharing raw files or extractable copies, including public Git, Git LFS, downloadable .blend files and archives.
4. Contractor/team access, where needed.
5. Uploading the asset to fal/PATINA/Tripo or another provider for processing. A paid-call approval is not permission to upload every local file.

Prefer verified CC0 for the pilot. Permit CC BY only with a reviewed attribution record, modification notice and delivery-credit plan; see the exact version [L10](sources.md#l10). Hold custom, share-alike, non-derivative and unclear licenses for scoped review instead of making universal legal assumptions. Exclude non-commercial, personal-use-only and editorial-only assets from this commercial-production pilot. Do not 'remove' a restriction by retexturing, decimating or processing through AI.

Custom QAL or royalty-free assets may permit commercial animation yet restrict asset redistribution. Keep such imports and embedded derivatives out of shared/source bundles until their exact use is reviewed. A private repository is not a universal exemption; collaborators and later public releases have separate implications. `.gitignore` does not untrack files already committed, and Git LFS does not change licensing.

For a conflict between a pack badge and a current provider policy, preserve both pieces of evidence. Verify the exact package/license and acquisition date; hold public redistribution until resolved. Do not overwrite an older verified acquisition license with a newer website label, nor automatically assume an old page applies to a new download.

## 4. Record evidence and download safely

Use the [external-asset record](../assets/templates/external-asset-record.json). It is a new proposed registry schema, not a replacement for the story visual bible or existing manifests. Adapt to a repository registry if it already exists. Never create a second competing source of truth.

For each selected package retain: creator/provider; stable asset-page URL and ID; version/free tier; acquisition date; exact license page plus packaged license when present; permitted uses and unresolved questions; original archive and selected file SHA-256s; dependencies; adaptations; destination and usage references. Avoid storing expiring signed download URLs or authentication tokens in public metadata. An evidence note may summarize the primary terms and date; do not redistribute arbitrary website text/previews without checking their rights.

Prefer official download buttons or documented APIs. Follow the API's own access terms separately from its asset license. Do not scrape, defeat access controls or hotlink runtime dependencies. Cache metadata politely, honor rate limits and retain downloaded outputs locally. Stop if an expected-free request is chargeable or requires a subscription. Poly Haven's current live API requires an identifying client header and source credit for surfaced content even though its downloaded assets are CC0 [L05](sources.md#l05).

Download into a dedicated staging area, not the production library. Inspect archives before extracting; reject traversal, absolute paths and unexpected executables, apply an expanded-size limit, and never overwrite existing files. Preserve raw imports; edit separate derivatives. Unknown .blend files can contain code: inspect with automatic Python execution disabled, and do not run embedded scripts, installers or drivers merely because a model is free [L11](sources.md#l11). Disabling auto-execution is not a complete security sandbox.

Default storage proposal, subject to existing repo conventions:
- `blender/asset_library/registry/`: small metadata records and legal/technical decisions.
- `blender/asset_library/receipts/`: appropriate license evidence and file hashes.
- `work/blender/external_assets/`: raw candidate downloads, excluded from normal Git.
- `blender/asset_library/<category>/<id>/<revision>/`: reviewed, normalized derivatives only when storage/redistribution is allowed.

Back up the raw assets separately. A fresh clone must have an honest dependency inventory and lawful restore instructions; do not imply all ignored bytes can be recovered from Git. Packing images or appending linked objects into a .blend can embed restricted content, so audit derivatives as well as original downloads.

## 5. Inspect the imported asset

Use an isolated test file and the installed Blender version. Record import success separately from render success. Check units, up-axis, transforms, object origins, negative scale, topology, normals, UVs, material slots, alpha cutouts, texture references and unsupported node/add-on dependencies. Inspect all required sides: some assets are camera-limited shells or cards. Do not use such assets as interactable volumes.

Inspect procedural materials for scripts/drivers/external dependencies. Game-engine shader packages do not automatically work in Blender; rebuilding a shader is separate work. A free mesh tier may not include a .blend source or full shader setup. DCC import of glTF/FBX/OBJ is not proof of accurate material translation.

For large vegetation, retain instances where practical; record prototype versus evaluated geometry and texture memory. Use screen-size-appropriate texture resolutions, normally 1K/2K for first trials unless justified. Do not fetch every 8K map by default. Simplify only after assessing hero silhouettes, collision/contact needs and aliasing. Do not automatically remesh the accepted Leo or Milo to make a scenery asset fit.

## 6. Convert to the Feltwillow medium

Preserve source rights; derive a new candidate rather than relabeling the untouched asset as original Feltwillow art. Use the material-evidence workflow. Keep character canon unchanged and choose scene-wide material scale, palette and lighting.

For meshes: preserve useful volume, soften overly sharp low-poly silhouettes where appropriate, add needed thickness to felt leaves, build coherent irregular clumps, and replace unsuitable realistic/flat materials. Keep root/branch and rock contact surfaces usable for the planned characters. A stock tree is a starting component, not automatically the hero Great Tree.

For maps: keep base color in its intended color space, treat normal/roughness/height/masks as data, verify normal-map convention, and distinguish roughness from gloss. Validate channel packing rather than wiring by filename alone. Use consistent UV/object coordinates and physical detail scale. Texture scale must not change randomly with each object's bounding box. See [L12](sources.md#l12).

Use realistic scans selectively for shape, broad variation or fine relief; do not preserve photographic dirt, bright specular minerals or bark grooves when they break the handmade medium. Avoid baked lighting/AO that doubles current scene shadows. Adding one wool-height map to every material is not enough. Sheen, micro-bump, mesh shape and limited stable fibers each solve different parts of the appearance.

Build a few distinct treatments: compressed-wool trunk/root ridges; soft moss cushions; matted path edges; rounded heathered rocks; thick felt leaf families. View them at delivery distance. Do not erase all medium-size detail through excessive smoothing, subdivision or denoising. Reuse current PATINA outputs when they already solve the gap; compare free and procedural options before requesting another paid map. New external-provider uploads still require permission.

## 7. Prove usefulness before dressing the set

Run one bounded sample scene, using the same camera, light, color transform, sampling and framing for comparisons. Show the prior material/asset, the imported baseline and the adapted result. Include a wide scene-context view and a useful close crop; a zoomed swatch alone does not establish the wide-shot effect. Record the render settings and source hashes.

Judge: felt recognition; silhouette; differentiated surface structure; material scale; readability near small actors; placement/contact; repetition; temporal stability; memory and actual render time. More polygons, connected texture nodes or a large library download do not pass these checks. A missing suitable asset is a valid result; report it rather than filling the scene with low-quality substitutes.

Approve only a **candidate for integration** after technical and visual evidence. Owner acceptance remains separate. Test short camera/deformation/ambient motion where relevant to catch shimmer, texture swimming, card exposure or alpha issues. If an asset fails, either adapt once within the stated cap or choose a different method; no infinite search.

## 8. Publish and reuse

After owner review, publish an immutable Feltwillow asset revision with provider/source bindings, adapted-file hashes and any credit obligations. Link or instance it into reviewed environments; do not silently mutate already-rendered scenes. Record scenes that use the revision and recheck affected views after changes.

For public release, verify the complete dependency graph, including packed textures and linked libraries. Separate render outputs from distributable source packages. Build attribution from verified records where required; voluntary credits may also be used without pretending they are a license requirement. Source-library access permission, asset rights and output-platform rules remain separate.

Run `scripts/asset_intake.py RECORD --root REPO --intent local_test` to catch missing file/evidence records, and `--intent public_bundle` to flag incompatible source-distribution decisions. A passing result means only the supplied metadata/files are consistent: it is not legal clearance, asset approval, provider authentication, a publish command or a security boundary. Existing production release gates still apply.

## 9. Example S05 application

Keep current `reference_inspired` direction. Search for a small material/geometry kit that improves the observed wool look: compressed bark/root relief, moss or felt base, a path surface, a rock form/finish, and one foliage family. Use ambientCG/Poly Haven primarily for map or shape leads; Kenney/Quaternius for mesh leads; inspect Blendkit's free tier only when it adds something specific. These are suggestions, not exclusive providers.

Do not replace the environment with a downloaded forest. Keep Leo and Milo scale, the interaction root and traversable clearings; integrate only tested pieces. Richness should come from coherent large forms, varied middle-scale clumps and controlled fine fibers. Keep unrelated future scenes as future demand, not a reason to bulk-download their assets now.
