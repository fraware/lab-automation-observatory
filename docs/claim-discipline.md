# Claim discipline

The publication claim ledger is the review boundary for this project.

## Approved classes

- descriptive corpus result;
- bounded case-study metric;
- source-reported quantitative claim;
- mechanism hypothesis with descriptive association;
- interpretive synthesis.

## Excluded claims

The release cannot support vendor reliability, installed-base, market-share, industry prevalence, or causal-effect claims. Simulation results cannot be presented as wet-lab or assay results unless the underlying evidence reaches those stages.

Rejected claims stay in the ledger rather than being deleted, because the recorded boundary is what keeps the nearby overclaim out of later drafts.

## Machine-checked traceability

The ledger is bound to the manuscript in two ways, and `make claims` fails if either binding is lost:

1. a `% claim: Cnn` comment marker in the LaTeX source, immediately before the passage that carries the claim;
2. the ledger's `Manuscript anchor`, a distinctive substring of the published wording that must appear in the body text of a file carrying that marker.

Anchors are matched against body text only. LaTeX comments are stripped first, so a marker or an editorial note can never satisfy an anchor. The check also fails when a marker names an unknown claim, when an approved claim has no anchor, and when a rejected claim is marked or anchored. `make validate` runs the same check and writes a review table to `build/claim_traceability.md`.

## Reliability claims

The pilot is single-coder and reports no inter-rater statistic. `data/derived/reliability_subset.csv` publishes the hard-case adjudication set so that an independent second coding pass can be performed against a fixed set of competing codes and adjudication questions. No agreement coefficient may be added to the repository or the manuscript before that second pass exists.
