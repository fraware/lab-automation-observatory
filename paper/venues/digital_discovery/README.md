# Digital Discovery package

## Files

- `paper/main_digital_discovery.tex`
- `paper/cover_letter_digital_discovery.tex`
- canonical generated figures and tables
- versioned v0.1.4 code/data release

## Positioning

This Full Paper variant treats the Observatory as an executable digital-laboratory research resource. It foregrounds machine-readable evidence, data stewardship, interface and event schemas, deterministic reproduction, robustness analysis, and validation-stage discipline.

## Mandatory final gate

Digital Discovery requires code and data to be available to referees at submission and a Data Availability Statement in the manuscript. Before upload:

1. deposit the exact v0.1.4 source and data package in a persistent archive;
2. insert the DOI in `09_declarations.tex`;
3. verify that the archived package contains every committed input needed for the paper;
4. run the complete reproduction and paper build from a clean clone;
5. provide the repository and archive links in the submission portal;
6. inspect the journal-generated PDF.

## Build

Run from `paper/`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main_digital_discovery.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error cover_letter_digital_discovery.tex
```

The generic LaTeX source is intentionally portable. Convert to the current RSC template at final submission only if requested by the portal or editorial office; do not change the empirical source files during formatting.
