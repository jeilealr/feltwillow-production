"""Report broken repository-relative links in tracked Markdown documents.

Historical or ignored local artifacts should be written as code paths, not
clickable relative links that fail in a clean checkout. External links and
same-page anchors are outside this check.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


REPO = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]]+\]\(([^)]+)\)")


def repository_files(repo: Path = REPO) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    return sorted((repo / item.decode("utf-8")).resolve() for item in result.stdout.split(b"\0") if item)


def broken_links(document: Path, repo: Path = REPO, available: set[Path] | None = None) -> list[str]:
    problems: list[str] = []
    for number, line in enumerate(document.read_text(encoding="utf-8").splitlines(), 1):
        for match in LINK.finditer(line):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            path = (document.parent / unquote(parts.path)).resolve()
            present = path.exists() if available is None else (
                path in available or (path.is_dir() and any(path in candidate.parents for candidate in available))
            )
            if not present:
                problems.append(f"{document.relative_to(repo)}:{number}: {target}")
    return problems


def repository_links(repo: Path = REPO) -> list[str]:
    available = set(repository_files(repo))
    return [
        problem
        for document in sorted(path for path in available if path.suffix == ".md")
        for problem in broken_links(document, repo, available)
    ]


def main() -> int:
    problems = repository_links()
    if problems:
        print("\n".join(problems))
        return 1
    print("All repository-relative Markdown links resolve in this checkout.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
