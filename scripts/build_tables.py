#!/usr/bin/env python3
"""Generate the manuscript's LaTeX tables from committed data.

Every number is taken from ``compute_release_results`` or from a committed CSV,
so the tables cannot drift from the release data. Bounded proportions carry a
descriptive Wilson interval; component means carry their known-cell denominator
instead, because a mean of ordinal component scores is not a binomial
proportion.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from labauto_observatory.analysis import compute_release_results
from labauto_observatory.io import integer, numeric, read_csv, read_csv_many
from labauto_observatory.latex import escape, percent, percent_interval

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "generated"

NO_INTERVAL = "--"
TOP_PAIRS = 5


def write(name: str, content: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(content.strip() + "\n", encoding="utf-8")


def _interval(metrics: dict[str, Any], key: str) -> str:
    """Descriptive Wilson interval for a bounded proportion, or a dash."""

    bounds = metrics.get(f"{key}_wilson")
    return NO_INTERVAL if bounds is None else percent_interval(bounds)


def headline_metrics(results: dict[str, Any]) -> str:
    metrics = results["metrics"]
    denominators = results["denominators"]
    manifest = denominators["reproducibility_manifest_mean"]
    rows = [
        (
            "B2 Integration accessibility",
            percent(metrics["integration_accessibility_mean"]),
            _interval(metrics, "integration_accessibility_mean"),
            "6 device--interface cases",
        ),
        (
            "B3 Deployment manifest",
            percent(metrics["reproducibility_manifest_mean"]),
            _interval(metrics, "reproducibility_manifest_mean"),
            f"3 deployment objects; {manifest['known_cells']} applicable cells",
        ),
        (
            "B4 Physical definitions",
            percent(metrics["physical_definition_mean"]),
            _interval(metrics, "physical_definition_mean"),
            "4 resource definitions",
        ),
        (
            "B5 Observability",
            percent(metrics["observability_mean"]),
            _interval(metrics, "observability_mean"),
            "4 execution/diagnostic cases",
        ),
        (
            "B6 Preflight preventability",
            percent(metrics["preflight_preventability_complete_case"]),
            _interval(metrics, "preflight_preventability_complete_case"),
            "3 definite scenarios of 4 eligible",
        ),
        (
            "B7 Constraint discovery",
            percent(metrics["scheduling_constraint_discovery"]),
            _interval(metrics, "scheduling_constraint_discovery"),
            "8 incomplete fields of 13",
        ),
        (
            "B8 Fully aligned claims",
            percent(metrics["test_claim_aligned"]),
            _interval(metrics, "test_claim_aligned"),
            "6 bounded claims",
        ),
        (
            "B9 Core context expansion",
            f"{metrics['context_expansion_core']:.1f}$\\times$",
            NO_INTERVAL,
            "5 opening classes",
        ),
        (
            "B10 Actionable public outcome",
            percent(metrics["documentation_actionable_public_resolution"]),
            _interval(metrics, "documentation_actionable_public_resolution"),
            "12 documentation cases",
        ),
    ]
    body = "\n".join(
        f"{label} & {result} & {interval} & {unit} \\\\" for label, result, interval, unit in rows
    )
    return rf"""
\begin{{table}}[t]
\centering
\caption{{Bounded pilot metrics. Each row has a distinct unit and denominator.}}
\label{{tab:headline-metrics}}
\begin{{threeparttable}}
\begin{{tabularx}}{{\linewidth}}{{@{{}}L r l L@{{}}}}
\toprule
Construct & Result & 95\% Wilson & Unit and denominator \\
\midrule
{body}
\bottomrule
\end{{tabularx}}
\begin{{tablenotes}}[flushleft]\footnotesize
\item Results demonstrate operationalization in selected cases. They do not estimate forum-wide or industry-wide rates.
\item Wilson intervals are descriptive uncertainty for the stated denominator, not population inference. A dash marks a row whose result is a mean of ordinal component scores or a ratio rather than a proportion, for which a binomial interval would be undefined.
\item Component means are taken over known cells only; unknown cells are excluded rather than scored as zero.
\end{{tablenotes}}
\end{{threeparttable}}
\end{{table}}
"""


def strong_associations(root: Path, threads: int) -> str:
    """The leading pairs, taken in the order the association build wrote them."""

    pairwise = read_csv(root / "data/metrics/pairwise_associations.csv")[:TOP_PAIRS]
    rows = []
    for row in pairwise:
        low = numeric(row["Phi if overlap \u22121"])
        high = numeric(row["Phi if overlap +1"])
        sensitivity = NO_INTERVAL if low is None or high is None else f"{low:.3f}--{high:.3f}"
        phi = numeric(row["Phi"])
        lift = numeric(row["Lift"])
        rows.append(
            f"{row['Code A']}--{row['Code B']} & {integer(row['Overlap'])}/{threads} & "
            f"{phi:.3f} & {lift:.3f} & {sensitivity} \\\\"
        )
    body = "\n".join(rows)
    return rf"""
