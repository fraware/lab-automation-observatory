"""Checks on the blind projection of the hard-case adjudication set.

``data/derived/reliability_subset_blind.csv`` exists so that a second coder can
reach the threads and the adjudication questions without reading the expected
primary code. Two properties matter and are asserted here: the projection is
derived from the key alone, and it carries none of the answer-key columns.
"""

from __future__ import annotations

import csv
from collections.abc import Callable
from pathlib import Path

import pytest

from labauto_observatory.blind_subset import (
    BLIND_COLUMNS,
    BLIND_RELATIVE,
    SUBSET_RELATIVE,
    WITHHELD_COLUMNS,
    blind_subset_drift,
    build_records,
    render_blind_csv,
    write_blind_csv,
)
from labauto_observatory.io import read_csv

ROOT = Path(__file__).resolve().parents[1]


def test_committed_blind_sheet_matches_its_key() -> None:
    assert blind_subset_drift(ROOT) == []


def test_blind_sheet_withholds_every_answer_key_column() -> None:
    """The point of the projection: no expected primary, alternative, or reason."""

    header = read_csv(ROOT / BLIND_RELATIVE)[0]
    key_header = read_csv(ROOT / SUBSET_RELATIVE)[0]
    assert set(BLIND_COLUMNS) & set(WITHHELD_COLUMNS) == set()
    for column in WITHHELD_COLUMNS:
        assert column in key_header
        assert column not in header
    rendered = render_blind_csv(ROOT)
    for row, projected in zip(read_csv(ROOT / SUBSET_RELATIVE), build_records(ROOT), strict=True):
        for column in WITHHELD_COLUMNS:
            assert row[column]
            # A one-token code such as `B4` also occurs inside the recorded
            # adjudication questions, so the test that matters is that no
            # projected cell restates a withheld cell.
            assert row[column] not in projected.values()
        assert row["Why disagreement is likely"] not in rendered


def test_blind_sheet_covers_every_thread_in_key_order() -> None:
    key = read_csv(ROOT / SUBSET_RELATIVE)
    blind = read_csv(ROOT / BLIND_RELATIVE)
    assert [row["Thread ID"] for row in blind] == [row["Thread ID"] for row in key]
    assert list(blind[0]) == list(BLIND_COLUMNS)


def test_blind_cells_are_copied_verbatim_from_the_key() -> None:
    key = read_csv(ROOT / SUBSET_RELATIVE)
    for projected, row in zip(build_records(ROOT), key, strict=True):
        assert projected == {column: row[column] for column in BLIND_COLUMNS}


def test_blind_sheet_gives_a_coder_the_thread_and_the_question() -> None:
    for row in read_csv(ROOT / BLIND_RELATIVE):
        assert row["Source URL"].startswith("https://")
        assert row["Specific adjudication question"].endswith("?")
        assert row["Episode segmentation required"]
        assert row["Priority"] in {"Critical", "High"}


def test_drift_check_reports_a_missing_artifact(tmp_path: Path) -> None:
    assert blind_subset_drift(tmp_path) == [f"{BLIND_RELATIVE} is missing; run `make derived`"]


def test_write_blind_csv_restores_a_hand_edited_sheet(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    target = write_blind_csv(data_root)
    assert target == data_root / BLIND_RELATIVE
    edit_csv(target, 0, Thread="Something else")
    assert blind_subset_drift(data_root) == [
        f"{BLIND_RELATIVE} has drifted from {SUBSET_RELATIVE}; run `make derived`"
    ]
    assert write_blind_csv(data_root) == target
    assert blind_subset_drift(data_root) == []


def test_a_key_edit_is_reported_as_drift(data_root: Path, edit_csv: Callable[..., None]) -> None:
    """The sheet is a projection: correcting the key must force a rebuild."""

    write_blind_csv(data_root)
    edit_csv(data_root / SUBSET_RELATIVE, 0, Priority="High")
    assert blind_subset_drift(data_root) == [
        f"{BLIND_RELATIVE} has drifted from {SUBSET_RELATIVE}; run `make derived`"
    ]


def test_drift_check_ignores_checkout_line_endings(data_root: Path) -> None:
    """A CRLF working tree is a checkout artifact, not drift."""

    target = write_blind_csv(data_root)
    with target.open(encoding="utf-8", newline="") as handle:
        committed = handle.read()
    assert "\r\n" not in committed
    with target.open("w", encoding="utf-8", newline="\r\n") as handle:
        handle.write(committed)
    assert blind_subset_drift(data_root) == []


def test_an_empty_key_is_refused(data_root: Path) -> None:
    target = data_root / SUBSET_RELATIVE
    header = target.read_text(encoding="utf-8").splitlines()[0]
    target.write_text(header + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="adjudication set is empty"):
        build_records(data_root)


def test_a_key_without_a_coder_facing_column_is_refused(data_root: Path) -> None:
    target = data_root / SUBSET_RELATIVE
    rows = read_csv(target)
    fieldnames = [column for column in rows[0] if column != "Priority"]
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="missing coder-facing columns"):
        build_records(data_root)
