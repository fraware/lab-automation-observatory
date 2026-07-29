"""Mutation tests for the release-data invariants.

Each test breaks exactly one invariant in a scratch copy of ``data/`` and asserts
that the corresponding check reports it. Without these, an invariant could stop
holding without any test noticing, because the committed data satisfies them all.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from labauto_observatory.io import read_csv
from labauto_observatory.register_validation import (
    EXPECTED_ROW_COUNTS,
    check_b2_component_bookkeeping,
    check_b3_applicable_fields,
    check_b6_denominator_status,
    check_b7_denominator,
    check_b8_alignment_eligibility,
    check_categoricals,
    check_derived_scores,
    check_episode_and_adjudication_subsets,
    check_episode_provenance,
    check_episode_thread_coherence,
    check_evidence_register,
    check_funnel_intervals,
    check_matched_cases,
    check_release_data,
    check_row_counts,
    check_score_cells,
    check_segmentation_targets,
)

ROOT = Path(__file__).resolve().parents[1]

B2 = "data/metrics/b2_integration_access.csv"
B3 = "data/metrics/b3_reproducibility_manifest.csv"
B6 = "data/metrics/b6_preflight_preventability.csv"
B7 = "data/metrics/b7_constraint_completeness.csv"
B8 = "data/metrics/b8_test_claim_alignment.csv"
B10 = "data/metrics/b10_documentation_profile.csv"
FUNNEL = "data/metrics/ai_validation_funnel.csv"
MATCHED = "data/metrics/b2_b10_matched_cases.csv"
REGISTER = "data/derived/evidence_register_part_01.csv"
EPISODES = "data/derived/episode_register_part_01.csv"
ADJUDICATION = "data/derived/reliability_subset.csv"


def test_committed_release_data_passes_every_check() -> None:
    report = check_release_data(ROOT)
    assert report.problems == ()
    assert report.ok
    assert report.checked_files == tuple(sorted(EXPECTED_ROW_COUNTS))


def test_every_documented_file_is_checked() -> None:
    """The row-count table must not silently omit a committed release CSV."""

    committed = {
        path.relative_to(ROOT).as_posix()
        for directory in ("data/derived", "data/metrics", "data/knowledge_index")
        for path in (ROOT / directory).glob("*.csv")
    }
    assert committed == set(EXPECTED_ROW_COUNTS)


def test_row_count_change_is_reported(
    data_root: Path, drop_csv_row: Callable[[Path, int], None]
) -> None:
    drop_csv_row(data_root / "data/derived/taxonomy_rules.csv", 0)
    assert check_row_counts(data_root) == [
        "data/derived/taxonomy_rules.csv: expected 10 rows, found 9"
    ]


def test_missing_file_is_reported(data_root: Path) -> None:
    (data_root / MATCHED).unlink()
    assert check_row_counts(data_root) == [f"{MATCHED}: required release file is missing"]


def test_out_of_range_score_cell_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / B2, 0, **{"Documentation": "0.7"})
    problems = check_score_cells(data_root)
    assert problems == [
        f"{B2} line 2: 'Documentation' is '0.7', not 0, 0.5, 1, or empty",
    ]


def test_derived_score_that_disagrees_with_its_components_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / B2, 0, IAS="0.1")
    problems = check_derived_scores(data_root)
    assert len(problems) == 1
    assert problems[0].startswith(f"{B2} line 2: 'IAS' is '0.1'")


def test_unknown_categorical_value_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / B2, 0, **{"Positive case": "Maybe"})
    problems = check_categoricals(data_root)
    assert problems == [
        f"{B2} line 2: 'Positive case' is 'Maybe', not one of ['No', 'Yes']",
    ]


def test_primary_code_outside_direct_support_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / REGISTER, 0, Primary="B9", B9="0")
    problems = check_evidence_register(data_root)
    assert any("so Primary is not a subset of Direct support" in problem for problem in problems)


def test_invalid_register_cells_are_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(
        data_root / REGISTER,
        1,
        B2="2",
        **{"Evidence strength": "9", "External migration": "Sometimes", "Source URL": " "},
    )
    problems = check_evidence_register(data_root)
    assert any("B2 flag is '2'" in problem for problem in problems)
    assert any("evidence strength '9' is not 1--4" in problem for problem in problems)
    assert any("external migration 'Sometimes' is invalid" in problem for problem in problems)
    assert any("source URL is empty" in problem for problem in problems)


def test_non_construct_primary_code_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / REGISTER, 2, Primary="B42")
    problems = check_evidence_register(data_root)
    assert any("primary code 'B42' is not a construct" in problem for problem in problems)


def test_register_identifier_gap_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / REGISTER, 0, ID="99")
    problems = check_evidence_register(data_root)
    assert "evidence register: IDs are not the contiguous range 1..N" in problems


def test_adjudication_set_must_equal_the_episode_subset(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / ADJUDICATION, 0, **{"Thread ID": "999"})
    problems = check_episode_and_adjudication_subsets(data_root)
    assert any("differ on threads" in problem for problem in problems)
    assert "thread 999 is referenced but absent from the evidence register" in problems


def test_duplicate_episode_identifier_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    target = data_root / EPISODES
    edit_csv(target, 1, **{"Episode ID": read_csv(target)[0]["Episode ID"]})
    problems = check_episode_and_adjudication_subsets(data_root)
    assert "episode register: episode IDs are not unique" in problems


def test_non_construct_episode_code_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / EPISODES, 0, **{"Primary technical code": "B42"})
    problems = check_episode_and_adjudication_subsets(data_root)
    assert any("is not a construct" in problem for problem in problems)


def test_episode_code_without_a_thread_flag_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    """An episode may not evidence a code its own thread records as unsupported."""

    edit_csv(data_root / EPISODES, 0, **{"Ecosystem modifiers": "B1; B5; B10"})
    assert check_episode_thread_coherence(data_root) == [
        "episode T02-E1: modifier B5 has no direct-support flag on thread 2, so the episode "
        "asserts a condition the thread-level coding denies"
    ]
    edit_csv(data_root / EPISODES, 0, **{"Primary technical code": "B5"})
    assert any(
        "primary technical code B5 has no direct-support flag" in problem
        for problem in check_episode_thread_coherence(data_root)
    )


def test_coherence_leaves_a_dangling_thread_reference_to_the_subset_check(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    """A thread ID absent from the register is one check's problem, not two."""

    edit_csv(data_root / EPISODES, 0, **{"Thread ID": "999"})
    assert check_episode_thread_coherence(data_root) == []
    assert any(
        "absent from the evidence register" in problem
        for problem in check_episode_and_adjudication_subsets(data_root)
    )


