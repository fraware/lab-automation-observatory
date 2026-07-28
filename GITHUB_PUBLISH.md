# GitHub publication model

The source-first v0.1.0 repository is published directly through GitHub's Git-data API and does not require hosted Actions.

## Authoritative validation

Run locally:

```bash
uv sync --all-extras
make ci
```

The manual-only workflow templates under `.github/workflows/` are optional. They consume no Actions minutes unless explicitly dispatched.

## Archival release

1. Deposit the versioned source package and compiled manuscript assets in Zenodo.
2. Confirm metadata against `.zenodo.json` and `CITATION.cff`.
3. Reserve or publish the DOI.
4. Insert the DOI into citation metadata and the manuscript data-availability statement.
5. Record the archival DOI in a metadata-only patch release.

The local Git bundle and source ZIP preserve the audited v0.1.0 release candidate independently of GitHub-hosted runners.
