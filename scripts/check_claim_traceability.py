#!/usr/bin/env python3
"""Check that every approved publication claim is traceable to the manuscript."""

from __future__ import annotations

from pathlib import Path

from labauto_observatory.traceability import (
    check_traceability,
    format_report,
    manuscript_tree_present,
)

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"


def main() -> None:
    BUILD.mkdir(exist_ok=True)
    if not manuscript_tree_present(ROOT):
        note = (
            "# Claim traceability\n\n"
            "Skipped: `paper/` is local-only and is not present in this checkout.\n"
            "Run this check on a machine that holds the manuscript tree.\n"
        )
        (BUILD / "claim_traceability.md").write_text(note, encoding="utf-8")
        print("paper/ not present; skipped manuscript claim traceability")
        return

    report = check_traceability(ROOT)
    (BUILD / "claim_traceability.md").write_text(format_report(report), encoding="utf-8")
    if not report.ok:
        for problem in report.problems:
            print(f"claim traceability failure: {problem}")
        raise SystemExit(1)
    print(f"traced {len(report.approved)} approved claims to the manuscript sources")


if __name__ == "__main__":
    main()
