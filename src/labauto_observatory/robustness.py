"""Deterministic robustness analyses for publication-critical results.

The analyses in this module are descriptive stress tests over the purposively
selected release data. They do not create population estimates or inferential
p-values. Their purpose is to expose dependence on a conventional partial-score
weight, any single selected thread, and defensible alternative denominators.
"""

from __future__ import annotations

import csv
import io
from collections import Counter
from itertools import combinations
from pathlib import Path

from .analysis import (
    B2_COMPONENTS,
    B3_COMPONENTS,
    B4_COMPONENTS,
    B5_COMPONENTS,
    METRIC_FILES,
    OPENING_SCORE_COLUMN,
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
from .metrics import association_from_counts, context_expansion_ratio, mean_score

PARTIAL_WEIGHTS: tuple[float, ...] = (0.0, 0.25, 0.5, 0.75, 1.0)
PARTIAL_SCORE_RELATIVE = "data/robustness/partial_score_sensitivity.csv"
ASSOCIATION_LOTO_RELATIVE = "data/robustness/association_leave_one_out.csv"
DENOMINATOR_RELATIVE = "data/robustness/denominator_sensitivity.csv"

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

DENOMINATOR_HEADER: tuple[str, ...] = (
    "Metric",
    "Variant",
    "Included units",
    "Numerator",
    "Denominator",
    "Estimate",
    "Secondary result",
    "Scope decision",
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
        rank_map = {(code_a, code_b): rank for rank, (code_a, code_b, _, _) in enumerate(ranked, 1)}
        value_map = {(code_a, code_b): (phi, lift) for code_a, code_b, phi, lift in ranked}
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


def _b6_record(rows: list[dict[str, str]], variant: str, scope: str) -> dict[str, str]:
    classes = Counter(row["Preflight detectability"] for row in rows)
    definite = classes["Yes"] + classes["No"]
    estimate = classes["Yes"] / definite
    lower = classes["Yes"] / len(rows)
    upper = (classes["Yes"] + classes["Indeterminate"]) / len(rows)
    return {
        "Metric": "B6 preflight preventability",
        "Variant": variant,
        "Included units": str(len(rows)),
        "Numerator": str(classes["Yes"]),
        "Denominator": str(definite),
        "Estimate": format_number(estimate),
        "Secondary result": f"sensitivity={format_number(lower)}--{format_number(upper)}",
        "Scope decision": scope,
    }


def _b7_record(rows: list[dict[str, str]], variant: str, scope: str) -> dict[str, str]:
    scores = [float(row[OPENING_SCORE_COLUMN]) for row in rows]
    incomplete = [row for row in rows if float(row[OPENING_SCORE_COLUMN]) < 1]
    discovered = sum(row["Identified in discussion?"] == "Yes" for row in incomplete)
    resolved = sum(row["Resolved with scenario-specific value?"] == "Yes" for row in incomplete)
    strict = sum(score == 1 for score in scores)
    covered = sum(score > 0 for score in scores)
    return {
        "Metric": "B7 constraint completeness",
        "Variant": variant,
        "Included units": str(len(rows)),
        "Numerator": format_number(sum(scores)),
        "Denominator": str(len(rows)),
        "Estimate": format_number(sum(scores) / len(rows)),
        "Secondary result": (
            f"strict={strict}/{len(rows)}; coverage={covered}/{len(rows)}; "
            f"discovery={discovered}/{len(incomplete)}; resolution={resolved}/{len(incomplete)}"
        ),
        "Scope decision": scope,
    }


def _b8_record(rows: list[dict[str, str]], variant: str, scope: str) -> dict[str, str]:
    aligned = sum(row["Alignment class"] == "Aligned" for row in rows)
    partial_or_better = sum(row["Alignment class"] in {"Aligned", "Partial"} for row in rows)
    return {
        "Metric": "B8 test--claim alignment",
        "Variant": variant,
        "Included units": str(len(rows)),
        "Numerator": str(aligned),
        "Denominator": str(len(rows)),
        "Estimate": format_number(aligned / len(rows)),
        "Secondary result": f"partial-or-better={partial_or_better}/{len(rows)}",
        "Scope decision": scope,
    }


def _b9_records(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    initial = sum(row["Origin"] == "Initial" for row in rows)
    variants = (
        (
            "core execution ontology",
            sum(
                row["Origin"] == "Reply-added" and row["Core execution scope?"] == "Yes"
                for row in rows
            ),
            "Counts reply-added context classes required for execution reasoning.",
        ),
        (
            "broad deployment ontology",
            sum(
                row["Origin"] == "Reply-added" and row["Broader deployment scope?"] == "Yes"
                for row in rows
            ),
            "Counts all reply-added execution and deployment context classes.",
        ),
        (
            "conservative grouped ontology",
            sum(
                row["Origin"] == "Reply-added" and row["Counted in conservative grouping?"] == "Yes"
                for row in rows
            ),
            "Merges related concepts to reduce dependence on coding granularity.",
        ),
    )
    return [
        {
            "Metric": "B9 context expansion",
            "Variant": label,
            "Included units": str(initial + added),
            "Numerator": str(added),
            "Denominator": str(initial),
            "Estimate": format_number(context_expansion_ratio(initial, added)),
            "Secondary result": f"initial={initial}; reply-added={added}",
            "Scope decision": scope,
        }
        for label, added, scope in variants
    ]


def _b10_record(rows: list[dict[str, str]], variant: str, scope: str) -> dict[str, str]:
    actionable = sum(row["Actionable public resolution"] == "Yes" for row in rows)
    partial_or_better = sum(
        row["Actionable public resolution"] in {"Yes", "Partial"} for row in rows
    )
    migrated = sum(row["Private migration"] in {"Yes", "Partial"} for row in rows)
    return {
        "Metric": "B10 documentation outcome",
        "Variant": variant,
        "Included units": str(len(rows)),
        "Numerator": str(actionable),
        "Denominator": str(len(rows)),
        "Estimate": format_number(actionable / len(rows)),
        "Secondary result": (
            f"partial-or-better={partial_or_better}/{len(rows)}; migrated={migrated}/{len(rows)}"
        ),
        "Scope decision": scope,
    }


def denominator_sensitivity_records(root: str | Path) -> list[dict[str, str]]:
    """Summarize primary and adversarial denominator definitions for B6--B10."""

    root_path = Path(root)
    b6 = read_csv(root_path / METRIC_FILES["b6"])
    b7 = read_csv(root_path / METRIC_FILES["b7"])
    b8 = read_csv(root_path / METRIC_FILES["b8"])
    b9 = read_csv(root_path / METRIC_FILES["b9"])
    b10 = read_csv(root_path / METRIC_FILES["b10"])

    records = [
        _b6_record(
            b6,
            "all discussed partial-execution scenarios",
            "Primary scope; includes one explicitly discussed hardware-crash scenario and reports scenarios, not incident prevalence.",
        ),
        _b6_record(
            [row for row in b6 if row["Failure class"] != "Hardware failure"],
            "reported or deliberately triggered software scenarios",
            "Adversarial subset excluding the general hardware-crash scenario.",
        ),
        _b7_record(
            b7,
            "operationally complete scheduler evaluation",
            "Primary scope; includes failure and recovery policy as an operational scheduler requirement.",
        ),
        _b7_record(
            [row for row in b7 if row["Requirement field"] != "Failure and recovery policy"],
            "nominal scheduling core",
            "Adversarial subset for evaluating a static nominal schedule without resilience behavior.",
        ),
        _b8_record(
            b8,
            "all bounded evaluation objects",
            "Primary scope; retains the unexecuted proposed experiment as an incomplete test--claim object.",
        ),
        _b8_record(
            [row for row in b8 if float(row["Observed evidence"]) > 0],
            "executed-evidence subset",
            "Adversarial subset excluding the prospective experiment with no observed evidence.",
        ),
    ]
    records.extend(_b9_records(b9))
    records.extend(
        [
            _b10_record(
                b10,
                "all documentation-centered cases",
                "Primary scope; retains censored cases and reports private migration separately.",
            ),
            _b10_record(
                [row for row in b10 if row["Private migration"] == "No"],
                "non-migrated public cases",
                "Adversarial subset; not preferred because excluding migrated cases can select on outcome visibility.",
            ),
        ]
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


def render_denominator_sensitivity_csv(root: str | Path) -> str:
    return _render(denominator_sensitivity_records(root), DENOMINATOR_HEADER)


def write_robustness_csvs(root: str | Path) -> tuple[Path, Path, Path]:
    root_path = Path(root)
    outputs = (
        (PARTIAL_SCORE_RELATIVE, render_partial_score_csv(root_path)),
        (ASSOCIATION_LOTO_RELATIVE, render_association_leave_one_out_csv(root_path)),
        (DENOMINATOR_RELATIVE, render_denominator_sensitivity_csv(root_path)),
    )
    paths: list[Path] = []
    for relative, rendered in outputs:
        destination = root_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8", newline="")
        paths.append(destination)
    return paths[0], paths[1], paths[2]


def robustness_drift(root: str | Path) -> list[str]:
    root_path = Path(root)
    expected: tuple[tuple[str, str], ...] = (
        (PARTIAL_SCORE_RELATIVE, render_partial_score_csv(root_path)),
        (ASSOCIATION_LOTO_RELATIVE, render_association_leave_one_out_csv(root_path)),
        (DENOMINATOR_RELATIVE, render_denominator_sensitivity_csv(root_path)),
    )
    problems: list[str] = []
    for relative, rendered in expected:
        destination = root_path / relative
        if not destination.is_file():
            problems.append(f"{relative} is missing; run `make derived`")
        elif read_text_lf(destination) != normalised_newlines(rendered):
            problems.append(f"{relative} has drifted from its source data; run `make derived`")
    return problems
