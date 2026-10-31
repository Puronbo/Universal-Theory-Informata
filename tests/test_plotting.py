"""Tests for model.plotting."""

import sys

import pytest

from model import plot_cosmic_web, plot_delta


def test_plot_delta_returns_plt():
    plt = plot_delta()
    import matplotlib.pyplot as plt_module

    assert plt is plt_module
    plt.close("all")


def test_plot_delta_rejects_small_n():
    with pytest.raises(ValueError):
        plot_delta(n=1)


def test_plot_cosmic_web():
    plt = plot_cosmic_web(depth=2, scale=0.5)
    import matplotlib.pyplot as plt_module

    assert plt is plt_module
    plt.close("all")


def test_plot_delta_missing_matplotlib(monkeypatch):
    monkeypatch.setitem(sys.modules, "matplotlib.pyplot", None)
    with pytest.raises(RuntimeError):
        plot_delta()


def test_plot_cosmic_web_missing_matplotlib(monkeypatch):
    monkeypatch.setitem(sys.modules, "matplotlib.pyplot", None)
    with pytest.raises(RuntimeError):
        plot_cosmic_web()
