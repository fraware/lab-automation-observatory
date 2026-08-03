# Adjudication pilot on three critical threads

**Status: process validation of the coding instrument only.** This memo does not report inter-rater reliability, does not constitute the independent second coding pass requested in [issue #11](https://github.com/fraware/lab-automation-observatory/issues/11), and does not license any agreement coefficient in the manuscript or the repository. The single-coder limitation stated in [README.md](../README.md) and [docs/contributing-evidence.md](../docs/contributing-evidence.md) is unchanged by this run. The purpose was narrow: find out whether the published rules are usable for selecting a primary code and for segmenting episodes, before anyone spends effort on all fourteen threads.

Date of run: 2026-07-29, against the post-`v0.1.2` working tree.

## Scope

The three threads are the first three rows of `data/derived/reliability_subset.csv` whose `Priority` is `Critical`, taken in file order:

| Thread ID | Thread | Registered episodes |
|---|---|---|
| 2 | Database storing common Labware specifications | `T02-E1`, `T02-E2`, `T02-E3` |
| 4 | 50ul Tip Troubleshooting Report / Post-Mortem | `T04-E1`, `T04-E2`, `T04-E3` |
| 5 | User feedback on Schedulers | `T05-E1`, `T05-E2`, `T05-E3` |

The remaining eleven threads were not coded. The per-thread record is `artifacts/adjudication_pilot_three_threads.csv`.

## Protocol actually followed, and where it departed from the intended protocol

Coding used the public `Source URL` for each thread plus `data/derived/taxonomy_rules.csv` and `data/derived/codebook.csv`. All three sources were retrievable. For thread 2, pages one and two and post 65 were read; for thread 5, both pages, of which the second holds only a one-line aside; for thread 4, both posts.

Two departures matter and are stated here rather than in a footnote.

First, the intended blindness was not achieved, and could not have been. `reliability_subset.csv` places `Expected primary`, `Plausible alternative`, and `Why disagreement is likely` in the same row as `Source URL`, `Specific adjudication question`, and `Episode segmentation required`. A coder cannot obtain the thread to read or the question to answer without also reading the answer key. The expected primary was therefore visible before the independent codes were recorded. This is finding F1 below and it is the most consequential result of the pilot.

Second, the coder here is the same agent working in the same repository as the original coding, not an independent person. Nothing in this run substitutes for a second human coder, and the codes recorded here are best understood as a re-derivation of the rules rather than an independent judgement.

Both departures point the same way: no agreement statistic may be computed from this run, which is consistent with the instruction under which it was performed.

## What happened

Independent primary codes matched the expected primary on threads 4 and 5 and diverged on thread 2. Two matches out of three is reported here only as a description of this run. It is not an agreement rate: n is three, the threads were selected because they are hard, the pass was not blind, and the coder was not independent.

The more informative result is that the two matches were reached directly from the boundary tests with no hesitation, while the one divergence was not caused by a vague construct. Both B1 and B4 are clearly defined, both were primary-eligible for thread 2, and the rules do not say how to choose between two eligible codes. The instrument's own prediction for thread 2 ("the thread moves from missing physical definitions to repository design and then to off-forum coordination") was accurate about where the tension is; what is missing is the rule that resolves it.

Episode segmentation was less stable than primary coding in every one of the three threads. On thread 4 the same wording supports either one episode or three. On threads 2 and 5 the independent segmentation produced more episodes than the register holds, and in both cases the additional segments carry evidence the register does not currently expose.

**Verdict on rule sufficiency.** The construct definitions are sufficient: each of the ten `Include when` / `Exclude when` / `Boundary test` triples did the work asked of it, and every code assignment in this pilot could be justified by quoting one boundary test. The selection and segmentation rules are not sufficient. Scaling to fourteen threads before fixing them would produce disagreements that are artifacts of the instructions rather than measurements of construct ambiguity, and an agreement coefficient computed over them would be uninterpretable.

## Findings

### F1. The instrument cannot support a blind coding pass as published

`reliability_subset.csv` is one table containing both the coder-facing material and the answer key. Any coder who uses it sees the expected primary. Until this is separated, no pass over this instrument can support an agreement statistic, however carefully it is executed.

### F2. Primary-code selection has no tie-break, and B1's own row contradicts itself

`codebook.csv` defines `Primary bottleneck` as "the proximate obstacle that best explains the thread's central technical or community problem" and says nothing further. For thread 2, both readings are defensible under that sentence: the thread is titled and structured as a database, schema, and hosting discussion, which is squarely inside B1's `Primary-code eligibility` ("Primary only for knowledge-governance, corpus, repository, database, or canonical-answer discussions"); and it names real missing physical attributes, which satisfies B4's `Required evidence`.

The contradiction is inside B1 itself. Its `Primary-code eligibility` invites B1 as a primary for database and repository discussions, while its `Pilot interpretation` says B1 is a "cross-cutting modifier". A coder reading the row top to bottom is told both that B1 may be primary here and that B1 is a modifier. Satisfying a code's `Required evidence` is also not the same as that code being primary, and the rules never say so.

### F3. The episode unit is undefined

`docs/contributing-evidence.md` requires that "each episode needs its own initiating problem, lifecycle stage, and primary code". Thread 4 is a single retrospective post that narrates an incident, a four-cause diagnosis, and a public institutionalisation. Read as discourse segments, that is one episode with one primary code. Read as lifecycle stages, it is the three registered episodes, two of which share primary code B4 and arguably share one initiating problem. Nothing in the current wording selects between these readings, so an independent coder's episode count is unpredictable rather than merely uncertain.

### F4. Episode-boundary agreement is not computable

Two separate reasons. The instrument states targets such as "Yes — at least three episodes", which no segmentation can contradict. And episode rows carry a `Source URL` that is either the thread root or a single post anchor, never the extent of the segment, so two segmentations cannot be compared even when both are recorded. Agreement on episode boundaries, which the contribution guide asks a second coder to submit, currently has no definition.

### F5. `Counterexample` is a boolean, and its scope survives only in free text

Thread 4's post-mortem is a counterexample to B1: tacit cross-machine diagnosis became a dated public artifact with catalogue numbers and a reusable measurement procedure. It is not a counterexample to B10, because the recommended procedure ends in contacting the named collaborators, which is expert-support dependence and therefore weak positive evidence for B10 in the same episode. `T04-E3` records `Counterexample = Yes` and carries B10 as an ecosystem modifier, and the only place that distinction is preserved is the free-text `Coding note`, "Counterexample to weak canonicalization". A second coder can agree with the boolean while disagreeing about which construct it contradicts, and no check can see the difference.

### F6. The coded read scope of a thread is unspecified

Thread 2 runs to at least sixty-five posts across multiple pages, and its most important resource-semantics evidence, including lot-to-lot z-height divergence and a definition invalidated by a moulding change, sits on the second page. A coder who reads only the landing page will code the thread differently from one who reads to the end. The instrument gives a URL but never states what constitutes the coded material.

### F7. A construct gap, deliberately not filled

Thread 5's opening post asks to compare orchestration products on deployment speed, device breadth, and end-user experience. Device breadth maps to B2, end-user experience maps to B10 and B7, and deployment speed maps to nothing: the thread's lead-time evidence, roughly six weeks build to pre-FAT, four to six months for a standard workcell, ten to twelve months from purchase order to commissioning, and third-party component shortages, has no home in the taxonomy. The recommendation is to declare procurement and installation lead time explicitly out of scope rather than to add an eleventh construct. A stated exclusion is cheap and prevents each coder from improvising a different home for the same facts.

### F8. One coherence gap found in passing, reported and not fixed

`T05-E3` records `Ecosystem modifiers = B1; B10`, but thread 5's row in `evidence_register_part_01.csv` has `B1 = 0`. An episode asserts a B1 condition that the thread-level direct-support flags deny. `check_episode_and_adjudication_subsets` verifies that each episode's primary technical code is a construct, and `check_evidence_register` verifies that a thread's primary code implies its own direct-support flag, but nothing ties an episode's primary code or ecosystem modifiers back to the thread-level flags.

This is left unchanged on purpose. Setting `B1 = 1` for thread 5 would move direct-support counts and the assertions in `tests/test_published_values.py`, which is a claim-affecting change and out of scope for a process pilot. The correct sequence is to add the missing check first, then adjudicate whichever rows it flags as a single reviewable correction.

## Recommended rule-text tightenings before scaling to fourteen threads

These are proposals. None of them is applied in this commit, because each touches a validated release file or generated output and should land as its own reviewable change.

**1. Split the instrument into a coder sheet and a key (F1).** Keep `data/derived/reliability_subset.csv` exactly as published so that no documented row count or supplement section changes, and add a generated projection, `data/derived/reliability_subset_blind.csv`, carrying only `Thread ID`, `Thread`, `Source URL`, `Specific adjudication question`, `Episode segmentation required`, and `Priority`. Generate it deterministically and add a drift check next to `pairwise_drift` and `atlas_drift` in `src/labauto_observatory/register_validation.py`, so the blind sheet cannot fall out of step with the instrument it is derived from.

**2. Add a primary-code tie-break rule to `codebook.csv` (F2).** A new row, type `Rule`:

> When more than one code is primary-eligible, the primary is the code whose boundary test fails for the request made in the initiating post. A thread that proposes creating a shared artifact in order to prevent a class of defect takes the ecosystem-condition code; a thread reporting an instance of that defect takes the technical code. Satisfying a code's required evidence makes it direct support, not primary. Record the rejected candidate and the reason in `Analytical note`.

Applied to thread 2, this rule selects B1 and would move the registered primary. Applied to thread 4, it confirms B4. The maintainer may prefer the opposite convention; what matters is that one of them is written down, because whichever is chosen, thread 2 stops being a coin flip.

**3. Remove the contradiction inside B1 (F2).** Replace B1's `Pilot interpretation`, currently "Cross-cutting modifier; frequent co-code should not be interpreted as an independent failure count", with:

> Cross-cutting modifier when it accompanies a technical failure; primary when the thread's object is the artifact, corpus, or governance itself. Frequent co-code should not be interpreted as an independent failure count.

**4. Define the episode unit in `docs/contributing-evidence.md` (F3, F4).** Extend the episode sentence with:

> An episode is a contiguous run of posts, identified by the anchor of its first post, that either raises a new initiating problem or moves to a new lifecycle stage. Two adjacent runs that share both their initiating problem and their primary code are one episode. A single retrospective post that narrates several stages is one episode unless the separate stages are independently evidenced elsewhere in the thread.

**5. Make segmentation targets falsifiable (F4).** Replace `Episode segmentation required` values of the form "Yes — at least three episodes" with an exact expected count, and add a `First post anchor` column to the episode register so that two segmentations can be compared post by post.

**6. Scope `Counterexample` to a code (F5).** Replace the boolean with `Counterexample to`, holding a code list or an empty cell, so that the scope currently buried in `Coding note` becomes structured: an episode can then be recorded as a counterexample to B1 while remaining positive evidence for B10.

**7. State the read scope (F6).** Add a `Read scope` column to the blind coder sheet naming the pages or post range that constitute the coded material for each thread, and record the same scope on the episode rows.

**8. Declare procurement out of scope (F7).** Add to B7's `Exclude when`: "the claim concerns purchasing lead time, installation schedule, or component supply, which are procurement facts outside the taxonomy." Add to B2's `Exclude when`: "the statement is a claim about vendor market structure rather than a specific integration attempt."

**9. Add the missing cross-file check (F8).** Every episode primary technical code and every episode ecosystem modifier must appear as a direct-support flag on that episode's thread. Add the check, then adjudicate what it flags separately.

## Before the full fourteen-thread pass

The three-thread pilot answered the question it was built to answer, and the answer is that the instrument is not yet ready to be handed to a second person. Recommendations 1, 2, 4, and 5 are prerequisites: without the blind sheet no statistic is admissible, and without the tie-break rule and the episode definition the disagreements that a full pass produces will mostly measure the instructions. Recommendations 3, 6, 7, 8, and 9 are quality improvements that can land alongside.

The pilot also did not change what the repository claims. No metric, count, published value, figure, or manuscript sentence moves because of this run, and no agreement coefficient enters the repository from it.

## Data

- `artifacts/adjudication_pilot_three_threads.csv` — one row per thread: independent primary, competing code considered and why it was rejected, the answer to the recorded adjudication question, episode-boundary notes, the expected primary as revealed after coding, primary-code agreement, ambiguity type, and the specific rule text implicated.

The worksheet is kept under `artifacts/` rather than `data/derived/` on purpose. `data/derived/` is the validated release surface that feeds published numbers, and every CSV in it is bound to a documented row count in `src/labauto_observatory/register_validation.py`. This worksheet is a record of a coding process that supports no published claim, so it does not belong in that surface.
