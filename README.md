<div align="center">

<pre>
  
  _       _                   _                        _   _             
 | | __ _| |__     __ _ _   _| |_ ___  _ __ ___   __ _| |_(_) ___  _ __  
 | |/ _` | '_ \   / _` | | | | __/ _ \| '_ ` _ \ / _` | __| |/ _ \| '_ \ 
 | | (_| | |_) | | (_| | |_| | || (_) | | | | | | (_| | |_| | (_) | | | |
 |_|\__,_|_.__/   \__,_|\__,_|\__\___/|_| |_| |_|\__,_|\__|_|\___/|_| |_|
        _                              _                                 
   ___ | |__  ___  ___ _ ____   ____ _| |_ ___  _ __ _   _               
  / _ \| '_ \/ __|/ _ \ '__\ \ / / _` | __/ _ \| '__| | | |              
 | (_) | |_) \__ \  __/ |   \ V / (_| | || (_) | |  | |_| |              
  \___/|_.__/|___/\___|_|    \_/ \__,_|\__\___/|_|   \__, |              
                                                     |___/               
          
</pre>

 where laboratory automation work breaks - measured, not guessed
 
</div>

<p align="center">
  <a href="https://api.reuse.software/info/github.com/fraware/lab-automation-observatory"><img alt="REUSE status" src="https://api.reuse.software/badge/github.com/fraware/lab-automation-observatory"></a>
</p>

<p align="center">
  <a href="#what-you-get">What you get</a> &middot;
  <a href="#ten-bottlenecks-five-layers">Bottlenecks</a> &middot;
  <a href="#principal-results">Results</a> &middot;
  <a href="#reproduce-it">Reproduce</a> &middot;
  <a href="#contribute">Contribute</a>
</p>

Laboratory automation fails in specific, repeatable places: a driver that will not
talk to a device, a deck definition that omits a physical property, a run that
half-finishes and leaves no record you can reconstruct. Practitioners describe
those failures in public, in operational detail, and then the detail is lost in
the thread that produced it.

This repository turns a set of those public discussions into something you can
check, cite, reuse, and disagree with: a coded evidence base, metrics with
explicit denominators, and ready-to-use artifacts for asking better technical
questions and keeping the answers.

## What you get

- **A coded evidence base.** 55 purposively selected public threads and 45
  analytical episodes drawn from a deliberately difficult 14-thread subset, coded
  against written inclusion, exclusion, and boundary rules.
- **Ten named bottlenecks** across five layers of the automation stack, each with
  a definition you can argue with rather than a label you have to accept.
- **Bounded metrics** with the unit and denominator attached to every number, plus
  the raw field-level inputs behind them.
- **Artifacts you can adopt today** — a minimum reproducible question template, a
  governed record format for resolved knowledge, and ten seeded records.
- **A pipeline that reproduces itself.** One command recomputes every published
  value; the test suite fails if any of them drifts.

## Ten bottlenecks, five layers

| Layer | Code | Bottleneck |
|---|---|---|
| Ecosystem knowledge and support | B1 | Knowledge packaging and canonicalization |
| | B10 | Documentation, training, and support dependence |
| Interfaces and representations | B2 | Driver and interface accessibility |
| | B3 | Method, configuration, calibration, and runtime entanglement |
| | B4 | Incomplete physical-resource definitions |
| Runtime coordination | B5 | Fragmented observability and evidence semantics |
| | B6 | Partial execution and recovery |
| | B7 | Scheduling requirements and capability ambiguity |
| Evaluation semantics | B8 | Testing and validation semantics |
| AI context and physical feedback | B9 | AI context and physical-feedback gap |

Full inclusion rules, exclusion rules, and boundary tests live in
`data/derived/taxonomy_rules.csv` and are summarized in
[docs/methods.md](docs/methods.md).

## Principal results

| Metric | Pilot value | Measured over |
|---|---:|---|
| Integration Accessibility Score | 63.9% | six device–interface cases |
| Reproducibility Manifest Completeness | 54.2% | three deployment objects |
| Physical Definition Completeness | 67.0% | four resource definitions |
| Observability Coverage | 52.5% | four execution/diagnostic cases |
| Preflight Preventability | 66.7% | three definitely classified scenarios |
| Scheduling constraint discovery | 87.5% | eight incomplete requirement classes |
| Fully aligned test claims | 33.3% | six bounded claims |
| Core AI context-expansion ratio | 2.0× | five opening context classes |
| Fully actionable documentation outcomes | 41.7% | twelve documentation-centered cases |

**How to read this table.** Every figure describes the named set of cases in the
right-hand column and nothing else. The denominators are small on purpose: each
case was scored field by field against a written rubric, and the inputs are
committed so you can re-score them yourself. Read `54.2%` as "mean manifest
completeness across the three deployment objects we examined," not as a rate for
the field.

The strongest technical association in the pilot links fragmented observability
(B5) to partial execution and recovery (B6), with `phi = 0.452` and
`lift = 2.353`. We publish it as a mechanism hypothesis worth testing, not as a
causal estimate.

## Reproduce it

Reproduction reads only the derived data committed in this repository. Nothing
queries the forum.

```bash
git clone https://github.com/fraware/lab-automation-observatory.git
cd lab-automation-observatory
uv sync --all-extras

make reproduce   # recompute every published value into build/results.json
make test        # assert published values, schemas, and generated outputs
```

`make reproduce` also writes a readable summary to `build/RESULTS.md`.
`make ci` runs lint, types, schema validation, tests, and the docs build.

Manuscript sources under `paper/` are **local-only** and are not published to
this repository. Venue PDFs, LaTeX sources, and submission bundles stay on the
maintainer machine; public GitHub Releases carry data/code assets only.
`make paper` / `make paper-only` work only where a local `paper/` tree exists.

On Windows, GNU Make is not installed by default;
[REPRODUCIBILITY.md](REPRODUCIBILITY.md#windows-and-powershell) lists the
PowerShell equivalents, along with exactly which generated artifacts are tracked.

## Use the artifacts

These are meant to be lifted out of the repository and used in your own lab,
forum, or internal wiki.

| Artifact | Path | Use it to |
|---|---|---|
| Troubleshooting question | `data/derived/troubleshooting_template.csv` | Ask a question someone else can actually reproduce |
| Question schema | `schemas/troubleshooting-question.schema.json` | Enforce that template in a form, bot, or CI check |
| Resolved-knowledge record | `schemas/knowledge-index.schema.json` | Store an answer with its scope, evidence, owner, and expiry |
| Ten seed records | `data/knowledge_index/seed_records.yaml` | See the format filled in against real discussions |
| Hard-case adjudication set | `data/derived/reliability_subset_blind.csv` for coding, `data/derived/reliability_subset.csv` for the key | Re-code the fourteen hardest threads and report agreement |
| Evidence atlas | `data/derived/evidence_atlas.csv`, browsable at [docs/generated/evidence_atlas_summary.md](docs/generated/evidence_atlas_summary.md) | Trace a named bottleneck to its quotes, counterexamples, key sources, and bounded metric |

The question schema requires the universal core of a reproducible problem report
and adds physical-state and intervention fields once a run has partially
executed — the point at which a description usually stops being useful. The
knowledge record keeps applicability, root-cause status, validation stage,
evidence grade, maintainer, and last-verified date attached to the answer, so a
simulation result can never quietly become a wet-lab result.

Publishing an artifact is not success. Judge these on whether they reduce
clarification rounds, shorten time to an actionable answer, stop the same
question from returning, keep records from going stale silently, and get final
outcomes recorded. Details in [docs/index.md](docs/index.md).

## Contribute

Contributions are welcome, and the most valuable ones are not code. Pick a lane:

- **Run a second coding pass.** This is the highest-value contribution in the
  repository. Code the threads in `data/derived/reliability_subset_blind.csv`
  from the public sources, answer the recorded adjudication questions, and submit
  your codes. Use the blind sheet only: the full key
  `data/derived/reliability_subset.csv` states the expected primary code in the
  same row as the source URL, so reading it makes the pass unusable for an
  agreement statistic. That is what turns a single-coder pilot into a measured
  one.
- **Correct a coded row.** If a thread was read wrong, say which boundary test it
  fails and why. Counterexamples are kept, not quietly dropped.
- **Propose a taxonomy change.** Splits, merges, and additions are expected. Say
  what your version predicts that the current one does not.
- **Bring a hard case.** A public thread that the taxonomy handles badly is more
  useful than one that fits.
- **Add or refresh a knowledge record.** Records need an owner and a verification
  date, or they rot.
- **Add a device-interface registry record.** The schema, seven checked seed
  records (six pilot cases plus one community-intake example), and a stated
  contribution path are at
  [docs/device-interface-registry.md](docs/device-interface-registry.md). One
  interface path, one public source, and the limitations and prohibited claims
  the evidence actually supports; `make validate` checks the rest. Schema
  questions belong on
  [issue #12](https://github.com/fraware/lab-automation-observatory/issues/12).

Two documents cover everything you need:
[CONTRIBUTING.md](CONTRIBUTING.md) for pull-request mechanics, and
[docs/contributing-evidence.md](docs/contributing-evidence.md) for a
step-by-step walkthrough of each change type above.

The ground rules, in one breath: link a public source; keep "unknown" distinct
from "absent"; claim only what your evidence reached; and update the tests when a
published number moves. Published numbers stay inside
[CLAIM_BOUNDARIES.md](CLAIM_BOUNDARIES.md); with a local `paper/` tree,
`make claims` checks manuscript bindings.

Hosted CI is deliberately not triggered on pull requests, so `make ci` on your
own machine is the authoritative check. Run it before you open one.

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before opening a discussion.

## Repository map

```text
src/labauto_observatory/  Metric and validation library
data/derived/             Public derived coding records
data/metrics/             Field-level metric inputs and association results
data/knowledge_index/     Seed resolved-knowledge records
schemas/                  JSON Schemas for community artifacts
scripts/                  Reproduction, figure, table, and validation commands
tests/                    Published-value, schema, and metric tests
docs/                     Methods, data dictionary, and artifact guides
artifacts/                Audit records, release notes, and provenance
paper/                    Local-only manuscript tree (gitignored; not on GitHub)
```

## Documentation

| Read this | For |
|---|---|
| [docs/index.md](docs/index.md) | Docs map and community-artifact summary |
| [docs/methods.md](docs/methods.md) | Corpus, coding, adjudication, robustness |
| [docs/data-dictionary.md](docs/data-dictionary.md) | Every column in every derived file |
| [docs/evidence-atlas.md](docs/evidence-atlas.md) | How to read one atlas row |
| [CLAIM_BOUNDARIES.md](CLAIM_BOUNDARIES.md) | Supported and unsupported inference; claim ledger rules |
| [REPRODUCIBILITY.md](REPRODUCIBILITY.md) | Environment, generated outputs, Windows notes |
| [artifacts/README.md](artifacts/README.md) | Current audit and release-notes index |
| [docs/project.md](docs/project.md) | Governance, ethics, data use, roadmap |
| [docs/device-interface-registry.md](docs/device-interface-registry.md) | Device-interface registry draft |
| [docs/event-schema.md](docs/event-schema.md) | Run-event schema draft and B5/B6 scoring path |
| [submissions/README.md](submissions/README.md) | Venue publication line (manuscripts local-only) |

`make docs` serves MkDocs at `http://127.0.0.1:8000`; `make docs-build` renders
`site/` with warnings as errors. The `Docs site` workflow
(`.github/workflows/pages.yml`) deploys on manual dispatch.

## Data, ethics, and licensing

This repository contains derived codes, short anonymized quotations, and links to
the public sources. It does not redistribute a verbatim forum corpus or user
handles. Outcomes are treated as censored when a discussion moves to private
support, direct messages, meetings, or local implementations, because a thread
going quiet is not the same as a problem being solved. See
[docs/project.md](docs/project.md).

Code is Apache-2.0. Original documentation and derived data are CC BY 4.0. Forum
content remains owned by the people who wrote it. Per-file licensing follows
[REUSE](https://reuse.software/); see [LICENSES/](LICENSES).

## Citation

Cite this repository using the metadata in [CITATION.cff](CITATION.cff).
Manuscript bibliography sources live in the local-only `paper/` tree.
