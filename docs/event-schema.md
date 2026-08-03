# Run-event stream schema (design proposal)

Status: design proposal for Roadmap 0.2. This page proposes a typed event stream
that would let B5 Observability Coverage and B6 preflight preventability be
measured from machine-readable run logs instead of reconstructed from forum
threads. The JSON Schema draft lives at
`schemas/run-event.schema.json`. No published
metric reads from it, and nothing here is a standard.

## Why an event stream, and why it is not `b5_observability.csv`

`data/metrics/b5_observability.csv` is a fixed, four-case snapshot: the ten
Observability Coverage (OC) component scores the pilot coded by reading threads
after the fact. Each row is a hand assessment of whether a run's public record
contained run identity, material identity, commands, acknowledgments, physical
observations, modeled state, warnings, human interventions, recovery actions,
and final disposition.

`data/metrics/b6_preflight_preventability.csv` extends the same limitation to
preflight: four scenarios were coded by asking, after reading the thread,
whether an irreversible prefix completed, what failure class appeared, and
whether the failure was detectable before dispatch.

An event stream is a different artifact. It records what happened **as an ordered
sequence of typed events** while a run executes (or immediately after, from an
export), so that the OC components and the B6 failure fields become **computable**
rather than inferred. What a stream can do that a retrospective CSV cannot:

- separate a scheduler's modeled state from a device's physical observation in
  the same run, instead of collapsing them into one ordinal score;
- mark which commands are physically irreversible, so the completed irreversible
  prefix after an abort is a count rather than a narrative judgment;
- carry `preflight_detectable: indeterminate` as a first-class value, because
  one of the four coded B6 scenarios is genuinely indeterminate and a boolean
  field would force a wrong answer.

## Event types and the ten OC fields

The schema defines thirteen `event_type` values. Ten of them correspond one to
one with the OC component columns in `b5_observability.csv`; the other three
(`run_started`, `config_bound`, `resource_bound`) are envelope events that bind
identity before the operational sequence begins.

| OC column in `b5_observability.csv` | `event_type` | Required payload fields |
|---|---|---|
| Run + config identity | `config_bound` | `method_identity` on the stream; event binds the executed method |
| Material / resource identity | `resource_bound` | (stream-level binding; event marks which labware or material slot is in scope) |
| Command | `command_issued` | `command`, `physically_irreversible`, optional `preflight_checkable` |
| Acknowledgment | `command_acknowledged` | `acknowledges`, `outcome` (`accepted`, `rejected`, `completed`, `aborted`, `unknown`) |
| Physical observation | `physical_observation` | `observation` |
| Modeled state change | `modeled_state_changed` | `modeled_state` |
| Warning / failure | `warning_raised` or `failure_raised` | `severity`, `message`; failures also require `failure_class`, `preflight_detectable` |
| Human intervention | `human_intervention` | `intervention` |
| Recovery record | `recovery_action` | `recovery`, `restores` (array of `event_id`s) |
| Final result / disposition | `disposition_recorded` then `run_finished` | `material_disposition`, `disposition_evidence`; terminal `run_result` |

Every event carries `event_id`, strictly increasing `sequence`, and `actor`
(`scheduler`, `device`, `operator`, or `analysis`). Ordering is explicit because
wall-clock timestamps from a scheduler and a device are not reliably comparable;
`recorded_at` is optional and nullable so an event whose time is unknown can
still be recorded in order.

## Failure vocabulary from B6

`failure_raised` events reuse the failure classes already coded in
`b6_preflight_preventability.csv`:

| B6 `Failure class` | `failure_class` enum value |
|---|---|
| Modeled-state incompatibility | `modeled_state_incompatibility` |
| Argument-shape / protocol validation error | `argument_shape_validation` |
| Post-aspiration software/vector error | `post_execution_software_error` |
| Hardware failure | `hardware_failure` |
| (other) | `other` |

`preflight_detectable` takes `yes`, `no`, or `indeterminate`, matching the B6
column `Preflight detectability` including the indeterminate scenario on the
return-volume-after-abort thread. A two-valued field would have forced that
case to yes or no.

`command_issued.physically_irreversible` is what makes
`Irreversible prefix completed` computable: after a `run_finished` with
`run_result: aborted`, count the irreversible commands that completed before the
abort and compare to the B6 coding rationale.

## Minimal valid stream

The schema is validated in `tests/test_schemas.py`. Example streams grounded in the B5-C3 and B6 pilot cases live under `data/run_event_examples/`, and `labauto_observatory.run_events` loads them, checks sequence and reference invariants, and computes OC components plus the B6 preflight fields the stream can express. `make validate` fails if an example stream drifts from the schema or its structural rules.

A minimal stream that expresses one command, one acknowledgment, and a terminal disposition:

```yaml
schema_version: "0.1.0-draft"
run_id: "RUN-2026-0001"
method_identity: "sha256:abc123…"
events:
  - event_id: e0
    sequence: 0
    event_type: run_started
    actor: scheduler
  - event_id: e1
    sequence: 1
    event_type: command_issued
    actor: scheduler
    command: aspirate 100 uL from A1
    physically_irreversible: true
    preflight_checkable: true
  - event_id: e2
    sequence: 2
    event_type: command_acknowledged
    actor: device
    acknowledges: e1
    outcome: completed
  - event_id: e3
    sequence: 3
    event_type: disposition_recorded
    actor: scheduler
    material_disposition: retained_in_tips
    disposition_evidence: null
  - event_id: e4
    sequence: 4
    event_type: run_finished
    actor: scheduler
    run_result: aborted
```

This stream would score poorly on several OC components (no physical observation,
no recovery) on purpose: the schema's job is to **record gaps honestly**, not
to imply completeness.

## What this design does not do

- It does not define an emitter API, wire format, or storage backend. The schema
  describes the logical stream only.
- It does not replace `b5_observability.csv` or `b6_preflight_preventability.csv`
  for the published pilot. Those files remain the manuscript's evidence until
  independent streams exist and are coded.
- It does not compute OC or preflight rates across streams. Aggregation policy
  is out of scope until real streams arrive from more than one laboratory.
- It is not version-stable. `schema_version: "0.1.0-draft"` is pinned so an
  early consumer cannot mistake the proposal for a contract.

## Open questions

- Should `resource_bound` carry a formal labware descriptor (SBS slot, barcode,
  content digest) or stay a free-text binding until a physical-resource registry
  exists?
- Is one `analysis` actor sufficient, or do post-run QC pipelines need their
  own actor class once event streams leave the instrument?
- Should `evidence_sources` at the stream level be required before any stream
  can be used as coding input, mirroring the registry's provenance rule?

Comment on the Roadmap item or open a draft pull request against
`schemas/run-event.schema.json` to continue the discussion. See also
[docs/index.md](index.md#community-artifacts-summary) and
[Project roadmap](project.md#roadmap).
