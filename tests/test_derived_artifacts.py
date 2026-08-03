"""Checks on the two CSVs that are generated from other committed data.

``pairwise_associations.csv`` and ``evidence_atlas.csv`` are derived artifacts:
they are committed for readers who do not run the pipeline, and `make validate`
fails if either drifts from the sources it is built from. These tests cover both
the happy path and the failure reports that a hand edit would produce.
"""

from __future__ import annotations

import csv
from collections.abc import Callable
from itertools import combinations
from pathlib import Path

import pytest

from labauto_observatory.associations import (
    ANNOTATIONS_RELATIVE,
    LIFT_THRESHOLD,
    PAIRWISE_RELATIVE,
    PHI_THRESHOLD,
    TECHNICAL_CODES,
    build_records,
    contingency,
    format_number,
    pairwise_drift,
    read_annotations,
    read_register,
    write_pairwise_csv,
)
from labauto_observatory.atlas import (
    ATLAS_RELATIVE,
    HEADER,
    NO_PAIRWISE,
    atlas_drift,
    write_atlas_csv,
)
from labauto_observatory.atlas import build_records as build_atlas_records
from labauto_observatory.io import read_csv

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PAIRS = 28
CONSTRUCTS = [f"B{index}" for index in range(1, 11)]


def test_committed_pairwise_table_matches_the_register() -> None:
    assert pairwise_drift(ROOT) == []


def test_committed_atlas_matches_its_sources() -> None:
    assert atlas_drift(ROOT) == []


def test_pairwise_covers_every_technical_pair_once() -> None:
    records = build_records(ROOT)
    assert len(records) == EXPECTED_PAIRS
    pairs = [(row["Code A"], row["Code B"]) for row in records]
    assert sorted(pairs) == sorted(combinations(TECHNICAL_CODES, 2))


def test_pairwise_is_ranked_by_descending_phi() -> None:
    records = build_records(ROOT)
    assert [int(row["Rank order"]) for row in records] == list(range(1, EXPECTED_PAIRS + 1))
    phis = [float(row["Phi"]) for row in records]
    assert phis == sorted(phis, reverse=True)
    assert (records[0]["Code A"], records[0]["Code B"]) == ("B5", "B6")


def test_pairwise_counts_partition_the_register() -> None:
    register = read_register(ROOT)
    counts = contingency(register, "B5", "B6")
    assert counts == (8, 9, 3, 35)
    assert sum(counts) == len(register)


def test_pilot_threshold_flag_follows_both_thresholds() -> None:
    for row in build_records(ROOT):
        met = float(row["Phi"]) >= PHI_THRESHOLD and float(row["Lift"]) >= LIFT_THRESHOLD
        assert row["Pilot threshold met?"] == ("Yes" if met else "No")


def test_sensitivity_columns_bracket_the_point_estimate() -> None:
    for row in build_records(ROOT):
        if not row["Phi if overlap \u22121"] or not row["Phi if overlap +1"]:
            continue
        low = float(row["Phi if overlap \u22121"])
        high = float(row["Phi if overlap +1"])
        assert low <= float(row["Phi"]) <= high
        assert float(row["Sensitivity width"]) == pytest.approx(high - low)


@pytest.mark.parametrize(
    ("value", "expected"),
    [(None, ""), (1.0, "1"), (0.0, "0"), (-2.0, "-2"), (0.5, "0.5")],
)
def test_format_number(value: float | None, expected: str) -> None:
    assert format_number(value) == expected


