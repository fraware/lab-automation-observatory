from __future__ import annotations

import importlib.util
import os
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest

# Figure scripts import pyplot at module load; force a headless backend first.
os.environ.setdefault("MPLBACKEND", "Agg")

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def _load_script(name: str) -> ModuleType:
    """Import a top-level script from ``scripts/`` without installing it."""

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
