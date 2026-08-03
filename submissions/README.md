# Venue publication line

This directory records the public publication strategy for the Observatory. The
empirical baseline is tag `v0.1.4`. Venue variants may change framing, structure,
declarations, and submission packaging without changing the coded evidence or
reported numerical results.

## Submission rule

Venue manuscripts are **alternatives, not parallel submissions**. Submit to one
archival venue at a time. A later submission must occur only after rejection or
formal withdrawal from the earlier venue, and any prior submission history must
be disclosed where the target venue requires it.

## Current sequence

1. **SLAS Technology — NexusXp: The Connected Lab**
   - Status: primary.
   - Article type: Original Research.
   - Current special-issue deadline: 30 November 2026.
   - Emphasis: connected-laboratory integration, operational boundaries,
     recovery, validation, and reusable community infrastructure.
   - Official call: https://www.slas.org/publications/nexusxp-special-issue/

2. **Digital Discovery**
   - Status: complete alternative Full Paper framing.
   - Emphasis: reproducible digital-laboratory infrastructure, machine-readable
     evidence, executable analysis, persistent code/data, and stage-bounded
     claims.
   - Author guidance: https://www.rsc.org/journals-books-databases/author-and-reviewer-hub/authors-information/insights/2023/july/open-data-in-digital-discovery/

3. **Patterns — Resource**
   - Status: conditional Resource draft; editorial confirmation of article-type
     fit precedes portal submission.
   - Emphasis: the Observatory as a reusable data and software resource for
     studying operational knowledge in laboratory automation.
   - Journal description: https://info.cell.com/patterns-registration

4. **CSCW Rolling — Design/Theory or Qualitative track**
   - Status: distinct anonymized framing; do not submit concurrently with the
     laboratory-automation paper.
   - Emphasis: articulation work, repair, infrastructuring, common information
     spaces, and the movement of technical knowledge between public and private
     channels.
   - Official call: https://cscw.acm.org/rolling.html

5. **Journal of Open Source Software**
   - Status: future-only software paper.
   - Earliest plausible eligibility: after more than six months of public
     development, sustained iteration, and demonstrated research adoption.
   - Emphasis: the software package and its research utility, not the empirical
     findings of the laboratory-automation study.
   - Requirements: https://joss.readthedocs.io/en/latest/submitting.html

Recheck each official source on the day of submission. Validation expectations
are in [build_matrix.md](build_matrix.md).

## Canonical evidence policy

Every venue variant must preserve:

- 55 purposively selected discussions and 45 analytical episodes;
- the single-coder pilot description and absence of an agreement statistic;
- the exact bounded denominators;
- the partial-score, leave-one-thread-out, and denominator sensitivity analyses;
- source-reported versus independently validated evidence distinctions;
- prohibitions on prevalence, causal, vendor-ranking, market-share, and
  installed-base inferences;
- the v0.1.4 source and data release as the numerical authority.

Claim boundaries are restated in [CLAIM_BOUNDARIES.md](../CLAIM_BOUNDARIES.md).

## Author-controlled final fields

Before any upload, the author completes identifiers and portal declarations
privately (persistent archive DOI, preprint identifier if used, funding and
competing-interest statements, and submission history). Those steps are not
tracked as public repository checklists.

## Venue requirements snapshot (verified 2026-07-30)

### SLAS Technology — NexusXp

- Completed-manuscript deadline: **30 November 2026**.
- Invited types include original research papers, case studies, technical briefs,
  and reviews.
- Scope includes advanced laboratory automation, AI/ML in laboratory workflows,
  laboratory data handling, robotics, smart laboratories and IoT, and real-world
  future-laboratory applications.
- Selected package: Original Research.

### Digital Discovery

- Selected type: Full Paper.
- Code and data must be available to referees during peer review.
- Custom code and associated data must be placed in persistent repositories, with
  DOI information supplied for publication.
- A Data Availability Statement is required.

### Patterns

- Patterns publishes transformative data-science research and promotes outputs
  that support sharing, collaboration, and practical solutions.
- Cell Press expects relevant data and code to be accessible at submission.
- The present package is constructed as a Resource manuscript and remains
  conditional on editorial confirmation of article-type fit.

### CSCW Rolling

- Submissions are evaluated on a rolling basis with no fixed deadline.
- Papers must make a social, cooperative, or collaborative computing contribution
  and be substantially contextualized in CSCW theory.
- Anonymous review applies to the manuscript and all supplementary files.
- No overlapping archival work can remain under review elsewhere.

### Journal of Open Source Software

- More than six months of public development with activity distributed across
  that period.
- Demonstrated research impact and credible utility.
- Feature completeness, installation, documentation, tests, community
  contribution paths, and maintainable extension are required.
- The paper focuses on the research software, not a new empirical study as the
  principal contribution.
