# Venue build and artifact matrix

All venue variants inherit the empirical baseline from tag `v0.1.4`. No venue package may alter the coded data, metric inputs, generated numerical results, source-audit records, or claim boundaries without a new scientific release.

## Common validation gate

Run from the repository root:

```bash
uv sync --frozen --all-extras
make derived
make validate
make test
make docs-build
git diff --exit-code
```

The venue branch must preserve the certified v0.1.4 numerical outputs. New manuscript sources must compile cleanly and receive page-image inspection, font inspection, text-extraction checks, unresolved-reference checks, and artifact hashes.

## Build matrix

| Venue | Source | Cover/inquiry | Status | Required extra gate |
|---|---|---|---|---|
| SLAS Technology / NexusXp | `paper/main_slas_v0.1.5.tex` | `paper/cover_letter_slas_v0.1.5.tex` | Primary | ORCID, archive DOI, special-issue selection, portal PDF comparison |
| Digital Discovery | `paper/main_digital_discovery.tex` | `paper/cover_letter_digital_discovery.tex` | Complete alternative | Code/data to referees, persistent DOI, final Data Availability Statement |
| Patterns Resource | `paper/main_patterns_resource.tex` | `paper/venues/patterns/editorial_inquiry.md` | Conditional | Positive editorial response, DOI, external reuse/adoption evidence |
| CSCW Rolling | `paper/main_cscw.tex` | `paper/venues/cscw/cover_letter.md` | Distinct alternative | Anonymous artifact, submission-history disclosure, TAPS check |
| JOSS | `paper/venues/joss/paper.md` | none | Future only | More than six months public development and demonstrated research impact |

## Paper builds

Run from `paper/`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main_slas_v0.1.5.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error cover_letter_slas_v0.1.5.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex

latexmk -pdf -interaction=nonstopmode -halt-on-error main_digital_discovery.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error cover_letter_digital_discovery.tex

latexmk -pdf -interaction=nonstopmode -halt-on-error main_patterns_resource.tex

latexmk -pdf -interaction=nonstopmode -halt-on-error main_cscw.tex
```

The CSCW build requires the current `acmart` package. The JOSS paper should be checked with the current JOSS paper tooling only after the eligibility gate is satisfied.

## Venue-specific artifact sets

### SLAS Technology

- manuscript PDF and complete LaTeX source;
- canonical supplement;
- NexusXp cover letter;
- highlights;
- graphical abstract;
- persistent code/data archive DOI;
- source and artifact checksums.

### Digital Discovery

- Full Paper PDF and source;
- Digital Discovery cover letter;
- graphical or TOC image if requested;
- exact code/data archive available to referees;
- Data Availability Statement with persistent DOI;
- reproduction instructions and environment lock.

### Patterns

- Resource manuscript PDF and source;
- editorial-inquiry response;
- permanent resource DOI and repository links;
- resource inventory and reuse documentation;
- evidence of external use or adoption;
- graphical summary if requested.

### CSCW

- anonymous manuscript PDF and source;
- anonymous artifact archive;
- scope statement;
- complete prior-submission disclosure;
- anonymized supplementary material;
- artifact and PDF metadata audit.

### JOSS

- `paper.md` and bibliography;
- stable installable release;
- user documentation and examples;
- archived DOI;
- external-use evidence;
- JOSS review checklist.

## Sequential-submission control

Only one archival manuscript from this evidence base can be under review at a time unless the venues explicitly approve non-overlapping simultaneous submissions. Record every submission, withdrawal, rejection, transfer, and revision. A later venue package must disclose relevant history and must not claim novelty already assigned to an accepted archival paper.

## Filename policy

Use filenames containing venue, article type, version, date, and certified commit, for example:

```text
LabAutomationObservatory_SLASTechnology_NexusXp_v0.1.5_2026-07-30_<sha7>.zip
LabAutomationObservatory_DigitalDiscovery_FullPaper_v0.1.5_2026-07-30_<sha7>.zip
LabAutomationObservatory_CSCW_Anonymous_v0.1.5_2026-07-30_<sha7>.zip
```

Never use an unqualified filename such as `final.pdf` or `latest.zip`.
