"""Checks on the generated LaTeX tables, figures, and reproduction outputs."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest

from labauto_observatory.analysis import compute_release_results

ROOT = Path(__file__).resolve().parents[1]
COMMITTED_TABLES = ROOT / "paper" / "generated"
TABLE_NAMES = ("headline_metrics.tex", "strong_associations.tex", "code_counts.tex")
FIGURE_NAMES = (
    "conceptual_model",
    "study_workflow",
    "metric_dashboard",
    "associations",
    "discovery_resolution",
    "validation_funnel",
)


@pytest.fixture(scope="module")
def tables(
    load_script: Callable[[str], ModuleType], tmp_path_factory: pytest.TempPathFactory
) -> dict[str, str]:
    """Regenerate the LaTeX tables into a scratch directory."""

    module = load_script("build_tables")
    out = tmp_path_factory.mktemp("tables")
    module.OUT = out
    module.main()
    return {path.name: path.read_text(encoding="utf-8") for path in sorted(out.iterdir())}


@pytest.fixture(scope="module")
def figures(
    load_script: Callable[[str], ModuleType], tmp_path_factory: pytest.TempPathFactory
) -> Path:
    """Regenerate every manuscript figure into a scratch directory."""

    module = load_script("build_figures")
    out = tmp_path_factory.mktemp("figures")
    module.OUT = out
    module.main()
    return out


def test_generated_tables_are_committed_in_sync(tables: dict[str, str]) -> None:
    """`paper/generated` must match a fresh build so LaTeX never uses stale numbers."""

    assert set(tables) == set(TABLE_NAMES)
    for name in TABLE_NAMES:
        committed = (COMMITTED_TABLES / name).read_text(encoding="utf-8")
        assert tables[name] == committed, f"{name} is out of date; run `make tables`"


def test_headline_metrics_table_content(tables: dict[str, str]) -> None:
    content = tables["headline_metrics.tex"]
    assert "\\label{tab:headline-metrics}" in content
    rows = [line for line in content.splitlines() if line.endswith("\\\\") and line[0].isalnum()]
    assert len(rows) == 10  # one header row plus nine construct rows
    assert "B2 Integration accessibility & 63.9\\% & 6 device--interface cases \\\\" in content
    assert "B6 Preflight preventability & 66.7\\% & 3 definite scenarios \\\\" in content
    assert "B9 Core context expansion & 2.0$\\times$ & 5 opening classes \\\\" in content
    assert "do not estimate forum-wide or industry-wide rates" in content


def test_headline_metrics_table_matches_recomputed_values(tables: dict[str, str]) -> None:
    metrics = compute_release_results(ROOT)["metrics"]
    content = tables["headline_metrics.tex"]
    for key in (
        "integration_accessibility_mean",
        "reproducibility_manifest_mean",
        "physical_definition_mean",
        "observability_mean",
        "preflight_preventability_complete_case",
        "scheduling_constraint_discovery",
        "test_claim_aligned",
        "documentation_actionable_public_resolution",
    ):
        assert f"{100 * metrics[key]:.1f}\\%" in content
    assert f"{metrics['context_expansion_core']:.1f}$\\times$" in content


def test_code_counts_table_content(tables: dict[str, str]) -> None:
    counts = compute_release_results(ROOT)["corpus"]
    content = tables["code_counts.tex"]
    assert "\\label{tab:code-counts}" in content
    for code in (f"B{index}" for index in range(1, 11)):
        direct = counts["direct_support_counts"][code]
        primary = counts["primary_counts"][code]
        assert f"{code} & {direct} & {primary} \\\\" in content


def test_strong_associations_table_content(tables: dict[str, str]) -> None:
    association = compute_release_results(ROOT)["strongest_association"]
    content = tables["strong_associations.tex"]
    assert "\\label{tab:associations}" in content
    rows = [line for line in content.splitlines() if line.startswith("B")]
    assert len(rows) == 5
    assert rows[0].startswith("B5--B6 & 8/55 & 0.452 & 2.353")
    assert f"{association['phi']:.3f}" in content
    assert "Associations are descriptive." in content


def test_figures_are_created(figures: Path) -> None:
    for name in FIGURE_NAMES:
        pdf = figures / f"{name}.pdf"
        png = figures / f"{name}.png"
        assert pdf.is_file() and png.is_file(), f"missing output for {name}"
        assert pdf.read_bytes().startswith(b"%PDF"), f"{name}.pdf is not a PDF"
        assert png.read_bytes().startswith(b"\x89PNG"), f"{name}.png is not a PNG"
        assert pdf.stat().st_size > 1024
    assert {path.stem for path in figures.glob("*.pdf")} == set(FIGURE_NAMES)


def test_figure_output_is_deterministic(
    load_script: Callable[[str], ModuleType], tmp_path: Path
) -> None:
    """Committed figures must not churn when regenerated on the locked environment."""

    module = load_script("build_figures")
    results = compute_release_results(ROOT)
    renders = []
    for index in range(2):
        out = tmp_path / f"run{index}"
        module.OUT = out
        module.discovery_resolution(results)
        renders.append((out / "discovery_resolution.pdf").read_bytes())
    assert renders[0] == renders[1]


def test_validation_funnel_stages_are_read_from_data(
    load_script: Callable[[str], ModuleType],
) -> None:
    module = load_script("build_figures")
    stages = module._funnel_stages(ROOT)
    assert [stage["label"] for stage in stages] == [
        "Input",
        "Syntax",
        "Simulation",
        "Dry",
        "Wet",
        "Assay",
    ]
    assert [stage["value"] for stage in stages] == [1.0, 1.0, 0.92, 0.0, 0.0, 0.0]
    simulation = stages[2]
    assert simulation["stage"] == module.SIMULATION_STAGE
    assert (simulation["numerator"], simulation["denominator"]) == (92.0, 100.0)
    assert [stage["stage"] for stage in stages if stage["rate"] is not None] == [
        module.SIMULATION_STAGE
    ]
    assert [stage["label"] for stage in stages if not stage["reported"]] == ["Dry", "Wet", "Assay"]


def test_validation_funnel_fails_closed_on_missing_stage(
    load_script: Callable[[str], ModuleType], tmp_path: Path
) -> None:
    module = load_script("build_figures")
    source = ROOT / "data/metrics/ai_validation_funnel.csv"
    lines = source.read_text(encoding="utf-8").splitlines(keepends=True)
    target = tmp_path / "data" / "metrics"
    target.mkdir(parents=True)
    (target / "ai_validation_funnel.csv").write_text("".join(lines[:3]), encoding="utf-8")
    with pytest.raises(SystemExit, match="missing expected stages"):
        module._funnel_stages(tmp_path)


def test_join_labels(load_script: Callable[[str], ModuleType]) -> None:
    module = load_script("build_figures")
    assert module._join_labels(["Dry"]) == "dry"
    assert module._join_labels(["Dry", "Wet"]) == "dry or wet"
    assert module._join_labels(["Dry", "Wet", "Assay"]) == "dry, wet, or assay"


def test_reproduce_results_writes_machine_readable_summary(
    load_script: Callable[[str], ModuleType], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    module = load_script("reproduce_results")
    module.BUILD = tmp_path
    module.main()
    capsys.readouterr()
    payload = json.loads((tmp_path / "results.json").read_text(encoding="utf-8"))
    assert payload == compute_release_results(ROOT)
    summary = (tmp_path / "RESULTS.md").read_text(encoding="utf-8")
    assert "- Threads: 55" in summary
    assert "- Episodes: 45" in summary
    assert "phi=0.4525" in summary
