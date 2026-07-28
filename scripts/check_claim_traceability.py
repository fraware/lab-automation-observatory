#!/usr/bin/env python3
"""Check that every approved publication claim is traceable to the manuscript."""

from __future__ import annotations

from pathlib import Path

from labauto_observatory.traceability import check_traceability, format_report

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"


def main() -> None:
    report = check_traceability(ROOT)
    BUILD.mkdir(exist_ok=True)
    (BUILD / "claim_traceability.md").write_text(format_report(report), encoding="utf-8")
    if not report.ok:
        for problem in report.problems:
            print(f"claim traceability failure: {problem}")
        raise SystemExit(1)
    print(f"traced {len(report.approved)} approved claims to the manuscript sources")


if __name__ == "__main__":
    main()
