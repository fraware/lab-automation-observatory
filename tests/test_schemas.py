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
