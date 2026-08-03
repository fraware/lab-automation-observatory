"""Traceability between the publication claim ledger and the manuscript.

Every approved claim in ``data/derived/publication_claim_ledger.csv`` must be
locatable in the LaTeX sources. Two independent bindings are required:

1. a ``% claim: Cxx`` marker placed next to the supporting passage, which gives
   a reviewable location for the claim; and
2. the claim's ``Manuscript anchor`` -- a distinctive substring of the published
   wording -- which must appear in the body text of a file carrying that marker.

The anchor is matched against body text only. LaTeX comments are stripped first
so that a marker or an editorial note can never satisfy an anchor.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .io import read_csv

APPROVED_STATUS = "Approved"
CLAIM_ID_COLUMN = "Claim ID"
STATUS_COLUMN = "Status"
ANCHOR_COLUMN = "Manuscript anchor"
LEDGER_RELATIVE = "data/derived/publication_claim_ledger.csv"
MANUSCRIPT_RELATIVE = ("paper/main.tex", "paper/supplement.tex")
MANUSCRIPT_GLOB = "paper/sections/*.tex"

_CLAIM_ID = re.compile(r"\AC\d{2}\Z")
_MARKER = re.compile(r"^[ \t]*%+[ \t]*claim:(?P<ids>[^\n]*)$", re.IGNORECASE | re.MULTILINE)
_MARKER_SEPARATOR = re.compile(r"[,;\s]+")
_UNESCAPED_PERCENT = re.compile(r"(?<!\\)%")
_WHITESPACE = re.compile(r"\s+")


@dataclass(frozen=True)
class Claim:
    """One row of the publication claim ledger."""

    claim_id: str
    status: str
    anchor: str

    @property
    def approved(self) -> bool:
        return self.status == APPROVED_STATUS


@dataclass(frozen=True)
class ClaimTrace:
    """Where a single claim was found in the manuscript sources."""

    claim: Claim
    marker_files: tuple[str, ...]
    anchor_files: tuple[str, ...]


@dataclass(frozen=True)
class TraceabilityReport:
    """Outcome of a claim-ledger to manuscript traceability check."""

    traces: tuple[ClaimTrace, ...]
    problems: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.problems

    @property
    def approved(self) -> tuple[ClaimTrace, ...]:
        return tuple(trace for trace in self.traces if trace.claim.approved)


def strip_latex_comments(text: str) -> str:
    """Remove LaTeX comments while preserving escaped percent signs."""

    lines = []
    for line in text.splitlines():
        match = _UNESCAPED_PERCENT.search(line)
        lines.append(line if match is None else line[: match.start()])
    return "\n".join(lines)


def normalize(text: str) -> str:
    """Collapse whitespace so that line-wrapped prose still matches an anchor."""

    return _WHITESPACE.sub(" ", text).strip()


def read_claims(ledger: str | Path) -> list[Claim]:
    """Read the claim ledger, requiring the traceability columns to be present."""

    rows = read_csv(ledger)
    if not rows:
        raise ValueError(f"claim ledger is empty: {ledger}")
    for column in (CLAIM_ID_COLUMN, STATUS_COLUMN, ANCHOR_COLUMN):
        if column not in rows[0]:
            raise ValueError(f"claim ledger is missing the {column!r} column: {ledger}")
    return [
        Claim(
            claim_id=row[CLAIM_ID_COLUMN].strip(),
            status=row[STATUS_COLUMN].strip(),
            anchor=row[ANCHOR_COLUMN].strip(),
        )
        for row in rows
    ]


def manuscript_tree_present(root: str | Path) -> bool:
    """Return True when the manuscript tree is available for checks."""

    root_path = Path(root)
    return all((root_path / relative).is_file() for relative in MANUSCRIPT_RELATIVE)


def manuscript_sources(root: str | Path) -> list[Path]:
    """Return the manuscript files that participate in claim traceability."""

    root_path = Path(root)
    sources = [root_path / relative for relative in MANUSCRIPT_RELATIVE]
    sources.extend(sorted(root_path.glob(MANUSCRIPT_GLOB)))
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"manuscript sources not found: {missing}")
    return sources


def find_markers(text: str) -> list[str]:
    """Extract claim identifiers from ``% claim: Cxx`` markers in one source."""

    found: list[str] = []
    for match in _MARKER.finditer(text):
        for token in _MARKER_SEPARATOR.split(match.group("ids").strip()):
            if token:
                found.append(token.upper())
    return found


def check_traceability(root: str | Path) -> TraceabilityReport:
    """Check that every approved claim is bound to the manuscript sources."""

    root_path = Path(root)
    claims = read_claims(root_path / LEDGER_RELATIVE)
    problems: list[str] = []

    by_id: dict[str, Claim] = {}
    for claim in claims:
        if not _CLAIM_ID.match(claim.claim_id):
            problems.append(f"ledger claim identifier is malformed: {claim.claim_id!r}")
        if claim.claim_id in by_id:
            problems.append(f"ledger contains duplicate claim identifier {claim.claim_id}")
        by_id[claim.claim_id] = claim

    markers: dict[str, list[str]] = {claim_id: [] for claim_id in by_id}
    bodies: dict[str, str] = {}
    for source in manuscript_sources(root_path):
        relative = source.relative_to(root_path).as_posix()
        text = source.read_text(encoding="utf-8")
        bodies[relative] = normalize(strip_latex_comments(text))
        for claim_id in find_markers(text):
            if claim_id not in by_id:
                problems.append(f"{relative} marks unknown claim {claim_id}")
                continue
            if relative not in markers[claim_id]:
                markers[claim_id].append(relative)

    traces: list[ClaimTrace] = []
    for claim_id, claim in by_id.items():
        marker_files = tuple(markers[claim_id])
        anchor = normalize(claim.anchor)
        anchor_files = tuple(
            sorted(name for name, body in bodies.items() if anchor and anchor in body)
        )
        traces.append(ClaimTrace(claim=claim, marker_files=marker_files, anchor_files=anchor_files))

        if not claim.approved:
            if marker_files:
                problems.append(
                    f"claim {claim_id} has status {claim.status!r} but is marked in {list(marker_files)}"
                )
            if claim.anchor:
                problems.append(
                    f"claim {claim_id} has status {claim.status!r} and must not declare a manuscript anchor"
                )
            continue

        if not marker_files:
            problems.append(
                f"approved claim {claim_id} has no '% claim: {claim_id}' marker in the manuscript"
            )
        if not claim.anchor:
            problems.append(f"approved claim {claim_id} has no manuscript anchor in the ledger")
            continue
        if not anchor_files:
            problems.append(
                f"approved claim {claim_id} anchor is absent from the manuscript: {claim.anchor!r}"
            )
        elif marker_files and not set(anchor_files) & set(marker_files):
            problems.append(
                f"approved claim {claim_id} anchor appears in {list(anchor_files)} "
                f"but its marker is in {list(marker_files)}"
            )

    return TraceabilityReport(traces=tuple(traces), problems=tuple(problems))


def format_report(report: TraceabilityReport) -> str:
    """Render a Markdown traceability table for review artifacts."""

    lines = [
        "# Claim traceability",
        "",
        "| Claim | Status | Marked in | Anchor found in |",
        "|---|---|---|---|",
    ]
    for trace in report.traces:
        marked = ", ".join(trace.marker_files) or "--"
        anchored = ", ".join(trace.anchor_files) or "--"
        lines.append(f"| {trace.claim.claim_id} | {trace.claim.status} | {marked} | {anchored} |")
    lines.extend(["", f"Approved claims traced: {len(report.approved)}", ""])
    if report.problems:
        lines.extend(["## Problems", ""])
        lines.extend(f"- {problem}" for problem in report.problems)
        lines.append("")
    return "\n".join(lines)
