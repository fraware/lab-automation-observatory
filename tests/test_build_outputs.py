"""Checks on the generated LaTeX tables, figures, and reproduction outputs."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest

from labauto_observatory.analysis import compute_release_results
from labauto_observatory.io import read_csv

ROOT = Path(__file__).resolve().parents[1]
COMMITTED_TABLES = ROOT / "paper" / "generated"
requires_paper = pytest.mark.skipif(
    not (ROOT / "paper" / "main.tex").is_file(),
    reason="manuscript sources are not present in this checkout",
)
TABLE_NAMES = (
    "headline_metrics.tex",
    "strong_associations.tex",
    "code_counts.tex",
    "quotations.tex",
)
ROBUSTNESS_TABLE_NAMES = (
    "partial_score_sensitivity.tex",
    "association_leave_one_out.tex",
    "denominator_sensitivity.tex",
)
# Five main-text figures and three supplement figures. Keeping the tuple exact
# guards the agreed main-text budget: a new figure must be a deliberate change
# here as well as in the LaTeX sources.
MAIN_FIGURE_NAMES = (
    "conceptual_model",
    "study_workflow",
    "component_heatmap",
    "discovery_resolution",
    "associations",
)
SUPPLEMENT_FIGURE_NAMES = (
    "validation_funnel",
    "b8_alignment_matrix",
    "b6_preflight_preventability",
)
FIGURE_NAMES = MAIN_FIGURE_NAMES + SUPPLEMENT_FIGURE_NAMES


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
def robustness_tables(
    load_script: Callable[[str], ModuleType], tmp_path_factory: pytest.TempPathFactory
) -> dict[str, str]:
    """Regenerate the robustness LaTeX tables into a scratch directory."""

    module = load_script("build_robustness_tables")
    out = tmp_path_factory.mktemp("robustness_tables")
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


@requires_paper
def test_generated_tables_are_committed_in_sync(tables: dict[str, str]) -> None:
    """`paper/generated` must match a fresh build so LaTeX never uses stale numbers."""

    assert set(tables) == set(TABLE_NAMES)
    for name in TABLE_NAMES:
        committed = (COMMITTED_TABLES / name).read_text(encoding="utf-8")
        assert tables[name] == committed, f"{name} is out of date; run `make tables`"


@requires_paper
def test_generated_robustness_tables_are_committed_in_sync(
    robustness_tables: dict[str, str],
) -> None:
    """Robustness `.tex` files must match a fresh `build_robustness_tables` run."""

    assert set(robustness_tables) == set(ROBUSTNESS_TABLE_NAMES)
    for name in ROBUSTNESS_TABLE_NAMES:
        committed = (COMMITTED_TABLES / name).read_text(encoding="utf-8")
        assert robustness_tables[name] == committed, f"{name} is out of date; run `make tables`"


def test_headline_metrics_table_content(tables: dict[str, str]) -> None:
    content = tables["headline_metrics.tex"]
    assert "\\label{tab:headline-metrics}" in content
    rows = [line for line in content.splitlines() if line.endswith("\\\\") and line[0].isalnum()]
    assert len(rows) == 10  # one header row plus nine construct rows
    assert "B2 Integration accessibility & 63.9\\% & -- & 6 device--interface cases \\\\" in content
    assert (
        "B6 Preflight preventability & 66.7\\% & 20.8--93.9\\% & "
        "3 definite scenarios of 4 eligible \\\\" in content
    )
    assert "B9 Core context expansion & 2.0$\\times$ & -- & 5 opening classes \\\\" in content
    assert "do not estimate forum-wide or industry-wide rates" in content


def test_headline_metrics_interval_column_is_only_for_proportions(
    tables: dict[str, str],
) -> None:
    """A mean of ordinal component scores must not carry a binomial interval."""

    content = tables["headline_metrics.tex"]
    intervals = {
        line.split("&")[0].strip(): line.split("&")[2].strip()
        for line in content.splitlines()
        if line.endswith("\\\\") and line.startswith("B")
    }
    means_and_ratios = (
        "B2 Integration accessibility",
        "B3 Deployment manifest",
        "B4 Physical definitions",
        "B5 Observability",
        "B9 Core context expansion",
    )
    for construct in means_and_ratios:
        assert intervals[construct] == "--"
    for construct, interval in intervals.items():
        if construct not in means_and_ratios:
            assert interval.endswith("\\%") and "--" in interval


def test_quotations_table_covers_the_whole_quote_bank(tables: dict[str, str]) -> None:
    quotes = read_csv(ROOT / "data/derived/quote_bank.csv")
    content = tables["quotations.tex"]
    rows = [line for line in content.splitlines() if line.endswith("\\\\") and line[0] == "B"]
    assert len(rows) == len(quotes)
    assert "\\label{tab:s-quotations}" in content
    assert "never counted as quantitative observations" in content


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


@requires_paper
def test_main_text_holds_seven_figures_and_tables() -> None:
    """The manuscript keeps a fixed main-text display budget of seven items."""

    sources = sorted((ROOT / "paper" / "sections").glob("*.tex"))
    body = "\n".join(path.read_text(encoding="utf-8") for path in sources)
    included = re.findall(r"\\includegraphics\[[^]]*\]\{figures/([^.}]+)\.pdf\}", body)
    inputs = re.findall(r"\\input\{generated/([^.}]+)\.tex\}", body)
    assert sorted(included) == sorted(MAIN_FIGURE_NAMES)
    assert sorted(inputs) == ["headline_metrics", "strong_associations"]
    assert len(included) + len(inputs) == 7


@requires_paper
def test_supplement_uses_the_remaining_figures_and_tables() -> None:
    """Supplement references every non-main generated figure and table stem."""

    supplement = (ROOT / "paper" / "supplement.tex").read_text(encoding="utf-8")
    included = re.findall(r"\\includegraphics\[[^]]*\]\{figures/([^.}]+)\.pdf\}", supplement)
    inputs = re.findall(r"\\input\{generated/([^.}]+)\.tex\}", supplement)
    assert sorted(included) == sorted(SUPPLEMENT_FIGURE_NAMES)
    assert sorted(inputs) == [
        "association_leave_one_out",
        "code_counts",
        "denominator_sensitivity",
        "partial_score_sensitivity",
        "quotations",
    ]


@requires_paper
def test_committed_figures_match_the_expected_set() -> None:
    """No stale PDF may linger in `paper/figures` after a figure is swapped out."""

    committed = {path.stem for path in (ROOT / "paper" / "figures").glob("*.pdf")}
    assert committed == set(FIGURE_NAMES)


@requires_paper
def test_every_figure_can_reach_a_float_page() -> None:
    """Guards the two halves of the fix for figures escaping past the bibliography.

    A float that LaTeX rejects everywhere is deferred behind every later float
    and flushed at the end of the document, so the multi-panel figures need both
    a raised top fraction and a float page as a last resort. Neither piece is
    visible in a compiled page count, so assert them at the source.
    """

    sources = sorted((ROOT / "paper" / "sections").glob("*.tex"))
    sources.append(ROOT / "paper" / "supplement.tex")
    for path in sources:
        placements = re.findall(r"\\begin\{figure\}\[([^]]*)\]", path.read_text(encoding="utf-8"))
        assert all("p" in placement for placement in placements), path.name

    macros = (ROOT / "paper" / "macros.tex").read_text(encoding="utf-8")
    assert "\\renewcommand{\\topfraction}{0.85}" in macros
    assert "\\renewcommand{\\floatpagefraction}{0.8}" in macros


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
