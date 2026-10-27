"""Portable exact-input packages and one-operation noninteractive workers.

Build/verify/materialize are CPU preparation. Execution needs separately recorded
exact-package authorization and a durable exclusive operation journal. No command
submits a scheduler job, downloads dependencies, or retries an attempt.
"""

from __future__ import annotations
import argparse, copy, json, os, re, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import yaml
from production.sequence_plan import digest, fingerprint
from production.sequence_export import atomic

SCHEMA = "feltwillow.execution-package.v1"
ROOT = Path(__file__).resolve().parents[1]


def safe_file(base, name):
    path = (Path(base) / name).resolve()
    if not path.is_relative_to(Path(base).resolve()) or not path.is_file():
        raise ValueError("package file missing or escapes root: " + str(name))
    return path


def build(packet_dir, out, source_root=ROOT):
    packet_dir = Path(packet_dir).resolve()
    out = Path(out).resolve()
    root = Path(source_root).resolve()
    if out.exists():
        raise ValueError("new immutable package directory required")
    original = json.loads((packet_dir / "packet.json").read_text())
    if (
        original.get("schema") != "feltwillow.sequence-packet.v1"
        or original.get("technical_render_ready") is not True
    ):
        raise ValueError("valid technically-ready frozen packet required")
    runtime_path = Path(original["runtime"]["path"])
    if (
        not runtime_path.is_file()
        or digest(runtime_path) != original["runtime"]["sha256"]
    ):
        raise ValueError("original runtime missing/stale")
    runtime = yaml.safe_load(runtime_path.read_text())
    if original["run_id"] != runtime["run_id"]:
        raise ValueError("packet/runtime run mismatch")
    commands = original["commands"]
    if any(
        c.get("state") != "not_submitted" or c.get("maximum_retries") != 0
        for c in commands
    ):
        raise ValueError(
            "unknown/attempted operations must be reconciled before packaging"
        )
    files = {}
    assets = {}
    prepared = []

    def add_asset(path, sha):
        path = Path(path)
        if not path.is_file() or digest(path) != sha:
            raise ValueError("package source missing/stale")
        name = "assets/" + sha + path.suffix.lower()
        assets[name] = path
        return {"asset": name, "sha256": sha}

    for scene in runtime["scenes"].values():
        for shot in scene["shots"]:
            if shot.get("method") not in {
                "wan_i2v_single",
                "wan_i2v_pair",
                "static_frame_hold",
                "bounded_local_effect",
            }:
                raise ValueError("unsupported portable method")
            for field in ("keyframe", "end_keyframe"):
                if shot.get(field):
                    shot[field] = add_asset(shot[field], shot[field + "_sha256"])
            for field in ("target", "mask"):
                if shot.get("local_effect"):
                    shot["local_effect"][field] = add_asset(
                        shot["local_effect"][field]["path"],
                        shot["local_effect"][field]["sha256"],
                    )
    # Code is versioned and self-contained; Python packages/model weights are not bundled.
    code = {}
    for folder in ("feltwillow", "production"):
        for path in (root / folder).glob("*.py"):
            code["payload/" + folder + "/" + path.name] = path
    if "payload/production/shot.py" not in code:
        raise ValueError("renderer code unavailable")
    for name, sha in runtime.get("implementation_sha256", {}).items():
        if "payload/" + name not in code or digest(code["payload/" + name]) != sha:
            raise ValueError("code changed after render packet freezing")
    for command in commands:
        if (
            command["run_id"] != runtime["run_id"]
            or command["runtime_sha256"] != original["runtime"]["sha256"]
        ):
            raise ValueError("command runtime mismatch")
        argv = command["argv"]
        name = argv[argv.index("--shot") + 1]
        seed = int(argv[argv.index("--seed") + 1])
        shots = [
            s
            for scene in runtime["scenes"].values()
            for s in scene["shots"]
            if s["name"] == name
        ]
        if len(shots) != 1 or shots[0].get("seeds") != [seed]:
            raise ValueError("one seed/call per exact operation required")
        if command["operation_id"] != f"{runtime['run_id']}:{name}:s{seed}" or command[
            "model_invocations"
        ] != (
            0
            if shots[0]["method"] in {"static_frame_hold", "bounded_local_effect"}
            else 1
        ):
            raise ValueError("operation identity or invocation count mismatch")
        prepared.append(
            dict(
                operation_id=command["operation_id"],
                shot=name,
                seed=seed,
                scene=int(argv[argv.index("--scene") + 1]),
                method=shots[0]["method"],
                model_invocations=command["model_invocations"],
                maximum_retries=0,
            )
        )
    if len({p["operation_id"] for p in prepared}) != len(prepared):
        raise ValueError("duplicate operation identity")
    out.mkdir(parents=True)
    for name, path in {**assets, **code}.items():
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        files[name] = digest(target)
    template = "runtime_template.json"
    atomic(out / template, (json.dumps(runtime, indent=2) + "\n").encode())
    files[template] = digest(out / template)
    manifest = dict(
        schema=SCHEMA,
        run_id=runtime["run_id"],
        story=runtime["story"],
        source_packet_sha256=digest(packet_dir / "packet.json"),
        source_runtime_sha256=original["runtime"]["sha256"],
        files=files,
        operations=prepared,
        requirements=dict(
            python="compatible with packaged source",
            packages=["Pillow", "numpy", "PyYAML", "opencv-python"],
            video_tools=["ffmpeg", "ffprobe"],
            model_environment=runtime.get("endpoint_capability"),
            gpu_compatibility="must be verified on execution host; no CPU inference",
        ),
        submission_authorized=False,
        retry_limit=0,
    )
    manifest["package_sha256"] = fingerprint(manifest)
    atomic(out / "package.json", (json.dumps(manifest, indent=2) + "\n").encode())
    return manifest


