# MCP, providers, automation and spending

## Minimal tool stack

Prefer the existing local Blender installation plus its official Blender Lab MCP connection and the user's Codex/ChatGPT environment. Use the existing fal account for Tripo/PATINA when generation is authorized. Do not install an entire tutorial tool list. Higgsfield, Unreal, Unity, Godot, alternative 3D generators and commercial rigging services are optional experiments only when a specific measured gap justifies them.

Skill instructions do not provide an MCP server, credentials, browser login, Blender runtime or remote access. Discover what is actually connected. Prefer direct data/API operations with real viewport/render feedback over fragile GUI clicking, while retaining permission controls. The official Blender Lab bridge can execute code with substantial filesystem access; its own warning rules out treating it as harmless [B00](sources.md#b00).

## Safe local connection

Inspect current configuration and installed versions; back up before changes. Pin the official add-on and server to compatible releases rather than mixing a similarly named third-party package. Verify the installed Blender-side host/port. Keep the bridge on loopback, not publicly exposed. Do not add a tunnel or disable security to mimic a video.

First read-only test: list current scene objects and tool capabilities. Next reversible test only with permission: create an explicitly named temporary object in a saved test scene, inspect it, then undo/remove only that test object. A server appearing in an MCP list is not proof that Blender communication or screenshots work.

Prefer checked-in, inspectable scripts for nontrivial geometry/rig changes, with small MCP calls to execute and preview them. Capture exceptions and actual tool output. Context-dependent `bpy.ops` may fail headlessly; use Blender data APIs when practical and inspect version-specific RNA instead of guessing renamed operators, engine IDs or sockets.

## fal authentication and discovery

The provider documents its hosted OAuth relay at `https://mcp.fal.ai/mcp-relay` and no separate MCP surcharge, while inference remains billable [P04](sources.md#p04). Codex supports remote MCP configuration and OAuth login [O02](sources.md#o02). After checking current documentation and preserving existing config, a compatible CLI route is:

```bash
codex mcp add fal --url https://mcp.fal.ai/mcp-relay
codex mcp login fal
codex mcp list
```

Do not repeat the add operation blindly when the name already exists. Let the user complete browser authentication. For other clients, inspect their supported connection mechanism rather than assuming Codex config is shared with ChatGPT Desktop. Never request a pasted secret in chat or commit credentials. Do not confuse an ordinary API key's authentication scheme with a bearer/OAuth MCP token.

Read-only discovery should verify these endpoint schemas and current prices:
`tripo3d/h3.1/image-to-3d`, `tripo3d/h3.1/multiview-to-3d`, `fal-ai/patina`, `fal-ai/patina/material`, and, when needed, `fal-ai/patina/material/extract`.

No generation is needed for a connection test. Discover actual tool names; the model endpoint is not necessarily the MCP tool's name.

## Tripo recipe discipline

Use the current H3.1 schema, not P2/Studio settings copied from a video. H3.1 supports single and 2-4 ordered multiview inputs; only use consistent approved views. Quad output can be FBX instead of GLB [T03](sources.md#t03), [T04](sources.md#t04). Verify the downloaded file's real type and textures. Keep safety settings enabled. Do not assume a face-count option means valid topology or that native provider/API options are all exposed through fal.

Keep geometry and texture seeds/settings in provenance where exposed. Do not promise repeatability beyond the provider's actual snapshot/version guarantees. Preserve the accepted output bytes rather than relying on regenerating it later. Rigging is a separate task unless an explicitly selected and verified rig endpoint is used.

## Paid job protocol

1. Bind the exact input files, upload scope, endpoint, settings and output count.
2. Read a current price estimate and cap for this request, including extras.
3. Obtain explicit approval tied to this request fingerprint. Do not treat a generic "set up MCP" request as spend authorization.
4. Reserve the maximum expected cost in a shared budget ledger before submission. One coordinator owns reservations across agents.
5. Submit once, record request ID immediately, and poll that request. A timeout or interrupted chat is not permission to resubmit.
6. Reconcile actual charge when known; leave unknown charges reserved. Download necessary results before links expire, record hashes and save review candidates.
7. Stop for visual selection; do not repeat until attractive automatically.

The supplied `preflight.py job` is a **local advisory check**, not an enforcement proxy. It cannot prevent a model from directly calling fal, cannot prove authorization authenticity and does not atomically reserve funds. A later production executor must enforce allowlists, budget locks, request idempotency and approval binding at the tool boundary. Never advertise a prompt-only budget as a hard cap.

## Data and rights

Uploading a reference sends it to a provider. Confirm rights and privacy expectations for owner art, client materials, human reference photos and external assets. Record provider/model terms and commercial rights at generation time; prices, plans and licensing can change. A software MIT/GPL license is not automatically the license of every downloaded model, motion or texture. Do not bundle paid tutorials or their assets into this skill.

Use local source labels in reports, not home-directory secrets. Avoid exporting internal images to public hosts merely because a tool requests a URL. Use the provider's documented upload mechanism only after permission. Preserve tokens in approved local credential stores/environment handling, not scene custom properties or `.blend` text blocks.

## External libraries (1.3.0)

Follow [external-assets](external-assets.md) for browser/API discovery, bounded downloads and safe import. Assets, add-ons, access APIs, generation services and rendered products can have different rights or costs. No additional MCP is mandatory for the workflow. Do not install new add-ons or treat unknown .blend scripts as trusted automation by default.
