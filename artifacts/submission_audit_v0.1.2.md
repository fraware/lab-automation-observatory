# Submission audit v0.1.2

Audit date: 2026-07-29

This audit reflects the tip of `main` at the `v0.1.2` tag. It supersedes
[submission_audit_v0.1.1.md](submission_audit_v0.1.1.md) as the live record;
the v0.1.0 and v0.1.1 audits remain frozen as the historical snapshots for
their tags.

Unlike the two audits before it, this one includes a **successful local document
build**. The MiKTeX font-expansion failure that blocked v0.1.1 was a missing
`cm-super` package on the audit machine, not a property of the manuscript; the
main text, supplement, and cover letter now compile locally, so page counts and
float placement are measured rather than carried forward.

## Automated checks

- 10 knowledge records validated against JSON Schema Draft 2020-12
- 11 approved claims validated against the publication claim ledger and traced
  to `% claim: Cnn` markers and `Manuscript anchor` substrings in the LaTeX
  source (`make claims` / `make validate`)
- 29 release CSVs structurally validated by
  `labauto_observatory.register_validation`, new in this release: documented row
  counts, score-cell domains, categorical vocabularies, derived-score
  recomputation, and the cross-file invariants (primary code implies direct
  support, the adjudication set equals the episode-segmented subset, the B8
  alignment class equals numerator eligibility, the funnel's Wilson columns
  match `metrics.wilson_interval`, and B7 has a non-empty incomplete-field
  denominator)
- 128 tests passed (`test_build_outputs.py`, `test_cli_and_io.py`,
  `test_derived_artifacts.py`, `test_latex.py`, `test_metrics.py`,
  `test_published_values.py`, `test_register_validation.py`, `test_schemas.py`,
  `test_traceability.py`), up from 53 at v0.1.1
- 98.84% branch-aware test coverage (floor enforced at 90% in
  `pyproject.toml`); 844 statements and 272 branches, 6 statements and 7 partial
  branches uncovered
- `ruff check .` and `ruff format --check .` pass with no findings across 59
  files
- `mypy --strict src/labauto_observatory` passes with no findings in 11 source
  files
- headline results reproduced from committed data via
  `scripts/reproduce_results.py`
- `mkdocs build --strict` (`make docs-build`) succeeds with no warnings
  escalated to errors

## Determinism

`make derived`, `make reproduce`, `make figures`, `make tables`, and
`make graphical-abstract` were run against the committed tip, and `git status`
was empty afterwards: the two derived CSVs, all eight figure PDFs, the four
generated LaTeX tables, and both graphical-abstract files regenerate
**byte-identically** to their committed copies. A second full regeneration
produced identical SHA-256 digests again, so the outputs are deterministic
across runs and not merely stable against the index.

The two committed derived CSVs are additionally drift-checked inside
`make validate`, by content rather than by bytes, because Git stores them with
LF and hands Windows working trees CRLF.

Two consecutive `pdflatex` passes over the settled auxiliary files produced
byte-identical `main.pdf` output (544,107 bytes both times).

## Document checks

All three documents compile locally:

| Document | Pages | Result |
|---|---:|---|
| `paper/main.pdf` | 28 | 0 LaTeX warnings, 0 undefined references or citations |
| `paper/supplement.pdf` | 8 | 0 LaTeX warnings |
| `paper/cover_letter.pdf` | 1 | 0 LaTeX warnings |

Float placement was checked page by page rather than assumed. All seven
main-text displays land on pages 7 through 18, ahead of the reference list on
page 25. This is what the raised float fractions in `paper/macros.tex` were for:
under the LaTeX defaults the component heatmap was rejected as a top float, and
a float rejected everywhere is deferred behind every later float until the
bibliography.

### Environment gap

`make paper`, `make paper-only`, and `make supplement` still fail on this
machine, because MiKTeX cannot find the `perl` script engine that `latexmk`
requires. The counts above were therefore produced by running the passes
`latexmk` would have run, directly:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex   # twice more
```

This is a local-toolchain gap, documented in
[REPRODUCIBILITY.md](../REPRODUCIBILITY.md#windows-and-powershell); installing
Strawberry Perl or TeX Live restores the Make targets. Nothing in the manuscript
sources depends on it.

## Journal-fit checks

Measured on the compiled `main.pdf` for this release rather than carried forward:

- Original Research structure present
- 5,772 words of narrative body text across the nine section files, excluding
  front matter, float contents, and captions; 8,093 words of extracted PDF text
  ahead of the reference list, which additionally includes the title block,
  abstract, keywords, table bodies, captions, and table notes
- five figures and two tables in the main manuscript, which is the display
  budget of seven now enforced by
  `test_main_text_holds_seven_figures_and_tables`
- three supplementary figures (validation-stage funnel, B8 alignment matrix, B6
  preflight preventability) and two generated supplementary tables (code counts,
  and all 20 short quotations)
- 36 entries in the compiled bibliography. Note that `paper/references.bib`
  holds 39 entries: `forum_contamination_tracking`, `forum_labware_database`,
  and `forum_plr_zheight` are retained forum sources that no current manuscript
  passage cites, so they do not appear in the reference list. The "39 references"
  figure in the v0.1.0 and v0.1.1 audits was the `.bib` entry count, not the
  rendered count.
- short title, author degree, affiliations, and correspondence metadata prepared
- cover letter aligned with `NexusXp: The Connected Lab`

## Claim scope

Unchanged by this release. 0.1.2 hardens how the numbers are computed, checked,
and displayed; it does not add, widen, or retire a claim. The claim ledger still
carries 11 approved claims, each bound to a manuscript passage, and the
manuscript still supports only bounded case-study and mechanism readings: no
prevalence, no causal effect, no market share, no vendor reliability comparison.

Two reporting changes make the existing bounds more visible rather than looser:
every bounded proportion now carries its numerator, denominator, and a
descriptive 95% Wilson interval, and the validation funnel now draws only the
one stage that has a denominator as a rate.

## Scope carried forward

Repo-only release. No journal portal upload, no Zenodo deposit, no DOI, no ORCID
registration, and no GitHub Release PDF assets are part of this audit; see
[paper/submission_checklist.md](../paper/submission_checklist.md) and
[external_submission_actions.md](external_submission_actions.md) for the
human and portal steps that remain outside this repository's automation.

The study is still a single-coder pilot and still reports no agreement
statistic. `data/derived/reliability_subset.csv` remains the published
instrument for changing that.
