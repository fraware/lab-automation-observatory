"""Render committed CSV text as LaTeX.

The manuscript sources are pure ASCII, so generated tables must be too. The
escaper therefore fails closed: any character it does not know how to render is
reported instead of being written into a table that LaTeX would silently
mangle.
"""

from __future__ import annotations

SPECIAL: tuple[tuple[str, str], ...] = (
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("$", r"\$"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
)
TYPOGRAPHIC: tuple[tuple[str, str], ...] = (
    ("\u2014", "---"),
    ("\u2013", "--"),
    ("\u2212", "$-$"),
    ("\u2019", "'"),
    ("\u2018", "`"),
    ("\u201c", "``"),
    ("\u201d", "''"),
    ("\u2026", r"\ldots{}"),
    ("\u00a0", "~"),
)


# One pass over the input, so a replacement that itself contains a special
# character (``\`` becomes ``\textbackslash{}``) is not escaped a second time.
REPLACEMENTS: dict[str, str] = dict(SPECIAL + TYPOGRAPHIC)


def escape(text: str) -> str:
    """Escape one CSV cell for LaTeX body text."""

    rendered = "".join(REPLACEMENTS.get(character, character) for character in text)
    unsupported = sorted({character for character in rendered if ord(character) > 127})
    if unsupported:
        raise ValueError(
            "cannot render these characters as ASCII LaTeX: "
            + ", ".join(f"U+{ord(character):04X}" for character in unsupported)
        )
    return rendered


def percent(value: float, digits: int = 1) -> str:
    """Render a proportion as a LaTeX percentage."""

    return f"{100 * value:.{digits}f}\\%"


def percent_interval(bounds: list[float] | tuple[float, float], digits: int = 1) -> str:
    """Render a descriptive interval as a compact ``low--high`` percentage range."""

    low, high = bounds
    return f"{100 * low:.{digits}f}--{100 * high:.{digits}f}\\%"
