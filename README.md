# Lab Automation Forum Bottleneck Observatory

[![CI](https://github.com/fraware/lab-automation-observatory/actions/workflows/ci.yml/badge.svg)](https://github.com/fraware/lab-automation-observatory/actions/workflows/ci.yml)
[![Paper](https://github.com/fraware/lab-automation-observatory/actions/workflows/paper.yml/badge.svg)](https://github.com/fraware/lab-automation-observatory/actions/workflows/paper.yml)
[![REUSE status](https://api.reuse.software/badge/github.com/fraware/lab-automation-observatory)](https://api.reuse.software/info/github.com/fraware/lab-automation-observatory)

A reproducible mixed-methods study of public practitioner discussions about laboratory automation. The repository contains the LaTeX manuscript, derived coded data, bounded metric implementations, publication claim controls, and community artifacts designed to improve technical question quality and knowledge retention.

## What this repository establishes

The retained pilot covers **55 purposively selected public threads** and **45 analytical episodes** from a deliberately difficult subset. It identifies ten bottlenecks across five layers:

1. ecosystem knowledge and support;
2. interfaces and representations;
3. runtime coordination;
4. evaluation semantics;
5. AI-specific context and physical feedback.

The analysis reports only bounded case-study metrics with explicit units and denominators. It does **not** estimate industry prevalence, vendor reliability, market share, or comparative failure rates.

## Principal results

| Result | Pilot estimate | Unit |
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

The strongest technical association connects observability and recovery (`phi = 0.452`, `lift = 2.353`). The repository treats this as a prospective mechanism hypothesis, not a causal estimate.

## Repository map

```text
paper/                 LaTeX manuscript, supplement, figures, generated tables
src/labauto_observatory/  Metric and validation library
data/derived/          Public derived coding records
data/metrics/          Field-level metric inputs and association results
data/knowledge_index/  Seed resolved-knowledge records
schemas/               JSON Schemas for community artifacts
scripts/               Reproduction, figure, table, and validation commands
tests/                 Published-value, schema, and metric tests
docs/                  Methods, data dictionary, ethics, and artifact guides
artifacts/              Retained research workbook snapshot
```

## Reproduce the analysis

The ordinary reproduction path uses the committed derived data and does not access the forum.

```bash
git clone https://github.com/fraware/lab-automation-observatory.git
cd lab-automation-observatory
uv sync --all-extras
make reproduce
make test
make paper
```

The principal machine-readable summary is written to `build/results.json`. Figures are regenerated under `paper/figures/`, and LaTeX tables under `paper/generated/`.

## Build the paper

A TeX Live distribution with `latexmk`, `elsarticle`, and BibTeX is required.

```bash
make paper
```

The compiled manuscript is written to `paper/main.pdf`. The source follows the Elsevier `elsarticle` structure used for an SLAS Technology Original Research submission. The checked-in manuscript remains venue-adaptable; journal-specific metadata can be changed without altering the analysis.

## Community artifacts

The study produces three immediately usable artifacts.

- `data/derived/troubleshooting_template.csv` defines a minimum reproducible laboratory-automation question.
- `schemas/knowledge-index.schema.json` defines a governed resolved-knowledge record.
- `data/knowledge_index/seed_records.yaml` provides ten validated seed records linked to their forum provenance.

These artifacts should be evaluated through clarification burden, time to actionable answer, repeated-question frequency, record staleness, and final-disposition completeness.

## Data scope and ethics

This repository contains derived codes, short anonymized quotations, and source links. It does not redistribute a verbatim forum corpus or user handles. Public outcomes can be censored when work moves to private support, direct messages, meetings, or local implementations. See [ETHICS.md](ETHICS.md), [DATA_USE.md](DATA_USE.md), and [docs/methods.md](docs/methods.md).

## Citation

See [CITATION.cff](CITATION.cff) and `paper/references.bib`. A DOI field will be added when the first Zenodo release is archived.

## Licensing

- Code is licensed under Apache-2.0.
- Original documentation and derived data are licensed under CC BY 4.0.
- Forum content remains owned by its original contributors; only short quotations and factual provenance links are included.

See `LICENSE`, `LICENSES/`, and `REUSE.toml`.
