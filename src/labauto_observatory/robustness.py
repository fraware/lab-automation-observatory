"""Deterministic robustness analyses for publication-critical results.

The analyses in this module are descriptive stress tests over the purposively
selected release data. They do not create population estimates or inferential
p-values. Their purpose is to expose dependence on a conventional partial-score
weight and on any single selected thread.
"""

from __future__ import annotations

import csv
import io
from itertools import combinations
from pathlib import Path

from .analysis import (
    B2_COMPONENTS,
    B3_COMPONENTS,
    B4_COMPONENTS,
    B5_COMPONENTS,
    METRIC_FILES,
)
from .associations import (
    LIFT_THRESHOLD,
    PHI_THRESHOLD,
    TECHNICAL_CODES,
    contingency,
    format_number,
    read_register,
)
from .io import normalised_newlines, numeric, read_csv, read_text_lf
from .metrics import association_from_counts, mean_score

PARTIAL_WEIGHTS: tuple[float, ...] = (0.0, 0.25, 0.5, 0.75, 1.0)
PARTIAL_SCORE_RELATIVE = "data/robustness/partial_score_sensitivity.csv"
ASSOCIATION_LOTO_RELATIVE = "data/robustness/association_leave_one_out.csv"

COMPONENT_SPECS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("IAS", METRIC_FILES["b2"], B2_COMPONENTS),
    ("RMC", METRIC_FILES["b3"], B3_COMPONENTS),
    ("PDC", METRIC_FILES["b4"], B4_COMPONENTS),
    ("OC", METRIC_FILES["b5"], B5_COMPONENTS),
)

PARTIAL_HEADER: tuple[str, ...] = (
    "Metric",
    "Partial weight",
    "Mean",
    "Cases",
    "Known cells",
    "Unknown cells",
)

LOTO_HEADER: tuple[str, ...] = (
    "Full rank",
    "Code A",
    "Code B",
    "Full phi",
    "Full lift",
    "Minimum phi",
    "Maximum phi",
    "Minimum lift",
    "Maximum lift",
    "Minimum rank",
    "Maximum rank",
    "Top-five deletions",
    "Threshold-retained deletions",
    "Total deletions",
)


def _case_score(row: dict[str, str], columns: tuple[str, ...], partial_weight: float) -> float:
    """Recompute one case mean after replacing every scored 0.5 cell."""

    values: list[float] = []
    for column in columns:
        value = numeric(row[column])
        if value is None:
            continue
        values.append(partial_weight if value == 0.5 else value)
    return mean_score(values)


def partial_score_records(root: str | Path) -> list[dict[str, str]]:
    """Recompute IAS, RMC, PDC, and OC over five partial-score weights."""

    root_path = Path(root)
    records: list[dict[str, str]] = []
    for metric, relative, columns in COMPONENT_SPECS:
        rows = read_csv(root_path / relative)
        all_cells = [numeric(row[column]) for row in rows for column in columns]
        known_cells = sum(value is not None for value in all_cells)
        unknown_cells = len(all_cells) - known_cells
        for weight in PARTIAL_WEIGHTS:
            case_scores = [_case_score(row, columns, weight) for row in rows]
            records.append(
                {
                    "Metric": metric,
                    "Partial weight": format_number(weight),
                    "Mean": format_number(mean_score(case_scores)),
                    "Cases": str(len(rows)),
                    "Known cells": str(known_cells),
                    "Unknown cells": str(unknown_cells),
                }
            )
    return records


def _association_rows(rows: list[dict[str, str]]) -> list[tuple[str, str, float, float]]:
    """Return all technical pairs in deterministic descending-phi order."""

    values: list[tuple[str, str, float, float]] = []
    for code_a, code_b in combinations(TECHNICAL_CODES, 2):
        association = association_from_counts(*contingency(rows, code_a, code_b))
        values.append((code_a, code_b, association.phi, association.lift))
    values.sort(key=lambda entry: (-entry[2], entry[0], entry[1]))
    return values


