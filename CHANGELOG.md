# Changelog

All notable changes follow Keep a Changelog principles.

## [Unreleased]

### Changed

- Consolidated public documentation into a tighter map: claim discipline folded
  into `CLAIM_BOUNDARIES.md`; governance/ethics/data-use/roadmap into
  `docs/project.md`; robustness into `docs/methods.md`; venue requirements into
  `submissions/README.md`. Removed redundant root and docs Markdown files.
  MkDocs navigation and `REUSE.toml` updated.

## [0.1.5] - 2026-07-30

### Added

- Venue-specific manuscripts and packages for SLAS Technology / NexusXp
  (`paper/main_slas_v0.1.5.tex`), Digital Discovery, Patterns Resource,
  anonymized CSCW, and a future JOSS draft, with a venue build matrix under
  `submissions/`.
- Restored public `CLAIM_BOUNDARIES.md` binding every venue manuscript to the
  certified inferential boundaries.
- `artifacts/submission_audit_v0.1.5.md`, `artifacts/release_notes_v0.1.5.md`,
  and `artifacts/submission_bundle_manifest_v0.1.5.yaml`.
- `scripts/build_cscw_anonymous_package.py` for the anonymous CSCW review
  archive.

### Changed

- Release version metadata reads `0.1.5` while preserving the certified
  v0.1.4 empirical data, metrics, robustness outputs, and numerical results.
- `scripts/build_submission_bundle.py` defaults to SLAS v0.1.5 manuscript,
  cover-letter, and highlights paths.
- Release workflow accepts `v0.1.5*` tags and the v0.1.5 bundle manifest.

## [0.1.4] - 2026-07-30

### Added

- `data/derived/source_quote_audit.csv`, a 25-row Gate 1 source/quotation audit ledger covering every manuscript forum/site bibliography key and every quote-bank entry, with surrounding-context and later-update outcomes, resolved quotation corrections, and claim boundaries. About (`/about`) and Terms (`/tos`) are separate identities. Documented in `docs/data-dictionary.md`, enforced by `tests/test_source_quote_audit.py` (including BibTeX key→URL→audit URL parity), `EXPECTED_ROW_COUNTS`, and `scripts/validate_release.py`.
- Robustness-table sync fixture and test so the three `build_robustness_tables` outputs stay byte-matched to `paper/generated/`, plus a B6 denominator mutation test that invalidates `data/robustness/denominator_sensitivity.csv`.
- Fix in `scripts/build_robustness_tables.py` so `denominator_table` passes a single iterable to `"\n".join` (latent arity bug exposed by the new sync fixture).
- `artifacts/submission_audit_v0.1.4.md` and `artifacts/release_notes_v0.1.4.md`.
- `scripts/build_submission_bundle.py` to assemble the canonical SLAS ZIP, nested data/code archive, and `SHA256SUMS.txt`.

### Changed

