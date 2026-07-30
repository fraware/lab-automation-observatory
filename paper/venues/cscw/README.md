# CSCW rolling package

## Status

Distinct manuscript, suitable only as a sequential alternative after the laboratory-automation manuscript is rejected or withdrawn. Do not submit concurrently with SLAS Technology, Digital Discovery, or Patterns.

## Files

- `paper/main_cscw.tex`
- `paper/venues/cscw/01_introduction.tex` through `09_anonymous_availability.tex`
- `paper/venues/cscw/references.bib`
- `paper/venues/cscw/cover_letter.md`

## Contribution

The CSCW paper is centered on:

- articulation work that produces the context missing from technical questions;
- repair across software histories, material state, and irreversible physical actions;
- public/private migration of support and its effect on shared knowledge;
- infrastructuring practices that turn diagnosis into maintained artifacts;
- design implications for questions, event records, public return paths, evidence grades, and community evaluation.

## Anonymous-review gate

Before submission:

1. export a clean anonymous source tree containing only required manuscript and artifact files;
2. remove Git history, author metadata, email, affiliations, acknowledgements, public authored repository URLs, release names, and identifiable checksums;
3. strip PDF metadata and inspect the source archive for names and usernames;
4. anonymize the supplementary artifact and its README;
5. complete the required scope and submission-history statements in `cover_letter.md`;
6. confirm no overlapping archival manuscript is under review;
7. compile with the current ACM `acmsmall` review template and verify TAPS compatibility;
8. keep the main text within the current rolling-submission word range.

## Build

Run from `paper/` in an environment containing `acmart`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main_cscw.tex
```

The public v0.1.4 repository must not be linked inside the anonymous review manuscript. It can be disclosed after the anonymity period.
