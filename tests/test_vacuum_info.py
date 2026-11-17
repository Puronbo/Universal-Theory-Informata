"""Tests for model.vacuum_info — what "nothing" can and cannot hold."""

import math

import pytest

from model import (
    BITS_PER_NAT,
    PLANCK_LENGTH,
    apply_local_unitary,
    bekenstein_bits,
    desitter_bits,
    desitter_horizon_radius,
    holographic_bits,
    landauer_energy,
    marginal_probabilities,
    two_mode_mutual_information,
    two_mode_squeezing_photon_number,
)

SQRT_HALF = 1.0 / math.sqrt(2.0)
BELL = (SQRT_HALF, 0j, 0j, SQRT_HALF)
X_GATE = ((0j, 1.0), (1.0, 0j))
Z_GATE = ((1.0, 0j), (0j, -1.0))
Y_GATE = ((0j, -1j), (1j, 0j))
IDENTITY_2 = ((1.0, 0j), (0j, 1.0))


def _entropy_bits(photons: float) -> float:
    """Entropy of one thermal mode, in bits, for a pure two-mode state."""
    if photons == 0.0:
        return 0.0
    entropy = (photons + 1.0) * math.log(photons + 1.0) - photons * math.log(photons)
    return entropy / math.log(2.0)


# Constants ----------------------------------------------------------------


def test_bits_per_nat_is_the_base_conversion():
    assert BITS_PER_NAT == pytest.approx(1.0 / math.log(2.0))
    assert BITS_PER_NAT == pytest.approx(1.4426950408889634)


def test_planck_length_is_the_standard_value():
    assert PLANCK_LENGTH == pytest.approx(1.616255e-35)
    assert 1.6e-35 < PLANCK_LENGTH < 1.7e-35


# Bekenstein bound ---------------------------------------------------------


def test_bekenstein_zero_energy_or_radius_holds_no_bits():
    assert bekenstein_bits(0.0, 1.0) == 0.0
    assert bekenstein_bits(1.0, 0.0) == 0.0
    assert bekenstein_bits(0.0, 0.0) == 0.0


def test_bekenstein_is_linear_in_radius_and_energy():
    base = bekenstein_bits(1.0, 1.0)
    assert bekenstein_bits(2.0, 1.0) == pytest.approx(2.0 * base)
    assert bekenstein_bits(1.0, 3.0) == pytest.approx(3.0 * base)
    assert bekenstein_bits(4.0, 5.0) == pytest.approx(20.0 * base)


def test_bekenstein_matches_the_formula():
    from model import REDUCED_PLANCK, SPEED_OF_LIGHT

    radius, energy = 2.5, 7.0
    expected = 2.0 * math.pi * radius * energy / (REDUCED_PLANCK * SPEED_OF_LIGHT * math.log(2.0))
    assert bekenstein_bits(radius, energy) == pytest.approx(expected)


def test_bekenstein_one_metre_and_one_joule_is_about_2_9e26_bits():
    assert bekenstein_bits(1.0, 1.0) == pytest.approx(2.87e26, rel=1e-2)


@pytest.mark.parametrize("radius", [-1.0, math.inf, -math.inf, math.nan])
def test_bekenstein_rejects_invalid_radius(radius):
    with pytest.raises(ValueError):
        bekenstein_bits(radius, 1.0)


@pytest.mark.parametrize("energy", [-1.0, math.inf, -math.inf, math.nan])
def test_bekenstein_rejects_invalid_energy(energy):
    with pytest.raises(ValueError):
        bekenstein_bits(1.0, energy)


# Holographic bound --------------------------------------------------------


def test_holographic_zero_area_holds_no_bits():
    assert holographic_bits(0.0) == 0.0


def test_one_planck_area_holds_one_quarter_ln2_bits():
    assert holographic_bits(PLANCK_LENGTH**2) == pytest.approx(1.0 / (4.0 * math.log(2.0)))
    assert holographic_bits(PLANCK_LENGTH**2) == pytest.approx(0.36067376022224085)


def test_holographic_is_linear_in_area():
    unit = holographic_bits(1.0)
    assert holographic_bits(7.0) == pytest.approx(7.0 * unit)
    assert holographic_bits(PLANCK_LENGTH**2 * 4.0) == pytest.approx(1.0 / math.log(2.0))