- Supplement inventory test now expects all five generated table stems (`association_leave_one_out`, `code_counts`, `denominator_sensitivity`, `partial_score_sensitivity`, `quotations`), matching `paper/supplement.tex` after the PR #14 robustness tables.
- Release version metadata reads `0.1.4` in `pyproject.toml`, `uv.lock`, `CITATION.cff`, `codemeta.json`, `.zenodo.json`, and the submission bundle manifest template.
- Submission manifest schema uses `source_content_sha` plus `certification_commit_sha` instead of a single ambiguous `commit_sha`.
- Root `requirements.environment.txt` relocated to `artifacts/requirements.environment.v0.1.0.txt` as a historical snapshot; install authority is `uv sync --frozen --all-extras` / `uv.lock`.
- Manual workflows (`ci`, `paper`, `release`, `pages`) use `uv sync --frozen --all-extras`; release workflow requires a `tag` input and uploads the full submission asset set.
- `README.md` restores a visible Markdown H1 beside the ASCII banner for accessibility and discoverability.
- Independent-coding guidance (issue #11) names only `reliability_subset_blind.csv`; the answer-bearing key must not be opened during coding.

### Fixed

- Broken release test contract where the supplement `\input` assertion lagged the five-table supplement source.
- Combined About/Terms audit row that listed two bib keys against only the About URL.

## [0.1.3] - 2026-07-29

### Added

- `docs/correction-workflow.md`, `artifacts/maintainer_correction_checklist.md`, a structured `evidence-correction` issue form, and a `CONTRIBUTING.md` pointer to them. A repository that publishes coded rows and bounded metrics needs a stated route for disputing either; the workflow names what a reporter must supply, which files a maintainer touches, and the rule that a correction changing a published number lands with its regenerated derived outputs, tables, figures, and golden tests in the same change set.
- `docs/evidence-atlas.md` and the generated `docs/generated/evidence_atlas_summary.md`, built by `labauto_observatory.atlas_summary` and `scripts/build_atlas_summary.py`, with a `make atlas-summary` target, a drift check in `make validate`, and its own tests. `data/derived/evidence_atlas.csv` existed only as a CSV that a reader had to download and open; the atlas is now browsable prose in the documentation site, generated from the same committed source so the two cannot disagree.
- `docs/device-interface-registry.md`, `schemas/device-interface-registry.schema.json`, and `data/registry_examples/device_interface_registry_examples.yaml`, a design draft for a bounded device-interface accessibility registry seeded from the B2 component structure and validated in the schema tests. This is the Roadmap 0.2 surface and is explicitly a draft: it records interface facts a practitioner can verify, and it carries no vendor ranking, reliability score, or market claim.
- `artifacts/adjudication_pilot_v0.1.2.md` and `artifacts/adjudication_pilot_three_threads.csv`, a process validation of the adjudication instrument on three critical threads. It is not a second coding pass and it reports no agreement statistic; its purpose was to find where the published rules underdetermine a coding decision. Its eight findings drive most of the rest of this release.
- `data/derived/reliability_subset_blind.csv`, the coder-facing projection of the hard-case adjudication set, together with `labauto_observatory.blind_subset`, `scripts/build_blind_subset.py`, a drift check in `make validate`, and its own tests. The published key states `Expected primary`, `Plausible alternative`, and `Why disagreement is likely` in the same row as the source URL, so a coder could not reach a thread without reading the answer; that is finding F1 of `artifacts/adjudication_pilot_v0.1.2.md`. The key is unchanged and stays the maintainer-facing instrument.
- A `Primary-code tie-break` rule in `data/derived/codebook.csv`. Two codes could both be primary-eligible with nothing to choose between them; the primary is now the code whose boundary test fails for the request made in the initiating post, satisfying a code's required evidence makes it direct support rather than primary, and the rejected candidate is recorded in `Analytical note`.
- A `Read scope` column on the adjudication key and the blind sheet, naming the pages or posts that constitute the coded material for each of the 14 hard threads. A coder who stops at the landing page of a sixty-five-post thread codes a different thread.
- A `First post anchor` column on the episode registers, filled where the public thread exposes a post anchor, so that two segmentations can be compared post by post rather than only counted. Empty is allowed; a populated cell is checked for post-anchor URL shape.
- An episode-unit definition in `docs/contributing-evidence.md`, and validation that each thread's expected episode count matches the episode register.
- An episode-to-thread coherence check in `make validate`: every episode `Primary technical code` and every entry in `Ecosystem modifiers` must carry a direct-support flag on that episode's thread. Nothing previously tied episode codes back to the thread-level flags, so an episode could assert a condition its own thread recorded as unsupported. That is finding F8 of `artifacts/adjudication_pilot_v0.1.2.md`, which reported `T05-E3` and deliberately left it unfixed until the check existed.
- `artifacts/submission_audit_v0.1.3.md` and `artifacts/release_notes_v0.1.3.md`. The audit records the checks measured at this tip rather than carried forward; the v0.1.2 audit is now frozen as the snapshot for its own tag.

### Changed

- `README.md`, `ROADMAP.md`, `REPRODUCIBILITY.md`, `docs/index.md`, `docs/community-artifacts.md`, and the MkDocs navigation carry the new correction, atlas, and registry surfaces, with the correction workflow listed ahead of the registry draft in both navigations. A reader who finds an error should reach the correction route before the forward-looking design draft.
- The second-coder path in `README.md`, `docs/contributing-evidence.md`, `docs/community-artifacts.md`, `docs/methods.md`, and supplement section S4 now names the blind sheet as the only file a second coder should open.
- B1's `Pilot interpretation` in `data/derived/taxonomy_rules.csv` no longer contradicts its own `Primary-code eligibility`: it is a cross-cutting modifier when it accompanies a technical failure and primary when the thread's object is the artifact, corpus, or governance itself.
- B7 now excludes purchasing lead time, installation schedule, and component supply, and B2 now excludes claims about vendor market structure rather than a specific integration attempt. Procurement and installation lead time is declared outside the taxonomy instead of each coder improvising a home for it.
- Episode `Counterexample` became `Counterexample to`, holding the construct or constructs the episode runs against. The scope previously survived only in free text, so a coder could agree with the boolean while disagreeing about what was contradicted. `T04-E3` is now recorded as a counterexample to B1 alone, since the recommended procedure still ends in contacting named collaborators and remains positive evidence for B10.
- `Episode segmentation required` states an exact episode count instead of "at least three episodes", which no segmentation could contradict.
- Thread 2's `Primary` moved from B4 to B1 under the new tie-break, which is finding F2 of the pilot. Its initiating post asks for a shared labware database rather than reporting a defective representation, and a maintained canonical corpus would satisfy the request, so B1's boundary test is the one that fails; B4 stays as direct support because the thread names real missing physical attributes. Primary counts move B1 1 to 2 and B4 7 to 6, and episode `T02-E2` already carried B1 as its own primary.
- The eight rows flagged by the new coherence check are adjudicated against each code's `Required evidence`. Threads 5, 13, and 33 gain the thread-level flags their episodes had already evidenced (`B1` for thread 5 and thread 33, `B1` and `B2` for thread 13), and four episodes lose a modifier that no recorded evidence supported (`B3` from `T07-E3` and `T21-E1`, `B5` from `T09-E2`, `B2` from `T32-E3`). Every affected row records the reason in its `Analytical note` or `Coding note`.
- Direct-support counts move B1 29 to 32 and B2 17 to 18, which is claim-affecting: the B2--B7 association phi falls to 0.382 with lift 2.037 and a 0.288--0.476 sensitivity width. `paper/sections/04_results.tex`, `data/metrics/strong_relationships.csv`, claim ledger row C06, `paper/generated/*`, `paper/figures/associations.pdf`, and the literals in `tests/test_published_values.py` are updated together. The pair stays above the pilot attention threshold and keeps its enabling-condition reading.
- The release version in `pyproject.toml`, `CITATION.cff`, `codemeta.json`, and `.zenodo.json` reads `0.1.3`, and `uv.lock` records the bumped project version. No DOI or ORCID is asserted, because none has been registered.

### Removed

- The `forum_contamination_tracking`, `forum_labware_database`, and `forum_plr_zheight` entries in `paper/references.bib`, which no manuscript or supplement passage cited. They were retained forum sources that never entered a reference list, so the `.bib` entry count and the compiled bibliography disagreed by three; both now read 36.

## [0.1.2] - 2026-07-29

### Added

- `labauto_observatory.associations` and `scripts/build_associations.py`, which recompute all 28 B2--B9 pairwise associations from the evidence register and join the coder-authored reading of each pair from the new `data/derived/association_annotations.csv`. The table and the register can no longer disagree.
- `labauto_observatory.atlas` and `scripts/build_evidence_atlas.py`, which rebuild `data/derived/evidence_atlas.csv` from committed sources. The atlas was referenced by the data dictionary, the workbook exporter, and claim ledger rows C01 and C11 but had never been committed; it now exists as a derived, drift-checked artifact.
- `labauto_observatory.register_validation`, wired into `make validate`: documented row counts, score-cell domains, categorical vocabularies, derived-score recomputation, and the cross-file invariants (primary implies direct support, adjudication set equals the episode subset, B8 alignment class equals numerator eligibility, funnel Wilson columns match the release code, B7 has a non-empty incomplete-field denominator).
- `data/metrics/b2_b10_matched_cases.csv`, the B2/B10 convergent-validity table the manuscript implied, with every cell checked against its two source files.
- `labauto_observatory.latex` for fail-closed LaTeX escaping, and a generated `paper/generated/quotations.tex` covering all 20 quotations instead of the ten previously hardcoded in the supplement.
- `scripts/figure_style.py`, one module owning print typography, the Okabe--Ito palette, deterministic saving, and the single taxonomy specification now shared by the conceptual-model figure and the graphical abstract.
- Supplement figures for the B8 alignment matrix and for B6 preflight detectability beside its rate, interval, and sensitivity bounds.
- A `make derived` target, and mutation tests that break one release-data invariant at a time and assert the reported problem.
- `artifacts/submission_audit_v0.1.2.md` and `artifacts/release_notes_v0.1.2.md`. This is the first audit with a successful local document build, so its page counts and reference count are measured rather than carried forward; the v0.1.1 audit is frozen.

### Changed

- `compute_release_results` now returns `components` and `denominators` alongside `metrics`, and every bounded proportion carries a descriptive Wilson interval plus its numerator and denominator. Component means carry their known-cell count instead, because a mean of ordinal component scores is not a binomial proportion.
- The headline metrics table gained a 95% Wilson column, and the strong-associations table gained the one-thread overlap sensitivity range.
- Replaced the main-text metric dashboard with a component-level heatmap for B2--B5, the discovery bar chart with a three-stage requirement matrix, and the association bar chart with the full 28-pair phi matrix. The main-text display budget stays at seven, now enforced by a test.
- Rebuilt the validation funnel so that only the stage with a denominator is drawn as a rate; stages reported without a denominator, and stages not reported at all, are drawn as bands across the whole axis so that "reported" cannot be read as a measured success rate.
- Fixed `latex.escape`, which escaped the braces of its own `\textbackslash{}` replacement.
- The drift checks for the two derived CSVs now compare content rather than bytes. Git stores those files with LF and hands Windows working trees CRLF, so the byte comparison would have failed `make validate` on a fresh clone.
- Raised the manuscript float fractions and allowed figures a float page as a last resort. Under the LaTeX defaults the component heatmap was too tall to be a top float, which deferred it and every later figure past the bibliography.
- `scripts/export_workbook.py` no longer exports the pairwise table or the evidence atlas, since both are now generated from committed data.

## [0.1.1] - 2026-07-28

### Added

- `uv.lock` pinning the full transitive dependency set, and a `docs` extra with MkDocs plus `make docs` and `make docs-build`.
- Machine-checked claim traceability: `labauto_observatory.traceability`, `scripts/check_claim_traceability.py`, and a `make claims` target. Every approved claim now needs a `% claim: Cnn` marker in the LaTeX source and a `Manuscript anchor` substring in the ledger.
- Golden tests for the secondary headline fields and the stable key set of `build/results.json`, content tests for the generated LaTeX tables, and smoke and determinism tests for the figure scripts.
- Supplementary section, methods pointer, and documentation for the hard-case adjudication set `data/derived/reliability_subset.csv`.
- Per-column definitions for every committed CSV in `docs/data-dictionary.md`, and a coding and evidence contribution guide at `docs/contributing-evidence.md`.
- Windows and PowerShell instructions in `REPRODUCIBILITY.md`, and a `make paper-only` target that builds the manuscript from committed figures without Python.
- `artifacts/submission_audit_v0.1.1.md` and `artifacts/release_notes_v0.1.1.md`, refreshing the audit record against the current test suite and claim ledger.
- `make links` for a local lychee link-check matching the CI scope, and a `docs-build` step in `make ci`.

### Changed

- Ran `ruff format` across the repository and aligned the pre-commit `ruff-pre-commit` hook with Ruff 0.16.0 from `uv.lock`.
- Retargeted the submission package to the SLAS Technology special issue `NexusXp: The Connected Lab`, with regular-journal transfer preference.
- Added complete submission metadata, journal-compliance checklist, and Editorial Manager copy-paste metadata.
- Added author degree to the manuscript and complete correspondence metadata to the submission package.
- Condensed the cover letter to one page and aligned it with the connected-laboratory scope.
- Committed the vector figures and the graphical abstract; the figure scripts now suppress output timestamps so regeneration on the locked environment is byte-identical. Only the raster previews `paper/figures/*.png` remain untracked.
- Drove the discovery--resolution and validation-funnel figures and the workflow figure counts from `compute_release_results` and `data/metrics/ai_validation_funnel.csv` instead of hardcoded arrays.
- Reused the shared `mean_score` and `weighted_completeness` helpers in `analysis.py` so unknown scores stay distinguishable from zero.
- Extended `build/results.json` with `episode_threads`, `adjudication_threads`, and `constructs` counts.
- Removed the unused `scipy` pin from `requirements.environment.txt` and documented that `uv.lock` is the authoritative install path.
- Aligned the coverage figure quoted in `README.md` with `artifacts/submission_audit_v0.1.0.md`, then repointed it at `artifacts/submission_audit_v0.1.1.md`.
- Bumped the pre-commit `pre-commit-hooks` revision past its deprecated `v4.6.0` pin.
- Extended the `.gitignore` figure-policy comment to note that `paper/graphical_abstract.png` is tracked alongside the PDF.

## [0.1.0] - 2026-07-28

### Added

- Venue-ready SLAS Technology LaTeX manuscript, supplement, highlights, cover letter, and graphical-abstract generator.
- Public derived datasets without user handles or a verbatim forum corpus.
- Executable metric, schema-validation, figure, and table reproduction code.
- Regression tests for all published headline values and JSON Schema tests for community artifacts.
- Minimum reproducible troubleshooting-question and resolved-knowledge-index schemas.
- Dual licensing, citation metadata, governance, ethics, data-use, security, and contribution policies.
- Manual-only workflow templates; authoritative validation is performed locally to avoid hosted-runner costs.