def verify(package):
    package = Path(package).resolve()
    manifest = json.loads((package / "package.json").read_text())
    check = dict(manifest)
    sha = check.pop("package_sha256", None)
    if manifest.get("schema") != SCHEMA or fingerprint(check) != sha:
        raise ValueError("package manifest changed")
    expected_payload = {
        name for name in manifest["files"] if name.startswith(("payload/", "assets/"))
    }
    observed = set()
    for folder in ("payload", "assets"):
        for path in (package / folder).rglob("*"):
            if path.is_symlink():
                raise ValueError("package payload symlinks are forbidden")
            if path.is_file():
                observed.add(path.relative_to(package).as_posix())
    if observed != expected_payload:
        raise ValueError("unexpected or missing package payload file")
    if not re.fullmatch(r"[a-z0-9_]+", manifest["story"]) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9_.-]*", manifest["run_id"]
    ):
        raise ValueError("unsafe package story/run identity")
    for op in manifest["operations"]:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", op["shot"]):
            raise ValueError("unsafe package shot identity")
    for name, expected in manifest["files"].items():
        if digest(safe_file(package, name)) != expected:
            raise ValueError("package file changed: " + name)
    return manifest


def contained_output(package, name):
    package = Path(package).resolve()
    path = package / name
    if not path.resolve().is_relative_to(package):
        raise ValueError("package output path escapes namespace")
    current = path
    while current != package:
        if current.is_symlink():
            raise ValueError("package output symlink forbidden")
        current = current.parent
    return path


def materialize(package, interpreter=sys.executable):
    package = Path(package).resolve()
    manifest = verify(package)
    runtime = json.loads((package / "runtime_template.json").read_text())
    runtime["scenes"] = {int(k): v for k, v in runtime["scenes"].items()}

    def resolve(ref):
        return str(safe_file(package, ref["asset"]))

    for scene in runtime["scenes"].values():
        for shot in scene["shots"]:
            for field in ("keyframe", "end_keyframe"):
                if shot.get(field):
                    shot[field] = resolve(shot[field])
            if shot.get("local_effect"):
                for field in ("target", "mask"):
                    ref = shot["local_effect"][field]
                    shot["local_effect"][field] = dict(
                        path=resolve(ref), sha256=ref["sha256"]
                    )
    folder = contained_output(package, "host_runtime")
    path = contained_output(package, "host_runtime/runtime.yaml")
    contained_output(package, "host_runtime/packet.json")
    data = yaml.safe_dump(runtime, sort_keys=False).encode()
    atomic(path, data)
    sha = digest(path)
    marker = dict(
        run_id=manifest["run_id"],
        runtime=dict(path=str(path), sha256=sha),
        package_sha256=manifest["package_sha256"],
        source_runtime_sha256=manifest["source_runtime_sha256"],
    )
    atomic(folder / "packet.json", (json.dumps(marker, indent=2) + "\n").encode())
    commands = {}
    for op in manifest["operations"]:
        commands[op["operation_id"]] = [
            str(interpreter),
            str(package / "payload/production/shot.py"),
            "--story",
            manifest["story"],
            "--scene",
            str(op["scene"]),
            "--shot",
            op["shot"],
            "--runtime",
            str(path),
            "--runtime-sha256",
            sha,
            "--run-id",
            manifest["run_id"],
            "--seed",
            str(op["seed"]),
        ]
    return manifest, commands