def test_vague_segmentation_target_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    """A target no segmentation can contradict is not a target."""

    edit_csv(
        data_root / ADJUDICATION, 0, **{"Episode segmentation required": "Yes — at least three"}
    )
    problems = check_segmentation_targets(data_root)
    assert any("states no exact episode count" in problem for problem in problems)


def test_segmentation_target_that_disagrees_with_the_register_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / ADJUDICATION, 0, **{"Episode segmentation required": "Yes — 9 episodes"})
    assert check_segmentation_targets(data_root) == [
        "adjudication thread 2: expects 9 episodes but the episode register holds 3"
    ]


def test_dropping_an_episode_contradicts_its_thread_target(
    data_root: Path, drop_csv_row: Callable[[Path, int], None]
) -> None:
    drop_csv_row(data_root / EPISODES, 0)
    assert check_segmentation_targets(data_root) == [
        "adjudication thread 2: expects 3 episodes but the episode register holds 2"
    ]


def test_empty_read_scope_is_reported(data_root: Path, edit_csv: Callable[..., None]) -> None:
    edit_csv(data_root / ADJUDICATION, 0, **{"Read scope": " "})
    assert check_segmentation_targets(data_root) == ["adjudication thread 2: read scope is empty"]


def test_non_construct_counterexample_scope_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / EPISODES, 0, **{"Counterexample to": "B4; B42"})
    assert check_episode_provenance(data_root) == [
        "episode T02-E1: counterexample scope 'B42' is not a construct"
    ]


def test_first_post_anchor_must_be_post_anchored(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    """An empty anchor is allowed; a page URL masquerading as one is not."""

    edit_csv(data_root / EPISODES, 0, **{"First post anchor": ""})
    assert check_episode_provenance(data_root) == []
    edit_csv(
        data_root / EPISODES,
        0,
        **{"First post anchor": "https://labautomation.io/t/thread/103?page=2"},
    )
    problems = check_episode_provenance(data_root)
    assert any("is not a post-anchored discussion URL" in problem for problem in problems)


def test_b2_unknown_component_bookkeeping_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / B2, 0, **{"Unknown components": "3"})
    problems = check_b2_component_bookkeeping(data_root)
    assert len(problems) == 1
    assert "'Unknown components' is '3'" in problems[0]


def test_b3_applicable_field_count_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / B3, 0, **{"Applicable fields": "99"})
    problems = check_b3_applicable_fields(data_root)
    assert len(problems) == 1
    assert "'Applicable fields' is '99'" in problems[0]


