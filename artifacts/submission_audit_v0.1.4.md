# Submission audit v0.1.4

Audit date: 2026-07-30

This audit reflects the `release/v0.1.4` working tree prepared from
`origin/main` at `63ad4f0c6392cbce53eef89eb19f4a7c6eb88e1d`. It supersedes
[submission_audit_v0.1.3.md](submission_audit_v0.1.3.md) as the live record;
earlier audits remain frozen for their tags.

**Freeze status:** implementation and automated checks are complete on an
**uncommitted** working tree. No freeze commit or `v0.1.4-rc1` tag has been
cut yet. PDF inspection and a clean-worktree Linux/TeX Live rebuild remain
blocking for issue #13 closure.

## Automated checks (measured on this host)

- Host: Windows 11 (`Windows-11-10.0.26200-SP0`), Python 3.13.11
- `uv.lock` SHA-256:
  `2530d4d6b97a5d258ae1969e43a6887cc9204087c1484c3fe92c72cbe0efa1bd`
- `uv sync --frozen --all-extras`: blocked here by PyPI TLS
  (`invalid peer certificate: UnknownIssuer`); local `.venv` used offline via
  `uv run --offline`
- 10 knowledge records validated against JSON Schema Draft 2020-12
- 11 approved claims validated and traced to manuscript anchors
- **31** release CSVs structurally validated by
  `labauto_observatory.register_validation` (includes new
  `data/derived/source_quote_audit.csv` with 24 rows) plus 3 robustness
  artifacts
- **205 tests passed** (`uv run --offline pytest`), up from 192 at v0.1.3
- **95.73%** branch-aware coverage (90% floor); 1,358 statements and 446
  branches, 44 statements and 29 partial branches uncovered
- `mkdocs build --strict` succeeds (Material for MkDocs 2.0 advisory only)
- Robustness CSVs regenerated without drift; robustness `.tex` sync fixture
  passes; denominator mutation test passes
- Supplement inventory expects five table stems; all seven generated `.tex`
  files match fresh builds

## Determinism

`scripts/build_associations.py`, `build_evidence_atlas.py`,
`build_atlas_summary.py`, `build_blind_subset.py`, `build_robustness.py`, and
`build_robustness_tables.py` were run; `scripts/validate_release.py` reports
no drift afterward. Working tree remains dirty pending an explicit freeze
commit.

## Document checks

**Not certified on this host.** `pdflatex` / `latexmk` / GNU `make` were not
available in PATH. Manuscript, supplement, cover letter, and graphical-abstract
PDF rebuild and visual inspection (embedded fonts, zero Type 3, extractable
text, links, page counts) are **pending a Linux + TeX Live environment**.

## Source / quotation audit

`data/derived/source_quote_audit.csv` has 24 complete rows (`SQA-01` …
`SQA-24`). Every quote-bank entry and every manuscript `forum_*` /
`labautomation_*` bib key maps to exactly one row. Seven source-fidelity
quotation corrections are recorded as `applied: …` with approved wording
matching the current quote bank.

## Claim scope

No new claim-affecting scientific re-estimate beyond the PR #14 robustness
tables already on `main`. B2–B7 full-corpus phi remains **0.382** (issue #13
body table with 0.409 is superseded). Version metadata is consistently
`0.1.4`. DOI / preprint / ORCID remain null.

## Remaining blockers before closing issue #13

1. Commit the freeze tip and tag `v0.1.4-rc1` on a clean worktree.
2. Re-run `uv sync --frozen --all-extras` and `make ci` on Linux.
3. Rebuild and visually inspect all submission PDFs; populate page counts,
   font/Type 3 results, and artifact SHA-256s in a concrete manifest.
4. Only then close #13 and unblock issue #8 (DOI / Zenodo / portal).
