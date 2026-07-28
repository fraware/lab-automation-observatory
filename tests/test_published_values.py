from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from labauto_observatory.analysis import compute_release_results

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_CORPUS_KEYS = {
    "threads",
    "episodes",
    "episode_threads",
    "adjudication_threads",
    "constructs",
    "direct_support_counts",
    "primary_counts",
}
EXPECTED_METRIC_KEYS = {
    "integration_accessibility_mean",
    "reproducibility_manifest_mean",
    "physical_definition_mean",
    "observability_mean",
    "preflight_preventability_complete_case",
    "preflight_preventability_sensitivity",
    "preflight_preventability_wilson",
    "scheduling_opening_weighted_completeness",
    "scheduling_constraint_discovery",
    "scheduling_scenario_resolution",
    "test_claim_aligned",
    "test_claim_partial_or_better",
    "context_expansion_core",
    "context_expansion_broad",
    "context_expansion_conservative",
    "documentation_actionable_public_resolution",
    "documentation_partial_or_better",
    "documentation_private_migration",
    "verisflow_simulation_trace_rate",
    "verisflow_simulation_trace_wilson",
}
EXPECTED_ASSOCIATION_KEYS = {
    "pair",
    "n11",
    "n10",
    "n01",
    "n00",
    "jaccard",
    "lift",
    "phi",
    "p_b_given_a",
    "p_b_given_not_a",
    "descriptive_risk_ratio",
}
CODES = [f"B{index}" for index in range(1, 11)]


@pytest.fixture(scope="module")
def results() -> dict[str, Any]:
    return compute_release_results(ROOT)


def test_result_schema_is_stable(results: dict[str, Any]) -> None:
    """Downstream tables, figures, and the manuscript depend on these key names."""

    assert set(results) == {"corpus", "metrics", "strongest_association"}
    assert set(results["corpus"]) == EXPECTED_CORPUS_KEYS
    assert set(results["metrics"]) == EXPECTED_METRIC_KEYS
    assert set(results["strongest_association"]) == EXPECTED_ASSOCIATION_KEYS
    assert json.loads(json.dumps(results)) == results


def test_corpus_size(results: dict[str, Any]) -> None:
    corpus = results["corpus"]
    assert corpus["threads"] == 55
    assert corpus["episodes"] == 45
    assert corpus["episode_threads"] == 14
    assert corpus["constructs"] == 10
    assert corpus["direct_support_counts"]["B10"] == 48


def test_adjudication_subset_matches_episode_subset(results: dict[str, Any]) -> None:
    """The released hard-case set is exactly the episode-segmented subset."""

    corpus = results["corpus"]
    assert corpus["adjudication_threads"] == corpus["episode_threads"] == 14


def test_direct_support_and_primary_counts(results: dict[str, Any]) -> None:
    corpus = results["corpus"]
    direct = corpus["direct_support_counts"]
    primary = corpus["primary_counts"]
    assert list(direct) == CODES
    assert set(primary) == set(CODES)
    assert direct == {
        "B1": 29,
        "B2": 17,
        "B3": 18,
        "B4": 13,
        "B5": 17,
        "B6": 11,
        "B7": 12,
        "B8": 19,
        "B9": 5,
        "B10": 48,
    }
    assert sum(primary.values()) == corpus["threads"]
    assert all(primary[code] <= direct[code] for code in CODES)


def test_field_level_metrics(results: dict[str, Any]) -> None:
    metrics = results["metrics"]
    assert metrics["integration_accessibility_mean"] == pytest.approx(0.6388888889)
    assert metrics["reproducibility_manifest_mean"] == pytest.approx(0.5416666667)
    assert metrics["physical_definition_mean"] == pytest.approx(0.6704545455)
    assert metrics["observability_mean"] == pytest.approx(0.525)


