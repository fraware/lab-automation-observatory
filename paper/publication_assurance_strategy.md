# Publication assurance strategy

This document separates software verification from scientific assurance and submission-artifact control. A high test count is useful evidence about the implementation. It does not, by itself, establish coding validity, source fidelity, or the scope of the paper's empirical claims.

## Assurance objects

The release contains six distinct objects that require different tests:

1. **Source evidence** — forum pages, short quotations, dates, later updates, and product-report status.
2. **Coded evidence** — thread-level direct-support flags, primary codes, episode boundaries, modifiers, and counterexamples.
3. **Metric inputs** — bounded cases, score components, eligibility rules, denominators, and unknown values.
4. **Derived results** — proportions, component means, Wilson intervals, associations, sensitivity analyses, tables, and figures.
5. **Manuscript claims** — normalized wording, source and data anchors, validation stage, and prohibited overclaim.
6. **Submission artifacts** — PDFs, LaTeX source, supplement, cover letter, graphical abstract, metadata, archive, and checksums.

A release is publishable only when all six objects are tied to the same frozen commit.

## Gate 1 — source and quotation fidelity

Required checks:

- one machine-readable audit row for every forum/site citation used in the manuscript and every quotation in `quote_bank.csv`;
- verified URL, title, date, approved quotation, surrounding context, later-update check, product-report status, and claim boundary;
- no silent correction of grammar, capitalization, or omitted words inside direct quotations;
- explicit ellipses for omitted words and `[sic]` where preserving an error is material;
- a source correction must update the audit ledger, quote bank, generated quotation table, manuscript or supplement, and tests in the same change set.

Release blocker: the complete 24-record source/quotation audit ledger described in issue #13 must be committed. The seven known quotation corrections have an approved wording and should be applied before the canonical bundle is built.

## Gate 2 — coding-instrument integrity

Required checks:

- the manuscript and documentation must direct any independent coding pass to `reliability_subset_blind.csv`, never to the answer-bearing key;
- the primary-code tie-break, read scope, episode unit, expected episode count, first-post anchor, and counterexample target must be explicit;
- every episode primary and ecosystem modifier must have direct support on its own thread;
- primary-code and direct-support changes must regenerate all dependent counts and associations;
- the three-thread adjudication pilot is described as process validation only. It is neither an independent second coding pass nor an agreement result.

The manuscript remains a single-coder pilot. An independent second pass is a useful extension and is not a publication blocker while the paper reports no inter-rater statistic.

## Gate 3 — data and metric integrity

The release validator must fail on:

- missing or duplicated identifiers;
- unexpected row counts;
- undocumented categorical values;
- component scores outside the declared domain;
- unknown values converted silently to zero;
- derived score columns inconsistent with their components;
- numerator or denominator drift;
- mismatches among evidence register, episodes, metric cases, claim ledger, generated tables, and figures;
- record reordering that changes a result.

Every bounded proportion must carry its numerator, denominator, and descriptive interval. Every component mean must carry its known-cell and unknown-cell counts. Component means are rubric summaries, not probabilities.

## Gate 4 — scientific robustness

### 4.1 Partial-score weighting

IAS, RMC, PDC, and OC use scores in `{0, 0.5, 1}`. Recompute each mean with the partial score replaced by `0`, `0.25`, `0.5`, `0.75`, and `1`. Report the complete curve in the supplement. The purpose is to show which conclusions depend on the conventional midpoint treatment. The four measures remain distinct instruments and must never be compared as one common performance scale.

### 4.2 Association stability

For all 28 B2–B9 pairs:

- perform leave-one-thread-out recomputation across all 55 selected threads;
- record the minimum and maximum phi, rank range, and number of deletions retaining a top-five rank;
- retain the existing one-overlap recoding sensitivity;
- identify pairs that cross the pilot attention threshold under either analysis;
- treat B8–B9 as exploratory because B9 has five coded threads;
- use the corrected current B2–B7 full-corpus value (`phi = 0.382`, lift `= 2.037`) as the baseline. Earlier robustness tables built around `phi = 0.409` are superseded.

Do not add p-values, bootstrap population intervals, or causal wording. The corpus is purposive and the units are multi-label forum threads.

### 4.3 Denominator adversarial review

Review eligibility without viewing the resulting point estimate:

- **B6:** distinguish observed incidents, deliberately triggered cases, hypothetical scenarios, and feature requests;
- **B7:** determine which fields are required for the stated scheduling decision and which are optional detail;
- **B8:** normalize the exact claim before judging alignment;
- **B9:** document ontology overlap and conservative grouping rules;
- **B10:** distinguish public actionable resolution, partial resolution, private migration, and operational outcome unknown.

Any eligibility change must be logged with its effect on the numerator, denominator, claim wording, tables, figures, and tests.

### 4.4 Mutation and property tests

Prioritize mutations that could alter published conclusions:

- score changes and unknown/zero swaps;
- dropped or duplicated rows;
- changed direct-support flags;
- changed claim anchors or prohibited-overclaim fields;
- reordered data;
- missing registry or schema invariants;
- stale generated artifacts;
- mismatched release versions or dates.

A surviving mutation affecting a published value, claim anchor, or release identity blocks publication. Coverage percentage alone is not the release criterion.

## Gate 5 — claim traceability

Every approved claim must have:

- a stable claim identifier;
- a manuscript anchor;
- an evidence source;
- a bounded denominator or explicit qualitative scope;
- approved wording;
- a prohibited overclaim;
- a sensitivity or limitation statement;
- a test that fails when its source value or anchor drifts.

Design drafts such as the device-interface registry and run-event schema remain community artifacts and future-work infrastructure. They do not become empirical results unless evaluated on independent records.

## Gate 6 — deterministic document build

Build from a clean checkout of one frozen commit using the locked environment:

```bash
uv sync --frozen --all-extras
make ci
git diff --exit-code
```

Then compile the manuscript, supplement, cover letter, and graphical abstract. The release gate requires:

- no missing references or unresolved citations;
- no Type 3 fonts in submission PDFs;
- embedded fonts and extractable text;
- no clipping, overlap, blank pages, broken glyphs, or missing figures;
- page-by-page visual inspection;
- a clean working tree after deterministic regeneration.

The v0.1.3 audit did not re-run the TeX build after claim-affecting changes. Its recorded document check cannot certify the current submission files.

## Gate 7 — bundle identity and venue parity

Each venue bundle must be generated from the same frozen commit and include a manifest with:

- project version and commit SHA;
- repository URL and tag;
- venue and article type;
- data-tree hash and source-tree hash;
- build environment and command;
- manuscript, supplement, cover-letter, graphical-abstract, archive, and checksum hashes;
- DOI, preprint, ORCID, and identifier status;
- creation timestamp;
- superseded-bundle list.

File names must include the target, version, date, and commit prefix. Do not use an unqualified `final` filename. The July 28, 2026 SLAS bundle is superseded and must not be uploaded.

After portal upload, inspect the portal-generated PDF and compare its text, pages, figures, and references with the approved local render.

## Non-blocking future validation

The following work can strengthen later versions without delaying a transparently framed SLAS pilot:

- independent coding of the blind hard-case pack;
- prospective evaluation of the troubleshooting template;
- real laboratory run-event streams;
- external contributions to the device-interface registry;
- replication on a second public technical source.

These become required only for stronger agreement, intervention-effect, external-validity, or software-adoption claims.
