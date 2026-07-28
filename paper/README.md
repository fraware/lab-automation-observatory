# Manuscript build

The main manuscript targets the structure expected for an SLAS Technology Original Research submission and uses Elsevier's `elsarticle` class.

```bash
make paper
make supplement
```

Submission support files:

- `main.tex` and `sections/`
- `supplement.tex`
- `highlights.txt`
- `cover_letter.tex`
- `graphical_abstract.png`
- reproducible figures under `figures/`
- generated LaTeX tables under `generated/`

The main manuscript contains five figures and two tables. Direct code counts and the AI validation funnel are placed in the supplement, keeping the main submission at seven combined figures and tables.

Before submission, insert the Zenodo DOI and the selected preprint identifier.

## Submission target

The release is prepared as Original Research for the **SLAS Technology special issue `NexusXp: The Connected Lab`**, with regular SLAS Technology as the transfer preference. See `submission_metadata.md` and `submission_checklist.md`.
