from model import navier_stokes_phase_bleed, poincare_closed


def test_poincare_closed():
    assert poincare_closed() is True


def test_navier_stokes_phase_bleed_below():
    z = navier_stokes_phase_bleed(1.0, 2.0)
    assert z.imag == 0.0
    assert z.real == 1.0


def test_navier_stokes_phase_bleed_above():
    z = navier_stokes_phase_bleed(3.0, 2.0)
    assert z.imag == 3.0
    assert z.real == 0.0
