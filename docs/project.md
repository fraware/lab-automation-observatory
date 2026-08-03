# Project governance, ethics, data use, and roadmap

## Governance

The project uses evidence-oriented stewardship.

### Roles

- **Project steward** maintains scope, releases, and claim discipline.
- **Data steward** reviews additions, corrections, provenance, and de-identification.
- **Domain reviewer** checks technical applicability and validation-stage wording.
- **Artifact maintainer** owns one or more community schemas or registries.

### Decision rules

Changes to the taxonomy, published values, schemas, or seed records require a pull request with:

1. the proposed change;
2. supporting public evidence;
3. affected denominators and outputs;
4. an invalid-inference review;
5. updated tests and documentation.

Disputed records remain visible with status `disputed`. Corrections supersede prior records through explicit lineage. Release tags are immutable.

See also [CLAIM_BOUNDARIES.md](https://github.com/fraware/lab-automation-observatory/blob/main/CLAIM_BOUNDARIES.md), [CODE_OF_CONDUCT.md](https://github.com/fraware/lab-automation-observatory/blob/main/CODE_OF_CONDUCT.md), and [SECURITY.md](https://github.com/fraware/lab-automation-observatory/blob/main/SECURITY.md).

## Ethics and public-discourse handling

The study analyzes public technical discussions. The release minimizes redistribution and identity exposure.

- No full forum corpus is redistributed.
- No usernames or profile attributes are included in the public dataset.
- Quotations are short, anonymized, and linked to their public discussion.
- Forum posts are treated as testimony, diagnosis, measurement, product report, or speculation according to context.
- Public non-resolution is not equated with operational non-resolution because work can move to private channels.
- Product-reported results remain labeled as source-reported and are bound to the deepest demonstrated validation stage.
- Vendor reliability, market share, and failure rates are outside the supported inference space.

Corrections or removal requests concerning the derived release should be opened as a repository issue with the affected record identifier.

## Data use

### Included

The repository includes derived codes, bounded metric inputs, anonymized short quotations, source URLs, and seeded knowledge records.

### Excluded

It excludes a verbatim forum dump, user handles, private messages, personal profiles, and inferred demographic attributes.

### Appropriate uses

- reproduce the reported pilot metrics;
- audit construct definitions and claim boundaries;
- extend schemas or add evidence-bearing records;
- design prospective studies and community interventions.

### Inappropriate uses

- ranking vendors or products by reliability;
- estimating market share or installed base;
- training identity or behavioral profiling systems;
- treating public discussion counts as operational incidence rates;
- representing source-reported product results as independent replication.

## Roadmap

### Release 0.1

- Reproducible derived data, schemas, tests, and local validation (manuscript sources stay local-only).
- Ten seed resolved-knowledge records.
- Forum-ready troubleshooting template.

### Release 0.2

- Public correction workflow and evidence-atlas site.
- Device-interface accessibility registry prototype. Schema draft and worked examples: [Device-interface accessibility registry](device-interface-registry.md) ([issue #12](https://github.com/fraware/lab-automation-observatory/issues/12)).
- Structured event-schema proposal. Draft schema and design note: [Run-event schema](event-schema.md) (`schemas/run-event.schema.json`).

### Release 0.3

- Prospective evaluation of question quality and knowledge reuse.
- Observability–recovery incident study.
- Scheduler benchmark instances with scientific constraints.
