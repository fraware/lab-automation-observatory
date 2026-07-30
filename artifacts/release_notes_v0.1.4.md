# v0.1.4 release notes

Release-blocker remediation for the SLAS publication gate (issue #13). Repairs
the broken supplement/table test contract, commits the 24-row source/quotation
audit ledger, bumps release metadata to 0.1.4, and records a measured freeze
including inspected PDFs. It does **not** start DOI, Zenodo, preprint, or
Editorial Manager work (issue #8).

Content freeze SHA: `c860747e7a8d4ae002ba2df250c224fc2d63a85f`  
Tag intent: `v0.1.4-rc1`  
Bundle manifest: [submission_bundle_manifest_v0.1.4.yaml](submission_bundle_manifest_v0.1.4.yaml)

## Why this release

1. `tests/test_build_outputs.py` still expected only two supplement table
   inputs after PR #14 added three robustness tables, so `make test` failed on
   checked-in source alone.
2. Robustness `.tex` files were existence-checked but not byte-synced to a fresh
   `build_robustness_tables` run; the denominator builder also had a latent
   `str.join` arity bug exposed by the new sync fixture.
3. Gate 1 required a machine-readable 24-record source/quotation audit ledger
   that was never committed.
4. Issue #11 still pointed independent coders at the answer-bearing
   `reliability_subset.csv`.

## What changed

- Supplement inventory expects five generated stems; robustness-table sync and
  B6 denominator mutation tests land beside the existing partial-score and
  leave-one-out mutation coverage.
- `data/derived/source_quote_audit.csv` (24 rows) plus
  `tests/test_source_quote_audit.py`, data-dictionary documentation,
  `EXPECTED_ROW_COUNTS`, and `validate_release` presence checks.
- Version `0.1.4` across `pyproject.toml`, `uv.lock`, `CITATION.cff`,
  `codemeta.json`, `.zenodo.json`, and the submission manifest template;
  CHANGELOG cut; README Markdown H1 restored above the ASCII banner.
- Issue #11 edited to require only `reliability_subset_blind.csv`.

## Measured checks (2026-07-30)

- Host: Windows 11, Python 3.13.11; `uv sync --frozen --all-extras` green
- 205 tests passed; 95.73% branch-aware coverage
- 31 release CSVs + 3 robustness artifacts validated
- 24 source-quote audit records
- `mkdocs build --strict` green; clean worktree after `make derived`
- PDFs (MiKTeX `pdflatex`/`bibtex`): main 29 pp, supplement 10 pp, cover letter
  1 pp, graphical abstract 1 pp; **zero Type 3 fonts**; extractable text OK

Measured detail and SHA-256 digests:
[submission_audit_v0.1.4.md](submission_audit_v0.1.4.md).
