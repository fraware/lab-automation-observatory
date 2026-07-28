"""Claim-ledger to manuscript traceability checks."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from labauto_observatory.traceability import (
    ANCHOR_COLUMN,
    LEDGER_RELATIVE,
    check_traceability,
    find_markers,
    format_report,
    normalize,
    read_claims,
    strip_latex_comments,
)

ROOT = Path(__file__).resolve().parents[1]
LEDGER_COLUMNS = ["Claim ID", "Prohibited overclaim", ANCHOR_COLUMN, "Status"]


def build_root(tmp_path: Path, rows: list[dict[str, str]], sources: dict[str, str]) -> Path:
    """Create a minimal repository layout with a ledger and manuscript sources."""

    ledger = tmp_path / LEDGER_RELATIVE
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (tmp_path / "paper" / "sections").mkdir(parents=True, exist_ok=True)
    defaults = {"paper/main.tex": "", "paper/supplement.tex": ""}
    for relative, text in {**defaults, **sources}.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


def claim_row(claim_id: str, anchor: str, status: str = "Approved") -> dict[str, str]:
    return {
        "Claim ID": claim_id,
        "Prohibited overclaim": "do not overclaim",
        ANCHOR_COLUMN: anchor,
        "Status": status,
    }


def test_release_claims_are_traceable() -> None:
    report = check_traceability(ROOT)
    assert report.problems == ()
    assert report.ok
    assert len(report.approved) == 11
    assert all(trace.marker_files and trace.anchor_files for trace in report.approved)


def test_release_report_renders_every_claim() -> None:
    report = check_traceability(ROOT)
    rendered = format_report(report)
    assert "Approved claims traced: 11" in rendered
    for trace in report.traces:
        assert f"| {trace.claim.claim_id} |" in rendered
    assert "| C12 | Rejected | -- | -- |" in rendered
    assert "## Problems" not in rendered


def test_strip_latex_comments_preserves_escaped_percent() -> None:
    text = "Coverage was 52.5\\% overall. % claim: C01\nSecond line % trailing"
    assert strip_latex_comments(text) == "Coverage was 52.5\\% overall. \nSecond line "


def test_normalize_collapses_wrapped_prose() -> None:
    assert normalize("first\n  second\tthird ") == "first second third"


def test_find_markers_accepts_multiple_identifiers() -> None:
    assert find_markers("% claim: C06, C07\n%claim:c11\ntext % claim: C99") == ["C06", "C07", "C11"]


def test_read_claims_requires_traceability_columns(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.csv"
    ledger.write_text("Claim ID,Status\nC01,Approved\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Manuscript anchor"):
        read_claims(ledger)


def test_read_claims_rejects_empty_ledger(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.csv"
    ledger.write_text("Claim ID,Manuscript anchor,Status\n", encoding="utf-8")
    with pytest.raises(ValueError, match="empty"):
        read_claims(ledger)


def test_missing_manuscript_source_is_reported(tmp_path: Path) -> None:
    root = build_root(tmp_path, [claim_row("C01", "anchor phrase")], {})
    (root / "paper" / "supplement.tex").unlink()
    with pytest.raises(FileNotFoundError, match=r"supplement\.tex"):
        check_traceability(root)


def test_approved_claim_without_marker_fails(tmp_path: Path) -> None:
    root = build_root(
        tmp_path,
        [claim_row("C01", "anchor phrase")],
        {"paper/sections/04_results.tex": "The anchor phrase appears here.\n"},
    )
    report = check_traceability(root)
    assert not report.ok
    assert any("has no '% claim: C01' marker" in problem for problem in report.problems)


def test_approved_claim_without_anchor_fails(tmp_path: Path) -> None:
    root = build_root(
        tmp_path,
        [claim_row("C01", "")],
        {"paper/sections/04_results.tex": "% claim: C01\nProse.\n"},
    )
    report = check_traceability(root)
    assert any("has no manuscript anchor" in problem for problem in report.problems)


def test_anchor_absent_from_manuscript_fails(tmp_path: Path) -> None:
    root = build_root(
        tmp_path,
        [claim_row("C01", "missing phrase")],
        {"paper/sections/04_results.tex": "% claim: C01\nUnrelated prose.\n"},
    )
    report = check_traceability(root)
    assert any("anchor is absent from the manuscript" in problem for problem in report.problems)


def test_anchor_inside_comment_does_not_count(tmp_path: Path) -> None:
    root = build_root(
        tmp_path,
        [claim_row("C01", "anchor phrase")],
        {"paper/sections/04_results.tex": "% claim: C01\n% anchor phrase\nUnrelated prose.\n"},
    )
    report = check_traceability(root)
    assert any("anchor is absent from the manuscript" in problem for problem in report.problems)


def test_anchor_and_marker_must_be_colocated(tmp_path: Path) -> None:
    root = build_root(
        tmp_path,
        [claim_row("C01", "anchor phrase")],
        {
            "paper/sections/04_results.tex": "% claim: C01\nUnrelated prose.\n",
            "paper/sections/05_discussion.tex": "The anchor phrase appears here.\n",
        },
    )
    report = check_traceability(root)
    assert any("but its marker is in" in problem for problem in report.problems)


def test_wrapped_anchor_matches_across_lines(tmp_path: Path) -> None:
    root = build_root(
        tmp_path,
        [claim_row("C01", "anchor phrase spanning lines")],
        {"paper/sections/04_results.tex": "% claim: C01\nAn anchor phrase\nspanning lines here.\n"},
    )
    assert check_traceability(root).ok


def test_unknown_marker_is_reported(tmp_path: Path) -> None:
    root = build_root(
        tmp_path,
        [claim_row("C01", "anchor phrase")],
        {"paper/sections/04_results.tex": "% claim: C01, C42\nThe anchor phrase is here.\n"},
    )
    report = check_traceability(root)
    assert any("marks unknown claim C42" in problem for problem in report.problems)


def test_rejected_claim_must_not_be_marked_or_anchored(tmp_path: Path) -> None:
    root = build_root(
        tmp_path,
        [claim_row("C01", "anchor phrase"), claim_row("C12", "vendor ranking", status="Rejected")],
        {"paper/sections/04_results.tex": "% claim: C01, C12\nThe anchor phrase is here.\n"},
    )
    report = check_traceability(root)
    assert any("is marked in" in problem for problem in report.problems)
    assert any("must not declare a manuscript anchor" in problem for problem in report.problems)


def test_malformed_and_duplicate_identifiers_are_reported(tmp_path: Path) -> None:
    root = build_root(
        tmp_path,
        [claim_row("C1", "anchor phrase"), claim_row("C1", "anchor phrase")],
        {"paper/sections/04_results.tex": "% claim: C1\nThe anchor phrase is here.\n"},
    )
    report = check_traceability(root)
    assert any("malformed" in problem for problem in report.problems)
    assert any("duplicate claim identifier" in problem for problem in report.problems)


def test_report_lists_problems(tmp_path: Path) -> None:
    root = build_root(
        tmp_path,
        [claim_row("C01", "missing phrase")],
        {"paper/sections/04_results.tex": "% claim: C01\nUnrelated prose.\n"},
    )
    rendered = format_report(check_traceability(root))
    assert "## Problems" in rendered
    assert "anchor is absent" in rendered
