# Submission audit v0.1.3

Audit date: 2026-07-29

This audit reflects the tip of `main` prepared for the `v0.1.3` release. It
supersedes [submission_audit_v0.1.2.md](submission_audit_v0.1.2.md) as the live
record; the v0.1.0, v0.1.1, and v0.1.2 audits remain frozen as the historical
snapshots for their tags.

Unlike v0.1.2, this release includes **claim-affecting register corrections**
(direct-support flag updates, thread 2 primary re-code under the new tie-break,
and regenerated association statistics). The manuscript sources and golden tests
were updated in the same change set; recompiling the PDF before any external
submission is mandatory even though this audit did not repeat a full TeX build.

## Automated checks

- 10 knowledge records validated against JSON Schema Draft 2020-12
- 11 approved claims validated against the publication claim ledger and traced
  to `% claim: Cnn` markers and `Manuscript anchor` substrings in the LaTeX
  source (`make claims` / `make validate`)
- 30 release CSVs structurally validated by
  `labauto_observatory.register_validation`, including the new
  `reliability_subset_blind.csv` drift check, episode-to-thread coherence
  (every episode primary and ecosystem-modifier code must carry direct support
  on that episode's thread), exact episode-count checks against the episode
  register, the device-interface registry seed invariants via
  `labauto_observatory.registry`, and run-event example streams via
  `labauto_observatory.run_events`
- 192 tests passed (`test_atlas_summary.py`, `test_blind_subset.py`,
  `test_build_outputs.py`, `test_cli_and_io.py`, `test_derived_artifacts.py`,
  `test_latex.py`, `test_metrics.py`, `test_published_values.py`,
  `test_register_validation.py`, `test_registry.py`, `test_release_metadata.py`,
  `test_run_events.py`, `test_schemas.py`, `test_traceability.py`), up from 128
  at v0.1.2
- 96.20% branch-aware test coverage (floor enforced at 90% in
  `pyproject.toml`); 1,212 statements and 418 branches, 33 statements and 27
  partial branches uncovered
- `ruff check .` passes with no findings across 76 files; `ruff format --check .`
  passes after formatting `registry.py` and `test_release_metadata.py`
- `mypy --strict src/labauto_observatory` passes with no findings in 14 source
  files (up from 11 at v0.1.2)
- headline results reproduced from committed data via
  `scripts/reproduce_results.py`
- `mkdocs build --strict` (`make docs-build`) succeeds; the Material for MkDocs
  upstream warning about MkDocs 2.0 is informational and does not fail the build

## Determinism

`make derived`, `make validate`, `make test`, and `make docs-build` were run
against the working tree at audit time. The four generated artifacts
(`pairwise_associations.csv`, `evidence_atlas.csv`,
`reliability_subset_blind.csv`, `docs/generated/evidence_atlas_summary.md`)
regenerate without drift; `make validate` confirms content equality for each.

## Document checks

The v0.1.2 audit recorded a successful local compile (28-page main text,
8-page supplement, 1-page cover letter). This audit **did not re-run** `pdflatex`
or `latexmk`: the register and association updates in v0.1.3 touch
`paper/sections/04_results.tex`, claim ledger row C06, and generated LaTeX
tables, and those sources must be recompiled and visually checked before any
portal submission. The MiKTeX/`latexmk` toolchain gap documented in
[REPRODUCIBILITY.md](../REPRODUCIBILITY.md#windows-and-powershell) is unchanged.

## Bibliography

`build/cite_check.py` reports 36 `.bib` entries, 36 distinct cited keys, and
**zero uncited keys**. The three forum sources removed in this release
(`forum_contamination_tracking`, `forum_labware_database`, `forum_plr_zheight`)
no longer appear in `paper/references.bib`; the compiled bibliography and the
`.bib` file now agree at 36.

## Claim scope

v0.1.3 **does** change one published association statistic: the B2--B7 phi
coefficient falls to 0.382 (lift 2.037, sensitivity width 0.288--0.476) after
direct-support flag corrections and thread 2's primary re-code. Claim ledger row
C06, `paper/sections/04_results.tex`, `data/metrics/strong_relationships.csv`,
and `tests/test_published_values.py` were updated together. The pair remains
above the pilot attention threshold and keeps its enabling-condition reading.

No new approved claims were added; the ledger still carries 11 approved claims.
The study remains a single-coder pilot and still reports no agreement statistic.
Second coders must use `data/derived/reliability_subset_blind.csv` only.

## Version metadata

Release version `0.1.3` is declared consistently in `pyproject.toml`,
`CITATION.cff`, `codemeta.json`, `.zenodo.json`, `uv.lock`, and
`CHANGELOG.md`. `labauto_observatory.__version__` reads from the installed
distribution and is checked by `tests/test_release_metadata.py`.

## Scope carried forward

Repo-only release preparation. No journal portal upload, no Zenodo deposit, no
DOI, no ORCID registration, no git tag, no push, and no GitHub Release PDF
assets are part of this audit; see
[paper/submission_checklist.md](../paper/submission_checklist.md) and
[external_submission_actions.md](external_submission_actions.md) for the human
and portal steps that remain outside this repository's automation.

The `Docs site` workflow (`.github/workflows/pages.yml`) is present for manual
dispatch but has not been run; no GitHub Pages URL is asserted yet.
