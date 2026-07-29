#!/usr/bin/env python3
"""Regenerate the pairwise association table from the evidence register."""

from __future__ import annotations

from pathlib import Path

from labauto_observatory.associations import write_pairwise_csv

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    destination = write_pairwise_csv(ROOT)
    print(f"wrote {destination.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