def worker(
    package,
    operation,
    journal=None,
    authorization=None,
    execute=False,
    interpreter=sys.executable,
    expected_package_sha256=None,
):
    package = Path(package).resolve()
    manifest = verify(package)
    if not execute and expected_package_sha256 != manifest["package_sha256"]:
        raise ValueError(
            "trusted expected package SHA required before preflight code execution"
        )
    if execute:
        if not journal or not authorization:
            raise ValueError("durable journal and exact authorization required")
        if Path(journal).resolve().is_relative_to(package) or Path(
            authorization
        ).resolve().is_relative_to(package):
            raise ValueError(
                "durable journal and trusted authorization must be external to package"
            )
        early_auth = json.loads(Path(authorization).read_text())
        if (
            early_auth.get("scope") != "execution_authorization"
            or early_auth.get("decision") != "authorized"
            or early_auth.get("reviewer") != "project_owner"
            or early_auth.get("package_sha256") != manifest["package_sha256"]
            or operation not in early_auth.get("operation_ids", [])
            or early_auth.get("maximum_retries") != 0
        ):
            raise ValueError("authorization does not cover exact package/operation")
    output_root = contained_output(package, "outputs")
    if output_root.exists():
        for item in output_root.rglob("*"):
            if item.is_symlink():
                raise ValueError("package output symlink forbidden")
    for op in manifest["operations"]:
        base = f"outputs/stories/{manifest['story']}/runs/{manifest['run_id']}"
        contained_output(package, base + "/shots")
        contained_output(package, base + "/operations")
    manifest, commands = materialize(package, interpreter)
    if operation not in commands:
        raise ValueError("unknown frozen operation")
    argv = commands[operation]
    env = dict(
        os.environ,
        FELTWILLOW_WORK=str(package / "outputs"),
        PYTHONDONTWRITEBYTECODE="1",
        HF_HUB_OFFLINE="1",
        TRANSFORMERS_OFFLINE="1",
    )
    if not execute:
        if expected_package_sha256 != manifest["package_sha256"]:
            raise ValueError(
                "trusted expected package SHA required before preflight code execution"
            )
        return subprocess.run(
            [*argv, "--dry-run"], check=True, env=env, capture_output=True, text=True
        ).stdout
    if not journal or not authorization:
        raise ValueError("durable journal and exact authorization required")
    auth = json.loads(Path(authorization).read_text())
    if (
        auth.get("scope") != "execution_authorization"
        or auth.get("decision") != "authorized"
        or auth.get("reviewer") != "project_owner"
        or auth.get("package_sha256") != manifest["package_sha256"]
        or operation not in auth.get("operation_ids", [])
        or auth.get("maximum_retries") != 0
    ):
        raise ValueError("authorization does not cover exact package/operation")
    # Preflight validates all assets, code, fit and installed endpoint config before claim/model.
    subprocess.run(
        [*argv, "--dry-run"], check=True, env=env, capture_output=True, text=True
    )
    journal = Path(journal).resolve()
    journal.mkdir(parents=True, exist_ok=True)
    claim = journal / (
        fingerprint(
            dict(
                operation_id=operation,
                source_runtime_sha256=manifest["source_runtime_sha256"],
            )
        )
        + ".json"
    )
    with claim.open("x") as stream:
        json.dump(
            dict(
                operation_id=operation,
                package_sha256=manifest["package_sha256"],
                state="attempt_started",
                scheduler_job_id=os.environ.get("SLURM_JOB_ID"),
                maximum_retries=0,
            ),
            stream,
        )
    result = subprocess.run(argv, env=env, capture_output=True, text=True)
    receipt = dict(
        operation_id=operation,
        package_sha256=manifest["package_sha256"],
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
        state="process_exited_outputs_require_verification",
        claim=str(claim),
        visual_review="pending",
        owner_selection="pending",
    )
    atomic(
        journal / (claim.stem + ".result.json"),
        (json.dumps(receipt, indent=2) + "\n").encode(),
    )
    if result.returncode:
        raise ValueError("worker failed; reconcile recorded claim/result; no retry")
    return receipt


