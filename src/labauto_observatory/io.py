"""Typed input helpers for committed release artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_csv_many(paths: list[str | Path]) -> list[dict[str, str]]:
    """Read and concatenate ordered CSV parts with identical headers."""

    rows: list[dict[str, str]] = []
    for path in paths:
        rows.extend(read_csv(path))
    return rows


def normalised_newlines(text: str) -> str:
    """Collapse CRLF and lone CR to LF so text compares by content only."""

    return text.replace("\r\n", "\n").replace("\r", "\n")


def read_text_lf(path: str | Path) -> str:
    """Read text and normalise its line endings to LF.

    Drift checks compare a rendered artifact against the committed file. A
    checkout can legitimately rewrite line endings -- Git's ``core.autocrlf``
    hands Windows working trees CRLF for files stored as LF -- so the comparison
    must ignore them or every drift check fails on a fresh clone. Reading is
    done with translation disabled and normalised explicitly, because the
    ``newline`` argument of ``Path.read_text`` requires Python 3.13 and this
    package supports 3.11.
    """

    with Path(path).open(encoding="utf-8", newline="") as handle:
        return normalised_newlines(handle.read())


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_yaml(path: str | Path) -> Any:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def numeric(value: str) -> float | None:
    stripped = value.strip()
    if not stripped:
        return None
    return float(stripped)


def integer(value: str) -> int | None:
    stripped = value.strip()
    if not stripped:
        return None
    return int(float(stripped))
