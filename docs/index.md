# Lab Automation Forum Bottleneck Observatory

This documentation accompanies the LaTeX paper, public derived data, bounded metric implementations, and community artifact schemas.

The central rule is simple. Every quantitative result must identify its unit, denominator, sampling frame, validation stage, and unsupported inference.

## Start here

- [Methods](methods.md)
- [Data dictionary](data-dictionary.md)
- [Evidence atlas](evidence-atlas.md) and its [generated summary](generated/evidence_atlas_summary.md)
- [Community artifacts](community-artifacts.md)
- [Claim discipline](claim-discipline.md)
- [Contributing evidence and coding changes](contributing-evidence.md)
- [Correction workflow](correction-workflow.md)

## Build these docs

```bash
uv sync --all-extras
make docs
```

`make docs` serves the site locally and `make docs-build` builds it with `--strict`.
