#!/usr/bin/env python3
"""Generate the manuscript's reproducible vector figures.

Every plotted value is derived from committed release data through
``compute_release_results`` or the metric CSV files. Output metadata is
suppressed so that repeated runs on a pinned environment produce byte-identical
files and the committed PDFs stay diff-free.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from labauto_observatory.analysis import compute_release_results
from labauto_observatory.io import numeric, read_csv

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figures"

# Short axis labels for the AI validation funnel. The mapping is exhaustive by
# design: an unexpected stage name in the CSV must fail rather than be dropped.
FUNNEL_STAGE_LABELS = {
    "Prompt / input parsing": "Input",
    "Syntactic / generation completion": "Syntax",
    "Simulation trace agreement": "Simulation",
    "Dry physical execution": "Dry",
    "Wet execution": "Wet",
    "Assay performance": "Assay",
}
NOT_REPORTED = "Not reported"
# The one funnel stage with a reported denominator; its caption names that stage.
SIMULATION_STAGE = "Simulation trace agreement"


def save(name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT / f"{name}.pdf", bbox_inches="tight", metadata={"CreationDate": None})
    plt.savefig(OUT / f"{name}.png", dpi=220, bbox_inches="tight", metadata={"Software": None})
    plt.close()


def conceptual_model() -> None:
    _, ax = plt.subplots(figsize=(10.4, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    layers = [
        (
            0.3,
            3.65,
            9.4,
            0.75,
            "Ecosystem knowledge and support",
            "B1  Knowledge packaging     B10  Documentation, training, support",
        ),
        (
            0.3,
            2.65,
            9.4,
            0.75,
            "Interfaces and representations",
            "B2  Device access     B3  Deployment identity     B4  Physical resources",
        ),
        (
            0.3,
            1.65,
            9.4,
            0.75,
            "Runtime coordination",
            "B5  Observability     B6  Recovery     B7  Scheduling",
        ),
        (0.3, 0.65, 5.85, 0.75, "Evaluation", "B8  Test–claim alignment"),
        (6.35, 0.65, 3.35, 0.75, "Emerging AI", "B9  Context and physical feedback"),
    ]
    for x, y, w, h, title, subtitle in layers:
        patch = FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", linewidth=1.2, alpha=0.13
        )
        ax.add_patch(patch)
        ax.text(x + 0.18, y + 0.48, title, fontsize=11, fontweight="bold", va="center")
        ax.text(x + 0.18, y + 0.19, subtitle, fontsize=8.5, va="center")
    for y1, y2 in [(3.65, 3.40), (2.65, 2.40), (1.65, 1.40)]:
        ax.add_patch(
            FancyArrowPatch((5, y1), (5, y2), arrowstyle="-|>", mutation_scale=12, linewidth=1)
        )
    ax.text(
        5,
        4.72,
        "Boundary-centered model of public laboratory-automation bottlenecks",
        ha="center",
        fontsize=13,
        fontweight="bold",
    )
    ax.text(
        5,
        0.12,
        "The model organizes analytical constructs; it does not claim exhaustiveness or population prevalence.",
        ha="center",
        fontsize=8.5,
    )
    save("conceptual_model")


def study_workflow(results: dict[str, Any]) -> None:
    corpus = results["corpus"]
    _, ax = plt.subplots(figsize=(10.2, 5.0))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 5.0)
    ax.axis("off")
    boxes = [
        (0.45, 2.95, "1", f"{corpus['threads']} public threads", "Purposive evidence register"),
        (3.75, 2.95, "2", f"{corpus['episode_threads']} difficult threads", "Coding-stress subset"),
        (
            7.05,
            2.95,
            "3",
            f"{corpus['episodes']} analytical episodes",
            "Problem, evidence, outcome",
        ),
        (
            7.05,
            1.00,
            "4",
            f"{corpus['constructs']} bounded constructs",
            "Explicit inclusion and exclusion",
        ),
        (3.75, 1.00, "5", "Executable metrics", "Units, denominators, sensitivity"),
        (0.45, 1.00, "6", "Community artifacts", "Templates, schemas, seed records"),
    ]
    for x, y, number, title, subtitle in boxes:
        patch = FancyBboxPatch(
            (x, y),
            2.65,
            1.08,
            boxstyle="round,pad=0.04,rounding_size=0.08",
            linewidth=1.15,
            alpha=0.15,
        )
        ax.add_patch(patch)
        ax.text(x + 0.18, y + 0.78, number, fontsize=10, fontweight="bold", va="center")
        ax.text(x + 0.48, y + 0.78, title, fontsize=10, fontweight="bold", va="center")
        ax.text(x + 0.18, y + 0.34, subtitle, fontsize=8.3, va="center")
    arrows = [
        ((3.10, 3.49), (3.72, 3.49)),
        ((6.40, 3.49), (7.02, 3.49)),
        ((8.38, 2.94), (8.38, 2.12)),
        ((7.02, 1.54), (6.43, 1.54)),
        ((3.72, 1.54), (3.13, 1.54)),
    ]
    for source, target in arrows:
        ax.add_patch(
            FancyArrowPatch(source, target, arrowstyle="-|>", mutation_scale=13, linewidth=1.1)
        )
    ax.text(5.1, 4.55, "Analytical workflow", ha="center", fontsize=14, fontweight="bold")
    ax.text(
        5.1,
        0.35,
        "Reproduction uses committed derived data and does not query the forum.",
        ha="center",
        fontsize=9,
    )
    save("study_workflow")


def metric_dashboard(results: dict[str, Any]) -> None:
    metrics = results["metrics"]
    entries = [
        ("B2 Interface\naccessibility", metrics["integration_accessibility_mean"]),
        ("B3 Deployment\nmanifest", metrics["reproducibility_manifest_mean"]),
        ("B4 Physical\ndefinition", metrics["physical_definition_mean"]),
        ("B5 Observability", metrics["observability_mean"]),
        ("B8 Test–claim\nalignment", metrics["test_claim_aligned"]),
        ("B10 Actionable\npublic outcome", metrics["documentation_actionable_public_resolution"]),
    ]
    fig, ax = plt.subplots(figsize=(9.4, 4.6))
    bars = ax.bar([e[0] for e in entries], [100 * e[1] for e in entries])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Pilot metric (%)")
    ax.set_title("Field-level metrics from bounded case studies")
    ax.grid(axis="y", alpha=0.25)
    for bar, (_, value) in zip(bars, entries, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            100 * value + 2,
            f"{100 * value:.1f}%",
            ha="center",
            fontsize=9,
        )
    fig.tight_layout()
    save("metric_dashboard")


def association_plot() -> None:
    frame = pd.read_csv(ROOT / "data/metrics/pairwise_associations.csv").head(5).iloc[::-1]
    labels = [f"{a}–{b}" for a, b in zip(frame["Code A"], frame["Code B"], strict=True)]
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    bars = ax.barh(labels, frame["Phi"])
    ax.set_xlim(0, 0.55)
    ax.set_xlabel("Phi coefficient")
    ax.set_title("Strongest technical-code associations")
    ax.grid(axis="x", alpha=0.25)
    for bar, value in zip(bars, frame["Phi"], strict=True):
        ax.text(
            value + 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.3f}",
            va="center",
            fontsize=9,
        )
    fig.tight_layout()
    save("associations")


def discovery_resolution(results: dict[str, Any]) -> None:
    metrics = results["metrics"]
    entries = [
        ("Opening weighted\ncompleteness", metrics["scheduling_opening_weighted_completeness"]),
        ("Incomplete fields\nsurfaced", metrics["scheduling_constraint_discovery"]),
        ("Incomplete fields\nresolved", metrics["scheduling_scenario_resolution"]),
    ]
    values = [100 * value for _, value in entries]
    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    bars = ax.bar([label for label, _ in entries], values)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Percent")
    ax.set_title("Scheduling toy problem: discovery without closure")
    ax.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2, value + 2, f"{value:.1f}%", ha="center", fontsize=9
        )
    fig.tight_layout()
    save("discovery_resolution")


def _funnel_stages(root: Path) -> list[dict[str, Any]]:
    """Read the ordered funnel stages plotted in the validation-funnel figure."""

    rows = read_csv(root / "data/metrics/ai_validation_funnel.csv")
    stages = [row for row in rows if row["Stage"] in FUNNEL_STAGE_LABELS]
    missing = set(FUNNEL_STAGE_LABELS) - {row["Stage"] for row in stages}
    if missing:
        raise SystemExit(f"validation funnel is missing expected stages: {sorted(missing)}")
    plotted: list[dict[str, Any]] = []
    for row in stages:
        rate = numeric(row["Rate"])
        reported = row["Evidence status"] != NOT_REPORTED
        plotted.append(
            {
                "stage": row["Stage"],
                "label": FUNNEL_STAGE_LABELS[row["Stage"]],
                # Stages without a denominator are plotted as reported capability;
                # only a stage with an explicit rate carries a quantitative result.
                "value": rate if rate is not None else float(reported),
                "rate": rate,
                "numerator": numeric(row["Numerator"]),
                "denominator": numeric(row["Denominator"]),
                "reported": reported,
            }
        )
    return plotted


def _join_labels(labels: list[str]) -> str:
    lowered = [label.lower() for label in labels]
    if len(lowered) == 1:
        return lowered[0]
    if len(lowered) == 2:
        return f"{lowered[0]} or {lowered[1]}"
    return f"{', '.join(lowered[:-1])}, or {lowered[-1]}"


def validation_funnel() -> None:
    stages = _funnel_stages(ROOT)
    labels = [stage["label"] for stage in stages]
    values = [stage["value"] for stage in stages]
    fig, ax = plt.subplots(figsize=(8.8, 4.5))
    ax.plot(labels, values, marker="o", linewidth=2)
    ax.fill_between(range(len(labels)), values, alpha=0.12)
    ax.set_ylim(-0.05, 1.08)
    ax.set_ylabel("Reported quantitative support")
    ax.set_title("AI method-generation validation funnel")
    for index, stage in enumerate(stages):
        if stage["stage"] != SIMULATION_STAGE or stage["rate"] is None:
            continue
        ax.annotate(
            f"{int(stage['numerator'])}/{int(stage['denominator'])} simulation-trace agreement",
            xy=(index, stage["rate"]),
            xytext=(index + 0.4, stage["rate"] - 0.2),
            arrowprops={"arrowstyle": "->"},
        )
    unreported = [index for index, stage in enumerate(stages) if not stage["reported"]]
    if unreported:
        note = f"No {_join_labels([stages[index]['label'] for index in unreported])} rate reported"
        ax.text(sum(unreported) / len(unreported), 0.08, note, ha="center", fontsize=9)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save("validation_funnel")


def main() -> None:
    results = compute_release_results(ROOT)
    conceptual_model()
    study_workflow(results)
    metric_dashboard(results)
    association_plot()
    discovery_resolution(results)
    validation_funnel()


if __name__ == "__main__":
    main()
