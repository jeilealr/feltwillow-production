# fal MCP — controlled Feltwillow generation

Verified 18 October 2026. **Installed and OAuth authenticated. All four requested
endpoints returned schemas through fal MCP. No inference or upload was run;
setup spent $0.** Existing Blender also answered a read-only query through
Codex. See [verification report](fal_mcp_setup_report.md).

This owner-authorized connection follows the Blender-only feasibility phase;
it does not rewrite that phase's historical results or approve new assets.
The mandatory spending rules are in the repository [AGENTS.md](../../AGENTS.md).

## Connection and authentication

Official remote endpoint: `https://mcp.fal.ai/mcp-relay`. It uses browser OAuth;
no fal API key is needed for this MCP connection. Existing account sign-in
completed successfully. Credentials remain managed by Codex outside the repo.
No packages or proxy were installed.

The working CLI used here is bundled with the desktop app. If `codex` on PATH
exits unexpectedly, use `/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex`
on this Mac. Do not reinstall or overwrite other integrations to fix PATH.

For another machine, use its installed Codex executable:

```sh
codex mcp list
# Only when fal is absent:
codex mcp add fal --url https://mcp.fal.ai/mcp-relay
# Only if authentication is still needed (add can start OAuth automatically):
codex mcp login fal
```

Back up `~/.codex/config.toml` before edits. Preserve all existing sections.
The installed server uses the supported native HTTP configuration:

```toml
[mcp_servers.fal]
url = "https://mcp.fal.ai/mcp-relay"
default_tools_approval_mode = "prompt"

[mcp_servers.fal.tools.get_model_schema]
approval_mode = "auto"

[mcp_servers.fal.tools.get_pricing]
approval_mode = "auto"

[mcp_servers.fal.tools.estimate_cost]
approval_mode = "auto"

[mcp_servers.fal.tools.search_models]
approval_mode = "auto"

[mcp_servers.fal.tools.run_model]
approval_mode = "prompt"

[mcp_servers.fal.tools.submit_job]
approval_mode = "prompt"

[mcp_servers.fal.tools.submit_jobs]
approval_mode = "prompt"
```

Unlisted tools retain the default prompt requirement. These are tool permissions,
not a fal account billing cap: the agent must first obtain explicit human
approval of the exact operation. An automatic reviewer is not human spending
approval. Provider suggestions to run immediately never override this rule.

A fresh Codex native MCP runtime successfully called `get_model_schema` for each
endpoint below and `get_pricing` once for all four. This is stronger evidence
than a server-list entry. The currently open chat may need MCP server reload or
an app restart/new chat to show newly added tools; authentication is already
complete. No restart was forced and no existing chat was interrupted.

## Verified models, inputs, outputs and published pricing

The sanitized [live schema snapshot](../config/fal_model_catalog_snapshot.json)
contains all parameter defaults, enums and output schemas returned by MCP.
Prices below are published examples checked on 18 October 2026; refresh before
any approved run.

