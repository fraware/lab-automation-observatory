from __future__ import annotations

from pathlib import Path

import pytest

from labauto_observatory.robustness import (
    association_leave_one_out_records,
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
    return {
        (row["Code A"], row["Code B"]): row for row in association_leave_one_out_records(ROOT)
    }


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


def test_robustness_outputs_have_no_drift() -> None:
    assert robustness_drift(ROOT) == []