def collect_results(package, out):
    """Copy verified result bytes with a path map; leave original receipts intact."""
    from feltwillow.render_receipt import inspect_render

    package = Path(package).resolve()
    out = Path(out).resolve()
    manifest = verify(package)
    if out.exists():
        raise ValueError("new immutable results directory required")
    runtime_path = contained_output(package, "host_runtime/runtime.yaml")
    if not runtime_path.is_file():
        raise ValueError("host runtime unavailable")
    # Reconstruct from the hash-verified immutable template; refuse an edited
    # host runtime even if its adjacent marker was rehashed to match.
    materialize(package)
    runtime = yaml.safe_load(runtime_path.read_text())
    runtime_sha = digest(runtime_path)
    marker = json.loads((package / "host_runtime/packet.json").read_text())
    if (
        marker.get("package_sha256") != manifest["package_sha256"]
        or marker["runtime"]["sha256"] != runtime_sha
    ):
        raise ValueError("host runtime changed")
    rows = []
    files = {}
    copies = {}
    shots = {
        s["name"]: s for scene in runtime["scenes"].values() for s in scene["shots"]
    }
    for op in manifest["operations"]:
        shot = shots[op["shot"]]
        suffix = "_fast" if shot["render"]["preset"] == "fast" else ""
        clip = contained_output(
            package,
            f"outputs/stories/{manifest['story']}/runs/{manifest['run_id']}/shots/{op['shot']}_s{op['seed']}{suffix}.mp4",
        )
        if not clip.is_file():
            raise ValueError(
                "result missing/uncertain; reconcile journal, never resubmit"
            )
        receipt = json.loads(clip.with_suffix(".json").read_text())
        expected = {k: receipt[k] for k in ("width", "height", "frames", "fps")}
        expected.update(
            run_id=manifest["run_id"],
            runtime_sha256=runtime_sha,
            shot=op["shot"],
            seed=op["seed"],
            method=op["method"],
            keyframe_sha256=shot["keyframe_sha256"],
            end_keyframe_sha256=shot.get("end_keyframe_sha256"),
        )
        if (
            receipt.get("frames") != shot["frames"]
            or receipt.get("width") != shot["render"]["width"]
            or receipt.get("height") != shot["render"]["height"]
            or receipt.get("fps") != 16
        ):
            raise ValueError("result recipe differs from frozen runtime")
        expected.update(prompt=shot['prompt'],negative=shot.get('negative',''),fast=False if op['method'] in {'static_frame_hold','bounded_local_effect'} else shot['render']['preset']=='fast')
        expected.update({k:shot['render'][k] for k in ('steps','guidance','guidance_2')})
        expected.update({k:shot.get(k) for k in ('sequence_dependency_sha256','alignment_sha256','edge_sha256','source_key_order')})
        if shot.get('editorial_plan_sha256'):
            expected.update(editorial_plan_sha256=shot['editorial_plan_sha256'],editorial_allocation=shot['editorial_allocation'])
        if shot.get('local_effect'):expected['local_effect']=shot['local_effect']
        from feltwillow import wan
        from PIL import Image
        for field,label in (('keyframe','start_fit'),('end_keyframe','end_fit')):
            if shot.get(field):
                with Image.open(shot[field]) as im:expected[label]=wan.fitted_record(im,shot['render']['width'],shot['render']['height'])
        status, reason = inspect_render(clip, expected)
        if status != "complete":
            raise ValueError("result failed verification: " + str(reason))
        name = f"results/{op['shot']}_s{op['seed']}"
        mapping = {}
        for original in [clip, clip.with_suffix(".json")] + [
            Path(b[k])
            for b in receipt["native_boundaries"].values()
            for k in ("path", "preview_path")
            if b.get(k)
        ]:
            if not original.resolve().is_relative_to(package):
                raise ValueError("result reference escapes package")
            rel = name + "/" + original.name
            copies[rel] = original
            files[rel] = digest(original)
            mapping[str(original)] = rel
        rows.append(
            dict(
                operation_id=op["operation_id"],
                clip=name + "/" + clip.name,
                receipt=name + "/" + clip.with_suffix(".json").name,
                boundary_paths={
                    b[k]: mapping[b[k]]
                    for b in receipt["native_boundaries"].values()
                    for k in ("path", "preview_path")
                    if b.get(k)
                },
                visual_review="pending",
                owner_selection="pending",
            )
        )
    out.mkdir(parents=True)
    for name, source in copies.items():
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    result = dict(
        schema="feltwillow.result-package.v1",
        package_sha256=manifest["package_sha256"],
        run_id=manifest["run_id"],
        story=manifest["story"],
        runtime_sha256=runtime_sha,
        files=files,
        operations=rows,
        whole_motion_review="pending",
        owner_selection="pending",
    )
    result["sha256"] = fingerprint(result)
    atomic(out / "results.json", (json.dumps(result, indent=2) + "\n").encode())
    return result


