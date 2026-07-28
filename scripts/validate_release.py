#!/usr/bin/env python3
"""Validate schemas, records, claims, and release invariants."""

from __future__ import annotations

import csv
from pathlib import Path

from labauto_observatory.io import read_yaml
from labauto_observatory.traceability import check_traceability
from labauto_observatory.validation import validate_file

ROOT = Path(__file__).resolve().parents[1]


def require(path: Path) -> None:
    if not path.exists() or path.stat().st_size == 0:
        raise SystemExit(f"required artifact missing or empty: {path}")


def main() -> None:
    validate_file(
        ROOT / "data/knowledge_index/seed_records.yaml",
        ROOT / "schemas/knowledge-index.schema.json",
    )
    validate_file(
        ROOT / "data/knowledge_index/example_question.yaml",
        ROOT / "schemas/troubleshooting-question.schema.json",
    )

    records = read_yaml(ROOT / "data/knowledge_index/seed_records.yaml")
    record_ids = [record["record_id"] for record in records]
    if len(record_ids) != len(set(record_ids)):
        raise SystemExit("knowledge-index record IDs are not unique")

    with (ROOT / "data/derived/publication_claim_ledger.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        claims = list(csv.DictReader(handle))
    approved = [claim for claim in claims if claim["Status"] == "Approved"]
    if not approved:
        raise SystemExit("claim ledger contains no approved claims")
    if any(not claim["Prohibited overclaim"].strip() for claim in approved):
        raise SystemExit("every approved claim must specify a prohibited overclaim")

    traceability = check_traceability(ROOT)
    if not traceability.ok:
        for problem in traceability.problems:
            print(f"claim traceability failure: {problem}")
        raise SystemExit("approved claims are not traceable to the manuscript sources")

    for relative in [
        "paper/main.tex",
        "paper/supplement.tex",
        "paper/references.bib",
        "data/derived/evidence_register_part_01.csv",
        "data/derived/evidence_register_part_02.csv",
        "data/derived/episode_register_part_01.csv",
        "data/derived/episode_register_part_02.csv",
        "data/derived/reliability_subset.csv",
        "schemas/knowledge-index.schema.json",
        "schemas/troubleshooting-question.schema.json",
    ]:
        require(ROOT / relative)

    print(
        f"validated {len(records)} knowledge records and {len(approved)} approved claims; "
        f"traced {len(traceability.approved)} approved claims to the manuscript"
    )


if __name__ == "__main__":
    main()
