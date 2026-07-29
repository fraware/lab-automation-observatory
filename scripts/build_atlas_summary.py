#!/usr/bin/env python3
"""Regenerate the browsable Markdown rendering of the evidence atlas."""

from __future__ import annotations

from pathlib import Path

from labauto_observatory.atlas_summary import write_atlas_summary

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    destination = write_atlas_summary(ROOT)
    print(f"wrote {destination.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
