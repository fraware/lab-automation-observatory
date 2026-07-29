#!/usr/bin/env python3
"""Build the boundary-centered graphical abstract.

The layers come from the single taxonomy specification in ``figure_style``, so
this asset and the conceptual-model figure cannot drift apart. Unlike the manuscript figures, the graphical
abstract keeps an in-figure title because it is a standalone submission asset
with no caption. Output metadata is suppressed so that repeated runs on a
pinned environment produce byte-identical files.
"""

from pathlib import Path

import matplotlib.pyplot as plt

from figure_style import apply_style, draw_taxonomy

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PNG = ROOT / "paper" / "graphical_abstract.png"
OUTPUT_PDF = ROOT / "paper" / "graphical_abstract.pdf"
TITLE = "Boundary-centered model of public laboratory-automation bottlenecks"


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=(12, 5.3))
    draw_taxonomy(
        ax,
        title=TITLE,
        title_size=18.0,
        layer_title_size=15.0,
        entry_size=11.5,
        note_size=10.5,
    )
    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PNG, dpi=180, bbox_inches="tight", metadata={"Software": None})
    fig.savefig(OUTPUT_PDF, bbox_inches="tight", metadata={"CreationDate": None})
    plt.close(fig)


if __name__ == "__main__":
    main()
