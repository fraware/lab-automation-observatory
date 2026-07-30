# Retained research artifacts

The public repository contains derived data and deterministic generators. The retained analysis workbook and compiled submission files are available from GitHub release tags when published; they are not required for ordinary reproduction.

## Audit and release-notes index

| File | Role |
|---|---|
| [submission_audit_v0.1.0.md](submission_audit_v0.1.0.md) | Frozen v0.1.0 snapshot (17 tests, 4-page supplement). Not updated after the v0.1.0 tag. |
| [release_notes_v0.1.0.md](release_notes_v0.1.0.md) | Frozen v0.1.0 release notes. |
| [submission_audit_v0.1.1.md](submission_audit_v0.1.1.md) | Frozen v0.1.1 snapshot (53 tests, local TeX build blocked). Not updated after the v0.1.1 tag. |
| [release_notes_v0.1.1.md](release_notes_v0.1.1.md) | Frozen v0.1.1 release notes. |
| [submission_audit_v0.1.2.md](submission_audit_v0.1.2.md) | Frozen v0.1.2 snapshot (128 tests, 29 validated release CSVs, first audit with a successful local document build). Not updated after the v0.1.2 tag. |
| [release_notes_v0.1.2.md](release_notes_v0.1.2.md) | Frozen v0.1.2 release notes. |
| [submission_audit_v0.1.3.md](submission_audit_v0.1.3.md) | Frozen historical audit: file itself reports 192 tests / 96.20% coverage and an incomplete TeX rebuild after claim-affecting register corrections (superseded README row that said 184 / 99.15%). |
| [release_notes_v0.1.3.md](release_notes_v0.1.3.md) | Frozen v0.1.3 release notes: adjudication instrument fixes, coherence corrections, and 0.2 scaffolding. |
| [submission_audit_v0.1.4.md](submission_audit_v0.1.4.md) | **Current** audit record: freeze `c860747`, 205 tests at 95.73% coverage, 31 validated release CSVs, 24-row source/quotation audit, inspected PDFs (29/10/1 pages, zero Type 3). |
| [release_notes_v0.1.4.md](release_notes_v0.1.4.md) | **Current** release notes: test-contract repair, source ledger, 0.1.4 metadata, measured freeze + PDF inspection. |
| [submission_bundle_manifest_v0.1.4.yaml](submission_bundle_manifest_v0.1.4.yaml) | Concrete v0.1.4-rc1 bundle manifest (commit, hashes, page counts, checks). |
| [external_submission_actions.md](external_submission_actions.md) | Human/portal follow-ups that stay outside repository automation. |
| [adjudication_pilot_v0.1.2.md](adjudication_pilot_v0.1.2.md) | Process validation of the adjudication instrument on three critical threads, with [adjudication_pilot_three_threads.csv](adjudication_pilot_three_threads.csv) as the per-thread record. Not a second coding pass and not a source of any agreement statistic. |

When citing "the audit" or "the release checks" for the live state of `main`, point at the highest-numbered `submission_audit_v*.md`; do not treat an older frozen audit as current.
