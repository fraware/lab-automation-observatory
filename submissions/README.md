# Venue-specific publication line

This directory separates publication strategy from the canonical scientific release. The empirical baseline is tag `v0.1.4`; venue variants change framing, structure, declarations, and submission artifacts without changing the coded evidence or reported numerical results.

**Manuscript sources are local-only.** Paths under `paper/` named below refer to the maintainer machine's gitignored manuscript tree. They are not present in the public GitHub clone, and venue submission ZIPs / manuscript PDFs are not attached to public releases.

## Submission rule

The manuscripts are **alternatives, not parallel submissions**. Submit to one archival venue at a time. A later submission must occur only after rejection or formal withdrawal from the earlier venue, and any prior submission history must be disclosed where the target venue requires it.

## Current sequence

1. **SLAS Technology — NexusXp: The Connected Lab**
   - Status: primary, submission-ready after author identifiers and portal fields.
   - Article type: Original Research.
   - Current special-issue deadline: 30 November 2026.
   - Scientific emphasis: connected-laboratory integration, operational boundaries, recovery, validation, and reusable community infrastructure.
   - Manuscript: `paper/main_slas_v0.1.5.tex`.
   - Official call: https://www.slas.org/publications/nexusxp-special-issue/

2. **Digital Discovery**
   - Status: complete alternative Full Paper source.
   - Scientific emphasis: reproducible digital-laboratory infrastructure, machine-readable evidence, executable analysis, persistent code/data, and stage-bounded claims.
   - Additional gate: referees must receive code and data at submission; add the persistent archive DOI to the Data Availability Statement before final upload.
   - Manuscript: `paper/main_digital_discovery.tex`.
   - Author guidance: https://www.rsc.org/journals-books-databases/author-and-reviewer-hub/authors-information/insights/2023/july/open-data-in-digital-discovery/

3. **Patterns — Resource**
   - Status: conditional complete draft; send the editorial inquiry before portal submission.
   - Scientific emphasis: the Observatory as a reusable data and software resource for studying operational knowledge in laboratory automation.
   - Additional gate: permanent resource links, DOI, and a clear case that the data model has utility beyond the original pilot.
   - Manuscript: `paper/main_patterns_resource.tex`; first contact: `paper/venues/patterns/editorial_inquiry.md`.
   - Journal description: https://info.cell.com/patterns-registration

4. **CSCW Rolling — Design/Theory or Qualitative track**
   - Status: distinct anonymized manuscript; do not submit concurrently with the laboratory-automation paper.
   - Scientific emphasis: articulation work, repair, infrastructuring, common information spaces, and the movement of technical knowledge between public and private channels.
   - Additional gate: export an anonymous artifact, strip PDF metadata, and ensure that every supplement is anonymized.
   - Manuscript: `paper/main_cscw.tex`.
   - Official call: https://cscw.acm.org/rolling.html

5. **Journal of Open Source Software**
   - Status: future-only paper.
   - Earliest plausible eligibility: after more than six months of public development, sustained iteration, and demonstrated research adoption.
   - Scientific emphasis: the software package and its research utility, not the empirical findings of the laboratory-automation study.
   - Draft: `paper/venues/joss/paper.md`.
   - Requirements: https://joss.readthedocs.io/en/latest/submitting.html

Recheck each official source on the day of submission. Build steps and artifact gates are in [build_matrix.md](build_matrix.md).

## Canonical evidence policy

Every venue variant must preserve:

- 55 purposively selected discussions and 45 analytical episodes;
- the single-coder pilot description and absence of an agreement statistic;
- the exact bounded denominators;
- the partial-score, leave-one-thread-out, and denominator sensitivity analyses;
- source-reported versus independently validated evidence distinctions;
- prohibitions on prevalence, causal, vendor-ranking, market-share, and installed-base inferences;
- the v0.1.4 source and data release as the numerical authority.

Claim boundaries are restated in [CLAIM_BOUNDARIES.md](../CLAIM_BOUNDARIES.md).

## Author-controlled final fields

Before any upload, complete the venue checklist for:

- ORCID;
- persistent archive DOI;
- preprint identifier, if used;
- reviewer conflicts;
- funding and competing-interest portal declarations;
- exact submission history;
- portal-generated PDF inspection.

## Venue requirements snapshot (verified 2026-07-30)

### SLAS Technology — NexusXp

- Completed-manuscript deadline: **30 November 2026**.
- Invited types include original research papers, case studies, technical briefs, and reviews.
- Scope includes advanced laboratory automation, AI/ML in laboratory workflows, laboratory data handling, robotics, smart laboratories and IoT, and real-world future-laboratory applications.
- Selected package: Original Research.

### Digital Discovery

- Selected type: Full Paper.
- Code and data must be available to referees during peer review.
- Custom code and associated data must be placed in persistent repositories, with DOI information supplied for publication.
- A Data Availability Statement is required.
- The journal can assign a dedicated data reviewer to run the code and assess reproducibility and reuse.

### Patterns

- Patterns publishes transformative data-science research and promotes outputs that support sharing, collaboration, and practical solutions.
- Cell Press expects relevant data and code to be accessible at submission.
- The present package is constructed as a Resource manuscript and remains conditional on editorial confirmation of article-type fit.

### CSCW Rolling

- Submissions are evaluated on a rolling basis with no fixed deadline.
- Papers must make a social, cooperative, or collaborative computing contribution and be substantially contextualized in CSCW theory.
- Anonymous review applies to the manuscript and all supplementary files.
- LaTeX submissions must use the ACM `acmsmall` format and remain TAPS compliant.
- The cover letter must include a scope statement and submission-history statement.
- No overlapping archival work can remain under review elsewhere.

### Journal of Open Source Software

- More than six months of public development with activity distributed across that period.
- Demonstrated research impact and credible utility.
- Feature completeness, installation, documentation, tests, community contribution paths, and maintainable extension are required.
- The paper uses Markdown with YAML metadata (about 750–1750 words) and must focus on the research software, not a new empirical study as the principal contribution.
