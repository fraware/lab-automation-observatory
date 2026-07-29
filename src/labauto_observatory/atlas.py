"""Rebuild the per-construct evidence atlas from committed release data.

The atlas was originally a sheet in the retained workbook and was never
committed, so ``docs/data-dictionary.md``, ``scripts/export_workbook.py``, and
claim ledger rows C01/C11 pointed at a file that did not exist. The workbook is
not available in the reproduction environment, so the atlas is rebuilt here
instead of restored: every cell is either copied from a committed source column
or computed by :func:`labauto_observatory.analysis.compute_release_results`. No
cell is authored in this module -- the only strings defined here are column
labels and unit names.
"""

from __future__ import annotations

import csv
import io
import re
from pathlib import Path
from typing import Any

from .analysis import compute_release_results
from .io import integer, normalised_newlines, read_csv, read_csv_many, read_text_lf

ATLAS_RELATIVE = "data/derived/evidence_atlas.csv"
TAXONOMY_RELATIVE = "data/derived/taxonomy_rules.csv"
QUOTES_RELATIVE = "data/derived/quote_bank.csv"
NEGATIVE_CASES_RELATIVE = "data/derived/negative_cases.csv"

KEY_SOURCE_COUNT = 3
_CODE = re.compile(r"B(?:10|[1-9])")

HEADER: tuple[str, ...] = (
    "Code",
    "Bottleneck",
    "Analytical layer",
    "Direct-support threads",
    "Primary-code threads",
    "Pilot interpretation",
    "Bounded quantitative result",
    "Strongest descriptive relationship",
    "Short anonymized quotation",
    "Quotation source",
    "Retained counterexample",
    "Key sources",
    "Evidence maturity",
)

# How each construct's headline number is bounded. Wilson intervals are only
# meaningful for the proportions, so the maturity label distinguishes them from
# component means and from the requirements-elicitation ratio.
EVIDENCE_MATURITY: dict[str, str] = {
    "B1": "Qualitative and count evidence only; no bounded metric",
    "B2": "Component mean over known cells in selected cases",
    "B3": "Component mean over applicable cells in selected cases",
    "B4": "Component mean plus ordinal evidence grade in selected cases",
    "B5": "Component mean over known cells in selected cases",
    "B6": "Bounded proportion with Wilson interval and sensitivity bounds",
    "B7": "Bounded proportions with Wilson intervals over one toy scenario",
    "B8": "Bounded proportion with Wilson interval in selected cases",
    "B9": "Requirements-elicitation ratio over one discussion",
    "B10": "Bounded proportion with Wilson interval in selected cases",
}
NO_PAIRWISE = "Not part of the B2--B9 pairwise set"


def _quantitative_result(code: str, results: dict[str, Any]) -> str:
    """Render the construct's headline result together with its denominator."""

    metrics = results["metrics"]
    denominators = results["denominators"]

    def mean(key: str, name: str, unit: str) -> str:
        cases = denominators[key]["cases"]
        return f"Mean {name} {100 * metrics[key]:.1f}% over {cases} {unit}"

    def proportion(key: str, name: str, unit: str) -> str:
        counts = denominators[key]
        low, high = metrics[f"{key}_wilson"]
        return (
            f"{name} {100 * metrics[key]:.1f}% "
            f"({counts['successes']}/{counts['trials']} {unit}; "
            f"Wilson {100 * low:.1f}%--{100 * high:.1f}%)"
        )

    if code == "B1":
        threads = results["corpus"]["direct_support_counts"]["B1"]
        total = results["corpus"]["threads"]
        return (
            f"Not separately quantified; cross-cutting modifier with direct support in "
            f"{threads} of {total} selected threads"
        )
    if code == "B2":
        return mean(
            "integration_accessibility_mean",
            "Integration Accessibility Score",
            "device--interface cases",
        )
    if code == "B3":
        return mean(
            "reproducibility_manifest_mean",
            "Reproducibility Manifest Completeness",
            "deployment objects",
        )
    if code == "B4":
        grade = metrics["physical_definition_median_evidence_grade"]
        return (
            mean(
                "physical_definition_mean",
                "Physical Definition Completeness",
                "resource definitions",
            )
            + f"; median evidence grade {grade}"
        )
    if code == "B5":
        return mean("observability_mean", "Observability Coverage", "execution or diagnostic cases")
    if code == "B6":
        low, high = metrics["preflight_preventability_sensitivity"]
        return (
            proportion(
                "preflight_preventability_complete_case",
                "Complete-case Preflight Preventability Rate",
                "definite scenarios",
            )
            + f"; sensitivity {100 * low:.1f}%--{100 * high:.1f}%"
        )
    if code == "B7":
        return (
            proportion(
                "scheduling_constraint_discovery", "Constraint discovery", "incomplete fields"
            )
            + "; "
            + proportion(
                "scheduling_scenario_resolution", "scenario resolution", "incomplete fields"
            )
        )
    if code == "B8":
        return proportion("test_claim_aligned", "Fully aligned claims", "bounded claims")
    if code == "B9":
        counts = denominators["context_expansion_core"]
        return (
            f"Core Context Expansion Ratio {metrics['context_expansion_core']:.1f}x "
            f"({counts['added_classes']} reply-added over {counts['initial_classes']} opening classes)"
        )
    return proportion(
        "documentation_actionable_public_resolution",
        "Actionable public resolution",
        "documentation cases",
    )