def verify_results(folder, expected_package_sha256, expected_result_sha256):
    from feltwillow.render_receipt import inspect_render

    folder = Path(folder).resolve()
    result = json.loads((folder / "results.json").read_text())
    check = dict(result)
    sha = check.pop("sha256", None)
    if (
        result.get("schema") != "feltwillow.result-package.v1"
        or not result.get("operations")
        or not result.get("files")
    ):
        raise ValueError("invalid or empty results schema")
    if (
        not expected_result_sha256
        or sha != expected_result_sha256
        or fingerprint(check) != sha
        or result.get("package_sha256") != expected_package_sha256
    ):
        raise ValueError(
            "result manifest/package differs from trusted collection digest"
        )
    if len({op["operation_id"] for op in result["operations"]}) != len(
        result["operations"]
    ):
        raise ValueError("duplicate result operation")
    for name, sha in result["files"].items():
        if digest(safe_file(folder, name)) != sha:
            raise ValueError("result bytes changed")
    for op in result["operations"]:
        clip = safe_file(folder, op["clip"])
        receipt = json.loads(safe_file(folder, op["receipt"]).read_text())
        if (
            receipt.get("run_id") != result["run_id"]
            or receipt.get("runtime_sha256") != result["runtime_sha256"]
        ):
            raise ValueError("result runtime identity changed")
        mapping = {
            old: str(safe_file(folder, new))
            for old, new in op["boundary_paths"].items()
        }
        status, reason = inspect_render(clip, receipt, boundary_paths=mapping)
        if status != "complete":
            raise ValueError("imported result failed decode/hash: " + str(reason))
    return result


def take_proposals(folder, package_sha256, result_sha256):
    folder = Path(folder).resolve()
    result = verify_results(folder, package_sha256, result_sha256)
    takes = {}
    for op in result["operations"]:
        receipt = json.loads(safe_file(folder, op["receipt"]).read_text())
        source = safe_file(folder, op["clip"])
        takes[receipt["shot"]] = dict(
            path=str(source),
            sha256=digest(source),
            owner_decision="pending",
            full_motion_review={"status": "pending"},
            boundary_paths={
                old: str(safe_file(folder, new))
                for old, new in op["boundary_paths"].items()
            },
        )
    return dict(
        schema="feltwillow.sequence-takes.v1",
        story=result["story"],
        run_id=result["run_id"],
        runtime_sha256=result["runtime_sha256"],
        source_results_sha256=result_sha256,
        takes=takes,
        approval_scope="unselected transport proposals only",
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    b = sub.add_parser("build")
    b.add_argument("packet", type=Path)
    b.add_argument("--out", type=Path, required=True)
    b.add_argument("--source-root", type=Path, default=ROOT)
    v = sub.add_parser("verify")
    v.add_argument("package", type=Path)
    w = sub.add_parser("worker")
    w.add_argument("package", type=Path)
    w.add_argument("--operation", required=True)
    w.add_argument("--journal", type=Path)
    w.add_argument("--authorization", type=Path)
    w.add_argument("--execute", action="store_true")
    w.add_argument(
        "--package-sha256", help="trusted expected package digest for CPU preflight"
    )
    c = sub.add_parser("collect")
    c.add_argument("package", type=Path)
    c.add_argument("--out", type=Path, required=True)
    i = sub.add_parser("verify-results")
    i.add_argument("folder", type=Path)
    i.add_argument("--package-sha256", required=True)
    i.add_argument(
        "--result-sha256",
        required=True,
        help="digest recorded independently from trusted execution-host collection",
    )
    t = sub.add_parser("take-proposals")
    t.add_argument("folder", type=Path)
    t.add_argument("--package-sha256", required=True)
    t.add_argument("--result-sha256", required=True)
    t.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    try:
        if a.command == "take-proposals":
            proposed = take_proposals(a.folder, a.package_sha256, a.result_sha256)
            atomic(a.out, (json.dumps(proposed, indent=2) + "\n").encode())
            print(json.dumps(proposed, indent=2))
            return
        if a.command == "collect":
            print(json.dumps(collect_results(a.package, a.out), indent=2))
            return
        if a.command == "verify-results":
            print(
                json.dumps(
                    verify_results(a.folder, a.package_sha256, a.result_sha256),
                    indent=2,
                )
            )
            return
        result = (
            build(a.packet, a.out, a.source_root)
            if a.command == "build"
            else verify(a.package)
            if a.command == "verify"
            else worker(
                a.package,
                a.operation,
                a.journal,
                a.authorization,
                a.execute,
                expected_package_sha256=a.package_sha256,
            )
        )
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        p.exit(1, "PACKAGE_BLOCKED: " + str(error) + "\n")


if __name__ == "__main__":
    main()
