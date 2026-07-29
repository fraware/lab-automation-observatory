"""Validation for the device-interface accessibility registry seed records.

``docs/device-interface-registry.md`` is a design draft, and the records in
``data/registry_examples/`` are seeds rather than a released dataset. That is
precisely why they need checking now: the contribution path invites outside
submissions, and a schema alone cannot express the three properties that make a
seed record trustworthy.

* **Arithmetic.** ``accessibility_score`` is a mean over the known components
  and ``unknown_components`` counts the unknown ones. JSON Schema can type both
  fields but cannot tie either to the six component cells beside them.
* **Agreement with the pilot.** A record carrying ``pilot_case_id`` re-describes
  a case whose accessibility numbers are already published in
  ``data/metrics/b2_integration_access.csv`` and already cited by the
  manuscript. The registry may add maintenance, lifecycle, and prohibited-claim
  facts to that case; it may not restate its score differently. The draft says
  the two files are "expected to stay in agreement on the numbers they share",
  and this module is what makes that a check instead of a promise.
* **Claim discipline.** ``docs/claim-discipline.md`` forbids reading a
  collection of single-vendor records as a league table. Every record must
  therefore prohibit exactly that use of itself, and a submission that omits the
  prohibition must fail rather than be silently accepted.

Checks return problem strings rather than raising, matching
:mod:`labauto_observatory.register_validation`, so one run reports every failure
it can find.
"""

from __future__ import annotations

from math import isclose
from pathlib import Path
from typing import Any

from .analysis import B2_COMPONENTS
from .io import integer, numeric, read_csv, read_yaml
from .validation import validate_file

EXAMPLES_RELATIVE = "data/registry_examples/device_interface_registry_examples.yaml"
SCHEMA_RELATIVE = "schemas/device-interface-registry.schema.json"
B2_RELATIVE = "data/metrics/b2_integration_access.csv"

TOLERANCE = 1e-9

# The registry restates the six B2 accessibility components under snake_case
# names. Pairing them here, rather than repeating either spelling, is what lets a
# `pilot_case_id` record be compared cell by cell against the published metric
# file without a second hand-maintained list of column names.
COMPONENT_COLUMNS: tuple[tuple[str, str], ...] = tuple(
    zip(
        (
            "documentation",
            "api_protocol",
            "licence_clarity",
            "simulator_isolated_testing",
            "examples_reference_implementation",
            "maintainer_support_declared",
        ),
        B2_COMPONENTS,
        strict=True,
    )
)

ACCESSIBILITY_FIELDS: tuple[str, ...] = tuple(field for field, _ in COMPONENT_COLUMNS)


def _known(record: dict[str, Any]) -> list[float]:
    return [value for field in ACCESSIBILITY_FIELDS if (value := record[field]) is not None]


def check_component_bookkeeping(records: list[dict[str, Any]]) -> list[str]:
    """``unknown_components`` counts the unknowns and the score is their mean."""

    problems: list[str] = []
    for record in records:
        label = record["record_id"]
        known = _known(record)
        unknown = len(ACCESSIBILITY_FIELDS) - len(known)
        if record["unknown_components"] != unknown:
            problems.append(
                f"{label}: 'unknown_components' is {record['unknown_components']!r} but "
                f"{unknown} of the six accessibility components are null"
            )
        if not known:
            problems.append(f"{label}: every accessibility component is unknown")
            continue
        expected = sum(known) / len(known)
        if not isclose(record["accessibility_score"], expected, abs_tol=TOLERANCE):
            problems.append(
                f"{label}: 'accessibility_score' is {record['accessibility_score']!r} but the "
                f"mean over its {len(known)} known components is {expected!r}"
            )
    return problems


