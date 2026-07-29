# Evidence atlas

`data/derived/evidence_atlas.csv` is the one file to start from if you want a
single-page view of what this pilot found, one row per construct. This page
explains what a row means, how to trace it back to the primary evidence, and
what the atlas does not support. It complements, and does not replace, the
column-by-column reference in [Data dictionary](data-dictionary.md#evidence_atlascsv-10-rows).

If you just want to browse the ten rows, read the generated
[Evidence atlas summary](generated/evidence_atlas_summary.md) instead. It
renders the same CSV as Markdown so you do not need a spreadsheet.

Both pages are readable three ways: as Markdown in `docs/` on GitHub, as a
locally served site through `make docs`, and as a published site once a
maintainer dispatches the `Docs site` workflow that builds this documentation
for GitHub Pages. No deployment has happened yet, so this page does not link a
hosted URL; use `make docs` in the meantime.

## What the atlas is

Ten rows, one per construct (`B1` through `B10`), each summarizing the pilot
evidence for one named bottleneck in laboratory automation. It is a
**generated** file: every cell is either copied from another committed CSV
(`taxonomy_rules.csv`, `quote_bank.csv`, `negative_cases.csv`,
`pairwise_associations.csv`, the evidence register) or computed by
`compute_release_results`. No cell is authored directly in the atlas, so it
cannot drift into a second, inconsistent account of a number that already
exists elsewhere in the release. `make derived` rebuilds it, and `make
validate` fails if the committed file no longer matches what that rebuild
produces.

## What one row means

Read a row left to right as an answer to five questions:

1. **What is the construct, and where does it sit in the stack?**
   `Code`, `Bottleneck`, and `Analytical layer` name the construct and place
   it among the five analytical layers (ecosystem condition, interface /
   representation, runtime coordination, evaluation, and the emerging AI
   layer).
2. **How much of the corpus touches it?**
   `Direct-support threads` counts threads where the construct's mechanism or
   consequence is directly evidenced, out of the 55 selected threads.
   `Primary-code threads` counts threads where it is the single best
   explanation for the thread's central problem. These are corpus counts, not
   incidence rates — see [What this does not support](#what-this-does-not-support).
3. **What does the current evidence support, and what would be reading too
   much into it?**
   `Pilot interpretation` states the bounded reading; the `Invalid inference`
   column in `taxonomy_rules.csv` (not repeated in the atlas) states the
   overclaim it must not be used to support.
4. **What is the headline number, and over what?**
   `Bounded quantitative result` gives the construct's measured result with
   its explicit denominator and, where the result is a proportion, a Wilson
   interval. A percentage in this column is never a bare percentage: it
   always names the unit and the case count it was measured over. Where a
   result is not separately quantified (`B1`), the column says so instead of
   forcing a number.
5. **What is the evidence made of, concretely?**
   `Short anonymized quotation` and `Quotation source` give one illustrative
   quotation and the discussion it came from. `Retained counterexample` names
   cases in `negative_cases.csv` that run against the construct, so the atlas
   cannot become a failure-only catalogue. `Key sources` names the three
   highest-evidence-strength threads that directly support the construct.
   `Evidence maturity` states how far the evidence goes and whether a Wilson
   interval is meaningful for it at all.

## Tracing a construct to its primary evidence

The atlas is a summary layer over five other committed files. To go deeper on
any row:

| From this atlas column | Go to | To find |
|---|---|---|
| `Short anonymized quotation`, `Quotation source` | `data/derived/quote_bank.csv` | Every quotation for the construct, with attribution, date, source URL, and analytical use |
| `Retained counterexample` | `data/derived/negative_cases.csv` | The full case: observed mechanism, why it matters, residual limitation, and evidence status |
| `Key sources`, `Direct-support threads`, `Primary-code threads` | `data/derived/evidence_register_part_01.csv` and `_02.csv` | Every thread that supports the construct, with date, category, resolution, evidence strength, and source URL |
| `Bounded quantitative result` | the matching `data/metrics/b*.csv` file (for example `b2_integration_access.csv` for `B2`) | The field-level cases and component scores the headline number was computed from |
| `Strongest descriptive relationship` | `data/metrics/pairwise_associations.csv` | The full 28-pair table: phi, lift, overlap, sensitivity range, and the bounded interpretation of that specific pair |
| `Pilot interpretation`, `Analytical layer` | `data/derived/taxonomy_rules.csv` | The inclusion rule, exclusion rule, primary-code eligibility, adjacent codes, required evidence, and boundary test that produced the coding |
| Any row | `data/derived/episode_register_part_01.csv` and `_02.csv` | Episode-level detail, where the construct's thread was one of the 14 segmented into episodes |

Every one of those files carries a `Source URL` (or, for quotes, its own
provenance columns) back to the original public discussion. The atlas is a
lens onto that evidence, not a replacement for it — always follow the trail
back to the source before citing a number.

## What this does not support

- **No prevalence.** `Direct-support threads` and `Primary-code threads` are
  counts within a purposive 55-thread sample selected for conceptual
  coverage, not a random or exhaustive sample of forum activity. They cannot
  tell you how often a given failure occurs among practitioners, how common a
  bottleneck is in the field, or how discussion volume relates to operational
  incidence.
- **No vendor or product rankings.** Nothing in the atlas compares the
  reliability, quality, or market position of any device, driver, or
  platform. Metrics like the Integration Accessibility Score describe the
  public accessibility conditions of a small, named set of cases, not the
  instrument's reliability.
- **No causality from association.** `Strongest descriptive relationship`
  reports a descriptive statistical association (phi, lift) between two
  constructs' direct-support flags across the 55 threads. It is published as
  a mechanism *hypothesis*, with its own sensitivity range and alternative
  explanations recorded in `data/derived/hypothesis_map.csv`, not as evidence
  that one construct causes another.
- **No inter-rater agreement.** The coding behind every row is a
  single-coder pilot. `data/derived/reliability_subset.csv` is the prepared
  instrument for an independent second pass; no agreement statistic exists
  yet, and none is implied by anything in the atlas.
- **No claim beyond what the manuscript already approved.** Every
  quantitative statement that leaves this repository in the paper is bound to
  `data/derived/publication_claim_ledger.csv` and checked by `make claims`.
  If you want to cite an atlas number outside this repository, phrase it the
  way `Bounded quantitative result` phrases it — with its unit and
  denominator attached — rather than as a bare percentage.

See [Claim discipline](claim-discipline.md) for the full set of excluded
claim types, and [Methods](methods.md) for the corpus and coding rationale
behind the counts.

## Regenerating the atlas and its summary

```bash
make derived         # rebuilds evidence_atlas.csv and the Markdown summary
make atlas-summary   # rebuilds only the Markdown summary from the committed CSV
make validate        # fails if either has drifted from its committed state
```

Without GNU Make:

```bash
uv run python scripts/build_evidence_atlas.py
uv run python scripts/build_atlas_summary.py
uv run python scripts/validate_release.py
```
