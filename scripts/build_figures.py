#!/usr/bin/env python3
"""Generate the manuscript's reproducible vector figures.

Every plotted value is derived from committed release data through
``compute_release_results``, ``component_matrices``, or the metric CSV files.
Shared typography, palettes, and the deterministic save path live in
``figure_style``, which also owns the single taxonomy specification used by both
the conceptual model and the graphical abstract.

Main-text figures stay at three: the B2--B5 component heatmap, the 13-field
scheduling requirement matrix, and the full 28-pair phi matrix, plus the two
schematic figures. The richer field-level panels go to the supplement.
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

from figure_style import (
    CELL_LABEL_SIZE,
    DIVERGING_CMAP,
    PALETTE,
    SCORE_CMAP,
    apply_style,
    draw_taxonomy,
    panel_label,
    save,
    score_heatmap,
)
from labauto_observatory.analysis import (
    B8_ELEMENTS,
    component_matrices,
    compute_release_results,
)
from labauto_observatory.associations import (
    PAIRWISE_RELATIVE,
    PHI_THRESHOLD,
    TECHNICAL_CODES,
)
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
QUANTITATIVE = "Product-reported quantitative"
# The one funnel stage with a reported denominator; its caption names that stage.
SIMULATION_STAGE = "Simulation trace agreement"

# The component grid needs more width than the text column, so it is drawn with
# oversized type that lands near the body size once LaTeX scales it down.
HEATMAP_TICK_SIZE = 9.8
HEATMAP_CELL_SIZE = 8.2
HEATMAP_TITLE_SIZE = 11.0

DETECTABILITY_COLORS = {
    "Yes": PALETTE[0],
    "No": PALETTE[1],
    "Indeterminate": PALETTE[4],
}
# PALETTE[4] is a light amber, so white in-bar text would be unreadable on it.
DETECTABILITY_TEXT_COLORS = {"Yes": "white", "No": "white", "Indeterminate": "#1a1a1a"}


def conceptual_model() -> None:
    """Layered taxonomy. The LaTeX caption carries the interpretation."""

    fig, ax = plt.subplots(figsize=(10.4, 4.6))
    draw_taxonomy(ax)
    fig.tight_layout()
    save(OUT, "conceptual_model", fig)


def study_workflow(results: dict[str, Any]) -> None:
    corpus = results["corpus"]
    fig, ax = plt.subplots(figsize=(10.2, 4.4))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0.4, 4.3)
    ax.axis("off")
    boxes = [
        (0.45, 2.75, "1", f"{corpus['threads']} public threads", "Purposive evidence register"),
        (3.75, 2.75, "2", f"{corpus['episode_threads']} difficult threads", "Coding-stress subset"),
        (
            7.05,
            2.75,
            "3",
            f"{corpus['episodes']} analytical episodes",
            "Problem, evidence, outcome",
        ),
        (
            7.05,
            0.90,
            "4",
            f"{corpus['constructs']} bounded constructs",
            "Explicit inclusion and exclusion",
        ),
        (3.75, 0.90, "5", "Executable metrics", "Units, denominators, sensitivity"),
        (0.45, 0.90, "6", "Community artifacts", "Templates, schemas, seed records"),
    ]
    for x, y, number, title, subtitle in boxes:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                2.65,
                1.02,
                boxstyle="round,pad=0.04,rounding_size=0.08",
                facecolor="#dce9f4",
                edgecolor="#7f8c99",
                linewidth=0.9,
            )
        )
        ax.text(x + 0.18, y + 0.72, number, fontsize=9.5, fontweight="bold", va="center")
        ax.text(x + 0.50, y + 0.72, title, fontsize=9.5, fontweight="bold", va="center")
        ax.text(x + 0.18, y + 0.30, subtitle, fontsize=8.0, va="center")
    arrows = [
        ((3.10, 3.26), (3.72, 3.26)),
        ((6.40, 3.26), (7.02, 3.26)),
        ((8.38, 2.74), (8.38, 1.95)),
        ((7.02, 1.41), (6.43, 1.41)),
        ((3.72, 1.41), (3.13, 1.41)),
    ]
    for source, target in arrows:
        ax.add_patch(
            FancyArrowPatch(
                source, target, arrowstyle="-|>", mutation_scale=11, linewidth=0.9, color="#44515e"
            )
        )
    ax.text(
        5.1,
        0.52,
        "Reproduction uses committed derived data and does not query the forum.",
        ha="center",
        fontsize=8.0,
    )
    fig.tight_layout()
    save(OUT, "study_workflow", fig)


def component_heatmap(root: Path) -> None:
    """Field-level component scores for B2--B5 over the same bounded cases.

    Components are placed on the vertical axis so that their long names stay
    horizontal and legible after the figure is scaled to the text width; the
    horizontal axis carries the short case identifiers.

    The height is capped so that the scaled artwork plus its caption stays
    inside elsarticle's ``\\topfraction`` of the text block. A taller panel grid
    cannot be placed as a top float and LaTeX defers it, and every later float,
    past the bibliography.
    """

    matrices = component_matrices(root)
    codes = ("B2", "B3", "B4", "B5")
    fig, axes = plt.subplots(2, 2, figsize=(7.4, 5.2), layout="constrained")
    images = []
    for ax, code in zip(axes.flat, codes, strict=True):
        matrix = matrices[code]
        transposed = [list(column) for column in zip(*matrix["values"], strict=True)]
        # The panel title already carries the construct, so the shared "B2-"
        # prefix is dropped from the tick labels to keep them from colliding.
        cases = [case.split("-", 1)[-1] for case in matrix["cases"]]
        images.append(
            score_heatmap(
                ax,
                transposed,
                matrix["components"],
                cases,
                cmap=SCORE_CMAP,
                rotation=0,
                cell_label_size=HEATMAP_CELL_SIZE,
            )
        )
        ax.tick_params(labelsize=HEATMAP_TICK_SIZE)
        ax.set_xlabel(f"{len(cases)} {matrix['unit']}", fontsize=HEATMAP_TICK_SIZE)
        panel_label(ax, f"{code} {matrix['label']}", size=HEATMAP_TITLE_SIZE)
    bar = fig.colorbar(
        images[0],
        ax=axes,
        orientation="horizontal",
        location="bottom",
        fraction=0.04,
        shrink=0.55,
        aspect=42,
    )
    bar.set_label(
        "Component score (0 absent, 0.5 partial, 1 complete; n/a unknown)",
        fontsize=HEATMAP_TICK_SIZE,
    )
    bar.set_ticks([0, 0.5, 1])
    bar.ax.tick_params(labelsize=HEATMAP_TICK_SIZE)
    bar.outline.set_visible(False)
    save(OUT, "component_heatmap", fig)


def discovery_resolution(results: dict[str, Any], root: Path = ROOT) -> None:
    """The 13 scheduling requirement fields at opening, discovery, and resolution."""

    metrics = results["metrics"]
    denominators = results["denominators"]
    rows = read_csv(root / "data/metrics/b7_constraint_completeness.csv")
    incomplete = denominators["scheduling_constraint_discovery"]["trials"]
    columns = (
        f"Specified at opening\n(weighted {100 * metrics['scheduling_opening_weighted_completeness']:.1f}%)",
        f"Surfaced in replies\n({denominators['scheduling_constraint_discovery']['successes']}/{incomplete} incomplete)",
        f"Resolved for the scenario\n({denominators['scheduling_scenario_resolution']['successes']}/{incomplete} incomplete)",
    )
    values = [
        [
            numeric(row["Opening score (0/0.5/1)"]),
            1.0 if row["Identified in discussion?"] == "Yes" else 0.0,
            1.0 if row["Resolved with scenario-specific value?"] == "Yes" else 0.0,
        ]
        for row in rows
    ]
    fig, ax = plt.subplots(figsize=(7.4, 5.6))
    image = score_heatmap(
        ax, values, [row["Requirement field"] for row in rows], columns, rotation=0
    )
    bar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.03)
    bar.set_ticks([0, 0.5, 1], labels=["absent", "partial", "specified"])
    bar.outline.set_visible(False)
    fig.tight_layout()
    save(OUT, "discovery_resolution", fig)


def association_matrix(root: Path) -> None:
    """All 28 descriptive phi coefficients among B2--B9."""

    size = len(TECHNICAL_CODES)
    phi_by_pair: dict[tuple[int, int], float] = {}
    for row in read_csv(root / PAIRWISE_RELATIVE):
        i = TECHNICAL_CODES.index(row["Code A"])
        j = TECHNICAL_CODES.index(row["Code B"])
        phi_by_pair[(i, j)] = float(row["Phi"])
    if set(phi_by_pair) != set(combinations(range(size), 2)):
        raise SystemExit("pairwise associations do not cover every B2--B9 pair")

    array = np.full((size, size), np.nan)
    for (i, j), phi in phi_by_pair.items():
        array[i, j] = array[j, i] = phi
    limit = float(np.nanmax(np.abs(array)))
    fig, ax = plt.subplots(figsize=(6.9, 5.9))
    image = ax.imshow(
        np.ma.masked_invalid(array),
        cmap=DIVERGING_CMAP,
        vmin=-limit,
        vmax=limit,
        aspect="equal",
    )
    ax.set_xticks(range(size), labels=list(TECHNICAL_CODES))
    ax.set_yticks(range(size), labels=list(TECHNICAL_CODES))
    ax.set_xticks(np.arange(size + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(size + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linewidth=0.8)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    for (i, j), phi in sorted(phi_by_pair.items()):
        for row_index, column_index in ((i, j), (j, i)):
            ax.text(
                column_index,
                row_index,
                f"{phi:.2f}".replace("0.", ".").replace("-.", "\u2212."),
                ha="center",
                va="center",
                fontsize=CELL_LABEL_SIZE,
                color="white" if abs(phi) > 0.62 * limit else "#333333",
            )
            if phi >= PHI_THRESHOLD:
                ax.add_patch(
                    Rectangle(
                        (column_index - 0.5, row_index - 0.5),
                        1,
                        1,
                        facecolor="none",
                        edgecolor="#111111",
                        linewidth=1.6,
                    )
                )
    for index in range(size):
        ax.add_patch(
            Rectangle(
                (index - 0.5, index - 0.5),
                1,
                1,
                facecolor="#f2f2f2",
                edgecolor="white",
                linewidth=0.8,
            )
        )
    ax.plot(
        [],
        [],
        marker="s",
        markersize=7,
        markerfacecolor="none",
        markeredgecolor="#111111",
        markeredgewidth=1.6,
        linestyle="none",
        label=f"Pilot attention threshold $\\phi\\geq{PHI_THRESHOLD:.2f}$",
    )
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), handletextpad=0.4)
    bar = fig.colorbar(image, ax=ax, fraction=0.045, pad=0.03)
    bar.set_label("Descriptive $\\phi$")
    bar.outline.set_visible(False)
    fig.tight_layout()
    save(OUT, "associations", fig)


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
                "quantitative": row["Evidence status"] == QUANTITATIVE,
                "wilson": (
                    None
                    if rate is None
                    else (numeric(row["95% Wilson low"]), numeric(row["95% Wilson high"]))
                ),
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


def validation_funnel(root: Path = ROOT) -> None:
    """Separate a quantitative rate from qualitative report and from silence.

    A stage without a denominator is drawn as a hatched band across the axis
    rather than as a bar at 100%, so that ``reported'' can never be read as a
    measured success rate.
    """

    stages = _funnel_stages(root)
    limit = 1.42
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    positions = range(len(stages))
    for position, stage in zip(positions, stages, strict=True):
        if stage["quantitative"] and stage["rate"] is not None:
            low, high = stage["wilson"] or (None, None)
            ax.barh(position, stage["rate"], height=0.58, color=PALETTE[0], zorder=3)
            annotation_x = stage["rate"]
            if low is not None and high is not None:
                ax.errorbar(
                    stage["rate"],
                    position,
                    xerr=[[stage["rate"] - low], [high - stage["rate"]]],
                    fmt="none",
                    ecolor="#111111",
                    elinewidth=1.1,
                    capsize=3.5,
                    zorder=4,
                )
                annotation_x = high
            ax.text(
                annotation_x + 0.025,
                position,
                f"{int(stage['numerator'] or 0)}/{int(stage['denominator'] or 0)} = "
                f"{100 * stage['rate']:.0f}%\nWilson "
                f"{100 * (low or 0):.0f}\u2013{100 * (high or 0):.0f}%",
                va="center",
                fontsize=7.6,
                zorder=4,
            )
            continue
        # Stages without a denominator are drawn as a band across the whole
        # axis rather than as a bar reaching 100%, so that "reported" cannot be
        # read as a measured success rate.
        reported = stage["reported"]
        ax.barh(
            position,
            limit,
            height=0.58,
            facecolor=PALETTE[5] if reported else "white",
            edgecolor="#9aa5b1",
            hatch="///" if reported else None,
            alpha=0.5 if reported else 1.0,
            zorder=2,
        )
        ax.text(
            limit / 2,
            position,
            "reported qualitatively; no denominator" if reported else "not reported",
            ha="center",
            va="center",
            fontsize=8.0,
            color="#333333",
            zorder=4,
        )

    ax.set_yticks(list(positions), labels=[stage["label"] for stage in stages])
    ax.invert_yaxis()
    ax.set_xlim(0, limit)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0], labels=["0%", "25%", "50%", "75%", "100%"])
    unreported = [stage["label"] for stage in stages if not stage["reported"]]
    label = "Reported agreement rate with 95% Wilson interval"
    if unreported:
        label += f"; no {_join_labels(unreported)} rate reported"
    ax.set_xlabel(label)
    ax.grid(axis="x", zorder=0)
    fig.tight_layout()
    save(OUT, "validation_funnel", fig)


def alignment_matrix(root: Path) -> None:
    """The five alignment elements for each of the six bounded B8 claims."""

    rows = read_csv(root / "data/metrics/b8_test_claim_alignment.csv")
    values = [[numeric(row[element]) for element in B8_ELEMENTS] for row in rows]
    labels = [f"{row['Case']}  ({row['Alignment class'].lower()})" for row in rows]
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    image = score_heatmap(ax, values, labels, list(B8_ELEMENTS))
    ax.tick_params(axis="x", labelrotation=25)
    bar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.03)
    bar.set_ticks([0, 0.5, 1], labels=["absent", "partial", "explicit"])
    bar.outline.set_visible(False)
    fig.tight_layout()
    save(OUT, "b8_alignment_matrix", fig)


def preflight_preventability(results: dict[str, Any], root: Path = ROOT) -> None:
    """Scenario detectability classes beside the rate, interval, and bounds."""

    metrics = results["metrics"]
    denominators = results["denominators"]
    rows = read_csv(root / "data/metrics/b6_preflight_preventability.csv")
    rate = metrics["preflight_preventability_complete_case"]
    wilson_low, wilson_high = metrics["preflight_preventability_complete_case_wilson"]
    sensitivity_low, sensitivity_high = metrics["preflight_preventability_sensitivity"]

    # Stacked rather than side by side: the scenario labels are long, and a
    # two-column layout would only fit inside the text width at unreadable type.
    fig, (left, right) = plt.subplots(
        2,
        1,
        figsize=(6.6, 5.0),
        gridspec_kw={"height_ratios": [1.6, 1.0]},
        layout="constrained",
    )
    for position, row in enumerate(rows):
        detectability = row["Preflight detectability"]
        left.barh(
            position,
            1.0,
            height=0.6,
            color=DETECTABILITY_COLORS[detectability],
            alpha=0.85,
            zorder=3,
        )
        left.text(
            0.02,
            position,
            f"Preflight detectable: {detectability.lower()}",
            va="center",
            fontsize=8.0,
            color=DETECTABILITY_TEXT_COLORS[detectability],
            zorder=4,
        )
    left.set_yticks(
        range(len(rows)),
        labels=[f"{row['Failure class']}\n({row['Thread']})" for row in rows],
    )
    left.invert_yaxis()
    left.set_xlim(0, 1)
    left.set_xticks([])
    left.spines["bottom"].set_visible(False)
    panel_label(left, f"Eligible partial-execution scenarios (n={len(rows)})")

    right.axvspan(
        100 * sensitivity_low,
        100 * sensitivity_high,
        color=PALETTE[4],
        alpha=0.22,
        zorder=1,
        label="Sensitivity bounds for the indeterminate scenario",
    )
    right.errorbar(
        [100 * rate],
        [0],
        xerr=[[100 * (rate - wilson_low)], [100 * (wilson_high - rate)]],
        fmt="o",
        color=PALETTE[0],
        ecolor=PALETTE[0],
        elinewidth=1.3,
        capsize=4,
        zorder=3,
        label="Complete-case rate with 95% Wilson interval",
    )
    counts = denominators["preflight_preventability_complete_case"]
    right.annotate(
        f"{counts['successes']}/{counts['trials']} definite scenarios",
        xy=(100 * rate, 0),
        xytext=(100 * rate, 0.42),
        ha="center",
        fontsize=8.0,
    )
    right.set_xlim(0, 100)
    right.set_ylim(-0.6, 0.85)
    right.set_yticks([])
    right.spines["left"].set_visible(False)
    right.set_xlabel("Preflight Preventability Rate (%)")
    right.grid(axis="x", zorder=0)
    panel_label(right, "Complete-case rate, interval, and sensitivity")
    handles, labels = right.get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside lower center", ncols=1, frameon=False)
    save(OUT, "b6_preflight_preventability", fig)


def main() -> None:
    apply_style()
    results = compute_release_results(ROOT)
    conceptual_model()
    study_workflow(results)
    component_heatmap(ROOT)
    discovery_resolution(results)
    association_matrix(ROOT)
    validation_funnel()
    alignment_matrix(ROOT)
    preflight_preventability(results)


if __name__ == "__main__":
    main()
