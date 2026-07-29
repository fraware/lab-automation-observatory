# Device-interface accessibility registry (design draft)

Status: design draft for Roadmap 0.2, seeded by [issue #12](https://github.com/fraware/lab-automation-observatory/issues/12). This page proposes a schema, ships six checked seed records, and states how to contribute a seventh. It is not a scored product comparison, and it is not an input to any published metric: no number in the manuscript reads from this registry, and adding records cannot change one.

## Why a registry, and why it is not `b2_integration_access.csv`

`data/metrics/b2_integration_access.csv` is a fixed, six-case snapshot: the field-level evidence behind the published Integration Accessibility Score (IAS) for the pilot corpus. It cannot grow, because growing it would change a number the manuscript already cites.

A registry is a different kind of artifact. It is meant to accept new device/interface cases over time, independent of any single manuscript's numbers, the same way `schemas/knowledge-index.schema.json` exists separately from any specific set of resolved-knowledge records. What a registry can do that a fixed snapshot cannot:

- accept a new device/interface case without touching a published metric;
- track whether an interface's maintenance state has changed *after* the accessibility facts were recorded, instead of freezing both together at one point in time;
- carry a per-record expiry (`last_verified`) so a stale entry is visible instead of silently trusted.

## Field groups

Every field belongs to exactly one of five groups. Mixing them in a single flat record is the failure mode this design avoids: an interface can be fully documented and completely unmaintained at the same time, and a registry record has to be able to say both without one fact overwriting the other.

### 1. Identity and provenance

| Field | Type | Requirement | Purpose |
|---|---|---|---|
| `record_id` | String, pattern `DIR-YYYY-NNNN` | Required | Stable, immutable identifier. |
| `vendor` | String | Required | The organization behind the device or control software. |
| `product` | String | Required | The specific product or platform line. |
| `interface_identity` | String | Required | The exact, version-bound interface path described by this record. One record describes one interface path, not a whole product line. |
| `interface_class` | Enum: `native_driver`, `vendor_sdk`, `rest_api`, `serial_protocol`, `plc_firmware`, `community_reimplementation`, `other` | Required | Structural kind of integration path, for grouping and filtering only. |
| `evidence_sources` | Array of URLs, at least one | Required | Public, stable links the record is derived from. Plays the role `forum_provenance` plays in the knowledge-index schema, generalized to more than one source. |
| `pilot_case_id` | String, pattern `B2-Cn` | Optional | Provenance link to the published pilot case in `data/metrics/b2_integration_access.csv` that this record re-describes. Present on the six seed records; omitted by any record about a device the pilot never coded. |
| `supersedes`, `superseded_by` | Arrays of `record_id` | Optional, default empty | Record lineage when a case is re-assessed or split. |

`pilot_case_id` exists so that "the registry agrees with the published metric file" is a check rather than an assurance. When it is present, `make validate` requires the record's six accessibility components, `unknown_components`, and `accessibility_score` to equal that case's published cells, and requires the case's source URL to appear in `evidence_sources`. A seed record may therefore add maintenance, lifecycle, evidence-grade, and prohibited-claim facts to a published case; it may not restate the case's score differently, and it may not introduce a seventh pilot case. Two records cannot claim the same pilot case.

### 2. Interface accessibility facts

These six fields are a **fixed snapshot** of what the reviewed public material showed at assessment time. They carry over directly from `data/metrics/b2_integration_access.csv`, using the same `0 / 0.5 / 1` scoring already documented in `docs/data-dictionary.md`:

| Field | Meaning |
|---|---|
| `documentation` | Public documentation of the interface. |
| `api_protocol` | A documented API, protocol, or command set. |
| `licence_clarity` | Whether licensing conditions for using the interface are clear. |
| `simulator_isolated_testing` | Whether the interface can be exercised without live hardware. |
| `examples_reference_implementation` | Whether a runnable example or reference implementation exists. |
| `maintainer_support_declared` | Whether a public maintainer or support channel was declared and observable at assessment time. |

Each of the six takes `0`, `0.5`, `1`, or `null`. **`null` is not `0`.** `0` means the reviewed material showed the property was explicitly absent; `null` means the material never addressed it at all. This is the same unknown-versus-absent rule already stated as a shared convention in `docs/data-dictionary.md`, carried into the registry rather than reinvented. `unknown_components` counts the `null` values, and `accessibility_score` is the mean over the non-null components only, exactly as `IAS`, `RMC`, `PDC`, and `OC` are computed elsewhere in this repository. None of the six seed records below need a `null` component, because all six B2 cases in `b2_integration_access.csv` report zero unknown components; the schema still types every component as nullable so a community submission can use it honestly instead of guessing `0`. Both the count and the mean are recomputed in `make validate`, so a record cannot claim a score its own cells do not produce.

`accessibility_score` measures **public accessibility conditions**, not device reliability, completeness, or quality. It is a photograph of what was documented, not an endorsement.

### 3. Current maintenance facts

Accessibility facts describe what was true when someone last read the documentation. Maintenance facts describe whether anyone is still keeping the interface working, and they are expected to change **without** the accessibility facts changing at all — an interface can stay perfectly documented while its maintainer goes silent. Keeping the two apart is what makes this a registry rather than a repost of the fixed snapshot:

| Field | Type | Requirement | Purpose |
|---|---|---|---|
| `maintenance_status` | Enum: `active`, `intermittent`, `dormant`, `unmaintained`, `unknown` | Required | Current upkeep state as of `last_verified`. |
| `last_activity_observed` | String or `null` | Optional | Coarse, source-bound date or range of the most recent observed activity (for example `'2025'` or `'2022-2023'`), using the same non-precise convention as the `Date relevance` column in `b2_integration_access.csv`. `null` when the source gives no independent activity signal. |
| `last_verified` | ISO date | Required | When a maintainer last checked this record's fields against public sources. Comparable to `Last verified` in `schemas/knowledge-index.schema.json`. |
| `correction_status` | Enum: `active`, `review_due`, `disputed`, `superseded`, `archived` | Required | Record lifecycle, using the same vocabulary as the knowledge-index schema. |
| `record_steward` | String | Required | Public role or project accountable for keeping *this record* current. Distinct from `maintainer_support_declared`, which is a fact about the device's own support channel, not about who owns the registry entry. |

`last_activity_observed` deliberately does not use a strict `date` format. The underlying evidence is almost always a forum-thread date or a stated year range, and forcing that into `YYYY-MM-DD` would manufacture a precision the source does not have.

### 4. Evidence grade

| Field | Type | Requirement | Purpose |
|---|---|---|---|
| `evidence_grade` | Integer 0-4 | Required | `0` unspecified, `1` declared, `2` measured, `3` device-validated, `4` independently reproduced. Same ladder already defined for the knowledge index in `data/knowledge_index/schema_fields.csv`. |
| `evidence_confidence` | Enum: `High`, `Medium`, `Low` | Required | Submitter or reviewer confidence in the row as coded, not a statistical interval. |
| `evidence_note` | String | Required | Short rationale tying the component scores, grade, and maintenance status back to what the source actually said. |

`evidence_grade` and `accessibility_score` are reported separately on purpose: a fully documented interface with no independent reproduction, and a partially documented interface someone has actually run on hardware, are different kinds of evidence and must not collapse into one number.

### 5. Prohibited downstream claims and known limitations

| Field | Type | Requirement | Purpose |
|---|---|---|---|
| `known_limitations` | Array of strings, at least one | Required | Explicit technical bounds of this specific record (partial feature coverage, single hardware generation, modified unit, and so on). |
| `prohibited_claims` | Array of strings, at least one | Required | Downstream claims this record must not be used to support. |

Every record's `prohibited_claims` must include a statement that the record cannot be used to rank its vendor against other vendors on accessibility or reliability. A registry made of many single-vendor records is exactly the shape of data that gets misread as a league table, so the prohibition is a required field, not a documentation aside. Consistent with `docs/claim-discipline.md`, the registry as a whole also carries no prevalence, market-share, or installed-base claim: a growing count of registry records describes registry coverage, not how common any interface pattern is among laboratories.

## Seed records

Seven seed records are checked into `data/registry_examples/device_interface_registry_examples.yaml`. Six cover every B2 case the pilot published, one record per case; the seventh is a community-intake example without `pilot_case_id`:

| `record_id` | `pilot_case_id` | Interface | `accessibility_score` | `maintenance_status` | `evidence_grade` |
|---|---|---|---|---|---|
| `DIR-2026-0001` | `B2-C2` | Hamilton VENUS 6.x REST API | 0.667 | active | 1 (declared) |
| `DIR-2026-0002` | `B2-C3` | CLARIOStar plate reader via PyLabRobot | 0.833 | active | 3 (device-validated) |
| `DIR-2026-0003` | `B2-C6` | LiCONiC STR240/STX via RS-232/PLC firmware | 0.333 | unmaintained | 2 (measured) |
| `DIR-2026-0004` | `B2-C1` | Hamilton HHS/HHC via Heater Shaker Box and PyLabRobot | 0.583 | dormant | 1 (declared) |
| `DIR-2026-0005` | `B2-C4` | Tecan LPT220 via Driver Framework and RS-232 wrapper | 0.583 | active | 2 (measured) |
| `DIR-2026-0006` | `B2-C5` | Cellario custom driver via the Driver Development Kit | 0.833 | active | 1 (declared) |
| `DIR-2026-0007` | — | In-house driver integration (community intake) | 0.400 | active | 2 (measured) |

Each `accessibility_score` is the mean over the same known components as the corresponding case's `IAS` in `data/metrics/b2_integration_access.csv`, and `make validate` fails if the two ever disagree. What each record adds is the maintenance, lifecycle, evidence-grade, and prohibited-claim structure that the fixed metric file has no place for. The set deliberately spans four maintenance states and three evidence grades, so the schema's separations are visible in real data rather than only in the field tables above. `DIR-2026-0004` is the clearest illustration of why maintenance is a separate field group: its accessibility facts are mid-range and unchanged, and the thing that makes it unusable today is that development stopped.

Six records is coverage of the pilot, not coverage of laboratory automation. The seventh record shows the community-intake shape: no `pilot_case_id`, one public source, explicit limitations, and a vendor-ranking prohibition. The registry does not become useful by growing; it becomes useful when records arrive from people who integrated the hardware themselves.

## Contributing a record

The contribution path is deliberately narrow, because the failure mode for a registry is not too few records but records that cannot be checked.

**What a submission needs.** One record, describing one version-bound interface path, with:

1. a public, stable URL in `evidence_sources` that a reader can open without an account;
2. the six accessibility components scored `0`, `0.5`, `1`, or `null`, where `null` means the source never addressed the component — never a stand-in for `0`;
3. `unknown_components` and `accessibility_score` consistent with those six cells;
4. `maintenance_status` and `last_verified` describing the state *you* observed, and `last_activity_observed` left `null` if the source gives no independent activity signal;
5. an `evidence_grade` you can defend from the source alone: `1` if the interface is only described, `2` if something was measured, `3` if it ran on the device, `4` if someone else reproduced it independently;
6. at least one `known_limitations` entry and at least one `prohibited_claims` entry, and the prohibitions must include that the record cannot be used to rank its vendor against others.

Omit `pilot_case_id` unless the record re-describes one of the six published pilot cases; you cannot add a seventh.

**How to submit.** Open a pull request adding your record to `data/registry_examples/device_interface_registry_examples.yaml`, or open an issue with the same fields if you would rather not edit YAML. Then run:

```bash
make validate
make test
```

`make validate` runs the registry checks in `labauto_observatory.registry`: schema conformance, the component arithmetic, unique and internally consistent record IDs and lineage, the vendor-ranking prohibition, and agreement with the published pilot case when `pilot_case_id` is present. `make test` adds the mutation tests in `tests/test_registry.py`, which break each of those properties in a scratch copy and assert that the check fires. A submission that fails either is not rejected on taste; it is failing a stated rule you can read.

**What review looks at.** Whether the record's claims are traceable to the cited source, whether `interface_identity` is specific enough that a reader knows which version was assessed, and whether the limitations and prohibitions match what the evidence actually supports. Reviewers do not adjust scores to make records comparable to each other; two records assessed from different sources are not meant to be comparable.

**Correcting a record.** Use the process in [Correction workflow](correction-workflow.md). Record IDs are immutable: a correction changes fields and `last_verified`, and a re-assessment that reaches a materially different conclusion is a new record joined to the old one through `supersedes` and `superseded_by`, with the old record's `correction_status` set to `superseded`.

## What this design does not do

- It does not promise a review turnaround. The contribution section above states what a submission must contain and what is checked mechanically; it deliberately states no SLA, because a single-maintainer project cannot honour one.
- It does not compute or publish any aggregate across records (count by vendor, mean accessibility by interface class, or similar). Aggregation policy is out of scope until the registry has enough independently contributed records for aggregation to mean something, and even then it must not become a vendor comparison.
- It does not touch `data/metrics/b2_integration_access.csv`, the published IAS values, or any claim in `docs/claim-discipline.md`. The two files describe the same underlying cases from different angles and are expected to stay in agreement on the numbers they share, not to be merged.

## Open questions for issue #12

- Should `interface_class` be closed (as drafted) or open with a controlled-vocabulary extension process, once real community submissions arrive?
- Is a single `record_steward` string sufficient, or does the registry eventually need the same kind of correction workflow defined in `docs/correction-workflow.md`, adapted for interface facts instead of evidence/metric facts?
- Should `evidence_sources` require more than one independent source before `evidence_grade` can exceed `2`, the way `Confirmed` root-cause status requires reproduction in the knowledge-index schema?

Comment on issue #12 or open a draft pull request against `schemas/device-interface-registry.schema.json` to continue the discussion.