def test_b6_denominator_status_must_follow_detectability(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / B6, 0, **{"Denominator status": "Eligible / indeterminate"})
    problems = check_b6_denominator_status(data_root)
    assert len(problems) == 1
    assert "implies denominator status 'Eligible / definite'" in problems[0]


def test_b7_rates_need_a_non_empty_denominator(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    target = data_root / B7
    for index in range(EXPECTED_ROW_COUNTS[B7]):
        edit_csv(target, index, **{"Opening score (0/0.5/1)": "1", "Present at opening?": "Yes"})
    problems = check_b7_denominator(data_root)
    assert any("empty denominator" in problem for problem in problems)


def test_b7_presence_flag_must_agree_with_the_opening_score(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / B7, 0, **{"Present at opening?": "No"})
    problems = check_b7_denominator(data_root)
    assert any("'Present at opening?' is 'No'" in problem for problem in problems)


def test_b8_alignment_class_must_match_numerator_eligibility(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / B8, 0, **{"Alignment class": "Aligned"})
    problems = check_b8_alignment_eligibility(data_root)
    assert any("numerator eligibility" in problem for problem in problems)
    assert any("not every alignment element scores 1" in problem for problem in problems)


def test_funnel_interval_columns_must_match_the_release_code(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / FUNNEL, 2, **{"95% Wilson low": "0.5", "Rate": "0.5"})
    problems = check_funnel_intervals(data_root)
    assert any("does not equal 92/100" in problem for problem in problems)
    assert any("Wilson low '0.5'" in problem for problem in problems)


def test_funnel_stage_without_counts_must_not_report_a_rate(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / FUNNEL, 0, Rate="1.0")
    problems = check_funnel_intervals(data_root)
    assert any("reports a rate or interval without both counts" in problem for problem in problems)


def test_matched_cases_must_restate_their_sources(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / MATCHED, 0, IAS="0.05", **{"Private migration": "Yes"})
    problems = check_matched_cases(data_root)
    assert any("IAS does not match" in problem for problem in problems)
    assert any("'Private migration' does not match" in problem for problem in problems)


def test_matched_cases_must_reference_known_cases(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / MATCHED, 0, **{"B2 case": "B2-C99"})
    problems = check_matched_cases(data_root)
    assert any("references an unknown B2 or B10 case" in problem for problem in problems)


def test_matched_cases_must_restate_their_narrative_columns(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(
        data_root / MATCHED,
        0,
        **{
            "Device / interface": "Something else",
            "Documentation subtypes at full weight": "None",
            "Source URL": "https://example.invalid",
        },
    )
    problems = check_matched_cases(data_root)
    assert any("device/interface does not match" in problem for problem in problems)
    assert any("documentation subtypes at full weight should be" in problem for problem in problems)
    assert any("source URL does not match" in problem for problem in problems)


def test_b7_opening_score_outside_the_scale_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / B7, 0, **{"Opening score (0/0.5/1)": "0.7"})
    problems = check_b7_denominator(data_root)
    assert any("is not 0, 0.5, or 1" in problem for problem in problems)


def test_funnel_wilson_high_mismatch_is_reported(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / FUNNEL, 2, **{"95% Wilson high": "0.99"})
    problems = check_funnel_intervals(data_root)
    assert any("Wilson high '0.99'" in problem for problem in problems)


def test_missing_score_column_is_reported(data_root: Path) -> None:
    target = data_root / B2
    rows = target.read_text(encoding="utf-8").splitlines()
    header = rows[0].replace("Documentation,", "", 1)
    body = [line.split(",", 1)[1] for line in rows[1:]]
    target.write_text("\n".join([header, *body]) + "\n", encoding="utf-8")
    assert any(
        "missing score column 'Documentation'" in problem
        for problem in check_score_cells(data_root)
    )


def test_missing_categorical_column_is_reported(data_root: Path) -> None:
    target = data_root / B8
    text = target.read_text(encoding="utf-8")
    target.write_text(
        text.replace("Numerator eligibility", "Numerator eligibility x", 1), encoding="utf-8"
    )
    problems = check_categoricals(data_root)
    assert any(
        "missing categorical column 'Numerator eligibility'" in problem for problem in problems
    )


def test_check_release_data_collects_problems_from_every_check(
    data_root: Path, edit_csv: Callable[..., None]
) -> None:
    edit_csv(data_root / B2, 0, **{"Documentation": "0.7"})
    edit_csv(data_root / B10, 0, **{"Private migration": "Sometimes"})
    report = check_release_data(data_root)
    assert not report.ok
    assert any("not 0, 0.5, 1, or empty" in problem for problem in report.problems)
    assert any("'Private migration' is 'Sometimes'" in problem for problem in report.problems)
