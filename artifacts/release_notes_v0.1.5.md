# v0.1.5 release notes

Publication-line release for venue-specific manuscripts on the certified
v0.1.4 empirical baseline.

Tag intent: `v0.1.5`
Empirical baseline: `v0.1.4`
Bundle manifest: [submission_bundle_manifest_v0.1.5.yaml](submission_bundle_manifest_v0.1.5.yaml)
Audit: [submission_audit_v0.1.5.md](submission_audit_v0.1.5.md)

## Highlights

1. Adds primary SLAS Technology / NexusXp manuscript
   (`paper/main_slas_v0.1.5.tex`) and cover letter, plus Digital Discovery,
   Patterns Resource, anonymized CSCW, and future JOSS package drafts.
2. Restores public `CLAIM_BOUNDARIES.md` and records a venue build matrix under
   `submissions/`.
3. Preserves coded data, metrics, robustness outputs, schemas, and the v0.1.4
   numerical results (`data/` tree hash unchanged).
4. Records a measured venue compile/audit: 206 tests, 95.73% coverage, seven
   compiled PDFs with zero Type 3 fonts, CSCW body word count 5206.
5. Extends `scripts/build_submission_bundle.py` for SLAS v0.1.5 paths and adds
   `scripts/build_cscw_anonymous_package.py` for the anonymous review archive.

## Out of scope

- ORCID / DOI / portal upload
- Concurrent multi-venue archival submission
- Any change to the certified numerical baseline
