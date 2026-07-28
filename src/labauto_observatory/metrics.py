"""Bounded metrics used by the Observatory paper."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass
from math import sqrt
from statistics import fmean


@dataclass(frozen=True)
class Association:
    """Association measures for a two-by-two table."""

    n11: int
    n10: int
    n01: int
    n00: int
    jaccard: float
    lift: float
    phi: float
    p_b_given_a: float
    p_b_given_not_a: float
    descriptive_risk_ratio: float | None

    def to_dict(self) -> dict[str, int | float | None]:
        return asdict(self)


def _require_nonnegative(*values: int) -> None:
    if any(value < 0 for value in values):
        raise ValueError("counts must be nonnegative")


def phi_coefficient(n11: int, n10: int, n01: int, n00: int) -> float:
    """Compute the phi coefficient for a two-by-two table."""

    _require_nonnegative(n11, n10, n01, n00)
    denominator = sqrt((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00))
    if denominator == 0:
        return 0.0
    return (n11 * n00 - n10 * n01) / denominator


def association_from_counts(n11: int, n10: int, n01: int, n00: int) -> Association:
    """Compute the paper's descriptive association measures."""

    _require_nonnegative(n11, n10, n01, n00)
    total = n11 + n10 + n01 + n00
    if total == 0:
        raise ValueError("association table must contain at least one observation")

    n_a = n11 + n10
    n_b = n11 + n01
    union = n11 + n10 + n01
    jaccard = n11 / union if union else 0.0
    lift = (n11 * total / (n_a * n_b)) if n_a and n_b else 0.0
    p_b_given_a = n11 / n_a if n_a else 0.0
    not_a = n01 + n00
    p_b_given_not_a = n01 / not_a if not_a else 0.0
    risk_ratio = p_b_given_a / p_b_given_not_a if p_b_given_not_a else None

    return Association(
        n11=n11,
        n10=n10,
        n01=n01,
        n00=n00,
        jaccard=jaccard,
        lift=lift,
        phi=phi_coefficient(n11, n10, n01, n00),
        p_b_given_a=p_b_given_a,
        p_b_given_not_a=p_b_given_not_a,
        descriptive_risk_ratio=risk_ratio,
    )


def wilson_interval(successes: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    """Return a two-sided Wilson score interval for a binomial proportion."""

    _require_nonnegative(successes, trials)
    if trials == 0:
        raise ValueError("trials must be positive")
    if successes > trials:
        raise ValueError("successes cannot exceed trials")

    p_hat = successes / trials
    denominator = 1 + z**2 / trials
    centre = (p_hat + z**2 / (2 * trials)) / denominator
    margin = z * sqrt(p_hat * (1 - p_hat) / trials + z**2 / (4 * trials**2)) / denominator
    return max(0.0, centre - margin), min(1.0, centre + margin)


def mean_score(values: Iterable[float | None]) -> float:
    """Mean over known scores while retaining unknown separately from zero."""

    known = [float(value) for value in values if value is not None]
    if not known:
        raise ValueError("at least one known score is required")
    if any(value < 0 or value > 1 for value in known):
        raise ValueError("scores must lie in [0, 1]")
    return fmean(known)


def context_expansion_ratio(initial_classes: int, added_classes: int) -> float:
    """Compute reply-added context classes divided by opening classes."""

    _require_nonnegative(initial_classes, added_classes)
    if initial_classes == 0:
        raise ValueError("initial_classes must be positive")
    return added_classes / initial_classes


def weighted_completeness(scores: Iterable[float]) -> float:
    """Compute mean completeness from 0, 0.5, and 1 item scores."""

    values = [float(value) for value in scores]
    if not values:
        raise ValueError("at least one score is required")
    if any(value not in {0.0, 0.5, 1.0} for value in values):
        raise ValueError("weighted completeness accepts only 0, 0.5, and 1")
    return fmean(values)
