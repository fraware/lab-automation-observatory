```
                                    __    ___    ____
                                 / /   /   |  / __ )
                                / /   / /| | / __  |
                                / /___/ ___ |/ /_/ /
                               /_____/_/  |_/_____/

              ___   __  ____________  __  ______  ______________  _   __
             /   | / / / /_  __/ __ \/  |/  /   |/_  __/  _/ __ \/ | / /
             / /| |/ / / / / / / / / / /|_/ / /| | / /  / // / / /  |/ /
            / ___ / /_/ / / / / /_/ / /  / / ___ |/ / _/ // /_/ / /|  /
            /_/  |_\____/ /_/  \____/_/  /_/_/  |_/_/ /___/\____/_/ |_/

            ____  ____ _____ __________ _    _____  __________  ______  __
           / __ \/ __ ) ___// ____/ __ \ |  / /   |/_  __/ __ \/ __ \ \/ /
          / / / / __  \__ \/ __/ / /_/ / | / / /| | / / / / / / /_/ /\  /
          / /_/ / /_/ /__/ / /___/ _, _/| |/ / ___ |/ / / /_/ / _, _/ / /
          \____/_____/____/_____/_/ |_| |___/_/  |_/_/  \____/_/ |_| /_/

          where laboratory automation work breaks - measured, not guessed
```

<p align="center">
  <a href="https://api.reuse.software/info/github.com/fraware/lab-automation-observatory"><img alt="REUSE status" src="https://api.reuse.software/badge/github.com/fraware/lab-automation-observatory"></a>
</p>

<p align="center">
  <a href="#what-you-get">What you get</a> &middot;
  <a href="#ten-bottlenecks-five-layers">Bottlenecks</a> &middot;
  <a href="#principal-results">Results</a> &middot;
  <a href="#reproduce-it">Reproduce</a> &middot;
  <a href="#contribute">Contribute</a>
</p>

Laboratory automation fails in specific, repeatable places: a driver that will not
talk to a device, a deck definition that omits a physical property, a run that
half-finishes and leaves no record you can reconstruct. Practitioners describe
those failures in public, in operational detail, and then the detail is lost in
the thread that produced it.

This repository turns a set of those public discussions into something you can
check, cite, reuse, and disagree with: a coded evidence base, metrics with
explicit denominators, and ready-to-use artifacts for asking better technical
questions and keeping the answers.

## What you get

- **A coded evidence base.** 55 purposively selected public threads and 45
  analytical episodes drawn from a deliberately difficult 14-thread subset, coded
  against written inclusion, exclusion, and boundary rules.
- **Ten named bottlenecks** across five layers of the automation stack, each with
  a definition you can argue with rather than a label you have to accept.
- **Bounded metrics** with the unit and denominator attached to every number, plus
  the raw field-level inputs behind them.
- **Artifacts you can adopt today** — a minimum reproducible question template, a
  governed record format for resolved knowledge, and ten seeded records.
- **A pipeline that reproduces itself.** One command recomputes every published
  value; the test suite fails if any of them drifts.

## Ten bottlenecks, five layers

| Layer | Code | Bottleneck |
|---|---|---|
| Ecosystem knowledge and support | B1 | Knowledge packaging and canonicalization |
| | B10 | Documentation, training, and support dependence |
| Interfaces and representations | B2 | Driver and interface accessibility |
| | B3 | Method, configuration, calibration, and runtime entanglement |
| | B4 | Incomplete physical-resource definitions |
| Runtime coordination | B5 | Fragmented observability and evidence semantics |
| | B6 | Partial execution and recovery |
| | B7 | Scheduling requirements and capability ambiguity |
| Evaluation semantics | B8 | Testing and validation semantics |
| AI context and physical feedback | B9 | AI context and physical-feedback gap |

Full inclusion rules, exclusion rules, and boundary tests live in
`data/derived/taxonomy_rules.csv` and are summarized in
[docs/methods.md](docs/methods.md).

## Principal results

| Metric | Pilot value | Measured over |
|---|---:|---|
| Integration Accessibility Score | 63.9% | six device–interface cases |
| Reproducibility Manifest Completeness | 54.2% | three deployment objects |
| Physical Definition Completeness | 67.0% | four resource definitions |
| Observability Coverage | 52.5% | four execution/diagnostic cases |
| Preflight Preventability | 66.7% | three definitely classified scenarios |
| Scheduling constraint discovery | 87.5% | eight incomplete requirement classes |
| Fully aligned test claims | 33.3% | six bounded claims |
| Core AI context-expansion ratio | 2.0× | five opening context classes |
| Fully actionable documentation outcomes | 41.7% | twelve documentation-centered cases |

