# Venue and artifact matrix

Only one journal may consider the manuscript at a time. The repository can support several publication routes, but each route requires a venue-specific manuscript and bundle. The SLAS file must not be reused unchanged for another journal.

## Route 1 — SLAS Technology, NexusXp: The Connected Lab

**Status:** primary route.

**Article type:** Original Research.

**Positioning:** empirical account of recurring connected-laboratory bottlenecks, bounded forum-derived metrics, and practical infrastructure for integration, observability, recovery, validation, and knowledge retention.

**Required bundle profile:**

- Elsevier `elsarticle` manuscript PDF and complete LaTeX source;
- supplementary PDF;
- NexusXp-specific cover letter;
- highlights;
- graphical abstract;
- source/data repository citation;
- commit-pinned manifest and checksums.

**Release condition:** build after all issue #13 gates pass. The July 28, 2026 bundle is superseded. The special-issue deadline is November 30, 2026.

## Route 2 — Digital Discovery

**Status:** strongest journal fallback and possible higher-ambition revision.

**Article type:** Full Paper. A Perspective would require a substantially less empirical and more field-level manuscript.

**Positioning:** evidence infrastructure for connected and autonomous laboratories, emphasizing machine-readable records, reproducible metrics, validation-stage discipline, and operational boundaries between software representations and physical execution.

**Required changes:**

- rewrite title, abstract, introduction, and discussion for the broader digital-laboratory and autonomous-experimentation readership;
- move the public technical-community method into a generalizable measurement framework;
- provide a journal-specific cover letter;
- provide an RSC-style Data Availability Statement with full repository and DOI links;
- archive the exact code and data version in a persistent repository with a DOI;
- prepare for a data reviewer to run the code and reproduce the reported results;
- convert reference and submission metadata to the journal's requirements.

**Do not submit:** the SLAS cover letter, the SLAS special-issue metadata, or a repository URL without a versioned archive.

## Route 3 — Patterns

**Status:** stretch route after a major scientific expansion.

**Positioning:** a transferable data-science method for deriving bounded operational constructs and claim-safe metrics from specialist technical communities.

**Required changes:**

- demonstrate transfer beyond one purposively selected forum, preferably through a second corpus or held-out evaluation;
- establish a reusable method contribution whose value is broader than laboratory automation;
- provide a fully archived data/code package and explicit availability statements;
- reduce platform-specific detail in the main argument;
- show how the method changes data stewardship, collaboration, or decision practice.

**Decision:** do not send the current paper to Patterns as a routine fallback. Submit only after the general-method contribution is independently validated.

## Route 4 — ACM CSCW / PACM HCI

**Status:** separate future paper.

**Positioning:** collaborative reconstruction of hidden technical systems, distributed support labor, public/private knowledge migration, and community governance in a specialist technical forum.

**Required changes:**

- rebuild the paper around human work, collaboration, knowledge infrastructure, and organizational practice;
- add appropriate CSCW theory and related work;
- strengthen the ethical treatment of public online-community research;
- preferably add interviews, participant feedback, or an evaluated community intervention;
- use the ACM submission format and a distinct contribution statement.

**Decision:** the SLAS manuscript is not the correct CSCW file.

## Route 5 — Journal of Open Source Software

**Status:** possible later software paper, not a venue for the present empirical manuscript.

**Positioning:** a maintained software package for evidence validation, metric reproduction, and governed laboratory-automation knowledge artifacts.

**Required maturity:** sustained public development, external research use, adoption evidence, and a concise JOSS software paper centered on software functionality and research impact.

**Decision:** do not submit the current research manuscript to JOSS. Reassess after the repository has a meaningful public history and external users.

## Public dissemination stack

These deposits complement journal submission and are not competing journal submissions:

1. **GitHub:** living source, issue tracking, correction workflow, and tagged releases.
2. **Zenodo:** immutable versioned archive and DOI for the exact code/data release.
3. **HAL:** manuscript preprint and later accepted-manuscript record where permitted.
4. **LabAutomation.io:** concise community summary, correction pathway, and links to the preprint, repository, and evidence atlas.
5. **SLAS conference abstract:** a presentation can support domain feedback, subject to the conference's current submission rules and the journal's prior-publication policy.

## Canonical file rule

Maintain one immutable source release and generate separate presentation layers:

- `slas-technology-nexusxp/`
- `digital-discovery/`
- `patterns-expanded/`
- `cscw-separate-study/`
- `joss-software-paper/`

Each directory or release profile must declare its source commit and may not silently inherit another venue's cover letter, declarations, references, or manuscript framing.
