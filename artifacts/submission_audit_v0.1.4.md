# Submission audit v0.1.4

Audit date: 2026-07-30

This audit reflects final certification on branch `release/v0.1.4-rc2`, cut from
tag `v0.1.4-rc1` (peel `9096c654990e9d259ba1b36da06b4cb8211cb00f`), not from
Dependabot-advanced `main`. It supersedes the rc1 freeze record in this file's
prior revision and remains the live record for annotated tag `v0.1.4`.

**Freeze status:**
- `source_content_sha`: `2a0fc1e21153198a383329f4ff313808957f163e` (About/Terms audit split to 25 rows)
- `certification_commit_sha`: filled in the companion manifest after the commit that carries visual-review results, artifact hashes, and `source_archive`
- Content ancestry remains a descendant of scientific freeze `c860747e7a8d4ae002ba2df250c224fc2d63a85f`
- Concrete bundle record: [submission_bundle_manifest_v0.1.4.yaml](submission_bundle_manifest_v0.1.4.yaml)

## Automated checks (measured on this host)

- Host: Windows 11 (`Windows-11-10.0.26200-SP0`), Python 3.13.11
- `uv.lock` SHA-256 (LF-normalized bytes):
  `2530d4d6b97a5d258ae1969e43a6887cc9204087c1484c3fe92c72cbe0efa1bd`
- Install authority: `uv sync --frozen --all-extras` / `uv.lock` (historical v0.1.0 pin list retained only as `artifacts/requirements.environment.v0.1.0.txt`)
- 10 knowledge records validated against JSON Schema Draft 2020-12
- 11 approved claims validated and traced to manuscript anchors
- **31** release CSVs structurally validated (includes
  `data/derived/source_quote_audit.csv` with **25** rows) plus 3 robustness
  artifacts
- **206 tests passed** (`pytest`), including BibTeX key→`\href` URL→audit URL parity
- **95.73%** branch-aware coverage (90% floor); 1,358 statements and 446
  branches, 44 statements and 29 partial branches uncovered
- `mkdocs build --strict` succeeds (Material for MkDocs 2.0 advisory only)
- Robustness CSVs regenerated without semantic drift; `git diff --exit-code`
  clean aside from Windows CRLF checkout noise

## Determinism

`make derived`, `make validate`, `make test`, `make docs-build`,
`make figures`, `make tables`, and `make graphical-abstract` were run against
this certification tip. Tree hashes recorded in the manifest are SHA-256 over
sorted relative paths and LF-normalized file bytes under `data/` and under
`paper/` excluding TeX aux/PDF build products.

## Document checks

Compiled with MiKTeX 24.1 `pdflatex` / `bibtex` (direct passes; `latexmk` Make
targets still need a `perl` script engine on PATH). Measured:

| Document | Pages | Type 3 fonts | Embedded fonts | Extractable text |
|---|---:|---:|---|---|
| `paper/main.pdf` | 29 | 0 | yes (Type 1 + CID TrueType) | yes |
| `paper/supplement.pdf` | 10 | 0 | yes | yes |
| `paper/cover_letter.pdf` | 1 | 0 | yes | yes |
| `paper/graphical_abstract.pdf` | 1 | 0 | yes | n/a (figure) |

### Page-image visual review

Tool: MiKTeX `pdftoppm -png -r 120` into a scratch directory (not committed).
Reviewed all **41** page images (29 + 10 + 1 + 1). No blank pages, no clipped
labels, no overlapping floats, no unreadable figure text, and a balanced
graphical abstract. Supplement still emits routine Overfull `\hbox` warnings on
narrow table columns (largest observed ~29 pt); content was not clipped in the
page images. Recorded in the manifest as
`completed_page_image_review_pdftoppm_png_120dpi_41_pages`.

SHA-256 digests (this build):

| Artifact | SHA-256 |
|---|---|
| `paper/main.pdf` | `70c474b8b67cccfedb840c74bf1f4de14608882168c1dcf176184ec598c0d8a2` |
| `paper/supplement.pdf` | `f5a5977538aa29676fbb4483eccffb0e4da922909f792b85c8c10394abb1cb10` |
| `paper/cover_letter.pdf` | `4ac210b00e5e3565fb926e251de67f4a174b7debf3bc0b60a8016f4df7db782a` |
| `paper/graphical_abstract.pdf` | `c12b6dcf4975b65c51a601902008a0fda3718df006196b01e29acf81c5267bf1` |
| `paper/graphical_abstract.png` | `719f52111c3befe3b8f6f859c0cb2ec1164918de0896c6014d31a8be4e9a25bf` |
| `paper/highlights.txt` | `fa9324a78a41e574a7142270fcb7b33636f5a6bf9be0d727a99ef3a650b9ec01` |
| `artifacts/bundles/data-and-code-source.zip` | `7ee515ba28b62c90d356a9d5eda743dfe16fcfe5bb94b566cee4563ec08e2067` |

Final `main.log` / `supplement.log` show no undefined references or undefined
citations after the settling passes.

## Source / quotation audit

`data/derived/source_quote_audit.csv` has **25** complete rows (`SQA-01` …
`SQA-25`). About (`/about`) and Terms (`/tos`) are separate identities. Every
quote-bank entry and every manuscript `forum_*` / `labautomation_*` bib key
maps to exactly one row whose `Source URL` equals that entry's `\href` URL.
Seven source-fidelity quotation corrections remain recorded as `applied: …`.

## Claim scope

No new claim-affecting scientific re-estimate. B2–B7 full-corpus phi remains
**0.382**. Version metadata is consistently `0.1.4`. DOI / preprint / ORCID
remain null.

## Remaining for full portal close (issue #8, not this audit)

1. Author portal / Editorial Manager upload and portal PDF comparison.
2. Zenodo / DOI / ORCID wiring (issue #8).
3. Optional: install a `perl`-capable `latexmk` (or TeX Live in WSL) so
   `make paper` / `make supplement` succeed without direct `pdflatex` passes.
