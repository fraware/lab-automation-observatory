"""Command-line interface."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from .analysis import compute_release_results
from .validation import validate_file

app = typer.Typer(no_args_is_help=True)


@app.command()
def reproduce(root: Path = typer.Option(Path.cwd(), exists=True, file_okay=False)) -> None:
    """Compute and print the release results."""

    typer.echo(json.dumps(compute_release_results(root), indent=2, ensure_ascii=False))


@app.command("validate-knowledge-index")
def validate_knowledge_index(
    records: Path = typer.Option(Path("data/knowledge_index/seed_records.yaml"), exists=True),
    schema: Path = typer.Option(Path("schemas/knowledge-index.schema.json"), exists=True),
) -> None:
    """Validate knowledge-index records against the public schema."""

    validate_file(records, schema)
    typer.echo(f"validated {records}")


if __name__ == "__main__":
    app()
