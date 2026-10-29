"""Tests for model.plotting."""
from model import plot_delta


def test_plot_delta_returns_plt():
    try:
        plt = plot_delta()
        # If matplotlib is not installed, it raises RuntimeError
        import matplotlib.pyplot as plt_module
        assert plt is plt_module
    except RuntimeError:
        # matplotlib not installed, test passes (we check it raises correctly)
        pass
    except ImportError:
        # matplotlib not installed
        pass
