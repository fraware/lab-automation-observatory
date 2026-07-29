"""Release-level computations used by scripts and tests.

Every percentage that appears in the manuscript is computed here so that
``tests/test_published_values.py`` can assert it. Bounded proportions carry a
Wilson interval and an explicit ``successes / trials`` denominator: the interval
describes the selected cases and is not a population estimate. Component means
report how many cells were known and how many were unknown, so that an unknown
score can never be mistaken for a zero.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io import numeric, read_csv, read_csv_many
from .metrics import (
    association_from_counts,
    context_expansion_ratio,
    mean_score,
    median_ordinal,
    weighted_completeness,
    wilson_interval,
)

CODES: tuple[str, ...] = tuple(f"B{index}" for index in range(1, 11))

B2_COMPONENTS: tuple[str, ...] = (
    "Documentation",
    "API / protocol",
    "Licence clarity",
    "Simulator / isolated testing",
    "Examples / reference implementation",
    "Maintainer / support",
)
B3_COMPONENTS: tuple[str, ...] = (
    "Method / source",
    "Libraries / submethods",
    "Labware definitions",
    "Liquid classes",
    "Deck / layout",
    "Teaching / calibration",
    "Drivers / interfaces",
    "Software / firmware",
    "Checksums / IDs",
    "Runtime / initialization",
)
B4_COMPONENTS: tuple[str, ...] = (
    "Identity / part number",
    "External geometry",
    "Internal geometry",
    "Material",
    "Tolerance / variation",
    "Coordinate semantics",
    "Nesting / attachment",
    "Operating properties",
    "Provenance",
    "Device validation",
    "Independent reproduction",
)
B5_COMPONENTS: tuple[str, ...] = (
    "Run + config identity",
    "Material / resource identity",
    "Command",
    "Acknowledgment",
    "Physical observation",
    "Modeled state change",
    "Warning / failure",
    "Human intervention",
    "Recovery record",
    "Final result / disposition",
)
B8_ELEMENTS: tuple[str, ...] = (
    "Test object",
    "Environment",
    "Acceptance criterion",
    "Observed evidence",
    "Claim scope",
)
B10_SUBTYPES: tuple[str, ...] = (
    "Absence",
    "Access / restriction",
    "Discoverability",
    "Currency / version",
    "Detail / completeness",
    "Terminology / semantics",
    "Examples / templates",
    "Training / mentoring",
    "Support responsiveness",
)

METRIC_FILES: dict[str, str] = {
    "b2": "data/metrics/b2_integration_access.csv",
    "b3": "data/metrics/b3_reproducibility_manifest.csv",
    "b4": "data/metrics/b4_physical_definitions.csv",
    "b5": "data/metrics/b5_observability.csv",
    "b6": "data/metrics/b6_preflight_preventability.csv",
    "b7": "data/metrics/b7_constraint_completeness.csv",
    "b8": "data/metrics/b8_test_claim_alignment.csv",
    "b9": "data/metrics/b9_context_expansion.csv",
    "b10": "data/metrics/b10_documentation_profile.csv",
    "funnel": "data/metrics/ai_validation_funnel.csv",
    "matched": "data/metrics/b2_b10_matched_cases.csv",
}

SIMULATION_STAGE = "Simulation trace agreement"
OPENING_SCORE_COLUMN = "Opening score (0/0.5/1)"
PRESENT_AT_OPENING = {"Yes", "Partial"}


@dataclass(frozen=True)
class Proportion:
    """A bounded proportion over selected cases, with its denominator."""

    successes: int
    trials: int

    def __post_init__(self) -> None:
        if self.trials <= 0:
            raise ValueError("a bounded proportion needs a positive denominator")
        if not 0 <= self.successes <= self.trials:
            raise ValueError("successes must lie within the denominator")

    @property
    def value(self) -> float:
        return self.successes / self.trials

    @property
    def wilson(self) -> list[float]:
        return list(wilson_interval(self.successes, self.trials))

    @property
    def denominator(self) -> dict[str, int]:
        return {"successes": self.successes, "trials": self.trials}


def _cells(rows: list[dict[str, str]], columns: tuple[str, ...]) -> list[float | None]:
    return [numeric(row[column]) for row in rows for column in columns]


def _component_means(
    rows: list[dict[str, str]], columns: tuple[str, ...]
) -> dict[str, float | None]:
    """Mean per component over the cases where the component is known."""

    means: dict[str, float | None] = {}
    for column in columns:
        known = [value for value in (numeric(row[column]) for row in rows) if value is not None]
        means[column] = mean_score(known) if known else None
    return means


def _cell_denominator(
    rows: list[dict[str, str]], columns: tuple[str, ...], unit: str
) -> dict[str, int]:
    cells = _cells(rows, columns)
    known = [value for value in cells if value is not None]
    return {
        "cases": len(rows),
        f"known_{unit}": len(known),
        f"unknown_{unit}": len(cells) - len(known),
    }


def _count_scored(rows: list[dict[str, str]], columns: tuple[str, ...], target: float) -> int:
    return sum(1 for value in _cells(rows, columns) if value == target)


def component_matrices(root: str | Path) -> dict[str, dict[str, Any]]:
    """Per-case component scores for the field-level figures.

    Kept out of ``compute_release_results`` because the release JSON reports
    aggregates; the matrices are a presentation input for the heatmap.
    """

    root_path = Path(root)
    specification = (
        ("B2", "Integration accessibility", "Case", "device\u2013interface cases", B2_COMPONENTS),
        ("B3", "Deployment manifest", "Case", "deployment objects", B3_COMPONENTS),
        ("B4", "Physical definitions", "Case", "resource definitions", B4_COMPONENTS),
        ("B5", "Observability", "Case", "execution/diagnostic cases", B5_COMPONENTS),
    )
    matrices: dict[str, dict[str, Any]] = {}
    for code, label, key_column, unit, columns in specification:
        rows = read_csv(root_path / METRIC_FILES[code.lower()])
        matrices[code] = {
            "label": label,
            "unit": unit,
            "cases": [row[key_column] for row in rows],
            "components": list(columns),
            "values": [[numeric(row[column]) for column in columns] for row in rows],
        }
    return matrices


def compute_release_results(root: str | Path) -> dict[str, Any]:
    root_path = Path(root)
    evidence = read_csv_many(
        sorted((root_path / "data/derived").glob("evidence_register_part_*.csv"))
    )
    episodes = read_csv_many(
        sorted((root_path / "data/derived").glob("episode_register_part_*.csv"))
    )
    adjudication = read_csv(root_path / "data/derived/reliability_subset.csv")

    code_counts = {code: sum(int(row[code]) for row in evidence) for code in CODES}
    primary_counts = Counter(row["Primary"] for row in evidence)
    episode_threads = {row["Thread ID"] for row in episodes}

    b2 = read_csv(root_path / METRIC_FILES["b2"])
    mean_ias = mean_score(numeric(row["IAS"]) for row in b2)

    b3 = read_csv(root_path / METRIC_FILES["b3"])
    mean_rmc = mean_score(numeric(row["RMC"]) for row in b3)
    b3_applicable = len([value for value in _cells(b3, B3_COMPONENTS) if value is not None])
    b3_fully_bound = Proportion(_count_scored(b3, B3_COMPONENTS, 1.0), b3_applicable)
    b3_partial = Proportion(_count_scored(b3, B3_COMPONENTS, 0.5), b3_applicable)

    b4 = read_csv(root_path / METRIC_FILES["b4"])
    mean_pdc = mean_score(numeric(row["PDC"]) for row in b4)
    median_evidence_grade = median_ordinal(numeric(row["Evidence grade"]) for row in b4)

    b5 = read_csv(root_path / METRIC_FILES["b5"])
    mean_oc = mean_score(numeric(row["OC"]) for row in b5)

    b6 = read_csv(root_path / METRIC_FILES["b6"])
    detectability = Counter(row["Preflight detectability"] for row in b6)
    ppr = Proportion(detectability["Yes"], detectability["Yes"] + detectability["No"])
    ppr_lower = detectability["Yes"] / len(b6)
    ppr_upper = (detectability["Yes"] + detectability["Indeterminate"]) / len(b6)

    b7 = read_csv(root_path / METRIC_FILES["b7"])
    opening_scores = [float(row[OPENING_SCORE_COLUMN]) for row in b7]
    incomplete = [row for row in b7 if float(row[OPENING_SCORE_COLUMN]) < 1]
    if not incomplete:
        raise ValueError(
            f"{METRIC_FILES['b7']} has no field scoring below 1 at opening, so the "
            "constraint discovery and resolution rates have no denominator"
        )
    strict_completeness = Proportion(sum(score == 1 for score in opening_scores), len(b7))
    field_coverage = Proportion(
        sum(row["Present at opening?"] in PRESENT_AT_OPENING for row in b7), len(b7)
    )
    discovery = Proportion(
        sum(row["Identified in discussion?"] == "Yes" for row in incomplete), len(incomplete)
    )
    resolution = Proportion(
        sum(row["Resolved with scenario-specific value?"] == "Yes" for row in incomplete),
        len(incomplete),
    )

    b8 = read_csv(root_path / METRIC_FILES["b8"])
    element_mean = mean_score(numeric(row["Element mean"]) for row in b8)
    aligned = Proportion(sum(row["Alignment class"] == "Aligned" for row in b8), len(b8))
    partial_or_better = Proportion(
        sum(row["Alignment class"] in {"Aligned", "Partial"} for row in b8), len(b8)
    )

    b9 = read_csv(root_path / METRIC_FILES["b9"])
    initial = sum(row["Origin"] == "Initial" for row in b9)
    core_added = sum(
        row["Origin"] == "Reply-added" and row["Core execution scope?"] == "Yes" for row in b9
    )
    broad_added = sum(
        row["Origin"] == "Reply-added" and row["Broader deployment scope?"] == "Yes" for row in b9
    )
    conservative_added = sum(
        row["Origin"] == "Reply-added" and row["Counted in conservative grouping?"] == "Yes"
        for row in b9
    )

    b10 = read_csv(root_path / METRIC_FILES["b10"])
    actionable = Proportion(
        sum(row["Actionable public resolution"] == "Yes" for row in b10), len(b10)
    )
    public_partial_or_better = Proportion(
        sum(row["Actionable public resolution"] in {"Yes", "Partial"} for row in b10), len(b10)
    )
    private_migration = Proportion(
        sum(row["Private migration"] in {"Yes", "Partial"} for row in b10), len(b10)
    )

    pairwise = read_csv(root_path / "data/metrics/pairwise_associations.csv")
    top_pair = max(pairwise, key=lambda row: float(row["Phi"]))
    top_counts = (
        int(float(top_pair["Overlap"])),
        int(float(top_pair["N(A)"])) - int(float(top_pair["Overlap"])),
        int(float(top_pair["N(B)"])) - int(float(top_pair["Overlap"])),
        len(evidence)
        - int(float(top_pair["N(A)"]))
        - int(float(top_pair["N(B)"]))
        + int(float(top_pair["Overlap"])),
    )
    recomputed_top = association_from_counts(*top_counts)

    ai_funnel = read_csv(root_path / METRIC_FILES["funnel"])
    simulation_row = next(row for row in ai_funnel if row["Stage"] == SIMULATION_STAGE)
    simulation = Proportion(
        int(float(simulation_row["Numerator"])), int(float(simulation_row["Denominator"]))
    )

    proportions: dict[str, Proportion] = {
        "preflight_preventability_complete_case": ppr,
        "reproducibility_manifest_fully_bound_cell_share": b3_fully_bound,
        "reproducibility_manifest_partial_cell_share": b3_partial,
        "scheduling_strict_completeness": strict_completeness,
        "scheduling_field_coverage": field_coverage,
        "scheduling_constraint_discovery": discovery,
        "scheduling_scenario_resolution": resolution,
        "test_claim_aligned": aligned,
        "test_claim_partial_or_better": partial_or_better,
        "documentation_actionable_public_resolution": actionable,
        "documentation_partial_or_better": public_partial_or_better,
        "documentation_private_migration": private_migration,
        "verisflow_simulation_trace_rate": simulation,
    }

    metrics: dict[str, Any] = {
        "integration_accessibility_mean": mean_ias,
        "integration_accessibility_cases_at_least_75": sum(
            1 for row in b2 if (numeric(row["IAS"]) or 0.0) >= 0.75
        ),
        "integration_accessibility_positive_cases": sum(
            1 for row in b2 if row["Positive case"] == "Yes"
        ),
        "reproducibility_manifest_mean": mean_rmc,
        "physical_definition_mean": mean_pdc,
        "physical_definition_median_evidence_grade": median_evidence_grade,
        "physical_definition_device_validated_cases": sum(
            1 for row in b4 if numeric(row["Device validation"]) == 1
        ),
        "physical_definition_independently_reproduced_cases": sum(
            1 for row in b4 if numeric(row["Independent reproduction"]) == 1
        ),
        "observability_mean": mean_oc,
        "observability_first_divergence_localized_cases": sum(
            1 for row in b5 if row["First divergence localized?"].startswith("Yes")
        ),
        "preflight_preventability_sensitivity": [ppr_lower, ppr_upper],
        "scheduling_opening_weighted_completeness": weighted_completeness(opening_scores),
        "scheduling_discovery_resolution_gap_pp": 100 * (discovery.value - resolution.value),
        "test_claim_element_mean": element_mean,
        "context_expansion_core": context_expansion_ratio(initial, core_added),
        "context_expansion_broad": context_expansion_ratio(initial, broad_added),
        "context_expansion_conservative": context_expansion_ratio(initial, conservative_added),
    }
    for name, proportion in proportions.items():
        metrics[name] = proportion.value
        metrics[f"{name}_wilson"] = proportion.wilson

    denominators: dict[str, Any] = {
        name: proportion.denominator for name, proportion in proportions.items()
    }
    denominators["preflight_preventability_sensitivity"] = {
        "definite": ppr.trials,
        "indeterminate": detectability["Indeterminate"],
        "eligible_scenarios": len(b6),
    }
    denominators["integration_accessibility_mean"] = _cell_denominator(
        b2, B2_COMPONENTS, "components"
    )
    denominators["reproducibility_manifest_mean"] = _cell_denominator(b3, B3_COMPONENTS, "cells")
    denominators["physical_definition_mean"] = _cell_denominator(b4, B4_COMPONENTS, "components")
    denominators["observability_mean"] = _cell_denominator(b5, B5_COMPONENTS, "components")
    denominators["test_claim_element_mean"] = _cell_denominator(b8, B8_ELEMENTS, "elements")
    denominators["scheduling_opening_weighted_completeness"] = {"requirement_fields": len(b7)}
    denominators["context_expansion_core"] = {
        "initial_classes": initial,
        "added_classes": core_added,
    }
    denominators["context_expansion_broad"] = {
        "initial_classes": initial,
        "added_classes": broad_added,
    }
    denominators["context_expansion_conservative"] = {
        "initial_classes": initial,
        "added_classes": conservative_added,
    }

    return {
        "corpus": {
            "threads": len(evidence),
            "episodes": len(episodes),
            "episode_threads": len(episode_threads),
            "adjudication_threads": len({row["Thread ID"] for row in adjudication}),
            "constructs": len(code_counts),
            "direct_support_counts": code_counts,
            "primary_counts": dict(sorted(primary_counts.items())),
        },
        "metrics": metrics,
        "components": {
            "integration_accessibility": _component_means(b2, B2_COMPONENTS),
            "reproducibility_manifest": _component_means(b3, B3_COMPONENTS),
            "physical_definition": _component_means(b4, B4_COMPONENTS),
            "observability": _component_means(b5, B5_COMPONENTS),
            "test_claim_alignment": _component_means(b8, B8_ELEMENTS),
            "documentation_profile": _component_means(b10, B10_SUBTYPES),
        },
        "denominators": denominators,
        "strongest_association": {
            "pair": [top_pair["Code A"], top_pair["Code B"]],
            **recomputed_top.to_dict(),
        },
    }
