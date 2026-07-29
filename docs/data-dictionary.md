# Data dictionary

This page defines every committed CSV column. Two files are normative and should be read first:

- `data/derived/codebook.csv` defines the coding variables and rules (primary versus secondary codes, evidence strength, resolution classes, external migration, quote eligibility).
- `data/derived/taxonomy_rules.csv` defines the ten constructs with inclusion rules, exclusion rules, primary-code eligibility, adjacent codes, required evidence, and a boundary test.

## Shared conventions

| Convention | Meaning |
|---|---|
| Score `1` | The property is explicitly and completely evidenced in the reviewed public material. |
| Score `0.5` | The property is partially represented, discussed without binding detail, or only indirectly evidenced. |
| Score `0` | The property is absent from the reviewed public material. |
| Empty cell | Unknown or not applicable. Unknown is never silently converted to zero; it is excluded from component means and reported separately. |
| `Source URL` | Canonical public discussion link. Reproduction does not fetch these URLs. |
| `Confidence`, `Coding confidence`, `Evidence confidence` | Coder confidence in the row, not statistical uncertainty. |
| `Interpretation` | The bounded reading the row supports. |
| `Invalid inference` | The specific overclaim the row must not be used to support. |
| `Positive case`, `Counterexample` | Marks evidence that runs against the expected bottleneck, retained to prevent a failure-only catalogue. |

Percentages derived from these files are bounded case-study results with explicit denominators. They do not estimate forum prevalence, operational incidence, industry frequency, or vendor reliability.

## Construct codes

| Code | Construct | Layer |
|---|---|---|
| B1 | Knowledge packaging and canonicalization | Ecosystem condition |
| B2 | Driver and interface accessibility | Interface / representation |
| B3 | Method, configuration, calibration, and runtime entanglement | Interface / representation |
| B4 | Incomplete physical-resource definitions | Interface / representation |
| B5 | Fragmented observability and evidence semantics | Runtime coordination |
| B6 | Partial execution and recovery | Runtime coordination |
| B7 | Scheduling requirements and capability ambiguity | Runtime coordination |
| B8 | Testing and validation semantics | Evaluation |
| B9 | AI context and physical-feedback gap | Emerging AI layer |
| B10 | Documentation, training, and support dependence | Ecosystem condition |

B1 and B10 are ecosystem conditions and become primary codes only when knowledge governance or support is the central object of the discussion.

## `data/derived/`

### `codebook.csv` (12 rows)

| Column | Definition |
|---|---|
| `Variable / rule` | The coding variable or rule being defined. |
| `Type` | Its form: exactly one, multi-label, ordinal, categorical, binary, or rule. |
| `Definition` | The operational definition applied during coding. |

### `taxonomy_rules.csv` (10 rows)

| Column | Definition |
|---|---|
| `Code` | Construct identifier B1 through B10. |
| `Construct` | Full construct name. |
| `Layer` | Analytical layer the construct belongs to. |
| `Include when` | Conditions under which the code applies. |
| `Exclude when` | Conditions that route the evidence to a different code. |
| `Primary-code eligibility` | When the code may be the single primary code for a thread or episode. |
| `Common adjacent codes` | Codes that legitimately co-occur. |
| `Required evidence` | Evidence that must be present before the code is assigned. |
| `Boundary test` | The counterfactual question used to separate this code from its neighbours. |
| `Pilot interpretation` | What the pilot evidence for this code does and does not support. |

### `evidence_register_part_01.csv`, `evidence_register_part_02.csv` (28 + 27 = 55 rows)

One row per selected thread. The two parts share identical headers and are concatenated in file order by `read_csv_many`.

| Column | Definition |
|---|---|
| `ID` | Stable thread identifier used across the release, including `reliability_subset.csv` and the episode register. |
| `Thread` | Public discussion title. |
| `Date` | Discussion date or date range. |
| `Category` | Forum category. |
| `Primary` | Exactly one construct code: the proximate obstacle that best explains the thread's central problem. |
| `B1` ... `B10` | Binary direct-support flags. `1` means the mechanism or consequence is directly evidenced, not merely topically related. Multi-label by design, so column sums exceed the row count. |
| `Evidence type` | Form of the evidence, for example incident, design discussion, product report, or documentation request. |
| `Resolution` | Public outcome class only: confirmed, partial, open, mixed, product-reported, or migrated. An open thread does not imply operational non-resolution. |
| `Public artifact / outcome` | Reusable artifact produced in public, such as a post-mortem, example, merged correction, or documentation path. |
| `External migration` | Binary flag for substantive work explicitly moving to a restricted channel. |
| `Evidence strength` | Ordinal 1 to 4, from contextual mention to detailed incident or measured report. |
| `Source URL` | Canonical discussion link. |
| `Analytical note` | Coder note recording the boundary decision. |

