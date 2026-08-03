"""Assemble an anonymous CSCW review source/PDF package for local inspection.

The ZIP is written under artifacts/bundles/ (gitignored). It intentionally omits
Git history, author metadata files, public repository URLs, and release names.
Run after compiling paper/main_cscw.pdf.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IDENTITY_PATTERNS = (
    re.compile(r"Petel", re.I),
    re.compile(r"mpetel", re.I),
    re.compile(r"fraware", re.I),
    re.compile(r"github\.com/fraware", re.I),
    re.compile(r"ORCID", re.I),
)

MANUSCRIPT_MEMBERS = (
    "paper/main_cscw.tex",
    "paper/venues/cscw/01_introduction.tex",
    "paper/venues/cscw/02_related_work.tex",
    "paper/venues/cscw/03_methods.tex",
    "paper/venues/cscw/04_findings.tex",
    "paper/venues/cscw/05_discussion.tex",
    "paper/venues/cscw/06_design_implications.tex",
    "paper/venues/cscw/07_limitations.tex",
    "paper/venues/cscw/08_conclusion.tex",
    "paper/venues/cscw/09_anonymous_availability.tex",
    "paper/venues/cscw/references.bib",
    "paper/venues/cscw/forum_references.bib",
    "paper/venues/cscw/cover_letter.md",
    "paper/venues/cscw/README.md",
)

ARTIFACT_MEMBERS = (
    "data/derived",
    "data/metrics",
    "data/robustness",
    "schemas",
    "src",
    "scripts",
    "tests",
    "pyproject.toml",
    "uv.lock",
    "CLAIM_BOUNDARIES.md",
)

ANON_README = """# Anonymous CSCW review package

This archive contains the anonymized CSCW manuscript sources, compiled PDF, and
derived artifact tree needed for review. It excludes Git history, author names,
affiliations, emails, acknowledgements, public authored repository URLs, and
release marketing names.

Reviewers receive derived data, schemas, analysis code, and tests. The archive
does not include a verbatim forum corpus or contributor handles.

Before portal upload, strip PDF metadata with venue tooling if the local PDF
still carries producer strings, and complete the submission-history disclosure
in cover_letter.md.
"""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_tree(archive: zipfile.ZipFile, source: Path, arc_prefix: str) -> None:
    for path in sorted(source.rglob("*")):
        if path.is_file():
            relative = path.relative_to(source).as_posix()
            archive.write(path, f"{arc_prefix}/{relative}")


def scan_text(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    return [pattern.pattern for pattern in IDENTITY_PATTERNS if pattern.search(text)]


def build_package(*, output_dir: Path, certification_sha: str, version: str) -> Path:
    pdf = ROOT / "paper/main_cscw.pdf"
    if not pdf.exists():
        raise SystemExit("compile paper/main_cscw.pdf before building the anonymous package")

    output_dir.mkdir(parents=True, exist_ok=True)
    sha7 = certification_sha[:7]
    stamp = date.today().isoformat()
    zip_name = f"LabAutomationObservatory_CSCW_Anonymous_v{version}_{stamp}_{sha7}.zip"
    zip_path = output_dir / zip_name

    identity_hits: dict[str, list[str]] = {}
    for relative in MANUSCRIPT_MEMBERS:
        path = ROOT / relative
        if not path.exists():
            raise SystemExit(f"missing manuscript member: {relative}")
        hits = scan_text(path)
        if hits:
            identity_hits[relative] = hits
    if identity_hits:
        details = "\n".join(f"  {path}: {', '.join(hits)}" for path, hits in identity_hits.items())
        raise SystemExit(f"identity strings found in anonymous sources:\n{details}")

    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("README_ANONYMOUS.md", ANON_README)
        archive.write(pdf, "manuscript/main_cscw.pdf")
        for relative in MANUSCRIPT_MEMBERS:
            source = ROOT / relative
            if relative == "paper/main_cscw.tex":
                archive.write(source, "manuscript/main_cscw.tex")
            else:
                archive.write(source, f"manuscript/{relative.removeprefix('paper/')}")
        for member in ARTIFACT_MEMBERS:
            source = ROOT / member
            if not source.exists():
                raise SystemExit(f"missing artifact member: {member}")
            if source.is_dir():
                add_tree(archive, source, f"artifact/{member}")
            else:
                archive.write(source, f"artifact/{member}")

    print(f"wrote {zip_path}")
    print(f"{sha256_file(zip_path)}  {zip_path.name}")
    print("identity_scan_manuscript_sources: clean")
    return zip_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certification-sha", required=True)
    parser.add_argument("--version", default="0.1.5")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "artifacts/bundles",
    )
    args = parser.parse_args()
    build_package(
        output_dir=args.output_dir,
        certification_sha=args.certification_sha,
        version=args.version,
    )


if __name__ == "__main__":
    main()
