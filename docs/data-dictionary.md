# Data dictionary

## `data/derived/evidence_register_part_*.csv`

One row per selected thread. Direct-support fields B1–B10 are binary. `Primary` records the main analytical construct. `Resolution` records the public outcome only. `Evidence strength` is an ordinal pilot field.

## `data/derived/episode_register_part_*.csv`

One row per segmented analytical episode. Episodes preserve lifecycle stage, primary technical code, ecosystem modifiers, evidence form, consequence, public artifact, counterexample status, and confidence.

## `data/metrics/`

Each file contains the field-level cases underlying one bounded metric. Scores use 0, 0.5, and 1. Unknown remains blank and is not silently converted to zero.

## `data/knowledge_index/`

Contains the public knowledge-record schema fields, ten seed records, and an example troubleshooting question. YAML and JSON seed files contain identical records.
