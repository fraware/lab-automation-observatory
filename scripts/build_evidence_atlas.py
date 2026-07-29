#!/usr/bin/env python3
"""Regenerate the per-construct evidence atlas from committed release data."""

from __future__ import annotations

from pathlib import Path

from labauto_observatory.atlas import write_atlas_csv

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    destination = write_atlas_csv(ROOT)
    print(f"wrote {destination.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
