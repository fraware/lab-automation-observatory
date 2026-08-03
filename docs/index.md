# Lab Automation Observatory docs

This site documents the public derived data, bounded metrics, claim boundaries, and community artifact schemas.

The central rule: every quantitative result must identify its unit, denominator, sampling frame, validation stage, and unsupported inference. See [CLAIM_BOUNDARIES.md](https://github.com/fraware/lab-automation-observatory/blob/main/CLAIM_BOUNDARIES.md).

## Documentation map

| Page | Use it for |
|---|---|
| [Methods](methods.md) | Corpus, coding, adjudication instrument, robustness outputs |
| [Data dictionary](data-dictionary.md) | Every column in every derived file |
| [Evidence atlas](evidence-atlas.md) | How to read one atlas row; [generated summary](generated/evidence_atlas_summary.md) |
| [Contributing evidence](contributing-evidence.md) | Add or change coded evidence and ledger rows |
| [Correction workflow](correction-workflow.md) | Fix something already in the release |
| [Device-interface registry](device-interface-registry.md) | Design draft and seed records (Roadmap 0.2) |
| [Run-event schema](event-schema.md) | Design draft for B5/B6 observability at the source |
| [Project](project.md) | Governance, ethics, data use, roadmap |

## Community artifacts (summary)

Adopt these from the repository:

- **Evidence atlas** — `data/derived/evidence_atlas.csv` and the [generated summary](generated/evidence_atlas_summary.md); see [Evidence atlas](evidence-atlas.md).
- **Troubleshooting question** — `schemas/troubleshooting-question.schema.json` and `data/derived/troubleshooting_template.csv`.
- **Resolved-knowledge index** — `schemas/knowledge-index.schema.json` and `data/knowledge_index/seed_records.yaml`.
- **Hard-case adjudication set** — blind sheet `data/derived/reliability_subset_blind.csv`; key `data/derived/reliability_subset.csv` (do not open the key for a second coding pass).
- **Planned registries** — [device-interface accessibility](device-interface-registry.md) and [run-event schema](event-schema.md).

Publication alone is not success. Judge artifacts on whether they reduce clarification rounds, keep validation stages honest, and get final outcomes recorded.

## Build these docs

```bash
uv sync --all-extras
make docs
```

`make docs` serves the site locally and `make docs-build` builds it with `--strict`.
