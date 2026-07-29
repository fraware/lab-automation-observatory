# v0.1.2 release notes

A patch release that hardens the data, the statistics, and the figures behind
the published numbers. It does not change any headline value, metric definition,
or manuscript claim. What changes is how much of the reasoning is checked by
machine and how much of the uncertainty is visible to a reader.

Three problems drove it:

1. two files the repository referenced were not actually derived from anything
   checkable, and one of them was not committed at all;
2. bounded proportions were published as bare point estimates, so a 2/3 rate and
   a 92/100 rate looked alike;
3. three main-text figures encoded more confidence than their denominators
   supported.

## Derived data now has one source of truth

- `data/metrics/pairwise_associations.csv` was maintained by hand and could
  disagree with the evidence register it summarises. All 28 B2--B9 pairs are now
  recomputed from the register by `labauto_observatory.associations`, and only
  the coder's reading of each pair stays authored, in the new
  `data/derived/association_annotations.csv`.
- `data/derived/evidence_atlas.csv` was referenced by the data dictionary, the
  workbook exporter, and claim-ledger rows C01 and C11, but had never been
  committed. It is now built by `labauto_observatory.atlas` from the taxonomy
  rules, the register, the quote bank, the negative cases, the pairwise table,
  and `compute_release_results`.
- `make derived` rebuilds both, `make reproduce` runs it first, and
  `make validate` fails if either has drifted from its sources. The drift check
  compares content rather than bytes, so a Windows checkout with CRLF line
  endings is not mistaken for a hand edit.
- `data/metrics/b2_b10_matched_cases.csv` publishes the B2/B10 convergent-validity
  comparison the manuscript implied, with every cell checked against its two
  source files and an explicit note that five matched cases make it a display
  rather than a rate.

## The register itself is now validated

`labauto_observatory.register_validation` runs inside `make validate` over all 29
release CSVs and asserts what the data dictionary and methods section already
state: documented row counts, score cells drawn only from 0, 0.5, 1, or an empty
unknown, categorical columns confined to their vocabularies, every derived score
recomputing from its own components, and the cross-file invariants. Mutation
tests break one invariant at a time and assert the reported problem, so the
checks are known to fail when they should.

## Uncertainty is reported, not implied

- `compute_release_results` returns `components` and `denominators` beside
  `metrics`. Every bounded proportion carries its numerator, its denominator, and
  a descriptive 95% Wilson interval. Component means carry their known-cell and
  unknown-cell counts instead, because a mean of ordinal component scores is not
  a binomial proportion.
- The headline metrics table gained a Wilson column; the strong-associations
  table gained the one-thread overlap sensitivity range.

## Figures state what they measure

- The metric dashboard is replaced by a component-level heatmap for B2--B5, which
  shows which parts of each rubric were actually observed instead of one bar per
  metric.
- The discovery bar chart is replaced by a three-stage requirement matrix.
- The association bar chart is replaced by the full 28-pair phi matrix, so the
  strongest pair is visible against the whole comparison it was selected from.
- The validation funnel draws only the one stage that has a denominator as a
  rate. Stages reported without one, and stages not reported at all, are drawn as
  bands across the whole axis, so "reported" cannot be read as a measured success
  rate.
- Two supplement figures are added: the B8 alignment matrix, and B6 preflight
  detectability beside its rate, interval, and sensitivity bounds.
- `scripts/figure_style.py` now owns print typography, the Okabe--Ito palette,
  deterministic saving, and the single taxonomy specification shared by the
  conceptual-model figure and the graphical abstract, so the two renderings
  cannot drift apart and an unknown score cannot be drawn like a zero.

## Manuscript and generated text

- All 20 short quotations are generated into `paper/generated/quotations.tex`
  through a fail-closed LaTeX escaper, replacing the ten previously typed into
  the supplement by hand. `labauto_observatory.latex` also fixes an escaper that
  escaped the braces of its own `\textbackslash{}` replacement.
- Captions for the rebuilt displays state the unit of each cell, the separate
  denominators behind each panel, and the readings the display does not license.
- Raised float fractions keep all seven main-text displays ahead of the
  bibliography; under the LaTeX defaults the component heatmap was rejected as a
  top float and deferred every later figure with it.

## Validation

128 tests pass with 98.84% branch-aware coverage (floor: 90%), up from 53 tests
at v0.1.1. Schema, claim-ledger, claim-traceability, and register validation all
pass, and the two derived CSVs, all eight figures, the four generated tables, and
the graphical abstract regenerate byte-identically against their committed
copies. `ruff`, `ruff format --check`, `mypy --strict`, and
`mkdocs build --strict` pass.

This is also the first release whose documents were compiled during the audit:
28-page main text, 8-page supplement, 1-page cover letter, no LaTeX warnings and
no undefined references. `latexmk` itself is still unavailable on the audit
machine, which is a local toolchain gap rather than a source problem; the detail
is in [submission_audit_v0.1.2.md](submission_audit_v0.1.2.md).

## Scope

Repo-only release: no journal portal submission, no Zenodo deposit, no DOI, no
ORCID registration, and no GitHub Release PDF assets. The release supports the
same bounded case-study and mechanism claims as v0.1.1; it does not support
industry-prevalence, causal-effect, market-share, or vendor-reliability claims.

## Beyond this tag

- An independent second coding pass on `data/derived/reliability_subset.csv`,
  before any inter-rater reliability statistic is reported. This remains the
  single largest methodological gap.
- Packaging the evidence atlas as an outward-facing artifact rather than a
  derived internal CSV.
- A documented public correction workflow for evidence and metric fixes.
- A bounded device-interface accessibility registry schema, seeded from the B2
  structures.
- Journal portal submission steps that stay outside repository automation, in
  [paper/submission_checklist.md](../paper/submission_checklist.md).