def association_leave_one_out_records(root: str | Path) -> list[dict[str, str]]:
    """Delete each selected thread once and summarize pairwise stability."""

    rows = read_register(root)
    if len(rows) < 2:
        raise ValueError("leave-one-thread-out analysis requires at least two threads")

    full = _association_rows(rows)
    pairs = [(code_a, code_b) for code_a, code_b, _, _ in full]
    full_values = {(code_a, code_b): (phi, lift) for code_a, code_b, phi, lift in full}

    phis: dict[tuple[str, str], list[float]] = {pair: [] for pair in pairs}
    lifts: dict[tuple[str, str], list[float]] = {pair: [] for pair in pairs}
    ranks: dict[tuple[str, str], list[int]] = {pair: [] for pair in pairs}
    threshold_counts: dict[tuple[str, str], int] = {pair: 0 for pair in pairs}

    for deleted_index in range(len(rows)):
        subset = rows[:deleted_index] + rows[deleted_index + 1 :]
        ranked = _association_rows(subset)
        rank_map = {
            (code_a, code_b): rank
            for rank, (code_a, code_b, _, _) in enumerate(ranked, 1)
        }
        value_map = {
            (code_a, code_b): (phi, lift) for code_a, code_b, phi, lift in ranked
        }
        for pair in pairs:
            phi, lift = value_map[pair]
            phis[pair].append(phi)
            lifts[pair].append(lift)
            ranks[pair].append(rank_map[pair])
            if phi >= PHI_THRESHOLD and lift >= LIFT_THRESHOLD:
                threshold_counts[pair] += 1

    records: list[dict[str, str]] = []
    for full_rank, pair in enumerate(pairs, 1):
        full_phi, full_lift = full_values[pair]
        pair_ranks = ranks[pair]
        records.append(
            {
                "Full rank": str(full_rank),
                "Code A": pair[0],
                "Code B": pair[1],
                "Full phi": format_number(full_phi),
                "Full lift": format_number(full_lift),
                "Minimum phi": format_number(min(phis[pair])),
                "Maximum phi": format_number(max(phis[pair])),
                "Minimum lift": format_number(min(lifts[pair])),
                "Maximum lift": format_number(max(lifts[pair])),
                "Minimum rank": str(min(pair_ranks)),
                "Maximum rank": str(max(pair_ranks)),
                "Top-five deletions": str(sum(rank <= 5 for rank in pair_ranks)),
                "Threshold-retained deletions": str(threshold_counts[pair]),
                "Total deletions": str(len(rows)),
            }
        )
    return records


def _render(records: list[dict[str, str]], header: tuple[str, ...]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(header), lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return buffer.getvalue()


def render_partial_score_csv(root: str | Path) -> str:
    return _render(partial_score_records(root), PARTIAL_HEADER)


def render_association_leave_one_out_csv(root: str | Path) -> str:
    return _render(association_leave_one_out_records(root), LOTO_HEADER)


def write_robustness_csvs(root: str | Path) -> tuple[Path, Path]:
    root_path = Path(root)
    partial_path = root_path / PARTIAL_SCORE_RELATIVE
    association_path = root_path / ASSOCIATION_LOTO_RELATIVE
    partial_path.parent.mkdir(parents=True, exist_ok=True)
    partial_path.write_text(render_partial_score_csv(root_path), encoding="utf-8", newline="")
    association_path.write_text(
        render_association_leave_one_out_csv(root_path), encoding="utf-8", newline=""
    )
    return partial_path, association_path


def robustness_drift(root: str | Path) -> list[str]:
    root_path = Path(root)
    expected: tuple[tuple[str, str], ...] = (
        (PARTIAL_SCORE_RELATIVE, render_partial_score_csv(root_path)),
        (ASSOCIATION_LOTO_RELATIVE, render_association_leave_one_out_csv(root_path)),
    )
    problems: list[str] = []
    for relative, rendered in expected:
        destination = root_path / relative
        if not destination.is_file():
            problems.append(f"{relative} is missing; run `make derived`")
        elif read_text_lf(destination) != normalised_newlines(rendered):
            problems.append(f"{relative} has drifted from its source data; run `make derived`")
    return problems
