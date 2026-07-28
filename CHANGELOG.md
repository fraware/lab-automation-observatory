# Changelog

All notable changes follow Keep a Changelog principles.

## [Unreleased]

## [0.1.1] - 2026-07-28

### Added

- `uv.lock` pinning the full transitive dependency set, and a `docs` extra with MkDocs plus `make docs` and `make docs-build`.
- Machine-checked claim traceability: `labauto_observatory.traceability`, `scripts/check_claim_traceability.py`, and a `make claims` target. Every approved claim now needs a `% claim: Cnn` marker in the LaTeX source and a `Manuscript anchor` substring in the ledger.
- Golden tests for the secondary headline fields and the stable key set of `build/results.json`, content tests for the generated LaTeX tables, and smoke and determinism tests for the figure scripts.
- Supplementary section, methods pointer, and documentation for the hard-case adjudication set `data/derived/reliability_subset.csv`.
- Per-column definitions for every committed CSV in `docs/data-dictionary.md`, and a coding and evidence contribution guide at `docs/contributing-evidence.md`.
- Windows and PowerShell instructions in `REPRODUCIBILITY.md`, and a `make paper-only` target that builds the manuscript from committed figures without Python.
- `artifacts/submission_audit_v0.1.1.md` and `artifacts/release_notes_v0.1.1.md`, refreshing the audit record against the current test suite and claim ledger.
- `make links` for a local lychee link-check matching the CI scope, and a `docs-build` step in `make ci`.

### Changed

- Ran `ruff format` across the repository and aligned the pre-commit `ruff-pre-commit` hook with Ruff 0.16.0 from `uv.lock`.
- Retargeted the submission package to the SLAS Technology special issue `NexusXp: The Connected Lab`, with regular-journal transfer preference.
- Added complete submission metadata, journal-compliance checklist, and Editorial Manager copy-paste metadata.
- Added author degree to the manuscript and complete correspondence metadata to the submission package.
- Condensed the cover letter to one page and aligned it with the connected-laboratory scope.
- Committed the vector figures and the graphical abstract; the figure scripts now suppress output timestamps so regeneration on the locked environment is byte-identical. Only the raster previews `paper/figures/*.png` remain untracked.
- Drove the discovery--resolution and validation-funnel figures and the workflow figure counts from `compute_release_results` and `data/metrics/ai_validation_funnel.csv` instead of hardcoded arrays.
- Reused the shared `mean_score` and `weighted_completeness` helpers in `analysis.py` so unknown scores stay distinguishable from zero.
- Extended `build/results.json` with `episode_threads`, `adjudication_threads`, and `constructs` counts.
- Removed the unused `scipy` pin from `requirements.environment.txt` and documented that `uv.lock` is the authoritative install path.
- Aligned the coverage figure quoted in `README.md` with `artifacts/submission_audit_v0.1.0.md`, then repointed it at `artifacts/submission_audit_v0.1.1.md`.
- Bumped the pre-commit `pre-commit-hooks` revision past its deprecated `v4.6.0` pin.
- Extended the `.gitignore` figure-policy comment to note that `paper/graphical_abstract.png` is tracked alongside the PDF.

## [0.1.0] - 2026-07-28

### Added

- Venue-ready SLAS Technology LaTeX manuscript, supplement, highlights, cover letter, and graphical-abstract generator.
- Public derived datasets without user handles or a verbatim forum corpus.
- Executable metric, schema-validation, figure, and table reproduction code.
- Regression tests for all published headline values and JSON Schema tests for community artifacts.
- Minimum reproducible troubleshooting-question and resolved-knowledge-index schemas.
- Dual licensing, citation metadata, governance, ethics, data-use, security, and contribution policies.
- Manual-only workflow templates; authoritative validation is performed locally to avoid hosted-runner costs.
