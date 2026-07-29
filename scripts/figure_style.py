"""Shared publication style for every generated figure.

One module owns the print typography, the colourblind-safe palettes, the
deterministic save path, and the taxonomy layer definition. The taxonomy is
drawn from a single specification so that the conceptual-model figure and the
graphical abstract cannot drift apart, and unknown scores are rendered as a
distinct hatched cell so that an unknown can never look like a zero.

Figures carry no redundant in-figure title: the LaTeX caption carries the
interpretation. The graphical abstract is the one exception, because it is a
standalone submission asset with no caption.

This module lives beside the build scripts rather than inside the installed
package, which keeps ``labauto_observatory`` a plotting-free data and metrics
library that the strict type check can cover on its own.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

# Okabe--Ito, which stays distinguishable under the common colour-vision
# deficiencies and in grayscale conversion.
PALETTE: tuple[str, ...] = (
    "#0072B2",
    "#D55E00",
    "#009E73",
    "#CC79A7",
    "#E69F00",
    "#56B4E9",
    "#F0E442",
    "#000000",
)
# Sequential map for bounded 0--1 scores; perceptually uniform and readable when
# printed in grayscale.
SCORE_CMAP = "cividis"
# Diverging map for the descriptive phi matrix, centred on zero.
DIVERGING_CMAP = "RdBu_r"
UNKNOWN_COLOR = "#f2f2f2"
UNKNOWN_HATCH = "///"
UNKNOWN_LABEL = "n/a"
PANEL_LABEL_SIZE = 9.0
CELL_LABEL_SIZE = 6.6

RC_PARAMS: dict[str, Any] = {
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "font.size": 9.0,
    "axes.titlesize": 9.0,
    "axes.titleweight": "bold",
    "axes.labelsize": 9.0,
    "xtick.labelsize": 8.0,
    "ytick.labelsize": 8.0,
    "legend.fontsize": 8.0,
    "legend.frameon": False,
    "axes.linewidth": 0.7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "grid.linewidth": 0.5,
    "grid.alpha": 0.3,
    "lines.linewidth": 1.4,
    "lines.markersize": 4.5,
    "patch.linewidth": 0.7,
    "hatch.linewidth": 0.6,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    # TrueType rather than Type 3, which journal preflight tools reject.
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "axes.prop_cycle": mpl.cycler(color=list(PALETTE)),
}


def apply_style() -> None:
    """Install the shared print style for the current process."""

    mpl.rcParams.update(RC_PARAMS)


def save(out_dir: Path, name: str, fig: Figure | None = None) -> None:
    """Write a figure as vector PDF and raster preview, without timestamps.

    Metadata is suppressed so that repeated runs on the pinned environment
    produce byte-identical files and the committed PDFs stay diff-free.
    """

    figure = plt.gcf() if fig is None else fig
    out_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(out_dir / f"{name}.pdf", bbox_inches="tight", metadata={"CreationDate": None})
    figure.savefig(
        out_dir / f"{name}.png", dpi=220, bbox_inches="tight", metadata={"Software": None}
    )
    plt.close(figure)


def score_label(value: float | None) -> str:
    """Compact cell annotation for a bounded 0/0.5/1 score."""

    if value is None:
        return UNKNOWN_LABEL
    if float(value).is_integer():
        return str(int(value))
    return f"{value:g}".lstrip("0")


def score_heatmap(
    ax: Axes,
    values: Sequence[Sequence[float | None]],
    row_labels: Sequence[str],
    column_labels: Sequence[str],
    *,
    cmap: str = SCORE_CMAP,
    vmin: float = 0.0,
    vmax: float = 1.0,
    annotate: bool = True,
    rotation: float = 40.0,
    cell_label_size: float = CELL_LABEL_SIZE,
) -> AxesImage:
    """Draw a bounded-score matrix, marking unknown cells explicitly.

    Unknown cells are hatched and labelled rather than coloured on the score
    scale, because the release convention is that unknown is not zero.
    """

    # Unknown cells enter as NaN, which matplotlib renders with the colormap's
    # "bad" colour instead of a score colour.
    array = [[float("nan") if value is None else float(value) for value in row] for row in values]
    colormap = mpl.colormaps[cmap].with_extremes(bad=UNKNOWN_COLOR)
    image = ax.imshow(array, cmap=colormap, vmin=vmin, vmax=vmax, aspect="auto")

    ax.set_xticks(
        range(len(column_labels)),
        labels=list(column_labels),
        rotation=rotation,
        ha="right" if rotation else "center",
    )
    ax.set_yticks(range(len(row_labels)), labels=list(row_labels))
    ax.set_xticks([index - 0.5 for index in range(len(column_labels) + 1)], minor=True)
    ax.set_yticks([index - 0.5 for index in range(len(row_labels) + 1)], minor=True)
    ax.grid(which="minor", color="white", linewidth=0.8)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    for row_index, row in enumerate(values):
        for column_index, value in enumerate(row):
            if value is None:
                ax.add_patch(
                    Rectangle(
                        (column_index - 0.5, row_index - 0.5),
                        1,
                        1,
                        facecolor="none",
                        edgecolor="#9a9a9a",
                        hatch=UNKNOWN_HATCH,
                        linewidth=0.0,
                    )
                )
            if not annotate:
                continue
            shade = 0.0 if value is None else (float(value) - vmin) / (vmax - vmin)
            ax.text(
                column_index,
                row_index,
                score_label(value),
                ha="center",
                va="center",
                fontsize=cell_label_size,
                color="#333333" if value is None or shade > 0.55 else "white",
            )
    return image


def panel_label(ax: Axes, text: str, size: float = PANEL_LABEL_SIZE) -> None:
    """Label a panel without repeating the LaTeX caption."""

    ax.set_title(text, loc="left", fontsize=size, pad=6)


@dataclass(frozen=True)
class TaxonomyLayer:
    """One row of the boundary-centered taxonomy diagram."""

    row: int
    x: float
    width: float
    title: str
    entries: tuple[str, ...]


ENTRY_SEPARATOR = "     "
# The single specification behind both the conceptual-model figure and the
# graphical abstract.
TAXONOMY_LAYERS: tuple[TaxonomyLayer, ...] = (
    TaxonomyLayer(
        row=0,
        x=0.0,
        width=1.0,
        title="Ecosystem knowledge and support",
        entries=("B1  Knowledge packaging", "B10  Documentation, training, support"),
    ),
    TaxonomyLayer(
        row=1,
        x=0.0,
        width=1.0,
        title="Interfaces and representations",
        entries=("B2  Device access", "B3  Deployment identity", "B4  Physical resources"),
    ),
    TaxonomyLayer(
        row=2,
        x=0.0,
        width=1.0,
        title="Runtime coordination",
        entries=("B5  Observability", "B6  Recovery", "B7  Scheduling"),
    ),
    TaxonomyLayer(
        row=3,
        x=0.0,
        width=0.62,
        title="Evaluation",
        entries=("B8  Test\u2013claim alignment",),
    ),
    TaxonomyLayer(
        row=3,
        x=0.66,
        width=0.34,
        title="Emerging AI",
        entries=("B9  Context and physical feedback",),
    ),
)
TAXONOMY_NOTE = (
    "The model organizes analytical constructs; "
    "it does not claim exhaustiveness or population prevalence."
)
# Deepest layer first, so the fill darkens downward and the hierarchy survives
# grayscale printing.
LAYER_SHADES: tuple[str, ...] = ("#dce9f4", "#c6dcee", "#b0cfe8", "#9ac2e2")


def draw_taxonomy(
    ax: Axes,
    *,
    title: str | None = None,
    title_size: float = 12.0,
    layer_title_size: float = 10.5,
    entry_size: float = 8.4,
    note_size: float = 8.0,
) -> None:
    """Draw the layered taxonomy in axes fractions from the shared specification."""

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    rows = max(layer.row for layer in TAXONOMY_LAYERS) + 1
    top = 0.90 if title else 0.98
    bottom = 0.10
    pitch = (top - bottom) / rows
    height = pitch * 0.78

    def row_bottom(row: int) -> float:
        return top - pitch * (row + 1) + (pitch - height) / 2

    for layer in TAXONOMY_LAYERS:
        y = row_bottom(layer.row)
        ax.add_patch(
            FancyBboxPatch(
                (layer.x, y),
                layer.width,
                height,
                boxstyle="round,pad=0.004,rounding_size=0.012",
                facecolor=LAYER_SHADES[layer.row],
                edgecolor="#7f8c99",
                linewidth=0.9,
            )
        )
        ax.text(
            layer.x + 0.014,
            y + height * 0.66,
            layer.title,
            fontsize=layer_title_size,
            fontweight="bold",
            va="center",
        )
        ax.text(
            layer.x + 0.014,
            y + height * 0.26,
            ENTRY_SEPARATOR.join(layer.entries),
            fontsize=entry_size,
            va="center",
        )

    for row in range(rows - 1):
        ax.add_patch(
            FancyArrowPatch(
                (0.5, row_bottom(row)),
                (0.5, row_bottom(row + 1) + height),
                arrowstyle="-|>",
                mutation_scale=11,
                linewidth=0.9,
                color="#44515e",
            )
        )

    if title:
        ax.text(0.5, 0.955, title, ha="center", va="center", fontsize=title_size, fontweight="bold")
    ax.text(0.5, 0.035, TAXONOMY_NOTE, ha="center", va="center", fontsize=note_size)
