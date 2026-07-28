"""Release-level computations used by scripts and tests."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .io import numeric, read_csv, read_csv_many
from .metrics import (
    association_from_counts,
    context_expansion_ratio,
    mean_score,
    weighted_completeness,
    wilson_interval,
)


def compute_release_results(root: str | Path) -> dict[str, Any]:
    root_path = Path(root)
    evidence = read_csv_many(
        sorted((root_path / "data/derived").glob("evidence_register_part_*.csv"))
    )
    episodes = read_csv_many(
        sorted((root_path / "data/derived").glob("episode_register_part_*.csv"))
    )
    adjudication = read_csv(root_path / "data/derived/reliability_subset.csv")

    code_counts = {f"B{i}": sum(int(row[f"B{i}"]) for row in evidence) for i in range(1, 11)}
    primary_counts = Counter(row["Primary"] for row in evidence)
    episode_threads = {row["Thread ID"] for row in episodes}

    b2 = read_csv(root_path / "data/metrics/b2_integration_access.csv")
    mean_ias = mean_score(numeric(row["IAS"]) for row in b2)

    b3 = read_csv(root_path / "data/metrics/b3_reproducibility_manifest.csv")
    mean_rmc = mean_score(numeric(row["RMC"]) for row in b3)

    b4 = read_csv(root_path / "data/metrics/b4_physical_definitions.csv")
    mean_pdc = mean_score(numeric(row["PDC"]) for row in b4)

    b5 = read_csv(root_path / "data/metrics/b5_observability.csv")
    mean_oc = mean_score(numeric(row["OC"]) for row in b5)

    b6 = read_csv(root_path / "data/metrics/b6_preflight_preventability.csv")
    detectability = Counter(row["Preflight detectability"] for row in b6)
    complete_case_ppr = detectability["Yes"] / (detectability["Yes"] + detectability["No"])
    ppr_lower = detectability["Yes"] / len(b6)
    ppr_upper = (detectability["Yes"] + detectability["Indeterminate"]) / len(b6)
    ppr_wilson = wilson_interval(detectability["Yes"], detectability["Yes"] + detectability["No"])

    b7 = read_csv(root_path / "data/metrics/b7_constraint_completeness.csv")
    opening_scores = [float(row["Opening score (0/0.5/1)"]) for row in b7]
    incomplete = [row for row in b7 if float(row["Opening score (0/0.5/1)"]) < 1]
    constraint_discovery = sum(
        row["Identified in discussion?"] == "Yes" for row in incomplete
    ) / len(incomplete)
    constraint_resolution = sum(
        row["Resolved with scenario-specific value?"] == "Yes" for row in incomplete
    ) / len(incomplete)

    b8 = read_csv(root_path / "data/metrics/b8_test_claim_alignment.csv")
    aligned_rate = sum(row["Alignment class"] == "Aligned" for row in b8) / len(b8)
    partial_or_better = sum(row["Alignment class"] in {"Aligned", "Partial"} for row in b8) / len(
        b8
    )

    b9 = read_csv(root_path / "data/metrics/b9_context_expansion.csv")
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

    b10 = read_csv(root_path / "data/metrics/b10_documentation_profile.csv")
    actionable = sum(row["Actionable public resolution"] == "Yes" for row in b10) / len(b10)
    partial_public = sum(
        row["Actionable public resolution"] in {"Yes", "Partial"} for row in b10
    ) / len(b10)
    private_migration = sum(row["Private migration"] in {"Yes", "Partial"} for row in b10) / len(
        b10
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

    ai_funnel = read_csv(root_path / "data/metrics/ai_validation_funnel.csv")
    simulation_row = next(row for row in ai_funnel if row["Stage"] == "Simulation trace agreement")
    sim_successes = int(float(simulation_row["Numerator"]))
    sim_trials = int(float(simulation_row["Denominator"]))
    sim_wilson = wilson_interval(sim_successes, sim_trials)

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
        "metrics": {
            "integration_accessibility_mean": mean_ias,
            "reproducibility_manifest_mean": mean_rmc,
            "physical_definition_mean": mean_pdc,
            "observability_mean": mean_oc,
            "preflight_preventability_complete_case": complete_case_ppr,
            "preflight_preventability_sensitivity": [ppr_lower, ppr_upper],
            "preflight_preventability_wilson": list(ppr_wilson),
            "scheduling_opening_weighted_completeness": weighted_completeness(opening_scores),
            "scheduling_constraint_discovery": constraint_discovery,
            "scheduling_scenario_resolution": constraint_resolution,
            "test_claim_aligned": aligned_rate,
            "test_claim_partial_or_better": partial_or_better,
            "context_expansion_core": context_expansion_ratio(initial, core_added),
            "context_expansion_broad": context_expansion_ratio(initial, broad_added),
            "context_expansion_conservative": context_expansion_ratio(initial, conservative_added),
            "documentation_actionable_public_resolution": actionable,
            "documentation_partial_or_better": partial_public,
            "documentation_private_migration": private_migration,
            "verisflow_simulation_trace_rate": sim_successes / sim_trials,
            "verisflow_simulation_trace_wilson": list(sim_wilson),
        },
        "strongest_association": {
            "pair": [top_pair["Code A"], top_pair["Code B"]],
            **recomputed_top.to_dict(),
        },
    }
