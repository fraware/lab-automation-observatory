from __future__ import annotations

from pathlib import Path

import pytest

from labauto_observatory.analysis import compute_release_results

ROOT = Path(__file__).resolve().parents[1]


def test_corpus_size() -> None:
    results = compute_release_results(ROOT)
    assert results["corpus"]["threads"] == 55
    assert results["corpus"]["episodes"] == 45
    assert results["corpus"]["direct_support_counts"]["B10"] == 48


def test_field_level_metrics() -> None:
    metrics = compute_release_results(ROOT)["metrics"]
    assert metrics["integration_accessibility_mean"] == pytest.approx(0.6388888889)
    assert metrics["reproducibility_manifest_mean"] == pytest.approx(0.5416666667)
    assert metrics["physical_definition_mean"] == pytest.approx(0.6704545455)
    assert metrics["observability_mean"] == pytest.approx(0.525)


def test_bounded_case_metrics() -> None:
    metrics = compute_release_results(ROOT)["metrics"]
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


def test_strongest_association() -> None:
    association = compute_release_results(ROOT)["strongest_association"]
    assert association["pair"] == ["B5", "B6"]
    assert association["phi"] == pytest.approx(0.4524614483)
    assert association["lift"] == pytest.approx(2.3529411765)