def check_claim_discipline(records: list[dict[str, Any]]) -> list[str]:
    """Every record forbids being read as a ranking of its own vendor."""

    problems: list[str] = []
    for record in records:
        label = record["record_id"]
        vendor_token = record["vendor"].split(" ")[0].lower()
        prohibitions = [claim.lower() for claim in record["prohibited_claims"]]
        if not any("rank" in claim and vendor_token in claim for claim in prohibitions):
            problems.append(
                f"{label}: 'prohibited_claims' must forbid ranking {record['vendor']!r} against "
                "other vendors; see docs/claim-discipline.md"
            )
    return problems


def check_identity_and_lineage(records: list[dict[str, Any]]) -> list[str]:
    """IDs are unique, and lineage points at records that exist."""

    problems: list[str] = []
    record_ids = [record["record_id"] for record in records]
    for record_id in sorted({value for value in record_ids if record_ids.count(value) > 1}):
        problems.append(f"{record_id}: duplicated record ID")

    known_ids = set(record_ids)
    for record in records:
        label = record["record_id"]
        for field in ("supersedes", "superseded_by"):
            for referenced in record.get(field, []):
                if referenced == label:
                    problems.append(f"{label}: '{field}' refers to the record itself")
                elif referenced not in known_ids:
                    problems.append(f"{label}: '{field}' refers to unknown record {referenced}")
    return problems


def check_pilot_case_agreement(root: Path, records: list[dict[str, Any]]) -> list[str]:
    """A seed record may not rescore the pilot case it re-describes."""

    problems: list[str] = []
    cases = {row["Case"]: row for row in read_csv(root / B2_RELATIVE)}
    linked = [record for record in records if "pilot_case_id" in record]

    seen: dict[str, str] = {}
    for record in linked:
        label = record["record_id"]
        case_id = record["pilot_case_id"]
        case = cases.get(case_id)
        if case is None:
            problems.append(f"{label}: 'pilot_case_id' {case_id} is not a case in {B2_RELATIVE}")
            continue
        if case_id in seen:
            problems.append(
                f"{label}: pilot case {case_id} is already described by {seen[case_id]}; "
                "one published case maps to at most one seed record"
            )
            continue
        seen[case_id] = label

        for field, column in COMPONENT_COLUMNS:
            published = numeric(case[column])
            if record[field] != published:
                problems.append(
                    f"{label}: '{field}' is {record[field]!r} but {case_id} publishes "
                    f"{column!r} as {published!r}"
                )
        published_unknown = integer(case["Unknown components"])
        if record["unknown_components"] != published_unknown:
            problems.append(
                f"{label}: 'unknown_components' is {record['unknown_components']!r} but "
                f"{case_id} publishes {published_unknown!r}"
            )
        published_score = numeric(case["IAS"])
        if published_score is None or not isclose(
            record["accessibility_score"], published_score, abs_tol=TOLERANCE
        ):
            problems.append(
                f"{label}: 'accessibility_score' is {record['accessibility_score']!r} but "
                f"{case_id} publishes an IAS of {case['IAS']!r}"
            )
        if case["Source URL"] not in record["evidence_sources"]:
            problems.append(
                f"{label}: 'evidence_sources' omits the source {case_id} was coded from, "
                f"{case['Source URL']}"
            )
    return problems


def check_registry_examples(root: str | Path) -> list[str]:
    """Validate the committed registry seeds against schema and invariants."""

    root_path = Path(root)
    path = root_path / EXAMPLES_RELATIVE
    if not path.is_file():
        return [f"{EXAMPLES_RELATIVE} is missing"]
    try:
        validate_file(path, root_path / SCHEMA_RELATIVE)
    except ValueError as error:
        # The invariant checks below index fields the schema guarantees are
        # present and correctly typed, so reporting a shape failure and stopping
        # is more useful than a cascade of key errors.
        return [f"{EXAMPLES_RELATIVE} does not satisfy {SCHEMA_RELATIVE}: {error}"]

    records = read_yaml(path)
    if not records:
        return [f"{EXAMPLES_RELATIVE} contains no records"]

    return [
        *check_component_bookkeeping(records),
        *check_claim_discipline(records),
        *check_identity_and_lineage(records),
        *check_pilot_case_agreement(root_path, records),
    ]
