"""Mutation tests for the device-interface registry seed invariants.

Each test breaks exactly one property in a scratch copy of the seed file and
asserts that the corresponding check reports it. The registry is the surface
that invites outside submissions, so a check that silently stopped firing would
be worse here than in the closed pilot data: it would accept a contributed
record that rescores a published pilot case or drops its claim prohibition.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from labauto_observatory.io import read_csv, read_yaml
from labauto_observatory.registry import (
    ACCESSIBILITY_FIELDS,
    B2_RELATIVE,
    EXAMPLES_RELATIVE,
    check_registry_examples,
)

ROOT = Path(__file__).resolve().parents[1]


def _records(root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = read_yaml(root / EXAMPLES_RELATIVE)
    return records


def _write(root: Path, records: list[dict[str, Any]]) -> None:
    (root / EXAMPLES_RELATIVE).write_text(
        yaml.safe_dump(records, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )


def _only(problems: list[str], fragment: str) -> None:
    assert len(problems) == 1, problems
    assert fragment in problems[0], problems[0]


def test_committed_seeds_pass_every_check() -> None:
    assert check_registry_examples(ROOT) == []


def test_every_published_b2_case_is_seeded() -> None:
    """The six published cases are the registry's starting coverage."""

    published = {row["Case"] for row in read_csv(ROOT / B2_RELATIVE)}
    linked = {record["pilot_case_id"] for record in _records(ROOT) if "pilot_case_id" in record}
    assert linked == published


def test_accessibility_fields_are_the_six_scored_components() -> None:
    assert len(ACCESSIBILITY_FIELDS) == 6
    assert len(set(ACCESSIBILITY_FIELDS)) == 6


def test_missing_seed_file_is_reported(data_root: Path) -> None:
    (data_root / EXAMPLES_RELATIVE).unlink()
    _only(check_registry_examples(data_root), "is missing")


def test_empty_seed_file_is_reported(data_root: Path) -> None:
    _write(data_root, [])
    _only(check_registry_examples(data_root), "contains no records")


def test_schema_violation_short_circuits(data_root: Path) -> None:
    records = _records(data_root)
    records[0]["interface_class"] = "telepathy"
    _write(data_root, records)
    _only(check_registry_examples(data_root), "does not satisfy")


def test_wrong_accessibility_score_is_reported(data_root: Path) -> None:
    records = _records(data_root)
    records[0]["accessibility_score"] = 0.25
    _write(data_root, records)
    problems = check_registry_examples(data_root)
    assert any("'accessibility_score' is 0.25" in problem for problem in problems), problems


def test_wrong_unknown_component_count_is_reported(data_root: Path) -> None:
    records = _records(data_root)
    records[0]["unknown_components"] = 2
    _write(data_root, records)
    problems = check_registry_examples(data_root)
    assert any("'unknown_components' is 2" in problem for problem in problems), problems


def test_all_unknown_components_is_reported(data_root: Path) -> None:
    records = [_records(data_root)[0]]
    for field in ACCESSIBILITY_FIELDS:
        records[0][field] = None
    records[0]["unknown_components"] = 6
    records[0].pop("pilot_case_id")
    _write(data_root, records)
    problems = check_registry_examples(data_root)
    assert any("every accessibility component is unknown" in problem for problem in problems), (
        problems
    )


def test_missing_vendor_ranking_prohibition_is_reported(data_root: Path) -> None:
    records = _records(data_root)
    records[0]["prohibited_claims"] = ["Must not be read as a support commitment."]
    _write(data_root, records)
    _only(check_registry_examples(data_root), "must forbid ranking")


def test_duplicate_record_id_is_reported(data_root: Path) -> None:
    records = _records(data_root)
    records[1]["record_id"] = records[0]["record_id"]
    _write(data_root, records)
    problems = check_registry_examples(data_root)
    assert any("duplicated record ID" in problem for problem in problems), problems


def test_lineage_pointing_at_an_unknown_record_is_reported(data_root: Path) -> None:
    records = _records(data_root)
    records[0]["supersedes"] = ["DIR-2026-9999"]
    _write(data_root, records)
    _only(check_registry_examples(data_root), "refers to unknown record DIR-2026-9999")


def test_self_referential_lineage_is_reported(data_root: Path) -> None:
    records = _records(data_root)
    records[0]["superseded_by"] = [records[0]["record_id"]]
    _write(data_root, records)
    _only(check_registry_examples(data_root), "refers to the record itself")


def test_unknown_pilot_case_is_reported(data_root: Path) -> None:
    records = _records(data_root)
    records[0]["pilot_case_id"] = "B2-C99"
    _write(data_root, records)
    _only(check_registry_examples(data_root), "is not a case in")


def test_two_records_claiming_one_pilot_case_are_reported(data_root: Path) -> None:
    records = _records(data_root)
    records[1]["pilot_case_id"] = records[0]["pilot_case_id"]
    # Keep the duplicate's own arithmetic honest so only the collision is left.
    records[1] = {**records[1], **{field: records[0][field] for field in ACCESSIBILITY_FIELDS}}
    records[1]["unknown_components"] = records[0]["unknown_components"]
    records[1]["accessibility_score"] = records[0]["accessibility_score"]
    records[1]["evidence_sources"] = list(records[0]["evidence_sources"])
    _write(data_root, records)
    _only(check_registry_examples(data_root), "is already described by")


def test_rescoring_a_pilot_component_is_reported(data_root: Path) -> None:
    """A seed record may add fields to a published case, never restate its score."""

    records = _records(data_root)
    linked = next(record for record in records if "pilot_case_id" in record)
    field = next(name for name in ACCESSIBILITY_FIELDS if linked[name] != 1)
    linked[field] = 1
    _write(data_root, records)
    problems = check_registry_examples(data_root)
    assert any(f"'{field}' is 1" in problem and "publishes" in problem for problem in problems), (
        problems
    )


def test_dropping_the_pilot_source_url_is_reported(data_root: Path) -> None:
    records = _records(data_root)
    linked = next(record for record in records if "pilot_case_id" in record)
    linked["evidence_sources"] = ["https://example.invalid/unrelated"]
    _write(data_root, records)
    _only(check_registry_examples(data_root), "omits the source")


def test_pilot_case_disagreement_is_caught_through_the_metric_file(
    data_root: Path, edit_csv: Any
) -> None:
    """Editing the published case, not the record, must also fail."""

    edit_csv(data_root / B2_RELATIVE, 1, IAS="0.99")
    problems = check_registry_examples(data_root)
    assert any("publishes an IAS of '0.99'" in problem for problem in problems), problems


@pytest.mark.parametrize("field", ["supersedes", "superseded_by"])
def test_absent_lineage_fields_are_allowed(data_root: Path, field: str) -> None:
    records = _records(data_root)
    for record in records:
        record.pop(field)
    _write(data_root, records)
    assert check_registry_examples(data_root) == []