### `episode_register_part_01.csv`, `episode_register_part_02.csv` (23 + 22 = 45 rows)

One row per analytical episode from the 14-thread difficult subset.

| Column | Definition |
|---|---|
| `Episode ID` | Stable episode identifier. |
| `Thread ID` | Foreign key to `ID` in the evidence register. |
| `Thread` | Public discussion title. |
| `Episode summary` | The initiating problem for this episode. |
| `Lifecycle stage` | Where in the automation lifecycle the episode sits. |
| `Primary technical code` | Exactly one construct code for the episode. |
| `Ecosystem modifiers` | B1 or B10 conditions that modify the episode without being its object. |
| `Evidence form` | Form of the episode evidence. |
| `Detectability` | Whether the problem was detectable before its consequence, where applicable. |
| `Consequence / analytical outcome` | What the episode established. |
| `Resolution class` | Public outcome class, using the same vocabulary as the evidence register. |
| `Public artifact` | Reusable artifact produced by the episode. |
| `Counterexample` | Whether the episode challenges the expected bottleneck. |
| `Source URL` | Canonical discussion link. |
| `Coding confidence` | Coder confidence for the episode. |
| `Coding note` | Segmentation and boundary rationale. |

### `reliability_subset.csv` (14 rows)

The prepared hard-case adjudication set. It covers exactly the 14 threads that were segmented into episodes and is an instrument for an independent second coding pass, not a result. No agreement coefficient is reported anywhere in this release because no second coding exists.

| Column | Definition |
|---|---|
| `Thread ID` | Foreign key to `ID` in the evidence register. |
| `Thread` | Public discussion title. |
| `Expected primary` | The primary code assigned by the single coder. |
| `Plausible alternative` | The competing code or codes a second coder is most likely to choose. |
| `Why disagreement is likely` | The specific ambiguity in the thread. |
| `Specific adjudication question` | The question a second coder must answer to resolve the disagreement. |
| `Episode segmentation required` | Whether the thread must be split, and the expected number of episodes. |
| `Priority` | Adjudication priority: critical or high. |
| `Source URL` | Canonical discussion link. |

### `publication_claim_ledger.csv` (12 rows)

The review boundary for the project. `scripts/validate_release.py` and `scripts/check_claim_traceability.py` both read this file.

| Column | Definition |
|---|---|
| `Claim ID` | Stable identifier of the form `Cnn`. |
| `Proposed statement` | The claim as originally proposed. |
| `Claim class` | Descriptive corpus result, bounded case-study metric, source-reported quantitative claim, mechanism hypothesis with descriptive association, mixed qualitative and bounded metric, interpretive synthesis, or unsupported overclaim. |
| `Evidence source` | Register or metric file the claim rests on. |
| `Denominator / scope` | The explicit denominator and sampling scope. |
| `Safe wording` | The wording the manuscript is permitted to use. |
| `Prohibited overclaim` | The nearby statement the evidence cannot support. Required for every approved claim. |
| `Sensitivity / limitation` | The limitation that must travel with the claim. |
| `Figure / table` | Where the claim is displayed. |
| `Citation set` | Supporting discussions. |
| `Manuscript anchor` | A distinctive substring of the published wording that must appear in the LaTeX source marked with `% claim: Cnn`. Empty for non-approved claims. |
| `Status` | `Approved` or `Rejected`. Rejected claims must carry no manuscript marker and no anchor. |

### `evidence_atlas.csv` (10 rows)

One row per construct, summarising the pilot evidence. **Generated file.** Every cell is
either copied from another committed file or computed by `compute_release_results`; no cell
is authored in the atlas itself. Rebuild it with `make derived`, which `make validate`
then checks for drift.

