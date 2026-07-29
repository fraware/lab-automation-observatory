"""Checks on the generated Markdown rendering of the evidence atlas.

``docs/generated/evidence_atlas_summary.md`` is derived from
``data/derived/evidence_atlas.csv`` alone, so every value it prints must be
copied verbatim from the committed atlas and nothing may be authored here by
hand. These tests cover the happy path and the drift-detection failure modes,
matching the pattern already used for ``pairwise_associations.csv`` and
``evidence_atlas.csv`` in ``tests/test_derived_artifacts.py``.
"""

from __future__ import annotations

from pathlib import Path

from labauto_observatory.atlas import ATLAS_RELATIVE, build_records
from labauto_observatory.atlas_summary import (
    SUMMARY_RELATIVE,
    atlas_summary_drift,
    render_atlas_summary,
    write_atlas_summary,
)
from labauto_observatory.io import read_csv

ROOT = Path(__file__).resolve().parents[1]
CONSTRUCTS = [f"B{index}" for index in range(1, 11)]


def test_committed_atlas_summary_matches_its_source() -> None:
    assert atlas_summary_drift(ROOT) == []


def test_summary_covers_every_construct_in_order() -> None:
    rendered = render_atlas_summary(ROOT)
    atlas = read_csv(ROOT / ATLAS_RELATIVE)
    headings = [line for line in rendered.splitlines() if line.startswith("## ")]
    assert len(headings) == len(CONSTRUCTS) == len(atlas)
    for code, heading in zip(CONSTRUCTS, headings, strict=True):
        assert heading.startswith(f"## {code} -- ")


def test_summary_values_are_copied_verbatim_from_the_atlas() -> None:
    rendered = render_atlas_summary(ROOT)
    for row in build_records(ROOT):
        assert row["Bounded quantitative result"] in rendered
        assert row["Evidence maturity"] in rendered
        if row["Short anonymized quotation"]:
            assert row["Short anonymized quotation"] in rendered


def test_summary_points_back_to_the_atlas_and_regeneration_command() -> None:
    rendered = render_atlas_summary(ROOT)
    assert ATLAS_RELATIVE in rendered
    assert "make atlas-summary" in rendered
    assert "build_atlas_summary.py" in rendered


def test_drift_check_reports_a_missing_artifact(tmp_path: Path) -> None:
    assert atlas_summary_drift(tmp_path) == [
        f"{SUMMARY_RELATIVE} is missing; run `make atlas-summary`"
    ]


def test_write_atlas_summary_restores_a_hand_edited_file(data_root: Path) -> None:
    target = write_atlas_summary(data_root)
    assert target == data_root / SUMMARY_RELATIVE
    original = target.read_text(encoding="utf-8")

    target.write_text(original.replace("Knowledge packaging", "Something else"), encoding="utf-8")
    assert atlas_summary_drift(data_root) == [
        f"{SUMMARY_RELATIVE} has drifted from {ATLAS_RELATIVE}; run `make atlas-summary`"
    ]

    assert write_atlas_summary(data_root) == target
    assert atlas_summary_drift(data_root) == []


def test_drift_check_ignores_checkout_line_endings(data_root: Path) -> None:
    """A CRLF working tree is a checkout artifact, not drift.

    Git stores this file with LF and hands Windows working trees CRLF, so a
    byte-for-byte comparison would fail `make validate` on a fresh clone.
    """

    target = write_atlas_summary(data_root)
    committed = target.read_text(encoding="utf-8")
    assert "\r\n" not in committed
    with target.open("w", encoding="utf-8", newline="\r\n") as handle:
        handle.write(committed)
    assert atlas_summary_drift(data_root) == []
