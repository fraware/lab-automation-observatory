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

Every approved claim in `data/derived/publication_claim_ledger.csv` is bound to the LaTeX sources twice: by a `% claim: Cnn` marker next to the supporting passage, and by a `Manuscript anchor` substring that must appear in that passage. `make claims` fails if either binding is lost.

## Public-data handling

The release contains derived coding, short anonymized quotations, and source links. It excludes a verbatim corpus and user handles. No automated forum collection is required to reproduce the published results.
