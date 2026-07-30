"""Executable Gate 1 checks for the committed source/quotation audit ledger."""

from __future__ import annotations

import re
from pathlib import Path

from labauto_observatory.io import read_csv

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "data/derived/source_quote_audit.csv"
QUOTE_BANK_PATH = ROOT / "data/derived/quote_bank.csv"
REFERENCES_PATH = ROOT / "paper/references.bib"

EXPECTED_COLUMNS = (
    "Audit ID",
    "Source URL",
    "Source title",
    "Source date",
    "Source role",
    "Bib keys",
    "Quote-bank codes",
    "Approved exact quotation",
    "Surrounding-context result",
    "Later-update result",
    "Product-report status",
    "Required correction",
    "Supported claim boundary",
    "Prohibited inference",
    "Review status",
)

FORUM_SITE_KEY_RE = re.compile(r"@\w+\{((?:forum_|labautomation_)\w+),")


def _split_codes(cell: str) -> list[str]:
    return [part.strip() for part in cell.split(";") if part.strip()]


def _audit_rows() -> list[dict[str, str]]:
    rows = read_csv(AUDIT_PATH)
    assert list(rows[0]) == list(EXPECTED_COLUMNS)
    return rows


def _forum_site_bib_keys() -> set[str]:
    return set(FORUM_SITE_KEY_RE.findall(REFERENCES_PATH.read_text(encoding="utf-8")))


def test_source_quote_audit_has_twenty_four_complete_rows() -> None:
    rows = _audit_rows()
    assert len(rows) == 24
    ids = [row["Audit ID"] for row in rows]
    assert ids == [f"SQA-{index:02d}" for index in range(1, 25)]
    assert len(set(ids)) == 24
    for row in rows:
        assert row["Audit ID"].strip()
        assert row["Source URL"].strip()
        assert row["Review status"] == "complete"
        assert row["Surrounding-context result"].strip()
        assert row["Later-update result"].strip()


def test_every_quote_bank_entry_maps_to_exactly_one_audit_row() -> None:
    audit = _audit_rows()
    quotes = read_csv(QUOTE_BANK_PATH)
    for quote in quotes:
        matches = [
            row
            for row in audit
            if quote["Source URL"] == row["Source URL"]
            and quote["Code"] in _split_codes(row["Quote-bank codes"])
        ]
        assert len(matches) == 1, quote["Source URL"]
        approved = matches[0]["Approved exact quotation"]
        assert approved == quote["Short anonymized quotation"]


def test_every_manuscript_forum_site_bib_key_maps_to_exactly_one_audit_row() -> None:
    audit = _audit_rows()
    for key in sorted(_forum_site_bib_keys()):
        matches = [row for row in audit if key in _split_codes(row["Bib keys"])]
        assert len(matches) == 1, key


def test_quote_mapped_rows_have_resolved_corrections() -> None:
    for row in _audit_rows():
        if not row["Quote-bank codes"].strip():
            continue
        correction = row["Required correction"].strip().lower()
        assert correction == "none" or correction.startswith("applied:")
