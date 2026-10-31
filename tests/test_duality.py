"""Tests for model.duality."""

import pytest

from model import DUAL_PAIRS, DualPair, all_poles, dual_of, dual_pair, dual_pairs


def test_registry_is_returned():
    assert dual_pairs() == DUAL_PAIRS


def test_pair_fields_and_swap():
    pair = DualPair("scale", "UV", "IR")
    assert pair.other("UV") == "IR"
    assert pair.other("IR") == "UV"


@pytest.mark.parametrize(
    ("pole", "expected"),
    [
        ("UV", "IR"),
        ("IR", "UV"),
        ("exterior", "interior"),
        ("interior", "exterior"),
        ("compression", "expansion"),
        ("expansion", "compression"),
        ("photon", "dark energy"),
        ("dark energy", "photon"),
        ("entropy", "structure"),
        ("structure", "entropy"),
        ("becoming", "block"),
        ("block", "becoming"),
        ("discrete", "continuous"),
        ("continuous", "discrete"),
        ("reprocessed", "erased"),
        ("erased", "reprocessed"),
    ],
)
def test_known_duals(pole, expected):
    assert dual_of(pole) == expected


def test_pair_lookup_by_name():
    assert dual_pair("scale") is DUAL_PAIRS[0]
    with pytest.raises(ValueError):
        dual_pair("unknown")


def test_all_poles_matches_registry():
    expected = tuple(pole for pair in DUAL_PAIRS for pole in (pair.left, pair.right))
    assert all_poles() == expected


def test_dual_is_an_involution():
    poles = [pole for pair in DUAL_PAIRS for pole in (pair.left, pair.right)]
    for pole in poles:
        assert dual_of(dual_of(pole)) == pole


def test_names_and_poles_are_unique():
    names = [pair.name for pair in DUAL_PAIRS]
    poles = [pole for pair in DUAL_PAIRS for pole in (pair.left, pair.right)]
    assert len(names) == len(set(names))
    assert len(poles) == len(set(poles))


def test_unknown_pole_is_rejected():
    with pytest.raises(ValueError):
        dual_of("visible")
    with pytest.raises(ValueError):
        DualPair("x", "a", "b").other("c")


def test_duals_are_case_sensitive():
    with pytest.raises(ValueError):
        dual_of("uv")


@pytest.mark.parametrize(
    "pair",
    [
        ("", "a", "b"),
        ("x", "", "b"),
        ("x", "a", ""),
        ("x", "a", "a"),
    ],
)
def test_invalid_pairs_are_rejected(pair):
    with pytest.raises(ValueError):
        DualPair(*pair)
