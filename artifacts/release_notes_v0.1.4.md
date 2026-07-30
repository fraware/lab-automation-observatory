# v0.1.4 release notes

Certified repository release for the SLAS Technology / NexusXp submission line.
Branches from tag `v0.1.4-rc1`, splits the About/Terms audit identity to 25 rows,
adds BibTeX URL parity tests, dual-SHA manifest fields, a canonical submission ZIP
builder, frozen workflow installs, and a completed page-image PDF visual pass.
DOI, Zenodo, and preprint identifiers are not asserted by this tag.

`source_content_sha`: `2a0fc1e21153198a383329f4ff313808957f163e`  
Scientific ancestry: `c860747e7a8d4ae002ba2df250c224fc2d63a85f`  
Tag intent: `v0.1.4`  
Bundle manifest: [submission_bundle_manifest_v0.1.4.yaml](submission_bundle_manifest_v0.1.4.yaml)

## Why this certification tip

1. rc1 ledger `SQA-01` listed both `labautomation_about` and `labautomation_terms`
   against only `https://labautomation.io/about`.
2. Manifest `commit_sha` conflated scientific freeze and certification tip.
3. Root `requirements.environment.txt` implied exact pins that Dependabot no
   longer maintains beside `uv.lock`.
4. Submission still needed a verifiable ZIP + `SHA256SUMS` and workflow
   `--frozen` hardening before tagging `v0.1.4`.

## What changed since rc1

- 25-row source-quote audit with About/Terms split and BibTeX href parity tests
- Dual SHA schema: `source_content_sha` + `certification_commit_sha`
- Historical env pins under `artifacts/requirements.environment.v0.1.0.txt`
- `scripts/build_submission_bundle.py` and release workflow asset completeness
- Page-image visual review recorded; computational and document checks recorded in the audit

## Measured checks (2026-07-30)

- Host: Windows 11, Python 3.13.11; install authority `uv.lock`
- **206** tests passed; 95.73% branch-aware coverage
- 31 release CSVs + 3 robustness artifacts validated
- 25 source-quote audit records
- `mkdocs build --strict` green
- PDFs (MiKTeX `pdflatex`/`bibtex`): main 29 pp, supplement 10 pp, cover letter
  1 pp, graphical abstract 1 pp; **zero Type 3 fonts**; 41 page images reviewed

Measured detail and SHA-256 digests:
[submission_audit_v0.1.4.md](submission_audit_v0.1.4.md).
