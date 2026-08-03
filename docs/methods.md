# Methods

## Corpus

The pilot contains 55 purposively selected public discussions. Selection supports conceptual coverage and metric design; it does not support prevalence estimates.

## Episode segmentation

Fourteen deliberately difficult threads were segmented into 45 episodes because one thread can move among interface access, deployment state, physical representation, observability, recovery, validation, and public artifact creation.

## Coding

The release uses ten constructs. B1 and B10 are ecosystem conditions. B2–B4 cover interfaces and representations. B5–B7 cover runtime coordination. B8 covers evaluation semantics. B9 covers AI context and physical feedback.

The study is a single-coder pilot. It reports no inter-rater statistic. Reliability is supported through explicit inclusion and exclusion rules, hard-case adjudication, retained counterexamples, machine-checked published values, and a claim ledger.

## Hard-case adjudication set

`data/derived/reliability_subset.csv` is the prepared instrument for an independent second coding pass. It covers the same fourteen threads that were segmented into episodes and records, for each thread, the expected primary code, the most plausible competing code, why disagreement is likely, the specific adjudication question, whether episode segmentation is required, and an adjudication priority.

The file is an instrument, not a result. Publishing the expected disagreement surface before any second pass is what would make a later agreement statistic meaningful, and it prevents agreement from being computed on the unambiguous threads only. No agreement coefficient appears in this release because no independent second coding exists. See [Contributing evidence and coding changes](contributing-evidence.md) for how to submit one.

Because the key states the expected primary code in the same row as the source URL, a coder cannot reach the thread without reading the answer. `data/derived/reliability_subset_blind.csv` is the generated coder-facing projection that withholds it, and it is the file a second coding pass uses.

## Claim traceability

Every approved claim in `data/derived/publication_claim_ledger.csv` is bound to the LaTeX sources twice when `paper/` is present: by a `% claim: Cnn` marker next to the supporting passage, and by a `Manuscript anchor` substring that must appear in that passage. `make claims` fails if either binding is lost. The public inferential boundary is [CLAIM_BOUNDARIES.md](https://github.com/fraware/lab-automation-observatory/blob/main/CLAIM_BOUNDARIES.md).

## Publication robustness

The repository separates headline metric inputs from publication stress tests. Headline case data remains under `data/metrics/`; deterministic stress-test outputs are generated under `data/robustness/`.

### Partial-score sensitivity

`data/robustness/partial_score_sensitivity.csv` recomputes IAS, RMC, PDC, and OC after replacing every component score of `0.5` with `0`, `0.25`, `0.5`, `0.75`, and `1`. Complete, absent, and unknown cells are unchanged. The output reports the across-case mean, case count, known cells, and unknown cells.

This analysis exposes dependence on the numerical encoding of partial evidence. It does not calibrate a probability, estimate a population parameter, or make the four instruments comparable to one another.

### Leave-one-thread-out associations

`data/robustness/association_leave_one_out.csv` deletes each of the 55 selected threads once and recomputes all 28 B2–B9 associations. For every pair it records the full-register phi and lift, deletion ranges, rank range, top-five retention, and retention of the pilot attention threshold.

This is a descriptive influence analysis over a purposive multi-label register. It is not a population jackknife and supplies no inferential interval.

### Regeneration

```bash
make robustness
make validate
make test
```

`make derived` also regenerates the robustness CSVs. `make tables` regenerates their supplementary LaTeX tables when `paper/` is present. `scripts/validate_release.py` fails when either CSV has drifted from its source data.

## Public-data handling

The release contains derived coding, short anonymized quotations, and source links. It excludes a verbatim corpus and user handles. No automated forum collection is required to reproduce the published results.
