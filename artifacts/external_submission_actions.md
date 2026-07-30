# External submission actions

Engineering certification for tag `v0.1.4` is complete. Remaining work is ORCID wiring, Zenodo DOI reservation/publish, HAL preprint deposit, and SLAS Editorial Manager upload. **Do not submit from `main` HEAD.** Submission baseline is annotated tag `v0.1.4` only.

No Zenodo DOI, HAL identifier, or portal confirmation is asserted here. Those steps require human login.

## Canonical package (frozen)

| Field | Value |
| --- | --- |
| Tag | `v0.1.4` |
| Release URL | https://github.com/fraware/lab-automation-observatory/releases/tag/v0.1.4 |
| Source content SHA | `2a0fc1e21153198a383329f4ff313808957f163e` |
| Certification commit SHA | `962cdfd3406c5fa18520754e9978b9260409a1a5` |
| Tag peel (annotated) | `56aa1a27b04245682278847b309484454a9ee097` |
| Canonical ZIP | `LabAutomationObservatory_SLASTechnology_NexusXp_v0.1.4_2026-07-30_962cdfd.zip` |
| ZIP SHA256 | `037eff1ad438b75f6875ab4f7f4adb350feda26d173e2736e165cc28aa3c66ea` |
| Manifest | `artifacts/submission_bundle_manifest_v0.1.4.yaml` (also on the release) |

Download assets from the release page, or use the local copies under `artifacts/bundles/` when present. Verify ZIP SHA256 before any portal upload.

## Upload inventory (exact files)

Upload only these release assets (hashes from the release digests / local SHA256SUMS):

| File | SHA256 | Portal use |
| --- | --- | --- |
| `main.pdf` | `70c474b8b67cccfedb840c74bf1f4de14608882168c1dcf176184ec598c0d8a2` | Manuscript PDF |
| `supplement.pdf` | `f5a5977538aa29676fbb4483eccffb0e4da922909f792b85c8c10394abb1cb10` | Supplement |
| `cover_letter.pdf` | `4ac210b00e5e3565fb926e251de67f4a174b7debf3bc0b60a8016f4df7db782a` | Cover letter |
| `highlights.txt` | `fa9324a78a41e574a7142270fcb7b33636f5a6bf9be0d727a99ef3a650b9ec01` | Highlights |
| `graphical_abstract.png` | `719f52111c3befe3b8f6f859c0cb2ec1164918de0896c6014d31a8be4e9a25bf` | Graphical abstract |
| `submission_bundle_manifest_v0.1.4.yaml` | `4ac1ef69db57098f37f9a732f6a51444461d9f6f97c4a4f92e35bdab18bb2b62` | Checksum / provenance |
| `LabAutomationObservatory_SLASTechnology_NexusXp_v0.1.4_2026-07-30_962cdfd.zip` | `037eff1ad438b75f6875ab4f7f4adb350feda26d173e2736e165cc28aa3c66ea` | Full package archive |
| `data-and-code-source.zip` | `7ee515ba28b62c90d356a9d5eda743dfe16fcfe5bb94b566cee4563ec08e2067` | Zenodo / data archive |
| `SHA256SUMS.txt` / `bundle-SHA256SUMS.txt` | on release | Operator verification |

LaTeX source is inside the canonical ZIP (`latex-source/`). Prefer uploading portal-required PDFs/PNG/TXT individually from the release, then attach the ZIP if the portal accepts supplementary archives.

## Repo-side readiness (as of issue #8 start)

| Item | Status |
| --- | --- |
| GitHub Release `v0.1.4` with PDF/ZIP/checksum assets | Done |
| Dual-SHA manifest (`source_content_sha` + `certification_commit_sha`) | Done |
| `.zenodo.json` version / title / creators / license / keywords | Ready for deposit draft; **ORCID missing** |
| `CITATION.cff` version / authors / preferred-citation | Ready; **ORCID missing**; DOI not yet insertable |
| Manifest `identifiers.doi` / `preprint` / `orcid` | All `null` (intentional until reserved) |
| `paper/submission_checklist.md` admin boxes | Still unchecked (portal-only) |
| Author ORCID in metadata | **Incomplete** — operator must supply ORCID iD, then patch `CITATION.cff`, `.zenodo.json`, manifest, and manuscript data-availability text on a follow-up commit **after** reservation (do not invent) |

## Operator sequence (human login required)

### A. ORCID

1. Confirm the author's ORCID iD from the ORCID account (do not invent).
2. Add it to `CITATION.cff` (`authors[].orcid`), `.zenodo.json` (`creators[].orcid`), `artifacts/submission_bundle_manifest_v0.1.4.yaml` (`identifiers.orcid`), and any manuscript data-availability / author metadata that expects it.
3. Commit and push that metadata-only change **after** the values are real; rebuild is not required for ORCID-only fields unless the PDF author block changes.

### B. Zenodo DOI (reserve, then publish)

1. Log into Zenodo (or Zenodo Sandbox first if testing).
2. New upload → upload at minimum:
   - `data-and-code-source.zip`
   - `LabAutomationObservatory_SLASTechnology_NexusXp_v0.1.4_2026-07-30_962cdfd.zip` (or the individual manuscript/supplement PDFs)
   - `submission_bundle_manifest_v0.1.4.yaml`
   - `SHA256SUMS.txt` / `bundle-SHA256SUMS.txt`
3. Prefill metadata from `.zenodo.json` (title, description, creators, license `cc-by-4.0`, keywords, version `0.1.4`, publication date `2026-07-30`, related identifier → GitHub repo / tag `v0.1.4`).
4. **Reserve** a DOI without publishing if the journal needs the DOI string in the manuscript first.
5. Insert the reserved DOI into manuscript data-availability, `CITATION.cff`, `.zenodo.json` `doi` / related identifiers, and manifest `identifiers.doi`; rebuild PDFs from tag lineage only if the PDF text must change (then cut a DOI-wiring follow-up tag — do not silently replace `v0.1.4` certification assets).
6. Publish the Zenodo record and verify every file hash against the table above.
7. Record the published DOI URL on issue #8.

### C. HAL preprint

1. Log into HAL.
2. Deposit the exact approved `main.pdf` and `supplement.pdf` from the `v0.1.4` release (hashes above).
3. Licence and version must match the journal package.
4. Add the HAL identifier to repository metadata and issue #8; leave manifest `identifiers.preprint` no longer `null` only after the deposit exists.

### D. SLAS Technology (Editorial Manager)

1. Start a new submission as **Original Research**.
2. Select special issue **NexusXp: The Connected Lab**.
3. Set transfer preference to regular **SLAS Technology**.
4. Complete reviewer conflict check using `paper/reviewer_selection.md`; enter preferred / excluded reviewers only after author approval.
5. Upload `main.pdf`, `supplement.pdf`, `cover_letter.pdf`, `highlights.txt`, and `graphical_abstract.png` from the `v0.1.4` release assets (verify SHA256).
6. Complete funding, competing-interest, author-contribution, data-availability, and generative-AI declarations (`paper/submission_metadata.md`).
7. Download the portal-generated PDF and visually compare against the local approved `main.pdf` before final confirmation.
8. Comment on issue #8 with the submission ID; check off admin boxes in `paper/submission_checklist.md` only after portal confirmation.

### E. Parallel conference (SLAS2027)

Prepare a distinct 450-word abstract; do not reuse the journal PDF as the conference file.

## Explicit non-claims

- No DOI has been reserved or published from this automation pass.
- No HAL deposit was started (login required).
- No Editorial Manager upload was performed.
- Issue #8 stays **OPEN** until the portal/DOI work above is actually complete.
