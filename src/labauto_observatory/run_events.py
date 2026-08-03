"""Load, validate, and score laboratory run-event streams.

``docs/event-schema.md`` proposes typed event streams so that Observability
Coverage (B5) and preflight preventability (B6) can be computed from machine-
readable logs instead of reconstructed from forum threads. This module is the
reference loader, structural validator, and scoring path for that proposal.
No published metric reads from it yet; the pilot CSVs remain the manuscript
evidence until independent streams exist.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .analysis import B5_COMPONENTS
from .io import read_json, read_yaml
from .validation import validate_file, validate_instance

SCHEMA_RELATIVE = "schemas/run-event.schema.json"
EXAMPLES_DIR_RELATIVE = "data/run_event_examples"

# Maps each OC column in ``b5_observability.csv`` to the event types that
# evidence it. The scoring rubric below turns presence and completeness of
# those events into the same 0 / 0.5 / 1 cells the pilot coded by hand.
OC_EVENT_TYPES: dict[str, frozenset[str]] = {
    "Run + config identity": frozenset({"config_bound", "run_started"}),
    "Material / resource identity": frozenset({"resource_bound"}),
    "Command": frozenset({"command_issued"}),
    "Acknowledgment": frozenset({"command_acknowledged"}),
    "Physical observation": frozenset({"physical_observation"}),
    "Modeled state change": frozenset({"modeled_state_changed"}),
    "Warning / failure": frozenset({"warning_raised", "failure_raised"}),
    "Human intervention": frozenset({"human_intervention"}),
    "Recovery record": frozenset({"recovery_action"}),
    "Final result / disposition": frozenset({"disposition_recorded", "run_finished"}),
}

PREFLIGHT_DETECTABILITY = frozenset({"yes", "no", "indeterminate"})


def load_stream(path: str | Path) -> dict[str, Any]:
    """Read a YAML or JSON run-event stream from disk."""

    stream_path = Path(path)
    if stream_path.suffix.lower() in {".yaml", ".yml"}:
        payload = read_yaml(stream_path)
    else:
        payload = read_json(stream_path)
    if not isinstance(payload, dict):
        raise ValueError(f"{stream_path}: run-event stream must be a mapping")
    return payload


def _events(stream: dict[str, Any]) -> list[dict[str, Any]]:
    events = stream.get("events")
    if not isinstance(events, list):
        return []
    return [event for event in events if isinstance(event, dict)]


def check_stream_structure(stream: dict[str, Any]) -> list[str]:
    """Structural invariants beyond JSON Schema: IDs, order, and references."""

    problems: list[str] = []
    events = _events(stream)
    if not events:
        return ["events: stream contains no events"]

    seen_ids: set[str] = set()
    previous_sequence = -1
    for event in events:
        event_id = event.get("event_id")
        sequence = event.get("sequence")
        if not isinstance(event_id, str) or not event_id:
            problems.append("every event must carry a non-empty event_id")
            break
        if event_id in seen_ids:
            problems.append(f"{event_id}: duplicated event_id")
        seen_ids.add(event_id)
        if not isinstance(sequence, int):
            problems.append(f"{event_id}: sequence must be an integer")
            continue
        if sequence <= previous_sequence:
            problems.append(
                f"{event_id}: sequence {sequence} is not strictly greater than {previous_sequence}"
            )
        previous_sequence = sequence

    event_ids = {event["event_id"] for event in events if isinstance(event.get("event_id"), str)}
    for event in events:
        event_id = event.get("event_id", "?")
        acknowledges = event.get("acknowledges")
        if acknowledges is not None and acknowledges not in event_ids:
            problems.append(f"{event_id}: acknowledges unknown event {acknowledges!r}")

        restores = event.get("restores")
        if isinstance(restores, list):
            for restored in restores:
                if restored not in event_ids:
                    problems.append(f"{event_id}: restores unknown event {restored!r}")
    return problems


def check_stream(stream: dict[str, Any], root: str | Path) -> list[str]:
    """Validate schema conformance and structural invariants."""

    root_path = Path(root)
    schema_path = root_path / SCHEMA_RELATIVE
    try:
        validate_instance(stream, read_json(schema_path))
    except ValueError as error:
        return [f"run-event stream does not satisfy {SCHEMA_RELATIVE}: {error}"]

    return check_stream_structure(stream)


def check_stream_file(path: str | Path, root: str | Path) -> list[str]:
    """Load and validate one run-event stream file."""

    stream_path = Path(path)
    if not stream_path.is_file():
        return [f"{stream_path}: run-event stream file is missing"]
    try:
        stream = load_stream(stream_path)
    except ValueError as error:
        return [str(error)]
    return check_stream(stream, root)


def _score_run_config_identity(stream: dict[str, Any], events: list[dict[str, Any]]) -> float:
    method = stream.get("method_identity")
    has_method = isinstance(method, str) and bool(method.strip())
    has_config = any(event.get("event_type") == "config_bound" for event in events)
    has_run = any(event.get("event_type") == "run_started" for event in events)
    if has_method and has_config:
        return 1.0
    if has_method or has_config or has_run:
        return 0.5
    return 0.0


def _score_acknowledgment(events: list[dict[str, Any]]) -> float:
    commands = [event for event in events if event.get("event_type") == "command_issued"]
    if not commands:
        return 0.0
    command_ids = {event["event_id"] for event in commands}
    acks = [
        event
        for event in events
        if event.get("event_type") == "command_acknowledged"
        and event.get("acknowledges") in command_ids
    ]
    if not acks:
        return 0.0
    known = [ack for ack in acks if ack.get("outcome") != "unknown"]
    if len(known) == len(command_ids) and all(
        ack.get("outcome") in {"accepted", "rejected", "completed", "aborted"} for ack in known
    ):
        return 1.0
    return 0.5


def _score_disposition(events: list[dict[str, Any]]) -> float:
    dispositions = [event for event in events if event.get("event_type") == "disposition_recorded"]
    if not dispositions:
        return 0.0
    last = dispositions[-1]
    if last.get("material_disposition") == "unknown":
        return 0.5
    return 1.0


def _score_presence(events: list[dict[str, Any]], event_types: frozenset[str]) -> float:
    return 1.0 if any(event.get("event_type") in event_types for event in events) else 0.0


def compute_oc_components(stream: dict[str, Any]) -> dict[str, float]:
    """Score the ten Observability Coverage cells from a validated stream."""

    events = _events(stream)
    return {
        "Run + config identity": _score_run_config_identity(stream, events),
        "Material / resource identity": _score_presence(
            events, OC_EVENT_TYPES["Material / resource identity"]
        ),
        "Command": _score_presence(events, OC_EVENT_TYPES["Command"]),
        "Acknowledgment": _score_acknowledgment(events),
        "Physical observation": _score_presence(events, OC_EVENT_TYPES["Physical observation"]),
        "Modeled state change": _score_presence(events, OC_EVENT_TYPES["Modeled state change"]),
        "Warning / failure": _score_presence(events, OC_EVENT_TYPES["Warning / failure"]),
        "Human intervention": _score_presence(events, OC_EVENT_TYPES["Human intervention"]),
        "Recovery record": _score_presence(events, OC_EVENT_TYPES["Recovery record"]),
        "Final result / disposition": _score_disposition(events),
    }


def compute_observability_coverage(stream: dict[str, Any]) -> float:
    """Mean over the ten OC component scores."""

    components = compute_oc_components(stream)
    return sum(components.values()) / len(B5_COMPONENTS)


def _completed_irreversible_prefix(events: list[dict[str, Any]]) -> bool:
    irreversible = {
        event["event_id"]
        for event in events
        if event.get("event_type") == "command_issued"
        and event.get("physically_irreversible") is True
    }
    if not irreversible:
        return False
    completed: set[str] = set()
    for event in events:
        if event.get("event_type") != "command_acknowledged":
            continue
        acknowledged = event.get("acknowledges")
        if (
            isinstance(acknowledged, str)
            and acknowledged in irreversible
            and event.get("outcome") == "completed"
        ):
            completed.add(acknowledged)
    return bool(completed)


def compute_b6_assessment(stream: dict[str, Any]) -> dict[str, Any]:
    """Derive the B6 preflight fields computable from a stream."""

    events = _events(stream)
    failures = [event for event in events if event.get("event_type") == "failure_raised"]
    assessment: dict[str, Any] = {
        "irreversible_prefix_completed": _completed_irreversible_prefix(events),
    }
    if failures:
        first = failures[0]
        assessment["failure_class"] = first.get("failure_class")
        assessment["preflight_detectable"] = first.get("preflight_detectable")
    return assessment


def check_example_streams(root: str | Path) -> list[str]:
    """Validate every committed example stream under ``data/run_event_examples/``."""

    root_path = Path(root)
    examples_dir = root_path / EXAMPLES_DIR_RELATIVE
    if not examples_dir.is_dir():
        return [f"{EXAMPLES_DIR_RELATIVE}/ is missing"]

    problems: list[str] = []
    paths = sorted(examples_dir.glob("*"))
    if not paths:
        return [f"{EXAMPLES_DIR_RELATIVE}/ contains no example streams"]

    for path in paths:
        if path.suffix.lower() not in {".yaml", ".yml", ".json"}:
            continue
        label = path.relative_to(root_path).as_posix()
        file_problems = check_stream_file(path, root_path)
        problems.extend(f"{label}: {problem}" for problem in file_problems)
    return problems


def validate_stream_file(path: str | Path, root: str | Path) -> None:
    """Fail closed when a stream file does not validate."""

    problems = check_stream_file(path, root)
    if problems:
        raise ValueError("\n".join(problems))


def validate_example_against_schema(path: str | Path, root: str | Path) -> None:
    """Schema-only validation helper for tests."""

    validate_file(path, Path(root) / SCHEMA_RELATIVE)
