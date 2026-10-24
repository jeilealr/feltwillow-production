#!/usr/bin/env python3
"""Receipt-aware, read-only inventory for LUMI's fast bulk story renderer.

Writes an inventory and missing-shot commands. Exits nonzero if any existing
media is stale or a shot cannot be audited. It never moves or overwrites media.
"""

from __future__ import annotations

import hashlib
import argparse
import json
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from feltwillow import paths  # noqa: E402


def inventory_story(story_slug: str, runtime: Path | None = None, run_id: str | None = None, operations: dict | None = None) -> dict:
    import yaml

    if not re.fullmatch(r"[a-z0-9_]+", story_slug):
        raise ValueError(f"invalid story slug: {story_slug}")
    if bool(runtime) != bool(run_id):
        raise ValueError("runtime and run_id must be supplied together")
    story_file = Path(runtime).resolve() if runtime else paths.STORIES / story_slug / "story.yaml"
    story = yaml.safe_load(story_file.read_text())
    runtime_hash = hashlib.sha256(story_file.read_bytes()).hexdigest()
    if runtime and (story.get("run_id") != run_id or story.get("story") != story_slug):
        raise ValueError("runtime identity mismatch")
    if operations and operations.get("runtime_sha256") != runtime_hash:
        raise ValueError("operation journal belongs to a different runtime")
    records = []
    commands = []
    command_records = []
    blocked_operations = []
    for scene, details in story["scenes"].items():
        for shot in details.get("shots", []):
            name = shot["name"]
            argv = [sys.executable, str(Path(__file__).with_name("shot.py")),
                    "--story", story_slug, "--scene", str(scene), "--shot", name,
                    "--audit-existing"]
            if runtime:
                argv.extend(["--runtime", str(story_file), "--run-id", run_id, "--runtime-sha256", runtime_hash])
            else:
                argv.append("--fast")
            result = subprocess.run(argv, cwd=paths.REPO, text=True, capture_output=True)
            if result.returncode:
                raise RuntimeError(f"{story_slug} scene {scene} shot {name}: "
                                   f"receipt audit failed: {result.stderr.strip()}")
            record = json.loads(result.stdout)
            actual_seeds = record.get("seeds", [])
            if (record.get("story") != story_slug or record.get("scene") != scene
                    or record.get("shot") != name
                    or {entry.get("seed") for entry in actual_seeds} != set(shot["seeds"])
                    or len(actual_seeds) != len(shot["seeds"])
                    or any(entry.get("status") not in {"complete", "missing", "stale"}
                           for entry in actual_seeds)):
                raise ValueError(f"invalid receipt audit result for scene {scene} shot {name}")
            records.append(record)
            if runtime:
                for seed in record["seeds"]:
                    if seed["status"] != "missing":
                        continue
                    operation_id = f"{run_id}:{name}:s{seed['seed']}"
                    # Missing files are not evidence that a submitted operation never ran.
                    state = (operations or {}).get("operations", {}).get(operation_id, "unreconciled")
                    if state != "not_submitted":
                        blocked_operations.append(dict(operation_id=operation_id, state=state,
                                                       reason="reconcile request/job before proposing submission"))
                        continue
                    command = [sys.executable, str(Path(__file__).with_name("shot.py")),
                               "--story", story_slug, "--scene", str(scene), "--shot", name,
                               "--runtime", str(story_file), "--run-id", run_id, "--runtime-sha256", runtime_hash,
                               "--seed", str(seed["seed"])]
                    commands.append(shlex.join(command))
                    command_records.append(dict(operation_id=operation_id, argv=command, runtime_sha256=runtime_hash, submission_authorized=False, maximum_retries=0))
            elif any(seed["status"] == "missing" for seed in record["seeds"]):
                # sbatch task lines run in the repo root. Quote data values.
                command = ["python", "production/shot.py", "--story", story_slug,
                           "--scene", str(scene), "--shot", name, "--fast"]
                commands.append(shlex.join(command))
    counts = {status: sum(seed["status"] == status for record in records
                          for seed in record["seeds"])
              for status in ("complete", "missing", "stale")}
    return dict(story=story_slug, work_root=str(paths.WORK),
                audited_at=datetime.now(timezone.utc).isoformat(),
                counts=counts, shots=records, commands=commands,
                **(dict(runtime=str(story_file), runtime_sha256=runtime_hash, run_id=run_id,
                        command_records=command_records, blocked_operations=blocked_operations)
                   if runtime else {}))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story", required=True)
    parser.add_argument("--runtime", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--operations", type=Path, help="reconciled operation journal; absent means no submission proposals")
    parser.add_argument("--output", type=Path, required=True,
                        help="JSON inventory path under the resolved work root")
    parser.add_argument("--commands", type=Path, required=True,
                        help="missing-shot task commands path under the resolved work root")
    args = parser.parse_args()
    try:
        inventory = inventory_story(args.story, args.runtime, args.run_id, json.loads(args.operations.read_text()) if args.operations else None)
    except (OSError, KeyError, ValueError, RuntimeError) as error:
        parser.exit(1, f"inventory failed closed: {error}\n")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.commands.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({key: value for key, value in inventory.items()
                                       if key != "commands"}, indent=2) + "\n")
    args.commands.write_text("\n".join(inventory["commands"]) +
                             ("\n" if inventory["commands"] else ""))
    counts = inventory["counts"]
    print(f"render inventory: {counts['complete']} complete, {counts['missing']} missing, "
          f"{counts['stale']} stale seed(s); {len(inventory['commands'])} shot(s) to run; "
          f"{args.output}", file=sys.stderr)
    if counts["stale"]:
        for record in inventory["shots"]:
            for seed in record["seeds"]:
                if seed["status"] == "stale":
                    print(f"stale {seed['output']}: {seed['reason']}", file=sys.stderr)
        parser.exit(2, "existing media is stale; review and move it aside explicitly before rerunning\n")


if __name__ == "__main__":
    main()
