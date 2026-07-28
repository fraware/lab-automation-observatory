# Reproducibility

The committed CSV, JSON, and YAML files are the release inputs. Reproduction does not query LabAutomation.io.

```bash
uv sync --all-extras
make reproduce
make test
make paper
```

Expected headline values are asserted in `tests/test_published_values.py`. JSON Schemas are checked against the seeded records. Figures, the graphical abstract, and LaTeX tables are regenerated from committed data.

The retained XLSX workbook and compiled submission files are distributed through the versioned archival package and future DOI record. They are not required for ordinary analysis.