For what a row means, how to trace a construct to its quotes, cases, and metrics, and what
the atlas does not support, read [Evidence atlas](evidence-atlas.md). For a browsable
rendering of all ten rows without a spreadsheet, read the generated
[Evidence atlas summary](generated/evidence_atlas_summary.md) (`docs/generated/evidence_atlas_summary.md`,
rebuilt with `make atlas-summary` and also checked for drift by `make validate`).

| Column | Definition |
|---|---|
| `Code`, `Bottleneck`, `Analytical layer` | Construct identity and layer, from `taxonomy_rules.csv`. |
| `Direct-support threads`, `Primary-code threads` | Register counts for the construct. |
| `Pilot interpretation` | What the pilot evidence supports, from `taxonomy_rules.csv`. |
| `Bounded quantitative result` | The construct's headline result with its denominator, and a Wilson interval where the result is a proportion. |
| `Strongest descriptive relationship` | The construct's largest phi in `pairwise_associations.csv`, or a note that the construct is outside the B2--B9 pairwise set. |
| `Short anonymized quotation`, `Quotation source` | Illustrative quotation and its discussion, from `quote_bank.csv`. |
| `Retained counterexample` | Cases in `negative_cases.csv` that challenge the construct. |
| `Key sources` | The three highest-evidence-strength supporting discussions. |
| `Evidence maturity` | How far the current evidence goes, and whether a Wilson interval is meaningful for it. |

### `association_annotations.csv` (28 rows)

The coder-authored reading of each B2--B9 code pair, kept separate from the counts so that
`pairwise_associations.csv` can be regenerated from the register without losing prose. Every
one of the 28 pairs must be present; a missing pair fails the build rather than producing a
blank reading.

| Column | Definition |
|---|---|
| `Code A`, `Code B` | The pair, in ascending construct order. |
| `Relationship class` | The coder's classification of the relationship. |
| `Interpretation` | The bounded reading the pair supports. |
| `Invalid inference` | The overclaim the pair must not be used to support. |

### `hypothesis_map.csv` (8 rows)

| Column | Definition |
|---|---|
| `Layer` | Analytical layer of the proposed mechanism. |
| `Source condition` | The proposed antecedent condition. |
| `Proposed effect` | The proposed consequence. |
| `Target construct` | Construct the effect is expressed in. |
| `Forum evidence` | Qualitative evidence for the mechanism. |
| `Association support` | Descriptive association, where one exists. |
| `Measurement-overlap risk` | Whether the two instruments share components, which would inflate the association. |
| `Alternative explanation` | Competing account of the same pattern. |
| `Prospective observation` | Observation a prospective study would need. |
| `Falsification criterion` | The result that would refute the mechanism. |
| `Priority` | Research priority. |
| `Current confidence` | Confidence in the mechanism given pilot evidence. |
| `Study-safe wording` | Wording the manuscript may use. |

### `negative_cases.csv` (10 rows)

| Column | Definition |
|---|---|
| `Case` | Short case name. |
| `Expected bottleneck challenged` | The construct the case runs against. |
| `Observed mechanism` | What actually happened. |
| `Why it matters` | The analytical consequence. |
| `Residual limitation` | What the case does not settle. |
| `Evidence status` | Strength of the public evidence. |
| `Source URL` | Canonical discussion link. |
| `Research use` | How the case is used in the analysis. |

### `quote_bank.csv` (20 rows)

| Column | Definition |
|---|---|
| `Code`, `Bottleneck` | Construct the quotation illustrates. |
| `Short anonymized quotation` | Short quotation meeting the codebook's quote-eligibility rule. |
| `Attribution` | Role-level attribution only; user handles and profile attributes are excluded. |
| `Thread`, `Date`, `Source URL` | Provenance of the quotation. |
| `Analytical use` | The illustrative purpose. Quotations are never counted as quantitative observations. |

### `troubleshooting_template.csv` (25 rows)

The minimum reproducible automation question, in tabular form. The machine-readable version is `schemas/troubleshooting-question.schema.json`.

| Column | Definition |
|---|---|
| `Section` | Section of the question form. |
| `Field / question` | The field requested from the asker. |
| `Requirement level` | Universal, conditional, or optional. |
| `Why it matters` | The diagnostic purpose. |
| `Common missing-information failure` | What typically goes wrong when the field is absent. |
| `Bottleneck codes` | Constructs the field relates to. |
| `Suggested response format` | Expected answer shape. |
| `Example` | A concrete example answer. |
| `Applicable to` | Question types the field applies to. |
| `Evidence status` | Whether the field is evidence-backed or proposed. |

