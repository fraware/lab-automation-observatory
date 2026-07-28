.PHONY: sync reproduce figures tables graphical-abstract validate claims test lint typecheck paper paper-only supplement cover-letter docs docs-build ci clean

sync:
	uv sync --all-extras

reproduce:
	uv run python scripts/reproduce_results.py

figures:
	uv run python scripts/build_figures.py

tables:
	uv run python scripts/build_tables.py

graphical-abstract:
	uv run python scripts/build_graphical_abstract.py

validate:
	uv run python scripts/validate_release.py

claims:
	uv run python scripts/check_claim_traceability.py

lint:
	uv run ruff check .
	uv run ruff format --check .

typecheck:
	uv run mypy src/labauto_observatory

test:
	uv run pytest

docs:
	uv run mkdocs serve

docs-build:
	uv run mkdocs build --strict

# `paper` refreshes the generated inputs first and therefore needs the Python
# environment. Committed figures and tables let `paper-only` build with a TeX
# distribution alone.
paper: reproduce figures tables
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

paper-only:
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

supplement: reproduce figures tables
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex

cover-letter:
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error cover_letter.tex

ci: lint typecheck validate test paper supplement cover-letter graphical-abstract

clean:
	cd paper && latexmk -C main.tex && latexmk -C supplement.tex && latexmk -C cover_letter.tex
	rm -rf build
