---
title: 'Lab Automation Observatory: Reproducible Evidence Infrastructure for Public Laboratory-Automation Knowledge'
tags:
  - Python
  - laboratory automation
  - reproducible research
  - qualitative data
  - research software
authors:
  - name: Matéo H. Petel
    orcid: ADD-ORCID-BEFORE-SUBMISSION
    affiliation: 1
affiliations:
  - name: Center for Strategic Research in Critical Technologies; SentinelOps
    index: 1
bibliography: ../../references.bib
---

# Summary

Lab Automation Observatory is an open-source Python package and versioned research-data system for transforming public laboratory-automation discussions into auditable analytical records, bounded metrics, reproducible figures and tables, and governed community artifacts. It addresses a recurring research-engineering problem: technical evidence about instrument interfaces, deployment state, physical resources, execution observability, recovery, scheduling, validation, and AI-assisted methods is distributed across public discussions and local artifacts, and the resulting claims can drift across data, analysis code, and manuscripts.

The software provides typed loaders, metric implementations, JSON Schema validation, release-level analysis, command-line reproduction, deterministic figure and table generation, source and claim traceability checks, and submission-bundle construction. The associated data model preserves source provenance, unit, denominator, uncertainty, validation stage, known limitations, and prohibited inference. The package does not collect or scrape forum content. Reproduction uses committed derived records and does not require network access.

# Statement of need

Laboratory-automation research combines software and physical systems. A nominally available driver can remain inaccessible due to licensing, missing documentation, or absent test surfaces. A version-controlled method can remain insufficiently identified when libraries, resource definitions, calibration, firmware, or runtime state are unbound. A log can identify a software exception without reconstructing material state after partial execution. A simulation result can be reported beyond the evidence stage it actually reached.

These cases require analytical software that retains field-level evidence and claim boundaries instead of reducing each discussion to a topic count. Existing laboratory-integration frameworks such as SiLA and PyLabRobot address device and programming interoperability [@bar2012sila; @wierenga2023pylabrobot]. Lab Automation Observatory complements those systems by supporting evidence analysis, knowledge stewardship, and reproducible publication around operational practice.

The package is intended for researchers studying laboratory automation, technical communities, cyber-physical operations, and reproducibility; maintainers building community knowledge bases; and laboratory teams evaluating question, interface, resource, or event schemas. It is not a vendor-comparison or incident-rate tool.

# Functionality

The package contains five connected layers.

1. **Data access and validation.** Typed input helpers read committed CSV, JSON, and YAML records. JSON Schema validation covers troubleshooting questions, resolved-knowledge records, device-interface records, and run-event streams. Cross-file checks enforce unique identifiers, expected row counts, allowed categories, source domains, episode-to-thread coherence, and blind-coding separation.

2. **Metrics and robustness.** The library implements bounded component means, Wilson intervals, phi coefficients, lift, conditional probabilities, context-expansion ratios, and release-level summaries. Robustness scripts recompute alternative partial-score weights, leave-one-thread-out association influence, and alternative denominators.

3. **Publication traceability.** Source-audit records bind bibliography keys and quotations to canonical URLs and approved wording. A claim ledger binds manuscript statements to data or source anchors, denominators, safe wording, limitations, and prohibited overclaims. Tests fail when generated values, tables, figures, or claim markers drift.

4. **Reproducible artifacts.** Commands regenerate results, vector figures, LaTeX tables, graphical abstracts, documentation, and versioned submission bundles. Manifests and SHA-256 hashes bind scientific source content, certification metadata, and compiled outputs.

5. **Community infrastructure.** Machine-readable schemas and seed records support reproducible troubleshooting questions, maintained resolved knowledge, interface-accessibility records, and linked run-event streams.

A typical reproduction uses:

```bash
uv sync --frozen --all-extras
make derived
make validate
make test
make docs-build
```

Paper and supplement builds require a TeX distribution. The package is tested through published-value assertions, schema tests, source-mapping tests, generated-output comparisons, and fail-closed mutation tests.

# Research use

The initial release supports a mixed-methods pilot covering 55 purposively selected public discussions and 45 analytical episodes. Every reported value is recomputed from committed field-level inputs. The release demonstrates how public technical evidence can support bounded construct development and prospective study design without being interpreted as field prevalence, product reliability, or causal effect.

Future research use includes independent recoding of the released blind hard-case set, application of the evidence model to other specialist technical communities, prospective evaluation of troubleshooting and knowledge-record interventions, device-interface accessibility studies, and incident research using the run-event schema. The package's contribution to research software will be established through such independent use and citation.

# Quality control and sustainability

The project uses semantic versioning, dual code/data licensing, structured governance, explicit record lifecycle states, correction lineage, deterministic generated outputs, and release audits. Claim-affecting changes require synchronized updates across evidence, metrics, manuscript markers, tests, and release metadata. The roadmap includes stable APIs, broader examples, external contributors, and documented migration paths for schemas.

# Acknowledgements

The author thanks the public laboratory-automation community whose discussions motivated the resource and the maintainers of the open-source scientific Python and laboratory-automation ecosystems.

# References
