# Contributing

Contributions are welcome when they improve evidence quality, applicability, or community utility.

For coding, register, claim-ledger, and knowledge-index changes, follow the step-by-step guide in [docs/contributing-evidence.md](docs/contributing-evidence.md).

## Pull-request requirements

- Identify the record, metric, schema, or manuscript claim affected.
- Link public supporting evidence.
- Separate observation, interpretation, and causal status.
- Preserve unknown separately from absent.
- State the validation stage and applicability boundary.
- Update tests, generated outputs, and the claim ledger when published values change.
- Keep every approved claim traceable: a `% claim: Cnn` marker next to the manuscript passage and a matching `Manuscript anchor` in the ledger.

Run:

```bash
uv sync --all-extras
make ci
```

On Windows, `make` is not available by default; [REPRODUCIBILITY.md](REPRODUCIBILITY.md#windows-and-powershell) lists the PowerShell equivalents.

Do not submit copied forum threads, user profiles, private correspondence, or unsupported vendor comparisons.
