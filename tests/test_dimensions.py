import math
import pytest
from model import dimension_circle, dimension_bleed


def test_dimension_circle():
    c = dimension_circle(4)
    assert len(c) == 4
    assert c[0] == 0.0
    assert abs(c[1] - math.pi / 2) < 1e-9
    assert abs(c[-1] - 3 * math.pi / 2) < 1e-9


def test_dimension_circle_validation():
    try:
        dimension_circle(0)
        assert False
    except ValueError:
        pass


def test_dimension_bleed():
    assert dimension_bleed(0.0, 0.05)
    assert not dimension_bleed(0.0, 1.0)
