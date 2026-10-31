from model import hertz_contact_radius, hertz_indentation, mie_efficiency, thermal_speed


def test_hertz_contact_radius():
    # R=275nm, E*=66.7MPa, P=20.63nN (approx)
    r = hertz_contact_radius(275e-9, 66.7e6, 20.63e-9)
    assert r > 0
    assert r < 1e-6


def test_hertz_indentation():
    d = hertz_indentation(275e-9, 66.7e6, 20.63e-9)
    assert d > 0
    assert d < 1e-8


def test_thermal_speed():
    v = thermal_speed(9.583e-17, T=300.0)
    assert v > 0
    assert v < 1.0  # ~11 mm/s


def test_mie_efficiency():
    import math

    assert mie_efficiency(math.pi, complex(1.5, 0.0)) == 3.4822
    assert mie_efficiency(1.0, complex(1.5, 0.0)) == 0.0
