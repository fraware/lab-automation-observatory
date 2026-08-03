# Venue validation matrix

All venue variants inherit the empirical baseline from tag `v0.1.4`. No venue
package may alter the coded data, metric inputs, generated numerical results,
source-audit records, or claim boundaries without a new scientific release.

## Common validation

Run from the repository root:

```bash
uv sync --frozen --all-extras
make derived
make validate
make test
make docs-build
git diff --exit-code
```

On Windows without GNU Make, use the PowerShell equivalents in
[REPRODUCIBILITY.md](../REPRODUCIBILITY.md#windows-and-powershell).

The certified v0.1.4 numerical outputs must be preserved. Venue manuscripts are
compiled and inspected privately by the author before upload.

## Venue status

| Venue | Status | Public readiness notes |
|---|---|---|
| SLAS Technology / NexusXp | Primary | Special-issue deadline 30 November 2026; Original Research |
| Digital Discovery | Complete alternative | Code/data available to referees; persistent DOI in Data Availability Statement |
| Patterns Resource | Conditional | Editorial confirmation of Resource fit; permanent resource links |
| CSCW Rolling | Distinct alternative | Anonymous review package; submission-history disclosure |
| JOSS | Future only | More than six months public development and demonstrated research impact |

## Sequential-submission control

Only one archival manuscript from this evidence base can be under review at a
time unless the venues explicitly approve non-overlapping simultaneous
submissions. Record every submission, withdrawal, rejection, transfer, and
revision privately. A later venue package must disclose relevant history and
must not claim novelty already assigned to an accepted archival paper.

## Public release assets

Public GitHub Releases publish reproducible data and code archives (for example
`data-and-code-source.zip` and checksums). Manuscript PDFs and venue submission
ZIPs are not published as GitHub Release assets.
