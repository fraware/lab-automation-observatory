#!/usr/bin/env python3
"""Recompute all headline results from committed release data."""

from __future__ import annotations

import json
from pathlib import Path

from labauto_observatory.analysis import compute_release_results

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"


def main() -> None:
    BUILD.mkdir(exist_ok=True)
    results = compute_release_results(ROOT)
    (BUILD / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    metrics = results["metrics"]
    pair = results["strongest_association"]
    lines = [
        "# Reproduced headline results",
        "",
        f"- Threads: {results['corpus']['threads']}",
        f"- Episodes: {results['corpus']['episodes']}",
        f"- Mean IAS: {metrics['integration_accessibility_mean']:.4f}",
        f"- Mean RMC: {metrics['reproducibility_manifest_mean']:.4f}",
        f"- Mean PDC: {metrics['physical_definition_mean']:.4f}",
        f"- Mean OC: {metrics['observability_mean']:.4f}",
        f"- Complete-case PPR: {metrics['preflight_preventability_complete_case']:.4f}",
        f"- Scheduling discovery: {metrics['scheduling_constraint_discovery']:.4f}",
        f"- Fully aligned claims: {metrics['test_claim_aligned']:.4f}",
        f"- Core CER: {metrics['context_expansion_core']:.4f}",
        f"- Strongest pair: {'–'.join(pair['pair'])}, phi={pair['phi']:.4f}, lift={pair['lift']:.4f}",
        "",
    ]
    (BUILD / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
