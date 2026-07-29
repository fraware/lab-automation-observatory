"""Tests for run-event stream loading, validation, and B5/B6 computation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from labauto_observatory.io import read_json
from labauto_observatory.run_events import (
    EXAMPLES_DIR_RELATIVE,
    check_example_streams,
    check_stream_structure,
    compute_b6_assessment,
    compute_observability_coverage,
    compute_oc_components,
    load_stream,
)
from labauto_observatory.validation import validate_instance

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / EXAMPLES_DIR_RELATIVE


def _example(name: str) -> dict[str, Any]:
    return load_stream(EXAMPLES / name)


def test_committed_example_streams_validate() -> None:
    assert check_example_streams(ROOT) == []


def test_b5_c3_example_scores_observability_fields() -> None:
    stream = _example("b5_c3_composite_transfer.yaml")
    components = compute_oc_components(stream)
    assert components["Command"] == 1.0
    assert components["Acknowledgment"] == 1.0
    assert components["Modeled state change"] == 1.0
    assert components["Warning / failure"] == 1.0
    assert components["Human intervention"] == 1.0
    assert components["Recovery record"] == 1.0
    assert components["Final result / disposition"] == 0.0
    assert compute_observability_coverage(stream) == pytest.approx(0.75)


def test_b5_c3_example_matches_b6_preflight_scenario() -> None:
    stream = _example("b5_c3_composite_transfer.yaml")
    assessment = compute_b6_assessment(stream)
    assert assessment["irreversible_prefix_completed"] is True
    assert assessment["failure_class"] == "modeled_state_incompatibility"
    assert assessment["preflight_detectable"] == "yes"


def test_b6_abort_example_carries_indeterminate_preflight() -> None:
    stream = _example("b6_return_volume_abort.yaml")
    assessment = compute_b6_assessment(stream)
    assert assessment["irreversible_prefix_completed"] is True
    assert assessment["failure_class"] == "post_execution_software_error"
    assert assessment["preflight_detectable"] == "indeterminate"


def test_b6_abort_example_records_disposition() -> None:
    stream = _example("b6_return_volume_abort.yaml")
    components = compute_oc_components(stream)
    assert components["Run + config identity"] == 1.0
    assert components["Material / resource identity"] == 1.0
    assert components["Final result / disposition"] == 1.0


def test_duplicate_event_id_is_reported() -> None:
    stream = _example("b5_c3_composite_transfer.yaml")
    stream["events"][1]["event_id"] = stream["events"][0]["event_id"]
    problems = check_stream_structure(stream)
    assert any("duplicated event_id" in problem for problem in problems)


def test_non_monotonic_sequence_is_reported() -> None:
    stream = _example("b5_c3_composite_transfer.yaml")
    stream["events"][2]["sequence"] = 1
    problems = check_stream_structure(stream)
    assert any("not strictly greater" in problem for problem in problems)


def test_schema_rejects_missing_failure_fields() -> None:
    schema = read_json(ROOT / "schemas/run-event.schema.json")
    stream = {
        "schema_version": "0.1.0-draft",
        "run_id": "RUN-test",
        "events": [
            {
                "event_id": "e0",
                "sequence": 0,
                "event_type": "failure_raised",
                "actor": "device",
                "severity": "error",
                "message": "hardware fault",
            }
        ],
    }
    with pytest.raises(ValueError, match="failure_class"):
        validate_instance(stream, schema)
