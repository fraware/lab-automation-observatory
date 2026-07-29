"""Lab Automation Forum Bottleneck Observatory analysis library."""

from importlib.metadata import version as _distribution_version

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

# Read from the installed distribution rather than repeated as a literal. The
# literal that stood here was still "0.1.0" three patch releases after it was
# written, because nothing compared it to `pyproject.toml`.
__version__ = _distribution_version("labauto-observatory")
