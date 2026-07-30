# Submission audit v0.1.4

Audit date: 2026-07-30

This audit reflects the `release/v0.1.4` freeze tip
`c860747e7a8d4ae002ba2df250c224fc2d63a85f` (implementation) plus this
certification commit. It supersedes
[submission_audit_v0.1.3.md](submission_audit_v0.1.3.md) as the live record;
earlier audits remain frozen for their tags.

**Freeze status:** content freeze `c860747` was rebuilt with a clean worktree;
manuscript, supplement, cover letter, and graphical abstract PDFs were compiled
and inspected on this host. Annotated tag intent: `v0.1.4-rc1`. Concrete bundle
record: [submission_bundle_manifest_v0.1.4.yaml](submission_bundle_manifest_v0.1.4.yaml).

## Automated checks (measured on this host)

- Host: Windows 11 (`Windows-11-10.0.26200-SP0`), Python 3.13.11
- `uv.lock` SHA-256:
  `2530d4d6b97a5d258ae1969e43a6887cc9204087c1484c3fe92c72cbe0efa1bd`
- `uv sync --frozen --all-extras`: succeeded (72 packages installed from the
  locked set)
- 10 knowledge records validated against JSON Schema Draft 2020-12
- 11 approved claims validated and traced to manuscript anchors
- **31** release CSVs structurally validated by
  `labauto_observatory.register_validation` (includes
  `data/derived/source_quote_audit.csv` with 24 rows) plus 3 robustness
  artifacts
- **205 tests passed** (`uv run pytest`), up from 192 at v0.1.3
- **95.73%** branch-aware coverage (90% floor); 1,358 statements and 446
  branches, 44 statements and 29 partial branches uncovered
- `mkdocs build --strict` succeeds (Material for MkDocs 2.0 advisory only)
- Robustness CSVs regenerated without drift; robustness `.tex` sync fixture
  passes; denominator mutation test passes
- Supplement inventory expects five table stems; generated tables match a fresh
  `build_robustness_tables` run

## Determinism

`make derived`, `make validate`, `make test`, `make docs-build`,
`make figures`, `make tables`, and `make graphical-abstract` were run against
`c860747`. `git diff --exit-code` reported a clean worktree afterward (LF/CRLF
normalization warnings only).

WSL2 is available (`make`, `uv`), but TeX Live is not installed there and
passwordless `sudo` is unavailable, so the PDF pass used the Windows MiKTeX
toolchain rather than Linux TeX Live.

## Document checks

Compiled with MiKTeX 24.1 `pdflatex` / `bibtex` (direct passes; `latexmk` Make
targets still need a `perl` script engine on PATH — Strawberry Perl winget
install reported success but `perl` was not resolvable in this shell). Measured:

| Document | Pages | Type 3 fonts | Embedded fonts | Extractable text |
|---|---:|---:|---|---|
| `paper/main.pdf` | 29 | 0 | yes (Type 1 + CID TrueType) | yes (title, abstract, body) |
| `paper/supplement.pdf` | 10 | 0 | yes | yes (S1–S3 headings, register prose) |
| `paper/cover_letter.pdf` | 1 | 0 | yes | yes (addressee, title, date 2026-07-30) |
| `paper/graphical_abstract.pdf` | 1 | 0 | yes | n/a (figure) |

SHA-256 digests (this build):

| Artifact | SHA-256 |
|---|---|
| `paper/main.pdf` | `0d6cd50d0ca461c5cf56edcf736a8c538f154ec76ec5d72d50471b48c1fdbdf2` |
| `paper/supplement.pdf` | `075ba6c00c590ed5afba0cfece509f6dd492e3872a1b739766a2ac6e81bb0de9` |
| `paper/cover_letter.pdf` | `b6b6e55acd1c6f1d77e1f4a6a7773648a964cd1cc815ac63e1ea2a193c42fb11` |
| `paper/graphical_abstract.pdf` | `c12b6dcf4975b65c51a601902008a0fda3718df006196b01e29acf81c5267bf1` |
| `paper/graphical_abstract.png` | `719f52111c3befe3b8f6f859c0cb2ec1164918de0896c6014d31a8be4e9a25bf` |
| `paper/highlights.txt` | `fa9324a78a41e574a7142270fcb7b33636f5a6bf9be0d727a99ef3a650b9ec01` |

Final `main.log` / `supplement.log` show no undefined references or undefined
citations after the settling passes. Supplement still emits routine Overfull
`\hbox` warnings on narrow table columns; no blank-page or missing-figure
symptoms in the extractable-text smoke or `pdffonts` inspection.

## Source / quotation audit

`data/derived/source_quote_audit.csv` has 24 complete rows (`SQA-01` …
`SQA-24`). Every quote-bank entry and every manuscript `forum_*` /
`labautomation_*` bib key maps to exactly one row. Seven source-fidelity
quotation corrections are recorded as `applied: …` with approved wording
matching the current quote bank.

## Claim scope

No new claim-affecting scientific re-estimate beyond the PR #14 robustness
tables already on `main`. B2–B7 full-corpus phi remains **0.382**. Version
metadata is consistently `0.1.4`. DOI / preprint / ORCID remain null.

## Remaining for full portal close (issue #8, not this audit)

1. Author portal / Editorial Manager upload and portal PDF comparison.
2. Zenodo / DOI / ORCID wiring (issue #8).
3. Optional: install a `perl`-capable `latexmk` (or TeX Live in WSL) so
   `make paper` / `make supplement` succeed without direct `pdflatex` passes.
