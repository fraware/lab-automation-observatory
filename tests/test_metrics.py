from __future__ import annotations

import pytest

from labauto_observatory.analysis import Proportion
from labauto_observatory.metrics import (
    association_from_counts,
    context_expansion_ratio,
    mean_score,
    median_ordinal,
    phi_coefficient,
    phi_with_shifted_overlap,
    weighted_completeness,
    wilson_interval,
)


def test_phi_matches_observability_recovery_pair() -> None:
    assert phi_coefficient(8, 9, 3, 35) == pytest.approx(0.4524614483)


def test_association_measures() -> None:
    association = association_from_counts(8, 9, 3, 35)
    assert association.jaccard == pytest.approx(0.4)
    assert association.lift == pytest.approx(2.3529411765)
    assert association.descriptive_risk_ratio == pytest.approx(5.9607843137)


def test_wilson_intervals() -> None:
    assert wilson_interval(92, 100) == pytest.approx((0.8500173312, 0.9589070305))
    assert wilson_interval(2, 3) == pytest.approx((0.2076549551, 0.9385096847))


def test_score_helpers_preserve_unknown() -> None:
    assert mean_score([1, 0.5, None, 0]) == pytest.approx(0.5)
    assert weighted_completeness([1, 1, 0.5, 0]) == pytest.approx(0.625)
    assert context_expansion_ratio(5, 10) == 2.0


def test_invalid_inputs_fail_closed() -> None:
    with pytest.raises(ValueError):
        wilson_interval(3, 2)
    with pytest.raises(ValueError):
        context_expansion_ratio(0, 3)
    with pytest.raises(ValueError):
        weighted_completeness([0.25])
    with pytest.raises(ValueError, match="at least one score"):
        weighted_completeness([])
    with pytest.raises(ValueError, match="at least one known score"):
        mean_score([None, None])
    with pytest.raises(ValueError, match="at least one known grade"):
        median_ordinal([None])


def test_median_ordinal_ignores_unknown_grades() -> None:
    """An unknown evidence grade must not be read as the lowest grade."""

    assert median_ordinal([4, None, 1, 3]) == pytest.approx(3.0)
    assert median_ordinal([2, 3]) == pytest.approx(2.5)


def test_phi_sensitivity_moves_one_thread_through_the_overlap_cell() -> None:
    base = phi_coefficient(8, 9, 3, 35)
    lower = phi_with_shifted_overlap(8, 9, 3, 35, -1)
    upper = phi_with_shifted_overlap(8, 9, 3, 35, 1)
    assert lower is not None and upper is not None
    assert lower < base < upper


def test_phi_sensitivity_is_undefined_when_a_margin_would_empty() -> None:
    """Shifting the overlap past a margin has no two-by-two table to describe."""

    assert phi_with_shifted_overlap(0, 0, 3, 35, -1) is None
    assert phi_with_shifted_overlap(3, 0, 0, 35, 1) is None


def test_proportion_requires_a_denominator_it_can_report() -> None:
    with pytest.raises(ValueError, match="positive denominator"):
        Proportion(0, 0)
    with pytest.raises(ValueError, match="within the denominator"):
        Proportion(4, 3)
    bounded = Proportion(2, 3)
    assert bounded.value == pytest.approx(2 / 3)
    assert bounded.denominator == {"successes": 2, "trials": 3}
    assert bounded.wilson == pytest.approx([0.2076549551, 0.9385096847])
