# Patterns Resource package

## Status

**Conditional. Do not submit through the portal until the editorial inquiry receives a positive response and a persistent archive DOI exists.**

## Files

- `paper/main_patterns_resource.tex`
- `paper/venues/patterns/editorial_inquiry.md`
- canonical figures, generated tables, code, data, schemas, and audits

## Positioning

This manuscript treats the Lab Automation Observatory as a reusable research resource. The central contribution is the integrated data, schema, software, provenance, validation, and governance architecture. The empirical analysis is included as a demonstration of the resource, not as the sole contribution.

## Additional evidence preferred before submission

- at least one independent coding pass or external reuse;
- adoption of one schema by a laboratory, project, or technical community;
- a persistent archive DOI;
- a concise record of maintenance and external contributions;
- editorial confirmation that the present scope fits the Resource article type.

## Build

Run from `paper/`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main_patterns_resource.tex
```

If the editorial response requests another Cell Press article type, revise the contribution structure before formatting. Do not submit the SLAS or Digital Discovery manuscript under a Patterns cover page.
