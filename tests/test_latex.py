"""The LaTeX escaper must fail closed rather than emit a character LaTeX mangles."""

from __future__ import annotations

import pytest

from labauto_observatory.latex import escape, percent, percent_interval


def test_special_characters_are_escaped() -> None:
    assert escape("50% of tips & 3_of_4 {sets}") == r"50\% of tips \& 3\_of\_4 \{sets\}"
    assert escape("$x^2$ ~ #1") == r"\$x\textasciicircum{}2\$ \textasciitilde{} \#1"
    assert escape(r"C:\path") == r"C:\textbackslash{}path"


def test_typographic_characters_become_ascii_latex() -> None:
    assert escape("Capture everything\u2014and only surface what you need") == (
        "Capture everything---and only surface what you need"
    )
    assert escape("test\u2013claim alignment") == "test--claim alignment"
    assert escape("\u201cquoted\u201d and \u2018quoted\u2019") == "``quoted'' and `quoted'"
    assert escape("\u22120.37") == "$-$0.37"
    assert escape("wait\u2026") == r"wait\ldots{}"
    assert escape("6\u00a0cases") == "6~cases"


def test_unmapped_non_ascii_character_is_reported() -> None:
    with pytest.raises(ValueError, match=r"U\+00E9"):
        escape("Mat\u00e9o")


def test_percentage_helpers() -> None:
    assert percent(0.6388888889) == r"63.9\%"
    assert percent(0.92, digits=0) == r"92\%"
    assert percent_interval([0.2076549551, 0.9385096847]) == r"20.8--93.9\%"