def test_holographic_one_square_metre_is_about_1_4e69_bits():
    assert holographic_bits(1.0) == pytest.approx(1.38e69, rel=1e-2)


@pytest.mark.parametrize("area", [-1.0, math.inf, -math.inf, math.nan])
def test_holographic_rejects_invalid_area(area):
    with pytest.raises(ValueError):
        holographic_bits(area)


# de Sitter horizon --------------------------------------------------------


def test_desitter_radius_is_c_over_h():
    from model import SPEED_OF_LIGHT

    hubble = 2.2e-18
    assert desitter_horizon_radius(hubble) == pytest.approx(SPEED_OF_LIGHT / hubble)
    assert desitter_horizon_radius(hubble) == pytest.approx(1.36e26, rel=1e-2)


def test_desitter_bits_uses_the_horizon_area():
    hubble = 2.2e-18
    radius = desitter_horizon_radius(hubble)
    assert desitter_bits(hubble) == pytest.approx(holographic_bits(4.0 * math.pi * radius**2))


def test_observed_hubble_scale_holds_about_1e122_bits():
    # H0 = 70 km/s/Mpc in inverse seconds.
    hubble = 70e3 / 3.085677581491367e22
    assert desitter_bits(hubble) == pytest.approx(3.0e122, rel=0.1)
    assert 1e122 < desitter_bits(hubble) < 1e123


def test_desitter_bits_grow_as_inverse_hubble_squared():
    assert desitter_bits(2.0e-18) == pytest.approx(4.0 * desitter_bits(4.0e-18))


@pytest.mark.parametrize("hubble", [0.0, -1.0, math.inf, -math.inf, math.nan])
def test_desitter_rejects_invalid_hubble(hubble):
    with pytest.raises(ValueError):
        desitter_horizon_radius(hubble)
    with pytest.raises(ValueError):
        desitter_bits(hubble)


# Landauer erasure ---------------------------------------------------------


def test_landauer_zero_temperature_costs_nothing():
    assert landauer_energy(0.0) == 0.0


def test_landauer_room_temperature_costs_about_2_9e21_joules():
    assert landauer_energy(300.0) == pytest.approx(2.871e-21, rel=1e-3)


def test_landauer_is_linear_in_temperature():
    assert landauer_energy(2.0) == pytest.approx(2.0 * landauer_energy(1.0))


def test_landauer_matches_kbt_ln2():
    from model import BOLTZMANN

    assert landauer_energy(7.5) == pytest.approx(BOLTZMANN * 7.5 * math.log(2.0))


@pytest.mark.parametrize("temperature", [-1.0, math.inf, -math.inf, math.nan])
def test_landauer_rejects_invalid_temperature(temperature):
    with pytest.raises(ValueError):
        landauer_energy(temperature)


# Two-mode squeezing -------------------------------------------------------


def test_zero_squeezing_is_the_vacuum():
    assert two_mode_squeezing_photon_number(0.0) == 0.0
    assert two_mode_mutual_information(0.0) == 0.0


def test_squeezing_photon_number_is_sinh_squared():
    for squeezing in (0.5, 1.0, 2.0):
        assert two_mode_squeezing_photon_number(squeezing) == pytest.approx(
            math.sinh(squeezing) ** 2
        )


def test_squeezing_is_symmetric_in_the_sign_of_r():
    for squeezing in (0.3, 1.0, 2.5):
        assert two_mode_squeezing_photon_number(-squeezing) == pytest.approx(
            two_mode_squeezing_photon_number(squeezing)
        )
        assert two_mode_mutual_information(-squeezing) == pytest.approx(
            two_mode_mutual_information(squeezing)
        )


def test_mutual_information_is_twice_the_marginal_entropy():
    for squeezing in (0.25, 0.5, 1.0, 2.0):
        photons = two_mode_squeezing_photon_number(squeezing)
        assert two_mode_mutual_information(squeezing) == pytest.approx(2.0 * _entropy_bits(photons))


def test_mutual_information_grows_with_squeezing():
    values = [two_mode_mutual_information(r) for r in (0.0, 0.25, 0.5, 1.0, 2.0)]
    assert values == sorted(values)
    assert values[0] == 0.0
    assert all(value > 0.0 for value in values[1:])


