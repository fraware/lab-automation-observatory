# Publication robustness outputs

The repository separates headline metric inputs from publication stress tests. Headline case data remains under `data/metrics/`; deterministic stress-test outputs are generated under `data/robustness/`.

## Partial-score sensitivity

`data/robustness/partial_score_sensitivity.csv` recomputes IAS, RMC, PDC, and OC after replacing every component score of `0.5` with `0`, `0.25`, `0.5`, `0.75`, and `1`. Complete, absent, and unknown cells are unchanged. The output reports the across-case mean, case count, known cells, and unknown cells.

This analysis exposes dependence on the numerical encoding of partial evidence. It does not calibrate a probability, estimate a population parameter, or make the four instruments comparable to one another.

## Leave-one-thread-out associations

`data/robustness/association_leave_one_out.csv` deletes each of the 55 selected threads once and recomputes all 28 B2–B9 associations. For every pair it records the full-register phi and lift, deletion ranges, rank range, top-five retention, and retention of the pilot attention threshold.

This is a descriptive influence analysis over a purposive multi-label register. It is not a population jackknife and supplies no inferential interval.

## Regeneration

```bash
make robustness
make validate
make test
```

`make derived` also regenerates the robustness CSVs. `make tables` regenerates their supplementary LaTeX tables. `scripts/validate_release.py` fails when either CSV has drifted from its source data.
