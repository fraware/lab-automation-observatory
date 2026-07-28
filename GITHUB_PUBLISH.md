# GitHub publication model

The source-first v0.1.0 repository is published directly through GitHub's Git-data API and does not require hosted Actions.

## Authoritative validation

Run locally:

```bash
uv sync --all-extras
make ci
```

The manual-only workflow templates under `.github/workflows/` are optional. They consume no Actions minutes unless explicitly dispatched.

## GitHub release assets

Tag the release and attach compiled manuscript PDFs, highlights, the graphical abstract, and `build/results.json` using the manual release workflow in `.github/workflows/release.yml`, or publish equivalent assets from a local `make ci` run.

Citation metadata lives in `CITATION.cff` and `codemeta.json`. The repository URL is the public access point for derived data, schemas, tests, and reproduction instructions.

The local Git bundle and source ZIP preserve the audited v0.1.0 release candidate independently of GitHub-hosted runners.
