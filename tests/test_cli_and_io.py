from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from labauto_observatory.cli import app
from labauto_observatory.io import (
    integer,
    normalised_newlines,
    numeric,
    read_csv_many,
    read_json,
    read_text_lf,
    read_yaml,
)
from labauto_observatory.metrics import (
    association_from_counts,
    mean_score,
    phi_coefficient,
    wilson_interval,
)
from labauto_observatory.validation import validate_file

ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_io_helpers() -> None:
    assert (
        len(read_csv_many(sorted((ROOT / "data/derived").glob("evidence_register_part_*.csv"))))
        == 55
    )
    assert isinstance(read_json(ROOT / "data/knowledge_index/seed_records.json"), list)
    assert isinstance(read_yaml(ROOT / "data/knowledge_index/seed_records.yaml"), list)
    assert numeric(" 0.5 ") == 0.5
    assert numeric("") is None
    assert integer(" 4.0 ") == 4
    assert integer(" ") is None


def test_line_ending_helpers(tmp_path: Path) -> None:
    assert normalised_newlines("a\r\nb\rc\nd") == "a\nb\nc\nd"
    target = tmp_path / "mixed.txt"
    target.write_bytes(b"a\r\nb\rc\nd")
    assert read_text_lf(target) == "a\nb\nc\nd"


def test_cli_reproduce() -> None:
    result = runner.invoke(app, ["reproduce", "--root", str(ROOT)])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["corpus"]["threads"] == 55


def test_cli_validation() -> None:
    result = runner.invoke(
        app,
        [
            "validate-knowledge-index",
            "--records",
            str(ROOT / "data/knowledge_index/seed_records.yaml"),
            "--schema",
            str(ROOT / "schemas/knowledge-index.schema.json"),
        ],
    )
    assert result.exit_code == 0


def test_validation_reads_json_instances(tmp_path: Path) -> None:
    records = read_yaml(ROOT / "data/knowledge_index/seed_records.yaml")
    instance = tmp_path / "records.json"
    instance.write_text(json.dumps(records), encoding="utf-8")
    validate_file(instance, ROOT / "schemas/knowledge-index.schema.json")


def test_additional_metric_error_paths() -> None:
    assert phi_coefficient(0, 0, 0, 0) == 0
    assert association_from_counts(0, 0, 0, 1).descriptive_risk_ratio is None
    with pytest.raises(ValueError, match="nonnegative"):
        phi_coefficient(-1, 0, 0, 0)
    with pytest.raises(ValueError, match="at least one observation"):
        association_from_counts(0, 0, 0, 0)
    with pytest.raises(ValueError, match="positive"):
        wilson_interval(0, 0)
    with pytest.raises(ValueError, match="at least one known"):
        mean_score([None])
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        mean_score([1.2])