def _strongest_relationship(code: str, pairwise: list[dict[str, str]], threads: int) -> str:
    """The code's largest positive phi among the committed pairwise table."""

    involving = [row for row in pairwise if code in (row["Code A"], row["Code B"])]
    if not involving:
        return NO_PAIRWISE
    best = max(involving, key=lambda row: float(row["Phi"]))
    overlap = integer(best["Overlap"])
    return (
        f"{best['Code A']}--{best['Code B']} (phi {float(best['Phi']):.3f}, "
        f"lift {float(best['Lift']):.3f}, overlap {overlap}/{threads}; "
        f"{best['Relationship class'].lower()})"
    )


def _key_sources(code: str, evidence: list[dict[str, str]]) -> str:
    """The best-evidenced threads that directly support the construct."""

    supporting = [row for row in evidence if int(row[code]) == 1]
    ranked = sorted(
        supporting,
        key=lambda row: (-(integer(row["Evidence strength"]) or 0), integer(row["ID"]) or 0),
    )
    return "; ".join(row["Thread"] for row in ranked[:KEY_SOURCE_COUNT])


def _counterexamples(code: str, negative_cases: list[dict[str, str]]) -> str:
    matches = [
        row["Case"]
        for row in negative_cases
        if code in _CODE.findall(row["Expected bottleneck challenged"])
    ]
    return "; ".join(matches)


def build_records(root: str | Path) -> list[dict[str, str]]:
    """Build one atlas row per construct, ordered B1 through B10."""

    root_path = Path(root)
    results = compute_release_results(root_path)
    taxonomy = read_csv(root_path / TAXONOMY_RELATIVE)
    quotes = read_csv(root_path / QUOTES_RELATIVE)
    negative_cases = read_csv(root_path / NEGATIVE_CASES_RELATIVE)
    pairwise = read_csv(root_path / "data/metrics/pairwise_associations.csv")
    evidence = read_csv_many(
        sorted((root_path / "data/derived").glob("evidence_register_part_*.csv"))
    )
    corpus = results["corpus"]

    records: list[dict[str, str]] = []
    for rule in taxonomy:
        code = rule["Code"]
        quotation = next((row for row in quotes if row["Code"] == code), None)
        records.append(
            {
                "Code": code,
                "Bottleneck": rule["Construct"],
                "Analytical layer": rule["Layer"],
                "Direct-support threads": str(corpus["direct_support_counts"][code]),
                "Primary-code threads": str(corpus["primary_counts"].get(code, 0)),
                "Pilot interpretation": rule["Pilot interpretation"],
                "Bounded quantitative result": _quantitative_result(code, results),
                "Strongest descriptive relationship": _strongest_relationship(
                    code, pairwise, corpus["threads"]
                ),
                "Short anonymized quotation": (
                    quotation["Short anonymized quotation"] if quotation else ""
                ),
                "Quotation source": quotation["Thread"] if quotation else "",
                "Retained counterexample": _counterexamples(code, negative_cases),
                "Key sources": _key_sources(code, evidence),
                "Evidence maturity": EVIDENCE_MATURITY[code],
            }
        )
    return records


def render_atlas_csv(root: str | Path) -> str:
    """Render the evidence atlas CSV exactly as it is committed."""

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(HEADER), lineterminator="\n")
    writer.writeheader()
    writer.writerows(build_records(root))
    return buffer.getvalue()


def write_atlas_csv(root: str | Path) -> Path:
    """Write the regenerated evidence atlas and return its path."""

    destination = Path(root) / ATLAS_RELATIVE
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_atlas_csv(root), encoding="utf-8", newline="")
    return destination


def atlas_drift(root: str | Path) -> list[str]:
    """Report whether the committed atlas still matches its sources."""

    destination = Path(root) / ATLAS_RELATIVE
    if not destination.is_file():
        return [f"{ATLAS_RELATIVE} is missing; run `make derived`"]
    if read_text_lf(destination) != normalised_newlines(render_atlas_csv(root)):
        return [f"{ATLAS_RELATIVE} has drifted from its sources; run `make derived`"]
    return []