## `data/metrics/`

Each file contains the field-level cases underlying one bounded metric. Component columns use the shared `0 / 0.5 / 1 / empty` encoding; the derived score column is the mean over known components only.

### `b2_integration_access.csv` (6 rows) -- Integration Accessibility Score

Unit: one device--interface pair. Components: `Documentation`, `API / protocol`, `Licence clarity`, `Simulator / isolated testing`, `Examples / reference implementation`, `Maintainer / support`.

| Column | Definition |
|---|---|
| `Case`, `Device / interface` | Case identity and the scored interface. |
| `Known-component score` | Sum of known component scores. |
| `Unknown components` | Count of components excluded as unknown. |
| `IAS` | Mean over known components. Measures public accessibility conditions, not device reliability. |
| `Outcome`, `Positive case`, `Evidence note` | Public outcome, counterexample flag, and coder note. |
| `Source URL`, `Date relevance`, `Confidence`, `Invalid inference` | Provenance, currency of the evidence, coder confidence, and the prohibited reading. |

### `b3_reproducibility_manifest.csv` (3 rows) -- Reproducibility Manifest Completeness

Unit: one deployment object. Components: `Method / source`, `Libraries / submethods`, `Labware definitions`, `Liquid classes`, `Deck / layout`, `Teaching / calibration`, `Drivers / interfaces`, `Software / firmware`, `Checksums / IDs`, `Runtime / initialization`. A score of `1` requires explicit immutable binding.

| Column | Definition |
|---|---|
| `Case`, `Deployment object` | Case identity and the scored deployment object. |
| `Applicable fields` | Number of manifest fields applicable to this object. |
| `RMC` | Mean over applicable fields. |
| `Interpretation`, `Source URL`, `Confidence` | Bounded reading, provenance, and coder confidence. |

### `b4_physical_definitions.csv` (4 rows) -- Physical Definition Completeness

Unit: one physical-resource definition. Components: `Identity / part number`, `External geometry`, `Internal geometry`, `Material`, `Tolerance / variation`, `Coordinate semantics`, `Nesting / attachment`, `Operating properties`, `Provenance`, `Device validation`, `Independent reproduction`.

| Column | Definition |
|---|---|
| `Case`, `Resource definition` | Case identity and the scored resource. |
| `PDC` | Mean over known components. |
| `Evidence grade` | Ordinal 1 to 5: unspecified, declared, measured, device-validated, independently reproduced. Reported independently of `PDC`, because field completeness and evidence depth are distinct. |
| `Observed failure / use` | The failure or use that exposed the definition. |
| `Public correction` | Whether a correction was published. |
| `Interpretation`, `Source URL`, `Confidence`, `Invalid inference` | Bounded reading, provenance, coder confidence, and the prohibited reading. |

### `b5_observability.csv` (4 rows) -- Observability Coverage

Unit: one execution or diagnostic object. Components: `Run + config identity`, `Material / resource identity`, `Command`, `Acknowledgment`, `Physical observation`, `Modeled state change`, `Warning / failure`, `Human intervention`, `Recovery record`, `Final result / disposition`. Raw log volume is not scored.

| Column | Definition |
|---|---|
| `Case`, `Execution / diagnostic object` | Case identity and the scored object. |
| `OC` | Mean over known components. |
| `First divergence localized?` | Whether the first consequential divergence could be located from the available evidence. |
| `Ground-truth caveat` | Why the available evidence may still be insufficient. |
| `Outcome`, `Interpretation`, `Positive mechanism` | Public outcome, bounded reading, and any mechanism the case supports. |
| `Source URL`, `Confidence`, `Invalid inference` | Provenance, coder confidence, and the prohibited reading. |

### `b6_preflight_preventability.csv` (4 rows) -- Preflight Preventability Rate

Unit: one partial-execution scenario, eligible when at least one physical action completed before failure.

| Column | Definition |
|---|---|
| `Scenario`, `Thread` | Scenario identity and its discussion. |
| `Irreversible prefix completed` | The physical actions that completed before failure. |
| `Failure class` | Class of the failure. |
| `Preflight detectability` | `Yes`, `No`, or `Indeterminate`. The complete-case rate uses `Yes / (Yes + No)`; `Indeterminate` defines the sensitivity bounds instead of being imputed. |
| `Recovery evidence` | Public evidence about the recovery. |
| `Denominator status` | Whether the scenario enters the complete-case denominator. |
| `Coding rationale` | Why the detectability class was assigned. |
| `Source URL`, `Evidence confidence` | Provenance and coder confidence. |

