#!/usr/bin/env python3
"""Generate the manuscript's reproducible vector figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from labauto_observatory.analysis import compute_release_results

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figures"


def save(name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    plt.savefig(OUT / f"{name}.png", dpi=220, bbox_inches="tight")
    plt.close()


def conceptual_model() -> None:
    fig, ax = plt.subplots(figsize=(10.4, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    layers = [
        (0.3, 3.65, 9.4, 0.75, "Ecosystem knowledge and support", "B1  Knowledge packaging     B10  Documentation, training, support"),
        (0.3, 2.65, 9.4, 0.75, "Interfaces and representations", "B2  Device access     B3  Deployment identity     B4  Physical resources"),
        (0.3, 1.65, 9.4, 0.75, "Runtime coordination", "B5  Observability     B6  Recovery     B7  Scheduling"),
        (0.3, 0.65, 5.85, 0.75, "Evaluation", "B8  Test–claim alignment"),
        (6.35, 0.65, 3.35, 0.75, "Emerging AI", "B9  Context and physical feedback"),
    ]
    for x, y, w, h, title, subtitle in layers:
        patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", linewidth=1.2, alpha=0.13)
        ax.add_patch(patch)
        ax.text(x + 0.18, y + 0.48, title, fontsize=11, fontweight="bold", va="center")
        ax.text(x + 0.18, y + 0.19, subtitle, fontsize=8.5, va="center")
    for y1, y2 in [(3.65, 3.40), (2.65, 2.40), (1.65, 1.40)]:
        ax.add_patch(FancyArrowPatch((5, y1), (5, y2), arrowstyle="-|>", mutation_scale=12, linewidth=1))
    ax.text(5, 4.72, "Boundary-centered model of public laboratory-automation bottlenecks", ha="center", fontsize=13, fontweight="bold")
    ax.text(5, 0.12, "The model organizes analytical constructs; it does not claim exhaustiveness or population prevalence.", ha="center", fontsize=8.5)
    save("conceptual_model")


def study_workflow() -> None:
    fig, ax = plt.subplots(figsize=(10.2, 5.0))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 5.0)
    ax.axis("off")
    boxes = [
        (0.45, 2.95, "1", "55 public threads", "Purposive evidence register"),
        (3.75, 2.95, "2", "14 difficult threads", "Coding-stress subset"),
        (7.05, 2.95, "3", "45 analytical episodes", "Problem, evidence, outcome"),
        (7.05, 1.00, "4", "10 bounded constructs", "Explicit inclusion and exclusion"),
        (3.75, 1.00, "5", "Executable metrics", "Units, denominators, sensitivity"),
        (0.45, 1.00, "6", "Community artifacts", "Templates, schemas, seed records"),
    ]
    for x, y, number, title, subtitle in boxes:
        patch = FancyBboxPatch((x, y), 2.65, 1.08, boxstyle="round,pad=0.04,rounding_size=0.08", linewidth=1.15, alpha=0.15)
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
        ax.add_patch(FancyArrowPatch(source, target, arrowstyle="-|>", mutation_scale=13, linewidth=1.1))
    ax.text(5.1, 4.55, "Analytical workflow", ha="center", fontsize=14, fontweight="bold")
    ax.text(5.1, 0.35, "Reproduction uses committed derived data and does not query the forum.", ha="center", fontsize=9)
    save("study_workflow")


def metric_dashboard() -> None:
    results = compute_release_results(ROOT)["metrics"]
    entries = [
        ("B2 Interface\naccessibility", results["integration_accessibility_mean"]),
        ("B3 Deployment\nmanifest", results["reproducibility_manifest_mean"]),
        ("B4 Physical\ndefinition", results["physical_definition_mean"]),
        ("B5 Observability", results["observability_mean"]),
        ("B8 Test–claim\nalignment", results["test_claim_aligned"]),
        ("B10 Actionable\npublic outcome", results["documentation_actionable_public_resolution"]),
    ]
    fig, ax = plt.subplots(figsize=(9.4, 4.6))
    bars = ax.bar([e[0] for e in entries], [100 * e[1] for e in entries])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Pilot metric (%)")
    ax.set_title("Field-level metrics from bounded case studies")
    ax.grid(axis="y", alpha=0.25)
    for bar, (_, value) in zip(bars, entries, strict=True):
        ax.text(bar.get_x() + bar.get_width() / 2, 100 * value + 2, f"{100*value:.1f}%", ha="center", fontsize=9)
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
        ax.text(value + 0.01, bar.get_y() + bar.get_height() / 2, f"{value:.3f}", va="center", fontsize=9)
    fig.tight_layout()
    save("associations")


def discovery_resolution() -> None:
    labels = ["Opening weighted\ncompleteness", "Incomplete fields\nsurfaced", "Incomplete fields\nresolved"]
    values = [53.8, 87.5, 0.0]
    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    bars = ax.bar(labels, values)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Percent")
    ax.set_title("Scheduling toy problem: discovery without closure")
    ax.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, values, strict=True):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 2, f"{value:.1f}%", ha="center", fontsize=9)
    fig.tight_layout()
    save("discovery_resolution")


def validation_funnel() -> None:
    stages = ["Input", "Syntax", "Simulation", "Dry", "Wet", "Assay"]
    reported = [1, 1, 0.92, 0, 0, 0]
    fig, ax = plt.subplots(figsize=(8.8, 4.5))
    ax.plot(stages, reported, marker="o", linewidth=2)
    ax.fill_between(range(len(stages)), reported, alpha=0.12)
    ax.set_ylim(-0.05, 1.08)
    ax.set_ylabel("Reported quantitative support")
    ax.set_title("AI method-generation validation funnel")
    ax.annotate("92/100 simulation-trace agreement", xy=(2, 0.92), xytext=(2.4, 0.72), arrowprops={"arrowstyle": "->"})
    ax.text(4.35, 0.08, "No dry, wet, or assay rate reported", ha="center", fontsize=9)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save("validation_funnel")


def main() -> None:
    conceptual_model()
    study_workflow()
    metric_dashboard()
    association_plot()
    discovery_resolution()
    validation_funnel()


if __name__ == "__main__":
    main()
