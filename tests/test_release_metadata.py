"""Every place the release version is declared must agree.

The version appears in five committed files plus the package itself. Nothing
compared them until this module existed, and `labauto_observatory.__version__`
had consequently read "0.1.0" since the 0.1.0 tag. A release that reports two
different versions is not citable, so these checks fail the build instead.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

import labauto_observatory
from labauto_observatory.io import read_json, read_text_lf, read_yaml

ROOT = Path(__file__).resolve().parents[1]


def _project() -> dict[str, str]:
    payload = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return {"name": payload["project"]["name"], "version": payload["project"]["version"]}


def _pyproject_version() -> str:
    return _project()["version"]


def _locked_version() -> str:
    payload = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    entries = [package for package in payload["package"] if package["name"] == _project()["name"]]
    assert len(entries) == 1, "the project should appear exactly once in uv.lock"
    version = entries[0]["version"]
    assert isinstance(version, str)
    return version


def test_declared_versions_agree() -> None:
    expected = _pyproject_version()
    assert read_yaml(ROOT / "CITATION.cff")["version"] == expected
    assert read_json(ROOT / "codemeta.json")["version"] == expected
    assert read_json(ROOT / ".zenodo.json")["version"] == expected
    assert _locked_version() == expected


def test_package_version_matches_pyproject() -> None:
    assert labauto_observatory.__version__ == _pyproject_version()


def test_changelog_documents_the_declared_version() -> None:
    changelog = read_text_lf(ROOT / "CHANGELOG.md")
    assert f"\n## [{_pyproject_version()}] - " in changelog


def test_release_dates_agree() -> None:
    released = read_yaml(ROOT / "CITATION.cff")["date-released"].isoformat()
    assert read_json(ROOT / "codemeta.json")["datePublished"] == released
    assert read_json(ROOT / ".zenodo.json")["publication_date"] == released
    assert f"\n## [{_pyproject_version()}] - {released}\n" in read_text_lf(ROOT / "CHANGELOG.md")