### `b7_constraint_completeness.csv` (13 rows) -- Constraint Completeness

Unit: one requirement field of the scheduling toy problem. Opening completeness, missing-field discovery, and scenario-specific resolution are three distinct measures over this file.

| Column | Definition |
|---|---|
| `Requirement field` | The scheduling requirement class. |
| `Opening score (0/0.5/1)` | Completeness of the field in the opening post. The weighted opening completeness is the mean of this column. |
| `Present at opening?` | Whether the field appeared at all in the opening post. |
| `Identified in discussion?` | Whether replies surfaced the field. The discovery rate is computed over fields scoring below `1` at opening. |
| `Resolved with scenario-specific value?` | Whether replies produced a definitive value for the scenario, over the same denominator. |
| `Opening evidence` | What the opening post stated. |
| `Discussion evidence / unresolved issue` | What replies added or left open. |
| `Required for evaluation?` | Whether the field is needed to evaluate a schedule. |
| `Source URL`, `Coding confidence` | Provenance and coder confidence. |

### `b8_test_claim_alignment.csv` (6 rows) -- Test--Claim Alignment

Unit: one bounded claim. Elements: `Test object`, `Environment`, `Acceptance criterion`, `Observed evidence`, `Claim scope`.

| Column | Definition |
|---|---|
| `Case`, `Test / claim` | Case identity and the normalized claim under review. |
| `Element mean` | Mean over the five alignment elements. |
| `Alignment class` | `Aligned`, `Partial`, or a weaker class. A fully aligned claim requires all five elements to support the normalized statement. |
| `Deepest validation stage` | The deepest stage the evidence actually reached. |
| `Reasoning` | Why the class was assigned. |
| `Positive case` | Whether the case is a counterexample. |
| `Numerator eligibility` | Whether the case counts toward the fully aligned numerator. |
| `Recommended wording` | Narrower wording the evidence would support. |
| `Quote / evidence cue` | The evidence cue in the discussion. |
| `Source URL`, `Confidence`, `Invalid inference` | Provenance, coder confidence, and the prohibited reading. |

### `b9_context_expansion.csv` (22 rows) -- Context Expansion Ratio

Unit: one context class in the AI method-writing discussion. The ratio is a requirements-elicitation measure and is not a model error rate.

| Column | Definition |
|---|---|
| `Context class` | The material, physical, or process context class. |
| `Origin` | `Initial` for classes present in the opening framing, `Reply-added` for classes introduced by replies. Denominator of every ratio is the count of `Initial` classes. |
| `Core execution scope?` | Whether the class belongs to the core execution ontology. |
| `Broader deployment scope?` | Whether the class belongs to the broader deployment ontology. |
| `Counted in conservative grouping?` | Whether the class survives a conservative grouping that merges related concepts. |
| `Evidence summary` | What the discussion said. |
| `Forum location`, `Source URL` | Where in the discussion, and the canonical link. |
| `Coding confidence` | Coder confidence. |
| `Potential overlap` | Overlap with another class that would affect granularity. |
| `Analytical note` | Coder note. |

### `b10_documentation_profile.csv` (12 rows) -- Documentation profile

Unit: one documentation-centered case. Subtype columns: `Absence`, `Access / restriction`, `Discoverability`, `Currency / version`, `Detail / completeness`, `Terminology / semantics`, `Examples / templates`, `Training / mentoring`, `Support responsiveness`.

| Column | Definition |
|---|---|
| `Case`, `Thread` | Case identity and its discussion. |
| `Initial blocker central?` | Whether the documentation subtype was the central initial blocker. |
| `Public outcome` | The public outcome of the case. |
| `Actionable public resolution` | `Yes`, `Partial`, or `No`. The headline rate counts `Yes`; the partial-or-better rate counts `Yes` and `Partial`. |
| `Private migration` | `Yes`, `Partial`, or `No` for work moving to a restricted channel. |
| `Interpretation`, `Source URL`, `Date`, `Confidence`, `Invalid inference` | Bounded reading, provenance, date, coder confidence, and the prohibited reading. |

### `b2_b10_matched_cases.csv` (5 rows) -- B2/B10 convergent validity

