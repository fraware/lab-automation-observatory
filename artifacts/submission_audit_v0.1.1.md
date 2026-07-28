# Submission audit v0.1.1

Audit date: 2026-07-28

This audit reflects the tip of `main` at the `v0.1.1` tag. It supersedes
[submission_audit_v0.1.0.md](submission_audit_v0.1.0.md) as the live record;
the v0.1.0 audit remains frozen as the historical snapshot for that tag.

## Automated checks

- 10 knowledge records validated against JSON Schema Draft 2020-12
- 11 approved claims validated against the publication claim ledger and traced
  to `% claim: Cnn` markers and `Manuscript anchor` substrings in the LaTeX
  source (`make claims` / `make validate`)
- 53 tests passed (`test_build_outputs.py`, `test_cli_and_io.py`,
  `test_metrics.py`, `test_published_values.py`, `test_schemas.py`,
  `test_traceability.py`)
- 98.51% branch-aware test coverage (floor enforced at 90% in
  `pyproject.toml`)
- `ruff check .` and `ruff format --check .` pass with no findings
- `mypy --strict src/labauto_observatory` passes with no findings
- headline results reproduced from committed data via
  `scripts/reproduce_results.py`
- figures (`make figures`) and LaTeX tables (`make tables`) regenerated and
  diffed against the committed copies under `paper/figures/*.pdf`,
  `paper/graphical_abstract.{pdf,png}`, and `paper/generated/*.tex`: **no
  diff**, confirming the deterministic-regeneration contract described in
  [REPRODUCIBILITY.md](../REPRODUCIBILITY.md)
- `mkdocs build --strict` (`make docs-build`) succeeds with no warnings
  escalated to errors

## Document checks

Local document compilation was attempted and is **blocked in this
environment**, not by the manuscript source:

- `make paper-only` (`latexmk`) fails because the local MiKTeX installation
  cannot locate the `perl` script engine that `latexmk` requires
  (`MiKTeX could not find the script engine 'perl'`). This is the exact
  local-toolchain gap anticipated in [REPRODUCIBILITY.md](../REPRODUCIBILITY.md#windows-and-powershell):
  installing Strawberry Perl or TeX Live resolves it.
- A direct single-pass `pdflatex main.tex` (bypassing `latexmk`) also fails,
  on an unrelated local font-expansion/`microtype` configuration error
  (`pdfTeX error (font expansion): auto expansion is only possible with
  scalable fonts`), which is a property of this machine's MiKTeX font
  database, not of the manuscript.

Because of these local blockers, **automated PDF page counts and rendered
page inspection were not re-audited for v0.1.1**. This audit does not invent
or carry forward page numbers from the v0.1.0 audit. Source readiness for the
document build is instead evidenced by:

- the manuscript, supplement, and cover-letter LaTeX sources are unchanged in
  structure since the v0.1.0 audit (`paper/main.tex`, `paper/supplement.tex`,
  `paper/cover_letter.tex`);
- `make claims` confirms every approved claim keeps its manuscript binding;
- the supplement includes the **S4 hard-case adjudication set** section
  (`Hard-case adjudication set` in `paper/supplement.tex`), documenting
  `data/derived/reliability_subset.csv` for an independent second coding pass;
- the vector figures and generated tables consumed by LaTeX are committed and
  reproduce byte-identically (see above), so a fresh clone with a working TeX
  toolchain (`latexmk` with a resolvable `perl`) is expected to build the same
  PDFs documented in
  [submission_audit_v0.1.0.md](submission_audit_v0.1.0.md), modulo the content
  changes tracked in [CHANGELOG.md](../CHANGELOG.md).

Anyone re-running this audit on a machine with a working `latexmk` should
replace this section with fresh page counts and rendered-page inspection
results rather than trust the numbers above by default.

## Journal-fit checks

Unchanged from v0.1.0 at the source level (no journal-fit-relevant content
edits since that audit):

- Original Research structure present
- approximately 6,169 main-text words
- five figures and two tables in the main manuscript
- 39 references
- short title, author degree, affiliations, and correspondence metadata
  prepared
- cover letter aligned with `NexusXp: The Connected Lab`

These figures were not re-measured for v0.1.1 because they depend on a
successful PDF compile (see **Document checks** above); they are carried
forward from the last environment where `latexmk` ran successfully and should
be re-verified alongside the next full document build.

## Scope carried forward

Repo-only release. No journal portal upload, no GitHub Release PDF assets,
and no Zenodo/ORCID/DOI work are part of this audit; see
[paper/submission_checklist.md](../paper/submission_checklist.md) for the
human/portal steps that remain outside this repository's automation.
