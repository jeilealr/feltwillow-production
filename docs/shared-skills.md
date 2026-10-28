# Shared skills

`.claude/skills/` owns all shared instructions and supporting resources. `.agents/skills -> ../.claude/skills` exposes the same directory, including future additions. The recursive comparison is in `stories/lion_and_mouse_v7/review/shared_skills_s06_handoff_r001/SKILL_COMPARISON.json`.

Edit canonical files once. Add a skill there and register its name in `.claude/shared-skills.json`. Before removing a skill, preserve useful content and review the inventory change; never use synchronization to delete content. Run `python production/check_shared_skills.py` before relying on skills. This fails for a split/broken discovery directory, missing entrypoint, broken resource link or unexpected skill inventory change.

Git must preserve symbolic links (normal macOS/Linux checkout). On hosts that flatten or disable links the check fails; restore the link before using the collection. The filesystem check proves both paths load identical files. It does not prove that every installed Claude/Codex client has refreshed its cached skill catalog: restart/reload both clients and confirm all five names appear. This session cannot inspect another client's live catalog. No automatic cross-provider model switching is installed; image-routing prepares an explicit handoff.

The image-routing skill is portable and its `scripts/route.py` runs offline. Its ZIP is a standalone skill folder, not an installer for the repository link layout.
