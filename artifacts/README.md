# Retained research artifacts

The public repository contains derived data, deterministic generators, and audit records. Manuscript sources under `paper/`, compiled venue PDFs, and submission ZIPs that embed LaTeX sources are **local-only** and are not published to GitHub (tree or Release assets). Public release tags may carry data/code archives such as `data-and-code-source.zip`; they are not required for ordinary reproduction from a clone.

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
| [submission_audit_v0.1.4.md](submission_audit_v0.1.4.md) | Frozen v0.1.4 audit: empirical certification tip, 206 tests at 95.73% coverage, 31 validated release CSVs, 25-row source/quotation audit, page-image visual review (41 pages), zero Type 3. |
| [release_notes_v0.1.4.md](release_notes_v0.1.4.md) | Frozen v0.1.4 release notes: audit split, dual-SHA manifest, ZIP builder, frozen workflows. |
| [submission_bundle_manifest_v0.1.4.yaml](submission_bundle_manifest_v0.1.4.yaml) | Frozen v0.1.4 local certification manifest (dual SHAs, hashes, page counts, checks, `source_archive`). |
| [submission_audit_v0.1.5.md](submission_audit_v0.1.5.md) | **Current** audit record: venue-specific manuscript line on the v0.1.4 empirical baseline, 206 tests at 95.73% coverage (compile details refer to the local-only `paper/` tree). |
| [release_notes_v0.1.5.md](release_notes_v0.1.5.md) | **Current** release notes: publication line and v0.1.5 bundle tooling; manuscript packages themselves stay local. |
| [submission_bundle_manifest_v0.1.5.yaml](submission_bundle_manifest_v0.1.5.yaml) | Local certification manifest for the v0.1.5 SLAS bundle (dual SHAs, hashes, page counts, checks); not a public manuscript download. |
| [requirements.environment.v0.1.0.txt](requirements.environment.v0.1.0.txt) | Historical v0.1.0 interpreter pin snapshot; not an install authority (`uv.lock` is). |
| [adjudication_pilot_v0.1.2.md](adjudication_pilot_v0.1.2.md) | Process validation of the adjudication instrument on three critical threads, with [adjudication_pilot_three_threads.csv](adjudication_pilot_three_threads.csv) as the per-thread record. Not a second coding pass and not a source of any agreement statistic. |

When citing "the audit" or "the release checks" for the live state of `main`, point at the highest-numbered `submission_audit_v*.md`; do not treat an older frozen audit as current.
