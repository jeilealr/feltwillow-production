"""Resolve/run C01–C52 CPU evidence; never turn it into a visual approval."""

from __future__ import annotations
import argparse, datetime, hashlib, json, subprocess, sys, time, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
ROOT = Path(__file__).resolve().parents[1]


def cases(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from cases(item)
        else:
            yield item


def load_requirements(path):
    doc = json.loads(Path(path).read_text())
    rows = doc["requirements"]
    if {r["id"] for r in rows} != {f"C{n:02}" for n in range(1, 53)} or len(rows) != 52:
        raise ValueError("exactly C01–C52 required")
    names = sorted({name for row in rows for name in row["tests"]})
    if not names or any(not name.startswith("tests.test_") for name in names):
        raise ValueError("only repository CPU tests may be mapped")
    suite = unittest.defaultTestLoader.loadTestsFromNames(names)
    actual = {test.id(): test for test in cases(suite)}
    if set(actual) != set(names):
        raise ValueError(
            "unknown/unloadable requirement test: " + str(set(names) - set(actual))
        )
    return doc, unittest.TestSuite(actual.values())


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outcomes = {}

    def addSuccess(self, test):
        super().addSuccess(test)
        self.outcomes[test.id()] = "passed"

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.outcomes[test.id()] = "failed"

    def addError(self, test, err):
        super().addError(test, err)
        self.outcomes[test.id()] = "error"

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.outcomes[test.id()] = "unavailable: " + reason


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--map", type=Path, default=ROOT / "tests/sequence_requirements.json"
    )
    p.add_argument("--run", action="store_true")
    p.add_argument("--out", type=Path)
    a = p.parse_args()
    doc, suite = load_requirements(a.map)
    if not a.run:
        print(
            json.dumps(
                dict(
                    requirements=52,
                    distinct_test_cases=suite.countTestCases(),
                    status="mapping_resolved_not_run",
                ),
                indent=2,
            )
        )
        return 0
    if not a.out:
        p.error("--out required for actual execution evidence")
    if a.out.exists():
        p.error("use a new evidence filename; previous results are immutable")
    start = time.monotonic()
    result = unittest.TextTestRunner(verbosity=1, resultclass=RecordedResult).run(suite)
    rows = []
    for row in doc["requirements"]:
        statuses = {name: result.outcomes.get(name, "not_run") for name in row["tests"]}
        rows.append(
            dict(
                row,
                cpu_status="passed"
                if all(s == "passed" for s in statuses.values())
                else "failed_or_unavailable",
                actual_tests=statuses,
                production_video_status="GPU_not_run; no visual/owner acceptance granted",
            )
        )
    files = [
        f
        for folder in ("production", "feltwillow", "tests")
        for f in (ROOT / folder).glob("*.py")
    ]
    report = dict(
        schema="feltwillow.requirements-evidence.v1",
        source_commit=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        interpreter=sys.executable,
        command=sys.argv,
        elapsed_seconds=time.monotonic() - start,
        tests_run=result.testsRun,
        failures=len(result.failures),
        errors=len(result.errors),
        skips=len(result.skipped),
        requirements=rows,
        code_sha256={
            f.relative_to(ROOT).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
            for f in files
        },
        GPU_not_run=True,
    )
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(report, indent=2) + "\n")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
