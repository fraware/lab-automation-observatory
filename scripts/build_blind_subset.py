#!/usr/bin/env python3
"""Regenerate the blind coder sheet from the hard-case adjudication key."""

from __future__ import annotations

from pathlib import Path

from labauto_observatory.blind_subset import write_blind_csv

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    destination = write_blind_csv(ROOT)
    print(f"wrote {destination.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
