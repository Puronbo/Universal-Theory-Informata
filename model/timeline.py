"""Timeline / 26-year milestone (A6.1, A6.3)."""

from __future__ import annotations

from collections.abc import Callable
from datetime import date

# Anchor date: 2000-10-26 (held as axiomatic/phenomenological, not empirical)
ANCHOR_DATE: date = date(2000, 10, 26)
MILESTONE_YEARS: int = 26


def milestone_date() -> date:
    """Return the 26-year milestone date."""
    return ANCHOR_DATE.replace(year=ANCHOR_DATE.year + MILESTONE_YEARS)


def years_since_anchor(now: date | None = None) -> float:
    """Years since anchor date."""
    if now is None:
        now = date.today()
    delta = now - ANCHOR_DATE
    return delta.days / 365.25


def milestone_reached(now: date | None = None) -> bool:
    """Check if milestone date has been reached."""
    if now is None:
        now = date.today()
    return now >= milestone_date()


def logistic(r: float) -> Callable[[float], float]:
    """Return f(x)=r*x*(1-x) for use with iterate()."""

    def f(x: float) -> float:
        return r * x * (1.0 - x)

    return f