def test_field_level_metrics_match_published_percentages(results: dict[str, Any]) -> None:
    """The percentages quoted in the abstract and results section are one-decimal rounds."""

    metrics = results["metrics"]
    rendered = {
        key: f"{100 * float(metrics[key]):.1f}"
        for key in (
            "integration_accessibility_mean",
            "reproducibility_manifest_mean",
            "physical_definition_mean",
            "observability_mean",
            "preflight_preventability_complete_case",
            "scheduling_opening_weighted_completeness",
            "scheduling_constraint_discovery",
            "test_claim_aligned",
            "documentation_actionable_public_resolution",
        )
    }
    assert rendered == {
        "integration_accessibility_mean": "63.9",
        "reproducibility_manifest_mean": "54.2",
        "physical_definition_mean": "67.0",
        "observability_mean": "52.5",
        "preflight_preventability_complete_case": "66.7",
        "scheduling_opening_weighted_completeness": "53.8",
        "scheduling_constraint_discovery": "87.5",
        "test_claim_aligned": "33.3",
        "documentation_actionable_public_resolution": "41.7",
    }


def test_bounded_case_metrics(results: dict[str, Any]) -> None:
    metrics = results["metrics"]
    assert metrics["preflight_preventability_complete_case"] == pytest.approx(2 / 3)
    assert metrics["preflight_preventability_sensitivity"] == pytest.approx([0.5, 0.75])
    assert metrics["scheduling_opening_weighted_completeness"] == pytest.approx(7 / 13)
    assert metrics["scheduling_constraint_discovery"] == pytest.approx(7 / 8)
    assert metrics["scheduling_scenario_resolution"] == 0
    assert metrics["test_claim_aligned"] == pytest.approx(2 / 6)
    assert metrics["test_claim_partial_or_better"] == pytest.approx(5 / 6)
    assert metrics["context_expansion_core"] == 2.0
    assert metrics["context_expansion_broad"] == pytest.approx(3.4)
    assert metrics["documentation_actionable_public_resolution"] == pytest.approx(5 / 12)


def test_secondary_headline_metrics(results: dict[str, Any]) -> None:
    """Secondary values that the manuscript and supplement also report."""

    metrics = results["metrics"]
    assert metrics["context_expansion_conservative"] == pytest.approx(2.2)
    assert metrics["documentation_partial_or_better"] == pytest.approx(10 / 12)
    assert metrics["documentation_private_migration"] == pytest.approx(3 / 12)
    assert metrics["verisflow_simulation_trace_rate"] == pytest.approx(0.92)


def test_interval_estimates(results: dict[str, Any]) -> None:
    metrics = results["metrics"]
    assert metrics["preflight_preventability_wilson"] == pytest.approx([0.2076549551, 0.9385096847])
    assert metrics["verisflow_simulation_trace_wilson"] == pytest.approx(
        [0.8500173312, 0.9589070305]
    )
    lower, upper = metrics["preflight_preventability_sensitivity"]
    assert lower <= metrics["preflight_preventability_complete_case"] <= upper


def test_strongest_association(results: dict[str, Any]) -> None:
    association = results["strongest_association"]
    assert association["pair"] == ["B5", "B6"]
    assert association["phi"] == pytest.approx(0.4524614483)
    assert association["lift"] == pytest.approx(2.3529411765)


def test_strongest_association_table_and_derived_measures(results: dict[str, Any]) -> None:
    association = results["strongest_association"]
    corpus = results["corpus"]
    assert (association["n11"], association["n10"], association["n01"], association["n00"]) == (
        8,
        9,
        3,
        35,
    )
    assert sum(association[key] for key in ("n11", "n10", "n01", "n00")) == corpus["threads"]
    assert association["jaccard"] == pytest.approx(0.4)
    assert association["p_b_given_a"] == pytest.approx(8 / 17)
    assert association["p_b_given_not_a"] == pytest.approx(3 / 38)
    assert association["descriptive_risk_ratio"] == pytest.approx(5.9607843137)