def test_mutual_information_matches_a_known_value():
    # n = sinh(1)**2 is about 1.3811, giving I about 4.674 bits.
    assert two_mode_mutual_information(1.0) == pytest.approx(4.674, rel=1e-3)


@pytest.mark.parametrize("squeezing", [math.inf, -math.inf, math.nan])
def test_squeezing_rejects_nonfinite_values(squeezing):
    with pytest.raises(ValueError):
        two_mode_squeezing_photon_number(squeezing)
    with pytest.raises(ValueError):
        two_mode_mutual_information(squeezing)


def test_squeezing_rejects_overflow():
    with pytest.raises(ValueError):
        two_mode_squeezing_photon_number(709.0)  # sinh is finite; its square is not
    with pytest.raises(ValueError):
        two_mode_squeezing_photon_number(1000.0)
    with pytest.raises(ValueError):
        two_mode_mutual_information(1000.0)


# Marginals ----------------------------------------------------------------


def test_bell_state_has_maximally_mixed_marginals():
    assert marginal_probabilities(BELL, subsystem=0) == pytest.approx((0.5, 0.5))
    assert marginal_probabilities(BELL, subsystem=1) == pytest.approx((0.5, 0.5))


def test_product_state_marginals_are_definite():
    state = (0j, 1j, 0j, 0j)
    assert marginal_probabilities(state, subsystem=0) == pytest.approx((1.0, 0.0))
    assert marginal_probabilities(state, subsystem=1) == pytest.approx((0.0, 1.0))


def test_marginals_normalize_an_unnormalized_state():
    assert marginal_probabilities((2j, 0j, 0j, 2j), subsystem=0) == pytest.approx((0.5, 0.5))


def test_marginals_sum_to_one():
    state = (1.0, 2.0j, 2.0, -1.0j)
    for subsystem in (0, 1):
        marginals = marginal_probabilities(state, subsystem=subsystem)
        assert sum(marginals) == pytest.approx(1.0)
        assert all(0.0 <= value <= 1.0 for value in marginals)


