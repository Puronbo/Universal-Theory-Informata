"""Tests for model.phenomena."""

import pytest

from model import PHENOMENA, phenomena_list, phenomenon_type


def test_phenomenon_type():
    assert phenomenon_type("light") == "fold"
    assert phenomenon_type("DARK_ENERGY") == "unfold"


def test_unknown_phenomenon():
    with pytest.raises(ValueError):
        phenomenon_type("phlogiston")


def test_phenomena_list():
    names = phenomena_list()
    assert set(names) == set(PHENOMENA)
    assert "consciousness" in names
