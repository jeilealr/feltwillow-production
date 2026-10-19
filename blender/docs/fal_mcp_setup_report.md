# fal MCP installation verification — 18 October 2026

**Outcome: installed, OAuth authenticated, all four model schemas/pricing
accessible through Codex, Blender verified. Setup inference spend: $0.**

## Verified environment

- macOS 26.7.1, arm64.
- Desktop app version 26.1013.31256, build 20586.
- Working bundled CLI: 0.163.0-alpha.10.2.
- Existing `/opt/homebrew/bin/codex` exited with status 137 during inspection;
  it was not replaced. The bundled CLI performed installation and verification.
- fal remote server: `https://mcp.fal.ai/mcp-relay`, server `fal-ai` version 0.1.0.
- fal was absent initially. Supported `mcp add` added it and automatically
  started OAuth; the owner completed browser authorization. CLI reported
  successful login and server inventory reports OAuth authenticated.
- No fal API key requested, no custom proxy or packages installed.

## Actual communication tests

A fresh ephemeral Codex native app-server session initialized fal and called:

| Tool | Arguments / purpose | Result |
|---|---|---|
| `get_model_schema` | `tripo3d/h3.1/image-to-3d`, full schema | Successful; 13 input parameters and mesh/variant/preview/task outputs |
| `get_model_schema` | `tripo3d/h3.1/multiview-to-3d`, full schema | Successful; 13 input parameters and mesh/variant/preview/task outputs |
| `get_model_schema` | `fal-ai/patina`, full schema | Successful; 6 parameters, map images/seed/timings |
| `get_model_schema` | `fal-ai/patina/material`, full schema | Successful; 16 parameters, texture/maps/prompt/seed/timings |
| `get_pricing` | All four exact IDs in one request | Successful; connected-account billing unit metadata returned |

The server exposes `run_model`, `submit_job` and `submit_jobs` with endpoint and
input arguments, so it advertises an execution route for these model IDs. None
was called. Paid execution entitlement, generation output quality and actual
billed costs remain intentionally untested. This report does not claim a paid
run succeeded.

Sanitized public model/schema and rate data are in
[the catalog snapshot](../config/fal_model_catalog_snapshot.json).
Current published configuration-sensitive prices and caveats are summarized in
[the setup guide](fal_mcp_setup.md). For example, Tripo's returned $0.01/credit
is a unit rate, not a $0.01 model-generation quote. PATINA material's optional
prompt expansion/upscaling must be included when estimating a future request.

## Existing Blender integration

The original Blender Local plugin remained enabled and all its files were
left unchanged. Its existing official launcher successfully initialized the
local server and read the open scene, with no scene mutation.

The current Codex loader rejected the plugin's existing absolute `/bin/sh`
command declaration under its plugin packaging rules. This explains why the
plugin was missing from `mcp list` despite a working bridge. Added a native
`mcp_servers.blender` compatibility entry pointing to that same unchanged
launcher. No package or add-on changes were required.

A second fresh Codex native MCP runtime successfully discovered `blender` and
called `get_objects_summary`. The tool returned scene/collection/object data
with `isError: false`. Final CLI inventory lists Blender enabled. Its auth
status is “unsupported” because it is local STDIO, not an OAuth failure.
The original plugin declaration still needs a packaging-format correction if
it is later used without this compatibility entry; it does not block the
verified global entry. Do not add another duplicate connection casually.

## Configuration changes and safeguards

Explicit user configuration edited: `~/.codex/config.toml`.
Backups were made first, outside the repository, with private permissions:

- `config.toml.backup-fal-20261018-134712` — original before installation.
- A second `backup-fal-policy-*` before approval settings.
- A `backup-blender-compat-*` before the compatibility entry.

Changes: add fal remote endpoint; fal defaults to prompting; four reviewed
read-only discovery tools may run automatically; `run_model`, `submit_job`
and `submit_jobs` explicitly require prompting. Add the Blender compatibility
entry. Codex CLI normalized away the pre-existing node_repl empty args array;
that original setting was restored. A parsed comparison confirms every original
setting, including plugin enablement, remains preserved after excluding the two
new MCP entries.

OAuth credentials were saved by Codex's supported flow; their contents/storage
were not copied into the repository or printed. Account identity from provider
responses was excluded from the repository schema snapshot.

Repository additions/edits:

- Root `AGENTS.md`: durable owner spending rules for all Feltwillow work.
- `blender/docs/fal_mcp_setup.md`: configuration, pricing, inputs/outputs,
  storage/receipt conventions and two approval-first example requests.
- This verification report.
- `blender/config/fal_model_catalog_snapshot.json`: sanitized read-only results.
- `blender/README.md`: link to the new setup guide.

Native tool prompts plus durable agent instructions enforce the requested
approval workflow. They are not a provider-side spending cap. Explicit human
approval of exact inputs/settings/count/cost is required before any paid tool,
HTTP API workaround or batch; automated approval is not spending consent.
No canonical assets, current prototype .blend files, selected images or
production image/video behavior changed during setup. No commits were made.

## Remaining user action

Authentication is complete. To expose fal in this already-running chat's tool
catalog, reload MCP servers in app settings or start a new chat/restart the app
if needed. Fresh Codex MCP runtime connectivity has already been tested; no
second sign-in or reinstallation is required. No app restart was forced.

No model or texture generation is authorized by this setup. Before the first
run, use one of the proposal-only examples in the guide and approve its exact
costed operation. Setup submitted zero inference requests and uploaded zero
files; fal inference credits spent by this task: **$0**.
