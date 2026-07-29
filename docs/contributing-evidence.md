# Contributing evidence and coding changes

This guide explains how to propose a change to the coded registers, the metric inputs, the publication claim ledger, or the resolved-knowledge index. It complements [CONTRIBUTING.md](https://github.com/fraware/lab-automation-observatory/blob/main/CONTRIBUTING.md), which covers the pull-request mechanics, and the [data dictionary](data-dictionary.md), which defines every column. If you are correcting something already in the release rather than adding new material, [docs/correction-workflow.md](correction-workflow.md) defines the accepted correction kinds, the minimum evidence for each, which files usually move together, and whether a correction is note-only, claim-affecting, or release-blocking.

## What counts as admissible evidence

- A public, linkable source. Every new or corrected row needs a `Source URL`.
- Derived coding only. Do not add verbatim thread text, user handles, profile attributes, or private correspondence.
- Short quotations must satisfy the quote-eligibility rule in `data/derived/codebook.csv`: short, technically material, non-identifying, context-preserving, linked, and within source quotation limits.
- Unknown must stay distinguishable from absent. Leave a cell empty rather than writing `0` when the public evidence does not settle the question.

## Choose the change type

### Correct a coded row

Applies to `data/derived/evidence_register_part_*.csv` and `data/derived/episode_register_part_*.csv`. See [docs/correction-workflow.md](correction-workflow.md) for how this and every other correction kind is classified and checked.

1. Quote the boundary test from `data/derived/taxonomy_rules.csv` for the code you are adding or removing, and say why the thread passes or fails it.
2. Keep `Primary` to exactly one code. Direct-support flags are multi-label, but a flag requires directly evidenced mechanism or consequence, not topical adjacency.
3. Update `Analytical note` or `Coding note` with the reason for the change, so the boundary decision stays reviewable.
4. Re-run the checks below. Any change to counts will move published values and the assertions in `tests/test_published_values.py`.

### Add a thread or an episode

State the selection rationale. The register is a purposive frame built for conceptual coverage and metric design, so an addition should extend coverage, add a hard case, or add a counterexample. It should not be justified by frequency, because the register does not estimate prevalence. Episodes are only added for threads in the difficult subset; each episode needs its own initiating problem, lifecycle stage, and primary code.

#### What counts as one episode

An episode is a contiguous run of posts, identified by the anchor of its first post, that either raises a new initiating problem or moves to a new lifecycle stage. Two adjacent runs that share both their initiating problem and their primary code are one episode. A single retrospective post that narrates several stages is one episode unless the separate stages are independently evidenced elsewhere in the thread.

Without this definition an independent coder's episode count is unpredictable rather than merely uncertain, which is what the adjudication pilot found. Applying it to the committed 45 episodes leaves the segmentation unchanged: wherever two adjacent runs carry the same primary code, they differ in initiating problem, in lifecycle stage, or in both. Record the anchor of the first post in `First post anchor` when the public thread exposes one, so that two segmentations can be compared post by post rather than only counted.

The expected number of episodes for each of the 14 hard threads is stated as an exact count in the `Episode segmentation required` column of `data/derived/reliability_subset.csv`, and `make validate` fails if that count and the episode register disagree. A re-segmentation therefore has to move both.

### Change a metric input

Applies to `data/metrics/*.csv`.

1. Keep the `0 / 0.5 / 1 / empty` encoding. A score of `1` means the property is explicitly and completely evidenced.
2. Do not change a metric's unit or denominator without saying so explicitly in the pull request, because the unit is part of every published claim.
3. Fill `Interpretation` and `Invalid inference` for the affected rows.
4. Update the expected values in `tests/test_published_values.py` in the same pull request, and regenerate `paper/generated/` with `make tables`.

### Change or add a published claim

Applies to `data/derived/publication_claim_ledger.csv`.

1. Set `Claim class`, `Evidence source`, `Denominator / scope`, `Safe wording`, `Prohibited overclaim`, and `Sensitivity / limitation`. An approved claim without a prohibited overclaim fails validation.
2. Set `Manuscript anchor` to a distinctive substring of the published wording. Avoid characters that LaTeX escapes, such as `%`, and avoid text that only appears in a comment.
3. Add a `% claim: Cnn` marker in the LaTeX source immediately before the passage that carries the claim. The anchor must appear in the body text of a file that carries the marker.
4. Run `make claims`. The check fails when an approved claim has no marker, when its anchor is missing from the manuscript, when the marker and the anchor sit in different files, or when a rejected claim is marked.

Rejected claims stay in the ledger. They document the boundary and must carry no marker and no anchor.

### Add or update a knowledge-index record

Applies to `data/knowledge_index/seed_records.yaml` and `seed_records.json`, which must stay identical.

1. Use a new unique `record_id`. Record identifiers are checked for uniqueness by `scripts/validate_release.py`.
2. Record `Root-cause status` and `Validation stage` honestly. Unknown root cause is a valid state; a simulation result must not be recorded as a wet-lab result.
3. Set `Evidence grade` so that a declared value is never presented as equivalent to an independently reproduced one.
4. Name a maintainer and a `Last verified` date. A record without ownership will go stale silently.
5. Supersede rather than overwrite. Link the superseding record instead of rewriting history.
6. Keep `Forum provenance`. The index exposes the current bounded answer and links back to the discussion; it does not replace it or remove contributor credit.

### Propose a taxonomy change

Taxonomy changes are welcome and expected. A proposal should state which construct is split, merged, or added; give the new inclusion rule, exclusion rule, primary-code eligibility, required evidence, and boundary test; and identify the coded rows that would move. Explain what the change predicts that the current taxonomy does not.

## Contribute a second coding pass

The pilot is single-coder and reports no inter-rater statistic. The prepared instrument for changing that is split into two files, and which one you open decides whether your codes can support an agreement statistic at all:

| File | Audience | Contents |
|---|---|---|
| `data/derived/reliability_subset_blind.csv` | Second coders | Thread, source URL, adjudication question, expected episode count, priority |
| `data/derived/reliability_subset.csv` | Maintainers, after the pass | The same rows plus `Expected primary`, `Plausible alternative`, and `Why disagreement is likely` |

**Use the blind sheet only.** The key names the expected primary code in the same row as the source URL, so anyone who opens it to find the thread has already read the answer. That is why the adjudication pilot could not be blind, and it is the reason the blind projection exists. The blind sheet is generated from the key by `make derived`, and `make validate` fails if the two fall out of step, so the blind sheet is never a stale copy.

An independent coder can:

1. code the threads listed in `reliability_subset_blind.csv` from the public sources, without opening `reliability_subset.csv`;
2. answer the recorded adjudication questions;
3. submit the independent codes and the resulting agreement on primary code and on episode boundaries.

Before doing that, read [artifacts/adjudication_pilot_v0.1.2.md](https://github.com/fraware/lab-automation-observatory/blob/main/artifacts/adjudication_pilot_v0.1.2.md). It is a process validation of this instrument on three critical threads, not a second coding pass, and it records the selection and segmentation rules that still need tightening.

Do not add an agreement coefficient to the repository or the manuscript until an independent second coding exists. Publishing the disagreement surface in advance is what makes a later statistic meaningful, and it prevents agreement from being computed on the unambiguous threads only.

## Checks to run

```bash
uv sync --all-extras
uv run python scripts/build_associations.py
uv run python scripts/build_evidence_atlas.py
uv run python scripts/build_atlas_summary.py
uv run python scripts/build_blind_subset.py
uv run python scripts/validate_release.py
uv run pytest
uv run python scripts/reproduce_results.py
uv run python scripts/build_tables.py
uv run python scripts/build_figures.py
```

Or, with GNU Make available:

```bash
make derived
make validate
make test
make reproduce
make tables
make figures
```

`make derived` must run first: `data/metrics/pairwise_associations.csv`, `data/derived/evidence_atlas.csv`, `data/derived/reliability_subset_blind.csv`, and `docs/generated/evidence_atlas_summary.md` are all computed from the register, the metric files, the adjudication key, or the atlas itself, and `make validate` fails if any of them is left stale.

Commit any resulting changes to the derived CSVs, the generated atlas summary, `paper/generated/`, and `paper/figures/*.pdf`. See [REPRODUCIBILITY.md](https://github.com/fraware/lab-automation-observatory/blob/main/REPRODUCIBILITY.md) for the Windows and PowerShell equivalents.

## What will be declined

- Prevalence, market-share, installed-base, or vendor-reliability claims derived from discussion counts.
- Causal claims derived from co-occurrence.
- Inter-rater reliability numbers without an independent second coding pass.
- Deeper validation claims than the underlying evidence reached, such as presenting a simulation result as a wet-lab or assay result.
- Copied forum threads, user profiles, or private correspondence.
