#!/usr/bin/env python3
"""Export publication datasets from the retained Observatory workbook.

The workbook is a retained research artifact.  Downstream analyses consume the
CSV/YAML files committed under ``data/`` and do not require this exporter.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import yaml

try:
    from artifact_tool import Blob, SpreadsheetFile
except ImportError as exc:  # pragma: no cover - environment-specific provenance tool
    raise SystemExit(
        "artifact_tool is required only to re-export the retained XLSX artifact. "
        "Use the committed CSV files for ordinary reproduction."
    ) from exc


EXPORTS: dict[str, tuple[int, int, str]] = {
    # sheet: (zero-based header row, inclusive zero-based final data row, output)
    "Evidence_Register": (0, 55, "data/derived/evidence_register.csv"),
    "Quote_Bank": (0, 20, "data/derived/quote_bank.csv"),
    "Codebook": (0, 12, "data/derived/codebook.csv"),
    "Taxonomy_Rules": (2, 12, "data/derived/taxonomy_rules.csv"),
    "Reliability_Subset": (2, 16, "data/derived/reliability_subset.csv"),
    "Episode_Register": (2, 47, "data/derived/episode_register.csv"),
    "Negative_Cases": (2, 12, "data/derived/negative_cases.csv"),
    "B2_Integration_Access": (2, 8, "data/metrics/b2_integration_access.csv"),
    "B3_Reproducibility_Manifest": (2, 5, "data/metrics/b3_reproducibility_manifest.csv"),
    "B4_Physical_Definitions": (2, 6, "data/metrics/b4_physical_definitions.csv"),
    "B5_Observability": (2, 6, "data/metrics/b5_observability.csv"),
    "B6_Preflight_PPR": (2, 6, "data/metrics/b6_preflight_preventability.csv"),
    "B7_Constraint_Completeness": (2, 15, "data/metrics/b7_constraint_completeness.csv"),
    "B8_Test_Claim_Alignment": (2, 8, "data/metrics/b8_test_claim_alignment.csv"),
    "B9_Context_Expansion": (2, 24, "data/metrics/b9_context_expansion.csv"),
    "B10_Documentation_Profile": (2, 14, "data/metrics/b10_documentation_profile.csv"),
    "AI_Validation_Funnel": (2, 9, "data/metrics/ai_validation_funnel.csv"),
    "Pairwise_Associations": (2, 30, "data/metrics/pairwise_associations.csv"),
    "Strong_Relationships": (2, 7, "data/metrics/strong_relationships.csv"),
    "Hypothesis_Map": (2, 10, "data/derived/hypothesis_map.csv"),
    "Evidence_Atlas": (2, 12, "data/derived/evidence_atlas.csv"),
    "Troubleshooting_Template": (2, 27, "data/derived/troubleshooting_template.csv"),
    "Knowledge_Index_Schema": (2, 20, "data/knowledge_index/schema_fields.csv"),
    "Seed_Knowledge_Records": (2, 12, "data/knowledge_index/seed_records.csv"),
    "Publication_Claim_Ledger": (2, 14, "data/derived/publication_claim_ledger.csv"),
}


def _normalise(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def export_sheet(
    workbook: Any, sheet_name: str, header_row: int, last_row: int, destination: Path
) -> None:
    sheet = workbook.worksheets.get_item(sheet_name)
    values = sheet.get_range(sheet.get_used_range().address).values
    header = [_normalise(v) for v in values[header_row]]
    if not header or not any(str(v).strip() for v in header):
        raise ValueError(f"{sheet_name}: empty header row {header_row + 1}")
    rows = values[header_row + 1 : last_row + 1]
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        for row in rows:
            clean = [_normalise(v) for v in row[: len(header)]]
            if any(str(v).strip() for v in clean):
                writer.writerow(clean)


def seed_records_to_yaml(csv_path: Path, yaml_path: Path) -> None:
    records: list[dict[str, Any]] = []
    with csv_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            records.append(
                {
                    "record_id": row["Record ID"],
                    "problem": row["Problem"],
                    "bottleneck_codes": [row["Primary code"]],
                    "systems_context": row["Systems / context"],
                    "root_cause_status": row["Root-cause status"],
                    "resolution": row["Resolution / reusable lesson"],
                    "validation_stage": row["Validation stage"],
                    "evidence_grade": int(row["Evidence grade"]),
                    "public_artifact": row["Public artifact"],
                    "known_limitations": [row["Known limitation"]],
                    "maintainer": row["Maintainer / owner"],
                    "last_verified": row["Last verified"],
                    "forum_provenance": row["Forum provenance"],
                    "status": row["Status"].lower().replace(" ", "_"),
                }
            )
    yaml_path.parent.mkdir(parents=True, exist_ok=True)
    yaml_path.write_text(
        yaml.safe_dump(records, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    (yaml_path.with_suffix(".json")).write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    workbook = SpreadsheetFile.import_xlsx(Blob.load(str(args.workbook)))
    for name, (header_row, last_row, relative_path) in EXPORTS.items():
        export_sheet(workbook, name, header_row, last_row, args.root / relative_path)

    seed_records_to_yaml(
        args.root / "data/knowledge_index/seed_records.csv",
        args.root / "data/knowledge_index/seed_records.yaml",
    )


if __name__ == "__main__":
    main()
