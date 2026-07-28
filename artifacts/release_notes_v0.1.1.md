# v0.1.1 release notes

This is a repo-only polish release. It reconciles version metadata and audit
artifacts with the test suite, documentation, and tooling that were already
added on `main` after `v0.1.0`, and closes a handful of small tooling-debt
items. It does not change any published headline result, metric definition,
or manuscript claim.

## Included since v0.1.0

- `uv.lock` pinning the full transitive dependency set, and a `docs` extra
  with MkDocs plus `make docs` / `make docs-build`.
- Machine-checked claim traceability (`labauto_observatory.traceability`,
  `scripts/check_claim_traceability.py`, `make claims`), binding every
  approved claim to a `% claim: Cnn` marker and manuscript anchor.
- Golden tests for `build/results.json`, content tests for generated LaTeX
  tables, and smoke/determinism tests for the figure scripts, growing the
  suite from 17 to 53 tests.
- The **S4 hard-case adjudication set** supplementary section documenting
  `data/derived/reliability_subset.csv`.
- A per-column data dictionary (`docs/data-dictionary.md`) and a coding and
  evidence contribution guide (`docs/contributing-evidence.md`).
- Windows/PowerShell reproduction instructions and a `make paper-only`
  target that builds the manuscript from committed figures without Python.
- Committed vector figures and graphical abstract, regenerated
  byte-identically by `make figures` / `make graphical-abstract` on the
  locked environment.

## New in this release

- `artifacts/submission_audit_v0.1.1.md`, replacing the frozen
  `submission_audit_v0.1.0.md` as the live audit record.
- `make links` for a local link check matching the scope of
  `.github/workflows/link-check.yml`.
- `docs-build` added to `make ci` as a cheap integrity check on the MkDocs
  site.
- An extended `.gitignore` figure-policy comment clarifying that
  `paper/graphical_abstract.png` is tracked alongside the PDF.
- A non-deprecated `pre-commit-hooks` revision in
  `.pre-commit-config.yaml`.

## Validation

53 tests passed with 98.51% branch-aware coverage (floor: 90%), schema and
claim-ledger validation (10 knowledge records, 11 approved claims), and
deterministic figure/table regeneration with no diff against the committed
copies. `ruff`, `ruff format --check`, `mypy --strict`, and
`mkdocs build --strict` all pass. Full detail, including a local TeX-toolchain
blocker on this audit machine, is in
[submission_audit_v0.1.1.md](submission_audit_v0.1.1.md).

## Scope

Repo-only release: no journal portal submission, no GitHub Release PDF
assets, and no Zenodo/ORCID/DOI work. The release supports the same bounded
case-study and mechanism claims as v0.1.0; it does not support
industry-prevalence, causal-effect, market-share, or vendor-reliability
claims.

## Beyond this tag

The following remain documented next steps, outside this repository's
automation:

- Journal portal submission: NexusXp collection selection, author
  agreements, reviewer suggestions, and final portal-generated proof
  (see [paper/submission_checklist.md](../paper/submission_checklist.md)).
- Optionally attaching GitHub Release assets from a local `make ci` / paper
  build once produced on a machine with a working TeX toolchain.
- A second independent coding pass on
  `data/derived/reliability_subset.csv` before reporting any inter-rater
  reliability statistic.
- ROADMAP v0.2 and later (evidence-atlas site, registries, prospective
  studies).
