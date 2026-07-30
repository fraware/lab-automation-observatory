"""Structural validation of the committed register and metric CSVs.

``scripts/validate_release.py`` checks schemas, the claim ledger, and claim
traceability. This module checks the tabular release data itself so that a
hand edit cannot silently change a published number:

* every committed CSV has its documented row count;
* score cells only ever contain ``0``, ``0.5``, ``1``, or an empty unknown;
* categorical columns only contain their documented vocabulary;
* every derived score column recomputes from its own component columns;
* the cross-file invariants hold (primary code implies direct support, an
  episode's codes are a subset of its thread's direct-support flags, the
  adjudication set is exactly the episode-segmented subset, each thread's
  expected episode count matches the episode register, the B8 alignment class
  agrees with numerator eligibility, and the funnel's Wilson columns agree with
  :func:`labauto_observatory.metrics.wilson_interval`);
* the generated ``pairwise_associations.csv``, ``evidence_atlas.csv``,
  ``reliability_subset_blind.csv``, and
  ``docs/generated/evidence_atlas_summary.md`` have not drifted from the
  sources they are built from;
* the device-interface registry seeds satisfy their schema and their own
  invariants (see :mod:`labauto_observatory.registry`).

Checks return problem strings rather than raising so that one run reports every
failure it can find.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from math import isclose
from pathlib import Path

from .analysis import (
    B2_COMPONENTS,
    B3_COMPONENTS,
    B4_COMPONENTS,
    B5_COMPONENTS,
    B8_ELEMENTS,
    B10_SUBTYPES,
    CODES,
    OPENING_SCORE_COLUMN,
)
from .associations import pairwise_drift
from .atlas import atlas_drift
from .atlas_summary import atlas_summary_drift
from .blind_subset import blind_subset_drift
from .io import integer, numeric, read_csv, read_csv_many
from .metrics import wilson_interval
from .registry import check_registry_examples
from .run_events import check_example_streams

SCORE_VALUES: frozenset[float] = frozenset({0.0, 0.5, 1.0})
TOLERANCE = 1e-9

EXPECTED_ROW_COUNTS: dict[str, int] = {
    "data/derived/association_annotations.csv": 28,
    "data/derived/codebook.csv": 13,
    "data/derived/episode_register_part_01.csv": 23,
    "data/derived/episode_register_part_02.csv": 22,
    "data/derived/evidence_atlas.csv": 10,
    "data/derived/evidence_register_part_01.csv": 28,
    "data/derived/evidence_register_part_02.csv": 27,
    "data/derived/hypothesis_map.csv": 8,
    "data/derived/negative_cases.csv": 10,
    "data/derived/publication_claim_ledger.csv": 12,
    "data/derived/quote_bank.csv": 20,
    "data/derived/source_quote_audit.csv": 24,
    "data/derived/reliability_subset.csv": 14,
    "data/derived/reliability_subset_blind.csv": 14,
    "data/derived/taxonomy_rules.csv": 10,
    "data/derived/troubleshooting_template.csv": 25,
    "data/knowledge_index/schema_fields.csv": 18,
    "data/knowledge_index/seed_records.csv": 10,
    "data/metrics/ai_validation_funnel.csv": 7,
    "data/metrics/b10_documentation_profile.csv": 12,
    "data/metrics/b2_b10_matched_cases.csv": 5,
    "data/metrics/b2_integration_access.csv": 6,
    "data/metrics/b3_reproducibility_manifest.csv": 3,
    "data/metrics/b4_physical_definitions.csv": 4,
    "data/metrics/b5_observability.csv": 4,
    "data/metrics/b6_preflight_preventability.csv": 4,
    "data/metrics/b7_constraint_completeness.csv": 13,
    "data/metrics/b8_test_claim_alignment.csv": 6,
    "data/metrics/b9_context_expansion.csv": 22,
    "data/metrics/pairwise_associations.csv": 28,
    "data/metrics/strong_relationships.csv": 5,
}

EXPECTED_THREADS = 55
EXPECTED_EPISODES = 45
EXPECTED_EPISODE_THREADS = 14

# "Yes — 3 episodes: ..." with the released em dash. The count is what a second
# segmentation can contradict; the trailing prose is a thematic hint.
SEGMENTATION_TARGET = re.compile(r"^Yes\s+\u2014\s+(\d+) episodes\b")
# A post anchor is the thread URL followed by the post number, not `?page=N`.
POST_ANCHOR = re.compile(r"^https://\S+/\d+/\d+$")

YES_NO = frozenset({"Yes", "No"})
YES_PARTIAL_NO = frozenset({"Yes", "Partial", "No"})
EVIDENCE_STRENGTHS = frozenset({1, 2, 3, 4})

# Score columns keyed by the file they belong to, with the derived score column
# each set of components must reproduce.
SCORE_BLOCKS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("data/metrics/b2_integration_access.csv", B2_COMPONENTS, "IAS"),
    ("data/metrics/b3_reproducibility_manifest.csv", B3_COMPONENTS, "RMC"),
    ("data/metrics/b4_physical_definitions.csv", B4_COMPONENTS, "PDC"),
    ("data/metrics/b5_observability.csv", B5_COMPONENTS, "OC"),
    ("data/metrics/b8_test_claim_alignment.csv", B8_ELEMENTS, "Element mean"),
    ("data/metrics/b10_documentation_profile.csv", B10_SUBTYPES, ""),
)

CATEGORICAL_COLUMNS: tuple[tuple[str, str, frozenset[str]], ...] = (
    ("data/metrics/b2_integration_access.csv", "Positive case", YES_NO),
    (
        "data/metrics/b6_preflight_preventability.csv",
        "Preflight detectability",
        frozenset({"Yes", "No", "Indeterminate"}),
    ),
    (
        "data/metrics/b7_constraint_completeness.csv",
        "Present at opening?",
        frozenset({"Yes", "Partial", "No"}),
    ),
    ("data/metrics/b7_constraint_completeness.csv", "Identified in discussion?", YES_NO),
    (
        "data/metrics/b7_constraint_completeness.csv",
        "Resolved with scenario-specific value?",
        YES_NO,
    ),
    ("data/metrics/b7_constraint_completeness.csv", "Required for evaluation?", YES_NO),
    (
        "data/metrics/b8_test_claim_alignment.csv",
        "Alignment class",
        frozenset({"Aligned", "Partial", "Incomplete"}),
    ),
    ("data/metrics/b8_test_claim_alignment.csv", "Numerator eligibility", YES_NO),
    ("data/metrics/b9_context_expansion.csv", "Origin", frozenset({"Initial", "Reply-added"})),
    ("data/metrics/b9_context_expansion.csv", "Core execution scope?", YES_NO),
    ("data/metrics/b9_context_expansion.csv", "Broader deployment scope?", YES_NO),
    ("data/metrics/b9_context_expansion.csv", "Counted in conservative grouping?", YES_NO),
    (
        "data/metrics/b10_documentation_profile.csv",
        "Actionable public resolution",
        YES_PARTIAL_NO,
    ),
    ("data/metrics/b10_documentation_profile.csv", "Private migration", YES_PARTIAL_NO),
)


@dataclass(frozen=True)
class DataReport:
    """Outcome of a release-data validation run."""

    checked_files: tuple[str, ...]
    problems: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.problems


def _register(root: Path) -> list[dict[str, str]]:
    return read_csv_many(sorted((root / "data/derived").glob("evidence_register_part_*.csv")))


def _episodes(root: Path) -> list[dict[str, str]]:
    return read_csv_many(sorted((root / "data/derived").glob("episode_register_part_*.csv")))


def _codes(cell: str) -> list[str]:
    """Split a semicolon-separated code list, tolerating an empty cell."""

    return [code.strip() for code in cell.split(";") if code.strip()]


def check_row_counts(root: Path) -> list[str]:
    problems: list[str] = []
    for relative, expected in EXPECTED_ROW_COUNTS.items():
        path = root / relative
        if not path.is_file():
            problems.append(f"{relative}: required release file is missing")
            continue
        actual = len(read_csv(path))
        if actual != expected:
            problems.append(f"{relative}: expected {expected} rows, found {actual}")
    return problems


def check_score_cells(root: Path) -> list[str]:
    """Score cells hold only 0, 0.5, 1, or an empty unknown."""

    problems: list[str] = []
    for relative, columns, _ in SCORE_BLOCKS:
        for index, row in enumerate(read_csv(root / relative), start=2):
            for column in columns:
                if column not in row:
                    problems.append(f"{relative}: missing score column {column!r}")
                    continue
                value = numeric(row[column])
                if value is not None and value not in SCORE_VALUES:
                    problems.append(
                        f"{relative} line {index}: {column!r} is {row[column]!r}, "
                        "not 0, 0.5, 1, or empty"
                    )
    return problems


def check_derived_scores(root: Path) -> list[str]:
    """Each derived score column is the mean over its known component cells."""

    problems: list[str] = []
    for relative, columns, score_column in SCORE_BLOCKS:
        if not score_column:
            continue
        for index, row in enumerate(read_csv(root / relative), start=2):
            known = [
                value for value in (numeric(row[column]) for column in columns) if value is not None
            ]
            stored = numeric(row[score_column])
            if not known:
                problems.append(f"{relative} line {index}: no known component scores")
                continue
            expected = sum(known) / len(known)
            if stored is None or not isclose(stored, expected, abs_tol=TOLERANCE):
                problems.append(
                    f"{relative} line {index}: {score_column!r} is {row[score_column]!r} "
                    f"but the known-component mean is {expected!r}"
                )
    return problems


def check_categoricals(root: Path) -> list[str]:
    problems: list[str] = []
    for relative, column, allowed in CATEGORICAL_COLUMNS:
        for index, row in enumerate(read_csv(root / relative), start=2):
            if column not in row:
                problems.append(f"{relative}: missing categorical column {column!r}")
                break
            if row[column] not in allowed:
                problems.append(
                    f"{relative} line {index}: {column!r} is {row[column]!r}, "
                    f"not one of {sorted(allowed)}"
                )
    return problems


def check_evidence_register(root: Path) -> list[str]:
    """Row-level rules and the primary-implies-direct-support invariant."""

    problems: list[str] = []
    rows = _register(root)
    if len(rows) != EXPECTED_THREADS:
        problems.append(
            f"evidence register: expected {EXPECTED_THREADS} threads, found {len(rows)}"
        )

    identifiers = [integer(row["ID"]) for row in rows]
    if sorted(filter(None, identifiers)) != list(range(1, len(rows) + 1)):
        problems.append("evidence register: IDs are not the contiguous range 1..N")

    for row in rows:
        label = f"evidence register thread {row['ID']}"
        for code in CODES:
            if row[code] not in {"0", "1"}:
                problems.append(f"{label}: {code} flag is {row[code]!r}, not 0 or 1")
        if row["Primary"] not in CODES:
            problems.append(f"{label}: primary code {row['Primary']!r} is not a construct")
        elif row[row["Primary"]] != "1":
            problems.append(
                f"{label}: primary code {row['Primary']} has no direct-support flag, "
                "so Primary is not a subset of Direct support"
            )
        if integer(row["Evidence strength"]) not in EVIDENCE_STRENGTHS:
            problems.append(f"{label}: evidence strength {row['Evidence strength']!r} is not 1--4")
        if row["External migration"] not in YES_PARTIAL_NO:
            problems.append(f"{label}: external migration {row['External migration']!r} is invalid")
        if not row["Source URL"].strip():
            problems.append(f"{label}: source URL is empty")
    return problems


def check_episode_and_adjudication_subsets(root: Path) -> list[str]:
    """The adjudication set is exactly the episode-segmented thread subset."""

    problems: list[str] = []
    episodes = _episodes(root)
    adjudication = read_csv(root / "data/derived/reliability_subset.csv")
    register_ids = {row["ID"] for row in _register(root)}

    if len(episodes) != EXPECTED_EPISODES:
        problems.append(
            f"episode register: expected {EXPECTED_EPISODES} episodes, found {len(episodes)}"
        )

    episode_threads = {row["Thread ID"] for row in episodes}
    adjudication_threads = {row["Thread ID"] for row in adjudication}
    if len(episode_threads) != EXPECTED_EPISODE_THREADS:
        problems.append(
            f"episode register: expected {EXPECTED_EPISODE_THREADS} segmented threads, "
            f"found {len(episode_threads)}"
        )
    if episode_threads != adjudication_threads:
        difference = sorted(episode_threads ^ adjudication_threads, key=int)
        problems.append(
            f"the adjudication set and the episode-segmented subset differ on threads {difference}"
        )
    for thread in sorted(episode_threads | adjudication_threads, key=int):
        if thread not in register_ids:
            problems.append(f"thread {thread} is referenced but absent from the evidence register")

    episode_ids = [row["Episode ID"] for row in episodes]
    if len(set(episode_ids)) != len(episode_ids):
        problems.append("episode register: episode IDs are not unique")
    for row in episodes:
        if row["Primary technical code"] not in CODES:
            problems.append(
                f"episode {row['Episode ID']}: primary technical code "
                f"{row['Primary technical code']!r} is not a construct"
            )
    return problems


def check_episode_thread_coherence(root: Path) -> list[str]:
    """An episode's codes are a subset of its thread's direct-support flags.

    An episode is a segment of a thread, so a code the episode evidences is a
    code the thread evidences. Without this check an episode could assert a
    condition that the thread-level flags deny: ``check_evidence_register``
    only ties a thread's own primary code to its own flag, and
    ``check_episode_and_adjudication_subsets`` only checks that an episode code
    is a construct. The pilot found exactly that gap on ``T05-E3``.
    """

    problems: list[str] = []
    threads = {row["ID"]: row for row in _register(root)}
    for episode in _episodes(root):
        thread = threads.get(episode["Thread ID"])
        if thread is None:
            continue
        primary = episode["Primary technical code"]
        claimed = [("primary technical code", primary)] + [
            ("modifier", code) for code in _codes(episode["Ecosystem modifiers"])
        ]
        for role, code in claimed:
            if code in CODES and thread[code] != "1":
                problems.append(
                    f"episode {episode['Episode ID']}: {role} {code} has no direct-support flag "
                    f"on thread {episode['Thread ID']}, so the episode asserts a condition the "
                    "thread-level coding denies"
                )
    return problems


def check_segmentation_targets(root: Path) -> list[str]:
    """Each thread's expected episode count matches the episode register.

    ``Episode segmentation required`` used to say things like "at least three
    episodes", which no segmentation can contradict. The count is now exact, so
    an independent segmentation can disagree with it and a re-segmentation has to
    move both files. Every hard thread also has to declare its coded read scope,
    because a coder who stops at the landing page codes a different thread.
    """

    problems: list[str] = []
    registered = Counter(row["Thread ID"] for row in _episodes(root))
    for row in read_csv(root / "data/derived/reliability_subset.csv"):
        thread = row["Thread ID"]
        target = row["Episode segmentation required"]
        match = SEGMENTATION_TARGET.match(target)
        if match is None:
            problems.append(
                f"adjudication thread {thread}: 'Episode segmentation required' is {target!r}, "
                "which states no exact episode count"
            )
        elif int(match.group(1)) != registered[thread]:
            problems.append(
                f"adjudication thread {thread}: expects {match.group(1)} episodes but the "
                f"episode register holds {registered[thread]}"
            )
        if not row["Read scope"].strip():
            problems.append(f"adjudication thread {thread}: read scope is empty")
    return problems


def check_episode_provenance(root: Path) -> list[str]:
    """``Counterexample to`` names constructs and ``First post anchor`` is a post link.

    The counterexample column used to be a boolean, so an episode could be
    recorded as challenging something without recording what. Both columns may be
    empty -- not every episode is a counterexample, and not every public thread
    exposes a usable post anchor -- but a populated cell has to be checkable.
    """

    problems: list[str] = []
    for row in _episodes(root):
        label = f"episode {row['Episode ID']}"
        for code in _codes(row["Counterexample to"]):
            if code not in CODES:
                problems.append(f"{label}: counterexample scope {code!r} is not a construct")
        anchor = row["First post anchor"].strip()
        if anchor and not POST_ANCHOR.match(anchor):
            problems.append(
                f"{label}: first post anchor {anchor!r} is not a post-anchored discussion URL"
            )
    return problems


def check_b2_component_bookkeeping(root: Path) -> list[str]:
    """``Known-component score`` and ``Unknown components`` describe the row."""

    problems: list[str] = []
    for index, row in enumerate(read_csv(root / "data/metrics/b2_integration_access.csv"), start=2):
        cells = [numeric(row[column]) for column in B2_COMPONENTS]
        known = [value for value in cells if value is not None]
        stored_known = numeric(row["Known-component score"])
        stored_unknown = integer(row["Unknown components"])
        expected = sum(known) / len(known)
        if stored_known is None or not isclose(stored_known, expected, abs_tol=TOLERANCE):
            problems.append(
                f"b2_integration_access.csv line {index}: 'Known-component score' is "
                f"{row['Known-component score']!r} but the known-component mean is {expected!r}"
            )
        if stored_unknown != len(cells) - len(known):
            problems.append(
                f"b2_integration_access.csv line {index}: 'Unknown components' is "
                f"{row['Unknown components']!r} but {len(cells) - len(known)} cells are empty"
            )
    return problems


def check_b3_applicable_fields(root: Path) -> list[str]:
    problems: list[str] = []
    for index, row in enumerate(
        read_csv(root / "data/metrics/b3_reproducibility_manifest.csv"), start=2
    ):
        known = sum(1 for column in B3_COMPONENTS if numeric(row[column]) is not None)
        if integer(row["Applicable fields"]) != known:
            problems.append(
                f"b3_reproducibility_manifest.csv line {index}: 'Applicable fields' is "
                f"{row['Applicable fields']!r} but {known} manifest cells are populated"
            )
    return problems


def check_b7_denominator(root: Path) -> list[str]:
    """The discovery and resolution rates need a non-empty incomplete-field set."""

    problems: list[str] = []
    rows = read_csv(root / "data/metrics/b7_constraint_completeness.csv")
    incomplete = [row for row in rows if (numeric(row[OPENING_SCORE_COLUMN]) or 0.0) < 1]
    if not incomplete:
        problems.append(
            "b7_constraint_completeness.csv: no requirement field scores below 1 at opening, "
            "so the discovery and resolution rates have an empty denominator"
        )
    for row in rows:
        score = numeric(row[OPENING_SCORE_COLUMN])
        if score is None or score not in SCORE_VALUES:
            problems.append(
                f"b7_constraint_completeness.csv: {row['Requirement field']!r} opening score "
                f"{row[OPENING_SCORE_COLUMN]!r} is not 0, 0.5, or 1"
            )
            continue
        present = row["Present at opening?"] != "No"
        if present != (score > 0):
            problems.append(
                f"b7_constraint_completeness.csv: {row['Requirement field']!r} has opening score "
                f"{score} but 'Present at opening?' is {row['Present at opening?']!r}"
            )
    return problems


def check_b8_alignment_eligibility(root: Path) -> list[str]:
    """A fully aligned claim is exactly a numerator-eligible claim."""

    problems: list[str] = []
    for row in read_csv(root / "data/metrics/b8_test_claim_alignment.csv"):
        aligned = row["Alignment class"] == "Aligned"
        eligible = row["Numerator eligibility"] == "Yes"
        if aligned != eligible:
            problems.append(
                f"b8_test_claim_alignment.csv: {row['Case']} has alignment class "
                f"{row['Alignment class']!r} but numerator eligibility "
                f"{row['Numerator eligibility']!r}"
            )
        if aligned and any(numeric(row[element]) != 1 for element in B8_ELEMENTS):
            problems.append(
                f"b8_test_claim_alignment.csv: {row['Case']} is fully aligned but not every "
                "alignment element scores 1"
            )
    return problems


def check_b6_denominator_status(root: Path) -> list[str]:
    problems: list[str] = []
    for row in read_csv(root / "data/metrics/b6_preflight_preventability.csv"):
        indeterminate = row["Preflight detectability"] == "Indeterminate"
        status = row["Denominator status"]
        expected = "Eligible / indeterminate" if indeterminate else "Eligible / definite"
        if status != expected:
            problems.append(
                f"b6_preflight_preventability.csv: detectability {row['Preflight detectability']!r} "
                f"implies denominator status {expected!r}, found {status!r}"
            )
    return problems


def check_funnel_intervals(root: Path) -> list[str]:
    """The funnel's rate and Wilson columns agree with the release code."""

    problems: list[str] = []
    for row in read_csv(root / "data/metrics/ai_validation_funnel.csv"):
        successes = integer(row["Numerator"])
        trials = integer(row["Denominator"])
        rate = numeric(row["Rate"])
        low = numeric(row["95% Wilson low"])
        high = numeric(row["95% Wilson high"])
        label = f"ai_validation_funnel.csv stage {row['Stage']!r}"
        if successes is None or trials is None:
            if rate is not None or low is not None or high is not None:
                problems.append(f"{label}: reports a rate or interval without both counts")
            continue
        expected_low, expected_high = wilson_interval(successes, trials)
        if rate is None or not isclose(rate, successes / trials, abs_tol=TOLERANCE):
            problems.append(f"{label}: rate {row['Rate']!r} does not equal {successes}/{trials}")
        if low is None or not isclose(low, expected_low, abs_tol=TOLERANCE):
            problems.append(f"{label}: Wilson low {row['95% Wilson low']!r} != {expected_low!r}")
        if high is None or not isclose(high, expected_high, abs_tol=TOLERANCE):
            problems.append(f"{label}: Wilson high {row['95% Wilson high']!r} != {expected_high!r}")
    return problems