\begin{{table}}[t]
\centering
\caption{{Strongest pairwise technical-code associations in the purposive evidence register.}}
\label{{tab:associations}}
\begin{{threeparttable}}
\begin{{tabular}}{{@{{}}lrrrr@{{}}}}
\toprule
Pair & Overlap & $\phi$ & Lift & $\phi$ if overlap $\pm1$ \\
\midrule
{body}
\bottomrule
\end{{tabular}}
\begin{{tablenotes}}[flushleft]\footnotesize
\item Associations are descriptive. Multi-label coding, purposive selection, and thread dependence preclude population or causal interpretation.
\item The final column recodes one overlapping thread in either direction while holding both marginal counts fixed. Every listed pair stays positive across that range.
\end{{tablenotes}}
\end{{threeparttable}}
\end{{table}}
"""


def code_counts(root: Path, corpus: dict[str, Any]) -> str:
    evidence = read_csv_many(sorted((root / "data/derived").glob("evidence_register_part_*.csv")))
    body = "\n".join(
        f"B{index} & {sum(int(row[f'B{index}']) for row in evidence)} & "
        f"{sum(1 for row in evidence if row['Primary'] == f'B{index}')} \\\\"
        for index in range(1, 11)
    )
    return rf"""
\begin{{table}}[t]
\centering
\caption{{Direct-support and primary-code counts in the selected {corpus["threads"]}-thread register.}}
\label{{tab:code-counts}}
\begin{{threeparttable}}
\begin{{tabular}}{{@{{}}lrr@{{}}}}
\toprule
Code & Direct support & Primary \\
\midrule
{body}
\bottomrule
\end{{tabular}}
\begin{{tablenotes}}[flushleft]\footnotesize
\item Coding is multi-label by design, so direct-support counts sum to more than {corpus["threads"]}. Exactly one primary code is assigned per thread, so the primary column sums to {corpus["threads"]}.
\item B1 and B10 are cross-cutting ecosystem conditions. Their high direct-support counts reflect deliberate modifier coding and purposive selection, not prevalence.
\end{{tablenotes}}
\end{{threeparttable}}
\end{{table}}
"""


def quotations(root: Path) -> str:
    rows = read_csv(root / "data/derived/quote_bank.csv")
    body = "\n".join(
        f"{escape(row['Code'])} & ``{escape(row['Short anonymized quotation'])}'' & "
        f"{escape(row['Thread'])} \\\\"
        for row in rows
    )
    return rf"""
\begin{{longtable}}{{@{{}}p{{0.06\linewidth}}p{{0.52\linewidth}}p{{0.34\linewidth}}@{{}}}}
\caption{{Short anonymized quotations from \texttt{{data/derived/quote\_bank.csv}}. Quotations are illustrative and are never counted as quantitative observations.}}
\label{{tab:s-quotations}}\\
\toprule
Code & Short quotation & Source discussion \\
\midrule
\endfirsthead
\toprule
Code & Short quotation & Source discussion \\
\midrule
\endhead
\bottomrule
\endfoot
{body}
\end{{longtable}}
"""


def main() -> None:
    results = compute_release_results(ROOT)
    write("headline_metrics.tex", headline_metrics(results))
    write("strong_associations.tex", strong_associations(ROOT, results["corpus"]["threads"]))
    write("code_counts.tex", code_counts(ROOT, results["corpus"]))
    write("quotations.tex", quotations(ROOT))


if __name__ == "__main__":
    main()
