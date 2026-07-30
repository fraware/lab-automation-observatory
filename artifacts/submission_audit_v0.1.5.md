# Submission audit v0.1.5

Audit date: 2026-07-30

This audit certifies the venue-specific publication line on branch
`agent/venue-specific-manuscripts-v0.1.5` (PR #17) for annotated tag `v0.1.5`.
It supersedes [submission_audit_v0.1.4.md](submission_audit_v0.1.4.md) as the
live audit record for `main` after merge. The empirical data, metrics,
robustness outputs, schemas, and numerical claims remain those certified at
`v0.1.4`.

**Freeze status:**
- Empirical baseline tag: `v0.1.4` (peel `6608d6156a025fb9d6e37a7c78112af0f88ea5a2`)
- `data/` tree SHA-256 (LF-normalized bytes):
  `8351f4d0aa821edbd8a0b0a904d851960b0d2a3195b8045f4e069bbe25a1d2a3`
  (byte-identical to the v0.1.4 certification tree hash)
- `paper/` source tree SHA-256 (LF-normalized; excludes TeX aux/PDF products):
  `c674e84cdb93c4c7488ce4feb7ad62d47da968512bc5b002892584b525bfa5b5`
- `git diff v0.1.4...HEAD -- data/ metrics/ robustness/ schemas/` empty
- Concrete bundle record:
  [submission_bundle_manifest_v0.1.5.yaml](submission_bundle_manifest_v0.1.5.yaml)

## Automated checks (measured on this host)

- Host: Windows 11 (`Windows-11-10.0.26200-SP0`), Python 3.13.11
- `uv.lock` SHA-256 (LF-normalized bytes):
  `2530d4d6b97a5d258ae1969e43a6887cc9204087c1484c3fe92c72cbe0efa1bd`
  (unchanged vs v0.1.4)
- Install authority: `uv sync --frozen --all-extras` / `uv.lock`
- 10 knowledge records validated against JSON Schema Draft 2020-12
- 11 approved claims validated and traced to manuscript anchors
- **31** release CSVs structurally validated (includes
  `data/derived/source_quote_audit.csv` with **25** rows) plus 3 robustness
  artifacts
- **206 tests passed** (`pytest`), **95.73%** branch-aware coverage (90% floor)
- `mkdocs build --strict` succeeds (Material for MkDocs 2.0 advisory only)
- Robustness CSVs regenerated without semantic drift; `git diff --exit-code`
  clean aside from Windows CRLF checkout warnings

## Determinism

`make derived`, `make validate`, `make test`, and `make docs-build` were run
against this tip. Venue manuscripts were compiled with MiKTeX 24.1 `pdflatex` /
`bibtex` direct passes (`latexmk` still needs `perl` on PATH).

## Document checks

| Document | Pages | Type 3 fonts | Embedded fonts | Unresolved refs/cites |
|---|---:|---:|---|---|
| `paper/main_slas_v0.1.5.pdf` | 29 | 0 | yes | 0 |
| `paper/cover_letter_slas_v0.1.5.pdf` | 1 | 0 | yes | 0 |
| `paper/supplement.pdf` | 10 | 0 | yes | 0 |
| `paper/main_digital_discovery.pdf` | 20 | 0 | yes | 0 |
| `paper/cover_letter_digital_discovery.pdf` | 1 | 0 | yes | 0 |
| `paper/main_patterns_resource.pdf` | 8 | 0 | yes | 0 |
| `paper/main_cscw.pdf` | 11 | 0 | yes | 0 |

SHA-256 digests (this build):

| Artifact | SHA-256 |
|---|---|
| `paper/main_slas_v0.1.5.pdf` | `66a786fabce7132bb8bcf5a87cf10cfbf47f23d47ac3bcf5f5d65b024b568ab8` |
| `paper/cover_letter_slas_v0.1.5.pdf` | `d02cfa5b014a4902771b8bacf3ef6ba513ee11c84e93886b812d4123972dd46f` |
| `paper/supplement.pdf` | `9088e791d9290e1fd781d7ee0ee9df33a8898a97d48f23bcad18d0f94f00883c` |
| `paper/main_digital_discovery.pdf` | `3c725e44dde8db530ee4653602a54c17c11f8b65a6834feff99b7e4c82435460` |
| `paper/cover_letter_digital_discovery.pdf` | `dd05ed8b70075786429defea4f0efc667c71734929db8bee6daeea27c3359540` |
| `paper/main_patterns_resource.pdf` | `205064f472873a51ece0120619aba554ff3fb1d65384a9a43ae97a1bace75f8b` |
| `paper/main_cscw.pdf` | `da87baca45e76c94cb2d2b171e567b38643349be1fb170c96076a6767b024a95` |
| `paper/graphical_abstract.png` | `719f52111c3befe3b8f6f859c0cb2ec1164918de0896c6014d31a8be4e9a25bf` |
| `paper/graphical_abstract.pdf` | `c12b6dcf4975b65c51a601902008a0fda3718df006196b01e29acf81c5267bf1` |
| `paper/highlights.txt` | `fa9324a78a41e574a7142270fcb7b33636f5a6bf9be0d727a99ef3a650b9ec01` |
| `paper/venues/slas/highlights_v0.1.5.txt` | `1c704f805bdd75e74d7d8ca7d72f400907320d32178740e83d41a6ce26e63195` |

### Page-image visual review

Tool: MiKTeX `pdftoppm -png -r 120` into a scratch directory (not committed).
Reviewed first pages, second pages where present, and last pages for every
compiled venue PDF above (19 images). No blank pages, no clipped labels, no
overlapping floats, and no unreadable figure text observed. Supplement retains
routine Overfull `\hbox` warnings on narrow table columns (5 observed); content
was not clipped in page images. Patterns has 1 Overfull `\hbox`. SLAS / Digital
Discovery / CSCW main logs show 0 Overfull `\hbox` after settling passes.

### CSCW rolling manuscript

- Body word count (pdftotext layout text before the References heading): **5206**
  (within the 5k–12k rolling-submission target; full extract including
  bibliography: 5616)
- PDF metadata Author field empty; extractable text has no matches for author
  name, email, `fraware`, `SentinelOps`, `Stanford`, or ORCID strings
- Anonymous review header renders as `Anon.`; author line is
  `Anonymous Author(s)`
- Anonymous package builder: `scripts/build_cscw_anonymous_package.py`
  (inspection notes recorded in this audit; ZIP lands under
  `artifacts/bundles/`, gitignored)

### Cover / inquiry letters outside PDF compile

- Patterns editorial inquiry: `paper/venues/patterns/editorial_inquiry.md`
  (Markdown; no PDF required by the build matrix)
- CSCW cover letter: `paper/venues/cscw/cover_letter.md` (Markdown)

## Claim scope

No new claim-affecting scientific re-estimate. B2–B7 full-corpus phi remains
**0.382**. Venue manuscripts change framing, structure, title, and contribution
emphasis only. `CLAIM_BOUNDARIES.md` restates the public inferential boundaries
and binds every venue manuscript to them. DOI / preprint / ORCID remain null.

Repository engineering certification for the v0.1.5 publication tip is complete
once the companion manifest carries the merge/certification commit SHA and the
canonical SLAS ZIP is built. Journal deposit, preprint identifiers, and DOI
assignment remain outside the scope of this audit.
