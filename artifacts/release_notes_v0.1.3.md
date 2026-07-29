# v0.1.3 release notes

A patch release that closes the adjudication-instrument gaps found in the
three-thread pilot, documents the post-0.1.2 sprint artifacts already on `main`,
and scaffolds the Roadmap 0.2 surfaces (evidence atlas site, registry
contribution path, run-event proposal). It **does** change one published
association statistic; everything else hardens process and adds forward-looking
design drafts without widening claim scope.

Four problems drove it:

1. the published adjudication key exposed expected primaries beside the source
   URL, so a second coder could not work blind;
2. the pilot found eight rule gaps (tie-break, episode unit, counterexample
   scope, read scope, procurement exclusions, and others) that let two careful
   coders disagree without violating any written rule;
3. episode codes were never tied back to thread-level direct-support flags, so
   an episode could assert a condition its own thread recorded as unsupported;
4. the repository referenced atlas, registry, and event-schema surfaces in the
   roadmap without checkable seeds or a deployment path.

## Adjudication instrument and rule tightenings

- `data/derived/reliability_subset_blind.csv` is generated from the key by
  `labauto_observatory.blind_subset`; second coders use the blind sheet only.
- A primary-code tie-break rule, B1 pilot-interpretation fix, exact episode
  counts, `Counterexample to` (replacing a boolean), `Read scope`, `First post
  anchor`, and B2/B7 procurement exclusions are written into validated sources
  and documented in `docs/contributing-evidence.md` and
  `docs/data-dictionary.md`.
- Thread 2's primary moves from B4 to B1 under the tie-break; B1 direct-support
  counts rise accordingly.

## Episode-to-thread coherence

- `make validate` now requires every episode primary and ecosystem-modifier code
  to carry direct support on that episode's thread. Eight flagged rows are
  adjudicated: threads 5, 13, and 33 gain thread-level flags their episodes
  already evidenced; four episodes lose unsupported modifiers.

## Claim-affecting statistics

- Direct-support counts move B1 29→32 and B2 17→18. The B2--B7 association phi
  falls to 0.382 (lift 2.037, sensitivity 0.288--0.476). Claim C06, the results
  section, strong-relationships table, generated LaTeX, association figure, and
  golden tests are updated together. The pair stays above the attention threshold.

## Post-0.1.2 sprint artifacts documented

- Correction workflow (`docs/correction-workflow.md`,
  `artifacts/maintainer_correction_checklist.md`).
- Evidence atlas browsable prose (`docs/evidence-atlas.md`, generated summary,
  drift checks).
- Device-interface registry design draft with six validated seed records.
- Adjudication pilot report (`artifacts/adjudication_pilot_v0.1.2.md`).

## 0.2 scaffolding

- Manual-dispatch GitHub Pages workflow (`.github/workflows/pages.yml`) builds
  MkDocs after release validation.
- Registry contribution path in `docs/device-interface-registry.md`, with
  `labauto_observatory.registry` wired into `make validate` and mutation tests in
  `tests/test_registry.py`.
- Run-event schema proposal (`docs/event-schema.md`,
  `schemas/run-event.schema.json`).

## Bibliography cleanup

Three uncited forum `.bib` entries removed; compiled bibliography and `.bib`
entry count both read 36.

## Validation

184 tests pass with 99.15% branch-aware coverage (floor: 90%), up from 128 tests
at v0.1.2. Schema, claim-ledger, claim-traceability, register, registry, blind
subset, atlas summary, and release-metadata checks all pass. `ruff`, `mypy
--strict`, and `mkdocs build --strict` pass.

Measured detail is in [submission_audit_v0.1.3.md](submission_audit_v0.1.3.md).
Recompile the manuscript before external submission; this release touched results
text and generated tables.

## Scope

Repo-only release preparation: no tag, no push, no journal portal submission, no
Zenodo deposit, no DOI, and no GitHub Release PDF assets in this change set.

## Beyond this release

- Human second coder on the blind pack (issue #11).
- First GitHub Pages deploy via the `Docs site` workflow.
- Independent run-event streams from real laboratories before the event schema
  graduates from proposal to dataset.
