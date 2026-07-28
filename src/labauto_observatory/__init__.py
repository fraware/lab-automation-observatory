"""Lab Automation Forum Bottleneck Observatory analysis library."""

from .metrics import (
    Association,
    association_from_counts,
    context_expansion_ratio,
    mean_score,
    phi_coefficient,
    wilson_interval,
)

__all__ = [
    "Association",
    "association_from_counts",
    "context_expansion_ratio",
    "mean_score",
    "phi_coefficient",
    "wilson_interval",
]

__version__ = "0.1.0"