def test_rectangular_dimensions_work():
    state = (1.0,) * 6
    assert marginal_probabilities(state, subsystem=0, dimensions=(2, 3)) == pytest.approx(
        (0.5, 0.5)
    )
    assert marginal_probabilities(state, subsystem=1, dimensions=(2, 3)) == pytest.approx(
        (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
    )


def test_marginals_reject_bad_dimensions():
    for dimensions in [(2,), (2, 2, 2), (0, 2), (-1, 2), (2.0, 2), (True, 2)]:
        with pytest.raises(ValueError):
            marginal_probabilities(BELL, dimensions=dimensions)  # type: ignore[arg-type]


def test_marginals_reject_wrong_length():
    with pytest.raises(ValueError):
        marginal_probabilities((1.0, 0.0, 0.0), dimensions=(2, 2))


def test_marginals_reject_bad_subsystem():
    with pytest.raises(ValueError):
        marginal_probabilities(BELL, subsystem=2)


def test_marginals_reject_zero_norm():
    with pytest.raises(ValueError):
        marginal_probabilities((0j, 0j, 0j, 0j))


@pytest.mark.parametrize("bad", [complex(math.inf, 0), complex(math.nan, 0), complex(0, math.nan)])
def test_marginals_reject_nonfinite_amplitudes(bad):
    with pytest.raises(ValueError):
        marginal_probabilities((bad, 0j, 0j, 0j))


# Local unitaries ----------------------------------------------------------


def test_identity_unitary_preserves_the_state():
    assert apply_local_unitary(BELL, IDENTITY_2, subsystem=0) == pytest.approx(BELL)


def test_local_unitary_preserves_the_norm():
    result = apply_local_unitary(BELL, Y_GATE, subsystem=0)
    assert sum(abs(value) ** 2 for value in result) == pytest.approx(1.0)


def test_pauli_x_permutes_the_bell_state_on_either_side():
    assert apply_local_unitary(BELL, X_GATE, subsystem=0) == pytest.approx(
        (0j, SQRT_HALF, SQRT_HALF, 0j)
    )
    assert apply_local_unitary(BELL, X_GATE, subsystem=1) == pytest.approx(
        (0j, SQRT_HALF, SQRT_HALF, 0j)
    )


def test_pauli_z_on_alice_flips_the_relative_phase():
    result = apply_local_unitary(BELL, Z_GATE, subsystem=0)
    assert result == pytest.approx((SQRT_HALF, 0j, 0j, -SQRT_HALF))


def test_local_unitary_squares_back_to_the_identity():
    once = apply_local_unitary(BELL, Y_GATE, subsystem=0)
    twice = apply_local_unitary(once, Y_GATE, subsystem=0)
    assert twice == pytest.approx(BELL)


def test_unitary_on_the_right_subsystem_of_a_rectangular_state():
    state = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    swap = ((0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
    result = apply_local_unitary(state, swap, subsystem=1, dimensions=(2, 3))
    assert result == pytest.approx((0j, 1.0, 0j, 0j, 0j, 0j))


def test_local_unitary_leaves_zero_coefficients_alone():
    state = (1.0, 0.0, 0.0, 0.0)
    assert apply_local_unitary(state, X_GATE, subsystem=0) == pytest.approx((0j, 0j, 1.0, 0.0))


def test_local_unitary_rejects_wrong_matrix_shape():
    with pytest.raises(ValueError):
        apply_local_unitary(BELL, ((1j, 0j),), subsystem=0)
    with pytest.raises(ValueError):
        apply_local_unitary(BELL, ((1j, 0j), (0j, 1j), (0j, 0j)), subsystem=0)
    with pytest.raises(ValueError):
        apply_local_unitary(BELL, ((1j, 0j), (0j,)), subsystem=0)


def test_local_unitary_rejects_bad_subsystem():
    with pytest.raises(ValueError):
        apply_local_unitary(BELL, X_GATE, subsystem=-1)


def test_local_unitary_rejects_wrong_state_length():
    with pytest.raises(ValueError):
        apply_local_unitary((1.0, 0.0, 0.0), X_GATE, subsystem=0)


def test_local_unitary_rejects_bad_dimensions():
    with pytest.raises(ValueError):
        apply_local_unitary(BELL, X_GATE, subsystem=0, dimensions=(2, 0))


def test_local_unitary_rejects_nonfinite_state():
    with pytest.raises(ValueError):
        apply_local_unitary((complex(math.inf, 0), 0j, 0j, 0j), X_GATE)


def test_local_unitary_rejects_nonfinite_matrix():
    with pytest.raises(ValueError):
        apply_local_unitary(BELL, ((complex(math.nan, 0), 0j), (0j, 1j)))


# No-signaling -------------------------------------------------------------


@pytest.mark.parametrize("gate", [X_GATE, Z_GATE, Y_GATE])
def test_alice_cannot_change_bobs_marginal(gate):
    before = marginal_probabilities(BELL, subsystem=1)
    after = marginal_probabilities(apply_local_unitary(BELL, gate, subsystem=0), subsystem=1)
    assert after == pytest.approx(before)


@pytest.mark.parametrize("gate", [X_GATE, Z_GATE, Y_GATE])
def test_bob_cannot_change_alices_marginal(gate):
    before = marginal_probabilities(BELL, subsystem=0)
    after = marginal_probabilities(apply_local_unitary(BELL, gate, subsystem=1), subsystem=0)
    assert after == pytest.approx(before)


def test_no_signaling_holds_for_a_partial_entangled_state():
    state = (math.sqrt(0.7), 0j, 0j, math.sqrt(0.3))
    before = marginal_probabilities(state, subsystem=1)
    for gate in (X_GATE, Z_GATE, Y_GATE):
        after = marginal_probabilities(apply_local_unitary(state, gate, subsystem=0), subsystem=1)
        assert after == pytest.approx(before)


def test_no_signaling_does_not_mean_no_correlation():
    # Local operations move the joint state even though they cannot move a marginal.
    original = marginal_probabilities(BELL, subsystem=0)
    rotated = apply_local_unitary(BELL, X_GATE, subsystem=0)
    assert original == pytest.approx(marginal_probabilities(rotated, subsystem=0))
    # The Bell state is X-invariant, so use Z for the joint-change check.
    phased = apply_local_unitary(BELL, Z_GATE, subsystem=0)
    assert phased != pytest.approx(BELL)
