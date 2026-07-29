.PHONY: sync derived reproduce figures tables graphical-abstract validate claims test lint typecheck paper paper-only supplement cover-letter docs docs-build links ci clean

sync:
	uv sync --all-extras

# Rebuilds the two committed CSVs that are derived from other committed data.
# `make validate` fails if either has drifted, so this target is what a data
# change must run before committing.
derived:
	uv run python scripts/build_associations.py
	uv run python scripts/build_evidence_atlas.py

reproduce: derived
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

# Mirrors the scope of .github/workflows/link-check.yml. Requires the
# `lychee` binary (https://github.com/lycheeverse/lychee) on PATH; it is not
# vendored through uv/npx.
links:
	lychee --no-progress --accept 200,206,429 --exclude-mail --max-retries 3 README.md docs paper data/derived data/knowledge_index

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

ci: lint typecheck validate test docs-build paper supplement cover-letter graphical-abstract

clean:
	cd paper && latexmk -C main.tex && latexmk -C supplement.tex && latexmk -C cover_letter.tex
	rm -rf build
