#!/usr/bin/env python3
"""Generate supplementary LaTeX tables for robustness analyses."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from labauto_observatory.io import read_csv
from labauto_observatory.latex import percent

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "generated"


def write(name: str, content: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(content.strip() + "\n", encoding="utf-8")


def partial_score_table() -> str:
    rows = read_csv(ROOT / "data/metrics/partial_score_sensitivity.csv")
    by_metric: dict[str, dict[str, str]] = defaultdict(dict)
    for row in rows:
        by_metric[row["Metric"]][row["Partial weight"]] = percent(float(row["Mean"]))
    order = ("IAS", "RMC", "PDC", "OC")
    weights = ("0", "0.25", "0.5", "0.75", "1")
    body = "\n".join(
        f"{metric} & " + " & ".join(by_metric[metric][weight] for weight in weights) + r" \\"
        for metric in order
    )
    return rf"""
\begin{{table}}[tp]
\centering
\caption{{Sensitivity of component-score means to the numerical value assigned to a partial field.}}
\label{{tab:s-partial-score-sensitivity}}
\begin{{threeparttable}}
\begin{{tabular}}{{@{{}}lrrrrr@{{}}}}
\toprule
Metric & Partial $=0$ & Partial $=0.25$ & Partial $=0.5$ & Partial $=0.75$ & Partial $=1$ \\
\midrule
{body}
\bottomrule
\end{{tabular}}
\begin{{tablenotes}}[flushleft]\footnotesize
\item The central release value uses 0.5. Each column recomputes case means and then the across-case mean while leaving absent, complete, and unknown cells unchanged. These ordinal summaries are neither calibrated probabilities nor a common cross-metric performance scale.
\end{{tablenotes}}
\end{{threeparttable}}
\end{{table}}
"""


def association_loto_table() -> str:
    rows = read_csv(ROOT / "data/metrics/association_leave_one_out.csv")[:5]
    body_lines: list[str] = []
    for row in rows:
        full_phi = float(row["Full phi"])
        low = float(row["Minimum phi"])
        high = float(row["Maximum phi"])
        rank_low = int(row["Minimum rank"])
        rank_high = int(row["Maximum rank"])
        top_five = int(row["Top-five deletions"])
        threshold = int(row["Threshold-retained deletions"])
        total = int(row["Total deletions"])
        body_lines.append(
            f"{row['Code A']}--{row['Code B']} & {full_phi:.3f} & {low:.3f}--{high:.3f} & "
            f"{rank_low}--{rank_high} & {top_five}/{total} & {threshold}/{total} \\\\"
        )
    body = "\n".join(body_lines)
    return rf"""
\begin{{table}}[tp]
\centering
\caption{{Leave-one-thread-out stability of the five leading technical-code associations.}}
\label{{tab:s-association-loto}}
\begin{{threeparttable}}
\begin{{tabular}}{{@{{}}lrrrrr@{{}}}}
\toprule
Pair & Full $\phi$ & Deletion range & Rank range & Top-five & Threshold retained \\
\midrule
{body}
\bottomrule
\end{{tabular}}
\begin{{tablenotes}}[flushleft]\footnotesize
\item Each of the 55 selected threads is deleted once. The threshold column counts deletions for which $\phi\geq0.30$ and lift $\geq1.50$. This is a descriptive influence analysis over a purposive multi-label register, not a population jackknife or inferential interval.
\end{{tablenotes}}
\end{{threeparttable}}
\end{{table}}
"""


def main() -> None:
    write("partial_score_sensitivity.tex", partial_score_table())
    write("association_leave_one_out.tex", association_loto_table())


if __name__ == "__main__":
    main()
