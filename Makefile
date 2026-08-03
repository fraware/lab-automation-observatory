.PHONY: sync derived robustness atlas-summary reproduce figures tables graphical-abstract validate claims test lint typecheck paper paper-only supplement cover-letter docs docs-build links ci clean

sync:
	uv sync --all-extras

# Rebuilds the committed CSVs and the atlas summary that are derived from
# other committed data. `make validate` fails if any of them has drifted, so
# this target is what a data change must run before committing.
derived:
	uv run python scripts/build_associations.py
	uv run python scripts/build_robustness.py
	uv run python scripts/build_evidence_atlas.py
	uv run python scripts/build_atlas_summary.py
	uv run python scripts/build_blind_subset.py

robustness:
	uv run python scripts/build_robustness.py
	uv run python scripts/build_robustness_tables.py

# Regenerates only the browsable Markdown rendering of the evidence atlas.
# Included in `derived` above; kept as its own target so docs-only changes
# don't need to think about the association table.
atlas-summary:
	uv run python scripts/build_atlas_summary.py

reproduce: derived
	uv run python scripts/reproduce_results.py

figures:
	uv run python scripts/build_figures.py

tables:
	uv run python scripts/build_tables.py
	uv run python scripts/build_robustness_tables.py

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

docs: atlas-summary
	uv run mkdocs serve

docs-build: atlas-summary
	uv run mkdocs build --strict

# Mirrors the scope of .github/workflows/link-check.yml. Requires the
# `lychee` binary (https://github.com/lycheeverse/lychee) on PATH; it is not
# vendored through uv/npx.
links:
	lychee --no-progress --accept 200,206,429 --exclude-mail --max-retries 3 README.md docs data/derived data/knowledge_index

paper: reproduce figures tables
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

paper-only:
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

supplement: reproduce figures tables
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex

cover-letter:
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error cover_letter.tex

ci: lint typecheck validate test docs-build

clean:
	rm -rf build
	@if [ -d paper ]; then cd paper && latexmk -C main.tex && latexmk -C supplement.tex && latexmk -C cover_letter.tex; fi
