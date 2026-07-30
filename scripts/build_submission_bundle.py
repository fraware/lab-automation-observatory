"""Assemble the canonical SLAS Technology submission ZIP and SHA256SUMS.txt."""

from __future__ import annotations

import argparse
import hashlib
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOP_LEVEL_MEMBERS = (
    "manuscript.pdf",
    "supplement.pdf",
    "cover_letter.pdf",
    "graphical_abstract.png",
    "highlights.txt",
    "latex-source/",
    "data-and-code-source.zip",
    "submission_manifest.yaml",
    "SHA256SUMS.txt",
)

LATEX_SOURCE_GLOBS = (
    "paper/*.tex",
    "paper/*.bib",
    "paper/*.sty",
    "paper/*.cls",
    "paper/figures/**/*",
    "paper/generated/**/*",
    "paper/highlights.txt",
    "paper/submission_bundle_manifest.template.yaml",
    "paper/submission_checklist.md",
)

DATA_CODE_MEMBERS = (
    "data",
    "src",
    "scripts",
    "tests",
    "schemas",
    "pyproject.toml",
    "uv.lock",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_sums(path: Path, entries: list[tuple[str, str]]) -> None:
    lines = [f"{digest}  {name}\n" for digest, name in sorted(entries, key=lambda item: item[1])]
    path.write_text("".join(lines), encoding="utf-8", newline="\n")


def add_tree(archive: zipfile.ZipFile, source: Path, arc_prefix: str) -> None:
    if source.is_file():
        archive.write(source, arc_prefix.replace("\\", "/"))
        return
    for path in sorted(source.rglob("*")):
        if path.is_file():
            relative = path.relative_to(source).as_posix()
            archive.write(path, f"{arc_prefix}/{relative}")


def collect_latex_sources() -> list[Path]:
    paths: set[Path] = set()
    for pattern in LATEX_SOURCE_GLOBS:
        paths.update(ROOT.glob(pattern))
    return sorted(path for path in paths if path.is_file())


def build_nested_data_code_zip(destination: Path) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for member in DATA_CODE_MEMBERS:
            source = ROOT / member
            if not source.exists():
                raise SystemExit(f"missing data/code member: {member}")
            if source.is_dir():
                add_tree(archive, source, member)
            else:
                archive.write(source, member)


def build_bundle(
    *,
    output_dir: Path,
    certification_sha: str,
    manifest_path: Path,
    version: str = "0.1.4",
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    sha7 = certification_sha[:7]
    stamp = date.today().isoformat()
    zip_name = (
        f"LabAutomationObservatory_SLASTechnology_NexusXp_"
        f"v{version}_{stamp}_{sha7}.zip"
    )
    zip_path = output_dir / zip_name
    staging = output_dir / f".staging_{sha7}"
    if staging.exists():
        for path in sorted(staging.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            else:
                path.rmdir()
    staging.mkdir(parents=True, exist_ok=True)

    required_pdfs = {
        "manuscript.pdf": ROOT / "paper/main.pdf",
        "supplement.pdf": ROOT / "paper/supplement.pdf",
        "cover_letter.pdf": ROOT / "paper/cover_letter.pdf",
    }
    for name, path in required_pdfs.items():
        if not path.exists():
            raise SystemExit(f"required PDF missing: {path}")
        (staging / name).write_bytes(path.read_bytes())

    ga = ROOT / "paper/graphical_abstract.png"
    highlights = ROOT / "paper/highlights.txt"
    for path in (ga, highlights, manifest_path):
        if not path.exists():
            raise SystemExit(f"required artifact missing: {path}")
    (staging / "graphical_abstract.png").write_bytes(ga.read_bytes())
    (staging / "highlights.txt").write_bytes(highlights.read_bytes())
    (staging / "submission_manifest.yaml").write_bytes(manifest_path.read_bytes())

    nested = staging / "data-and-code-source.zip"
    build_nested_data_code_zip(nested)

    latex_dir = staging / "latex-source"
    latex_dir.mkdir(parents=True, exist_ok=True)
    for path in collect_latex_sources():
        relative = path.relative_to(ROOT / "paper")
        target = latex_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())

    sum_entries: list[tuple[str, str]] = []
    for name in (
        "manuscript.pdf",
        "supplement.pdf",
        "cover_letter.pdf",
        "graphical_abstract.png",
        "highlights.txt",
        "data-and-code-source.zip",
        "submission_manifest.yaml",
    ):
        sum_entries.append((sha256_file(staging / name), name))

    # Hash latex-source as a single zip-style directory listing via a temp archive digest of members.
    latex_digest = hashlib.sha256()
    for path in sorted(latex_dir.rglob("*")):
        if path.is_file():
            relative = path.relative_to(latex_dir).as_posix()
            latex_digest.update(relative.encode("utf-8"))
            latex_digest.update(b"\0")
            latex_digest.update(path.read_bytes())
            latex_digest.update(b"\0")
    sum_entries.append((latex_digest.hexdigest(), "latex-source/"))

    sums_path = staging / "SHA256SUMS.txt"
    write_sums(sums_path, sum_entries)

    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in (
            "manuscript.pdf",
            "supplement.pdf",
            "cover_letter.pdf",
            "graphical_abstract.png",
            "highlights.txt",
            "data-and-code-source.zip",
            "submission_manifest.yaml",
            "SHA256SUMS.txt",
        ):
            archive.write(staging / name, name)
        for path in sorted(latex_dir.rglob("*")):
            if path.is_file():
                archive.write(path, f"latex-source/{path.relative_to(latex_dir).as_posix()}")

    external_sums = output_dir / "SHA256SUMS.txt"
    write_sums(
        external_sums,
        [
            (sha256_file(zip_path), zip_path.name),
            (sha256_file(sums_path), "bundle-internal-SHA256SUMS.txt"),
            (sha256_file(manifest_path), manifest_path.name),
            (sha256_file(nested), "data-and-code-source.zip"),
        ],
    )

    # Keep a copy of the nested archive and internal sums beside the ZIP for release upload.
    (output_dir / "data-and-code-source.zip").write_bytes(nested.read_bytes())
    (output_dir / "bundle-SHA256SUMS.txt").write_bytes(sums_path.read_bytes())

    print(f"wrote {zip_path}")
    print(f"wrote {external_sums}")
    for digest, name in sum_entries:
        print(f"{digest}  {name}")
    return zip_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--certification-sha",
        required=True,
        help="Full certification commit SHA used in the ZIP filename",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "artifacts/submission_bundle_manifest_v0.1.4.yaml",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "artifacts/bundles",
    )
    parser.add_argument("--version", default="0.1.4")
    args = parser.parse_args()
    build_bundle(
        output_dir=args.output_dir,
        certification_sha=args.certification_sha,
        manifest_path=args.manifest,
        version=args.version,
    )


if __name__ == "__main__":
    main()