Unit: one case that appears in both the B2 integration-accessibility set and the B10
documentation set. The table restates the two source rows side by side so that the
documentation profile of an integration case can be read without joining files by hand.
Every column is checked against its source file, so this table cannot drift into a second
version of either metric. It supports no separate quantitative claim: with five matched
cases it is a convergent-validity display, not a rate.

| Column | Definition |
|---|---|
| `Matched case`, `Thread` | Identifier of the pairing and its discussion. |
| `B2 case`, `B10 case` | The rows being matched in each source file. |
| `Device / interface` | Copied from the B2 row. |
| `IAS` | Integration Accessibility Score, copied from the B2 row. |
| `Documentation subtypes at full weight` | The B10 subtypes scoring `1` for the case. |
| `Actionable public resolution`, `Private migration` | Copied from the B10 row. |
| `Shared instrument components` | The components both instruments score, which is why the pairing cannot be read as independent corroboration. |
| `Convergent reading` | The bounded reading the pairing supports. |
| `Invalid inference` | The prohibited reading. |
| `Source URL` | Canonical discussion link, copied from the B10 row. |

### `ai_validation_funnel.csv` (7 rows)

One row per validation stage of the source-reported AI method-generation result. `scripts/build_figures.py` reads this file to draw the funnel; the `Generation efficiency` row is excluded from the figure because its denominator differs from the success test.

| Column | Definition |
|---|---|
| `Stage` | The validation stage. |
| `Evidence reported` | What the source reported for the stage. |
| `Numerator`, `Denominator`, `Rate` | The reported counts and rate, empty when no denominator was reported. |
| `95% Wilson low`, `95% Wilson high` | Wilson score interval for the reported rate, recomputed by `labauto_observatory.metrics.wilson_interval`. |
| `Evidence status` | `Feature description`, `Product-reported qualitative`, `Product-reported quantitative`, or `Not reported`. |
| `Supported claim` | The claim the stage evidence supports, and its limit. |
| `Source URL` | Canonical discussion link. |

### `pairwise_associations.csv` (28 rows)

All 28 pairs among B2 through B9, computed from the 55-thread direct-support matrix. Associations are descriptive; multi-label coding, purposive selection, and thread dependence preclude population or causal interpretation.

**Generated file.** Every numeric column is recomputed from `evidence_register_part_*.csv`, and the three prose columns are joined from `association_annotations.csv`. Rebuild it with `make derived`, which `make validate` then checks for drift.

| Column | Definition |
|---|---|
| `Rank order` | Rank by phi coefficient. |
| `Code A`, `Code B` | The construct pair. |
| `N(A)`, `N(B)` | Direct-support counts for each code. |
| `Overlap`, `Union` | Threads supporting both codes, and either code. |
| `Jaccard` | `Overlap / Union`. |
| `Lift` | Observed co-occurrence over the product of marginals. |
| `Phi` | Phi coefficient for the two-by-two table. |
| `P(B\|A)`, `P(B\|not A)` | Conditional proportions within the selected register. |
| `Descriptive RR` | Ratio of the two conditional proportions. Descriptive only; empty when undefined. |
| `Phi if overlap −1`, `Phi if overlap +1` | One-thread recoding sensitivity, holding marginals fixed. |
| `Sensitivity width` | Width of that sensitivity range. |
| `Pilot threshold met?` | Whether the pair meets the prioritization rule of phi at least 0.30 and lift at least 1.50. The threshold has no inferential interpretation. |
| `Relationship class` | How the pair is treated: mechanism hypothesis, convergent validity, or not interpreted. |
| `Interpretation`, `Invalid inference` | Bounded reading and the prohibited reading. |

### `strong_relationships.csv` (5 rows)

The leading relationships after qualitative adjudication.

| Column | Definition |
|---|---|
| `Hypothesis` | The proposed mechanism. |
| `Pair`, `Overlap / 55`, `Phi`, `Lift`, `Descriptive RR` | The pair and its descriptive measures. |
| `One-thread phi range` | Phi range under one-thread recoding sensitivity. |
| `Episode evidence` | Episode-level evidence for the mechanism. |
| `Proposed mechanism` | The mechanism statement. |
| `Alternative explanation` | Competing account. |
| `Counterexample / limit` | Retained counterexample or boundary. |
| `Construct independence` | Whether the two instruments measure independently. |
| `Current status` | Evidence status of the hypothesis. |
| `Prospective falsifier` | The result that would refute it. |
| `Prospective metric` | The measurement a prospective study should record. |
| `Forum references` | Supporting discussions. |
| `Publication-safe conclusion` | The permitted wording. |

