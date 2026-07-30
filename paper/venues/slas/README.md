# SLAS Technology / NexusXp package

## Files

- `paper/main_slas_v0.1.5.tex`
- `paper/cover_letter_slas_v0.1.5.tex`
- canonical supplement `paper/supplement.tex`
- canonical highlights `paper/highlights.txt`
- canonical graphical abstract generator and output
- `paper/submission_metadata.md`

## Positioning

The manuscript is written as Original Research for `NexusXp: The Connected Lab`. It foregrounds connected-laboratory engineering, integration boundaries, execution observability, recovery, and stage-bounded validation. It preserves the v0.1.4 data and numerical results.

## Build

Run from `paper/`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main_slas_v0.1.5.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error cover_letter_slas_v0.1.5.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex
```

## Final author gate

- Add ORCID in the submission portal.
- Insert the persistent code/data DOI when available.
- Confirm that the special-issue collection is selected.
- Enter preferred and excluded reviewers only in the portal.
- Compare the portal-generated PDF against the locally approved render.
- Do not submit another venue variant while this manuscript is under review.
