"""Project the hard-case adjudication set onto a blind coder sheet.

``data/derived/reliability_subset.csv`` is one table holding both the material a
second coder needs and the answer key: ``Expected primary``, ``Plausible
alternative``, and ``Why disagreement is likely`` sit in the same row as the
source URL and the adjudication question. A coder cannot reach the thread
without reading the expected code, so no pass over that file can support an
agreement statistic. ``artifacts/adjudication_pilot_v0.1.2.md`` records this as
finding F1.

This module keeps the key exactly as published and derives the coder-facing
projection ``data/derived/reliability_subset_blind.csv`` from it. Column order
follows the pilot's recommendation rather than the key's own order: the coder
first learns which thread to read and how much of it, then the question to
answer, then how many episodes the segmentation is expected to yield. No cell is
authored here, so the
blind sheet cannot state anything the key does not, and
:func:`blind_subset_drift` fails ``make validate`` if the committed projection
falls out of step with the key.
"""

from __future__ import annotations

import csv
import io
from pathlib import Path

from .io import normalised_newlines, read_csv, read_text_lf

SUBSET_RELATIVE = "data/derived/reliability_subset.csv"
BLIND_RELATIVE = "data/derived/reliability_subset_blind.csv"

# Coder-facing columns, in the order a second coder needs them.
BLIND_COLUMNS: tuple[str, ...] = (
    "Thread ID",
    "Thread",
    "Source URL",
    "Read scope",
    "Specific adjudication question",
    "Episode segmentation required",
    "Priority",
)

# Answer-key columns. These are what makes the key unusable for a blind pass, so
# the projection must never carry them and a test asserts the disjointness.
WITHHELD_COLUMNS: tuple[str, ...] = (
    "Expected primary",
    "Plausible alternative",
    "Why disagreement is likely",
)


def build_records(root: str | Path) -> list[dict[str, str]]:
    """Project every key row onto the coder-facing columns, in file order."""

    rows = read_csv(Path(root) / SUBSET_RELATIVE)
    if not rows:
        raise ValueError(f"the adjudication set is empty: {SUBSET_RELATIVE}")
    missing = [column for column in BLIND_COLUMNS if column not in rows[0]]
    if missing:
        raise ValueError(f"{SUBSET_RELATIVE} is missing coder-facing columns: {missing}")
    return [{column: row[column] for column in BLIND_COLUMNS} for row in rows]


def render_blind_csv(root: str | Path) -> str:
    """Render the blind coder sheet exactly as it is committed."""

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(BLIND_COLUMNS), lineterminator="\n")
    writer.writeheader()
    writer.writerows(build_records(root))
    return buffer.getvalue()


def write_blind_csv(root: str | Path) -> Path:
    """Write the regenerated blind coder sheet and return its path."""

    destination = Path(root) / BLIND_RELATIVE
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_blind_csv(root), encoding="utf-8", newline="")
    return destination


def blind_subset_drift(root: str | Path) -> list[str]:
    """Report whether the committed blind sheet still matches the key."""

    destination = Path(root) / BLIND_RELATIVE
    if not destination.is_file():
        return [f"{BLIND_RELATIVE} is missing; run `make derived`"]
    if read_text_lf(destination) != normalised_newlines(render_blind_csv(root)):
        return [f"{BLIND_RELATIVE} has drifted from {SUBSET_RELATIVE}; run `make derived`"]
    return []