**How to read this table.** Every figure describes the named set of cases in the
right-hand column and nothing else. The denominators are small on purpose: each
case was scored field by field against a written rubric, and the inputs are
committed so you can re-score them yourself. Read `54.2%` as "mean manifest
completeness across the three deployment objects we examined," not as a rate for
the field.

The strongest technical association in the pilot links fragmented observability
(B5) to partial execution and recovery (B6), with `phi = 0.452` and
`lift = 2.353`. We publish it as a mechanism hypothesis worth testing, not as a
causal estimate.

## What this study does not claim

Being useful here depends on being clear about the limits.

- **No prevalence.** A purposive sample of discussions cannot tell you how often
  anything happens in the field, and discussion counts are not incident counts.
- **No vendor rankings.** Nothing here supports a reliability, quality, or
  market-share comparison between products or suppliers.
- **No causality from co-occurrence.** Associations are reported as hypotheses.
- **No agreement statistic.** This is a single-coder pilot, so it reports none.
  Instead it publishes the hard cases where a second coder would most likely
  disagree, so that a real agreement number becomes possible later — see
  [Contribute](#contribute).

## Repository map

```text
paper/                    LaTeX manuscript, supplement, generated tables
src/labauto_observatory/  Metric and validation library
data/derived/             Public derived coding records
data/metrics/             Field-level metric inputs and association results
data/knowledge_index/     Seed resolved-knowledge records
schemas/                  JSON Schemas for community artifacts
scripts/                  Reproduction, figure, table, and validation commands
tests/                    Published-value, schema, and metric tests
docs/                     Methods, data dictionary, ethics, and artifact guides
artifacts/                Archive and provenance notes
```

## Reproduce it

Reproduction reads only the derived data committed in this repository. Nothing
queries the forum.

```bash
git clone https://github.com/fraware/lab-automation-observatory.git
cd lab-automation-observatory
uv sync --all-extras

make reproduce   # recompute every published value into build/results.json
make test        # assert published values, schemas, and generated outputs
make paper       # build the manuscript (needs TeX Live with latexmk)
```

`make reproduce` also writes a readable summary to `build/RESULTS.md`. Figures
land in `paper/figures/`, LaTeX tables in `paper/generated/`. Because the vector
figures and generated tables are committed, a fresh clone with only a TeX
distribution can build the paper through `make paper-only`, with no Python step.
`make ci` runs the whole battery — lint, types, schema validation, tests, docs,
and the PDF builds.

On Windows, GNU Make is not installed by default;
[REPRODUCIBILITY.md](REPRODUCIBILITY.md#windows-and-powershell) lists the
PowerShell equivalents, along with exactly which generated artifacts are tracked.

## Community artifacts

- `data/derived/troubleshooting_template.csv` defines a minimum reproducible laboratory-automation question.
- `schemas/knowledge-index.schema.json` defines a governed resolved-knowledge record.
- `data/knowledge_index/seed_records.yaml` provides ten validated seed records linked to forum provenance.
- `data/derived/reliability_subset.csv` is the prepared hard-case adjudication set for an independent second coding pass.

These artifacts should be evaluated through clarification burden, time to actionable answer, repeated-question frequency, record staleness, and final-disposition completeness.

## Claim control

Every approved claim in `data/derived/publication_claim_ledger.csv` carries a `% claim: Cnn` marker next to the manuscript passage it supports and a `Manuscript anchor` substring that must appear in that passage. `make claims` fails if a claim loses its manuscript binding and writes a review table to `build/claim_traceability.md`. See [docs/claim-discipline.md](docs/claim-discipline.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for pull-request requirements and [docs/contributing-evidence.md](docs/contributing-evidence.md) for how to propose register, metric, claim-ledger, or knowledge-index changes.

## Data scope and ethics

This repository contains derived codes, short anonymized quotations, and source links. It does not redistribute a verbatim forum corpus or user handles. Public outcomes can be censored when work moves to private support, direct messages, meetings, or local implementations. See [ETHICS.md](ETHICS.md), [DATA_USE.md](DATA_USE.md), and [docs/methods.md](docs/methods.md).

## Citation and licensing

See [CITATION.cff](CITATION.cff) and `paper/references.bib`. Code is Apache-2.0. Original documentation and derived data are CC BY 4.0. Forum content remains owned by its original contributors.
