from __future__ import annotations

from pathlib import Path

import pytest

from labauto_observatory.io import read_json, read_yaml
from labauto_observatory.validation import validate_file, validate_instance

ROOT = Path(__file__).resolve().parents[1]


def test_seed_knowledge_records_validate() -> None:
    validate_file(
        ROOT / "data/knowledge_index/seed_records.yaml",
        ROOT / "schemas/knowledge-index.schema.json",
    )


def test_example_question_validates() -> None:
    validate_file(
        ROOT / "data/knowledge_index/example_question.yaml",
        ROOT / "schemas/troubleshooting-question.schema.json",
    )


def test_partial_execution_requires_state_and_intervention() -> None:
    question = read_yaml(ROOT / "data/knowledge_index/example_question.yaml")
    schema = read_json(ROOT / "schemas/troubleshooting-question.schema.json")
    question.pop("physical_state_after_failure")
    with pytest.raises(ValueError, match="physical_state_after_failure"):
        validate_instance(question, schema)


_REGISTRY_ACCESSIBILITY_FIELDS = [
    "documentation",
    "api_protocol",
    "licence_clarity",
    "simulator_isolated_testing",
    "examples_reference_implementation",
    "maintainer_support_declared",
]


def test_device_interface_registry_examples_validate() -> None:
    validate_file(
        ROOT / "data/registry_examples/device_interface_registry_examples.yaml",
        ROOT / "schemas/device-interface-registry.schema.json",
    )


def test_device_interface_registry_record_ids_unique() -> None:
    records = read_yaml(ROOT / "data/registry_examples/device_interface_registry_examples.yaml")
    record_ids = [record["record_id"] for record in records]
    assert len(record_ids) == len(set(record_ids))


def test_device_interface_registry_accessibility_score_matches_known_components() -> None:
    records = read_yaml(ROOT / "data/registry_examples/device_interface_registry_examples.yaml")
    for record in records:
        components = [record[field] for field in _REGISTRY_ACCESSIBILITY_FIELDS]
        known = [value for value in components if value is not None]
        assert record["unknown_components"] == len(components) - len(known)
        assert known, f"{record['record_id']} has no known accessibility components"
        expected = sum(known) / len(known)
        assert record["accessibility_score"] == pytest.approx(expected), record["record_id"]


def test_device_interface_registry_records_prohibit_vendor_ranking() -> None:
    records = read_yaml(ROOT / "data/registry_examples/device_interface_registry_examples.yaml")
    for record in records:
        assert record["known_limitations"], record["record_id"]
        assert record["prohibited_claims"], record["record_id"]
        assert any(
            "rank" in claim.lower() and record["vendor"].split(" ")[0].lower() in claim.lower()
            for claim in record["prohibited_claims"]
        ), f"{record['record_id']} must prohibit vendor-ranking use of this record"


def test_run_event_schema_accepts_minimal_stream() -> None:
    schema = read_json(ROOT / "schemas/run-event.schema.json")
    stream = {
        "schema_version": "0.1.0-draft",
        "run_id": "RUN-2026-0001",
        "method_identity": "sha256:abc123",
        "events": [
            {
                "event_id": "e0",
                "sequence": 0,
                "event_type": "run_started",
                "actor": "scheduler",
            },
            {
                "event_id": "e1",
                "sequence": 1,
                "event_type": "command_issued",
                "actor": "scheduler",
                "command": "aspirate 100 uL from A1",
                "physically_irreversible": True,
                "preflight_checkable": True,
            },
            {
                "event_id": "e2",
                "sequence": 2,
                "event_type": "command_acknowledged",
                "actor": "device",
                "acknowledges": "e1",
                "outcome": "completed",
            },
            {
                "event_id": "e3",
                "sequence": 3,
                "event_type": "disposition_recorded",
                "actor": "scheduler",
                "material_disposition": "retained_in_tips",
                "disposition_evidence": None,
            },
            {
                "event_id": "e4",
                "sequence": 4,
                "event_type": "run_finished",
                "actor": "scheduler",
                "run_result": "aborted",
            },
        ],
    }
    validate_instance(stream, schema)


def test_run_event_schema_rejects_missing_failure_fields() -> None:
    schema = read_json(ROOT / "schemas/run-event.schema.json")
    stream = {
        "schema_version": "0.1.0-draft",
        "run_id": "RUN-2026-0002",
        "events": [
            {
                "event_id": "e0",
                "sequence": 0,
                "event_type": "failure_raised",
                "actor": "device",
                "severity": "error",
                "message": "lid state incompatible",
            },
        ],
    }
    with pytest.raises(ValueError, match="failure_class"):
        validate_instance(stream, schema)
