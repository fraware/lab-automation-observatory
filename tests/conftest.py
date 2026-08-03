from __future__ import annotations

import csv
import importlib.util
import os
import shutil
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest

# Figure scripts import pyplot at module load; force a headless backend first.
os.environ.setdefault("MPLBACKEND", "Agg")

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PAPER_AVAILABLE = (ROOT / "paper" / "main.tex").is_file()
requires_paper = pytest.mark.skipif(
    not PAPER_AVAILABLE,
    reason="manuscript sources are not present in this checkout",
)


def _load_script(name: str) -> ModuleType:
    """Import a top-level script from ``scripts/`` without installing it."""

    # The build scripts share `figure_style` as a sibling module, which resolves
    # through sys.path[0] when they run as `python scripts/<name>.py`.
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"observatory_scripts_{name}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load script: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def load_script() -> Callable[[str], ModuleType]:
    return _load_script


@pytest.fixture
def data_root(tmp_path: Path) -> Path:
    """A scratch repository root holding private copies of ``data/`` and ``schemas/``.

    Validation and drift checks read only from those two trees, so a test can
    break one invariant here and assert on the reported problem without touching
    the committed release. ``schemas/`` is copied because the registry seeds are
    validated against their schema as part of ``check_release_data``.
    """

    shutil.copytree(ROOT / "data", tmp_path / "data")
    shutil.copytree(ROOT / "schemas", tmp_path / "schemas")
    return tmp_path


def _edit_csv(path: Path, index: int, **changes: str) -> None:
    """Rewrite one data row of a CSV in place, preserving header and order."""

    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or ())
        rows = list(reader)
    unknown = set(changes) - set(fieldnames)
    if unknown:
        raise KeyError(f"{path.name} has no columns {sorted(unknown)}")
    rows[index].update(changes)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


@pytest.fixture
def edit_csv() -> Callable[..., None]:
    return _edit_csv


def _drop_csv_row(path: Path, index: int) -> None:
    """Delete one data row of a CSV in place."""

    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or ())
        rows = list(reader)
    del rows[index]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


@pytest.fixture
def drop_csv_row() -> Callable[[Path, int], None]:
    return _drop_csv_row
