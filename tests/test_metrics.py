from __future__ import annotations

import pytest

from labauto_observatory.metrics import (
    association_from_counts,
    context_expansion_ratio,
    mean_score,
    phi_coefficient,
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
