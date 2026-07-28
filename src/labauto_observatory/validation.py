"""JSON Schema validation for community artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .io import read_json, read_yaml


def validate_instance(instance: Any, schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        details = "\n".join(f"- {'/'.join(map(str, error.path))}: {error.message}" for error in errors)
        raise ValueError(f"schema validation failed:\n{details}")


def validate_file(instance_path: str | Path, schema_path: str | Path) -> None:
    instance_file = Path(instance_path)
    schema = read_json(schema_path)
    if instance_file.suffix.lower() in {".yaml", ".yml"}:
        instance = read_yaml(instance_file)
    else:
        instance = read_json(instance_file)
    validate_instance(instance, schema)
