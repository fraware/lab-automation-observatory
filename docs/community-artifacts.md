# Community artifacts

## Evidence atlas

`data/derived/evidence_atlas.csv` and its generated
[Markdown summary](generated/evidence_atlas_summary.md) are a community
artifact in their own right: a scannable, one-row-per-construct entry point
into the coded evidence, with a bounded metric, a quotation, a retained
counterexample, and the key supporting threads for each of the ten named
bottlenecks. See [Evidence atlas](evidence-atlas.md) for what a row means,
how to trace it back to the primary evidence, and what it does not support.

## Troubleshooting question

The JSON Schema defines the universal core of a reproducible technical question and conditionally requires physical-state and intervention fields after partial execution.

## Resolved-knowledge index

Each record contains applicability, evidence, root-cause status, resolution, validation stage, evidence grade, limitations, maintenance ownership, last verification, provenance, and lifecycle status.

## Hard-case adjudication set

`data/derived/reliability_subset.csv` is released as a community artifact in its own right. It fixes the competing codes and adjudication questions for the fourteen hardest threads so that an independent coder can repeat those decisions and report agreement. It carries no agreement statistic, because none exists yet.

A second coder works from the generated projection `data/derived/reliability_subset_blind.csv` instead, which withholds the expected primary code, the plausible alternative, and the reason disagreement is likely. The key states all three in the same row as the source URL, so it cannot be used for a blind pass. See [Contributing evidence and coding changes](contributing-evidence.md).

## Planned registries

- device-integration accessibility: schema draft, seven checked seed records, and a stated contribution path — see
  [Device-interface accessibility registry](device-interface-registry.md);
- physical-resource definitions with evidence grades;
- minimal laboratory event schema: design proposal, JSON Schema, example streams, and a reference scoring path at
  [Run-event schema](event-schema.md) (`schemas/run-event.schema.json`, `data/run_event_examples/`, `labauto_observatory.run_events`);
- scheduling benchmarks with scientific constraints.

Each artifact has an evaluation plan. Publication alone is not treated as success.
