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
