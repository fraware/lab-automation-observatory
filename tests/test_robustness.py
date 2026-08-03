from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from labauto_observatory.robustness import (
    ASSOCIATION_LOTO_RELATIVE,
    DENOMINATOR_RELATIVE,
    PARTIAL_SCORE_RELATIVE,
    association_leave_one_out_records,
    denominator_sensitivity_records,
    partial_score_records,
    robustness_drift,
)

ROOT = Path(__file__).resolve().parents[1]


def _partial_lookup() -> dict[tuple[str, float], float]:
    return {
        (row["Metric"], float(row["Partial weight"])): float(row["Mean"])
        for row in partial_score_records(ROOT)
    }


def _association_lookup() -> dict[tuple[str, str], dict[str, str]]:
    return {(row["Code A"], row["Code B"]): row for row in association_leave_one_out_records(ROOT)}


def _denominator_lookup() -> dict[tuple[str, str], dict[str, str]]:
    return {(row["Metric"], row["Variant"]): row for row in denominator_sensitivity_records(ROOT)}


def test_partial_score_sensitivity_values() -> None:
    values = _partial_lookup()
    assert [values[("IAS", weight)] for weight in (0, 0.25, 0.5, 0.75, 1)] == pytest.approx(
        [0.3888888889, 0.5138888889, 0.6388888889, 0.7638888889, 0.8888888889]
    )
    assert [values[("RMC", weight)] for weight in (0, 0.25, 0.5, 0.75, 1)] == pytest.approx(
        [0.2166666667, 0.3791666667, 0.5416666667, 0.7041666667, 0.8666666667]
    )
    assert [values[("PDC", weight)] for weight in (0, 0.25, 0.5, 0.75, 1)] == pytest.approx(
        [0.5, 0.5852272727, 0.6704545455, 0.7556818182, 0.8409090909]
    )
    assert [values[("OC", weight)] for weight in (0, 0.25, 0.5, 0.75, 1)] == pytest.approx(
        [0.25, 0.3875, 0.525, 0.6625, 0.8]
    )


def test_partial_score_sensitivity_is_monotone() -> None:
    values = _partial_lookup()
    for metric in ("IAS", "RMC", "PDC", "OC"):
        sequence = [values[(metric, weight)] for weight in (0, 0.25, 0.5, 0.75, 1)]
        assert sequence == sorted(sequence)


def test_leave_one_out_leading_pairs() -> None:
    rows = _association_lookup()
    expected = {
        ("B5", "B6"): (0.4524614483, 0.4214813532, 0.4980232641, 1, 2, 55, 55),
        ("B5", "B8"): (0.4242333422, 0.4014775343, 0.4560740746, 1, 3, 55, 55),
        ("B2", "B7"): (0.3821079319, 0.3501688212, 0.4226664577, 2, 3, 55, 55),
        ("B4", "B8"): (0.3158151333, 0.2834733548, 0.3523741786, 4, 5, 55, 47),
        ("B8", "B9"): (0.3022817709, 0.25, 0.3838859480, 4, 6, 53, 16),
    }
    for pair, (full, low, high, rank_low, rank_high, top_five, threshold) in expected.items():
        row = rows[pair]
        assert float(row["Full phi"]) == pytest.approx(full)
        assert float(row["Minimum phi"]) == pytest.approx(low)
        assert float(row["Maximum phi"]) == pytest.approx(high)
        assert int(row["Minimum rank"]) == rank_low
        assert int(row["Maximum rank"]) == rank_high
        assert int(row["Top-five deletions"]) == top_five
        assert int(row["Threshold-retained deletions"]) == threshold
        assert int(row["Total deletions"]) == 55


def test_adversarial_denominator_results() -> None:
    rows = _denominator_lookup()
    expected = {
        ("B6 preflight preventability", "all discussed partial-execution scenarios"): 2 / 3,
        (
            "B6 preflight preventability",
            "reported or deliberately triggered software scenarios",
        ): 1.0,
        ("B7 constraint completeness", "operationally complete scheduler evaluation"): 7 / 13,
        ("B7 constraint completeness", "nominal scheduling core"): 7 / 12,
        ("B8 test--claim alignment", "all bounded evaluation objects"): 2 / 6,
        ("B8 test--claim alignment", "executed-evidence subset"): 2 / 5,
        ("B9 context expansion", "core execution ontology"): 2.0,
        ("B9 context expansion", "broad deployment ontology"): 3.4,
        ("B9 context expansion", "conservative grouped ontology"): 2.2,
        ("B10 documentation outcome", "all documentation-centered cases"): 5 / 12,
        ("B10 documentation outcome", "non-migrated public cases"): 5 / 9,
    }
    for key, value in expected.items():
        assert float(rows[key]["Estimate"]) == pytest.approx(value)


def test_robustness_outputs_have_no_drift() -> None:
    assert robustness_drift(ROOT) == []


def test_component_mutation_invalidates_partial_score_output(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / "data/metrics/b2_integration_access.csv", 0, Documentation="0")
    problems = robustness_drift(data_root)
    assert (
        f"{PARTIAL_SCORE_RELATIVE} has drifted from its source data; run `make derived`" in problems
    )


def test_register_mutation_invalidates_association_influence_output(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / "data/derived/evidence_register_part_01.csv", 0, B2="1")
    problems = robustness_drift(data_root)
    assert (
        f"{ASSOCIATION_LOTO_RELATIVE} has drifted from its source data; run `make derived`"
        in problems
    )


def test_metric_mutation_invalidates_denominator_sensitivity_output(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    """Flipping a B6 failure class must invalidate the denominator sensitivity CSV."""

    edit_csv(
        data_root / "data/metrics/b6_preflight_preventability.csv",
        0,
        **{"Failure class": "Hardware failure"},
    )
    problems = robustness_drift(data_root)
    assert (
        f"{DENOMINATOR_RELATIVE} has drifted from its source data; run `make derived`" in problems
    )
