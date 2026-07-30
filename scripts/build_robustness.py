#!/usr/bin/env python3
"""Regenerate publication robustness CSVs from committed release data."""

from __future__ import annotations

from pathlib import Path

from labauto_observatory.robustness import write_robustness_csvs

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    for destination in write_robustness_csvs(ROOT):
        print(f"wrote {destination.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
