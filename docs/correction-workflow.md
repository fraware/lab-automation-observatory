# Correction workflow

This page defines how a correction to a coded row, a metric input, a published claim, or a
knowledge-index record moves from a report to a merged change. It is the correction-specific
companion to [Contributing evidence and coding changes](contributing-evidence.md), which covers
the mechanics of each change type, and to [CONTRIBUTING.md](https://github.com/fraware/lab-automation-observatory/blob/main/CONTRIBUTING.md),
which covers pull-request requirements. [GOVERNANCE.md](https://github.com/fraware/lab-automation-observatory/blob/main/GOVERNANCE.md)
sets the roles and the immutability rule this page assumes.

A correction fixes something already in the release: a wrong code, a wrong score, a stale
source, a wrong claim boundary, a stale knowledge record. It is not the same as an addition
(a new thread, episode, or record) or a taxonomy proposal; both of those already have their own
sections in `docs/contributing-evidence.md` and follow the same checks but a different review
question. Use the [evidence-correction issue template](https://github.com/fraware/lab-automation-observatory/blob/main/.github/ISSUE_TEMPLATE/evidence-correction.yml)
to report a correction before opening a pull request.

## Accepted correction kinds and minimum evidence

| Kind | What it changes | Minimum evidence required |
|---|---|---|
| Coded-row correction | `Primary`, a `B1`-`B10` direct-support flag, `Resolution`, `Evidence type`, or `Evidence strength` in `evidence_register_part_*.csv` | The exact boundary test from `data/derived/taxonomy_rules.csv` the current code fails, quoted; the public passage the corrected code rests on; a rewritten `Analytical note` recording the reasoning. |
| Episode correction | A field in `episode_register_part_*.csv`, including re-segmentation | The public passage for the corrected episode; a restated boundary test for `Primary technical code` or `Lifecycle stage`; confirmation of whether the thread stays in `reliability_subset.csv`. |
| Metric-input correction | One row or component cell of a `data/metrics/*.csv` file | A public source URL for the corrected value; for a component score, which of `0 / 0.5 / 1 / empty` applies and why, under the shared scoring convention in [the data dictionary](data-dictionary.md). |
| Published-claim correction | A row in `data/derived/publication_claim_ledger.csv` | The `Evidence source` file or row the claim now rests on; a restated `Denominator / scope`; a non-empty `Prohibited overclaim`. |
| Knowledge-index correction | A record in `seed_records.yaml` / `seed_records.json` | A newer or better public source. A correction that changes the answer supersedes the record through explicit lineage; it does not overwrite the prior record. |
| Taxonomy or schema correction | `taxonomy_rules.csv`, `codebook.csv`, or a file under `schemas/` | The construct(s) affected, the new inclusion / exclusion / boundary test, and which coded rows would move under the new rule. |
| Provenance-only correction | `Source URL`, coder attribution, `Last verified` date, or maintainer name | The replacement value itself. No new evidentiary argument is required because no interpretation changes. |
| Wording or note-only correction | Prose fields that carry no computed value: `Analytical note`, `Coding note`, `Interpretation`, or documentation prose | The corrected text. Must not introduce a new claim, code, or score under cover of a wording fix. |

A correction that would add prevalence, market-share, vendor-reliability, or causal-effect
wording, or that would present a simulation result as a wet-lab or device-validated result, is
declined regardless of how it is filed. The declined list in `docs/contributing-evidence.md`
applies to corrections exactly as it applies to new material.

## Which files usually move together

| Kind | Files that usually move together |
|---|---|
| Coded-row correction | The register part file; the same thread's rows in `episode_register_part_*.csv` and `reliability_subset.csv` if it is one of the 14 hard threads; `data/derived/pairwise_associations.csv` and `data/derived/evidence_atlas.csv` after `make derived`; the literals in `tests/test_published_values.py` if any count moves; `paper/generated/*` and `paper/figures/*` after `make tables` and `make figures`; a `CHANGELOG.md` `Unreleased` entry. |
| Metric-input correction | The one `data/metrics/*.csv` file; `data/metrics/b2_b10_matched_cases.csv` if the row is a matched case; `tests/test_published_values.py`; `paper/generated/*`, `paper/figures/*`; `publication_claim_ledger.csv` if the metric backs an approved claim's `Evidence source` or `Denominator / scope`. |
| Published-claim correction | `publication_claim_ledger.csv`; the manuscript file carrying the `% claim: Cnn` marker; `docs/claim-discipline.md` only if the approved-claim classes themselves change. |
| Knowledge-index correction | `seed_records.yaml` and `seed_records.json` together, which must stay identical; `seed_records.csv`, the flattened review view; the superseded record's `Status`. |
| Taxonomy or schema correction | `taxonomy_rules.csv` or `codebook.csv`; every register row whose `Primary` or direct-support flags move as a result; `docs/data-dictionary.md`. |
| Provenance-only correction | The single corrected field. No other file, unless the new source changes what evidence strength or resolution class the row can support, in which case it becomes a coded-row correction. |
| Wording or note-only correction | The single prose field or documentation page. No CSV that other checks depend on. |

## Checks that must pass

1. `make derived` first, whenever the corrected file is `evidence_register_part_*.csv`,
   `episode_register_part_*.csv`, `reliability_subset.csv`, `association_annotations.csv`, or any
   `data/metrics/*.csv`. `pairwise_associations.csv`, `evidence_atlas.csv`, and
   `reliability_subset_blind.csv` are computed from those sources, and `make validate` fails
   closed if any of them has drifted.
2. `make validate`, always. It checks documented row counts, the `0 / 0.5 / 1 / empty` score
   domain, categorical vocabularies, derived-score recomputation, the cross-file invariants
   (primary implies direct support, an episode's codes are a subset of its thread's
   direct-support flags, the adjudication set equals the episode-segmented subset,
   the B8 alignment class agrees with numerator eligibility, funnel intervals recompute), schema
   validation for the knowledge index, record-ID uniqueness, and claim traceability.
3. `make test` (`uv run pytest`), always. If the correction moves a published number,
   `tests/test_published_values.py` fails until its literals are updated in the same pull
   request. That failure is the expected signal that a downstream value must be revised, not a
   problem to route around.
4. `make tables` and `make figures`, whenever a changed value feeds a generated table or figure:
   the headline metrics table, the component heatmaps, the discovery/resolution matrix, the
   association phi matrix, the validation funnel, or an atlas export. Commit the regenerated
   `paper/generated/*` and `paper/figures/*`.
5. `make claims`, whenever the claim ledger, a `Manuscript anchor`, or a `% claim: Cnn` marker
   changes. It fails when an approved claim has no marker, when the anchor is missing from the
   manuscript, when the marker and the anchor sit in different files, or when a rejected claim is
   marked.
6. `make docs-build`, whenever a documentation page or the `mkdocs.yml` navigation changes.
7. `make ci` before merge for any correction that touches the register, the metrics, the claim
   ledger, or a schema. It chains lint, typecheck, `validate`, `test`, `docs-build`, and the
   manuscript, supplement, and cover-letter builds, so it is the single command that reproduces
   what the release pipeline will do with the correction applied.

A correction limited to a provenance field or a note (see the classification below) only needs
`make validate` and, if a doc changed, `make docs-build`; it will not change what `make test` or
`make tables` produce.

## Classifying the correction

Every correction falls into exactly one of three classes. The class determines which checks are
required and who signs off, per the roles in `GOVERNANCE.md`.

### Note-only

The correction changes no score cell, no categorical value that feeds `compute_release_results`,
no count, and no `Status` or lifecycle field that another check depends on. Examples: a typo in a
thread title, an `Analytical note` or `Coding note` rewrite, a `Source URL` correction that points
to the same content, a maintainer name or `Last verified` date update that does not change the
resolution the record reports.

- Required checks: `make validate`, plus `make docs-build` if a doc page changed.
- No entry in `tests/test_published_values.py`, `paper/generated/*`, or `CHANGELOG.md` is
  expected to change. If one does, the correction is not note-only; reclassify it.
- Can be merged by any maintainer once `make validate` passes.

### Claim-affecting

The correction changes a score cell, a categorical value that `compute_release_results` reads, a
`Primary` or direct-support flag, a resolution or evidence-strength value, or a
`publication_claim_ledger.csv` field (`Claim class`, `Denominator / scope`, `Safe wording`,
`Prohibited overclaim`, `Manuscript anchor`, `Status`). These values flow into a published number,
a table, a figure, or manuscript prose.

- Required checks: the full sequence in [Checks that must pass](#checks-that-must-pass) relevant
  to the changed files, ending in `make claims` if the ledger or a manuscript anchor moved.
  `tests/test_published_values.py` literals must be updated in the same pull request.
  `CHANGELOG.md` gets an `Unreleased` entry naming the value that moved and why.
- Requires a domain reviewer or the project steward, per `GOVERNANCE.md`, in addition to the data
  steward who reviews the evidence itself.
- If the changed number is already published under a cut release tag (`vX.Y.Z` in `CHANGELOG.md`),
  the correction lands as a new release, not a retroactive edit. Release tags are immutable.

### Release-blocking

The correction is required because leaving the current state unfixed breaks an invariant that
`scripts/validate_release.py`, `labauto_observatory.register_validation`, or
`tests/test_published_values.py::test_result_schema_is_stable` enforces. Examples: a row-count
mismatch, a primary code with no matching direct-support flag, an episode primary code or
ecosystem modifier with no direct-support flag on its own thread, the adjudication set diverging from
the episode-segmented subset, an approved claim with an empty `Prohibited overclaim` or a missing
manuscript anchor, a duplicate knowledge-index `record_id`, or a generated CSV that has drifted
from `make derived`.

- Required checks: `make ci` must pass before merge. A release-blocking correction cannot be
  deferred to a later pull request; `main` should not carry a known invariant violation.
- Requires the project steward's sign-off, because a release-blocking correction changes what
  "the current validated baseline" (see the audit artifacts under `artifacts/`) means.
- If the invariant break was already present in a cut release, document it in a fresh audit note
  rather than silently rewriting the frozen one.

## Maintainer checklist

The one-page version of this section is [`artifacts/maintainer_correction_checklist.md`](https://github.com/fraware/lab-automation-observatory/blob/main/artifacts/maintainer_correction_checklist.md).

1. Confirm the pull request names the exact record, claim, metric, or file affected, and links a
   public source, per the [pull-request template](https://github.com/fraware/lab-automation-observatory/blob/main/.github/pull_request_template.md).
2. Classify the correction as note-only, claim-affecting, or release-blocking using the section
   above, and confirm the required checks for that class actually ran.
3. Confirm the files that usually move together for that correction kind either all moved, or the
   pull request explains why one of them did not need to.
4. For a claim-affecting or release-blocking correction, confirm `tests/test_published_values.py`
   was updated to the new values rather than loosened or skipped.
5. Confirm `Unknown` was not converted to `0`, and that a counterexample or a disputed record was
   not quietly dropped instead of being marked `disputed` or superseded with lineage.
6. Merge only when `make validate` (note-only) or `make ci` (claim-affecting or release-blocking)
   is green on the pull request's own branch, not on a stale local run.
