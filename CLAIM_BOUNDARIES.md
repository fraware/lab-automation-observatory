# Claim boundaries

The Lab Automation Observatory is a purposive, single-coder pilot designed for construct development, bounded measurement, robustness analysis, and prospective study design.

## Supported claims

The release supports:

- descriptive findings within the selected 55-discussion register;
- bounded metrics over explicitly named case sets;
- source-reported quantitative claims restricted to their demonstrated validation stage;
- descriptive associations used to prioritize prospective mechanisms;
- qualitative interpretations supported by coded episodes, source audits, and counterexamples;
- design proposals for questions, knowledge records, interface registries, and event schemas.

## Unsupported claims

The release does not support:

- forum-wide or industry-wide prevalence estimates;
- incident or failure rates without operational denominators;
- vendor, product, platform, or supplier reliability rankings;
- market-share or installed-base inference;
- causal effects from co-occurrence or selected cases;
- claims of independent replication for source-reported product results;
- an inter-rater agreement statistic;
- claims that the proposed community artifacts improve outcomes prior to prospective evaluation.

## Required wording discipline

Every quantitative statement must retain its analytical unit, numerator or component set, denominator, sampling frame, validation stage, and material sensitivity. Unknown values remain distinct from zero or absence. Public non-resolution remains distinct from operational non-resolution. Simulation, dry execution, wet execution, assay evidence, and production monitoring remain separate stages.

Every venue-specific manuscript under `paper/` is governed by these boundaries. Framing, structure, title, and contribution emphasis can change by venue. The empirical values and their supported inference cannot.

## Approved claim classes

The publication claim ledger (`data/derived/publication_claim_ledger.csv`) is the review boundary for this project. Approved classes:

- descriptive corpus result;
- bounded case-study metric;
- source-reported quantitative claim;
- mechanism hypothesis with descriptive association;
- interpretive synthesis.

Rejected claims stay in the ledger rather than being deleted, because the recorded boundary is what keeps the nearby overclaim out of later drafts.

## Machine-checked traceability

The ledger is bound to the manuscript in two ways, and `make claims` fails if either binding is lost when `paper/` is present:

1. a `% claim: Cnn` comment marker in the LaTeX source, immediately before the passage that carries the claim;
2. the ledger's `Manuscript anchor`, a distinctive substring of the published wording that must appear in the body text of a file carrying that marker.

Anchors are matched against body text only. LaTeX comments are stripped first, so a marker or an editorial note can never satisfy an anchor. The check also fails when a marker names an unknown claim, when an approved claim has no anchor, and when a rejected claim is marked or anchored. `make validate` runs the same check when `paper/` is present and writes a review table to `build/claim_traceability.md`.

## Reliability claims

The pilot is single-coder and reports no inter-rater statistic. `data/derived/reliability_subset.csv` publishes the hard-case adjudication set so that an independent second coding pass can be performed against a fixed set of competing codes and adjudication questions. No agreement coefficient may be added to the repository or the manuscript before that second pass exists.
