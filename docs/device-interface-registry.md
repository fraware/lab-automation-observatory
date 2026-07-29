# Device-interface accessibility registry (design draft)

Status: design draft for Roadmap 0.2, seeded by [issue #12](https://github.com/fraware/lab-automation-observatory/issues/12). This page proposes a schema and shows worked examples. It does not describe a shipped artifact, a validated release input, or a scored product comparison.

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
| `supersedes`, `superseded_by` | Arrays of `record_id` | Optional, default empty | Record lineage when a case is re-assessed or split. |

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

Each of the six takes `0`, `0.5`, `1`, or `null`. **`null` is not `0`.** `0` means the reviewed material showed the property was explicitly absent; `null` means the material never addressed it at all. This is the same unknown-versus-absent rule already stated as a shared convention in `docs/data-dictionary.md`, carried into the registry rather than reinvented. `unknown_components` counts the `null` values, and `accessibility_score` is the mean over the non-null components only, exactly as `IAS`, `RMC`, `PDC`, and `OC` are computed elsewhere in this repository. None of the three worked examples below need a `null` component, because all six known B2 cases in `b2_integration_access.csv` report zero unknown components; the schema still types every component as nullable so a future community submission can use it honestly instead of guessing `0`.

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

## Worked examples

Three example records are checked into `data/registry_examples/device_interface_registry_examples.yaml` and validate against `schemas/device-interface-registry.schema.json`:

| `record_id` | Interface | `accessibility_score` | `maintenance_status` | `evidence_grade` |
|---|---|---|---|---|
| `DIR-2026-0001` | Hamilton VENUS 6.x REST API | 0.667 | active | 1 (declared) |
| `DIR-2026-0002` | CLARIOStar plate reader via PyLabRobot | 0.833 | active | 3 (device-validated) |
| `DIR-2026-0003` | LiCONiC STR240/STX via RS-232/PLC firmware | 0.333 | unmaintained | 2 (measured) |

Each `accessibility_score` is the mean over the same known components as the corresponding case's `IAS` in `data/metrics/b2_integration_access.csv`, so the two numbers match exactly; the registry record adds the maintenance, evidence-grade, and prohibited-claim fields that the fixed metric file has no place for. The three records deliberately span `active` and `unmaintained` maintenance states and three different evidence grades, so the schema's separations are visible in real data rather than only in the field table above.

## What this design does not do

- It does not define an ingestion process, a submission form, or a review SLA. That is implementation, not schema.
- It does not compute or publish any aggregate across records (count by vendor, mean accessibility by interface class, or similar). Aggregation policy is out of scope until the registry has enough independently contributed records for aggregation to mean something, and even then it must not become a vendor comparison.
- It does not touch `data/metrics/b2_integration_access.csv`, the published IAS values, or any claim in `docs/claim-discipline.md`. The two files describe the same underlying cases from different angles and are expected to stay in agreement on the numbers they share, not to be merged.

## Open questions for issue #12

- Should `interface_class` be closed (as drafted) or open with a controlled-vocabulary extension process, once real community submissions arrive?
- Is a single `record_steward` string sufficient, or does the registry eventually need the same kind of correction workflow defined in `docs/correction-workflow.md`, adapted for interface facts instead of evidence/metric facts?
- Should `evidence_sources` require more than one independent source before `evidence_grade` can exceed `2`, the way `Confirmed` root-cause status requires reproduction in the knowledge-index schema?

Comment on issue #12 or open a draft pull request against `schemas/device-interface-registry.schema.json` to continue the discussion.
