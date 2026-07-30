# SLAS Technology submission compliance checklist

This checklist maps the frozen release candidate to the current SLAS author requirements and the NexusXp special-issue call. A checked manuscript-form item does not certify the latest PDF; document certification belongs to the release gate below.

## Manuscript form

- [x] Original Research structure with Introduction, Materials and Methods, Results, and Discussion
- [x] Abstract and keywords
- [x] Main text below the journal's preferred 7,000-word guideline
- [x] Seven combined main-text figures and tables
- [x] Fewer than 50 cited references
- [x] Ancillary code-count and validation material moved to the supplement
- [x] Short title of no more than 45 characters
- [x] Author name, degree, affiliations, correspondence address, telephone, fax status, and email
- [x] Graphical abstract supplied
- [x] Highlights supplied

## Scientific integrity

- [x] Purposive sampling stated explicitly
- [x] Single-coder design stated explicitly
- [x] No prevalence, market-share, vendor-ranking, or causal overclaims
- [x] Product-reported results labeled and bounded by validation stage
- [x] Unknown values remain distinct from absent values
- [x] Counterexamples and positive community mechanisms retained
- [x] Published numerical claims asserted in regression tests
- [x] Public-data minimization documented
- [x] Blind coder projection identified as the only independent-coding entry point
- [x] Commit the complete source/quotation audit ledger
- [x] Apply and regenerate all seven identified source-fidelity quotation corrections
- [x] Complete partial-score weighting sensitivity
- [x] Complete leave-one-thread-out association stability using the current corrected register
- [x] Complete adversarial denominator sensitivity for B6--B10

## Computational release gate

- [x] Freeze one commit and declare its release version
- [x] Run `uv sync --frozen --all-extras`
- [x] Run `make ci` computational subset (`validate`, `pytest`, `docs-build`; TeX via direct `pdflatex`/`bibtex` where `latexmk`/perl is unavailable)
- [x] Confirm deterministic regeneration leaves a clean working tree
- [x] Confirm all claim anchors, source rows, denominators, tables, and figures agree
- [x] Confirm mutation/property tests cover changes that could alter published values
- [x] Complete `submission_bundle_manifest.template.yaml` with hashes and measured check counts

## Document release gate

- [x] Rebuild manuscript, supplement, cover letter, and graphical abstract from the frozen commit
- [x] Confirm no missing citations, references, figures, or generated tables
- [x] Confirm embedded fonts and zero Type 3 fonts
- [x] Confirm extractable text and searchable links
- [x] Render and inspect every PDF page for clipping, overlap, blank pages, and glyph errors
- [x] Name the archive with venue, version/date, and commit prefix
- [x] Mark the July 28, 2026 bundle as superseded

## Submission administration

- [ ] Select `Original Research` and the NexusXp special-issue collection in the submission portal
- [ ] Complete author-agreement declarations in the portal
- [ ] Provide preferred and non-preferred reviewers after a final conflict check
- [ ] Upload the exact manifest-listed manuscript, supplement, cover letter, highlights, and graphical abstract
- [ ] Inspect and compare the portal-generated PDF with the approved local render

## Final gate

Submit only when every numerical statement traces to a committed input, every direct quotation has passed the source ledger, every external identifier resolves, and the portal files match the commit-pinned manifest. The current v0.1.4 audit and annotated tag certify the rebuilt PDFs for this release line; portal upload remains issue #8.
