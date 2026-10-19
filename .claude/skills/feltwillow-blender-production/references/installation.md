# Installation and first use

## One source for Claude Code and Codex

Keep the actual skill in the repository's `.claude/skills/` directory. Expose
that same directory to Codex with a relative symbolic link, not a second copy:

```text
<repo>/.claude/skills/feltwillow-blender-production/    # actual files
<repo>/.agents/skills/feltwillow-blender-production    # symlink to those files
```

The link target, relative to `.agents/skills/`, is exactly:

```text
../../.claude/skills/feltwillow-blender-production
```

Claude Code discovers project skills in `.claude/skills` [C01](sources.md#c01).
Codex discovers `.agents/skills` and explicitly follows linked skill folders
[O01](sources.md#o01). This shares the entire skill, including references,
scripts, templates and specialist briefs. Edit only the actual Claude-folder
copy. This does not synchronize a separately uploaded ChatGPT/Claude skill or
configure any MCP server; local tool access and permissions remain separate.

## Install safely

The distribution includes `install_feltwillow_shared.py` alongside `skill.zip`.
The same installer is bundled as `scripts/install_shared.py` for later reuse.
Download the two distribution files to the same directory, then run with the
actual checkout root (Python 3.9+ for this installer):

```bash
python3 /path/to/install_feltwillow_shared.py \
  --repo /path/to/feltwillow-production \
  --archive /path/to/skill.zip \
  --apply
```

Omit `--apply` for a dry run. The installer:

- Installs from the archive only when neither client has the skill.
- Preserves an existing Claude copy, including local edits; it does not upgrade it.
- Moves an existing Codex-only copy to Claude's folder, preserving its contents.
- Moves an identical Codex duplicate into a backup outside the repository before
  replacing it with the link. It prints the backup path.
- Stops without changes if installed copies differ, parents are linked, or an
  existing link points elsewhere. Resolve conflicts without discarding edits.
- Leaves other skills, client configuration, Blender assets and Git commits alone.
- Verifies that both clients' paths resolve to the exact same `SKILL.md` file.

Do not use `unzip -n` to merge a new release into an old copy: that can retain old
instructions beside new helper files. For upgrades, compare a freshly extracted
release with the source folder, preserve local changes, and update only that
source. The Codex link need not change.

For an already-installed source and an absent Codex entry, the link alone is:

```bash
cd /path/to/feltwillow-production
mkdir -p .agents/skills
# Run only after confirming the source exists and the destination is absent.
ln -s ../../.claude/skills/feltwillow-blender-production \
  .agents/skills/feltwillow-blender-production
```

Keep the actual skill and its relative link in version control after reviewing
the diff; do not commit backup folders or generated caches. Launch each client
from this checkout and test discovery in a fresh session. In Claude Code use
`/feltwillow-blender-production`; in Codex use `$feltwillow-blender-production`.
Verify the discovered path, especially if you also have a global/plugin copy.

For a ChatGPT environment with skill import, upload the single `skill.zip`
through its supported interface. That uploaded bundle is separate from the
repository installation and does not grant access to local Blender or MCP.

## Upgrade an existing shared installation

For release 1.2.0, use the separate `update_feltwillow_shared.py` distributed with the new `skill.zip` (also bundled as `scripts/update_shared.py`). Do not rerun the older installer expecting an upgrade: it deliberately preserves existing files.

This release manifest targets the 1.1.0 shared package. Upgrade older installations through their matching release or ask the local agent to merge; never force an unknown baseline. It compares previous release, new release and local file hashes. It updates `.claude/skills/feltwillow-blender-production/` only and retains the relative `.agents/skills/feltwillow-blender-production` link. Unknown files and edits to unchanged upstream files are preserved. Overlapping edits, local deletions, unexpected symlinks or a second Codex copy cause a stop before writes. Do not force-overwrite a conflict; merge it with your local agent against the new release.

Save the new ZIP and updater together. Stop active agents that could edit the skill. Preview:

```bash
python3 /path/to/update_feltwillow_shared.py \
  --repo /path/to/feltwillow-production \
  --archive /path/to/new/skill.zip
```

Apply only after reviewing the plan, by adding `--apply`. No administrator rights, new dependency installation or network access are needed. A backup and receipt are created beneath `~/.local/state/feltwillow/skill-backups/` unless `--backup-dir` names another outside-repository location. A normal caught failure/interrupt rolls back the folder swap. This is not a power-loss-safe database transaction; retain the printed backup and do not edit the source during the update.

Verify the source `VERSION` begins `1.2.0` and that both `SKILL.md` paths are the same file. Start fresh Codex/Claude Code sessions from the repository; explicitly invoke the skill and ask it to read `VERSION` and the new module. Client discovery must still be tested on your Mac [O01](sources.md#o01).

The upgrade does not commit or push. Review only the skill changes and the existing link on your chosen branch. Do not include Python caches or unrelated local work. A separately uploaded ChatGPT skill is another copy: re-import the complete new ZIP there only when you intend to update it. Local repository edits do not synchronize to that cloud copy.

## First prompt

> Use the feltwillow-blender-production skill. Inspect my current local Feltwillow checkout and existing Blender/Tripo Leo work. Reconcile current owner decisions before proposing changes. Prepare a bounded Leo + S05 pilot and risk report, using the existing Leo model rather than generating another. No paid calls, deletions, scene overwrites or production approvals. Identify exactly what can be tested with the tools available.

## Optional task prompts

**Environment:** "Use the environment and world-state modules to design a reusable 3D/2.5D Great Tree set with a reviewed camera envelope and calm ambient motion. Select plate-match or reference-inspired mode from owner direction, then propose geometry versus cards and retained story invariants. Preserve published landmarks; design candidates within their permitted freedom."

**Future bird:** "Use the anatomy and rigging modules to audit this approved bird model for perching, wing folding and landing. Do not apply a humanoid auto-rig by default. Report missing capabilities before changing the mesh."

**Independent review:** "Act as the independent QA role. Compare these exact asset and shot revisions to their canonical sources. Review the entire sequence, including ambient and prop state. Do not modify assets or approve on behalf of the owner."

## Requirements

Portable validators use Python 3.10+ standard library. The optional contact-sheet and scene-match helpers require Pillow (with ImageCms for scene matching). The Blender inventory helper requires Blender's `bpy` runtime and must be tested locally. The research environment did not have Blender. MCP connections, authentication, paid service credits, approved art and actual scene assets are separate dependencies.

Run the bundled portable tests from the skill directory:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m compileall -q scripts tests
```

Read `validation.md` for exactly what was and was not tested. Do not enable a new production export merely because these helper tests pass.

## Upgrade to 1.3.0

The 1.3.0 release contains baseline hashes for the exact previously distributed 1.2.0 package. Run the included `update_shared.py` helper with the new `skill.zip`, first as a dry run and then with `--apply`. It updates the `.claude/skills/feltwillow-blender-production` source and retains the `.agents/skills/feltwillow-blender-production` relative link. Never unpack over an edited installation. Earlier-version or overlapping-edit conflicts need sequential upgrades or an explicit local merge. A downloadable ZIP is not a remote update of Codex or your filesystem. No external asset library or MCP is installed by this update.