## `data/knowledge_index/`

### `schema_fields.csv` (18 rows)

Human-readable companion to `schemas/knowledge-index.schema.json`.

| Column | Definition |
|---|---|
| `Field` | Field name in the schema. |
| `Definition` | What the field records. |
| `Data type` | Field type. |
| `Requirement` | Required, conditional, or optional. |
| `Allowed values / format` | Permitted values or format. |
| `Quality check` | The check a maintainer applies. |
| `Maintainer responsibility` | Who keeps the field current. |
| `Why it exists` | The failure mode the field prevents. |
| `Example` | An example value. |

### `seed_records.csv`, `seed_records.yaml`, `seed_records.json` (10 records)

Ten validated resolved-knowledge records. The YAML and JSON files contain identical records and are validated against the schema by `make validate` and by `tests/test_schemas.py`. The CSV is a flattened review view.

| Column | Definition |
|---|---|
| `Record ID` | Stable record identifier, unique across the index. |
| `Problem` | The observable problem. |
| `Primary code` | Construct code for the problem. |
| `Systems / context` | Applicable systems and physical or process context. |
| `Root-cause status` | Confirmed, probable, competing, or unknown. Uncertainty is a state, not a defect to hide. |
| `Resolution / reusable lesson` | The bounded answer. |
| `Validation stage` | The deepest validation stage the answer reached. |
| `Evidence grade` | Evidence depth, so that a declared value never appears equivalent to a cross-machine reproduction. |
| `Public artifact` | Linked maintained artifact. |
| `Known limitation` | Applicability boundary. |
| `Maintainer / owner` | Accountable maintainer. |
| `Last verified` | Date of last verification, used to compute staleness. |
| `Forum provenance` | Originating discussion. The index links back to the discussion and never replaces it. |
| `Status` | Active, review due, disputed, superseded, or archived. |

### `example_question.yaml`

One worked instance of the minimum reproducible automation question, validated against `schemas/troubleshooting-question.schema.json`. Partial execution activates the conditional `physical_state_after_failure` and intervention requirements.

## `data/registry_examples/`

### `device_interface_registry_examples.yaml` (3 records)

Design-draft examples for the Roadmap 0.2 device-interface accessibility registry, not
wired into `make validate` or `make reproduce`. Validated against
`schemas/device-interface-registry.schema.json`. See
[Device-interface accessibility registry](device-interface-registry.md) for the field
groups and their rationale.

| Column | Definition |
|---|---|
| `record_id` | Stable identifier, pattern `DIR-YYYY-NNNN`. |
| `vendor`, `product`, `interface_identity`, `interface_class` | Identity of the device/interface case. |
| `documentation`, `api_protocol`, `licence_clarity`, `simulator_isolated_testing`, `examples_reference_implementation`, `maintainer_support_declared` | The six fixed accessibility-fact components, `0 / 0.5 / 1 / null` as elsewhere in this repository. |
| `unknown_components`, `accessibility_score` | Null-component count and the mean over known components. |
| `maintenance_status`, `last_activity_observed`, `last_verified`, `correction_status`, `record_steward` | Living maintenance facts, kept separate from the fixed accessibility snapshot. |
| `evidence_grade`, `evidence_confidence`, `evidence_note` | Evidence depth, coder confidence, and the supporting rationale. |
| `evidence_sources` | Public source URLs. |
| `known_limitations`, `prohibited_claims` | Explicit bounds and the downstream claims the record must not be used to support. |
| `supersedes`, `superseded_by` | Record lineage. |

## `docs/generated/`

### `evidence_atlas_summary.md`

A Markdown rendering of every row in `data/derived/evidence_atlas.csv`, one section per
construct. **Generated file.** Every value is copied verbatim from the atlas; rebuild it
with `make atlas-summary` (also run as part of `make derived`), which `make validate` then
checks for drift. See [Evidence atlas](evidence-atlas.md) for what a row means.

## Proposing changes

See [Contributing evidence and coding changes](contributing-evidence.md) for how to propose register, ledger, metric, or knowledge-index changes.