def check_matched_cases(root: Path) -> list[str]:
    """The B2/B10 convergent-validity table restates its two source files."""

    problems: list[str] = []
    matched = read_csv(root / "data/metrics/b2_b10_matched_cases.csv")
    b2 = {row["Case"]: row for row in read_csv(root / "data/metrics/b2_integration_access.csv")}
    b10 = {
        row["Case"]: row for row in read_csv(root / "data/metrics/b10_documentation_profile.csv")
    }
    for row in matched:
        label = f"b2_b10_matched_cases.csv {row['Matched case']!r}"
        b2_row = b2.get(row["B2 case"])
        b10_row = b10.get(row["B10 case"])
        if b2_row is None or b10_row is None:
            problems.append(f"{label}: references an unknown B2 or B10 case")
            continue
        if row["Device / interface"] != b2_row["Device / interface"]:
            problems.append(f"{label}: device/interface does not match {row['B2 case']}")
        stored_ias = numeric(row["IAS"])
        source_ias = numeric(b2_row["IAS"])
        if stored_ias is None or source_ias is None or not isclose(stored_ias, source_ias):
            problems.append(f"{label}: IAS does not match {row['B2 case']}")
        for column in ("Actionable public resolution", "Private migration"):
            if row[column] != b10_row[column]:
                problems.append(f"{label}: {column!r} does not match {row['B10 case']}")
        full_weight = "; ".join(
            subtype for subtype in B10_SUBTYPES if numeric(b10_row[subtype]) == 1
        )
        if row["Documentation subtypes at full weight"] != full_weight:
            problems.append(
                f"{label}: documentation subtypes at full weight should be {full_weight!r}"
            )
        if row["Source URL"] != b10_row["Source URL"]:
            problems.append(f"{label}: source URL does not match {row['B10 case']}")
    return problems


CHECKS: tuple[Callable[[Path], list[str]], ...] = (
    check_row_counts,
    check_score_cells,
    check_derived_scores,
    check_categoricals,
    check_evidence_register,
    check_episode_and_adjudication_subsets,
    check_episode_thread_coherence,
    check_segmentation_targets,
    check_episode_provenance,
    check_b2_component_bookkeeping,
    check_b3_applicable_fields,
    check_b6_denominator_status,
    check_b7_denominator,
    check_b8_alignment_eligibility,
    check_funnel_intervals,
    check_matched_cases,
    check_registry_examples,
    check_example_streams,
    pairwise_drift,
    atlas_drift,
    atlas_summary_drift,
    blind_subset_drift,
)


def _flatten(results: Iterable[list[str]]) -> tuple[str, ...]:
    return tuple(problem for result in results for problem in result)


def check_release_data(root: str | Path) -> DataReport:
    """Run every release-data check and collect the problems they report."""

    root_path = Path(root)
    problems = _flatten(check(root_path) for check in CHECKS)
    return DataReport(checked_files=tuple(sorted(EXPECTED_ROW_COUNTS)), problems=problems)
