# Maintainer correction checklist

One-page merge gate for an evidence or metric correction. The reasoning behind each item is in
[`docs/correction-workflow.md`](../docs/correction-workflow.md); this page is the checklist only.

## Triage

- [ ] The affected record, claim, metric, or file is named exactly (an ID, a `Cnn` claim, or a
      path), not described only in prose.
- [ ] A public, linkable source backs the correction.
- [ ] The correction is classified as **note-only**, **claim-affecting**, or **release-blocking**
      (`docs/correction-workflow.md#classifying-the-correction`).

## Files

- [ ] Every file that usually moves with this correction kind either moved, or the pull request
      states why it did not.
- [ ] `Unknown` was not converted to `0`.
- [ ] A counterexample or a disputed record was not dropped; it was marked `disputed` or
      superseded with explicit lineage.

## Checks, by classification

Note-only:

- [ ] `make validate` passes.
- [ ] `make docs-build` passes, if a doc page changed.

Claim-affecting:

- [ ] `make derived` ran first, if a register or metric CSV changed.
- [ ] `make validate` and `make test` pass, with `tests/test_published_values.py` updated to the
      new values in the same pull request.
- [ ] `make tables` and `make figures` ran, and the regenerated `paper/generated/*` /
      `paper/figures/*` are committed.
- [ ] `make claims` passes, if the claim ledger, a manuscript anchor, or a `% claim: Cnn` marker
      changed.
- [ ] `CHANGELOG.md` has an `Unreleased` entry naming the value that moved and why.
- [ ] If the changed number is already published under a cut release tag, the correction targets
      a new release rather than rewriting the tagged one.

Release-blocking:

- [ ] `make ci` passes on the pull request's own branch.
- [ ] The project steward has signed off, since a release-blocking correction changes what the
      current validated baseline is.
- [ ] If the break was present in a cut release, a fresh audit note records it instead of editing
      the frozen one under `artifacts/`.

## Merge

- [ ] Merge only when the classification's required checks above are green on the pull request's
      own branch, not on a stale local run.
