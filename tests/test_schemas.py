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
