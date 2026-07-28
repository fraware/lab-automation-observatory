"""Lab Automation Forum Bottleneck Observatory analysis library."""

from .metrics import (
    Association,
    association_from_counts,
    context_expansion_ratio,
    mean_score,
    phi_coefficient,
    weighted_completeness,
    wilson_interval,
)
from .traceability import TraceabilityReport, check_traceability

__all__ = [
    "Association",
    "TraceabilityReport",
    "association_from_counts",
    "check_traceability",
    "context_expansion_ratio",
    "mean_score",
    "phi_coefficient",
    "weighted_completeness",
    "wilson_interval",
]

__version__ = "0.1.0"