def test_write_pairwise_csv_restores_a_hand_edited_table(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    target = data_root / PAIRWISE_RELATIVE
    edit_csv(target, 0, Phi="0.999")
    assert pairwise_drift(data_root) == [
        f"{PAIRWISE_RELATIVE} has drifted from the evidence register; run `make derived`"
    ]
    assert write_pairwise_csv(data_root) == target
    assert pairwise_drift(data_root) == []


def test_write_atlas_csv_restores_a_hand_edited_atlas(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    target = data_root / ATLAS_RELATIVE
    edit_csv(target, 0, Bottleneck="Something else")
    assert atlas_drift(data_root) == [
        f"{ATLAS_RELATIVE} has drifted from its sources; run `make derived`"
    ]
    assert write_atlas_csv(data_root) == target
    assert atlas_drift(data_root) == []


def test_drift_checks_report_a_missing_artifact(tmp_path: Path) -> None:
    assert pairwise_drift(tmp_path) == [f"{PAIRWISE_RELATIVE} is missing; run `make derived`"]
    assert atlas_drift(tmp_path) == [f"{ATLAS_RELATIVE} is missing; run `make derived`"]


@pytest.mark.parametrize("relative", [PAIRWISE_RELATIVE, ATLAS_RELATIVE])
def test_drift_checks_ignore_checkout_line_endings(data_root: Path, relative: str) -> None:
    """A CRLF working tree is a checkout artifact, not drift.

    Git stores these files with LF and may hand Windows clones CRLF, so a
    byte-for-byte comparison would fail `make validate` on a fresh clone.
    """

    target = data_root / relative
    with target.open(encoding="utf-8", newline="") as handle:
        committed = handle.read().replace("\r\n", "\n")
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(committed)
    with target.open("w", encoding="utf-8", newline="\r\n") as handle:
        handle.write(committed)
    assert pairwise_drift(data_root) == []
    assert atlas_drift(data_root) == []


def test_read_register_requires_at_least_one_part(tmp_path: Path) -> None:
    (tmp_path / "data/derived").mkdir(parents=True)
    with pytest.raises(FileNotFoundError, match="no evidence register parts"):
        read_register(tmp_path)


def test_annotations_must_not_be_empty(data_root: Path) -> None:
    target = data_root / ANNOTATIONS_RELATIVE
    header = target.read_text(encoding="utf-8").splitlines()[0]
    target.write_text(header + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="annotations are empty"):
        read_annotations(data_root)


def test_annotations_must_carry_every_prose_column(data_root: Path) -> None:
    target = data_root / ANNOTATIONS_RELATIVE
    rows = read_csv(target)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["Code A", "Code B", "Interpretation"], extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="missing columns"):
        read_annotations(data_root)


def test_every_pair_must_be_annotated(
    data_root: Path, drop_csv_row: Callable[[Path, int], None]
) -> None:
    drop_csv_row(data_root / ANNOTATIONS_RELATIVE, 0)
    with pytest.raises(ValueError, match="missing pairs"):
        build_records(data_root)


def test_atlas_has_one_row_per_construct() -> None:
    records = build_atlas_records(ROOT)
    assert [row["Code"] for row in records] == CONSTRUCTS
    assert all(set(row) == set(HEADER) for row in records)


def test_atlas_binds_every_construct_to_a_denominator() -> None:
    """No atlas row may state a bare percentage."""

    for row in build_atlas_records(ROOT):
        result = row["Bounded quantitative result"]
        assert result
        assert row["Evidence maturity"]
        assert row["Key sources"]
        if "%" in result:
            assert any(marker in result for marker in ("over", "/", "of"))


def test_atlas_marks_constructs_outside_the_pairwise_set() -> None:
    relationships = {
        row["Code"]: row["Strongest descriptive relationship"] for row in build_atlas_records(ROOT)
    }
    assert relationships["B1"] == NO_PAIRWISE
    assert relationships["B10"] == NO_PAIRWISE
    assert relationships["B5"].startswith("B5--B6")


def test_atlas_reports_the_retained_counterexamples() -> None:
    counterexamples = {
        row["Code"]: row["Retained counterexample"] for row in build_atlas_records(ROOT)
    }
    negative_cases = read_csv(ROOT / "data/derived/negative_cases.csv")
    assert any(counterexamples[code] for code in CONSTRUCTS)
    listed = {case for value in counterexamples.values() for case in value.split("; ") if case}
    assert listed <= {row["Case"] for row in negative_cases}
