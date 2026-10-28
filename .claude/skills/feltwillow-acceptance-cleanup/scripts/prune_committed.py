#!/usr/bin/env python3
"""Fail-closed exact-path Git pruning of committed, superseded Feltwillow files.

No interactive approval gate. A clean committed snapshot, current authority
records, recovered Git blobs, absence of retained references, and passing
focused tests are the preconditions. Does NOT push or rewrite Git history.
The agent must supply a factually supported, scoped manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from cleanup_audit import git, is_protected_evidence, repo_root, sha256, tracked, validate_path

SCHEMA = "feltwillow.cleanup-committed.v1"
CATEGORIES = {"superseded_revision", "review_derivative", "legacy_v6", "chrono_probe"}
IMAGE_REV = re.compile(r"_r\d{2,3}_candidate\.(png|jpe?g|json)$", re.I)
SHA_RE = re.compile(r"[0-9a-f]{64}")
HEAD_RE = re.compile(r"[0-9a-f]{40}")
HTML_REF_RE = re.compile(r"(?:href|src)\s*=\s*['\"]([^'\"]+)['\"]", re.I)
MD_REF_RE = re.compile(r"\]\(([^)]+)\)")
GENERIC_NAMES = {"README.md", "REVIEW.html", "RECEIPT.json", "CONTACT_SHEET.jpg",
                 "STATUS.md", "MANIFEST.json", "INDEX.json", "SUMMARY.md"}
MAX_FILES = 250  # bounded single-operation blast radius; repeat batches automatically


def _clean_committed(root: Path) -> tuple[str, str]:
    branch = git(root, "branch", "--show-current").stdout.decode().strip()
    head = git(root, "rev-parse", "HEAD").stdout.decode().strip()
    if not branch or not HEAD_RE.fullmatch(head):
        raise ValueError("Detached or invalid HEAD; no cleanup")
    for args in (("diff", "--quiet"), ("diff", "--cached", "--quiet")):
        r = git(root, *args, check=False)
        if r.returncode != 0:
            raise ValueError("Tracked changes are not committed; commit first, then retry")
    if git(root, "ls-files", "--deleted").stdout.strip():
        raise ValueError("Tracked paths already missing; repair/commit first")
    return branch, head


def _entry(root: Path, row: dict, known: set[str], label: str) -> tuple[str, Path, str]:
    if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
        raise ValueError(f"{label} entry must contain exactly path and sha256")
    rel, digest = row["path"], row["sha256"]
    if not isinstance(rel, str) or not isinstance(digest, str) or not SHA_RE.fullmatch(digest):
        raise ValueError(f"Invalid {label} entry")
    if rel not in known:
        raise ValueError(f"Not tracked ({label}): {rel}")
    path = validate_path(root, rel)
    if sha256(path) != digest:
        raise ValueError(f"Changed or mismatched bytes ({label}): {rel}")
    return rel, path, digest


def _committed_sha(root: Path, rel: str) -> str:
    # Check actual recoverability, not merely existence of a Git object by ID.
    proc = subprocess.Popen(["git", "-C", str(root), "show", f"HEAD:{rel}"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    h = hashlib.sha256()
    assert proc.stdout is not None
    first = proc.stdout.read(256 * 1024)
    try:
        if first.startswith(b"version https://git-lfs.github.com/spec/v1"):
            proc.kill();proc.wait()
            raise ValueError(f"Git stores only an LFS pointer; external recovery needed: {rel}")
        h.update(first)
        for chunk in iter(lambda: proc.stdout.read(1024 * 1024), b""):
            h.update(chunk)
        assert proc.stderr is not None
        err = proc.stderr.read().decode("utf8", "replace")
        if proc.wait() != 0:
            raise ValueError(f"Cannot recover committed file {rel}: {err[:250]}")
        return h.hexdigest()
    finally:
        proc.stdout.close()
        if proc.stderr is not None: proc.stderr.close()


def _safe_scope(rel: str, category: str) -> None:
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category for {rel}: {category}")
    if rel.startswith(".claude/") or rel.startswith(".agents/") or rel.startswith(".github/"):
        raise ValueError(f"Never remove active agent or CI infrastructure: {rel}")
    if rel.startswith("stories/lion_and_mouse_v6/"):
        if category != "legacy_v6":
            raise ValueError(f"Wrong V6 category: {rel}")
        return
    if rel.startswith("character/characters/_chrono_probe/"):
        if category != "chrono_probe":
            raise ValueError(f"Wrong probe category: {rel}")
        return
    if rel.startswith("stories/lion_and_mouse_v7/review/"):
        if category != "review_derivative" or is_protected_evidence(rel):
            raise ValueError(f"Current V7 approval/provenance evidence protected: {rel}")
        # Keep cleanup tooling documentation outside old reviews, and protect owner records.
        if any(t in rel.lower() for t in ("owner_", "approved", "acceptance", "selection", "authority")):
            raise ValueError(f"Current V7 owner authority protected: {rel}")
        return
    if category == "superseded_revision" and rel.startswith("character/") and IMAGE_REV.search(rel):
        # Never delete canons, active selected variants or final release render surfaces.
        if "/canonical/" in rel.lower() or is_protected_evidence(rel):
            raise ValueError(f"Canonical/selected asset protected: {rel}")
        return
    raise ValueError(f"Not in a narrowly allowed cleanup class: {rel}")


def _run_tests(root: Path, commands: list[list[str]], stage: str) -> None:
    if not isinstance(commands, list) or not commands or len(commands) > 8:
        raise ValueError("1-8 focused validation commands required")
    for cmd in commands:
        if (not isinstance(cmd, list) or len(cmd) < 3 or len(cmd) > 20 or
                any(not isinstance(c, str) or not c or "\0" in c for c in cmd)):
            raise ValueError("Invalid test argv list")
        name = PurePosixPath(cmd[0]).name
        if name not in {"python", "python3", "python3.11", "python3.12", "python3.13"}:
            raise ValueError("Validation command must use Python, no shell")
        if cmd[1:3] != ["-m", "unittest"] and not (cmd[1].startswith("production/") and cmd[1].endswith(".py")):
            raise ValueError("Validation must be unittest or a production Python validator")
        print(f"{stage}: {' '.join(cmd)}", flush=True)
        try:
            proc = subprocess.run(cmd, cwd=root, timeout=180, check=False,
                                  capture_output=True, text=True)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"{stage} validation timeout: {cmd}") from exc
        if proc.returncode != 0:
            print((proc.stdout + "\n" + proc.stderr)[-1800:], file=sys.stderr)
            raise RuntimeError(f"{stage} validation failed ({proc.returncode}): {cmd}")


def _relative_link_targets(root: Path, retained: str, text: str) -> set[str]:
    """Extract static HTML/Markdown link targets relative to tracked file."""
    refs = HTML_REF_RE.findall(text) + MD_REF_RE.findall(text)
    out = set()
    for raw in refs:
        path = unquote(urlsplit(raw).path)
        if not path or path.startswith(("http:", "https:", "mailto:", "data:", "//")):
            continue
        if path.startswith("/") or "\\" in path:
            continue
        # Process ../ for links only; disallow actual filesystem escape.
        bits = list(PurePosixPath(retained).parts[:-1])
        good = True
        for part in PurePosixPath(path).parts:
            if part == "..":
                if bits: bits.pop()
                else: good = False; break
            elif part != ".":
                bits.append(part)
        if good: out.add("/".join(bits))
    return out


def _reference_blockers(root: Path, removed: set[str], hashes: dict[str,str], known: set[str]) -> list[str]:
    """Conservative retained-text scan; cannot certify dynamically generated paths."""
    blockers = []
    relevant = [p for p in sorted(known - removed) if Path(p).suffix.lower() in
                {".json", ".jsonl", ".md", ".html", ".py", ".yaml", ".yml", ".toml", ".txt", ".sh", ".csv"}]
    removed_names = [(p, PurePosixPath(p).name) for p in sorted(removed)]
    roots = set()
    for path in removed:
        if path.startswith("stories/lion_and_mouse_v6/"): roots.add("stories/lion_and_mouse_v6")
        if path.startswith("character/characters/_chrono_probe/"): roots.add("_chrono_probe")
    for rel in relevant:
        local = root / rel
        try:
            # Extremely large generated JSON is not parsed as binary. Limit per-file scan.
            if local.stat().st_size > 40 * 1024 * 1024:
                blockers.append(f"Cannot scan oversized retained file: {rel}")
                if len(blockers)>=30: return blockers
                continue
            content = local.read_bytes()
            if b"\0" in content[:1024]: continue
            text = content.decode("utf8", "replace")
        except OSError:
            blockers.append(f"Cannot scan retained file: {rel}")
            if len(blockers)>=30: return blockers
            continue
        # Explicit retained paths, hashes, and known static links.
        links = _relative_link_targets(root, rel, text)
        for p, basename in removed_names:
            if (p in text or hashes[p] in text or p in links or
                    (basename not in GENERIC_NAMES and len(basename)>15 and basename in text)):
                blockers.append(f"Retained reference {rel} -> {p}")
                if len(blockers)>=30: return blockers
        # If removing a legacy root, references to its root name are potentially dynamic.
        for term in roots:
            if term in text:
                blockers.append(f"Retained legacy-root reference {rel} -> {term}")
                if len(blockers)>=30: return blockers
    return blockers


def verify(root: Path, manifest: dict) -> dict:
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA:
        raise ValueError("Unsupported cleanup manifest")
    branch, head = _clean_committed(root)
    if (manifest.get("source_branch") != branch or manifest.get("source_head") != head):
        raise ValueError("Manifest HEAD/branch stale; regenerate for newly committed state")
    known = set(tracked(root))
    authority = manifest.get("authority_records")
    if not isinstance(authority, list) or len(authority)<2:
        raise ValueError("Exact current owner selection and scene-use resolution records required")
    roles, authority_evidence, forbidden = set(), [], set()
    for row in authority:
        if not isinstance(row,dict) or set(row)!={"role","path","sha256"}:
            raise ValueError("Invalid authority record")
        if row["role"] not in {"owner_selection","scene_use_resolution","performance_registry","source_plan"}:
            raise ValueError("Unknown authority role")
        x=_entry(root,{"path":row["path"],"sha256":row["sha256"]},known,"authority")
        authority_evidence.append(x);roles.add(row["role"]);forbidden.add(x[0])
    if not {"owner_selection","scene_use_resolution"}.issubset(roles):
        raise ValueError("Missing independent owner-selection or scene-use authority")
    keep = manifest.get("keep")
    if not isinstance(keep, list) or not keep:
        raise ValueError("Exact-hash retained selected assets/lineage must be listed in keep")
    keeps = {}
    for x in keep:
        rel,_,sha=_entry(root,x,known,"keep")
        if rel in keeps: raise ValueError("Duplicate keep entry")
        keeps[rel]=sha
    files=manifest.get("files")
    if not isinstance(files,list) or not files or len(files)>MAX_FILES:
        raise ValueError(f"Supply 1-{MAX_FILES} exact paths per commit")
    deletions, categories = {}, {}
    for row in files:
        if not isinstance(row,dict) or set(row)!={"path","sha256","category"} and set(row)!={"path","sha256","category","replacement","owner_record"}:
            raise ValueError("Each candidate needs path/hash/category; superseded requires replacement+owner_record")
        rel,_,sha=_entry(root,{"path":row["path"],"sha256":row["sha256"]},known,"candidate")
        if rel in deletions: raise ValueError("Duplicate deletion entry")
        category=row["category"]
        _safe_scope(rel,category)
        if rel in keeps or rel in forbidden:
            raise ValueError(f"Cannot delete selected or authority file: {rel}")
        if category=="superseded_revision":
            if set(row)!={"path","sha256","category","replacement","owner_record"}:
                raise ValueError(f"Superseded revision lacks exact selected replacement: {rel}")
            replacement=row["replacement"]
            if not isinstance(replacement,dict) or set(replacement)!={"path","sha256"}:
                raise ValueError("Invalid replacement reference")
            repl=replacement["path"]
            if repl not in keeps or keeps[repl]!=replacement["sha256"]:
                raise ValueError("Replacement must be an exact-hash KEEP asset")
            record=row["owner_record"]
            if record not in forbidden or not any(a[0]==record and a[2]==sha256(root/record) for a in authority_evidence):
                raise ValueError("Selected replacement requires a verified owner record")
            data=(root/record).read_text(encoding="utf8")
            if replacement["sha256"] not in data or (repl not in data and PurePosixPath(repl).name not in data):
                raise ValueError("Owner record does not name selected replacement + hash")
        else:
            if set(row)!={"path","sha256","category"}:
                raise ValueError("Non-revision removal must not carry made-up replacement")
        deletions[rel]=sha;categories[rel]=category
    for rel, sha in deletions.items():
        if _committed_sha(root,rel)!=sha:
            raise ValueError(f"Committed Git bytes are unavailable or changed: {rel}")
    blockers=_reference_blockers(root,set(deletions),deletions,known)
    if blockers:
        raise ValueError("Retained references prevent automatic removal:\n  - "+"\n  - ".join(blockers))
    cmds=manifest.get("validation_commands")
    if not isinstance(cmds,list) or not cmds:
        raise ValueError("Focused validation commands required")
    return {"branch":branch,"head":head,"count":len(deletions),
            "bytes":sum((root/p).stat().st_size for p in deletions),
            "files":deletions,"categories":categories,"keep":keeps,
            "validation_commands":cmds,"authority_records":authority}


def _staged_delete_paths(root:Path) -> set[str]:
    raw=git(root,"diff","--cached","--name-status","-z").stdout.split(b"\0")
    if raw and raw[-1]==b"":raw.pop()
    if len(raw)%2:raise RuntimeError("Unexpected staged diff shape")
    return_paths=set()
    for i in range(0,len(raw),2):
        status,path=raw[i].decode(),raw[i+1].decode("utf8","surrogateescape")
        if status!="D":raise RuntimeError(f"Unexpected staged change: {status} {path}")
        return_paths.add(path)
    return return_paths


def apply(root:Path, manifest:dict, *, commit:bool=True) -> dict:
    result=verify(root,manifest)
    _run_tests(root,result["validation_commands"],"BEFORE")
    branch,head=_clean_committed(root)
    if (branch,head)!=(result["branch"],result["head"]):
        raise RuntimeError("Branch/HEAD changed during prechecks")
    # The manifest pin and repeat check defend against concurrent edits to requested bytes.
    for p,h in result["files"].items():
        if sha256(root/p)!=h:raise RuntimeError(f"Cleanup source changed: {p}")
    paths=sorted(result["files"])
    staged=[]
    try:
        for start in range(0,len(paths),60):
            chunk=paths[start:start+60]
            proc=git(root,"rm","--quiet","--",*chunk)
            staged.extend(chunk)
        if _staged_delete_paths(root)!=set(paths):
            raise RuntimeError("Staged diff differs from exact manifest")
        if git(root,"diff","--quiet",check=False).returncode!=0:
            raise RuntimeError("Unexpected unstaged modifications")
        for p,h in result["keep"].items():
            if sha256(root/p)!=h:
                raise RuntimeError(f"Protected KEEP bytes changed: {p}")
        for a in result["authority_records"]:
            if sha256(root/a["path"])!=a["sha256"]:
                raise RuntimeError(f"Authority changed: {a['path']}")
        _run_tests(root,result["validation_commands"],"AFTER")
        if git(root,"diff","--quiet",check=False).returncode!=0:
            raise RuntimeError("Posttests modified tracked files")
        if _staged_delete_paths(root)!=set(paths):
            raise RuntimeError("Posttests modified the staged diff")
        if commit:
            p=git(root,"commit","-m",f"chore: prune {len(paths)} committed superseded Feltwillow files")
            if git(root,"rev-parse","HEAD").stdout.decode().strip()==head:
                raise RuntimeError("Git commit did not advance HEAD")
            state="COMMITTED_LOCAL_NO_PUSH"
        else:
            state="STAGED_LOCAL_NO_PUSH"
        return {"status":state,"base_head":head,"head":git(root,"rev-parse","HEAD").stdout.decode().strip(),
                "files_removed":len(paths),"removed_worktree_bytes":result["bytes"],
                "scope_categories":sorted(set(result["categories"].values())),
                "warning":"Git history retains bytes. Local commits are not an external backup; no push/history rewrite/GC."}
    except Exception:
        if staged and git(root,"rev-parse","HEAD").stdout.decode().strip()==head:
            # Only undo the exact files we staged; never reset or touch unrelated paths.
            for start in range(0,len(staged),60):
                git(root,"restore","--source=HEAD","--staged","--worktree","--",*staged[start:start+60])
        raise


def main(argv=None)->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo",required=True)
    ap.add_argument("--manifest",type=Path,required=True)
    mode=ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run",action="store_true")
    mode.add_argument("--apply",action="store_true")
    ap.add_argument("--no-commit",action="store_true",help="Stage exact files without making cleanup commit")
    args=ap.parse_args(argv)
    try:
        root=repo_root(args.repo)
        manifest=json.loads(args.manifest.read_text())
        if args.dry_run:
            r=verify(root,manifest)
            print(json.dumps({"status":"VALIDATED_DRY_RUN_ONLY","branch":r["branch"],"head":r["head"],
                              "files":r["count"],"working_tree_bytes":r["bytes"]},indent=2))
        else:
            print(json.dumps(apply(root,manifest,commit=not args.no_commit),indent=2))
        return 0
    except (ValueError,RuntimeError,FileNotFoundError,FileExistsError,OSError,subprocess.SubprocessError,json.JSONDecodeError) as exc:
        print(f"BLOCKED: {exc}",file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
