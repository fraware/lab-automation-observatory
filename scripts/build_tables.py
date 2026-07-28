#!/usr/bin/env python3
"""Generate compact LaTeX tables from committed data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from labauto_observatory.analysis import compute_release_results
from labauto_observatory.io import read_csv_many

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "generated"


def pct(value: float) -> str:
    return f"{100 * value:.1f}\\%"


def write(name: str, content: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(content.strip() + "\n", encoding="utf-8")


def main() -> None:
    results = compute_release_results(ROOT)
    m = results["metrics"]
    metric_rows = [
        ("B2 Integration accessibility", pct(m["integration_accessibility_mean"]), "6 device--interface cases"),
        ("B3 Deployment manifest", pct(m["reproducibility_manifest_mean"]), "3 deployment objects"),
        ("B4 Physical definitions", pct(m["physical_definition_mean"]), "4 resource definitions"),
        ("B5 Observability", pct(m["observability_mean"]), "4 execution/diagnostic cases"),
        ("B6 Preflight preventability", pct(m["preflight_preventability_complete_case"]), "3 definite scenarios"),
        ("B7 Constraint discovery", pct(m["scheduling_constraint_discovery"]), "8 incomplete fields"),
        ("B8 Fully aligned claims", pct(m["test_claim_aligned"]), "6 bounded claims"),
        ("B9 Core context expansion", f"{m['context_expansion_core']:.1f}$\\times$", "5 opening classes"),
        ("B10 Actionable public outcome", pct(m["documentation_actionable_public_resolution"]), "12 documentation cases"),
    ]
    body = "\n".join(f"{label} & {result} & {unit} \\\\" for label, result, unit in metric_rows)
    write(
        "headline_metrics.tex",
        rf"""
\begin{{table}}[t]
\centering
\caption{{Bounded pilot metrics. Each row has a distinct unit and denominator.}}
\label{{tab:headline-metrics}}
\begin{{threeparttable}}
\begin{{tabularx}}{{\linewidth}}{{@{{}}L R L@{{}}}}
\toprule
Construct & Result & Unit \\
\midrule
{body}
\bottomrule
\end{{tabularx}}
\begin{{tablenotes}}[flushleft]\footnotesize
\item Results demonstrate operationalization in selected cases. They do not estimate forum-wide or industry-wide rates.
\end{{tablenotes}}
\end{{threeparttable}}
\end{{table}}
""",
    )

    pairwise = pd.read_csv(ROOT / "data/metrics/pairwise_associations.csv").head(5)
    rows = "\n".join(
        f"{row['Code A']}--{row['Code B']} & {int(row['Overlap'])}/55 & {row['Phi']:.3f} & {row['Lift']:.3f} \\\\"
        for _, row in pairwise.iterrows()
    )
    write(
        "strong_associations.tex",
        rf"""
\begin{{table}}[t]
\centering
\caption{{Strongest pairwise technical-code associations in the purposive evidence register.}}
\label{{tab:associations}}
\begin{{threeparttable}}
\begin{{tabular}}{{@{{}}lrrr@{{}}}}
\toprule
Pair & Overlap & $\phi$ & Lift \\
\midrule
{rows}
\bottomrule
\end{{tabular}}
\begin{{tablenotes}}[flushleft]\footnotesize
\item Associations are descriptive. Multi-label coding, purposive selection, and thread dependence preclude population or causal interpretation.
\end{{tablenotes}}
\end{{threeparttable}}
\end{{table}}
""",
    )

    evidence = pd.DataFrame(read_csv_many(sorted((ROOT / "data/derived").glob("evidence_register_part_*.csv"))))
    for column in [f"B{i}" for i in range(1, 11)]:
        evidence[column] = evidence[column].astype(int)
    support_rows = "\n".join(
        f"B{i} & {int(evidence[f'B{i}'].sum())} & {int((evidence['Primary'] == f'B{i}').sum())} \\\\"
        for i in range(1, 11)
    )
    write(
        "code_counts.tex",
        rf"""
\begin{{table}}[t]
\centering
\caption{{Direct-support and primary-code counts in the selected 55-thread register.}}
\label{{tab:code-counts}}
\begin{{tabular}}{{@{{}}lrr@{{}}}}
\toprule
Code & Direct support & Primary \\
\midrule
{support_rows}
\bottomrule
\end{{tabular}}
\end{{table}}
""",
    )


if __name__ == "__main__":
    main()
