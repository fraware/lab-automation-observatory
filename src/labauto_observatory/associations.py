"""Rebuild the pairwise association table from the evidence register.

``data/metrics/pairwise_associations.csv`` used to be an independent workbook
export, which made the register and the table two sources of truth for the same
counts. Everything numeric in the table is now derived here from
``data/derived/evidence_register_part_*.csv``, and only the coder-authored
relationship class, interpretation, and prohibited reading are read from
``data/derived/association_annotations.csv``. Every one of the 28 B2--B9 pairs
must be annotated, so a new pair cannot silently acquire a blank reading.
"""

from __future__ import annotations

import csv
import io
from itertools import combinations
from pathlib import Path

from .io import normalised_newlines, read_csv, read_csv_many, read_text_lf
from .metrics import association_from_counts, phi_with_shifted_overlap

TECHNICAL_CODES: tuple[str, ...] = tuple(f"B{index}" for index in range(2, 10))
PHI_THRESHOLD = 0.30
LIFT_THRESHOLD = 1.50

PAIRWISE_RELATIVE = "data/metrics/pairwise_associations.csv"
ANNOTATIONS_RELATIVE = "data/derived/association_annotations.csv"
REGISTER_GLOB = "evidence_register_part_*.csv"

# "Phi if overlap -1" uses U+2212 MINUS SIGN, matching the released header.
HEADER: tuple[str, ...] = (
    "Rank order",
    "Code A",
    "Code B",
    "N(A)",
    "N(B)",
    "Overlap",
    "Union",
    "Jaccard",
    "Lift",
    "Phi",
    "P(B|A)",
    "P(B|not A)",
    "Descriptive RR",
    "Phi if overlap \u22121",
    "Phi if overlap +1",
    "Sensitivity width",
    "Pilot threshold met?",
    "Relationship class",
    "Interpretation",
    "Invalid inference",
)
ANNOTATION_COLUMNS: tuple[str, ...] = (
    "Code A",
    "Code B",
    "Relationship class",
    "Interpretation",
    "Invalid inference",
)


def read_register(root: str | Path) -> list[dict[str, str]]:
    """Read the concatenated evidence register parts in file order."""

    parts = sorted((Path(root) / "data/derived").glob(REGISTER_GLOB))
    if not parts:
        raise FileNotFoundError(f"no evidence register parts under {root}")
    return read_csv_many(list(parts))


def read_annotations(root: str | Path) -> dict[tuple[str, str], dict[str, str]]:
    """Read the coder-authored reading for each ordered code pair."""

    rows = read_csv(Path(root) / ANNOTATIONS_RELATIVE)
    if not rows:
        raise ValueError(f"association annotations are empty: {ANNOTATIONS_RELATIVE}")
    missing = [column for column in ANNOTATION_COLUMNS if column not in rows[0]]
    if missing:
        raise ValueError(f"association annotations are missing columns: {missing}")
    return {(row["Code A"], row["Code B"]): row for row in rows}


def supporting_ids(rows: list[dict[str, str]], code: str) -> set[str]:
    """Thread identifiers whose direct-support flag for ``code`` is set."""

    return {row["ID"] for row in rows if int(row[code]) == 1}


def contingency(rows: list[dict[str, str]], code_a: str, code_b: str) -> tuple[int, int, int, int]:
    """Two-by-two direct-support table ``(n11, n10, n01, n00)`` over all threads."""

    support_a = supporting_ids(rows, code_a)
    support_b = supporting_ids(rows, code_b)
    n11 = len(support_a & support_b)
    return n11, len(support_a) - n11, len(support_b) - n11, len(rows) - len(support_a | support_b)


def format_number(value: float | None) -> str:
    """Render a measure the way the release CSV does: blank when undefined."""

    if value is None:
        return ""
    if float(value).is_integer():
        return str(int(value))
    return repr(float(value))


def build_records(root: str | Path) -> list[dict[str, str]]:
    """Build the 28 B2--B9 association rows, ranked by descending phi."""

    rows = read_register(root)
    annotations = read_annotations(root)
    pairs = list(combinations(TECHNICAL_CODES, 2))
    unannotated = [pair for pair in pairs if pair not in annotations]
    if unannotated:
        raise ValueError(f"association annotations are missing pairs: {unannotated}")

    computed = []
    for code_a, code_b in pairs:
        counts = contingency(rows, code_a, code_b)
        association = association_from_counts(*counts)
        phi_low = phi_with_shifted_overlap(*counts, -1)
        phi_high = phi_with_shifted_overlap(*counts, 1)
        width = None if phi_low is None or phi_high is None else phi_high - phi_low
        computed.append((code_a, code_b, counts, association, phi_low, phi_high, width))

    computed.sort(key=lambda entry: (-entry[3].phi, entry[0], entry[1]))

    records: list[dict[str, str]] = []
    for rank, (code_a, code_b, counts, association, phi_low, phi_high, width) in enumerate(
        computed, start=1
    ):
        n11, n10, n01, _ = counts
        annotation = annotations[(code_a, code_b)]
        threshold_met = association.phi >= PHI_THRESHOLD and association.lift >= LIFT_THRESHOLD
        records.append(
            {
                "Rank order": str(rank),
                "Code A": code_a,
                "Code B": code_b,
                "N(A)": str(n11 + n10),
                "N(B)": str(n11 + n01),
                "Overlap": str(n11),
                "Union": str(n11 + n10 + n01),
                "Jaccard": format_number(association.jaccard),
                "Lift": format_number(association.lift),
                "Phi": format_number(association.phi),
                "P(B|A)": format_number(association.p_b_given_a),
                "P(B|not A)": format_number(association.p_b_given_not_a),
                "Descriptive RR": format_number(association.descriptive_risk_ratio),
                "Phi if overlap \u22121": format_number(phi_low),
                "Phi if overlap +1": format_number(phi_high),
                "Sensitivity width": format_number(width),
                "Pilot threshold met?": "Yes" if threshold_met else "No",
                "Relationship class": annotation["Relationship class"],
                "Interpretation": annotation["Interpretation"],
                "Invalid inference": annotation["Invalid inference"],
            }
        )
    return records


def render_pairwise_csv(root: str | Path) -> str:
    """Render the pairwise association CSV exactly as it is committed."""

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(HEADER), lineterminator="\n")
    writer.writeheader()
    writer.writerows(build_records(root))
    return buffer.getvalue()


def write_pairwise_csv(root: str | Path) -> Path:
    """Write the regenerated pairwise association CSV and return its path."""

    destination = Path(root) / PAIRWISE_RELATIVE
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_pairwise_csv(root), encoding="utf-8", newline="")
    return destination


def pairwise_drift(root: str | Path) -> list[str]:
    """Report whether the committed table still matches the register."""

    destination = Path(root) / PAIRWISE_RELATIVE
    if not destination.is_file():
        return [f"{PAIRWISE_RELATIVE} is missing; run `make derived`"]
    if read_text_lf(destination) != normalised_newlines(render_pairwise_csv(root)):
        return [f"{PAIRWISE_RELATIVE} has drifted from the evidence register; run `make derived`"]
    return []