| Exact endpoint | Required input; important options | Outputs | Published request pricing |
|---|---|---|---|
| [`tripo3d/h3.1/image-to-3d`](https://fal.ai/models/tripo3d/h3.1/image-to-3d) | `image_url`; face limit, geometry/texture quality, texture/PBR toggles, seeds, alignment, orientation, auto-size, quad | GLB/FBX variants, preview, task ID | $0.20 untextured, $0.30 standard textures, $0.40 detailed textures; add $0.20 detailed geometry and $0.05 quad when selected |
| [`tripo3d/h3.1/multiview-to-3d`](https://fal.ai/models/tripo3d/h3.1/multiview-to-3d) | `image_urls`, 2–4 views ordered front/left/back/right; same major geometry/texture options | GLB/FBX variants, preview, task ID | Same published pricing as single-image |
| [`fal-ai/patina`](https://fal.ai/models/fal-ai/patina) | `image_url`; selected maps, seed, output format, sync mode | Basecolor, normal, roughness, metalness and height images; seed/timings | $0.01 base + $0.01 per megapixel per output map; published 1024×1024/all-five example about $0.06 |
| [`fal-ai/patina/material`](https://fal.ai/models/fal-ai/patina/material) | `prompt`; dimensions, image count, seed, steps, tiling, optional image/mask/strength, maps, upscaling, prompt expansion | Tileable texture plus selected PBR maps, prompt, seed/timings | $0.01 base + $0.02/MP + $0.01/MP/map; upscaling adds charges; published 1024×1024/five-map/no-upscale example about $0.08 |

Important pricing limitation: authenticated `get_pricing` returns the connected
account's billing rate: Tripo $0.01/credit; each PATINA endpoint $0.01/megapixel.
Those unit rates are **not complete per-request costs**. Option-dependent
charges, quantities, minimums and rounding are not fully expressed by that
response. Do not equate one credit or megapixel with one whole model request.
PATINA material prompt expansion may add a charge; show its setting explicitly.
Use the live pricing tool and published option rules together; disclose any
remaining uncertainty before approval. Execution entitlement and actual billed
amounts were intentionally not tested by submitting paid jobs.

PATINA Image-to-PBR derives maps from an image; it does not accept a text prompt
to design a new felt surface. PATINA material generates a new tiling surface.
Neither creates physical silhouette fibers or guarantees that a generated mesh
is rig-ready. Blender still handles scale, material assignment, fibers and rigging.

## Before every paid operation

1. Present one reviewable proposal: exact endpoint, local input paths/hashes,
   eventual upload scope, prompt, full settings, count and estimated total cost.
2. Wait for explicit owner approval. Setup, discovery and these examples grant
   no spending permission. Unknown cost is never treated as free.
3. Upload only approved inputs and submit only the approved request(s).
4. Preserve the returned request ID immediately. Poll an accepted job; never
   resubmit a processing job. On uncertain submission, reconcile before retry.
5. Download results before CDN expiry and record files/hashes, model/settings,
   request ID, estimated/actual cost if available and review status. Never
   invent actual cost when it is absent from the response.
6. Keep outputs as candidates. Owner approval is required before promotion.
   No batch, variation, retry or automatic canonical regeneration without
   separate explicit permission.

## Asset and receipt locations

| Purpose | Repository-relative location |
|---|---|
| Raw downloads and large intermediates | `work/blender/fal/<request_id>/` (existing ignored work area) |
| Selected Tripo model candidates | `blender/assets/characters/leo/candidates/fal/<revision>/` |
| Selected PATINA swatches/maps | `blender/assets/materials/fal/<material>/<revision>/` |
| Portable generation receipts | `blender/generation/<date>_<subject>_<revision>.json` |
| Blender-ready imported candidates | A distinct candidate `.blend` in the character/material revision folder |
| Approval state | Receipt with `candidate_pending_owner_review`, then exact owner decision/hash |

These paths are conventions; no generated asset folders or outputs were created
during setup. Raw source model, maps and selected portable dependencies must be
preserved before cleaning work files. Large binary Git/LFS decisions remain for
the owner. Keep originals separate from Blender cleanup/rigging derivatives.
Never overwrite approved 2D canonicals or the current production pipeline.

Receipts should include endpoint/version, parameters/seeds, source hashes,
request/status identifiers, estimate, actual cost or null, output paths/hashes,
Blender import scale and approval. Keep credentials, private signed upload URLs,
OAuth links and account identity out of tracked metadata. Texture maps need
appropriate color-space handling in Blender; height is not automatically a
finished displacement setup.

## Example requests — proposals only

**Leo:** “Prepare one request for `tripo3d/h3.1/image-to-3d` using the current
approved v6 Leo canonical. Show its exact path/hash, geometry and texture
settings, mesh options and total estimated cost. Preserve canonical identity
and register the result as a candidate. Stop for my explicit approval before
uploading or spending credits; do not run a batch.”

**Felt material:** “Prepare one `fal-ai/patina/material` request for a compact,
matte honey-cream needle-felt wool surface matching Leo's canonical pigment.
Use one 1024×1024 texture, both-axis tiling, PNG, explicit seed, five PBR maps,
no upscaling and prompt expansion disabled. Show the exact input JSON and cost
estimate. Wait for my explicit approval before any generation.”

For an already approved flat felt swatch, propose `fal-ai/patina` instead,
showing the source crop/hash and map selection. A full character photograph is
not automatically an appropriate uniform material swatch.

References: [official Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli),
[official fal OAuth endpoint instructions](https://fal.ai/learn/tools/motion-design-video-generation-with-claude).
