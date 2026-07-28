#!/usr/bin/env python3
"""Build the boundary-centered graphical abstract."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PNG = ROOT / "paper" / "graphical_abstract.png"
OUTPUT_PDF = ROOT / "paper" / "graphical_abstract.pdf"


def _box(ax: plt.Axes, x: float, y: float, width: float, height: float, title: str, body: str) -> None:
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.012",
        facecolor="#e4eef5",
        edgecolor="#c7cdd1",
        linewidth=1.5,
    )
    ax.add_patch(patch)
    ax.text(x + 0.02, y + height * 0.65, title, fontsize=17, fontweight="bold", va="center")
    ax.text(x + 0.02, y + height * 0.27, body, fontsize=12.5, va="center")


def _arrow(ax: plt.Axes, y_top: float, y_bottom: float) -> None:
    ax.add_patch(
        FancyArrowPatch(
            (0.5, y_top),
            (0.5, y_bottom),
            arrowstyle="-|>",
            mutation_scale=17,
            linewidth=1.5,
        )
    )


def main() -> None:
    fig, ax = plt.subplots(figsize=(12, 5.3))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(
        0.5,
        0.955,
        "Boundary-centered model of public laboratory-automation bottlenecks",
        ha="center",
        va="center",
        fontsize=19,
        fontweight="bold",
    )
    _box(
        ax,
        0.04,
        0.735,
        0.92,
        0.145,
        "Ecosystem knowledge and support",
        "B1  Knowledge packaging     B10  Documentation, training, support",
    )
    _arrow(ax, 0.73, 0.695)
    _box(
        ax,
        0.04,
        0.535,
        0.92,
        0.145,
        "Interfaces and representations",
        "B2  Device access     B3  Deployment identity     B4  Physical resources",
    )
    _arrow(ax, 0.53, 0.495)
    _box(
        ax,
        0.04,
        0.335,
        0.92,
        0.145,
        "Runtime coordination",
        "B5  Observability     B6  Recovery     B7  Scheduling",
    )
    _arrow(ax, 0.33, 0.295)
    _box(ax, 0.04, 0.135, 0.57, 0.145, "Evaluation", "B8  Test–claim alignment")
    _box(
        ax,
        0.64,
        0.135,
        0.32,
        0.145,
        "Emerging AI",
        "B9  Context and physical feedback",
    )
    ax.text(
        0.5,
        0.055,
        "The model organizes analytical constructs; it does not claim exhaustiveness or population prevalence.",
        ha="center",
        va="center",
        fontsize=11.5,
    )
    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PNG, dpi=180, bbox_inches="tight")
    fig.savefig(OUTPUT_PDF, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
